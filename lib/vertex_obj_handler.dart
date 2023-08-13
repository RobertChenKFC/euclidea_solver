import 'package:euclidea_solver/bounded_intersection.dart';
import 'package:euclidea_solver/fixed_intersection.dart';
import 'package:flutter/material.dart';
import 'dart:collection';
import 'dart:developer' as developer;
import 'obj.dart';
import 'obj1d.dart';
import 'obj_handler.dart';
import 'vertex.dart';

class VertexObjHandler extends ObjHandler {
  static Vertex? _getDuplicateVertex(LinkedList<Obj> objs, Vertex v) {
    for (final o in objs) {
      if (o is Vertex && o.isCloseTo(v)) {
        return o;
      }
    }
    return null;
  }

  @override
  Vertex onTapUp(LinkedList<Obj> objs, TapUpDetails details) {
    var i = 0;
    for (final o1 in objs) {
      if (o1 is Obj1d && o1.inHover(details.localPosition)) {
        var j = 0;
        for (final o2 in objs) {
          if (j >= i) {
            break;
          }
          if (o2 is Obj1d && o2.inHover(details.localPosition)) {
            Vertex? excludedVertex, v;
            var mind2 = double.infinity;
            for (final u in o1.getIntersections(o2)) {
              final vec = Offset(
                  u.v.dx - details.localPosition.dx,
                  u.v.dy - details.localPosition.dy);
              final d2 = vec.dx * vec.dx + vec.dy * vec.dy;
              final w = _getDuplicateVertex(objs, u);
              if (w == null && d2 < mind2) {
                v = u;
                mind2 = d2;
              } else {
                excludedVertex = w;
              }
            }
            if (v != null) {
              if (excludedVertex != null && v is ChosenFixedIntersection) {
                v.excludedVertex = excludedVertex;
              }
              objs.add(v);
              return v;
            }
          }
          ++j;
        }
      }
      ++i;
    }
    
    for (final o in objs) {
      if (o is Obj1d && o.inHover(details.localPosition)) {
        final v = BoundedIntersection(o, details.localPosition);
        if (_getDuplicateVertex(objs, v) == null) {
          objs.add(v);
          return v;
        }
      }
    }
    
    final v = Vertex(details.localPosition);
    objs.add(v);
    return v;
  }
}