import 'package:flutter/material.dart';
import 'vertex.dart';

base class Intersection extends Vertex {
  static const nx = -100.0;
  static const ny = -100.0;

  Intersection([Offset? v]) : super(Offset(v?.dx ?? nx, v?.dy ?? ny));
}