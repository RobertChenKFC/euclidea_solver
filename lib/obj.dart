import 'package:flutter/material.dart';
import 'dart:collection';

abstract base class Obj extends LinkedListEntry<Obj> {
  static const threshold = 100.0;

  void move(Offset v);
  bool movable();
  void draw(Canvas canvas, Size size);
  bool inHover(Offset p);
  bool isForeground();
}