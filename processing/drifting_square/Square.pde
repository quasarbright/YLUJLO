class Square{
  PVector position;
  PVector velocity;
  float w;
  float h;
  color c;

  Square(){
    position = new PVector(200, 200);
    velocity = new PVector(17, 23);
    w = 30;
    h = 30;
    colorMode(HSB);
    c = color(random(255), 255, 255);

  }

  void update(){
    position.add(velocity);
    checkBounds();

  }

  void checkBounds(){
    if((position.x == width) || (position.x == 0)) {
      velocity.x = -1 * velocity.x;
    }
    if((position.y == width) || (position.y == 0)) {
      velocity.y = -1 * velocity.y;
    }
    changeColor();

  }

  void changeColor(){
    c = color(random(255), 255, 255);

  }

  void show(){
    fill(c);
    rect(position.x, position.y, w, h);
  }
}
