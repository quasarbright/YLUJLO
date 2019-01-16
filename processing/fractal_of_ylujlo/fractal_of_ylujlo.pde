PImage img;
// the complex plane from -amax-amax*i to amax+amax*i will be displayed
float amax = 2;
int maxIterations = 100;
void setup() {
  img = loadImage("virgil.jpg");
  img.loadPixels();
  size(600,600);
  // Images must be in the "data" directory to load correctly
}

void draw() {
  loadPixels();
  PVector mouse = new PVector(mouseX, mouseY);
  Complex c = pxToComplex(mouse);
  for(int x = 0; x < width; x++){
    for(int y = 0; y < height; y++){
      PVector p = new PVector(x, y);
      Complex z0 = pxToComplex(p);
      Complex zland = landingPoint(z0, c);
      PVector pland = complexToPx(zland);
      int xland, yland, landInd;
      xland = floor(pland.x);
      yland = floor(pland.y);
      landInd = constrain(xland+width*yland, 0, width*height -1);
      pixels[floor(p.x + width * p.y)] = img.pixels[landInd];
      //if(doesExplode(z0,c,maxIterations)){
      //  pixels[floor(p.x + width * p.y)] = color(255);
      //}
    }
  }
  updatePixels();
}

class Complex{
  float a, b;
  Complex(float a, float b){
    this.a = a;
    this.b = b;
  }
  
  Complex square(){
    return new Complex(a*a-b*b, 2*a*b);
  }
  
  Complex sum(Complex other){
    return new Complex(a + other.a, b + other.b);
  }
  
  float magSq() {
    return a*a+b*b;
  }
  
  Complex clone(){
    return new Complex(a, b);
  }
}

Complex pxToComplex(PVector px){
  float a, b;
  a = map(px.x, 0, width, -amax, amax);
  b = map(px.y, 0, height, amax, -amax);
  return new Complex(a, b);
}

PVector complexToPx(Complex z){
  float x, y;
  x = map(z.a, -amax, amax, 0, width);
  y = map(z.b, -amax, amax, height, 0);
  return new PVector(x, y);
}

Complex landingPoint(Complex z, Complex c){
  Complex zn = z.clone();
  for(int i = 0; i < maxIterations; i++){
    zn = zn.square().sum(c);
    if(zn.magSq() > 4.0){
      break;
    }
  }
  return zn;
}

boolean doesExplode(Complex z, Complex c, int maxIterations){
  Complex zn = z.clone();
  for(int i = 0; i < maxIterations; i++){
    zn = zn.square().sum(c);
    if(zn.magSq() > 4.0){
      return true;
    }
  }
  return false;
}
