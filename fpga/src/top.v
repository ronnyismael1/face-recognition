`timescale 1ns / 1ps

module top(
    input clk,
    input ck_io11_mosi,
    input ck_io13_sck,
    input ck_io10_ss,
    output ck_io12_miso
    ); 
    
    
// Instantiate echo 
spi_echo echo(
    .clk(clk),
    .i_mosi(ck_io11_mosi),
    .i_sclk(ck_io13_sck),
    .i_ss(ck_io10_ss),
    .o_miso(ck_io12_miso)
);
    
//// Instantiate module 
//spi_slave mySPI(
//    .clk(clk),
//    .i_mosi(i_mosi),
//    .i_sclk(i_sclk),
//    .i_ss(i_ss),
//    .o_miso(o_miso)
//);

endmodule
