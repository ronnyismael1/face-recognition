`timescale 1ns / 1ps

module spi_slave
    #(parameter SPI_MODE=0)
    (
    input clk, // System clock
    input i_mosi, // Master out, slave in
    input i_sclk, // SPI Clock
    input i_ss, // Chip select
    output reg o_miso // Master in, slave out
    );
/*
SPI mode 0
  CPOL = 0, Idle high
  CPHA = 0, Data sampled on leading edge
*/

endmodule
