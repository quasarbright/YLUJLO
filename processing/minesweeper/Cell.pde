int cellSize = 10;
abstract class Cell {
  boolean flagged = false;
  boolean exposed = false;
  
  abstract void drawAt(PVector pos);
  abstract void expose();
  abstract void flag();
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
  
  void flag() {
    if(!this.exposed){
      this.flagged = !this.flagged;
    }
  }
}

class Safe extends Cell {
  
}
