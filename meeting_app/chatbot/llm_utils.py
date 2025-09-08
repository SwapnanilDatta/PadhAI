from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage

import os
from dotenv import load_dotenv
load_dotenv()  


def get_groq_response(session):
    try:
        # Import inside the function to avoid circular imports
        from .models import ChatMessage
        
        # Get recent messages for this session
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')

        history = []
        for msg in messages:
            if msg.role == 'user':
                history.append(HumanMessage(content=msg.content))
            else:
                history.append(AIMessage(content=msg.content))

        # Ensure we have at least one message
        if not history:
            return "I'm ready to help! Please send me a message."

        # Call Groq's LLaMA3-70B
        chat = ChatGroq(
            model="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )

        response = chat.invoke(history)
        return response.content
    
    except Exception as e:
        print(f"Error in get_groq_response: {e}")
        return f"Sorry, I encountered an error while processing your request: {str(e)}"