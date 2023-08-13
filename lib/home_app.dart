import 'package:euclidea_solver/obj_painter.dart';
import 'package:flutter/material.dart';

class HomeApp extends StatelessWidget {
  final GlobalKey<ObjPainterWidgetState> _objPainterWidgetKey = GlobalKey();

  HomeApp({Key ?key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Euclidea Solver"),
        actions: [
          PopupMenuButton(
            itemBuilder: (context) {
              return [
                PopupMenuItem(
                  onTap: () {
                    _objPainterWidgetKey.currentState!.clear();
                  },
                  child: const Row(
                    children: [
                      Padding(
                        padding: EdgeInsets.all(4.0),
                        child: Icon(
                          Icons.refresh,
                          color: Colors.black,
                          size: 24.0,
                        )
                      ),
                      Text("Reset")
                    ]
                  )
                ),
              ];
            }
          )
        ],
      ),
      body: ObjPainterWidget(key: _objPainterWidgetKey),
    );
  }
}