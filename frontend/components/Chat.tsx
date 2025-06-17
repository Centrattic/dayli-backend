import React, { useState, useEffect } from 'react';
import { ChatMessage, ChatResponse } from '../types';
import { sendMessage } from '../api';

interface ChatProps {
    userId: string;
    otherUserId: string;
}

export const Chat: React.FC<ChatProps> = ({ userId, otherUserId }) => {
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState<ChatResponse['conversation_history']>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!message.trim()) return;

        const chatMessage: ChatMessage = {
            content: message,
            sender_id: userId,
            receiver_id: otherUserId
        };

        try {
            setLoading(true);
            const response = await sendMessage(chatMessage);
            setConversation(response.conversation_history);
            setMessage('');
            setError(null);
        } catch (err) {
            setError('Failed to send message');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {conversation.map((msg, index) => (
                    <div 
                        key={index} 
                        className={`message ${msg.role === 'user' ? 'user-message' : 'ai-message'}`}
                    >
                        <p>{msg.content}</p>
                    </div>
                ))}
            </div>

            <form onSubmit={handleSendMessage} className="chat-input-form">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}
        </div>
    );
}; 