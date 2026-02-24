from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from src.vector import retriever
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize LLM and Chain
try:
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = OllamaLLM(model="llama3.2", base_url=ollama_base_url)
    
    template = """
    You are an expert in answering questions about a pizza restaurant
    
    Here are some reviews: {reviews}
    
    Here is the question to answer: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    logger.info("LLM and Chain initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise e

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received question: {request.question}")
        reviews = retriever.invoke(request.question)
        result = chain.invoke({
            "reviews": reviews,
            "question": request.question
        })
        logger.info("Generated answer successfully.")
        return {"answer": result}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend)
# We mount this last to avoid satisfying API routes with static files if names collide
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
