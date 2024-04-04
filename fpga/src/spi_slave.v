`timescale 1ns / 1ps

module spi_slave(
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

// Internal registers
reg[7:0] data_received;
reg[7:0] data_to_send;
reg[2:0] bit_count;

always @ (posedge i_sclk or posedge i_ss)
begin
    if (i_ss)
    begin
        bit_count <= 0; // If CS goes high again we reset
    end else begin
        // SPI communication logic
        if (bit_count < 8)
        begin
            // Receive data on MOSI
            data_received <= (data_received << 1) | i_mosi;
            // Prepare data to send back on MISO
            // o_miso <= data_to_send[7 - bit_count]; // Example for sending data back
            bit_count <= bit_count + 1;
        end
    end
end

// TO-DO: Other logic stuff

endmodule
