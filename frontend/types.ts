export interface UserProfile {
    user_id: string;
    description: string;
    interests: string[];
    groups: Group[];
    description_embedding: number[];
}

export interface Group {
    id: string;
    name: string;
    type: 'work' | 'friends' | 'club' | 'other';
    description: string;
}

export interface InteractionRequest {
    user_id: string;
    target_group_id?: string;
    interaction_type: string;
    description: string;
    preferences: string[];
}

export interface ChatMessage {
    content: string;
    sender_id: string;
    receiver_id: string;
    group_id?: string;
}

export interface Interaction {
    id: string;
    user_id: string;
    other_user_id: string;
    messages: Array<{
        role: 'user' | 'assistant';
        content: string;
    }>;
    summary: string;
    embedding: number[];
    group_id?: string;
    timestamp: string;
}

export interface Match {
    user_id: string;
    profile: UserProfile;
    match_score: number;
    match_reason: string;
    interaction_type: string;
    group_id?: string;
}

export interface ChatResponse {
    response: string;
    conversation_history: Array<{
        role: 'user' | 'assistant';
        content: string;
    }>;
    updated_user_description?: string;
}

export interface UserDescription {
    user_id: string;
    description: string;
    embedding: number[];
    last_updated: string;
}

export interface Friend {
    user_id: string;
    profile: UserProfile;
    last_conversation_summary: string;
}

export interface FriendRecommendation {
    user_id: string;
    profile: UserProfile;
    recommendation: string;
    confidence_score: number;
} 