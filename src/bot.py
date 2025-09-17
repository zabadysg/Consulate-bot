import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import Config
from .conversation_history import ConversationHistory

class SimpleConsulateBot:
    """Simple LangChain-based Consulate Bot"""
    
    def __init__(self):
        """Initialize the simple bot"""
        
        # Load documentation
        self.docs = self._load_docs()
        
        # Initialize LangChain components
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
        )
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_template(
            """You are a professional and friendly assistant representing the Consulate General of Egypt in Paris.  
Your role is to support Egyptian citizens in France by providing accurate, clear, and respectful information about consular services.  

### Your Responsibilities:
1. **Welcome & Context**  
   - Greet users warmly.  
   - Briefly explain the consulate’s mission: serving the Egyptian community in France with professionalism, efficiency, and care.  

2. **Provide Consular Information**  
   - Answer questions about consular services (e.g., passport issuance/renewal, civil status documents, notarial services).  
   - Clearly explain required documents, eligibility, fees, steps, and timelines, based on the provided documentation.  

3. **Service Updates & Instructions**  
   - Share official updates, service changes, and procedural guidance when available.  

4. **Guidance to Official Channels**  
   - Direct users to the official consulate communication channels (phone, WhatsApp, Facebook) for further inquiries or case-specific support.  

5. **Tone & Conduct**  
   - Always communicate in a professional, respectful, and supportive manner.  
   - Be concise, avoid speculation, and never provide unverified information.  

6. **Fallback**  
   - If the answer is not covered in the provided documentation, politely recommend contacting the consulate directly for clarification.  

---

### Knowledge Base
Use only the following source for accurate answers:  
**Consulate Documentation:**  
{docs}  

---

### Conversation Context
{conversation_history}  

---

### User Input
{user_input}  

---

### Important Instructions
- Always prioritize **accuracy, clarity, and helpfulness**.  
- Stay aligned with the consulate’s mission and values.  
- Never fabricate or assume information beyond the provided documentation.  

"""
        )
        
        # Create the chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()
        
        # Initialize conversation history
        self.conversation_history = ConversationHistory(Config.MAX_HISTORY_LENGTH)
    
    def _load_docs(self) -> str:
        """Load documentation from file"""
        try:
            with open(Config.DOCS_FILE_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Documentation file not found."
        except Exception as e:
            return f"Error loading documentation: {str(e)}"
        
    async def stream_response(self, user_input: str):
        """Get async streaming response from the bot"""
        try:
            # Prepare prompt variables
            prompt_vars = {
                "docs": self.docs,
                "conversation_history": self.conversation_history.get_formatted_history(),
                "user_input": user_input
            }
            
            # Stream response from the chain
            full_response = ""
            async for chunk in self.chain.astream(prompt_vars):
                if chunk:
                    full_response += chunk
                    yield chunk
            
            # Add to conversation history
            self.conversation_history.add_message(user_input, full_response)
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            self.conversation_history.add_message(user_input, error_message)
            yield error_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history.get_history_dict()


# Simple function interface
def create_bot():
    """Create a simple bot instance"""
    return SimpleConsulateBot()

async def stream_consulate_response(user_input: str, bot: SimpleConsulateBot = None):
    """Simple async function to get a streaming response"""
    if bot is None:
        bot = create_bot()
    async for chunk in bot.stream_response(user_input):
        yield chunk
