module controller_tb;
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
