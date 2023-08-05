import 'package:flutter/material.dart';
import 'obj.dart';

abstract base class Obj1d extends Obj {
  Offset vecToProj(Offset v);

  @override
  bool inHover(Offset p) {
    final vec = vecToProj(p);
    return vec.dx * vec.dx + vec.dy * vec.dy <= Obj.threshold;
  }
}