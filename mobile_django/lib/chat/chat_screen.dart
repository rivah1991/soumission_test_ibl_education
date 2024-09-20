import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mobile_django/AuthContext/auth_service.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  WebSocketChannel? _channel; // Changed to nullable to handle uninitialized state
  final List<Map<String, dynamic>> _messages = [];
  final TextEditingController _controller = TextEditingController();
  String? _lastReceivedMessage;

  @override
  void initState() {
    super.initState();
    _initializeWebSocket(); // Initialize WebSocket connection when widget is first built
  }

  Future<String?> _fetchToken() async {
    try {
      final authService = AuthService();
      return await authService.getToken();
    } catch (e) {
      print('Error fetching token: $e');
      return null;
    }
  }

  Future<void> _initializeWebSocket() async {
    final token = await _fetchToken();
    if (token == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to retrieve authentication token')),
      );
      return;
    }

    // Initialize WebSocket channel
    _channel = WebSocketChannel.connect(
      Uri.parse('ws://192.168.100.116:8000/ws/socket-server/?token=$token'),
    );

    _channel!.stream.listen(
      (message) {
        print('Message brut reçu: $message'); // Log for debugging

        try {
          final data = jsonDecode(message);

          // Check if the message contains valid data
          if (data != null && data['message'] is String && data['message'].isNotEmpty) {
            final messageId = data['message'] as String?;

            if (messageId != null && messageId != _lastReceivedMessage) {
              // Clean up special characters
              final cleanedMessage = messageId.replaceAll(RegExp(r'\\u2019'), "'");

              setState(() {
                _messages.add({'text': cleanedMessage, 'sent': false});
                _lastReceivedMessage = cleanedMessage;
              });

              print("Message reçu et nettoyé: $cleanedMessage");
            }
          } else {
            print('Le message reçu n\'est pas valide : $data');
          }
        } catch (e) {
          print('Erreur lors du décodage du message : $e');
        }
      },
      onError: (error) {
        print('WebSocket error: $error');
      },
      onDone: () {
        print('WebSocket connection closed');
      },
    );
  }

  Future<void> _logout() async {
    try {
      final authService = AuthService();
      await authService.logout();
      _channel?.sink.close(status.goingAway); // Close WebSocket connection safely
      Navigator.pushReplacementNamed(context, '/login'); // Redirect to login screen
    } catch (e) {
      print('Error during logout: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error during logout: $e')),
      );
    }
  }

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isNotEmpty && _channel != null) {
      _channel!.sink.add(jsonEncode({'message': text})); // Send message to WebSocket server
      setState(() {
        _messages.add({'text': text, 'sent': true});
        _controller.clear(); // Clear text field after sending
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return Container(
                  padding: const EdgeInsets.all(8.0), // Padding for spacing
                  child: Text(
                    msg['text'],
                    style: TextStyle(
                      color: msg['sent'] ? Colors.green : Colors.black,
                      fontSize: 16, // Font size
                    ),
                    maxLines: null, // Allow text to span multiple lines
                    softWrap: true, // Enable text wrapping
                    overflow: TextOverflow.visible, // Ensure full text display
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type a message',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(), // Send message on "Enter" key
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage, // Button to send the message
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _channel?.sink.close(status.goingAway); // Close WebSocket connection when widget is disposed
    super.dispose();
  }
}
