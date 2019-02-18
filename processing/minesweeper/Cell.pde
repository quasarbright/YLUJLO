abstract class Cell {
  boolean flagged = false;
  boolean exposed = false;

  abstract void drawExposed(PVector pos);

  void flag() {
    if(!this.exposed){
      this.flagged = !this.flagged;
    }
  }
  
  void expose() {
    if(!this.flagged) this.exposed = true;
  }
  
  void drawAt(PVector pos) {
    if (this.flagged) drawFlagged(pos);
    else if (this.exposed) drawExposed(pos);
    else drawUnexposed(pos);
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
    noStroke();
    fill(210,0,0);
    rect(pos.x, pos.y, cellSize, cellSize);
    fill(0,0,0);
    ellipse(pos.x + cellSize / 2, pos.y + cellSize / 2,
      cellSize * 1 /3 , cellSize * 1 / 3);
    popMatrix();
  }
  
}

class Safe extends Cell {
  int numBombs;
  Safe(int numBombs){
    this.numBombs = numBombs;
  }

  void drawExposed(PVector pos) {
    pushMatrix();
    //noStroke();
    //fill(0,0);
    //rect(pos.x, pos.y, cellSize, cellSize);
    if (numBombs != 0) {
      PFont font;
      font = loadFont("Monaco-48.vlw");
      fill(240);
      textFont(font, 20 * cellSize / 50);
      textAlign(CENTER, CENTER);
      text("" + numBombs, pos.x + cellSize * 0.5, pos.y + cellSize * 0.5);
    }
    popMatrix();
  }
}
