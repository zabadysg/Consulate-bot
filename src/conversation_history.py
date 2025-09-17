from typing import List, Dict, Any
from datetime import datetime

class ConversationHistory:
    """Manages conversation history for the bot"""
    
    def __init__(self, max_length: int = 10):
        self.max_length = max_length
        self.history: List[Dict[str, Any]] = []
    
    def add_message(self, user_input: str, bot_response: str):
        """Add a new conversation turn to history"""
        timestamp = datetime.now().isoformat()
        
        conversation_turn = {
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response
        }
        
        self.history.append(conversation_turn)
        
        # Keep only the last max_length conversations
        if len(self.history) > self.max_length:
            self.history = self.history[-self.max_length:]
    
    def get_formatted_history(self) -> str:
        """Get formatted conversation history for the prompt"""
        if not self.history:
            return "No previous conversation."
        
        formatted_history = []
        for turn in self.history:
            formatted_history.append(f"User: {turn['user']}")
            formatted_history.append(f"Assistant: {turn['bot']}")
            formatted_history.append("---")
        
        return "\n".join(formatted_history)
    
    def clear(self):
        """Clear conversation history"""
        self.history = []
    
    def get_history_dict(self) -> List[Dict[str, Any]]:
        """Get raw history as list of dictionaries"""
        return self.history.copy()
