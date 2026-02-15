# Pizza Restaurant RAG Chatbot 🍕

A local Retrieval-Augmented Generation (RAG) application that answers questions about a pizza restaurant based on customer reviews. Built with **LangChain**, **Ollama**, **ChromaDB**, and **FastAPI**.

## Features

-   **Hybrid Search**: Combines **Semantic Search** (ChromaDB) and **Keyword Search** (BM25) for highly accurate retrieval.
-   **Local LLM**: Uses **Ollama** (Llama 3.2) for privacy and local inference.
-   **Web Interface**: Clean, responsive frontend built with vanilla HTML/CSS/JS.
-   **Optimized Performance**: Pickles the BM25 retriever to speed up initialization.
-   **REST API**: Backend powered by **FastAPI**.

## Prerequisites

-   **Python 3.11+**
-   **Ollama**: Download and install from [ollama.com](https://ollama.com/).
    -   Pull the implementation model: `ollama pull llama3.2`
    -   Pull the embedding model: `ollama pull mxbai-embed-large`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .env
    source .env/bin/activate  # On Windows: .env\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Server**:
    ```bash
    python server.py
    ```

2.  **Access the App**:
    Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

3.  **Chat**:
    Ask questions like:
    -   "How is the pizza crust?"
    -   "Do they have good vegan options?"
    -   "What do people say about the service?"

## Docker Usage

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
2.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000)

## Project Structure

-   `server.py`: FastAPI backend that handles chat requests.
-   `vector.py`: RAG logic, initializing the Hybrid Search (Chroma + BM25).
-   `frontend/`: Contains the static web assets (`index.html`, `style.css`, `script.js`).
-   `requirements.txt`: Python package dependencies.
-   `realistic_restaurant_reviews.csv`: Dataset used for the knowledge base.

## Technologies Used

-   [LangChain](https://www.langchain.com/) - Orchestration
-   [Ollama](https://ollama.com/) - LLM & Embeddings
-   [ChromaDB](https://www.trychroma.com/) - Vector Store
-   [FastAPI](https://fastapi.tiangolo.com/) - Backend API
-   [Rank-BM25](https://github.com/dorianbrown/rank_bm25) - Keyword Search algorithm
