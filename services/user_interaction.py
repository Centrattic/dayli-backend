from typing import List, Dict, Any
from .openai_service import OpenAIService
from .supabase_service import SupabaseService

class UserInteractionService:
    def __init__(self, openai_service: OpenAIService, supabase_service: SupabaseService):
        self.openai_service = openai_service
        self.supabase_service = supabase_service
        self.max_tokens_per_conversation = 2000  # Adjust based on your needs

    async def process_message(self, message: Dict[str, str]) -> Dict[str, Any]:
        """Process a new message in a conversation."""
        # Get both users' profiles
        sender_profile = await self.supabase_service.get_user_profile(message["sender_id"])
        receiver_profile = await self.supabase_service.get_user_profile(message["receiver_id"])

        # Get conversation history
        conversation_history = await self.supabase_service.get_conversation_history(
            message["sender_id"],
            message["receiver_id"]
        )

        # Add the new message to history
        conversation_history.append({
            "role": "user",
            "content": message["content"]
        })

        # Generate AI response
        ai_response = await self.openai_service.generate_chat_response(
            sender_profile["profile_data"]["description"],
            receiver_profile["profile_data"]["description"],
            conversation_history
        )

        # Add AI response to history
        conversation_history.append({
            "role": "assistant",
            "content": ai_response
        })

        # Check if we should summarize the conversation
        if self._should_summarize_conversation(conversation_history):
            summary = await self.openai_service.summarize_conversation(conversation_history)
            await self.supabase_service.save_conversation(
                message["sender_id"],
                message["receiver_id"],
                conversation_history,
                summary
            )
            # Clear conversation history after saving
            conversation_history = []

        return {
            "response": ai_response,
            "conversation_history": conversation_history
        }

    def _should_summarize_conversation(self, conversation_history: List[Dict[str, str]]) -> bool:
        """Determine if the conversation should be summarized based on token count."""
        # This is a simplified version - in production, you'd want to use a proper tokenizer
        total_tokens = sum(len(msg["content"].split()) for msg in conversation_history)
        return total_tokens >= self.max_tokens_per_conversation

    async def update_user_description(self, user_id: str, conversation_history: List[Dict[str, str]]) -> None:
        """Update a user's description based on their conversation history."""
        new_description = await self.openai_service.generate_user_description(conversation_history)
        
        # Get current profile
        current_profile = await self.supabase_service.get_user_profile(user_id)
        
        # Update profile with new description
        current_profile["profile_data"]["description"] = new_description
        await self.supabase_service.update_user_profile(user_id, current_profile["profile_data"]) 