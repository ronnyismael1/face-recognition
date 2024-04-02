import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi_bus_number = 0  # Adjust as necessary
spi_device_number = 0  # Adjust as necessary
spi.open(spi_bus_number, spi_device_number)

# Set SPI speed and mode
spi_max_speed = 1e6  # 1MHz, adjust this to ensure both devices support this speed
spi.mode = 0  # Adjust if a different SPI mode is required

# Configure SPI
spi.bits_per_word = 8  # word size