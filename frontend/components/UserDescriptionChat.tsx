import React, { useState, useEffect } from 'react';
import { ChatMessage, ChatResponse, UserDescription } from '../types';
import { sendMessage, getUserDescription, updateUserDescription } from '../api';

interface UserDescriptionChatProps {
    userId: string;
}

export const UserDescriptionChat: React.FC<UserDescriptionChatProps> = ({ userId }) => {
    const [message, setMessage] = useState('');
    const [conversation, setConversation] = useState<ChatResponse['conversation_history']>([]);
    const [userDescription, setUserDescription] = useState<UserDescription | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadUserDescription();
    }, [userId]);

    const loadUserDescription = async () => {
        try {
            const description = await getUserDescription(userId);
            setUserDescription(description);
        } catch (err) {
            setError('Failed to load user description');
        }
    };

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!message.trim()) return;

        const chatMessage: ChatMessage = {
            content: message,
            sender_id: userId,
            receiver_id: 'ai' // Special ID for AI interactions
        };

        try {
            setLoading(true);
            const response = await sendMessage(chatMessage);
            setConversation(response.conversation_history);
            setMessage('');
            setError(null);

            // If the AI has updated the user description, update it
            if (response.updated_user_description) {
                await updateUserDescription(userId, response.updated_user_description);
                await loadUserDescription();
            }
        } catch (err) {
            setError('Failed to send message');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="user-description-chat">
            <div className="current-description">
                <h3>Your Current Description</h3>
                {userDescription ? (
                    <div className="description-content">
                        <p>{userDescription.description}</p>
                        <p className="last-updated">
                            Last updated: {new Date(userDescription.last_updated).toLocaleString()}
                        </p>
                    </div>
                ) : (
                    <p>No description yet. Start chatting to build your profile!</p>
                )}
            </div>

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
                        placeholder="Tell me about yourself..."
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Sending...' : 'Send'}
                    </button>
                </form>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="chat-tips">
                <h4>Tips for better matches:</h4>
                <ul>
                    <li>Share your interests and hobbies</li>
                    <li>Describe your communication style</li>
                    <li>Mention your professional background</li>
                    <li>Talk about your social preferences</li>
                    <li>Share your goals and aspirations</li>
                </ul>
            </div>
        </div>
    );
}; 