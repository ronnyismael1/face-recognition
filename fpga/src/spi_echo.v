`timescale 1ns / 1ps

module spi_echo(
    input clk,
    input i_mosi,
    input i_sclk,
    input i_ss,
    output reg o_miso
    );

reg [7:0] shift_reg;
always @(posedge i_sclk or posedge i_ss) begin
    if (i_ss) begin
        // Reset the shift register on chip select
        shift_reg <= 8'd0;
    end else begin
        // Shift in from MOSI, shift out to MISO
        shift_reg <= (shift_reg << 1) | i_mosi;
        o_miso <= shift_reg[7]; // Echo the most significant bit
    end
end    

endmodule
