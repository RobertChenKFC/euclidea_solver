import 'package:flutter/material.dart';
import 'obj.dart';

base class Vertex extends Obj {
  Offset _v;
  static const r = 5.0;
  static const strokeWidth = 3.0;

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

    canvas.drawCircle(_v, r, paint);
  }
  
  @override
  bool inHover(Offset p) {
    final dx = _v.dx - p.dx, dy = _v.dy - p.dy;
    return dx * dx + dy * dy <= Obj.threshold;
  }

  @override
  bool isForeground() => true;
}