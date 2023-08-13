import 'package:flutter/material.dart';
import 'circle.dart';
import 'fixed_intersection.dart';
import 'lines_intersection.dart';
import 'line_circle_intersection.dart';
import 'obj1d.dart';
import 'vertex.dart';

final class Line extends Obj1d {
  final _strokeWidth = 3.0;
  final Vertex _v1, _v2;

  Line(this._v1, this._v2);

  Vertex get v1 => _v1;
  Vertex get v2 => _v2;

  @override
  List<FixedIntersection> getIntersections(Obj1d obj) {
    if (obj is Line) {
      return [LinesIntersection(this, obj)];
    } else if (obj is Circle) {
      return [
          LineCircleIntersection(this, obj, true),
          LineCircleIntersection(this, obj, false)];
    }
    return [];
  }

  @override
  void draw(Canvas canvas, Size size) {
    Paint paint = Paint()
        ..color = Colors.black
        ..strokeCap = StrokeCap.square
        ..strokeWidth = _strokeWidth;
    var x1 = _v1.v.dx, y1 = _v1.v.dy;
    var x2 = _v2.v.dx, y2 = _v2.v.dy;
    if (x1 == x2) {
      y1 = 0;
      y2 = size.height;
    } else {
      final m = (y2 - y1) / (x2 - x1);
      y1 -= x1 * m;
      x1 = 0;
      y2 += (size.width - x2) * m;
      x2 = size.width;
    }
    canvas.drawLine(Offset(x1, y1), Offset(x2, y2), paint);
  }

  @override
  Offset vecToProj(Offset v) {
    final u = Offset(_v2.v.dx - _v1.v.dx, _v2.v.dy - _v1.v.dy);
    final s = (u.dy * (v.dx - _v1.v.dx) - u.dx * (v.dy - _v1.v.dy)) /
              (u.dx * u.dx + u.dy * u.dy);
    return Offset(-s * u.dy, s * u.dx);
  }

  @override
  bool movable() => false;

  @override
  void move(Offset v) {}

  @override
  bool isForeground() => false;
}