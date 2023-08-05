import 'two_vertices_handler.dart';
import 'vertex.dart';
import 'circle.dart';

class CircleObjHandler extends TwoVerticesHandler {
  @override
  Circle handleTwoVertices(Vertex v1, Vertex v2) {
    return Circle(v1, v2);
  }
}