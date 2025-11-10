import RPi.GPIO as GPIO
from time import sleep

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN)      
    GPIO.setup(24, GPIO.OUT)

def read_slide_switch():
    return GPIO.input(22)       

def main():
    init()
    print("Program running...")

    blinked = False   # <-- NEW: remember if we already blinked when switch is on the "right side"

    try:
        while True:
            if read_slide_switch() == 1:
                # switch ON → blink at 5 Hz (or whatever you want here)
                GPIO.output(24, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(24, GPIO.LOW)
                sleep(0.1)

                # since switch is on this side, reset the flag
                blinked = False

            else:
                # switch on the "right side"
                if not blinked:
                    # 10 Hz for 5 seconds (50 * 0.1s)
                    for _ in range(50):
                        GPIO.output(24, GPIO.HIGH)
                        sleep(0.05)
                        GPIO.output(24, GPIO.LOW)
                        sleep(0.05)

                    GPIO.output(24, GPIO.LOW)   # make sure LED off after blinking
                    blinked = True              # mark as done so it won't repeat
                else:
                    # already blinked → keep LED OFF
                    GPIO.output(24, GPIO.LOW)
                    sleep(0.1)   # tiny pause so it doesn’t spam the CPU

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped.")

if __name__ == "__main__":
    main()
