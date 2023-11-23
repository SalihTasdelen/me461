import microcontroller
import board
import time
import pwmio
from analogio import AnalogIn
import digitalio  

led_pins = [2, 3, 4, 5, 6, 7, 8, 9] 
button_l_pin = "15"  
button_r_pin = "22"  
pot_pin = "A0"  

class LEDDisplay:
    def __init__(self, led_pins):
        
        self.leds = [pwmio.PWMOut(getattr(board, f'GP{pin}'), frequency=1000, duty_cycle=0) for pin in led_pins]
        self.pot = AnalogIn(getattr(board, pot_pin))
        
        self.button_l = digitalio.DigitalInOut(getattr(board, f'GP{button_l_pin}'))
        self.button_l.direction = digitalio.Direction.INPUT
        self.button_l.pull = digitalio.Pull.UP

        self.button_r = digitalio.DigitalInOut(getattr(board, f'GP{button_r_pin}'))
        self.button_r.direction = digitalio.Direction.INPUT
        self.button_r.pull = digitalio.Pull.UP

        self.last_button_l_state = self.button_l.value
        self.last_button_r_state = self.button_r.value

        self.counter = int(microcontroller.cpu.temperature)

    def ByteDisplay(self, val=0):
        for i in range(8):
            self.leds[i].duty_cycle = 0xFFFF if (val >> i) & 1 else 0
        print("Displayed value:", val)

    def Volta(self, N=1, speed=0.1):
        for _ in range(N):
            for led in self.leds:
                led.duty_cycle = 0xFFFF
                time.sleep(speed)
                led.duty_cycle = 0

            for led in reversed(self.leds):
                led.duty_cycle = 0xFFFF
                time.sleep(speed)
                led.duty_cycle = 0

    def Snake(self, L=3, speed=0.1):
        max_brightness = 0xFFFF
        if L > len(self.leds):
            L = len(self.leds)

        while True:
            for i in range(len(self.leds) + L):
                for j in range(L):
                    led_index = i - j
                    if 0 <= led_index < len(self.leds):
                        brightness_factor = (L - j) / L
                        self.leds[led_index].duty_cycle = int(max_brightness * brightness_factor)

                time.sleep(speed)

                if i - L >= 0 and i - L < len(self.leds):
                    self.leds[i - L].duty_cycle = 0
                    
    def digitalVUmeter(self):
        while True:
            pot_value = self.pot.value  
            pot_voltage = (pot_value * 3.3) / 65536
            mapped_value = int(pot_value / (65535 / 8))
            print(f"Voltage: {pot_voltage}", f"Led display:{mapped_value}")
            for i in range(8):
                if i < mapped_value:
                    self.leds[i].duty_cycle = 0xFFFF
                else:
                    self.leds[i].duty_cycle = 0
            time.sleep(0.1)

    def ButtonCounter(self):
        if not self.button_l.value and self.last_button_l_state:
            self.counter = (self.counter + 1) % 256  
            self.ByteDisplay(self.counter)
            print(f"Counter increased: {self.counter}")

        if not self.button_r.value and self.last_button_r_state:
            self.counter = (self.counter - 1) % 256  
            self.ByteDisplay(self.counter)
            print(f"Counter decreased: {self.counter}")

        self.last_button_l_state = self.button_l.value
        self.last_button_r_state = self.button_r.value

        time.sleep(0.1)  
        
    def displayTemperature(self):
        temperature = microcontroller.cpu.temperature

        print(f"Current Temperature: {temperature:.2f}°C")
        self.ByteDisplay(int(temperature))

    def startup_menu():
        menu_options = """
        LED Display Test Menu:
        1. Byte Display (Enter a byte value)
        2. Volta (Enter number of cycles and speed)
        3. Snake (Enter length and speed)
        4. Digital VU Meter
        5. Button Counter
        6. Display Temperature

        Enter the number of the test you want to run:
        """
        print(menu_options)
        choice = input("Your choice: ")
        return choice
        
    def get_input(prompt):
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")
        
        return get_input(prompt)
        
        
display = LEDDisplay(led_pins)

while True:
    user_choice = LEDDisplay.startup_menu()

    if user_choice == "1":
        byte_val = LEDDisplay.get_input("Enter a integer number(0-255): ")
        display.ByteDisplay(byte_val)
    elif user_choice == "2":
        cycles = LEDDisplay.get_input("Enter number of cycles: ")
        speed = float(input("Enter delay time (e.g., 0.1): "))
        display.Volta(cycles, speed)
    elif user_choice == "3":
        length = LEDDisplay.get_input("Enter snake length: ")
        speed = float(input("Enter speed (e.g., 0.1): "))
        display.Snake(length, speed)
    elif user_choice == "4":
        display.digitalVUmeter()
    elif user_choice == "5":
        while True:
            display.ButtonCounter()
    elif user_choice == "6":
        while True:
            display.displayTemperature()
    else:
        print("Invalid choice. Please restart the device.")

    continue_testing = input("Do you want to continue testing? (yes/no): ").lower()
    if continue_testing != "yes":
        break
print("Testing completed.")

