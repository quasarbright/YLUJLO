World world;
int numMines;
int cellSize;
void setup() {
  size(500,500);
  int worldSize = 16;
  numMines = floor(worldSize*worldSize * .2);
  world = new World(worldSize, worldSize, numMines);
  cellSize = width/worldSize;
}

void draw() {
  background(51);
  stroke(51);
  strokeWeight(5);
  fill(240);
  world.show();
}

enum Actions {
  EXPOSE, FLAG, BIGEXPOSE;
}

void mouseClicked() {
  PVector p = new PVector(mouseX, mouseY);
  if(mouseButton==RIGHT){
    world.onClick(p, Actions.FLAG);
  } else if(keyPressed){
    if(keyCode == CONTROL){
      world.onClick(p, Actions.FLAG);
    } else if(keyCode == SHIFT){
      world.onClick(p, Actions.BIGEXPOSE);
    }
  } else {
    world.onClick(p, Actions.EXPOSE);
  }
}
