import React, { useEffect, useState, useContext } from 'react';
import AuthContext from '../context/AuthContext';

const ChatComponent = () => {
  const { authToken } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [webSocket, setWebSocket] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [lastReceivedMessage, setLastReceivedMessage] = useState('');

  useEffect(() => {
    if (!authToken) {
      console.log('No token available, cannot connect to WebSocket');
      return;
    }

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/socket-server/?token=${authToken.access}`);

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data && typeof data.message === 'string') {         
        const truncatedMessage = data.message.slice(0, 300); // Limiter à 300 caractères
        if (truncatedMessage !== lastReceivedMessage) {
        setMessages((prevMessages) => [...prevMessages, { text: truncatedMessage, sent: false }]);
        setLastReceivedMessage(truncatedMessage);
          }
        } else {
          console.warn('Invalid message structure received:', data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onclose = (event) => {
      if (event.code === 4000) {
        console.log('WebSocket closed with code 4000');
      }
      console.log('WebSocket closed:', event.reason);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWebSocket(ws);

    return () => {
      ws.close();
    };
  }, [authToken, lastReceivedMessage]);

  const sendMessage = (message) => {
    if (webSocket) {
      try {
        webSocket.send(JSON.stringify({ message }));
        setMessages((prevMessages) => [...prevMessages, { text: message, sent: true }]);
        setInputValue('');
      } catch (error) {
        console.error('Error sending WebSocket message:', error);
      }
    }
  };

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage(inputValue);
    }
  };

  const handleClick = () => {
    sendMessage(inputValue);
  };

  return (
    <div>
      <h1>Chat</h1>
      <ul>
        {messages.map((msg, index) => (
          <li key={index} style={{ color: msg.sent ? 'green' : 'black' }}>
            {msg.text}
          </li>
        ))}
      </ul>
      <input
        type="text"
        value={inputValue}
        onChange={handleChange}
        onKeyPress={handleKeyPress}
        placeholder="Type a message"
        aria-label="Chat input"
      />
      <button onClick={handleClick}>Send Message</button>
    </div>
  );
};

export default ChatComponent;
