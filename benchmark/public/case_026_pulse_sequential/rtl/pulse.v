module pulse(input wire clk, rst, signal_in, enable, output reg pulse_out);
reg previous;
always @(posedge clk) begin
    if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
    else begin
        previous = signal_in;
        pulse_out <= enable && signal_in && !previous;
    end
end
endmodule
