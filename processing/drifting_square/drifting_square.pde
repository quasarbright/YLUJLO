Square square;
void setup(){
  size(400,400);
  square = new Square();
}

void draw(){
  background(0);
  square.update();
  square.show();
}
