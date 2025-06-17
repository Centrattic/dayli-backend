from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from services.openai_service import OpenAIService
from services.supabase_service import SupabaseService
from services.user_interaction import UserInteractionService
from services.friend_recommendation import FriendRecommendationService
from services.matching_service import MatchingService

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_service = OpenAIService()
supabase_service = SupabaseService()
user_interaction_service = UserInteractionService(openai_service, supabase_service)
friend_recommendation_service = FriendRecommendationService(openai_service, supabase_service)
matching_service = MatchingService(openai_service, supabase_service)

class UserProfile(BaseModel):
    user_id: str
    description: str
    interests: List[str]

class ChatMessage(BaseModel):
    content: str
    sender_id: str
    receiver_id: str

class InteractionRequest(BaseModel):
    user_id: str
    interaction_type: str
    description: str
    preferences: List[str]
    target_group_id: Optional[str] = None
    use_embeddings: bool = False

@app.post("/users/{user_id}/profile")
async def update_user_profile(user_id: str, profile: UserProfile):
    try:
        await supabase_service.update_user_profile(user_id, profile.dict())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    try:
        profile = await supabase_service.get_user_profile(user_id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def send_message(message: ChatMessage):
    try:
        response = await user_interaction_service.process_message(message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/friends")
async def get_friends(user_id: str):
    try:
        friends = await supabase_service.get_user_friends(user_id)
        return friends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/recommendations")
async def get_friend_recommendations(user_id: str):
    try:
        recommendations = await friend_recommendation_service.get_recommendations(user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/matchmaking/request")
async def request_match(request: InteractionRequest):
    try:
        matches = await matching_service.find_matches(
            request.user_id,
            request.interaction_type,
            request.use_embeddings,
            request.target_group_id
        )
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/matchmaking/embeddings/{user_id}")
async def get_embedding_matches(
    user_id: str,
    interaction_type: str,
    group_id: Optional[str] = None
):
    try:
        matches = await matching_service.find_matches(
            user_id,
            interaction_type,
            use_embeddings=True,
            group_id=group_id
        )
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/interactions")
async def get_user_interactions(
    user_id: str,
    interaction_type: Optional[str] = None,
    group_id: Optional[str] = None
):
    try:
        interactions = await supabase_service.get_user_interactions(
            user_id,
            interaction_type,
            group_id
        )
        return interactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 