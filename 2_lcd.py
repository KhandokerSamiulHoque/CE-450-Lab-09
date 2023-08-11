import time
import smbus2 as smbus

I2C_BUS = smbus.SMBus(1)

def write_data(addr, data):
    global ENABLE_BIT
    temp = data
    if ENABLE_BIT == 1:
        temp |= 0x08
    else:
        temp &= 0xF7
    I2C_BUS.write_byte(addr, temp)

def send_instruction(instr):
    # Send high 4 bits first
    buffer = instr & 0xF0
    buffer |= 0x04
    write_data(LCD_ADDRESS, buffer)
    time.sleep(0.002)
    buffer &= 0xFB
    write_data(LCD_ADDRESS, buffer)

    # Send low 4 bits next
    buffer = (instr & 0x0F) << 4
    buffer |= 0x04
    write_data(LCD_ADDRESS, buffer)
    time.sleep(0.002)
    buffer &= 0xFB
    write_data(LCD_ADDRESS, buffer)

def send_text(text):
    for char in text:
        # Send high 4 bits of character
        buffer = ord(char) & 0xF0
        buffer |= 0x05
        write_data(LCD_ADDRESS, buffer)
        time.sleep(0.002)
        buffer &= 0xFB
        write_data(LCD_ADDRESS, buffer)

        # Send low 4 bits of character
        buffer = (ord(char) & 0x0F) << 4
        buffer |= 0x05
        write_data(LCD_ADDRESS, buffer)
        time.sleep(0.002)
        buffer &= 0xFB
        write_data(LCD_ADDRESS, buffer)

def initialize_lcd(addr, enable_bit):
    global LCD_ADDRESS
    global ENABLE_BIT
    LCD_ADDRESS = addr
    ENABLE_BIT = enable_bit
    try:
        send_instruction(0x33)
        time.sleep(0.005)
        send_instruction(0x32)
        time.sleep(0.005)
        send_instruction(0x28)
        time.sleep(0.005)
        send_instruction(0x0C)
        time.sleep(0.005)
        send_instruction(0x01)
        I2C_BUS.write_byte(LCD_ADDRESS, 0x08)
    except:
        return False
    else:
        return True

def clear_screen():
    send_instruction(0x01)

def turn_on_backlight():
    I2C_BUS.write_byte(0x27, 0x08)
    I2C_BUS.close()

def display_text(p, q, text):
    if p < 0:
        p = 0
    if p > 15:
        p = 15
    if q < 0:
        q = 0
    if q > 1:
        q = 1

    # Move cursor
    address = 0x80 + 0x40 * q + p
    send_instruction(address)

    send_text(text)

if __name__ == '__main__':
    initialize_lcd(0x27, 1)
    display_text(6, 0, 'Hello')
    display_text(8, 1, 'world!')