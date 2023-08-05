import 'package:flutter/material.dart';
import 'dart:developer' as developer;
import 'intersection.dart';
import 'obj1d.dart';

final class BoundedIntersection extends Intersection {
  final Obj1d _boundedObj;
  Offset _p;

  BoundedIntersection(this._boundedObj, this._p);

  @override
  void move(Offset v) {
    _p = v;

    // DEBUG
    developer.log("Move cursor vertex to $_p");
  }

  @override
  void draw(Canvas canvas, Size size) {
    final vec = _boundedObj.vecToProj(_p);
    final v = Offset(_p.dx + vec.dx, _p.dy + vec.dy);
    super.move(v);
    super.draw(canvas, size);
  }
}