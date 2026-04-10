import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const NicheWatcherApp());
}

class NicheWatcherApp extends StatelessWidget {
  const NicheWatcherApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Niche Watcher',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
