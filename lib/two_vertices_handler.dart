import 'dart:collection';
import 'package:flutter/material.dart';

import 'obj.dart';
import 'obj_handler.dart';
import 'vertex.dart';
import 'vertex_obj_handler.dart';

abstract class TwoVerticesHandler extends ObjHandler {
  Vertex? _v1;

  Obj handleTwoVertices(Vertex v1, Vertex v2);

  @override
  Obj? onTapUp(LinkedList<Obj> objs, TapUpDetails details) {
    Vertex? v1 = _v1, v2;
    for (final obj in objs) {
      if (obj is Vertex && obj.inHover(details.localPosition)) {
        if (v1 == null) {
          _v1 = obj;
          return null;
        } else {
          _v1 = null;
          v2 = obj;
          final l = handleTwoVertices(v1, v2);
          objs.add(l);
          return l;
        }
      }
    }

    final v = VertexObjHandler().onTapUp(objs, details);
    if (v1 == null) {
      _v1 = v;
      return null;
    } else {
      _v1 = null;
      v2 = v;
      final l = handleTwoVertices(v1, v2);
      objs.add(l);
      return l;
    }
  }
}