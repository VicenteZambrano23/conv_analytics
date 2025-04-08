import { useState } from "react";
import styles from "./Controls.module.css";
import { Chat } from "../Chat/Chat";

export function Controls({ onSend }) {
  const [content, setContent] = useState("");

  function addMessage(message){
    setMessages((prevMessages) => [...prevMessages, message])
  }

  function handleContentChange(event) {
    setContent(event.target.value);
  }

  async function handleContentSend(content) {
    addMessage({content, role : 'user'})
    try {
      const result = await chat.sendMessage(content);
      addMessage({content: result.response.text(), role : 'assistant'});
    } catch(error){
      addMessage({content: "Sorry, doesn´t work", role : 'system'});
    }
  }

  function handleEnterPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleContentSend();
    }
  }

  return (
    <div className={styles.Controls}>
      <div className={styles.TextAreaContainer}>
        <textarea
          className={styles.TextArea}
          placeholder="Message AI Chatbot"
          value={content}
          onChange={handleContentChange}
          onKeyDown={handleEnterPress}
        />
      </div>
      <button className={styles.Button} onClick={handleContentSend}>
        <SendIcon />
      </button>
    </div>
  );
}

function SendIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      height="24px"
      viewBox="0 -960 960 960"
      width="24px"
      fill="#5f6368"
    >
      <path d="M120-160v-240l320-80-320-80v-240l760 320-760 320Z" />
    </svg>
  );
}