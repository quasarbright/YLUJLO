let vertices = []

function setup() {
    createCanvas(800, 600, WEBGL);
    for (let i = 0; i < 1; i++) {
        vertices.push(randomVector())
    }
}
function randomVector(){
  return createVector(random(-height,height), random(-height,height), random(-height,height)).limit(height)
}

function mousePressed() {
    vertices.push(createVector(mouseX, mouseY))
    loop()
}

function clearVertices(){
    vertices = []
    loop()
}

function draw() {
    if(frameCount % 6 == 0 && frameRate() > 60){
      // vertices.pop()
      vertices.push(randomVector())
    }
    // background(51);
    translate(0, 0, -800)
    rotateX(.5*millis()/1000.0)
    rotateY(.5*.25*millis()/1000.0)
    rotateZ(.5*.5*millis()/1000.0)

    let reached = []
    let unreached = vertices.map((e) => e) //copy

    reached.push(unreached[0])
    unreached.splice(0, 1)

    while (unreached.length > 0) {
        let record = Infinity
        let rind;
        let uind;

        for (var i = 0; i < reached.length; i++) {
            for (var j = 0; j < unreached.length; j++) {
                let v1 = reached[i]
                let v2 = unreached[j]
                let d = p5.Vector.dist(v1, v2)

                if (d < record) {
                    record = d
                    rind = i
                    uind = j
                }
            }
        }
        stroke(255)
        strokeWeight(2)
        line3d(reached[rind], unreached[uind])
        reached.push(unreached[uind])
        unreached.splice(uind,1)
    }

    for (v of vertices) {
        stroke(255)
        strokeWeight(10)
        point3d(v, v)
    }
    stroke(255,0,0)
    strokeWeight(10)
    point3d(vertices[0])
    // noLoop()
}

function line3d(u, v){
  beginShape()
  vertex(u.x, u.y, u.z)
  vertex(v.x, v.y, v.z)
  endShape()
}

function point3d(u){
  push()
  translate(u.x, u.y, u.z)
  sphere(5)
  pop()
}
