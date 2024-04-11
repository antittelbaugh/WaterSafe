import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for power and ground
power_pin = 19
ground_pin = 6

# Set up the GPIO pins
GPIO.setup(power_pin, GPIO.OUT)  # Power pin set as output
#GPIO.setup(ground_pin, GPIO.OUT) # Ground pin set as output

# Function to turn on the LED
def turn_on_led():
    GPIO.output(power_pin, GPIO.HIGH)
    #GPIO.output(ground_pin, GPIO.LOW)
    print("LED is ON")

# Function to turn off the LED
def turn_off_led():
    GPIO.output(power_pin, GPIO.LOW)
    #GPIO.output(ground_pin, GPIO.HIGH)
    print("LED is OFF")

# Test the functions
if __name__ == "__main__":
    try:
        # Turn on the LED
        turn_on_led()
        time.sleep(2)  # Leave the LED on for 2 seconds
        
        # Turn off the LED
        turn_off_led()
        time.sleep(2)  # Leave the LED off for 2 seconds
        
    except KeyboardInterrupt:
        pass  # If the script is interrupted by the user
    
    # Clean up the GPIO settings
    GPIO.cleanup()
