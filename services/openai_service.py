import os
from openai import AsyncOpenAI
from typing import List, Dict, Any

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"  # Using the latest GPT-4 model

    async def generate_user_description(self, conversation_history: List[Dict[str, str]]) -> str:
        """Generate a user description based on conversation history."""
        prompt = f"""Based on the following conversation history, create a detailed description of the user's personality, interests, and communication style. 
        Focus on key traits that would be relevant for social interactions.
        
        Conversation History:
        {conversation_history}
        
        Generate a concise but comprehensive description:"""
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content

    async def generate_chat_response(self, 
                                   user_description: str, 
                                   other_user_description: str, 
                                   conversation_history: List[Dict[str, str]]) -> str:
        """Generate a chat response considering both users' descriptions."""
        prompt = f"""You are having a conversation with another person. Here are the relevant descriptions:

        Your description: {user_description}
        Other person's description: {other_user_description}

        Previous conversation:
        {conversation_history}

        Generate a natural, engaging response that matches your personality:"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content

    async def summarize_conversation(self, conversation_history: List[Dict[str, str]]) -> str:
        """Summarize a conversation for future reference."""
        prompt = f"""Summarize the following conversation in a concise paragraph, highlighting key topics discussed and any notable insights or connections made:

        {conversation_history}

        Summary:"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content

    async def generate_friend_recommendation(self, 
                                          user_description: str, 
                                          potential_friends: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate friend recommendations based on user descriptions."""
        prompt = f"""Given the following user description and potential friends, recommend the best match and explain why:

        User Description: {user_description}

        Potential Friends:
        {potential_friends}

        Provide a recommendation with explanation:"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300
        )
        return {
            "recommendation": response.choices[0].message.content,
            "confidence_score": 0.85  # This could be made more sophisticated
        } 