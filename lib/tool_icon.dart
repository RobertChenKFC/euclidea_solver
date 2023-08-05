import 'package:flutter/material.dart';
import 'circle_obj_handler.dart';
import 'line_obj_handler.dart';
import 'move_obj_handler.dart';
import 'obj_handler.dart';
import 'obj_painter.dart';
import 'vertex_obj_handler.dart';

class ToolIconsWidget extends StatefulWidget {
  final ObjPainterWidgetState _parentPainter;

  const ToolIconsWidget(ObjPainterWidgetState parentPainter, {Key? key}) :
      _parentPainter = parentPainter,
      super(key: key);

  @override
  State<StatefulWidget> createState() => ToolIconsWidgetState();
}

enum Tool {
  move,
  vertex,
  line,
  circle;

  static Tool get defaultTool {
    return Tool.vertex;
  }

  String get filename {
    switch (this) {
      case Tool.move:
        return "hand";
      case Tool.vertex:
        return "vertex";
      case Tool.line:
        return "line";
      case Tool.circle:
        return "circle";
    }
  }

  ObjHandler get handler {
    switch (this) {
      case Tool.move:
        return MoveObjHandler();
      case Tool.vertex:
        return VertexObjHandler();
      case Tool.line:
        return LineObjHandler();
      case Tool.circle:
        return CircleObjHandler();
    }
  }
}

enum ToolState {
  normal,
  inHover,
  selected
}

class ToolIconsWidgetState extends State<ToolIconsWidget> {
  final List<ToolIconWidget> _toolWidgets = List.empty(growable: true);
  final List<ToolState> _toolStates = List.empty(growable: true);
  int _selectedIdx = 0;

  ToolIconsWidgetState() {
    var i = 0;
    for (final tool in Tool.values) {
      if (tool == Tool.defaultTool) {
        _toolStates.add(ToolState.selected);
        _selectedIdx = i;
      } else {
        _toolStates.add(ToolState.normal);
      }
      ++i;
    }
  }

  void setToolState(int idx, ToolState state) {
    setState(() {
      if (_toolStates[idx] != ToolState.selected) {
        _toolStates[idx] = state;
        if (state == ToolState.selected) {
          _toolStates[_selectedIdx] = ToolState.normal;
          _selectedIdx = idx;

          widget._parentPainter.objHandler = Tool.values[_selectedIdx].handler;
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    _toolWidgets.clear();
    for (var i = 0; i < Tool.values.length; ++i) {
      final toolName = Tool.values[i].filename;
      final toolState = _toolStates[i];

      var imgPath = "assets/$toolName";
      switch (toolState) {
        case ToolState.normal:
          imgPath += ".png";
          break;
        case ToolState.inHover:
          imgPath += "-hover.png";
          break;
        case ToolState.selected:
          imgPath += "-select.png";
          break;
      }
      _toolWidgets.add(ToolIconWidget(this, i, imgPath));
    }

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: _toolWidgets
    );
  }
}

class ToolIconWidget extends StatelessWidget {
  final ToolIconsWidgetState _parentToolbar;
  final int _idx;
  final Image _img;
  static const size = 48.0;

  const ToolIconWidget._(
      this._parentToolbar, this._idx, this._img, {Key? key}) : super(key: key);

  factory ToolIconWidget(
      ToolIconsWidgetState parentToolbar, int idx, String imgPath, {Key ?key}) {
    final img = Image.asset(imgPath, width: size, height: size);
    return ToolIconWidget._(parentToolbar, idx, img, key: key);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        _parentToolbar.setToolState(_idx, ToolState.selected);
      },
      child: MouseRegion(
        onEnter: (event) {
          _parentToolbar.setToolState(_idx, ToolState.inHover);
        },
        onExit: (event) {
          _parentToolbar.setToolState(_idx, ToolState.normal);
        },
        child: _img,
      )
    );
  }
}
