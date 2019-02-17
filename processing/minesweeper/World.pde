int numMines = 10;
class World {
  Cell[][] cells;
  int w, h;
  World(Cell[][] cells) {
    this.cells = cells;
    this.w = cells[0].length;
    this.h = cells.length;
  }
  
  World(int w, int h) {
    this.w = w;
    this.h = h;
    this.cells = new Cell[h][w];
    this.initializeCells();
  }
  
  void initializeCells() {
    ArrayList<PVector> minePositions = new ArrayList<PVector>();
    while(minePositions.size() < numMines) {
      int x = floor(random(this.w));
      int y = floor(random(this.h));
      PVector p = new PVector(x,y);
      if(minePositions.indexOf(p) == -1){
        cells[y][x] = new Mine();
      }
    }
  }
  
  
}
