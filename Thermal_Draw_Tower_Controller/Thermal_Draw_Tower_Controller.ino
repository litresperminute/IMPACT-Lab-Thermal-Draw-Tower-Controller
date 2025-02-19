/*
  ARDUNIO CONNECTION AND PINOUT SUMMARY:
  LED Display - GND/+5V/SCL/SDA (daisy-chained I2C cable)
  Digital Pot - GND/+5V/SCL/SDA (I2C cable plugged into +5V/GND/SCL/SDA Pins)
  Rotary Pot 1 - GND/A0/+5V (Used to manually control the feeder speed by adjusting the resistance/read voltage of the wiper pin from 0 - 5V in 10 turns)
  Rotary Pot 2 - GND/A1/+5V (Used to manually control the digital potentiometer by adjusting the resistance/read voltage of the wiper pin from 0 - 5V in 1 turnwhich controls the winder speed)
  Fans x 2 - GND/+5V (on either side of the stepper controller to push air through. No power or on/off control incorporated)
  Stepper: Enable / Direction / Pulse - D8/D7/D6 (enable is routed through an on/off switch || Direction is routed to a breadboard row, to which the centre pin from the switch is connected, the other two pins being tied to GND and +5V)
  (The intention of this decision is to enable the direction to be brute-force overtaken by the GND/+5V rails when closed in those positions, but to allow the digital pin to automate direction in the middle position.)
  Positive Carriage Limit Switch (bottom): +5V/GND - D2(write)/D3(read) (use interrupt pins to ensure stop command is triggered immediately?)
  Negative Carriage Limit Switch (top): +5V/GND - D5(write)/D4(read)
  Tensiometer Analog Signal: GND/+10V - voltage split to 5V max with 2x10kohm resistors and connected to pin A2 (GND is connected to device power supply, but may be floating and need to be properly grounded in the future)
  Winder Control Switch: Rot Pot 2 Wiper/On-Board Filabot Pot Wiper - GND/A3/+5V || GND/A3/+5V (voltage supplied here from filabot, not sourced from Arduino)
  Keyence Analog Diameter Readout: (Not sure what will be required but presumably at least 1 digital or analog pin connected that provides data from the keyence power block thing)
*/


// Initialize digital potentiometer
#include <Adafruit_DS3502.h>  // Digital Potentiometer library
Adafruit_DS3502 ds3502 = Adafruit_DS3502();
#define DS3502_ADDR 0x28 // I2C hex address of the DS3502 - RH to 5V / RL to GND / RW to WIPER_VALUE_PIN for rot pot 2


// Initialize screen
#include <Wire.h> // This library allows you to communicate with I2C devices
#include <Adafruit_GFX.h> // 
#include <Adafruit_SSD1306.h> // 
#define SCREEN_WIDTH 128 // OLED display width
#define SCREEN_HEIGHT 32 // OLED display height
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
#define OLED_RESET    -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


// define limit switch pins - Positive is bottom-most position / negative is top-most position
#define pos_limit_read 2 // INTERRUPT PIN | white wire - supply voltage for NC (normally closed) circuit so that when it opens the read pin drops to GND voltage
#define pos_limit_write 5 // green wire - read constantly for a change from the normally-closed value (presumably +5V) and interrupt code with a stop command
#define neg_limit_read 3 // INTERRUPT PIN | black wire - supply voltage for NC (normally closed) circuit so that when it opens the read pin drops to GND voltage
#define neg_limit_write 4 // blue wire - read constantly for a change from the normally-closed value (presumably +5V) and interrupt code with a stop command
#include <ezButton.h> // this library can be used to de-bounce the limit switches, steadying the limit switch response
ezButton pos_limit_switch(neg_limit_read);
ezButton neg_limit_switch(pos_limit_read);


// Analog pins
#define feeder_speed_pot A0  // feed speed rotary potentiometer wiper pin on the arduino
#define winder_pot_value_pin A1 // winder speed rotary pontentiometer wiper pin on the arduino
#define winder_pin A2 // this pin is reading the toggled winder value, either from the FILAWINDER or from the winder rotary potentiometer
#define tension_pin A3 // this pin is reading the signal + output from the tensiometer after being voltage-divided from 0-10V to 0-5V on the breadboard using 2 split 10 kohm resistors
#define micrometer_pin A4 // this pin is reading the LS-9030 micrometer signal from the LS-9051 controller module's analog output
//Check micrometer pin

