import os
from openai import AsyncOpenAI
from typing import List, Dict, Any, Tuple
import numpy as np

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"  # Using the latest GPT-4 model
        self.embedding_model = "text-embedding-ada-002"
        self.max_interaction_tokens = 2000  # Maximum tokens for model interactions

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

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for the given text."""
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    async def simulate_model_interaction(self, 
                                      user1_description: str, 
                                      user2_description: str,
                                      interaction_type: str,
                                      max_tokens: int = None) -> Tuple[List[Dict[str, str]], str]:
        """Simulate an interaction between two user models."""
        if max_tokens is None:
            max_tokens = self.max_interaction_tokens

        conversation = []
        total_tokens = 0
        
        # Initial prompt for the interaction
        system_prompt = f"""You are simulating an interaction between two people with the following descriptions:
        
        Person 1: {user1_description}
        Person 2: {user2_description}
        
        The interaction type is: {interaction_type}
        
        Generate a natural conversation between these two people, considering their personalities and the interaction type.
        Keep responses concise and focused on the interaction type."""

        # Start the conversation
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}],
            max_tokens=150
        )
        
        conversation.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        total_tokens += len(response.choices[0].message.content.split())

        # Continue the conversation until max tokens
        while total_tokens < max_tokens:
            # Generate response from user 1
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[{"role": msg["role"], "content": msg["content"]} for msg in conversation],
                    {"role": "user", "content": "Continue the conversation from Person 1's perspective"}
                ],
                max_tokens=150
            )
            
            conversation.append({
                "role": "user",
                "content": response.choices[0].message.content
            })
            total_tokens += len(response.choices[0].message.content.split())

            if total_tokens >= max_tokens:
                break

            # Generate response from user 2
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[{"role": msg["role"], "content": msg["content"]} for msg in conversation],
                    {"role": "user", "content": "Continue the conversation from Person 2's perspective"}
                ],
                max_tokens=150
            )
            
            conversation.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            total_tokens += len(response.choices[0].message.content.split())

        # Generate summary of the interaction
        summary = await self.summarize_conversation(conversation)
        
        return conversation, summary

    async def find_best_match(self, 
                            user_description: str,
                            interaction_type: str,
                            potential_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find the best match for a user based on their description and interaction type."""
        prompt = f"""Given the following user description and potential matches, determine the best match for the specified interaction type:

        User Description: {user_description}
        Interaction Type: {interaction_type}

        Potential Matches:
        {potential_matches}

        Consider:
        1. Compatibility of personalities
        2. Relevance to the interaction type
        3. Potential for meaningful interaction
        4. Shared interests or complementary traits

        Provide a detailed explanation for your choice and a confidence score (0-1)."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300
        )

        # Parse the response to extract the match and confidence score
        content = response.choices[0].message.content
        confidence_score = 0.85  # Default score, could be made more sophisticated

        return {
            "recommendation": content,
            "confidence_score": confidence_score
        }

    async def find_embedding_matches(self,
                                   user_embedding: List[float],
                                   interaction_type: str,
                                   potential_matches: List[Dict[str, Any]],
                                   top_k: int = 5) -> List[Dict[str, Any]]:
        """Find matches based on embedding similarity."""
        matches = []
        
        for match in potential_matches:
            match_embedding = match["profile_data"]["description_embedding"]
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(user_embedding, match_embedding)
            
            matches.append({
                "user_id": match["user_id"],
                "profile": match,
                "similarity_score": similarity,
                "interaction_type": interaction_type
            })
        
        # Sort by similarity score and return top k
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        return matches[:top_k]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)) 