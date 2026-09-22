module controller(input wire clk, rst, start, finish, output wire busy, done);
reg [1:0] state;
assign busy = (state == 2'd1);
assign done = (state == 2'd1);
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
