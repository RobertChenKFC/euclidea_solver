import 'dart:math';

import 'package:flutter/material.dart';
import 'circle.dart';
import 'fixed_intersection.dart';
import 'intersection.dart';
import 'line.dart';
import 'vertex.dart';

final class LineCircleIntersection extends ChosenFixedIntersection {
  final Line _l;
  final Circle _c;

  LineCircleIntersection(this._l, this._c, bool isFirstSol) :
      super(isFirstSol);

  @override
  Offset calcIntersection(bool isFirstSol) {
    final x0 = _c.v1.v.dx, y0 = _c.v1.v.dy;
    final r2 = _c.r2;
    final x2 = _l.v1.v.dx, y2 = _l.v1.v.dy;
    final x3 = _l.v2.v.dx, y3 = _l.v2.v.dy;

    final dx = x3 - x2, dy = y3 - y2;
    final dx2 = x2 - x0, dy2 = y2 - y0;
    final a = dx * dx + dy * dy;
    final b = 2 * (dx * dx2 + dy * dy2);
    final c = dx2 * dx2 + dy2 * dy2 - r2;

    var det = b * b - 4 * a * c;
    if (det < Vertex.eps) {
      return const Offset(Intersection.nx, Intersection.ny);
    }
    det = max(det, 0);
    var t = sqrt(det);
    if (!isFirstSol) {
      t = -t;
    }
    t = (-b + t) / (2 * a);

    return Offset(x2 + dx * t, y2 + dy * t);
  }
}
