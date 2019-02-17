abstract class Cell {
  boolean flagged;
  boolean exposed;
  
  abstract void drawAt(PVector pos);
  abstract void expose();
  abstract void flag();
}

class Mine extends Cell {
  
}

class Safe extends Cell {
  
}
