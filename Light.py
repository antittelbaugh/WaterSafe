from gpiozero import LED
#import time

# Set up the GPIO mode
led = LED(17)
def turn_on_led():
    led.on()
    #GPIO.output(ground_pin, GPIO.LOW)
    print("LED is ON")

# Function to turn off the LED
def turn_off_led():
    led.off()
    #GPIO.output(ground_pin, GPIO.HIGH)
    print("LED is OFF")

# Test the functions
if __name__ == "__main__":
    try:
        # Turn on the LED
        turn_on_led()
        #time.sleep(2)  # Leave the LED on for 2 seconds
        
        # Turn off the LED
        #turn_off_led()
        #time.sleep(2)  # Leave the LED off for 2 seconds
        
    except KeyboardInterrupt:
        pass  # If the script is interrupted by the user
    
    # Clean up the GPIO settings
    #GPIO.cleanup()
