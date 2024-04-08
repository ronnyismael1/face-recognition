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
reg[2:0] bit_count;

// Data processing buffer and ready signal
reg [31:0] data_buffer = 0; // Adjust size based on data structure
reg [1:0] byte_count = 0; // Counts up to 4 for a 32-bit number
wire data_ready; // Indicates when a full number is ready

assign data_ready = (byte_count == 4); // Adjust condition based on data structure size

always @ (posedge i_sclk or posedge i_ss)
begin
    if (i_ss)
    begin
        bit_count <= 0;
        byte_count <= 0;
        data_buffer <= 0;
    end else begin
        // SPI communication logic
        if (bit_count < 8)
        begin
            // Receive data on MOSI by shifting and or-ing
            // ex: 0101 -> 1010 -> 1011
            data_received <= (data_received << 1) | i_mosi;
            // Prepare data to send back on MISO
            bit_count <= bit_count + 1;
        end
        if (bit_count == 7)
        begin
            // Once byte is full we shift it into the data buffer
            data_buffer <= (data_buffer << 8) | data_received;
            byte_count <= byte_count + 1;
            bit_count <= 0; // Reset bit counter for next byte
        end
    end
end

// TO-DO: Implement logic to use data_buffer once data_ready is high

endmodule
