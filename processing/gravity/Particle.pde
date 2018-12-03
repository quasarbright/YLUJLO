float g = 1;
float maxVel = 20;

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
    PVector force = disp.copy().setMag(g);
    return force;
  }
  
  void pullTo(){
    PVector mouse;
    mouse = new PVector(mouseX, mouseY);
    acceleration = calcForce(mouse);
    // set acceleration towards mouse and set the magnitude to g
  }
  
  void update(){
    velocity.limit(maxVel);
    pullTo();
    position.add(velocity);
    velocity.add(acceleration);
    velocity.limit(maxVel);
    // pull to mouse
    // add velocity to position
    // add acceleration to velocity
    // limit velocity
  }
  
  void checkBounds(){
    position.x = constrain(position.x, 0, width);
    position.y = constrain(position.y, 0, height);
  }
  
  void show(){
    stroke(c);
    point(position.x, position.y);
  }
}
