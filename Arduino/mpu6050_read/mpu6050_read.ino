#include <Wire.h>
const int MPU6050_ADDR = 0x68; // MPU6050 I2C address

int16_t temp;
int16_t accelerometer_x, accelerometer_y, accelerometer_z;
int16_t gyroscope_x, gyroscope_y, gyroscope_z;

double Ax, Ay, Az, Gx, Gy, Gz, T;

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

  // Read Temp
  temp = Wire.read() << 8 | Wire.read();
  
  // Read gyroscope data
  gyroscope_x = Wire.read() << 8 | Wire.read();
  gyroscope_y = Wire.read() << 8 | Wire.read();
  gyroscope_z = Wire.read() << 8 | Wire.read();

  // Correct values
  Ax = accelerometer_x / 16384.0;
  Ay = accelerometer_y / 16384.0;
  Az = accelerometer_z / 16384.0;

  Gx = gyroscope_x / 131.0;
  Gy = gyroscope_y / 131.0;
  Gz = gyroscope_z / 131.0;

  // Print the values
  // TODO cambiar esto a un mensaje estandar con los 6 datos para parsear en unity
  Serial.print("Accelerometer: ");
  Serial.print("X = "); Serial.print(Ax);
  Serial.print(", Y = "); Serial.print(Ay);
  Serial.print(", Z = "); Serial.println(Az);

  Serial.print("Gyroscope: ");
  Serial.print("X = "); Serial.print(Gx);
  Serial.print(", Y = "); Serial.print(Gy);
  Serial.print(", Z = "); Serial.println(Gz);
  Serial.print("\n");

  delay(1000);  // Delay for 1 second
}
