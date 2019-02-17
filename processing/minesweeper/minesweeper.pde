World world;
int numMines = 10;
int cellSize = 10;
void setup() {
  size(500,500);
  world = new World(5, 5, 10);
}

void draw() {
  background(51);
  stroke(51);
  fill(240);
  rect(100,100,100,100);
}
