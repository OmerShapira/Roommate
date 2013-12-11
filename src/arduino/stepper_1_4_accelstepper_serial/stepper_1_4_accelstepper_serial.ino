#define NUM_STEPPERS
#include <AccelStepper.h>

#define SHUT_FAST 0
#define SHUT_SLOWLY 1
#define RANDOM_PATTERN1 10

AccelStepper steppers[NUM_STEPPERS] = {
  AccelStepper(1, 9, 8),
  AccelStepper(1, 5, 4),
  AccelStepper(1, 3, 2),
  AccelStepper(1, 7, 6)};
int delta[NUM_STEPPERS] = {800, 600, 600, 820}; //TODO: Give 1,2 a real value
int speed[NUM_STEPPERS] = {3000, 3000, 3000, 2500};
int acceleration[NUM_STEPPERS] = {1000, 1000, 100, 800};

bool newCommand = false;
int command = 0;
int mode = 0;

void setup()
{  
  Serial.begin(9600);
  for(int i=0; i<NUM_STEPPERS; i++){
      steppers[i].setMaxSpeed(speed[i]);
      steppers[i].setAcceleration(acceleration[i]);
  }
}

void loop()
{
  if(newCommand){
    newCommand = false;
    switch (command) {
        case SHUT_FAST:
          // do something
          break;
        case SHUT_SLOWLY:
          // do something
          break;
        case RANDOM_PATTERN1:
          setMotorsByArrays(true);
          break;
        default: break; //Should never happen
    }
  } else {
    switch (commmand) {
        case RANDOM_PATTERN1:
          setMotorsByArrays(false); //Don't force new values
          break;
        default:
          // do something
    }
  }

  for(int i=0; i<NUM_STEPPERS; i++){
    steppers[i].run();
  }
}

void setMotorsByArrays(bool force){
  for(int i=0; i<NUM_STEPPERS; i++){ //if you're looping
      if (steppers[i].distanceToGo() == 0){
        delta[i] *= -1; //HACK: To save Building another array
      }
      if (steppers[i].distanceToGo() == 0 || force){
        steppers[i].moveTo(max(delta[i], 0));
      }
  }
}

void serialEvent() {
  while (Serial.available()) {
    command = Serial.parseInt();
    newCommand = true;
  }
}

