import React, { useState, useEffect } from 'react';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatStatus, setChatStatus] = useState('ended');
  const [loading, setLoading] = useState(false); // Add loading state

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch('http://10.128.0.84:5008/api/get_message');
        const data = await response.json();
        if (data.message) {
          setMessages(prevMessages => [...prevMessages, { text: data.message, sender: 'bot' }]);
          setChatStatus(data.chat_status);
        } else {
          setChatStatus(data.chat_status);
        }
      } catch (error) {
        console.error('Error fetching message:', error);
      }
    };

    const intervalId = setInterval(fetchMessages, 1000); // Poll every second

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const startChat = async () => {
    setLoading(true); // Set loading to true while starting chat
    try {
      const response = await fetch('http://10.128.0.84:5008/api/start_chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* your initial data here */ }),
      });
      const data = await response.json();
      setChatStatus(data.status);
      setLoading(false); // Reset loading state
    } catch (error) {
      console.error('Error starting chat:', error);
      setLoading(false); // Reset loading state
    }
  };

  const sendMessage = async () => {
    if (input.trim()) {
      setMessages(prevMessages => [...prevMessages, { text: input, sender: 'user' }]);
      setInput('');
      try {
        const response = await fetch('http://10.128.0.84:5008/api/send_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input }),
        });
        const data = await response.json();
        console.log(data.status);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>
            <strong>{message.sender}:</strong> {message.text}
          </div>
        ))}
      </div>
      <div>
      {chatStatus === 'ended' ? (
          <button onClick={startChat} disabled={loading}>
            {loading ? 'Starting...' : 'Start Chat'}
          </button>
        ) : (
          <>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button onClick={sendMessage}>Send</button>
          </>
        )}
      </div>
      <div>
        <p>Chat Status: {chatStatus}</p>
      </div>
    </div>
  );
}

export default ChatInterface;
