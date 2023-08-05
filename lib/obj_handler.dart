import 'package:flutter/material.dart';
import 'dart:collection';
import 'obj.dart';

abstract class ObjHandler {
  Obj? onTapUp(LinkedList<Obj> objs, TapUpDetails details) {
    return null;
  }

  Obj? onPanStart(LinkedList<Obj> objs, DragStartDetails details) {
    return null;
  }

  Obj? onPanEnd(LinkedList<Obj> objs, DragEndDetails details) {
    return null;
  }

  Obj? onPanUpdate(LinkedList<Obj> objs, DragUpdateDetails details) {
    return null;
  }
}