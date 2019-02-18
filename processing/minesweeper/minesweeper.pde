World world;
int numMines = 10;
int cellSize = 50;
void setup() {
  size(500,500);
  world = new World(5, 5, 10);
}

void draw() {
  background(51);
  stroke(51);
  strokeWeight(5);
  fill(240);
  //PVector pos = new PVector(250, 250);
  //int cellSize = 20;
  //int numBombs = 5;
  world.exposeAll();
  world.show();
}
