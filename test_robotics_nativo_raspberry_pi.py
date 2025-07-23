#!/usr/bin/env python3
# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL ROBOTICS
# Archivo .vdr ejecutado nativamente para Raspberry Pi

import RPi.GPIO as GPIO
import time

class VaderRoboticsRaspberryPi:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.led_pin = 18
        self.motor_pin1 = 23
        self.motor_pin2 = 24
        self.sensor_pin = 25
        
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.motor_pin1, GPIO.OUT)
        GPIO.setup(self.motor_pin2, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        
        print("🤖 VADER 7.0 - Raspberry Pi Robotics Runtime")
    
    def controlar_led(self, estado):
        GPIO.output(self.led_pin, estado)
    
    def mover_motor(self, direccion):
        if direccion:
            GPIO.output(self.motor_pin1, GPIO.HIGH)
            GPIO.output(self.motor_pin2, GPIO.LOW)
        else:
            GPIO.output(self.motor_pin1, GPIO.LOW)
            GPIO.output(self.motor_pin2, GPIO.HIGH)
    
    def leer_sensor(self):
        return GPIO.input(self.sensor_pin)
    
    def ejecutar_comportamiento(self):
        try:
            while True:
                sensor_state = self.leer_sensor()
                
                if sensor_state:
                    self.controlar_led(True)
                    self.mover_motor(True)
                else:
                    self.controlar_led(False)
                    self.mover_motor(False)
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            GPIO.cleanup()

def main():
    robot = VaderRoboticsRaspberryPi()
    robot.ejecutar_comportamiento()

if __name__ == '__main__':
    main()
