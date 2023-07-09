const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const BACKGROUND_COLOR = 230;
const EPSILON = 1e-6;
let objects = [];
let vertexTable = {};
let conditions = [];
let numObjectsDiv;
let labelInput;
let conditionInput;
let conditionTable;
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
    // DEBUG
    if (selected && this instanceof Vertex)
      console.log(`(${this.getX()}, ${this.getY()})`);

    if (!this.disabled)
      this.selected = selected;
  }

  draw() {
    // DEBUG
    // if (!this.disabled)
    if (!this.disabled || this.forceDraw)
      this.drawImpl();
  }
}

class Vertex extends Obj {
  static RADIUS = 4;
  static RADIUS_SQ = Vertex.RADIUS * Vertex.RADIUS;
  static STROKE;
  static STROKE_WEIGHT = 3;
  static HOVER_RADIUS = 6;
  static LABEL_X_DIFF = 10;
  static LABEL_Y_DIFF = -10;
  static LABEL_SIZE = 14;
  static LABEL_COLOR = 0;
  static LABEL_STROKE_WEIGHT = 1;
  static COLOR;
  static selectedVertex = null;

  constructor(x, y) {
    super();
    this.x = x;
    this.y = y;
    this.label = null;
  }

  getX() {
    return this.x;
  }

  getY() {
    return this.y;
  }

  setLabel(label) {
    this.label = label;
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

    if (this.label) {
      fill(Vertex.LABEL_COLOR);
      stroke(Vertex.LABEL_COLOR);
      strokeWeight(Vertex.LABEL_STROKE_WEIGHT);
      textSize(Vertex.LABEL_SIZE);
      text(this.label,
           this.getX() + Vertex.LABEL_X_DIFF,
           this.getY() + Vertex.LABEL_Y_DIFF);
    }

    pop();
  }

  inHover() {
    if (this.disabled)
      return false;
    const distVec = createVector(this.getX() - mouseX, this.getY() - mouseY);
    return distVec.magSq() <= Vertex.RADIUS_SQ;
  }

  closeTo(v) {
    // DEBUG
    /*
    return Math.abs(this.getX() - v.getX()) < EPSILON &&
           Math.abs(this.getY() - v.getY()) < EPSILON;
    */
    return round(this.getX()) == round(v.getX()) &&
           round(this.getY()) == round(v.getY());
  }

  static addObject(objects) {
    const v = new Vertex(mouseX, mouseY);
    objects.push(v);
    return v;
  }

