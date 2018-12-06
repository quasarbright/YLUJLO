class Graph{
  ArrayList<PVector> points;
  Graph(ArrayList<PVector> ps){
    points = ps;
  }
  
  float getEdge(int i, int j){
    return PVector.sub(points.get(i), points.get(j)).magSq();
  }
  
  void show(){
    for(PVector v: points){
      ellipse(v.x, v.y, 5, 5);
      for(PVector u: points){
        line(v.x, v.y, u.x, u.y);
      }
    }
  }
}
