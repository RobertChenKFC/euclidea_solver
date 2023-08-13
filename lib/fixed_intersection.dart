import 'package:flutter/material.dart';
import 'intersection.dart';
import 'vertex.dart';
import 'dart:developer' as developer;
import 'dart:math';

base class FixedIntersection extends Intersection {
  @override
  void draw(Canvas canvas, Size size) {
    Paint paint = Paint()
        ..color = Colors.black
        ..strokeCap = StrokeCap.square
        ..style = PaintingStyle.fill
        ..strokeWidth = Vertex.strokeWidth;
    canvas.drawCircle(v, Vertex.r, paint);
  }

  @override
  void move(Offset v) {}

  @override
  bool movable() => false;
}

abstract base class ChosenFixedIntersection extends FixedIntersection {
  final bool _isFirstSol;
  Vertex? _excludedVertex;

  ChosenFixedIntersection(this._isFirstSol) :
      _excludedVertex = null;

  set excludedVertex(Vertex v) {
    _excludedVertex = v;
  }

  Offset calcIntersection(bool isFirstSol);

  @override
  Offset get v {
    Offset v1 = calcIntersection(_isFirstSol);
    final excludedVertex = _excludedVertex;
    if (excludedVertex == null || !excludedVertex.isCloseToOffset(v1)) {
      // DEBUG
      // developer.log("First solution, excludedVertex = $excludedVertex\n");
      /*
      if (excludedVertex != null) {
        final dx = excludedVertex.v.dx - v1.dx;
        final dy = excludedVertex.v.dy - v1.dy;
        developer.log("Excluded: (${excludedVertex.v.dx}, ${excludedVertex.v.dy}), cur: (${v1.dx}, ${v1.dy}), distance: ${sqrt(dx * dx + dy * dy)}");
      }
      */

      return v1;
    }

    // DEBUG
    // developer.log("Second solution, excludedVertex = $excludedVertex\n");

    return calcIntersection(!_isFirstSol);
  }
}