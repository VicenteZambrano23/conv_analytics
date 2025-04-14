import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatStatus, setChatStatus] = useState('ended');

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get('http://localhost:5008/api/get_message')
        .then(response => {
          if (response.data.message) {
            setMessages(prevMessages => [...prevMessages, response.data.message]);
          }
          setChatStatus(response.data.chat_status);
        })
        .catch(error => console.error('Error fetching messages:', error));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const startChat = () => {
    axios.post('http://localhost:5008/api/start_chat')
      .then(response => setChatStatus(response.data.status))
      .catch(error => console.error('Error starting chat:', error));
  };

  const sendMessage = () => {
    axios.post('http://localhost:5008/api/send_message', { message: input })
      .then(response => {
        setInput('');
        console.log(response.data.status);
      })
      .catch(error => console.error('Error sending message:', error));
  };

  return (
    <div>
      <h1>Chat Application</h1>
      <button onClick={startChat} disabled={chatStatus === 'Chat ongoing'}>Start Chat</button>
      <div>
        {messages.map((msg, index) => (
          <div key={index}>{msg}</div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        disabled={chatStatus !== 'Chat ongoing'}
      />
      <button onClick={sendMessage} disabled={chatStatus !== 'Chat ongoing'}>Send</button>
    </div>
  );
};

export default Chat;
