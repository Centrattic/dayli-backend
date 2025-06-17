# AI-Powered Social Networking Backend

This is the backend for a social networking application where users interact with AI models that learn about them and facilitate interactions with other users.

## Features

- User profile management with AI-generated descriptions
- Real-time chat with AI-powered responses
- Conversation summarization
- Friend recommendations based on user profiles and interactions
- Supabase integration for data persistence

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
4. Set up your Supabase database with the following tables:
   - user_profiles
   - conversations
   - friend_recommendations

## Database Schema

### user_profiles
- user_id (primary key)
- profile_data (JSON)
  - description
  - interests
  - other profile fields

### conversations
- id (primary key)
- user_id
- other_user_id
- messages (JSON array)
- summary
- timestamp

### friend_recommendations
- id (primary key)
- user_id
- recommended_user_id
- recommendation_data (JSON)
- timestamp

## Running the Server

```bash
uvicorn main:app --reload
```

The server will start on http://localhost:8000

## API Endpoints

- POST /users/{user_id}/profile - Update user profile
- GET /users/{user_id}/profile - Get user profile
- POST /chat - Send a message
- GET /users/{user_id}/friends - Get user's friends
- GET /users/{user_id}/recommendations - Get friend recommendations

## Environment Variables

- OPENAI_API_KEY: Your OpenAI API key
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_KEY: Your Supabase API key
- PORT: Server port (default: 8000)
- HOST: Server host (default: 0.0.0.0)
