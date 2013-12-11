#define NUM_STEPPERS 4
#include <AccelStepper.h>

#define SHUT_FAST 0
#define SHUT_SLOWLY 1
#define RANDOM_PATTERN1 2
#define STAY_OPEN 8
#define STOP 9

AccelStepper steppers[NUM_STEPPERS] = {
  AccelStepper(1, 9, 8),
  AccelStepper(1, 5, 4),
  AccelStepper(1, 3, 2),
  AccelStepper(1, 7, 6)};
int delta[NUM_STEPPERS] = {1600, 1200, 1200, 1640}; //TODO: Give 1,2 a real value
int speed[NUM_STEPPERS] = {3000, 1200, 1000, 2500};
int acceleration[NUM_STEPPERS] = {1200, 200, 100, 800};

bool newCommand = false;
int command = SHUT_SLOWLY;
bool stopped = false;

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
      case STOP:
        stopped = true;
        break;
      case SHUT_FAST:
      stopped = false;
      for (int i = 0 ; i < NUM_STEPPERS ; i++){
        steppers[i].setMaxSpeed(5000);
        steppers[i].setAcceleration(5000);
        steppers[i].moveTo(0);
      }
      break;
      case SHUT_SLOWLY:
      stopped = false;
      for (int i = 0 ; i < NUM_STEPPERS ; i++){
        steppers[i].moveTo(0);
        steppers[i].setMaxSpeed(1200);
        steppers[i].setAcceleration(800);
      }
      break;
      case STAY_OPEN: //do the randomPattern
        stopped = false;
        setMotorsByArrays(true,false);
        break;
      case RANDOM_PATTERN1:
        stopped = false;
        setMotorsByArrays(true,true);
        break;
        default: break; //Should never happen
      }
      } else {
        switch (command) {
          case STAY_OPEN:
            setMotorsByArrays(false,false);
            break;
          case RANDOM_PATTERN1:
            setMotorsByArrays(false,true); //Don't force new values
            break;
          default: break;
        }
      }

      if(!stopped){
        for(int i=0; i<NUM_STEPPERS; i++){
          steppers[i].run();
        }
      }
      
    }

    void setMotorsByArrays(bool force, bool allowReverse){
  for(int i=0; i<NUM_STEPPERS; i++){ //if you're looping
    if (steppers[i].distanceToGo() == 0){
        delta[i] *= -1; //HACK: To save Building another array
      }
    if (force){
      steppers[i].setMaxSpeed(speed[i]);
      steppers[i].setAcceleration(acceleration[i]);
    }
    if (!allowReverse) {
      delta[i] = abs(delta[i]);
    }
    steppers[i].moveTo(max(delta[i],0));
    }
  }

  void serialEvent() {
    if (Serial.available()) {
      command = Serial.parseInt();
      newCommand = true;
    }
  }


