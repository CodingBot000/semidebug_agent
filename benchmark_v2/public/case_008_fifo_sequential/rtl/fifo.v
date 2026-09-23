module fifo(input wire clk, rst, wr_en, rd_en, input wire [7:0] data_in,
            output reg [7:0] data_out, output wire full, empty);
reg [7:0] mem [0:3];
reg [1:0] wr_ptr, rd_ptr;
reg [2:0] count;
wire push = wr_en && full;
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
