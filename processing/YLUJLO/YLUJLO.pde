int hu;
void setup(){
  size(400,400);
  colorMode(HSB);
  hu = 0;
}
void draw(){
  background(hu,255,255);
  textSize(64);
  fill((hu+128) % 256, 255, 255);
  text("YLUJLO", 100,200);
  hu++;
  hu = hu % 256;
}
