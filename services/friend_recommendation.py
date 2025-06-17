from typing import List, Dict, Any
from .openai_service import OpenAIService
from .supabase_service import SupabaseService

class FriendRecommendationService:
    def __init__(self, openai_service: OpenAIService, supabase_service: SupabaseService):
        self.openai_service = openai_service
        self.supabase_service = supabase_service

    async def get_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get friend recommendations for a user."""
        # Get user's profile
        user_profile = await self.supabase_service.get_user_profile(user_id)
        
        # Get potential friends
        potential_friends = await self.supabase_service.get_potential_friends(user_id)
        
        # Get recommendations from AI
        recommendations = []
        for potential_friend in potential_friends:
            recommendation = await self.openai_service.generate_friend_recommendation(
                user_profile["profile_data"]["description"],
                [potential_friend]
            )
            
            if recommendation["confidence_score"] > 0.7:  # Only include high-confidence recommendations
                recommendations.append({
                    "user_id": potential_friend["user_id"],
                    "profile": potential_friend,
                    "recommendation": recommendation["recommendation"],
                    "confidence_score": recommendation["confidence_score"]
                })
                
                # Save the recommendation
                await self.supabase_service.save_friend_recommendation(
                    user_id,
                    potential_friend["user_id"],
                    recommendation
                )
        
        # Sort recommendations by confidence score
        recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations

    async def get_recommendation_explanation(self, 
                                          user_id: str, 
                                          recommended_user_id: str) -> Dict[str, Any]:
        """Get a detailed explanation for why a specific user was recommended."""
        # Get both users' profiles
        user_profile = await self.supabase_service.get_user_profile(user_id)
        recommended_profile = await self.supabase_service.get_user_profile(recommended_user_id)
        
        # Get any existing conversation summaries
        conversation_summaries = await self.supabase_service.get_conversation_history(
            user_id,
            recommended_user_id
        )
        
        # Generate explanation
        explanation = await self.openai_service.generate_friend_recommendation(
            user_profile["profile_data"]["description"],
            [{
                **recommended_profile,
                "conversation_history": conversation_summaries
            }]
        )
        
        return {
            "explanation": explanation["recommendation"],
            "confidence_score": explanation["confidence_score"]
        } 