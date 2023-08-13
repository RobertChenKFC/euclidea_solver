import 'package:flutter/material.dart';
import 'obj.dart';

base class Vertex extends Obj {
  Offset _v;
  static const r = 5.0;
  static const strokeWidth = 3.0;
  static const eps = 1e-6;

  Vertex(this._v);

  Offset get v {
    return _v;
  }

  @override
  void move(Offset v) {
    _v = v;
  }

  @override
  bool movable() => true;

  @override
  void draw(Canvas canvas, Size size) {
    Paint paint = Paint()
      ..color = Colors.blue.shade800
      ..strokeCap = StrokeCap.square
      ..style = PaintingStyle.fill
      ..strokeWidth = strokeWidth;

    canvas.drawCircle(v, r, paint);
  }
  
  @override
  bool inHover(Offset p) {
    final dx = v.dx - p.dx, dy = v.dy - p.dy;
    return dx * dx + dy * dy <= Obj.threshold;
  }

  @override
  bool isForeground() => true;

  bool isCloseTo(Vertex v2) {
    final dx = v.dx - v2.v.dx, dy = v.dy - v2.v.dy;
    return dx * dx + dy * dy < eps;
  }

  bool isCloseToOffset(Offset v2) {
    final dx = v.dx - v2.dx, dy = v.dy - v2.dy;
    return dx * dx + dy * dy < eps;
  }
}