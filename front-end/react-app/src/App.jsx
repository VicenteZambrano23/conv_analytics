import { useState, useEffect, useRef } from "react";
import { Chat } from "./components/Chat/Chat";
import { Controls } from "./components/Controls/Controls";
import styles from "./App.module.css";
import { Graph } from "./components/Graph/Graph";
import { Loader } from "./components/Loader/Loader";
import { GraphLoader } from "./components/GraphLoader/GraphLoader";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import React from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [chatStatus, setChatStatus] = useState("ended");
  const messagesEndRef = useRef(null);
  const lastSentUserMessage = useRef(null);
  const [loader, setLoader] = useState(false);
  const [loaderGraph, setLoaderGraph] = useState(false);
  const [key, setKey] = useState("user");
  const [isGraph, setIsGraph] = useState(false);
  const [graphData, setGraphData] = useState(null);
  // Initial chat request structure (can be empty or contain an initial message)
  const initialChatRequest = {};

  const fetchGraphData = async () => {
    try {
      const response = await fetch(
        "https://5009-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/data"
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const jsonData = await response.json();
      setGraphData(Array.isArray(jsonData) ? [...jsonData] : jsonData);
    } catch (err) {
      console.error("Error fetching graph data:", err);
      setGraphData(null);
    }
  };

  // Function to send message/start chat
  const handleContentSend = async (content) => {
    let apiEndpoint, requestBody;
    lastSentUserMessage.current = content; // Store the sent message

    // Optimistic update: Add user message immediately for better UX
    setMessages((prevMessages) => [
      ...prevMessages,
      { content, role: "user", tempId: Date.now() },
    ]);

    if (chatStatus === "Chat ongoing" || chatStatus === "inputting") {
      // Send message request
      apiEndpoint =
        "https://5009-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/send_message";
      requestBody = { message: content };
    } else {
      // Start chat request
      apiEndpoint =
        "https://5009-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/start_chat";
      requestBody = { ...initialChatRequest, message: content };
    }

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      setLoader(true);
      if (!response.ok) {
        throw new Error("Failed to send request");
      }
    } catch (error) {
      console.error("Error sending request:", error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.tempId === Date.now()
            ? { content: "Error sending message.", role: "assistant" }
            : msg
        )
      );
    }
  };

  // Function to fetch messages from the backend
  const fetchMessages = async () => {
    try {
      const response = await fetch(
        "https://5009-01jr7k2qz227qhygnkh9vjydzp.cloudspaces.litng.ai/api/get_message"
      );
      if (!response.ok) {
        throw new Error("Failed to fetch messages");
      }

      const data = await response.json();
      if (data.message) {
        const messageUser = data.message.user;
        const messageContent = data.message.message;

        // Only add messages from 'User_Proxy' or 'sql_proxy'
        if (
          messageUser === "User_Proxy" ||
          messageUser === "sql_proxy" ||
          messageUser === "graph_agent" ||
          messageUser === "graph_executor" ||
          messageUser === "RAG_executor" ||
          messageUser === "terminology_executor" ||
          messageUser === "terminology_agent" ||
          messageUser === "query_agent" ||
          messageUser === "RAG_agent" ||
          messageUser === "executor_query" ||
          messageUser == "add_filter_agent" ||
          messageUser == "add_filter_executor"
        ) {
          const isUserProxy = messageUser === "User_Proxy";
          const isSqlProxy = messageUser === "sql_proxy";
          const isGraphAgent = messageUser === "graph_agent";
          const isFilterAgent = messageUser === "add_filter_agent";
          const isGraphExecutor = messageUser === "graph_executor";
          const isFilterExecutor = messageUser === "add_filter_executor";

          // Only add the message if it's not the echoed user message from User_Proxy
          if (!isUserProxy || messageContent !== lastSentUserMessage.current) {
            if (messageContent === "None") {
              setMessages((prevMessages) => [
                ...prevMessages,
                {
                  content: "Working on it!",
                  role: isUserProxy ? "user" : "assistant",
                  agent: messageUser,
                },
              ]);
            } else {
              setMessages((prevMessages) => [
                ...prevMessages,
                {
                  content: messageContent,
                  role: isUserProxy ? "user" : "assistant",
                  agent: messageUser,
                },
              ]);

              if (isGraphAgent) {
                setIsGraph(true);
              }

              if (isGraphExecutor || isFilterExecutor) {
                fetchGraphData(); // Call the API to fetch graph data
              }

              if (isSqlProxy) {
                setLoader(false);
                setLoaderGraph(false);
              }

              if (isGraphAgent) {
                setLoaderGraph(true);
              }

              if (isFilterAgent) {
                setLoaderGraph(true);
              }

              // Reset the last sent user message after a short delay to avoid potential issues
              setTimeout(() => {
                lastSentUserMessage.current = null;
              }, 500); // Adjust the delay as needed
            }
          }
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
    (msg) =>
      msg.role === "user" ||
      msg.agent === "User_Proxy" ||
      msg.agent === "sql_proxy"
  );

  return (
    <div className={styles.MainContainer}>
      {loader ? <Loader isGraph={isGraph} /> : <div />}

      <div className={styles.HeaderContainer}>
        <div className={styles.TitleContainer}>
          <img className={styles.Title} src="../public/title.png" alt="Title" />
        </div>
      </div>

      {isGraph ? (
        <div className={styles.ChatGraphContainer}>
          <div className={styles.ChatControlsContainer}>
            <Tabs
              id="controlled-tab-example"
              activeKey={key}
              onSelect={(k) => setKey(k)}
              className="m-0"
            >
              <Tab eventKey="user" title="User">
                <div className={styles.ChatContainer}>
                  <Chat
                    messages={filteredMessages}
                    messagesEndRef={messagesEndRef}
                    eventKey="user"
                  />
                </div>
                <div className={styles.ControlsContainer}>
                  <Controls onSend={handleContentSend} />
                </div>
              </Tab>
              <Tab eventKey="agents" title="Agents">
                <div className={styles.ChatContainer}>
                  <Chat
                    messages={messages}
                    messagesEndRef={messagesEndRef}
                    eventKey="agents"
                  />
                </div>
                <div className={styles.ControlsContainer}>
                  <Controls onSend={handleContentSend} />
                </div>
              </Tab>
            </Tabs>
          </div>
          <div className={styles.GraphContainer}>
            {loaderGraph ? (
              <GraphLoader />
            ) : (
              <Graph isGraph={isGraph} graphData={graphData} />
            )}
          </div>
        </div>
      ) : (
        <div className={styles.ChatGraphContainer}>
          <div className={styles.ChatControlsContainer}>
            <Tabs
              id="controlled-tab-example"
              activeKey={key}
              onSelect={(k) => setKey(k)}
              className="m-0"
            >
              <Tab eventKey="user" title="User">
                <div className={styles.ChatContainer}>
                  <Chat
                    messages={filteredMessages}
                    messagesEndRef={messagesEndRef}
                    eventKey="user"
                  />
                </div>
                <div className={styles.ControlsContainer}>
                  <Controls onSend={handleContentSend} />
                </div>
              </Tab>
              <Tab eventKey="agents" title="Agents">
                <div className={styles.ChatContainer}>
                  <Chat
                    messages={messages}
                    messagesEndRef={messagesEndRef}
                    eventKey="agents"
                  />
                </div>
                <div className={styles.ControlsContainer}>
                  <Controls onSend={handleContentSend} />
                </div>
              </Tab>
            </Tabs>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
