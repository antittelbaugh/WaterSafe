import time
import lgpio

gLED = 23
bLED = 24

# open the gpio chip and set the LED pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED)
def turn_on_gled():
    lgpio.gpio_write(h, gLED, 1)
def turn_goff_led():
    lgpio.gpio_write(h, gLED, 0)
def turn_on_bled():
    lgpio.gpio_write(h, bLED, 1)
def turn_boff_led():
    lgpio.gpio_write(h, bLED, 0)
def turn_on_both():
    lgpio.gpio_write(h, bLED, 1)
    lgpio.gpio_write(h, gLED, 1)
def turn_off_both():
    lgpio.gpio_write(h, bLED, 0)
    lgpio.gpio_write(h, gLED, 0)

