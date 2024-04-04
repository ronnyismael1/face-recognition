`timescale 1ns / 1ps

module top(
    input clk,
    input i_mosi,
    input i_sclk,
    input i_ss,
    output reg o_miso
    ); 
    
// Instantiate module 
spi_slave mySPI(
    .i_mosi(i_mosi),
    .i_sclk(i_sclk),
    .i_ss(i_ss),
    .o_miso(o_miso)
);

endmodule
