class Graph {
  ArrayList<PVector> points = new ArrayList<PVector>();
  ArrayList<PVector> reached = new ArrayList<PVector>();
  ArrayList<PVector> unreached = new ArrayList<PVector>();
  Graph(ArrayList<PVector> ps) {
    points = ps;
    reset();
  }

  void reset() {
    reached = new ArrayList<PVector>();
    unreached = new ArrayList<PVector>();
    for (PVector v : points) {
      unreached.add(v.copy());
    }
    reached.add(unreached.remove(0));
  }

  float getEdge(int rind, int urind) {
    return PVector.sub(reached.get(rind), unreached.get(urind)).magSq();
  }

  void prim() {
    reset();
    while (unreached.size() > 0) {
      int closestUR = 0;
      int closestR = 0;
      float minDist = 3.40282347E+38;
      for (int ri = 0; ri < reached.size(); ri++) {
        for (int ui = 0; ui < unreached.size(); ui++) {
          if (getEdge(ri, ui) < minDist) {
            minDist = getEdge(ri, ui);
            closestUR = ui;
            closestR = ri;
          }
        }
      }
      PVector UR = unreached.get(closestUR);
      PVector R = reached.get(closestR);
      println(closestUR);
      line(UR.x, UR.y, R.x, R.y);
      reached.add(unreached.remove(closestUR));
    }
  }

  void show() {
    for (PVector v : points) {
      ellipse(v.x, v.y, 5, 5);
    }
  }
}