// define feed motor input pins
#include <AccelStepper.h> // motor controller library
#define interface 1   // interface == 1 indicates use of 2 pin motor control (pin 1 = step, pin 2 = direction) (enable pin can be initialized AFTER AccelStepper construction if needed) 
#define step_pin 6    // stepper pin on the arduino (pulse+ pin)
#define dir_pin 7     // direction pin on the arduino (dir+ pin) (routed to a 3-position rocker switch that can select REV/AUTO/FWD and manually override the program)
AccelStepper feeder(interface, step_pin, dir_pin);  // initialize feed stepper motor
AccelStepper setPinsInverted(true, false, false);
const int stepsPerRev = 3200; // number of steps per revolution of the screw, based on the DIP switch settings of the microstepper controller (OFF OFF ON = 3200)

#include <math.h> //math library for rounding

// define CLOCK: the frequency that the controller checks and updates motor speeds
unsigned long previousMillis = 0; // stores the last time timer was updated
const long interval = 200; //interval at which to refresh feed and winder speeds and update display (milliseconds)


//------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
// defining controls for the winder
bool control_winder = true;
int setpoint = 1818; // diameter micrometer set point in microns
float error = 0; // initialize error
float fiber_diameter = 0; // starting value

// Inital Values
float kp_gain = 0.02; // proporitonal control gain
float winder_pot_value = 3; // m/min This is the value to initialize the tower. Need to get this started.

//function for quick conversion
// Don't think this is required any more
/*
void convert_winder_to_voltage(float &winder_pot_value) {
  winder_pot_value *= 1000.0; // convert from m/min to mm/min
  winder_pot_value /= 60.0; // convert to mm/s
  winder_pot_value /= 0.2237; //Aconert to voltage to read = 0.2237mm/(s*Volt)
}
*/

// this is to convert the signal to a voltage this may not be right. **the 0.2237 is from the winder I think it applies but it may not.

// min and max values of the system
float min_winder_speed = 0; // mm/min
float max_winder_speed = 13730; // mm/min -> 13.73 m/min

// defining controls for the feeder
bool control_feeder = false;
float feeder_speed = 1; // mm/min //this will intialize in the setup function
float feeder_pot_value;
float kp_gain_feeder = 1;
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

void setup() {

  // Assign pin mode for each limit switch pin, set both switches to GND
  pinMode(neg_limit_read, INPUT_PULLUP);
  pinMode(pos_limit_read, INPUT_PULLUP);
  pinMode(neg_limit_write, OUTPUT);
  pinMode(pos_limit_write, OUTPUT);
  digitalWrite(neg_limit_write, LOW); // sets the negative limit switch to GND
  digitalWrite(pos_limit_write, LOW); // sets the positive limit switch to GND
  pos_limit_switch.setDebounceTime(100); // debounce time set to 50 milliseconds for both switches
  neg_limit_switch.setDebounceTime(100);

  //pinMode(dir_pin, INPUT_PULLUP); // Not sure if  this is necessary
  //digitalWrite(dir_pin, true);  // set the direction pin value to 1 (down)


  Serial.begin(115200);
  while (!Serial) {
    delay(1);  // Wait until serial port is opened
  }

  Serial.println("Adafruit DS3502 Test");
  if (!ds3502.begin()) {
    Serial.println("Couldn't find DS3502 chip"); /* while (1); */
  }
  Serial.println("Found DS3502 chip");

  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) { // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  display.clearDisplay(); // Clear the OLED display buffer

  //Initialize feeder speed
  //would need to make an if and get rid of this?
  feeder.setMaxSpeed(stepsPerRev / 2); // Set max motor speed in steps per second. Must be positive.  Library documentation says speeds exceeding 1000 are unreliable but 3200 steps = 1 revolution = 5.08 mm with current controller DIP switch settings
  // with the max speed set this way, the speed limit will be based on the DIP switch settings.  In any case, one revolution per second = 5.08 mm/s
  if (control_feeder = false) {
    float feeder_pot_value = analogRead(feeder_speed_pot); // replace with map command?
    feeder_pot_value /= 1023;
    feeder_pot_value *= 20;
    float feeder_speed = feeder_pot_value * 5.08 / stepsPerRev * 60; //conversion from potentiometer reading to feed speed in mm/min (5.08 mm per turn, 3200 steps per turn, 60 sec per minute)
    }
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------     
  if (control_feeder = true){
    float feeder_pot_value = feeder_speed / 5.08 *stepsPerRev / 60;  //convert from mm/min to a readable value
    }

  feeder.setSpeed(feeder_pot_value);
  Serial.println("time, Feed (mm/min), Wind (m/min), diameter (um), predicted diameter (um)");
  
  // Initialize the winder
  //convert_winder_to_voltage(winder_pot_value);
  //Writing to Digi pot
  int winder_dig = (winder_pot_value/max_winder_speed*127*1000); // (m/min)/(mm/min) *1000 mm/m * 127 round to an integer if winder_pot_value  == 3 then this is 28 for the value
  ds3502.setWiper(winder_dig);
  Serial.print("DS2502_wiper_setting");
  Serial.print(winder_pot_value);
  Serial.println("m/min");
  delay(10000);
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
}

