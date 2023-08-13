import 'package:flutter/material.dart';
import 'dart:collection';
import 'dart:developer' as developer;
import 'obj.dart';
import 'obj_handler.dart';

class MoveObjHandler extends ObjHandler {
  Obj? _objToMove;

  @override
  Obj? onPanStart(LinkedList<Obj> objs, DragStartDetails details) {
    for (final obj in objs) {
      if (obj.movable() && obj.inHover(details.localPosition)) {
        _objToMove = obj;
        break;
      }
    }
    return null;
  }

  @override
  Obj? onPanUpdate(LinkedList<Obj> objs, DragUpdateDetails details) {
    final objToMove = _objToMove;
    if (objToMove == null) {
      return null;
    }
    objToMove.move(details.localPosition);
    return null;
  }

  @override
  Obj? onPanEnd(LinkedList<Obj> objs, DragEndDetails details) {
    _objToMove = null;
    return null;
  }
}