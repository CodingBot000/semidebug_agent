#!/usr/bin/env python3
"""Original RTL + reference testbenches. Gold is verified BEFORE mutations are emitted.
This module is evaluator-only and must never be imported by the repair agent.
"""

import json
import shutil
from pathlib import Path

from semidebug.benchmark.loader import load_case
from semidebug.tools.validation import regress, validate

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = {}
DESIGNS["counter"] = (
    """module counter(input wire clk, rst, en, output reg [3:0] count);
always @(posedge clk) begin
    if (rst) count <= 4'd0;
    else if (en) begin
        if (count == 4'd9) count <= 4'd0;
        else count <= count + 4'd1;
    end
end
endmodule
""",
    """module counter_tb;
reg clk=0, rst=1, en=0;
wire [3:0] count;
integer i, expected=0, seed=7, dummy, cycles=40;
counter dut(clk,rst,en,count);
task step;
begin
    #1; clk=1;
    if (rst) expected=0;
    else if (en) begin
        if (expected==9) expected=0; else expected=expected+1;
    end
    #1;
    if (count !== expected[3:0]) $fatal(1,"counter cycle=%0d expected=%0d actual=%0d",i,expected,count);
    clk=0; #1;
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if ($test$plusargs("REGRESSION")) cycles=250;
    step; rst=0; en=1;
    for(i=0;i<25;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin
        en=($random(seed)&3)!=0; rst=(i%37==19); step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("syntax", "count + 4'd1;", "count + 4'd1"),
        ("reset", "if (rst)", "if (!rst)"),
        ("boundary", "count == 4'd9", "count == 4'd8"),
        ("sequential", "else if (en)", "else if (!en)"),
        ("width_signedness", "reg [3:0] count", "reg [2:0] count"),
    ],
)
DESIGNS["fifo"] = (
    """module fifo(input wire clk, rst, wr_en, rd_en, input wire [7:0] data_in,
            output reg [7:0] data_out, output wire full, empty);
reg [7:0] mem [0:3];
reg [1:0] wr_ptr, rd_ptr;
reg [2:0] count;
wire push = wr_en && !full;
wire pop = rd_en && !empty;
assign full = (count == 3'd4);
assign empty = (count == 3'd0);
always @(posedge clk) begin
    if (rst) begin
        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd0; data_out <= 8'd0;
    end else begin
        if (push) begin mem[wr_ptr] <= data_in; wr_ptr <= wr_ptr + 2'd1; end
        if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
        case ({push,pop})
            2'b10: count <= count + 3'd1;
            2'b01: count <= count - 3'd1;
            default: count <= count;
        endcase
    end
end
endmodule
""",
    """module fifo_tb;
reg clk=0,rst=1,wr_en=0,rd_en=0;
reg [7:0] data_in=0;
wire [7:0] data_out;
wire full,empty;
reg [7:0] queue[0:1023];
reg [7:0] expected_out=0;
integer head=0,tail=0,n=0,i=0,seed=7,dummy,cycles=50;
reg push,pop;
fifo dut(clk,rst,wr_en,rd_en,data_in,data_out,full,empty);
task step;
begin
    push=wr_en && n<4; pop=rd_en && n>0;
    #1; clk=1;
    if(rst) begin head=0; tail=0; n=0; expected_out=0; end
    else begin
        if(pop) begin expected_out=queue[head]; head=head+1; end
        if(push) begin queue[tail]=data_in; tail=tail+1; end
        n=n+push-pop;
    end
    #1;
    if(full !== (n==4) || empty !== (n==0) || data_out !== expected_out)
        $fatal(1,"FIFO step=%0d occupancy=%0d full=%b empty=%b expected_out=%0d actual=%0d",i,n,full,empty,expected_out,data_out);
    clk=0; #1;
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if($test$plusargs("REGRESSION")) cycles=400;
    step; rst=0; wr_en=1;
    for(i=0;i<6;i=i+1) begin data_in=i+8'd11; step; end
    wr_en=0; rd_en=1;
    for(i=0;i<6;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin
        wr_en=$random(seed); rd_en=$random(seed); data_in=$random(seed);
        rst=(i%71==70); step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("boundary", "count == 3'd4", "count == 3'd3"),
        ("connectivity", "mem[rd_ptr]", "mem[wr_ptr]"),
        ("sequential", "wr_en && !full", "wr_en && full"),
        ("reset", "count <= 3'd0; data_out", "count <= 3'd1; data_out"),
        ("boundary", "count - 3'd1", "count + 3'd1"),
    ],
)
DESIGNS["arbiter"] = (
    """module arbiter(input wire clk, rst, input wire [1:0] req, output reg [1:0] grant);
reg priority_bit;
always @* begin
    grant = 2'b00;
    case (req)
        2'b01: grant = 2'b01;
        2'b10: grant = 2'b10;
        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
        default: grant = 2'b00;
    endcase
end
always @(posedge clk) begin
    if (rst) priority_bit <= 1'b0;
    else if (grant[0]) priority_bit <= 1'b1;
    else if (grant[1]) priority_bit <= 1'b0;
end
endmodule
""",
    """module arbiter_tb;
reg clk=0,rst=1;
reg [1:0] req=0;
wire [1:0] grant;
reg priority_ref=0;
reg [1:0] expected;
integer i=0,seed=7,dummy,cycles=50;
arbiter dut(clk,rst,req,grant);
task check_grant;
begin
    case(req)
        0: expected=0;
        1: expected=1;
        2: expected=2;
        3: expected=priority_ref ? 2 : 1;
    endcase
    if(grant !== expected) $fatal(1,"arbiter req=%b priority=%b expected=%b got=%b",req,priority_ref,expected,grant);
end
endtask
task step;
begin
    #1; check_grant; clk=1;
    if(rst) priority_ref=0;
    else if(expected==1) priority_ref=1;
    else if(expected==2) priority_ref=0;
    #1; check_grant; clk=0; #1;
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if($test$plusargs("REGRESSION")) cycles=300;
    #1; clk=1; #1; clk=0; rst=0;
    req=3; for(i=0;i<10;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin req=$random(seed); rst=(i%31==30); step; end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("connectivity", "2'b01: grant = 2'b01", "2'b01: grant = 2'b10"),
        (
            "sequential",
            "else if (grant[0]) priority_bit <= 1'b1",
            "else if (grant[0]) priority_bit <= 1'b0",
        ),
        ("reset", "if (rst) priority_bit <= 1'b0", "if (rst) priority_bit <= 1'b1"),
        ("combinational", "priority_bit ? 2'b10 : 2'b01", "priority_bit ? 2'b01 : 2'b10"),
        ("combinational", "default: grant = 2'b00", "default: grant = 2'b01"),
    ],
)
DESIGNS["controller"] = (
    """module controller(input wire clk, rst, start, finish, output wire busy, done);
reg [1:0] state;
assign busy = (state == 2'd1);
assign done = (state == 2'd2);
always @(posedge clk) begin
    if (rst) state <= 2'd0;
    else case (state)
        2'd0: if (start) state <= 2'd1;
        2'd1: if (finish) state <= 2'd2;
        2'd2: state <= 2'd0;
        default: state <= 2'd0;
    endcase
end
endmodule
""",
    """module controller_tb;
reg clk=0,rst=1,start=0,finish=0;
wire busy,done;
integer refstate=0,i=0,seed=7,dummy,cycles=60;
controller dut(clk,rst,start,finish,busy,done);
task step;
begin
    #1; clk=1;
    if(rst) refstate=0;
    else case(refstate)
        0: if(start) refstate=1;
        1: if(finish) refstate=2;
        2: refstate=0;
    endcase
    #1;
    if(busy !== (refstate==1) || done !== (refstate==2))
        $fatal(1,"FSM state=%0d busy=%b done=%b",refstate,busy,done);
    clk=0; #1;
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if($test$plusargs("REGRESSION")) cycles=300;
    step; rst=0; start=1; step; start=0; finish=1; step; finish=0; step;
    for(i=0;i<cycles;i=i+1) begin
        start=$random(seed); finish=$random(seed); rst=(i%43==42); step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("fsm", "if (start) state <= 2'd1", "if (!start) state <= 2'd1"),
        ("fsm", "if (finish) state <= 2'd2", "if (finish) state <= 2'd0"),
        ("reset", "if (rst) state <= 2'd0", "if (rst) state <= 2'd1"),
        ("combinational", "assign done = (state == 2'd2)", "assign done = (state == 2'd1)"),
        ("fsm", "2'd2: state <= 2'd0", "2'd2: state <= 2'd1"),
    ],
)
DESIGNS["alu"] = (
    """module alu(input wire [7:0] a, b, input wire [2:0] op, output reg [7:0] result);
always @* begin
    result = 8'd0;
    case (op)
        3'd0: result = a + b;
        3'd1: result = a - b;
        3'd2: result = a & b;
        3'd3: result = a | b;
        3'd4: result = a ^ b;
        3'd5: result = a << b[2:0];
        3'd6: result = {7'd0, ($signed(a) < $signed(b))};
        default: result = a;
    endcase
end
endmodule
""",
    """module alu_tb;
reg [7:0] a=0,b=0;
reg [2:0] op=0;
wire [7:0] result;
reg [7:0] expected;
integer i,j,seed=7,dummy,cycles=40,sa,sb;
alu dut(a,b,op,result);
task check;
begin
    sa=a; sb=b;
    if(a[7]) sa=sa-256;
    if(b[7]) sb=sb-256;
    case(op)
        0: expected=a+b;
        1: expected=a-b;
        2: expected=a&b;
        3: expected=a|b;
        4: expected=a^b;
        5: expected=a << b[2:0];
        6: expected=(sa<sb);
        7: expected=a;
    endcase
    #1;
    if(result !== expected) $fatal(1,"ALU op=%0d a=%0d b=%0d expected=%0d actual=%0d",op,a,b,expected,result);
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if($test$plusargs("REGRESSION")) cycles=300;
    for(i=0;i<cycles;i=i+1) begin
        a=$random(seed); b=$random(seed);
        for(j=0;j<8;j=j+1) begin op=j; check; end
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("combinational", "result = a + b", "result = a - b"),
        ("connectivity", "result = a - b", "result = b - a"),
        ("width_signedness", "$signed(a) < $signed(b)", "a < b"),
        ("combinational", "result = a << b[2:0]", "result = a >> b[2:0]"),
        ("syntax", "result = a ^ b;", "result = a ^ nonexistent;"),
    ],
)
DESIGNS["pulse"] = (
    """module pulse(input wire clk, rst, signal_in, enable, output reg pulse_out);
reg previous;
always @(posedge clk) begin
    if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
    else begin
        previous <= signal_in;
        pulse_out <= enable && signal_in && !previous;
    end
end
endmodule
""",
    """module pulse_tb;
reg clk=0,rst=1,signal_in=0,enable=0;
wire pulse_out;
reg previous_ref=0,expected=0;
integer i=0,seed=7,dummy,cycles=60;
pulse dut(clk,rst,signal_in,enable,pulse_out);
task step;
begin
    #1; clk=1;
    if(rst) begin previous_ref=0; expected=0; end
    else begin expected=enable && signal_in && !previous_ref; previous_ref=signal_in; end
    #1;
    if(pulse_out !== expected) $fatal(1,"pulse signal=%b enable=%b expected=%b actual=%b",signal_in,enable,expected,pulse_out);
    clk=0; #1;
end
endtask
initial begin
    dummy=$value$plusargs("SEED=%d",seed);
    if($test$plusargs("REGRESSION")) cycles=300;
    step; rst=0; enable=1; signal_in=1; step; step; signal_in=0; step;
    for(i=0;i<cycles;i=i+1) begin
        signal_in=$random(seed); enable=$random(seed); rst=(i%47==46); step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
""",
    [
        ("sequential", "previous <= signal_in", "previous = signal_in"),
        ("combinational", "signal_in && !previous", "signal_in && previous"),
        ("sequential", "enable && signal_in", "!enable && signal_in"),
        ("reset", "pulse_out <= 1'b0", "pulse_out <= 1'b1"),
        ("connectivity", "previous <= signal_in", "previous <= enable"),
    ],
)


def write_case(path, name, code, testbench, case_id, category):
    for d in ["rtl", "tb", "expected"]:
        (path / d).mkdir(parents=True, exist_ok=True)
    (path / "rtl" / f"{name}.v").write_text(code)
    (path / "tb" / f"{name}_tb.v").write_text(testbench)
    (path / "expected/metadata.json").write_text(
        json.dumps({"completion_marker": "SEMIDEBUG_PASS"}, indent=2) + "\n"
    )
    case = {
        "id": case_id,
        "category": category,
        "design_top": name,
        "mutable": [f"rtl/{name}.v"],
        "immutable": [f"tb/{name}_tb.v", "expected/metadata.json"],
        "target": {
            "name": "target",
            "top": f"{name}_tb",
            "sources": [f"tb/{name}_tb.v"],
            "plusargs": ["+SEED=7"],
        },
        "regression": [
            {
                "name": f"regression_{seed}",
                "top": f"{name}_tb",
                "sources": [f"tb/{name}_tb.v"],
                "plusargs": ["+REGRESSION", f"+SEED={seed}"],
            }
            for seed in [17, 103]
        ],
        "timeout_sec": 10,
    }
    (path / "case.json").write_text(json.dumps(case, indent=2) + "\n")


def main():
    audit = {"measurement": "dataset-validation-not-ai-repair", "gold": [], "mutations": []}
    for name, (code, tb, _) in DESIGNS.items():
        root = ROOT / "evaluator/gold" / name
        write_case(root, name, code, tb, f"gold_{name}", "gold")
        case = load_case(root)
        target = validate(root, case)
        regression = regress(root, case)
        audit["gold"].append(
            {"design": name, "target": target.model_dump(), "regression": regression.model_dump()}
        )
        if not target.passed or not regression.passed:
            (ROOT / "results/dataset_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
            raise SystemExit(f"Gold failed: {name}")
        print(f"GOLD PASS {name}", flush=True)
    manifest = []
    number = 0
    for name, (code, tb, mutations) in DESIGNS.items():
        for index, (category, before, after) in enumerate(mutations):
            number += 1
            if code.count(before) != 1:
                raise ValueError(f"Mutation not unique: {name} {before}")
            split = "public" if index < 4 else "hidden"
            case_id = f"case_{number:03d}_{name}_{category}"
            root = ROOT / "benchmark" / split / case_id
            write_case(root, name, code.replace(before, after), tb, case_id, category)
            case = load_case(root)
            bundle = validate(root, case)
            audit["mutations"].append(
                {
                    "case_id": case_id,
                    "split": split,
                    "category": category,
                    "baseline": bundle.model_dump(),
                }
            )
            if bundle.passed or bundle.infrastructure_error:
                raise SystemExit(f"Broken mutation invalid: {case_id}")
            manifest.append(
                {
                    "id": case_id,
                    "path": f"{split}/{case_id}",
                    "category": category,
                    "split": split,
                    "design": name,
                }
            )
            print(f"BROKEN VERIFIED {case_id}", flush=True)
    (ROOT / "benchmark/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (ROOT / "results/dataset_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    demo = ROOT / "examples/fifo_off_by_one"
    if demo.exists():
        shutil.rmtree(demo)
    shutil.copytree(
        ROOT / "benchmark/public/case_006_fifo_boundary",
        demo,
        ignore=shutil.ignore_patterns(".build"),
    )
    print(f"Verified {len(audit['gold'])} gold designs and {len(manifest)} failing mutations.")


if __name__ == "__main__":
    main()
