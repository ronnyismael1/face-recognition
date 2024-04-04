import spidev

# Open SPI bus
spi = spidev.SpiDev()
spi_bus_number = 0
spi_device_number = 0
spi.open(spi_bus_number, spi_device_number)

# Set SPI speed and mode
spi_max_speed = 1e6  # 1MHz clock speed
spi.mode = 0  # SPI mode based on CPOL and CPHA

# Configure SPI
spi.bits_per_word = 8  # word size