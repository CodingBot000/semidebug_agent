module alu_tb;
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
