Graph g;
int popsize = 100;
void setup(){
  size(800,800);
  ArrayList<PVector> points = new ArrayList<>();
  for(int i = 0; i < popsize; i++){
    points.add(new PVector(random(width), random(height)));
  }
  g = new Graph(points);
  stroke(255);
  fill(255);
  strokeWeight(2);
}

void draw(){
  background(0);
  g.show();
  g.prim();
}

void mousePressed(){
  g.points.add(new PVector(mouseX, mouseY));
  g.reset();
}
