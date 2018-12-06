import peasy.*;

PeasyCam cam;

Graph g;
int popsize = 1;
boolean shouldSpawn = true;
void setup(){
  fullScreen(P3D);
  cam = new PeasyCam(this, 2500);
  ArrayList<PVector> points = new ArrayList<PVector>();
  for(int i = 0; i < popsize; i++){
    points.add(randomVector());
  }
  g = new Graph(points);
  stroke(255);
  fill(255);
  strokeWeight(2);
}

PVector randomVector(){
  return new PVector(random(-height, height), random(-height, height), random(-height, height)).limit(height);
}

void draw(){
  background(0);
  rotateY(millis()/1000.0);
  rotateX(.5*millis()/1000.0);
  rotateZ(-.25*millis()/1000.0);
  g.show();
  g.prim();
  if(frameCount % 6 == 0 && shouldSpawn){
    g.points.add(randomVector());
  }
}

void keyPressed(){
  if(key == ' '){
    g.points.add(randomVector());
  } else {
    shouldSpawn = !shouldSpawn;
  }
}
