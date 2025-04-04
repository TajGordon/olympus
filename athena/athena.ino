#include "Wire.h"
#include "PowerfulBLDCdriver.h"

PowerfulBLDCdriver motor1;

void setup() {
  Serial.begin(115200); // initialise serial
  Wire.setSCL(9);
  Wire.setSDA(8);
  Wire.begin(); // initialise i2c0, make sure to look up the i2c pins of your microcontroller.
  Wire.setClock(1000000); // set i2c speed to 1MHz
  motor1.begin(25, &Wire); // motor1 has i2c address 25 and is using i2c0.
  Serial.print("The firmware version of the motor driver is: ");
  Serial.println(motor1.getFirmwareVersion()); // get the firmware version and print it to the serial monitor.
  motor1.setCurrentLimitFOC(65536); // set current limit to 1 amp (only works in FOC mode)
  motor1.setIdPidConstants(1500, 200); 
  motor1.setIqPidConstants(1500, 200);
  motor1.setSpeedPidConstants(4e-2, 4e-4, 3e-2); // Constants valid for FOC and Robomaster M2006 P36 motor only, see tuning constants document for more details
  motor1.setELECANGLEOFFSET(1160405248); // set the ELECANGLEOFFSET calibration value. Each motor needs its own calibration value.
  motor1.setSINCOSCENTRE(1251); // set the SINCOSCENTRE calibration value. Each motor needs its own calibration value.
  motor1.configureOperatingModeAndSensor(3, 1); // configure FOC mode and sin/cos encoder
  motor1.configureCommandMode(12); // configure speed command mode
  delay(500);
}

void loop() {
  // when using Robomaster M2006 P36 motor max speed (no load) is 100000000 @ 12V and 130000000 @ 16V
  // for Robomaster M2006 P36 motor, there are 7 pole pairs and 36:1 gearbox. So for 1 output revolution there will be 7*36=252 electrical revolutions
  motor1.setSpeed(25000000); // set the motor speed to 25000000/2^16 elec rev/s
  delay(2000);

  motor1.updateQuickDataReadout(); // update quick data readout
  Serial.print("pos:");
  Serial.print(motor1.getPositionQDR()); // get the motor position from quick data readout
  Serial.print(" spd:");
  Serial.print(motor1.getSpeedQDR()); // get the motor speed from quick data readout
  Serial.print(" err1:");
  Serial.print(motor1.getERROR1QDR()); // See documentation for details
  Serial.print(" err2:");
  Serial.println(motor1.getERROR2QDR()); // ERROR2 is not fully implemented in motor driver firmware. Ignore the value of this for now.

  motor1.setSpeed(-25000000); // negative values reverse the direction of the motor.
  delay(2000);

  motor1.updateQuickDataReadout();
  Serial.print("pos:");
  Serial.print(motor1.getPositionQDR());
  Serial.print(" spd:");
  Serial.print(motor1.getSpeedQDR());
  Serial.print(" err1:");
  Serial.print(motor1.getERROR1QDR());
  Serial.print(" err2:");
  Serial.println(motor1.getERROR2QDR());
}