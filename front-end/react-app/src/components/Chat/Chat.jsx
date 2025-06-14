// ./components/Chat/Chat.js
import styles from "./Chat.module.css";
import Markdown from 'react-markdown'
const WELCOME_MESSAGE = {
  role: "assistant",
  content: "Hello! How can I assist you right now?",
};

export function Chat({ messages, messagesEndRef, eventKey}) {
  
  return (
    <div className={styles.Chat}>
      {[WELCOME_MESSAGE, ...messages].map(({ role, content, agent }, index) => (
        (
          role === "user" ? (
            <div key={index} className={styles.Message} data-role={role}>
              <Markdown>{content}</Markdown>
            </div>) :
            (
              <div key={index} className= {styles.AssistantMessages}>

                    <div>
                      {agent === 'graph_agent' ? (
                        <img className={styles.Logo} src="/graph_agent.png" alt="Graph Agent" />
                      ) : agent === 'graph_executor' ? (
                        <img className={styles.Logo} src="/graph_executor.png" alt="Graph Executor Agent" />
                      ) : agent === 'query_agent' ? (
                        <img className={styles.Logo} src="/query_agent.png" alt="Query Agent" />
                      ) : agent === 'executor_query' ? (
                        <img className={styles.Logo} src="/executor_query.png" alt="Query Executor Agent" />
                      ) : agent === 'add_filter_agent' ? (
                        <img className={styles.Logo} src="/add_filter_agent.png" alt="Add Filter Agent" />
                      ) : agent === 'add_filter_executor' ? (
                        <img className={styles.Logo} src="/add_filter_executor.png" alt="Add Filter Executor" />
                      ) : agent === 'RAG_agent' ? (
                        <img className={styles.Logo} src="/RAG_agent.png" alt="RAG Agent" />
                      ) : agent === 'RAG_executor' ? (
                        <img className={styles.Logo} src="/RAG_executor.png" alt="RAG Executor" />
                      ) : agent === 'terminology_agent' ? (
                        <img className={styles.Logo} src="/terminology_agent.png" alt="Terminology Agent" />
                      ) : agent === 'terminology_executor' ? (
                        <img className={styles.Logo} src="/terminology_executor.png" alt="Terminology Executor" />
                      ) : (
                        <img className={styles.Logo} src="/robot-assistant.png" alt="Proxy" />
                      )}
                    </div>
                
             
                <div className={styles.Message} data-role={role} agent = {agent}>
                  {eventKey === "agents" ? <div>
                      {agent === 'graph_agent' ? (
                        <div className={styles.AgentTitle} > Graph Agent </div>
                      ) : agent === 'graph_executor' ? (
                        <div className={styles.AgentTitle}> Graph Executor Agent</div>
                      ) : agent === 'query_agent' ? (
                        <div className={styles.AgentTitle} > Query Agent </div>
                      ) : agent === 'executor_query' ? (
                        <div className={styles.AgentTitle} > Query Executor Agent</div>
                      ) :  agent === 'add_filter_agent' ? (
                        <div className={styles.AgentTitle} > Add Filter Agent</div>
                      ) :agent === 'add_filter_executor' ? (
                        <div className={styles.AgentTitle} > Add Filter Executor</div>
                      ) : agent === 'RAG_agent' ? (
                        <div className={styles.AgentTitle} > RAG Agent</div>
                      ) : agent === 'RAG_executor' ? (
                        <div className={styles.AgentTitle} > RAG Executor Agent</div>
                      ) : agent === 'terminology_agent' ? (
                        <div className={styles.AgentTitle} > Terminology Agent</div>
                      ) : agent === 'terminology_executor' ? (
                        <div className={styles.AgentTitle} > Terminology Executor Agent</div>
                      ) : (
                        <div className={styles.AgentTitle}  > Proxy</div>
                      )}
                    </div>
                     : " "}
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