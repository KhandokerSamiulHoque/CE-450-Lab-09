from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import version_info
import time

if version_info.major == 3:
    initial_input = input
def disp_text():
    print ("========================================")
    print ("|                LCD1602               |")
    print ("|    ------------------------------    |")
    print ("|         GND connect to PIN 6         |")
    print ("|         VCC connect to PIN 2         |")
    print ("|         SDA connect to PIN 3         |")
    print ("|         SCL connect to PIN 5         |")
    print ("========================================\n")


    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    initial_input ("Press Enter to start\n")

lcd = LCD()
def exit_point(signum, frame):
    exit(1)

signal(SIGTERM, exit_point)
signal(SIGHUP, exit_point)

def main():
    disp_text()
    txt = "you did good job"
    p = 0
    while True:
        if p + 16 < len(txt):
            lcd.text(txt[p:p+16],1)
        if p + 16 >= len(txt):
            q = txt[p:len(txt)]
            r = 16 - len(q)
            lcd.text(q + '   ' + txt[0:r], 1)
        if p == len(txt):
            p = -1
        p += 1
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        lcd.clear()