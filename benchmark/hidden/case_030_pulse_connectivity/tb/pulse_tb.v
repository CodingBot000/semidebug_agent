module pulse_tb;
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
