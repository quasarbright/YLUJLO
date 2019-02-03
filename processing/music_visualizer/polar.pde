int numtheta = 25;
float dtheta = TWO_PI / (1.0*numtheta);
int numphi = 100;
float dphi = TWO_PI / (1.0*numphi);
public interface PolarFunc {
  float apply(float theta, float phi);
}

void graph(PolarFunc f) {
  fft.analyze(spectrum);
  //ArrayList<PVector> globe = new ArrayList<>();
  for(float theta = 0; theta <= TWO_PI; theta += dtheta) {
    beginShape(TRIANGLE_STRIP);
    for(float phi = 0; phi <= PI; phi += dphi) {
      
      float r, x, y, z;
      r = f.apply(theta, phi);
      x = r * sin(phi) * cos(theta);
      y = r * sin(phi) * sin(theta);
      z = r * cos(phi);
      PVector a = new PVector(x, y, z);
      x = r * sin(phi+dphi) * cos(theta);
      y = r * sin(phi+dphi) * sin(theta);
      z = r * cos(phi+dphi);
      PVector b = new PVector(x, y, z);
      x = r * sin(phi+dphi) * cos(theta+dtheta);
      y = r * sin(phi+dphi) * sin(theta+dtheta);
      z = r * cos(phi+dphi);
      PVector c = new PVector(x, y, z);
      x = r * sin(phi) * cos(theta+dtheta);
      y = r * sin(phi) * sin(theta+dtheta);
      z = r * cos(phi);
      PVector d = new PVector(x, y, z);
      float hu = map(theta, 0, TWO_PI, 0, 255) + map(phi, 0, TWO_PI, 0, 255);
      hu += (millis()) / 10.0;
      hu = hu % 256;
      //hu = 255;
      fill(hu, 255, 255);
      //stroke(hu, 255, 255);
      vertex(a.x, a.y, a.z);
      //vertex(b.x, b.y, b.z);
      //vertex(c.x, c.y, c.z);
      vertex(d.x, d.y, d.z);
      //vertex(a.x, a.y, a.z);
      
    }
    endShape();
  }
}

class R implements PolarFunc{
  float apply(float theta, float phi) {
    return 100;//*sin(theta)*sin(theta) + sin(phi)*sin(phi);
  }
}

float supershape(float theta, float m, float n1, float n2, float n3) {
  float t1 = abs((1)*cos(m * theta / 4));
  t1 = pow(t1, n2);
  float t2 = abs((1)*sin(m * theta/4));
  t2 = pow(t2, n3);
  float t3 = t1 + t2;
  float r = pow(t3, - 1 / n1);
  return r;
}

class SuperShape implements PolarFunc{
  float apply(float theta, float phi) {
    // not rings
    int index = floor(map(2+sin(theta)+sin(phi), 0, 4, bands/4, bands/3));
    // rings
    //int index = floor(map(phi, 0, PI, bands/4, bands/3));
    // slices
    //int index = floor(map(1+sin(theta), 0, 2, bands/4, bands/3));
    //println(index, phi);
    float amplitude = spectrum[index];
    //println(amplitude);
    return 100 + 1000 * sqrt(amplitude);
    //return 1 * supershape(theta, 1.01, 0.2, 1.7, 10.7) * (supershape(phi, 5, 0.5, 10.6, 1.7)) + 1000 * sqrt(amplitude);
  }
}
