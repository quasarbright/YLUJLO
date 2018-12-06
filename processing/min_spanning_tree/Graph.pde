class Graph{
  ArrayList<PVector> points;
  ArrayList<PVector> reached;
  ArrayList<PVector> unreached;
  Graph(ArrayList<PVector> ps){
    points = ps;
    reset();
  }
  
  void reset(){
    for(PVector v: points){
      unreached.add(v.copy());
    }
    reached.add(unreached.remove(0));
  }
  
  float getEdge(int i, int j){
    return PVector.sub(points.get(i), points.get(j)).magSq();
  }
  
  void show(){
    for(PVector v: points){
      ellipse(v.x, v.y, 5, 5);
    }
  }
}
