import 'package:flutter/material.dart';
import 'intersection.dart';
import 'vertex.dart';

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