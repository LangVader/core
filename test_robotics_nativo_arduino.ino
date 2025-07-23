// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL ROBOTICS
// Archivo .vdr ejecutado nativamente para Arduino

#include <Arduino.h>
#include <Servo.h>

class VaderRoboticsArduino {
private:
    static const int LED_PIN = 13;
    static const int MOTOR_PIN1 = 2;
    static const int MOTOR_PIN2 = 3;
    static const int SENSOR_PIN = A0;
    
public:
    void inicializar() {
        Serial.begin(9600);
        pinMode(LED_PIN, OUTPUT);
        pinMode(MOTOR_PIN1, OUTPUT);
        pinMode(MOTOR_PIN2, OUTPUT);
        Serial.println("🤖 VADER 7.0 - Arduino Robotics Runtime");
    }
    
    void moverMotor(bool direccion) {
        digitalWrite(MOTOR_PIN1, direccion ? HIGH : LOW);
        digitalWrite(MOTOR_PIN2, direccion ? LOW : HIGH);
    }
    
    int leerSensor() {
        return analogRead(SENSOR_PIN);
    }
    
    void ejecutarComportamiento() {
        int sensorValue = leerSensor();
        
        if (sensorValue > 500) {
            digitalWrite(LED_PIN, HIGH);
            moverMotor(true);
        } else {
            digitalWrite(LED_PIN, LOW);
            moverMotor(false);
        }
        
        delay(100);
    }
};

VaderRoboticsArduino robot;

void setup() {
    robot.inicializar();
}

void loop() {
    robot.ejecutarComportamiento();
}
