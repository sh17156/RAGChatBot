from flask import Flask, render_template, request, jsonify
from app.document_loader import DocumentLoader
from app.embeddings_manager import EmbeddingsManager
from app.vector_store import VectorStoreManager
from app.chat_manager import ChatManager
import os
from dotenv import load_dotenv

load_dotenv()

# Update the template and static folder paths
app = Flask(__name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# Initialize components
embeddings_manager = EmbeddingsManager()
vector_store = VectorStoreManager("data/vector_store")
chat_manager = ChatManager(provider='openai', model='gpt-3.5-turbo')

# Initialize vector store
def initialize_vector_store():
    try:
        # Try to load existing store
        if os.path.exists("data/vector_store"):
            vector_store.load_store()
        else:
            # Create new store if it doesn't exist
            os.makedirs("data/vector_store", exist_ok=True)
            documents = DocumentLoader.load_documents("data/documents")
            if documents:  # Check if we have any documents
                chunks = embeddings_manager.split_documents(documents)
                vector_store.initialize_store(chunks)
            else:
                print("Warning: No documents found in data/documents directory")
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        # Always create a new store if loading fails
        documents = DocumentLoader.load_documents("data/documents")
        if documents:
            chunks = embeddings_manager.split_documents(documents)
            vector_store.initialize_store(chunks)

# Initialize on startup
initialize_vector_store()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json['query']
    
    # Get relevant documents
    relevant_docs = vector_store.similarity_search(query)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Get response
    response = chat_manager.get_response(query, context)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False) 