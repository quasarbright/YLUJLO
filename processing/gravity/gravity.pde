Particle particle;
void setup(){
  size(800,800);
  particle = new Particle();
}

void draw(){
  background(0);
  particle.update();
  particle.show();
}
