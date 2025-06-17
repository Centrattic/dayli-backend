import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    async def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> None:
        """Update or create a user profile."""
        data = {
            "user_id": user_id,
            "profile_data": profile_data
        }
        await self.supabase.table("user_profiles").upsert(data).execute()

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get a user's profile."""
        response = await self.supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
        if not response.data:
            raise Exception("User profile not found")
        return response.data[0]

    async def save_conversation(self, 
                              user_id: str, 
                              other_user_id: str, 
                              messages: List[Dict[str, str]], 
                              summary: str) -> None:
        """Save a conversation and its summary."""
        data = {
            "user_id": user_id,
            "other_user_id": other_user_id,
            "messages": messages,
            "summary": summary,
            "timestamp": "now()"
        }
        await self.supabase.table("conversations").insert(data).execute()

    async def get_user_friends(self, user_id: str) -> List[Dict[str, Any]]:
        """Get a user's friends list with their latest conversation summaries."""
        response = await self.supabase.table("conversations")\
            .select("other_user_id, summary")\
            .eq("user_id", user_id)\
            .order("timestamp", desc=True)\
            .execute()
        
        friends = []
        for conv in response.data:
            friend_profile = await self.get_user_profile(conv["other_user_id"])
            friends.append({
                "user_id": conv["other_user_id"],
                "profile": friend_profile,
                "last_conversation_summary": conv["summary"]
            })
        return friends

    async def get_potential_friends(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get potential friends for recommendations."""
        # Get users who haven't interacted with the current user
        response = await self.supabase.table("user_profiles")\
            .select("*")\
            .neq("user_id", user_id)\
            .limit(limit)\
            .execute()
        
        return response.data

    async def save_friend_recommendation(self, 
                                       user_id: str, 
                                       recommended_user_id: str, 
                                       recommendation_data: Dict[str, Any]) -> None:
        """Save a friend recommendation."""
        data = {
            "user_id": user_id,
            "recommended_user_id": recommended_user_id,
            "recommendation_data": recommendation_data,
            "timestamp": "now()"
        }
        await self.supabase.table("friend_recommendations").insert(data).execute()

    async def get_conversation_history(self, 
                                     user_id: str, 
                                     other_user_id: str, 
                                     limit: int = 50) -> List[Dict[str, str]]:
        """Get conversation history between two users."""
        response = await self.supabase.table("conversations")\
            .select("messages")\
            .or_(f"user_id.eq.{user_id},other_user_id.eq.{user_id}")\
            .or_(f"user_id.eq.{other_user_id},other_user_id.eq.{other_user_id}")\
            .order("timestamp", desc=True)\
            .limit(limit)\
            .execute()
        
        messages = []
        for conv in response.data:
            messages.extend(conv["messages"])
        return messages 