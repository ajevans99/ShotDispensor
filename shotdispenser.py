from magstripe import MagStripe, MagStripeError
from lcddriver import LCD
import RPi.GPIO as GPIO
import time
import sys
import logging

RELAY_PIN  = 11 # BOARD

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_PIN, GPIO.OUT)

def keyboard_input():
    return str(sys.stdin.readline().strip())

def pump(on=True):
    if on:
        GPIO.output(RELAY_PIN, GPIO.LOW)
        logging.info('Relay on')
    else:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        logging.info('Relay off')

def process_id_card(data, mag):
    try:
        parsed_data = mag.parse(data)
        logging.info('Parsed data: ' + parsed_data['name'])
        return parsed_data
    except MagStripeError as e:
        logging.error(e)
    return None

if __name__ == "__main__":
    setup_logging()
    setup_gpio()
    pump(on=False)
    lcd = LCD()
    mag = MagStripe()
    while True:
        lcd.lcd_clear()
        lcd.lcd_display_string('Scan your MSU ID')
        mag_data = keyboard_input()
        logging.info('Keyboard read:', mag_data)
        result = process_id_card(mag_data, mag)
        if result is None:
            continue
        lcd.lcd_display_string(result['name'])
        lcd.lcd_display_string(result['pid'], line=2)
        pump(on=True)
        time.sleep(30)
        pump(on=False)
