int popsize = 5000;
Particle[] particles;
void setup(){
  size(800,800);
  colorMode(HSB);
  particles = new Particle[popsize];
  for(int i = 0; i < popsize; i++){
    particles[i] = new Particle();
  }
  strokeWeight(1);
}

void draw(){
  background(0);
  for(Particle particle: particles){
    particle.update();
    particle.show();
  }
}
