module arbiter_tb;
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

    #1; clk=1; #1; clk=0; rst=0;
    req=3; for(i=0;i<10;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin req=$random(seed); rst=(i%31==30); step; end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
