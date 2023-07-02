const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const BACKGROUND_COLOR = 230;
const EPSILON = 1e-6;
let objects = [];
let numObjectsDiv;
let OBJECT_TYPES;

class Obj {
  constructor() {
    this.selected = false;
    this.disabled = false;
  }

  setDisable(disabled) {
    this.disabled = disabled;
  }

  setSelect(selected) {
    if (!this.disabled) {
      this.selected = selected;

      // DEBUG
      console.log(this);
    }
  }

  draw() {
    if (!this.disabled)
      this.drawImpl();
  }
}

class Vertex extends Obj {
  static RADIUS = 4;
  static RADIUS_SQ = Vertex.RADIUS * Vertex.RADIUS;
  static STROKE;
  static STROKE_WEIGHT = 3;
  static HOVER_RADIUS = 6;
  static COLOR;
  static selectedVertex = null;

  constructor(x, y) {
    super();
    this.x = x;
    this.y = y;
  }

  getX() {
    return this.x;
  }

  getY() {
    return this.y;
  }

  drawImpl() {
    this.drawWithColor(Vertex.COLOR);
  }

  drawWithColor(color) {
    push();
    if (this.selected)
      stroke(Vertex.STROKE);
    else
      stroke(color);
    strokeWeight(Vertex.STROKE_WEIGHT);
    const radius = this.inHover() ? Vertex.HOVER_RADIUS : Vertex.RADIUS;
    fill(color);
    circle(this.getX(), this.getY(), radius * 2);
    pop();
  }

  inHover() {
    if (this.disabled)
      return false;
    const distVec = createVector(this.getX() - mouseX, this.getY() - mouseY);
    return distVec.magSq() <= Vertex.RADIUS_SQ;
  }

  closeTo(v) {
    return Math.abs(this.getX() - v.getX()) < EPSILON &&
           Math.abs(this.getY() - v.getY()) < EPSILON;
  }

  static addObject(objects) {
    const v = new Vertex(mouseX, mouseY);
    objects.push(v);
    return v;
  }

  static setVertexToMove(objects) {
    for (const object of objects) {
      if (object instanceof Vertex && !(object instanceof Intersection) &&
          object.inHover()) {
        if (Vertex.selectedVertex)
          Vertex.selectedVertex.setSelect(false);
        Vertex.selectedVertex = object;
        Vertex.selectedVertex.setSelect(true);
      }
    }
    return null;
  }

  static unsetVertexToMove(objects) {
    if (Vertex.selectedVertex) {
      Vertex.selectedVertex.setSelect(false);
      Vertex.selectedVertex = null;
    }
  }

  static move(objects) {
    if (Vertex.selectedVertex) {
      Vertex.selectedVertex.x = mouseX;
      Vertex.selectedVertex.y = mouseY;
    }
  }
}

class Line extends Obj {
  static STROKE;
  static STROKE_WEIGHT = 2;
  static selectedVertex = null;

  constructor(v1, v2) {
    super();
    this.v1 = v1;
    this.v2 = v2;
  }

  drawImpl() {
    push();
    stroke(Line.STROKE);
    strokeWeight(Line.STROKE_WEIGHT);
    const dx = this.v1.getX() - this.v2.getX();
    const dy = this.v1.getY() - this.v2.getY();
    if (abs(dx) > abs(dy)) {
      line(0,
           this.v1.getY() - this.v1.getX() * dy / dx,
           CANVAS_WIDTH,
           this.v2.getY() + (CANVAS_WIDTH - this.v2.getX()) * dy / dx);
    } else {
      line(this.v1.getX() - this.v1.getY() * dx / dy,
           0,
           this.v2.getX() + (CANVAS_HEIGHT - this.v2.getY()) * dx / dy,
           CANVAS_HEIGHT);
    }
    pop();
  }

  closeTo(l) {
    function colinear(v1, v2, v3) {
      return Math.abs(
          (v2.getY() - v1.getY()) * (v3.getX() - v2.getX()) -
          (v3.getY() - v2.getY()) * (v2.getX() - v1.getX())) < EPSILON;
    }
    return colinear(this.v1, this.v2, l.v1) && colinear(this.v2, l.v1, l.v2);
  }

