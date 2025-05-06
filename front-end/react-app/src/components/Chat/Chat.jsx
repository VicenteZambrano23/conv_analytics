// ./components/Chat/Chat.js
import styles from "./Chat.module.css";
import Markdown from 'react-markdown'
const WELCOME_MESSAGE = {
  role: "assistant",
  content: "Hello! How can I assist you right now?",
};

export function Chat({ messages, messagesEndRef }) {
  return (
    <div className={styles.Chat}>
      {[WELCOME_MESSAGE, ...messages].map(({ role, content }, index) => (
        (
          role === "user" ? (
            <div key={index} className={styles.Message} data-role={role}>
              <Markdown>{content}</Markdown>
            </div>) :
            (
              <div key={index} className= {styles.AssistantMessages}>
                <div>
                  <img className={styles.Logo} src="/robot-assistant.png" alt="AI Chatbot Logo" />
                </div>
                <div className={styles.Message} data-role={role}>
                  <Markdown>{content}</Markdown>
                </div>
              </div>
            )

        )
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}