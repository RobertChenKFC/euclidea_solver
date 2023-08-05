import 'package:euclidea_solver/bounded_intersection.dart';
import 'package:flutter/material.dart';
import 'dart:collection';
import 'dart:developer' as developer;
import 'obj.dart';
import 'obj1d.dart';
import 'obj_handler.dart';
import 'vertex.dart';

class VertexObjHandler extends ObjHandler {
  @override
  Vertex onTapUp(LinkedList<Obj> objs, TapUpDetails details) {
    for (final obj in objs) {
      if (obj is Obj1d && obj.inHover(details.localPosition)) {
        // DEBUG
        developer.log("Created bounded intersection on object $obj");

        final v = BoundedIntersection(obj, details.localPosition);
        objs.add(v);
        return v;
      }
    }
    
    final v = Vertex(details.localPosition);
    objs.add(v);
    return v;
  }
}