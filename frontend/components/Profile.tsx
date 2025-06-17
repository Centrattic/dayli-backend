import React, { useState, useEffect } from 'react';
import { UserProfile } from '../types';
import { getUserProfile, updateUserProfile } from '../api';

interface ProfileProps {
    userId: string;
}

export const Profile: React.FC<ProfileProps> = ({ userId }) => {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadProfile();
    }, [userId]);

    const loadProfile = async () => {
        try {
            setLoading(true);
            const data = await getUserProfile(userId);
            setProfile(data);
            setError(null);
        } catch (err) {
            setError('Failed to load profile');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateProfile = async (updatedProfile: UserProfile) => {
        try {
            await updateUserProfile(userId, updatedProfile);
            await loadProfile(); // Reload the profile after update
        } catch (err) {
            setError('Failed to update profile');
        }
    };

    if (loading) return <div>Loading profile...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!profile) return <div>No profile found</div>;

    return (
        <div className="profile-container">
            <h2>User Profile</h2>
            <div className="profile-info">
                <p><strong>User ID:</strong> {profile.user_id}</p>
                <p><strong>Description:</strong> {profile.description}</p>
                <div>
                    <strong>Interests:</strong>
                    <ul>
                        {profile.interests.map((interest, index) => (
                            <li key={index}>{interest}</li>
                        ))}
                    </ul>
                </div>
            </div>
            {/* Add profile edit form here if needed */}
        </div>
    );
}; 