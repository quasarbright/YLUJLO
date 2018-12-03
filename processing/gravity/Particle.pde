float g = 1;
float maxVel = 10;

class Particle{
  PVector position, velocity, acceleration;
  color c;
  
  Particle(){
    position = new PVector(random(width), random(height)); // rand pos
    velocity = PVector.fromAngle(random(TWO_PI)).mult(maxVel); // rand vel
    acceleration = new PVector(0, 0); // no acc
    c = color(random(255), 255, 255); // rand color
  }
  
  PVector calcForce(PVector target){
    PVector disp = PVector.sub(target, position);
    float magsq = disp.magSq();
    float fmag = g/magsq;
    PVector force = disp.copy().setMag(fmag);
    return force;
  }
  
  void pullTo(){
    PVector mouse;
    mouse = new PVector(mouseX, mouseY);
    acceleration = calcForce(mouse);
    // set acceleration towards mouse and set the magnitude to g
  }
  
  void update(){
    pullTo();
    position.add(velocity);
    velocity.add(acceleration);
    velocity.limit(maxVel);
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
