`timescale 1ns / 1ps

module spi_slave_tb;

reg clk = 0;
reg i_mosi = 0;
reg i_sclk = 0;
reg i_ss = 1; // Start with chip select not active
wire o_miso;

// Instance of spi_slave module
spi_slave uut (
    .clk(clk),
    .i_mosi(i_mosi),
    .i_sclk(i_sclk),
    .i_ss(i_ss),
    .o_miso(o_miso)
);

// Clock generation
always #10 clk = ~clk; // Generate a clock with a period of 20ns

// SPI communication simulation
initial begin
    // Initialize SPI lines
    i_ss = 1;
    #100; // Wait for some time
    i_ss = 0; // Activate chip select

    // Simulate sending a byte over SPI
    send_byte(8'b10101010); // Example byte

    #100; // Wait for some time
    i_ss = 1; // Deactivate chip select
end

// Function to simulate sending a byte over SPI
task send_byte;
    input [7:0] byte;
    integer i;
    begin
        for (i=0; i<8; i=i+1) begin
            i_mosi = byte[7-i];
            #20; // Half-period for clock to change state
            i_sclk = 1;
            #20; // Another half-period
            i_sclk = 0;
        end
    end
endtask

endmodule
