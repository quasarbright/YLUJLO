class Graph{
  ArrayList<PVector> points;
  ArrayList<PVector> reached;
  ArrayList<PVector> unreached;
  Graph(ArrayList<PVector> ps){
    points = ps;
    for(PVector v: points){
      unreached.add(v.copy());
    }
    reached.add(unreached.remove(0));
  }
  
  float getEdge(int i, int j){
    return PVector.sub(points.get(i), points.get(j)).magSq();
  }
  
  void prim(){
    reset();
    int closestUR;
    int closestR;
    float minDist = 3.40282347E+38;
    for(int ri = 0; ri < reached.length(); ri++){
      for(int ui = 0; ui < unreached.length(); ui++) {
        if(getEdge(ri, ui) < minDist) {
          minDist = getEdge(ri, ui);
          closestUR = ui;
          closestR = ri;
        }
      }
    }
    PVector UR = unreached.get(closestUR);
    PVector R = reached.get(closestR);
    line(UR.x, UR.y, R.x, R.y);
    reached.add(unreached.remove(closestUR));
  }
  
  void show(){
    for(PVector v: points){
      ellipse(v.x, v.y, 5, 5);
    }
  }
}
