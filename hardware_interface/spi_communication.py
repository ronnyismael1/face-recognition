import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI port 0, device (CS) 0
spi.max_speed_hz = 1000000  # Set speed (1 MHz)

try:
    for byte in range(256):  # Send bytes 0x00 to 0xFF
        response = spi.xfer2([byte])
        print(f"Sent: {byte}, Received: {response[0]}")
        if byte != response[0]:
            print(f"Mismatch at {byte}!")
        time.sleep(0.1)  # Short delay
finally:
    spi.close()  # Ensure SPI is closed on error or normal completion