  static addObject(objects) {
    let l = null;
    for (const object of objects) {
      if (object instanceof Vertex && object.inHover()) {
        if (Line.selectedVertex) {
          if (Line.selectedVertex !== object) {
            l = new Line(Line.selectedVertex, object);
            objects.push(l);
          }
          Line.selectedVertex.setSelect(false);
          Line.selectedVertex = null;
        } else {
          Line.selectedVertex = object;
          Line.selectedVertex.setSelect(true);
        }
      }
    }
    return l;
  }
}

class Circle extends Obj {
  static STROKE = 0;
  static STROKE_WEIGHT = 2;
  static selectedVertex = null;

  constructor(v1, v2) {
    super();
    this.v1 = v1;
    this.v2 = v2;
  }

  drawImpl() {
    push();
    stroke(Circle.STROKE);
    strokeWeight(Circle.STROKE_WEIGHT);
    noFill();
    const distVec = createVector(this.v1.getX() - this.v2.getX(),
                                 this.v1.getY() - this.v2.getY());
    circle(this.v1.getX(), this.v1.getY(), distVec.mag() * 2);
    pop();
  }

  closeTo(c) {
    function rSq(o) {
      const dx = o.v1.getX() - o.v2.getX(), dy = o.v1.getY() - o.v2.getY();
      return dx * dx + dy * dy;
    }
    return this.v1.closeTo(c.v1) && Math.abs(rSq(this) - rSq(c)) < EPSILON;
  }

  static addObject(objects) {
    let c = null;
    for (const object of objects) {
      if (object instanceof Vertex && object.inHover()) {
        if (Circle.selectedVertex) {
          if (Circle.selectedVertex !== object) {
            c = new Circle(Circle.selectedVertex, object);
            objects.push(c);
          }
          Circle.selectedVertex.setSelect(false);
          Circle.selectedVertex = null;
        } else {
          Circle.selectedVertex = object;
          Circle.selectedVertex.setSelect(true);
        }
      }
    }
    return c;
  }
}

class Intersection extends Vertex {
  static INF_X = CANVAS_WIDTH * 2;
  static INF_Y = CANVAS_HEIGHT * 2;
  static COLOR;

  constructor() {
    super(null, null);
  }

  draw() {
    this.drawWithColor(Intersection.COLOR);
  }

  getX() {
    return this.calc()[0];
  }

  getY() {
    return this.calc()[1];
  }

  static check(o1, o2) {
    if (o1 instanceof Vertex || o2 instanceof Vertex)
      return [];
  
    if (o1 instanceof Line) {
      const t = o1;
      o1 = o2;
      o2 = t;
    }

    if (o1 instanceof Line) {
      return [new LinesIntersection(o1, o2)];
    } else if (o2 instanceof Line) {
      return [
          new LineCircleIntersection(o2, o1, true),
          new LineCircleIntersection(o2, o1, false)];
    } else {
      return [
          new CirclesIntersection(o1, o2, true),
          new CirclesIntersection(o1, o2, false)];
    }
  }
}

class LinesIntersection extends Intersection {
  constructor(l1, l2) {
    super();
    this.l1 = l1;
    this.l2 = l2;
  }

  static getLineCoeffs(l) {
    return [l.v2.getY() - l.v1.getY(), l.v1.getX() - l.v2.getX(),
            l.v1.getX() * l.v2.getY() - l.v2.getX() * l.v1.getY()];
  }

  calc() {
    const l1 = LinesIntersection.getLineCoeffs(this.l1);
    const l2 = LinesIntersection.getLineCoeffs(this.l2);
    const den = l1[0] * l2[1] - l2[0] * l1[1];
    if (den == 0)
      return [Intersection.INF_X, Intersection.INF_Y];
    return [(l2[1] * l1[2] - l1[1] * l2[2]) / den,
            (l1[0] * l2[2] - l2[0] * l1[2]) / den];
  }
}

class LineCircleIntersection extends Intersection {
  constructor(l, c, first) {
    super();
    this.l = l;
    this.c = c;
    this.first = first;
  }

  calc() {
    const dx = this.l.v2.x - this.l.v1.x;
    const dy = this.l.v2.y - this.l.v1.y;
    const a = dx * dx + dy * dy;
    const dx2 = this.l.v1.x - this.c.v1.x;
    const dy2 = this.l.v1.y - this.c.v1.y;
    const b = 2 * (dx * dx2 + dy * dy2);
    const dx3 = this.c.v2.x - this.c.v1.x;
    const dy3 = this.c.v2.y - this.c.v1.y;
    const c = dx2 * dx2 + dy2 * dy2 - dx3 * dx3 - dy3 * dy3;

    let det = b * b - 4 * a * c;
    if (det < -EPSILON)
      return [Intersection.INF_X, Intersection.INF_Y];
    det = max(det, 0);
    let t = -b;
    if (this.first)
      t += Math.sqrt(det);
    else
      t -= Math.sqrt(det);
    t /= 2 * a;
    return [this.l.v1.x + t * dx, this.l.v1.y + t * dy];
  }
}

