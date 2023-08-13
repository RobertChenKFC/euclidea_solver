import 'package:flutter/material.dart';
import 'fixed_intersection.dart';
import 'intersection.dart';
import 'line.dart';

class _LineCoeff {
  final double a, b, c;
  _LineCoeff(this.a, this.b, this.c);
}

final class LinesIntersection extends FixedIntersection {
  final Line _l1, _l2;

  LinesIntersection(this._l1, this._l2);

  static _LineCoeff _getLineCoeff(Line l) {
    final x1 = l.v1.v.dx, y1 = l.v1.v.dy;
    final x2 = l.v2.v.dx, y2 = l.v2.v.dy;
    return _LineCoeff(y2 - y1, x1 - x2, x1 * y2 - x2 * y1);
  }

  @override
  Offset get v {
    final coeff1 = _getLineCoeff(_l1);
    final a1 = coeff1.a, b1 = coeff1.b, c1 = coeff1.c;
    final coeff2 = _getLineCoeff(_l2);
    final a2 = coeff2.a, b2 = coeff2.b, c2 = coeff2.c;
    final d = a1 * b2 - a2 * b1;
    if (d == 0) {
      return const Offset(Intersection.nx, Intersection.ny);
    }
    return Offset((b2 * c1 - b1 * c2) / d, (a1 * c2 - a2 * c1) / d);
  }
}