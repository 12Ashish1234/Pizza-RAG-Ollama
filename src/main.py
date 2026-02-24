from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from src.vector import retriever

model = OllamaLLM(model="deepseek-v3.2:cloud")

template = """
You are an expert in answering questions about a pizza restaurant

Here are some reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("--------------------------------------------------")
    question = input("Ask your question: (q to quit):")
    print("--------------------------------------------------")

    if question == 'q':
        break
    
    reviews = retriever.invoke(question)
    result = chain.invoke({
        "reviews": reviews,
        "question": question
    })
    
    print(result)