  static selectVertex(objects) {
    for (const object of objects) {
      if (object instanceof Vertex && object.inHover()) {
        if (Vertex.selectedVertex)
          Vertex.selectedVertex.setSelect(false);
        if (Vertex.selectedVertex !== object) {
          Vertex.selectedVertex = object;
          Vertex.selectedVertex.setSelect(true);
        } else {
          Vertex.selectedVertex = null;
        }
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
    this.vcache = null;
    this.icache = null;
  }

  draw() {
    this.drawWithColor(Intersection.COLOR);
  }

  calcWithCache() {
    let outOfDate = false;
    if (this.icache !== null && this.vcache !== null) {
      const newVertices = this.getVertices();
      if (newVertices.length != this.vcache.length) {
        outOfDate = true;
      } else {
        for (let i = 0; i < this.vcache.length; ++i) {
          if (this.vcache[i] != newVertices[i]) {
            outOfDate = true;
            break;
          }
        }
      }
    } else {
      outOfDate = true;
    }
    if (outOfDate) {
      this.vcache = this.getVertices();
      this.icache = this.calc();
    }
    return this.icache;
  }

  getX() {
    return this.calcWithCache()[0];
  }

  getY() {
    return this.calcWithCache()[1];
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

  getVertices() {
    const vertices = [];
    for (const l of [this.l1, this.l2]) {
      for (const v of [l.v1, l.v2]) {
        vertices.push(v.getX());
        vertices.push(v.getY());
      }
    }
    return vertices;
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

  getVertices() {
    const vertices = [];
    for (const obj of [this.l, this.c]) {
      for (const v of [obj.v1, obj.v2]) {
        vertices.push(v.getX());
        vertices.push(v.getY());
      }
    }
    return vertices;
  }

  calc() {
    const dx = this.l.v2.getX() - this.l.v1.getX();
    const dy = this.l.v2.getY() - this.l.v1.getY();
    const a = dx * dx + dy * dy;
    const dx2 = this.l.v1.getX() - this.c.v1.getX();
    const dy2 = this.l.v1.getY() - this.c.v1.getY();
    const b = 2 * (dx * dx2 + dy * dy2);
    const dx3 = this.c.v2.getX() - this.c.v1.getX();
    const dy3 = this.c.v2.getY() - this.c.v1.getY();
    const c = dx2 * dx2 + dy2 * dy2 - dx3 * dx3 - dy3 * dy3;

    let det = b * b - 4 * a * c;
    if (det < 0)
      return [Intersection.INF_X, Intersection.INF_Y];

    let t = -b;
    if (this.first)
      t += Math.sqrt(det);
    else
      t -= Math.sqrt(det);
    t /= 2 * a;
    return [this.l.v1.getX() + t * dx, this.l.v1.getY() + t * dy];
  }
}

class CirclesIntersection extends Intersection {
  constructor(c1, c2, first) {
    super();
    this.c1 = c1;
    this.c2 = c2;
    this.first = first;
  }

  getVertices() {
    const vertices = [];
    for (const c of [this.c1, this.c2]) {
      for (const v of [c.v1, c.v2]) {
        vertices.push(v.getX());
        vertices.push(v.getY());
      }
    }
    return vertices;
  }

  calc() {
    function sqDiff(a, b) {
      return a * a - b * b;
    }

    function rSq(a, b) {
      return a * a + b * b;
    }

    const x2Diff = sqDiff(this.c1.v1.getX(), this.c2.v1.getX());
    const y2Diff = sqDiff(this.c1.v1.getY(), this.c2.v1.getY());
    const r2Diff = rSq(this.c1.v1.getX() - this.c1.v2.getX(),
                       this.c1.v1.getY() - this.c1.v2.getY()) -
                   rSq(this.c2.v1.getX() - this.c2.v2.getX(),
                       this.c2.v1.getY() - this.c2.v2.getY());
    const z = x2Diff + y2Diff - r2Diff;

    let x1, y1, x2, y2;
    const dx = this.c1.v1.getX() - this.c2.v1.getX();
    const dy = this.c1.v1.getY() - this.c2.v1.getY();
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

class ASTNode {
  constructor(children) {
    this.children = children;
  }

  verify() {
    for (const child of this.children) {
      if (child instanceof ASTNode && !child.verify())
        return false;
    }
    return true;
  }
}

class NumericNode extends ASTNode {}

class NumericOperandsNode extends ASTNode {
  verify() {
    return this.children.reduce(
        (r, x) => r && x instanceof NumericNode, true);
  }  
}

class ArithNode extends NumericOperandsNode {}

class UnaryArithNode extends ArithNode {
  constructor(child) {
    super([child]);
  }

  verify() {
    return super.verify() && this.children.length == 1;
  }
}

class BinaryArithNode extends ArithNode {
  constructor(child1, child2) {
    super([child1, child2]);
  }

  verify() {
    return super.verify() && this.children.length == 2;
  }
}

class AddNode extends BinaryArithNode {
  calc() {
    return this.children[0].calc() + this.children[1].calc();
  }
}

class SubNode extends BinaryArithNode {
  calc() {
    return this.children[0].calc() - this.children[1].calc();
  }
}

class MulNode extends BinaryArithNode {
  calc() {
    return this.children[0].calc() * this.children[1].calc();
  }
}

class DivNode extends BinaryArithNode {
  calc() {
    return this.children[0].calc() / this.children[1].calc();
  }
}

class PowNode extends BinaryArithNode {
  calc() {
    return Math.pow(this.children[0].calc(), this.children[1].calc());
  }
}

class EqNode extends NumericOperandsNode {
  constructor(v1, v2) {
    super([v1, v2]);
  }

  verify() {
    super.verify() && this.children.length == 2;
  }

  calc() {
    return abs(this.children[0].calc() - this.children[1].calc()) < EPSILON;
  }
}

class SqrtNode extends UnaryArithNode {
  calc() {
    return Math.sqrt(this.children[0].calc());
  }
}

class VertexOperandsNode extends ASTNode {
  constructor(vertices) {
    // DEBUG
    console.log(vertices);

    super(vertices.map(label => vertexTable[label]));
  }

  verify() {
    if (this.children.length != 2)
      return false;
    return this.children.reduce((r, x) => r && x instanceof Vertex);
  }
}

class DistNode extends VertexOperandsNode {
  constructor(v1, v2) {
    super([v1, v2]);
  }

  verify() {
    return super.verify() && this.children.length == 2;
  }

  calc() {
    const x1 = this.children[0].getX();
    const x2 = this.children[1].getX();
    const y1 = this.children[0].getY();
    const y2 = this.children[1].getY();
    const dx = x1 - x2, dy = y1 - y2;
    return Math.sqrt(dx * dx + dy * dy);
  }
}

class AngleNode extends VertexOperandsNode {
  constructor(v1, v2, v3) {
    super([v1, v2, v3]);
  }

  verify() {
    return super.verify() && this.children.length == 3;
  }

  calc() {
    const v1 = createVector(
        this.children[0].getX() - this.children[1].getX(),
        this.children[0].getY() - this.children[1].getY());
    const v2 = createVector(
        this.children[2].getX() - this.children[1].getX(),
        this.children[2].getY() - this.children[1].getY());
    v1.normalize();
    v2.normalize();

    // TODO: deal with angles greater than 180 degrees
    return acos(v1.dot(v2));
  }
}

class NumNode extends NumericNode {
  constructor(num) {
    super([]);
    this.num = num;
  }

  verify() {
    return true;
  }

  calc() {
    return this.num;
  }
} 

class Condition {
  constructor(text) {
    this.text = text;
    this.node = condition.parse(text);
    this.row = conditionTable.insertRow();
  }

  updateStatus() {
    let stat = `<tr><td>${this.text}</td>`;
    if (this.node.calc())
      stat += `<td>✅</td></tr>`;
    else
      stat += `<td>❌</td></tr>`;
    this.row.innerHTML = stat;
  }
}

let toolSelect = null;
function setup() {
  const canvas = createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
  canvas.parent("canvas");
  textAlign(CENTER);
  angleMode(DEGREES);

  Vertex.COLOR = color(0, 0, 255);
  Vertex.STROKE = color(255, 0, 0);

  Line.STROKE = 0;
  Intersection.COLOR = 0;
  toolSelect = select("#tool");
  numObjectsDiv = select("#numObjects");
  labelInput = select("#label");
  conditionInput = select("#condition");
  conditionTable = document.getElementById("conditionTable");
  OBJECT_TYPES = [Line, Circle, Intersection, Vertex];
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
  "move": Vertex.selectVertex,
  "name": Vertex.selectVertex,
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

function drawObjects() {
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
}

function updateConditionTable() {
  for (const cond of conditions)
    cond.updateStatus();
}

function draw() {
  if (mouseIsPressed && mouseInCanvas())
    applyHandler(mouseIsPressedHandlers);

  background(BACKGROUND_COLOR);
  drawObjects();
  updateConditionTable();
  numObjectsDiv.html(`Number of objects: ${objects.length}`);
}

function clearObjects() {
  objects = [];
  vertexTable = {};
  conditions = [];
  while (conditionTable.rows.length > 1)
    conditionTable.deleteRow(conditionTable.rows.length - 1);
}

function nameVertex() {
  if (Vertex.selectedVertex) {
    const label = labelInput.value();
    if (label in vertexTable) {
      alert(`Vertex "${label}" already exists!`);
    } else {
      Vertex.selectedVertex.setLabel(label);
      vertexTable[label] = Vertex.selectedVertex;
    }
  }  
}

function clearSelectedVertex() {
  if (Vertex.selectedVertex) {
    Vertex.selectedVertex.setSelect(false);
    Vertex.selectedVertex = null;
  }
}

function addCondition() {
  const txt = conditionInput.value();
  conditions.push(new Condition(txt));
}

