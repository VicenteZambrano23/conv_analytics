import React, { useState, useEffect, useRef } from "react";
import { Chat } from "./components/Chat/Chat";
import { Controls } from "./components/Controls/Controls";
import styles from "./App.module.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [chatStatus, setChatStatus] = useState("ended");
  const messagesEndRef = useRef(null);
  const lastSentUserMessage = useRef(null); // To track the last message sent by the user

  // Initial chat request structure (can be empty or contain an initial message)
  const initialChatRequest = {};

  // Function to send message/start chat
  const handleContentSend = async (content) => {
    let apiEndpoint, requestBody;
    lastSentUserMessage.current = content; // Store the sent message

    // Optimistic update: Add user message immediately for better UX
    setMessages((prevMessages) => [...prevMessages, { content, role: "user", tempId: Date.now() }]);

    if (chatStatus === "Chat ongoing" || chatStatus === "inputting") {
      // Send message request
      apiEndpoint = "https://5008-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/send_message";
      requestBody = { message: content };
    } else {
      // Start chat request
      apiEndpoint = "https://5008-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/start_chat";
      requestBody = { ...initialChatRequest, message: content };
    }

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error("Failed to send request");
      }

    } catch (error) {
      console.error("Error sending request:", error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.tempId === Date.now() ? { content: "Error sending message.", role: "assistant" } : msg
        )
      );
    }
  };

  // Function to fetch messages from the backend
  const fetchMessages = async () => {
    try {
      const response = await fetch("https://5008-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/get_message");
      if (!response.ok) {
        throw new Error("Failed to fetch messages");
      }

      const data = await response.json();
      if (data.message) {
        const messageUser = data.message.user;
        const messageContent = data.message.message;

        // Only add messages from 'User_Proxy' or 'sql_proxy'
        if (messageUser === "User_Proxy" || messageUser === "sql_proxy") {
          const isUserProxy = messageUser === "User_Proxy";
          // Only add the message if it's not the echoed user message from User_Proxy
          if (!isUserProxy || messageContent !== lastSentUserMessage.current) {
            setMessages((prevMessages) => [
              ...prevMessages,
              { content: messageContent, role: isUserProxy ? "user" : "assistant", agent: messageUser },
            ]);
          }
          // Reset the last sent user message after a short delay to avoid potential issues
          setTimeout(() => {
            lastSentUserMessage.current = null;
          }, 500); // Adjust the delay as needed
        }
      }
      setChatStatus(data.chat_status);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  // Use useEffect to poll for new messages
  useEffect(() => {
    const intervalId = setInterval(fetchMessages, 1000);
    return () => clearInterval(intervalId);
  }, [messages]);

  // Scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Filter messages to only show those from 'user' (your input), 'User_Proxy', or 'sql_proxy'
  const filteredMessages = messages.filter(
    (msg) => msg.role === "user" || msg.agent === "User_Proxy" || msg.agent === "sql_proxy"
  );

  return (
    <div className={styles.App}>
      <header className={styles.Header}>
        <img className={styles.Logo} src="/robot-assistant.png" alt="AI Chatbot Logo" />
        <h2 className={styles.Title}>Conversational Analytics</h2>
      </header>
      <div className={styles.ChatContainer}>
        <Chat messages={filteredMessages} messagesEndRef={messagesEndRef} />
      </div>
      <Controls onSend={handleContentSend} />
      <p className={styles.ChatStatus}>Chat Status: {chatStatus}</p>
    </div>

  );
}

export default App;