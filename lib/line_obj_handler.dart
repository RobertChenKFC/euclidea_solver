import 'two_vertices_handler.dart';
import 'line.dart';
import 'vertex.dart';

class LineObjHandler extends TwoVerticesHandler {
  @override
  Line handleTwoVertices(Vertex v1, Vertex v2) {
    return Line(v1, v2);
  }
}