module arbiter(input wire clk, rst, input wire [1:0] req, output reg [1:0] grant);
reg priority_bit;
always @* begin
    grant = 2'b00;
    case (req)
        2'b01: grant = 2'b01;
        2'b10: grant = 2'b10;
        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
        default: grant = 2'b00;
    endcase
end
always @(posedge clk) begin
    if (rst) priority_bit <= 1'b0;
    else if (grant[0]) priority_bit <= 1'b1;
    else if (grant[1]) priority_bit <= 1'b0;
end
endmodule