void loop() {

  pos_limit_switch.loop(); // begin limit switch de-bouncing loops
  neg_limit_switch.loop();
  int pos_limit_check = pos_limit_switch.getState(); // check limit switch state using ezButton (de-bounce) library command
  int neg_limit_check = neg_limit_switch.getState();

  if (pos_limit_check == 0 && neg_limit_check == 0) { // if neither limit switch is triggered (opens on contact) then the program runs as usual.

    feeder.runSpeed(); // Runs feed motor. Need to run every iteration (as often as possible)

    // Check if enough time has (value of 'inverval' variable in ms) has passed
    // If enough time has passed, execute the tasks below (read input and output speeds, update speeds based on controller settings)
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      // Save the last time the interval completed
      previousMillis = currentMillis;

      // this starts the control aspect
      control_function(control_winder, control_feeder, winder_pot_value, feeder_speed); //units of the winder_pot_value going in is in volts needs to be converted

      // TASK 3: Read micrometer and tension data
      float tension_Value = analogRead(tension_pin);
      float fiber_diameter = analogRead(micrometer_pin);
      fiber_diameter *= 9.77517; // analogRead outputs 1023 bits per 10V, then 2000 microns per V

      // TASK 5: Output readings to serial monitor and display
      Serial.print(millis() / 100);
      Serial.print(",");
      Serial.print(feeder_speed);
      Serial.print(",");
      Serial.print(winder_pot_value);
      Serial.print(",");
      Serial.print(fiber_diameter);
      Serial.print(",");
      Serial.println(20000 * sqrt(feeder_speed / winder_pot_value / 1000));


      // Display the linear feed speed
      display.clearDisplay();// Clear the buffer
      display.setTextSize(1);
      display.setTextColor(WHITE);
      display.setCursor(0, 0);
      // Display static text
      display.print("Feed Spd:");
      display.print(feeder_speed);
      display.println("mm/min");
      display.print("Wind Spd:");
      display.print(winder_pot_value);
      display.println("m/min");
      display.print("Pred. Dia:");
      display.println(20000 * sqrt(feeder_speed / winder_pot_value / 1000));
      display.print("Fiber Dia: ");
      display.print(fiber_diameter);
      display.println("um");
      display.display();

    }

  }

  //PROCEDURE AFTER POSITIVE LIMIT SWITCH IS REACHED (NO USER CONTROL DURING THIS SECTION)
  if (pos_limit_check == 1 && neg_limit_check == 0) { //

    feeder.stop();
    //int reverseSpeed = -1000;feeder.maxSpeed()*-1
    //digitalWrite(dir_pin, 0);  // set the direction pin value to 0 (up)
    feeder.setSpeed(-400); // set speed to previously set maximum and direction to reverse (negative numbers)

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    display.println("Positive limit");
    display.println("switch hit!");
    display.println();
    display.println("Please Wait..");
    Serial.println("Positive Limit Reached!");
    Serial.println("Please Wait..");
    delay(1000);

    do { // once in this loop, it should run until the negative limit switch is triggered - no manual feed speed control
      neg_limit_switch.loop();
      neg_limit_check = neg_limit_switch.getState(); // Check limit switch every loop iteration while running in reverse until
      //Serial.print("Neg limit state: ");
      //Serial.print(neg_limit_check);
      //Serial.print(" Direction Pin: ");
      //Serial.println(digitalRead(dir_pin));
      feeder.runSpeed();
    }
    while (neg_limit_check == 0);

    Serial.println("END OF CARRIAGE RETURN LOOP");
    display.clearDisplay();
  }

  //PROCEDURE AFTER NEGATIVE LIMIT SWITCH IS REACHED (NO USER CONTROL DURING THIS SECTION)
  if (pos_limit_check == 0 && neg_limit_check == 1) {

    feeder.stop();
    //digitalWrite(dir_pin, 1);  // set the direction pin value to 1 (down)
    feeder.setSpeed(400);

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    display.println("Please Wait..");
    //Serial.println("Negative Limit Reached!");
    //Serial.print("Direction Pin Set to: ");
    //Serial.println(digitalRead(dir_pin));
    //Serial.println("Moving to Start Position Now.. Please Wait");

    delay(10);

    for ( int i = 0; i <= 20; i++) {
      feeder.runSpeed();
      delay(10);
    } //while (neg_limit_check != 1);

    Serial.println("END OF FOR LOOP FOR MOVING TO STARTING POSITION");
  }
}


