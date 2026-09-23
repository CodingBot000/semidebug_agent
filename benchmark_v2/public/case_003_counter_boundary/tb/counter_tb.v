module counter_tb;
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

    step; rst=0; en=1;
    for(i=0;i<25;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin
        en=($random(seed)&3)!=0; rst=(i%37==19); step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
