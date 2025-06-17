from typing import List, Dict, Any, Optional
from .openai_service import OpenAIService
from .supabase_service import SupabaseService

class MatchingService:
    def __init__(self, openai_service: OpenAIService, supabase_service: SupabaseService):
        self.openai_service = openai_service
        self.supabase_service = supabase_service

    async def find_matches(self,
                          user_id: str,
                          interaction_type: str,
                          use_embeddings: bool = False,
                          group_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find matches for a user using either traditional or embedding-based matching."""
        # Get user's profile
        user_profile = await self.supabase_service.get_user_profile(user_id)
        
        if use_embeddings:
            return await self._find_embedding_matches(
                user_id,
                user_profile,
                interaction_type,
                group_id
            )
        else:
            return await self._find_traditional_matches(
                user_id,
                user_profile,
                interaction_type,
                group_id
            )

    async def _find_traditional_matches(self,
                                      user_id: str,
                                      user_profile: Dict[str, Any],
                                      interaction_type: str,
                                      group_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find matches using traditional AI-based matching."""
        # Get potential matches
        potential_matches = await self.supabase_service.get_potential_matches(
            user_id,
            interaction_type,
            group_id
        )
        
        matches = []
        for potential_match in potential_matches:
            # Simulate interaction between user models
            conversation, summary = await self.openai_service.simulate_model_interaction(
                user_profile["profile_data"]["description"],
                potential_match["profile_data"]["description"],
                interaction_type
            )
            
            # Get match recommendation
            recommendation = await self.openai_service.find_best_match(
                user_profile["profile_data"]["description"],
                interaction_type,
                [potential_match]
            )
            
            if recommendation["confidence_score"] > 0.7:  # Only include high-confidence matches
                matches.append({
                    "user_id": potential_match["user_id"],
                    "profile": potential_match,
                    "conversation_summary": summary,
                    "match_reason": recommendation["recommendation"],
                    "confidence_score": recommendation["confidence_score"],
                    "interaction_type": interaction_type,
                    "group_id": group_id
                })
        
        # Sort by confidence score
        matches.sort(key=lambda x: x["confidence_score"], reverse=True)
        return matches[:5]  # Return top 5 matches

    async def _find_embedding_matches(self,
                                    user_id: str,
                                    user_profile: Dict[str, Any],
                                    interaction_type: str,
                                    group_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find matches using embedding-based matching."""
        # Get potential matches
        potential_matches = await self.supabase_service.get_potential_matches(
            user_id,
            interaction_type,
            group_id
        )
        
        matches = []
        for potential_match in potential_matches:
            # Simulate interaction between user models
            conversation, summary = await self.openai_service.simulate_model_interaction(
                user_profile["profile_data"]["description"],
                potential_match["profile_data"]["description"],
                interaction_type
            )
            
            # Generate embedding for the interaction
            interaction_text = f"Interaction Type: {interaction_type}\nSummary: {summary}"
            interaction_embedding = await self.openai_service.generate_embedding(interaction_text)
            
            # Save the interaction
            await self.supabase_service.save_interaction(
                user_id,
                potential_match["user_id"],
                interaction_type,
                conversation,
                summary,
                interaction_embedding,
                group_id
            )
            
            # Find similar interactions
            similar_interactions = await self.supabase_service.find_similar_interactions(
                interaction_embedding,
                interaction_type,
                group_id
            )
            
            # Calculate average similarity score
            similarity_scores = [interaction["similarity_score"] for interaction in similar_interactions]
            avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
            
            matches.append({
                "user_id": potential_match["user_id"],
                "profile": potential_match,
                "conversation_summary": summary,
                "similarity_score": avg_similarity,
                "interaction_type": interaction_type,
                "group_id": group_id
            })
        
        # Sort by similarity score
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        return matches[:5]  # Return top 5 matches 