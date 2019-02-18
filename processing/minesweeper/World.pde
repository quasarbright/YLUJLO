class World {
  Cell[][] cells;
  int w, h, numMines;
  World(Cell[][] cells) {
    this.cells = cells;
    this.w = cells[0].length;
    this.h = cells.length;
    this.numMines = this.getNumMines();
  }
  
  World(int w, int h, int numMines) {
    this.w = w;
    this.h = h;
    this.numMines = numMines;
    this.cells = new Cell[h][w];
    this.initializeCells();
  }
  
  void makeMines() {
    ArrayList<PVector> minePositions = new ArrayList<PVector>();
    while(minePositions.size() < this.numMines) {
      int x = floor(random(this.w));
      int y = floor(random(this.h));
      PVector p = new PVector(x,y);
      if(minePositions.indexOf(p) == -1){
        minePositions.add(p);
        cells[y][x] = new Mine();
      }
    }
  }
  
  void initializeCells() {
    this.makeMines();
    for(int i = 0; i < this.h; i++){
      for(int j = 0; j < this.w; j++){
        if(this.cells[i][j] == null)
          cells[i][j] = new Safe(this.getNumNeighboringBombs(j, i));
      }
    }
  }
  
  int getNumNeighboringBombs(int x, int y){
    ArrayList<Cell> neighbors = this.getNeighbors(x,y);
    int count = 0;
    for(Cell neighbor:neighbors){
      if(neighbor instanceof Mine)
        count++;
    }
    return count;
  }
  
  ArrayList<PVector> getNeighborPositions(int x, int y) {
    ArrayList<Integer> xs = new ArrayList<Integer>();
    ArrayList<Integer> ys = new ArrayList<Integer>();
    ArrayList<PVector> neighborPositions = new ArrayList<PVector>();
    xs.add(x);
    ys.add(y);
    if(x > 0){
      xs.add(x-1);
    }
    if(x < this.w-1){
        xs.add(x+1);
      }
    if(y > 0){
      ys.add(y-1);
    }
    if(y < this.h-1){
        ys.add(y+1);
      }
    for(int x_:xs){
      for(int y_:ys){
        if(x_ != x || y_!=y)
          neighborPositions.add(new PVector(x, y));
      }
    }
    return neighborPositions;
  }
  
  ArrayList<Cell> getNeighbors(int x, int y) {
    ArrayList<Integer> xs = new ArrayList<Integer>();
    ArrayList<Integer> ys = new ArrayList<Integer>();
    ArrayList<Cell> neighbors = new ArrayList<Cell>();
    xs.add(x);
    ys.add(y);
    if(x > 0){
      xs.add(x-1);
    }
    if(x < this.w-1){
        xs.add(x+1);
      }
    if(y > 0){
      ys.add(y-1);
    }
    if(y < this.h-1){
        ys.add(y+1);
      }
    for(int x_:xs){
      for(int y_:ys){
        if(x_ != x || y_!=y)
          neighbors.add(cells[y_][x_]);
      }
    }
    return neighbors;
  }
  
  // number of mines on the whole board
  int getNumMines() {
    int count = 0;
    for(Cell[] row:cells){
      for(Cell cell:row){
        if(cell instanceof Mine)
          count++;
      }
    }
    return count;
  }
  
  void show() {
    for(int i = 0; i < this.h; i++){
      for(int j = 0; j < this.w; j++){
        PVector p = new PVector(j*cellSize, i*cellSize);
        cells[i][j].drawAt(p);
      }
    }
  }
  
  void exposeAll() {
    for(Cell[] row:cells){
      for(Cell cell: row){
        cell.expose();
      }
    }
  }
  
  ////////// user interaction ////////////
  
  // vector in pixel space
  void onClick(PVector mousePosition) {
    
  }
  
  void flag(int x, int y){
    
  }
  
  //expose only that cell (and possibly trigger flood)
  void expose(int x, int y) {
    
  }
  
  //expose this cell and all non-flagged neighboring cells
  void bigExpose(int x, int y) {
    
  }
  
  void flood(int x, int y) { // check exposed for termination
    
  }
}
