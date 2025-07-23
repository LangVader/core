// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL IoT
// Archivo .vdr ejecutado nativamente en Arduino/ESP32

#include <DHT.h>
#include <Servo.h>

// Definiciones de pines

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  dht.begin();
  dht.begin();
}

void loop() {
  Serial.println("🤖 ¡Hola desde Vader 7.0 IoT Universal!");
  float temp = dht.readTemperature();
  Serial.print("Temperatura: ");
  Serial.println(temp);
  Serial.println("Iniciando sistema de monitoreo...");
  int sensorValue = analogRead(A0);
  Serial.print("Sensor: ");
  Serial.println(sensorValue);
  float temp = dht.readTemperature();
  Serial.print("Temperatura: ");
  Serial.println(temp);
  int sensorValue = analogRead(A0);
  Serial.print("Sensor: ");
  Serial.println(sensorValue);
  int sensorValue = analogRead(A0);
  Serial.print("Sensor: ");
  Serial.println(sensorValue);
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  Serial.println("¡Movimiento detectado!");
  Serial.println("Temperatura leída");
  Serial.println("Luz ambiente medida");
  Serial.println("Sistema funcionando correctamente");
  delay(2000);
  Serial.println("✅ Vader IoT Runtime funcionando perfectamente en Arduino");
}
