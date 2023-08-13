import 'package:flutter/material.dart';
import 'dart:math';
import 'circles_intersection.dart';
import 'fixed_intersection.dart';
import 'line.dart';
import 'line_circle_intersection.dart';
import 'obj1d.dart';
import 'vertex.dart';

final class Circle extends Obj1d {
  final Vertex _v1, _v2;
  final _strokeWidth = 3.0;

  Circle(this._v1, this._v2);

  Vertex get v1 => _v1;
  Vertex get v2 => _v2;

  @override
  List<FixedIntersection> getIntersections(Obj1d obj) {
    if (obj is Line) {
      return [
          LineCircleIntersection(obj, this, true),
          LineCircleIntersection(obj, this, false)];
    } else if (obj is Circle) {
      return [
          CirclesIntersection(this, obj, true),
          CirclesIntersection(this, obj, false)];
    }
    return [];
  }

  double get r2 {
    final dx = _v1.v.dx - _v2.v.dx;
    final dy = _v1.v.dy - _v2.v.dy;
    return dx * dx + dy * dy;
  }

  double get r {
    return sqrt(r2);
  }

  @override
  void draw(Canvas canvas, Size size) {
    Paint paint = Paint()
        ..color = Colors.black
        ..strokeCap = StrokeCap.square
        ..strokeWidth = _strokeWidth
        ..style = PaintingStyle.stroke;
    canvas.drawCircle(_v1.v, r, paint);
  }

  @override
  Offset vecToProj(Offset v) {
    final u = Offset(_v1.v.dx - v.dx, _v1.v.dy - v.dy);
    final mag = sqrt(u.dx * u.dx + u.dy * u.dy);
    final s = (mag - r) / mag;

    return Offset(s * u.dx, s * u.dy);
  }

  @override
  bool isForeground() => false;

  @override
  void move(Offset v) {}

  @override
  bool movable() => false;
}