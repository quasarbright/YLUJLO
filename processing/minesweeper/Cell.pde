int cellSize = 10;
abstract class Cell {
  boolean flagged = false;
  boolean exposed = false;
  
  abstract void drawAt(PVector pos);
  abstract void expose();
  
  void flag() {
    if(!this.exposed){
      this.flagged = !this.flagged;
    }
  }
}

class Mine extends Cell {
  void drawAt(PVector pos) {
    pushMatrix();
    fill(240,0,0);
    rect(pos.x, pos.y, cellSize, cellSize);
    popMatrix();
  }
  
  void expose() {
    this.exposed = true;
    println("game over");
  }
}

class Safe extends Cell {
  int numBombs;
  Safe(int numBombs){
    this.numBombs = numBombs;
  }
  
  void expose() {
    this.exposed = true;
  }
}