class CirclesIntersection extends Intersection {
  constructor(c1, c2, first) {
    super();
    this.c1 = c1;
    this.c2 = c2;
    this.first = first;
  }

  calc() {
    function sqDiff(a, b) {
      return a * a - b * b;
    }

    function rSq(a, b) {
      return a * a + b * b;
    }

    const x2Diff = sqDiff(this.c1.v1.x, this.c2.v1.x);
    const y2Diff = sqDiff(this.c1.v1.y, this.c2.v1.y);
    const r2Diff = sqDiff(
        rSq(this.c1.v1.x - this.c1.v2.x, this.c1.v1.y - this.c1.v2.y),
        rSq(this.c2.v1.x - this.c2.v2.x, this.c2.v1.y - this.c2.v2.y));
    const z = x2Diff + y2Diff - r2Diff;

    let x1, y1, x2, y2;
    const dx = this.c1.v1.x - this.c2.v1.x;
    const dy = this.c1.v1.y - this.c2.v1.y;
    if (dx == 0) {
      if (dy == 0) {
        return [Intersection.INF_X, Intersection.INF_Y];
      } else {
        x1 = 0;
        y1 = 1;
        y1 = y2 = z / (2 * dy);
      }
    } else if (dy == 0) {
      x1 = x2 = z / (2 * dx);
      y1 = 0;
      y2 = 1;
    } else {
      x1 = z / (2 * dx);
      y1 = 0;
      x2 = 0;
      y2 = z / (2 * dy);
    }

    const l = new Line(new Vertex(x1, y1), new Vertex(x2, y2));
    return (new LineCircleIntersection(l, this.c1, this.first)).calc();
  }
}

let toolSelect = null;
function setup() {
  createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
  Vertex.COLOR = color(0, 0, 255);
  Vertex.STROKE = color(255, 0, 0);
  Line.STROKE = 0;
  Intersection.COLOR = 0;
  toolSelect = select("#tool");
  numObjectsDiv = select("#numObjects");
  OBJECT_TYPES = [Line, Circle, Vertex];
}

function applyHandler(handlers) {
  const handler = handlers[toolSelect.value()];
  if (handler)
    return handler(objects);
  return null;
}

function mouseInCanvas() {
  return mouseX >= 0 && mouseX < CANVAS_WIDTH &&
         mouseY >= 0 && mouseY < CANVAS_HEIGHT;
}

const mousePressedHandlers = {
  "move": Vertex.setVertexToMove,
  "vertex": Vertex.addObject,
  "line": Line.addObject,
  "circle": Circle.addObject,
};

function mousePressed() {
  if (!mouseInCanvas())
    return;
  const o1 = applyHandler(mousePressedHandlers);
  if (o1) {
    const newObjects = [];
    for (let i = 0; i < objects.length - 1; ++i) {
      const o2 = objects[i];
      for (const o of Intersection.check(o1, o2))
        newObjects.push(o);
    }
    for (const o of newObjects)
      objects.push(o);
  }
}

const mouseReleasedHandlers = {
  "move": Vertex.unsetVertexToMove
};

function mouseReleased() {
  if (!mouseInCanvas())
    return;
  applyHandler(mouseReleasedHandlers);
}

const mouseIsPressedHandlers = {
  "move": Vertex.move
};

function draw() {
  if (mouseIsPressed && mouseInCanvas())
    applyHandler(mouseIsPressedHandlers);

  background(BACKGROUND_COLOR);
  // TODO: come up with a better solution to draw everything in order
  for (const type of OBJECT_TYPES) {
    const curObjs = [];
    for (const o1 of objects) {
      if (o1 instanceof type) {
        let disabled = false;
        for (const o2 of curObjs) {
          if (o2.closeTo(o1)) {
            disabled = true;
            break;
          }
        }
        if (!disabled) {
          curObjs.push(o1);
          o1.draw();
        }
        o1.setDisable(disabled);
      }
    }
  }
  

  numObjectsDiv.html(`Number of objects: ${objects.length}`);
}

function clearObjects() {
  objects = [];
}
