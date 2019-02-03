import peasy.*;
import processing.sound.*;

PeasyCam cam;
FFT fft;
//Amplitude amp;
SoundFile file;
int bands = 512;
float[] spectrum = new float[bands];

void setup() {
  size(1000, 1000, P3D);
  colorMode(HSB);
  cam = new PeasyCam(this, 500);
  // Create an Input stream which is routed into the Amplitude analyzer
  fft = new FFT(this, bands);
  //amp = new Amplitude(this);
  file = new SoundFile(this, "Asu no Yozora Shoukaihan - Yuaru.mp3");
  
  // start the Audio Input  
  // patch the AudioIn
  fft.input(file);
  file.play();
  //amp.input(in);
  
  stroke(255);
  strokeWeight(1);
  //noStroke();
}      

void draw() { 
  background(0);
  lights();
  //sphere(100);
  graph(new SuperShape());
  fft.analyze(spectrum);
  //amp.analyze();
  //println(amp.analyze());

  //for(int i = 0; i < bands; i++){
  //// The result of the FFT is normalized
  //// draw the line for frequency band i scaling it up by 5 to get more amplitude.
  //line( i, height, i, height - spectrum[i]*height*5 );
  //}
  
  
}
