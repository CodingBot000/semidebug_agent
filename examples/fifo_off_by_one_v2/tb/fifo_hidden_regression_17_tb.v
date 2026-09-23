// SEMIDEBUG_HIDDEN_REGRESSION_17_MARKER
module fifo_hidden_regression_17_tb;
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
    cycles=400;
    step; rst=0; wr_en=1;
    for(i=0;i<6;i=i+1) begin data_in=i+8'd11; step; end
    wr_en=0; rd_en=1;
    for(i=0;i<6;i=i+1) step;
    for(i=0;i<cycles;i=i+1) begin
        wr_en=$random(seed); rd_en=$random(seed); data_in=$random(seed);
        rst=(i%71==70); step;
    end
    rst=1; wr_en=0; rd_en=0; step; rst=0;
    for(i=0;i<16;i=i+1) begin
        wr_en=1; rd_en=0; data_in=i; step;
        wr_en=0; rd_en=1; step;
    end
    $display("SEMIDEBUG_PASS"); $finish;
end
endmodule
