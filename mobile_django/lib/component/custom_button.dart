import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  const CustomButton({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        // Action à effectuer lors du clic sur le bouton
      },
      child: const Text('Press Me'),
    );
  }
}
