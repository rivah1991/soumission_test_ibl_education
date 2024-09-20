import 'package:flutter/material.dart';
import 'package:mobile_django/AuthContext/auth_service.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  String? _userToken;
  bool _isLoading = true;

  AuthProvider() {
    _init();
  }

  bool get isLoading => _isLoading;
  String? get userToken => _userToken;

  Future<void> _init() async {
    _userToken = await _authService.getToken();
    _isLoading = false;
    notifyListeners();
  }

  Future<bool> login(String username, String password) async {
    final success = await _authService.login(username, password);
    if (success) {
      _userToken = await _authService.getToken();
      debugPrint('Authentication successful, token received: $_userToken');
      notifyListeners();
    } else {
      debugPrint('Authentication failed');
    }
    return success;
  }

  Future<void> logout() async {
    await _authService.logout();
    _userToken = null;
    debugPrint('Logged out successfully');
    notifyListeners();
  }

  Future<void> updateToken() async {
    await _authService.updateToken();
    _userToken = await _authService.getToken();
    debugPrint('Token updated successfully: $_userToken');
    notifyListeners();
  }
}
