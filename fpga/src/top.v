`timescale 1ns / 1ps

module top(
    input CLK12MHZ,
    input ck_io11_mosi,
    input ck_io13_sck,
    input ck_io10_ss,
    output ck_io12_miso,
    output led0
    ); 
    
    
// Instantiate echo 
spi_echo echo(
    .clk(CLK12MHZ),
    .MOSI(ck_io11_mosi),
    .SCK(ck_io13_sck),
    .SSEL(ck_io10_ss),
    .MISO(ck_io12_miso),
    .LED(led0)
);

endmodule
