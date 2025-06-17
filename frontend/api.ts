import axios from 'axios';
import { 
    UserProfile, 
    ChatMessage, 
    Match, 
    ChatResponse, 
    InteractionRequest,
    Group,
    Interaction,
    UserDescription
} from './types';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// User Profile Endpoints
export const updateUserProfile = async (userId: string, profile: UserProfile): Promise<void> => {
    try {
        await api.post(`/users/${userId}/profile`, profile);
    } catch (error) {
        console.error('Error updating user profile:', error);
        throw error;
    }
};

export const getUserProfile = async (userId: string): Promise<UserProfile> => {
    try {
        const response = await api.get(`/users/${userId}/profile`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        throw error;
    }
};

// Group Endpoints
export const getUserGroups = async (userId: string): Promise<Group[]> => {
    try {
        const response = await api.get(`/users/${userId}/groups`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user groups:', error);
        throw error;
    }
};

export const createGroup = async (group: Omit<Group, 'id'>): Promise<Group> => {
    try {
        const response = await api.post('/groups', group);
        return response.data;
    } catch (error) {
        console.error('Error creating group:', error);
        throw error;
    }
};

// Chat and Interaction Endpoints
export const sendMessage = async (message: ChatMessage): Promise<ChatResponse> => {
    try {
        const response = await api.post('/chat', message);
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};

export const getInteractions = async (userId: string, groupId?: string): Promise<Interaction[]> => {
    try {
        const url = groupId 
            ? `/users/${userId}/interactions?group_id=${groupId}`
            : `/users/${userId}/interactions`;
        const response = await api.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching interactions:', error);
        throw error;
    }
};

// Matchmaking Endpoints
export const requestMatch = async (request: InteractionRequest): Promise<Match[]> => {
    try {
        const response = await api.post('/matchmaking/request', request);
        return response.data;
    } catch (error) {
        console.error('Error requesting match:', error);
        throw error;
    }
};

export const getEmbeddingMatches = async (
    userId: string, 
    interactionType: string,
    groupId?: string
): Promise<Match[]> => {
    try {
        const url = groupId
            ? `/matchmaking/embeddings/${userId}?interaction_type=${interactionType}&group_id=${groupId}`
            : `/matchmaking/embeddings/${userId}?interaction_type=${interactionType}`;
        const response = await api.get(url);
        return response.data;
    } catch (error) {
        console.error('Error getting embedding matches:', error);
        throw error;
    }
};

// User Description Endpoints
export const updateUserDescription = async (
    userId: string, 
    description: string
): Promise<UserDescription> => {
    try {
        const response = await api.post(`/users/${userId}/description`, { description });
        return response.data;
    } catch (error) {
        console.error('Error updating user description:', error);
        throw error;
    }
};

export const getUserDescription = async (userId: string): Promise<UserDescription> => {
    try {
        const response = await api.get(`/users/${userId}/description`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user description:', error);
        throw error;
    }
}; 