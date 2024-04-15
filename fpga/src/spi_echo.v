module spi_echo(
    input clk,       // System clock
    input SCK,       // SPI Clock
    input MOSI,      // Master Out Slave In
    input SSEL,      // Slave Select (active low)
    output reg MISO, // Master In Slave Out
    output reg LED   // Debug LED
);

// Sync SPI signals to the FPGA clock
reg [2:0] SCKr;  always @(posedge clk) SCKr <= {SCKr[1:0], SCK};
wire SCK_risingedge = (SCKr[2:1] == 2'b01);  // Detect SCK rising edges
wire SCK_fallingedge = (SCKr[2:1] == 2'b10);  // Detect SCK falling edges

reg [2:0] SSELr;  always @(posedge clk) SSELr <= {SSELr[1:0], SSEL};
wire SSEL_active = ~SSELr[1];  // SSEL is active low
wire SSEL_startmessage = (SSELr[2:1] == 2'b10);  // Message starts at falling edge
wire SSEL_endmessage = (SSELr[2:1] == 2'b01);  // Message stops at rising edge

reg [1:0] MOSIr;  always @(posedge clk) MOSIr <= {MOSIr[0], MOSI};
wire MOSI_data = MOSIr[1];  // Synchronized MOSI data

// Receiving data from SPI
reg [2:0] bitcnt;
reg byte_received;  // High when a byte has been received
reg [7:0] byte_data_received;

always @(posedge clk) begin
    if(~SSEL_active)
        bitcnt <= 3'b000;
    else if(SCK_risingedge) begin
        bitcnt <= bitcnt + 3'b001;
        byte_data_received <= {byte_data_received[6:0], MOSI_data};  // Shift-left register
    end
end

always @(posedge clk)
    byte_received <= SSEL_active && SCK_risingedge && (bitcnt == 3'b111);

// Use LSB of the data received to control the LED
always @(posedge clk) 
    if(byte_received) LED <= byte_data_received[0];

// Transmitting data back to master
reg [7:0] byte_data_sent;
reg [7:0] cnt;  // Count messages
always @(posedge clk) 
    if(SSEL_startmessage) cnt <= cnt + 8'h1;

always @(posedge clk)
if(SSEL_active) begin
    if(SSEL_startmessage)
        byte_data_sent <= cnt;  // First byte is the message count
    else if(SCK_fallingedge) begin
        if(bitcnt == 3'b000)
            byte_data_sent <= 8'h00;  // Send 0s after the first byte
        else
            byte_data_sent <= {byte_data_sent[6:0], 1'b0};
    end
end

// Assign MSB of byte_data_sent to MISO
always @(posedge clk) begin
    if (SSEL_active) begin
        MISO <= byte_data_sent[7]; // send MSB first
    end else begin
        MISO <= 1'bZ; // Optional: drive MISO to high impedance when not active
    end
end

endmodule