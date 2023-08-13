import 'package:flutter/material.dart';
import 'dart:collection';
import 'obj.dart';
import 'tool_icon.dart';
import 'obj_handler.dart';
import 'dart:developer' as developer;

class ObjPainterWidget extends StatefulWidget {
  const ObjPainterWidget({Key? key}) : super(key: key);

  @override
  ObjPainterWidgetState createState() => ObjPainterWidgetState();
}

class ObjPainterWidgetState extends State<ObjPainterWidget> {
  final LinkedList<Obj> _objs = LinkedList();
  ObjHandler _objHandler = Tool.defaultTool.handler;

  void clear() {
    setState(() {
      _objs.clear();
    });
  }

  set objHandler(ObjHandler objHandler) {
    _objHandler = objHandler;
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (ctx, constrains) {
        return Column(
          children: [
            SizedBox(
              width: constrains.maxWidth,
              height: constrains.maxHeight - ToolIconWidget.size,
              child: Center(
                child: GestureDetector(
                  onTapUp: (details) {
                    setState(() {
                      _objHandler.onTapUp(_objs, details);
                    });
                  },
                  onPanStart: (details) {
                    setState(() {
                      _objHandler.onPanStart(_objs, details);
                    });
                  },
                  onPanUpdate: (details) {
                    setState(() {
                      _objHandler.onPanUpdate(_objs, details);
                    });
                  },
                  onPanEnd: (details) {
                    setState(() {
                      _objHandler.onPanEnd(_objs, details);
                    });
                  },
                  child: Stack(children: [
                    CustomPaint(
                      size: Size.infinite,
                      painter: ObjPainter(_objs, paintForeground: false),
                    ),
                    CustomPaint(
                      size: Size.infinite,
                      painter: ObjPainter(_objs, paintForeground: true),
                    ),
                  ]),
                )
              )
            ),
            ToolIconsWidget(this),
          ]
        );
      }
    );
  }
}

class ObjPainter extends CustomPainter {
  final LinkedList<Obj> objs;
  final bool paintForeground;

  ObjPainter(this.objs, {required this.paintForeground});

  @override
  void paint(Canvas canvas, Size size) {
    // DEBUG
    // developer.log("Foreground: $paintForeground, Current number of objects: ${objs.length}");

    for (final obj in objs) {
      if (obj.isForeground() == paintForeground) {
        obj.draw(canvas, size);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}