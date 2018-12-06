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
  
  float getEdge(int rind, int urind){
    return PVector.sub(reached.get(rind), unreached.get(urind)).magSq();
  }
  
  
  void show(){
    for(PVector v: points){
      ellipse(v.x, v.y, 5, 5);
    }
  }
}
