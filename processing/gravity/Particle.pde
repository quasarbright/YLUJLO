float g = 1;
float maxVel = 10;

class Particle{
  PVector position, velocity, acceleration;
  color c;
  
  Particle(){
    // rand pos
    // rand vel
    // no acc
    // rand color
    PVector.fromAngle(random(TWO_PI)).mult(maxVel);
  }
  
  PVector calcForce(PVector target){
    PVector disp = PVector.sub(target, position);
    float magsq = disp.magSq();
    float fmag = g/magsq;
    PVector force = disp.copy().setMag(fmag);
    return force;
  }
  
  void pullTo(){
    // set acceleration towards mouse and set the magnitude to g
  }
  
  void update(){
    // pull to mouse
    // add velocity to position
    // add acceleration to velocity
    // limit velocity
  }
  
  void show(){
    stroke(c);
    point(position.x, position.y);
  }
}
