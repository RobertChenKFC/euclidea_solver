import 'package:euclidea_solver/line_circle_intersection.dart';
import 'package:flutter/material.dart';

import 'circle.dart';
import 'fixed_intersection.dart';
import 'intersection.dart';
import 'line.dart';
import 'vertex.dart';

final class CirclesIntersection extends ChosenFixedIntersection {
  final Circle _c1, _c2;

  CirclesIntersection(this._c1, this._c2, bool isFirstSol) : super(isFirstSol);

  static double sqDiff(double a, double b) {
    return a * a - b * b;
  }

  @override
  Offset calcIntersection(bool isFirstSol) {
    final x1 = _c1.v1.v.dx, y1 = _c1.v1.v.dy;
    final r12 = _c1.r2;
    final x2 = _c2.v1.v.dx, y2 = _c2.v1.v.dy;
    final r22 = _c2.r2;

    var x = 0.0, y = 0.0;
    final num = (sqDiff(x1, x2) + sqDiff(y1, y2) - (r12 - r22));
    if (x1 != x2) {
      x = num / (2 * (x1 - x2));
    }
    if (y1 != y2) {
      y = num / (2 * (y1 - y2));
    }

    Offset v1, v2;
    if (x1 == x2) {
      if (y1 == y2) {
        return const Offset(Intersection.nx, Intersection.ny);
      } else {
        v1 = Offset(0, y);
        v2 = Offset(1, y);
      }
    } else if (y1 == y2) {
      v1 = Offset(x, 0);
      v2 = Offset(x, 1);
    } else {
      v1 = Offset(x, 0);
      v2 = Offset(0, y);
    }

    final l = Line(Vertex(v1), Vertex(v2));
    return LineCircleIntersection(l, _c1, isFirstSol).v;
  }
}