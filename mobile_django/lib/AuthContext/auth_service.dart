import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';  // Ajoutez cet import

class AuthService {
  // final String apiUrl = 'http://192.168.100.116:8000/api/token/';
  // final String apiUrl = 'http://127.0.0.1:8000/api/token/';
  final String apiUrl = 'http://192.168.100.116:8000/api/token/';


  Future<bool> login(String username, String password) async {
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _saveToken(data['access'], data['refresh']);
      return true;
    } else {
      return false;
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('authToken');
    await prefs.remove('refreshToken');
  }

  Future<void> updateToken() async {
    final prefs = await SharedPreferences.getInstance();
    final refreshToken = prefs.getString('refreshToken') ?? '';

    final response = await http.post(
      Uri.parse('http://192.168.100.116:8000/api/token/refresh/'),
      //  Uri.parse('http://127.0.0.1:8000/api/token/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refreshToken}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _saveToken(data['access'], data['refresh']);
    } else {
      await logout();
    }
  }

  Future<void> _saveToken(String accessToken, String refreshToken) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('authToken', accessToken);
    await prefs.setString('refreshToken', refreshToken);
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('authToken');
  }

  Future<String?> getRefreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('refreshToken');
  }
}
