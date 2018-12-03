float g = 1;
float maxVel = 10;

class Particle{
  PVector position, velocity, acceleration;
  color c;
  
  Particle(){
    position = new PVector(random(width), random(height)); // rand pos
    velocity = PVector.fromangle(random(TWO_PI)).mult(maxVel); // rand vel
    acceleration = new PVector(0, 0); // no acc
    c = color(random(255), 255, 255); // rand color
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
    
  }
}
