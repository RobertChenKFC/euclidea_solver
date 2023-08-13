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
  }

  @override
  Offset get v {
    // DEBUG
    // developer.log("Recalculating bounded intersection");
    
    final vec = _boundedObj.vecToProj(_p);
    return Offset(_p.dx + vec.dx, _p.dy + vec.dy);
  }

  @override
  void draw(Canvas canvas, Size size) {
    // DEBUG
    // developer.log("Redrawing bounded intersection");

    super.draw(canvas, size);
  }
}