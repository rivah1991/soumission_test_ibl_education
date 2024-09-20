import 'package:flutter/material.dart';
import 'package:mobile_django/providers/auth_provider.dart';
import 'package:provider/provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _usernameController,
              decoration: const InputDecoration(labelText: 'Username'),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _login,
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
  }

  void _login() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);

    try {
      bool success = await authProvider.login(
        _usernameController.text,
        _passwordController.text,
      );

      if (success) {
        // Afficher un message de succès dans la console de débogage
        debugPrint('Login successful');
        Navigator.pushReplacementNamed(context, '/home');
      } else {
        // Afficher un message d'erreur dans la console de débogage
        debugPrint('Login failed: Invalid credentials');
        _showErrorDialog('Invalid credentials');
      }
    } catch (e) {
      // Gérer les exceptions et afficher un message d'erreur
      debugPrint('Login failed: $e');
      _showErrorDialog('An error occurred: $e');
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}
