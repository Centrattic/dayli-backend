import React, { useState, useEffect } from 'react';
import { Friend, FriendRecommendation } from '../types';
import { getFriends, getFriendRecommendations } from '../api';

interface FriendsProps {
    userId: string;
}

export const Friends: React.FC<FriendsProps> = ({ userId }) => {
    const [friends, setFriends] = useState<Friend[]>([]);
    const [recommendations, setRecommendations] = useState<FriendRecommendation[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadFriendsAndRecommendations();
    }, [userId]);

    const loadFriendsAndRecommendations = async () => {
        try {
            setLoading(true);
            const [friendsData, recommendationsData] = await Promise.all([
                getFriends(userId),
                getFriendRecommendations(userId)
            ]);
            setFriends(friendsData);
            setRecommendations(recommendationsData);
            setError(null);
        } catch (err) {
            setError('Failed to load friends and recommendations');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading friends...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="friends-container">
            <section className="friends-list">
                <h2>Your Friends</h2>
                {friends.length === 0 ? (
                    <p>No friends yet</p>
                ) : (
                    <ul>
                        {friends.map((friend) => (
                            <li key={friend.user_id} className="friend-item">
                                <h3>{friend.profile.user_id}</h3>
                                <p>{friend.profile.description}</p>
                                <p className="last-conversation">
                                    Last conversation: {friend.last_conversation_summary}
                                </p>
                            </li>
                        ))}
                    </ul>
                )}
            </section>

            <section className="friend-recommendations">
                <h2>Recommended Friends</h2>
                {recommendations.length === 0 ? (
                    <p>No recommendations available</p>
                ) : (
                    <ul>
                        {recommendations.map((rec) => (
                            <li key={rec.user_id} className="recommendation-item">
                                <h3>{rec.profile.user_id}</h3>
                                <p>{rec.profile.description}</p>
                                <p className="recommendation-reason">{rec.recommendation}</p>
                                <p className="confidence-score">
                                    Match confidence: {Math.round(rec.confidence_score * 100)}%
                                </p>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    );
}; 