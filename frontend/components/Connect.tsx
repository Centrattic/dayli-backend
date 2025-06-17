import React, { useState, useEffect } from 'react';
import { InteractionRequest, Group, Match } from '../types';
import { requestMatch, getUserGroups, getEmbeddingMatches } from '../api';

interface ConnectProps {
    userId: string;
}

export const Connect: React.FC<ConnectProps> = ({ userId }) => {
    const [groups, setGroups] = useState<Group[]>([]);
    const [selectedGroup, setSelectedGroup] = useState<string>('');
    const [interactionType, setInteractionType] = useState('');
    const [description, setDescription] = useState('');
    const [preferences, setPreferences] = useState<string[]>([]);
    const [matches, setMatches] = useState<Match[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [useEmbeddings, setUseEmbeddings] = useState(false);

    useEffect(() => {
        loadGroups();
    }, [userId]);

    const loadGroups = async () => {
        try {
            const groupsData = await getUserGroups(userId);
            setGroups(groupsData);
        } catch (err) {
            setError('Failed to load groups');
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            let matchesData: Match[];
            
            if (useEmbeddings) {
                matchesData = await getEmbeddingMatches(
                    userId,
                    interactionType,
                    selectedGroup || undefined
                );
            } else {
                const request: InteractionRequest = {
                    user_id: userId,
                    target_group_id: selectedGroup || undefined,
                    interaction_type: interactionType,
                    description,
                    preferences
                };
                matchesData = await requestMatch(request);
            }
            
            setMatches(matchesData);
        } catch (err) {
            setError('Failed to find matches');
        } finally {
            setLoading(false);
        }
    };

    const handlePreferenceChange = (pref: string) => {
        setPreferences(prev => 
            prev.includes(pref)
                ? prev.filter(p => p !== pref)
                : [...prev, pref]
        );
    };

    return (
        <div className="connect-container">
            <h2>Find Your Match</h2>
            
            <form onSubmit={handleSubmit} className="connect-form">
                <div className="form-group">
                    <label>Group (Optional)</label>
                    <select 
                        value={selectedGroup}
                        onChange={(e) => setSelectedGroup(e.target.value)}
                    >
                        <option value="">All Groups</option>
                        {groups.map(group => (
                            <option key={group.id} value={group.id}>
                                {group.name} ({group.type})
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label>Type of Interaction</label>
                    <input
                        type="text"
                        value={interactionType}
                        onChange={(e) => setInteractionType(e.target.value)}
                        placeholder="e.g., casual chat, professional discussion"
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Description</label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Describe what kind of interaction you're looking for..."
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Preferences</label>
                    <div className="preferences-list">
                        {['Professional', 'Casual', 'Technical', 'Creative', 'Social'].map(pref => (
                            <label key={pref} className="preference-item">
                                <input
                                    type="checkbox"
                                    checked={preferences.includes(pref)}
                                    onChange={() => handlePreferenceChange(pref)}
                                />
                                {pref}
                            </label>
                        ))}
                    </div>
                </div>

                <div className="form-group">
                    <label className="checkbox-label">
                        <input
                            type="checkbox"
                            checked={useEmbeddings}
                            onChange={(e) => setUseEmbeddings(e.target.checked)}
                        />
                        Use embedding-based matching
                    </label>
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Finding Matches...' : 'Find Matches'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {matches.length > 0 && (
                <div className="matches-section">
                    <h3>Your Matches</h3>
                    <div className="matches-list">
                        {matches.map(match => (
                            <div key={match.user_id} className="match-card">
                                <h4>{match.profile.user_id}</h4>
                                <p>{match.profile.description}</p>
                                <p className="match-reason">{match.match_reason}</p>
                                <p className="match-score">
                                    Match Score: {Math.round(match.match_score * 100)}%
                                </p>
                                <button 
                                    className="connect-button"
                                    onClick={() => {/* Handle connection request */}}
                                >
                                    Connect
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}; 