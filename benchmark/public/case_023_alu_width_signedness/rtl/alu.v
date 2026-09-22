module alu(input wire [7:0] a, b, input wire [2:0] op, output reg [7:0] result);
always @* begin
    result = 8'd0;
    case (op)
        3'd0: result = a + b;
        3'd1: result = a - b;
        3'd2: result = a & b;
        3'd3: result = a | b;
        3'd4: result = a ^ b;
        3'd5: result = a << b[2:0];
        3'd6: result = {7'd0, (a < b)};
        default: result = a;
    endcase
end
endmodule
