int cellSize = 20;
abstract class Cell {
  boolean flagged = false;
  boolean exposed = false;
  
  abstract void drawExposed(PVector pos);
  abstract void expose();
  
  void flag() {
    if(!this.exposed){
      this.flagged = !this.flagged;
    }
  }
  
  void drawFlagged(PVector pos) {
    fill(230, 230, 50);
    rect(pos.x, pos.y, cellSize, cellSize);
  }
  
  void drawUnexposed(PVector pos) {
    fill(240);
    rect(pos.x, pos.y, cellSize, cellSize);
  }
}

class Mine extends Cell {
  void drawExposed(PVector pos) {
    pushMatrix();
    fill(210,0,0);
    rect(pos.x, pos.y, cellSize, cellSize);
    fill(0,0,0);
    ellipse(pos.x + cellSize / 2, pos.y + cellSize / 2, 
      cellSize * 5 / 8, cellSize * 5 / 8);
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
  
  void drawExposed(PVector pos) {
    pushMatrix();
    //noStroke();
    //fill(0,0);
    //rect(pos.x, pos.y, cellSize, cellSize);
    fill(240);
    textSize(15);
    textAlign(CENTER, CENTER);
    text("" + numBombs, pos.x + cellSize * 0.5, pos.y + cellSize * 0.4);
    popMatrix();
  }
}