//------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
void control_function(bool control_winder, bool control_feeder, float &winder_pot_value, float &feeder_pot_value) {

  float new_winder_speed;
  //Task 0: Have the speed estimate
  // "plant"
  float plug_diameter = 25.4; //mm 1 inch plug - should check
  float target_diameter = setpoint/1000; // convert microns to the mm
  // feeder speed is already defined with variable feeder_speed - may not be defined in here though . defined in mm/min for now it should be estimated that the feeder speed is constant.
  float target_winder_speed = feeder_speed * sq(plug_diameter) / sq(target_diameter) / 1000; // this will output the in m/min ~ 2.5 m/min

  //convert the winder_pot_value back to mm/min
  /*
   * This likely is not needed and could be deleted.
  winder_pot_value *= 0.2237; // Analog voltage reading to linear winding speed conversion = 0.2237mm/(s*Volt)
  winder_pot_value *= 60; // converts mm/s to mm/min
  winder_pot_value /= 1000; // converts mm/min to m/min
  */
  
  // TASK 1: Update winder speed
  // Check if we aree using controls
  if (control_winder == true) {
    error = (fiber_diameter - setpoint) / (setpoint); // is there a diffeerent error metric to go for?
    float prop_gain = abs(error * kp_gain);

    // future add integral values where integral wind up is accounted for 
    float ki_winder = 0;
    float int_gain = 0;

    // Future task, add in derivative terms if needed
    float kd_winder = 0;
    float der_gain = 0;

    // total gain
    float tot_gain = (prop_gain + int_gain + der_gain)*target_winder_speed;

    // check if the error which checks if it is to big or to small.
    /* Old code that is being kept out for now
    if (error > 0) {
      float new_winder_speed = winder_pot_value + tot_gain; // increase the speed to decrease the diameter
      Serial.print(" Speed Increased by: "); Serial.print(tot_gain); 
      
      }
      else {
        float new_winder_speed = winder_pot_value - tot_gain; // decrease the speed to increase the diameter
      Serial.print(" Speed Decreased by: "); Serial.print(tot_gain); 
    }
    */

    //check if the winder the winder is at max or min speed.
    /*
    if (new_winder_speed > max_winder_speed) {
      new_winder_speed = max_winder_speed;
      }
    if (new_winder_speed < min_winder_speed) {
      new_winder_speed = min_winder_speed;
      }
     */
    
    //convert_winder_to_voltage(new_winder_speed);
    //convert back to winder_pot_value so that it writes it back
    //winder_pot_value = new_winder_speed;

    int dig_pot = 28; // only here if it needs to be defined again
    if (error > 0) {
      dig_pot += 1;
      }
   
    if (error < 0){
      dig_pot -= 1;
      }

  
    //Writing to Digi pot
    // formula to control with
    //int dig_pot = (winder_pot_value * 1000 / max_winder_speed *127);

    ds3502.setWiper(dig_pot);
    Serial.print("DS2502_wiper_setting");
    //Serial.print(winder_pot_value);
    //Serial.println(" mm/min");
    //Serial.print(dig_pot);


    // print new speed, error, speed increase or decrease (above), setpoint
    //Serial.print(" New winder speed: "); Serial.print(new_winder_speed); 
    Serial.print(" Current Error: "); Serial.print(error); 
    Serial.print(" Diameter Aimed for: "); Serial.print(setpoint); 
  }
    else {
      float winder_pot_value = analogRead(winder_pot_value_pin); // Might be computationally better not to initialize this every loop but idk
      winder_pot_value *= 0.2237; // Analog voltage reading to linear winding speed conversion = 0.2237mm/(s*Volt)
      winder_pot_value *= 60; // converts mm/s to mm/min
      winder_pot_value /= 1000; // converts mm/min to m/min
  }

  // could be useful to translate this to a different function
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
  //Make a seperate function eventually
  // TASK 2: Update feed speed
  // if we want to control the feeder speed
  float new_feeder_speed;
  if (control_feeder = true) {
    error = (fiber_diameter - setpoint) / ((fiber_diameter + setpoint) / 2); // is there a diffeerent error metric to go for?

    //may need too adjust the feeder_speed variable

    
    //proportional gain
    float gain = abs(error * kp_gain_feeder);

    //integral gain


    //derivative gain

    
    //increase or decrease speed
    if (error > 0) {
      new_feeder_speed = feeder_pot_value + gain; // increase the speed to decrease the diameter
      Serial.print(gain); Serial.print("Speed Increased by");
    }
      else {
        new_feeder_speed = feeder_pot_value - gain; // decrease the speed to increase the diameter
        Serial.print(gain); Serial.print("Speed Decreased by");
    }
  // add mins and maxes
  

  }
    else {
      float feeder_pot_value = analogRead(feeder_speed_pot);
    feeder_pot_value /= 1023;
    feeder_pot_value *= 100;
    float feeder_speed = feeder_pot_value * 5.08 / 3200 * 60; //conversion from potentiometer reading to feed speed in mm/min.  (feed speed) x (mm/rev) / (steps/rev) x (60 s/min)
    feeder.setSpeed(feeder_pot_value);
  }
}
