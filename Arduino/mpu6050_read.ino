#include <Wire.h>
const int MPU6050_ADDR = 0x68; // MPU6050 I2C address

int16_t accelerometer_x, accelerometer_y, accelerometer_z;
int16_t gyroscope_x, gyroscope_y, gyroscope_z;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Initialize MPU6050
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // Wake up the MPU-6050
  Wire.endTransmission(true);
}

void loop() {
  // Read accelerometer and gyroscope data
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 14, true);

  // Read accelerometer data
  accelerometer_x = Wire.read() << 8 | Wire.read();
  accelerometer_y = Wire.read() << 8 | Wire.read();
  accelerometer_z = Wire.read() << 8 | Wire.read();

  // Read gyroscope data
  gyroscope_x = Wire.read() << 8 | Wire.read();
  gyroscope_y = Wire.read() << 8 | Wire.read();
  gyroscope_z = Wire.read() << 8 | Wire.read();

  // Print the values
  Serial.print("Accelerometer: ");
  Serial.print("X = "); Serial.print(accelerometer_x);
  Serial.print(", Y = "); Serial.print(accelerometer_y);
  Serial.print(", Z = "); Serial.println(accelerometer_z);

  Serial.print("Gyroscope: ");
  Serial.print("X = "); Serial.print(gyroscope_x);
  Serial.print(", Y = "); Serial.print(gyroscope_y);
  Serial.print(", Z = "); Serial.println(gyroscope_z);

  delay(1000);  // Delay for 1 second
}
