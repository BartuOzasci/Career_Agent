import React, { useState, useRef, useEffect } from "react";
import { Container, Row, Col, Form, Button, Card } from "react-bootstrap";
import "./ChatInterface.css";
import axios from "axios";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
  isTyping?: boolean;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Merhaba! Ben Kariyer Gelişim Ajanı. Size kariyer hedeflerinizde yardımcı olabilirim. Kariyer hedefinizi benimle paylaşır mısınız?",
      sender: "bot",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [typingText, setTypingText] = useState("");

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, typingText]);

  const handleSendMessage = async () => {
    if (inputValue.trim() === "" || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      // Streaming yanıt al
      const response = await fetch("http://localhost:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: inputValue,
          user_id: "default_user",
        }),
      });

      if (!response.ok) {
        throw new Error("API isteği başarısız oldu");
      }

      // Bot mesajı için placeholder ekle
      const botMessageId = messages.length + 2;
      const botMessage: Message = {
        id: botMessageId,
        text: "",
        sender: "bot",
        timestamp: new Date(),
        isTyping: true,
      };
      setMessages((prev) => [...prev, botMessage]);

      // Stream'i oku
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let fullText = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.done) {
                  // Typing tamamlandı
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === botMessageId
                        ? { ...msg, text: fullText, isTyping: false }
                        : msg,
                    ),
                  );
                } else {
                  fullText += data.text;
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === botMessageId
                        ? { ...msg, text: fullText }
                        : msg,
                    ),
                  );
                }
              } catch (e) {
                // JSON parse hatası, devam et
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Hata:", error);
      const errorMessage: Message = {
        id: messages.length + 2,
        text: "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.",
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container fluid className="chat-container">
      <Row className="w-100 h-100 m-0">
        <Col xs={12} className="p-0">
          <Card className="chat-card shadow-lg">
            {/* Header */}
            <Card.Header className="chat-header">
              <div className="d-flex align-items-center">
                <div className="avatar-container">
                  <img
                    src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                    alt="Kariyer Gelişim Ajanı"
                    className="avatar-img"
                  />
                  <span className="status-indicator"></span>
                </div>
                <div className="ms-3">
                  <h5 className="mb-0 agent-name">Kariyer Gelişim Ajanı</h5>
                  <small className="text-muted">Çevrimiçi • AI Destekli</small>
                </div>
              </div>
            </Card.Header>

            {/* Messages */}
            <Card.Body className="chat-body">
              <div className="messages-container">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`message-wrapper ${
                      message.sender === "user" ? "user-message" : "bot-message"
                    }`}
                  >
                    {message.sender === "bot" && (
                      <div className="bot-avatar">
                        <img
                          src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                          alt="Bot"
                          className="mini-avatar"
                        />
                      </div>
                    )}
                    <div className="message-bubble">
                      <div className="message-text">
                        {message.text}
                        {message.isTyping && (
                          <span className="typing-cursor">|</span>
                        )}
                      </div>
                      <div className="message-time">
                        {message.timestamp.toLocaleTimeString("tr-TR", {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading &&
                  messages[messages.length - 1]?.sender === "user" && (
                    <div className="message-wrapper bot-message">
                      <div className="bot-avatar">
                        <img
                          src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                          alt="Bot"
                          className="mini-avatar"
                        />
                      </div>
                      <div className="message-bubble">
                        <div className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  )}
                <div ref={messagesEndRef} />
              </div>
            </Card.Body>

            {/* Input */}
            <Card.Footer className="chat-footer">
              <Form className="d-flex gap-2">
                <Form.Control
                  type="text"
                  placeholder="Kariyer hedefinizi yazın..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isLoading}
                  className="message-input"
                />
                <Button
                  variant="primary"
                  onClick={handleSendMessage}
                  disabled={isLoading || inputValue.trim() === ""}
                  className="send-button"
                >
                  {isLoading ? (
                    <span className="spinner-border spinner-border-sm" />
                  ) : (
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="22" y1="2" x2="11" y2="13"></line>
                      <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                  )}
                </Button>
              </Form>
            </Card.Footer>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ChatInterface;
