import os
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Directory configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Initialize Embeddings model (runs fully locally using sentence-transformers)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Global vector store reference
_vector_store = None

def extract_section(chunk_text: str) -> str:
    """
    Extracts the section name from a text chunk.
    If a line starting with '#' is found, it uses it as the section.
    Otherwise, it uses the first non-empty line of the chunk.
    """
    lines = [line.strip() for line in chunk_text.split("\n") if line.strip()]
    if not lines:
        return "General"
    
    # Check for Markdown headers
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
            
    # Fallback to the first non-empty line
    return lines[0]

def initialize_database():
    """
    Loads support documents from the data/ directory,
    chunks them, extracts metadata, and indexes them in FAISS.
    """
    global _vector_store
    
    if not os.path.exists(DATA_DIR):
        print(f"Warning: Data directory {DATA_DIR} does not exist.")
        return
        
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md") or filename.endswith(".txt"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
                
            # Perform character splitting on the file content
            chunks = text_splitter.split_text(content)
            
            # Formulate Document objects with metadata
            for chunk in chunks:
                section = extract_section(chunk)
                metadata = {
                    "source": filename,
                    "section": section
                }
                documents.append(Document(page_content=chunk, metadata=metadata))
                
    if documents:
        _vector_store = FAISS.from_documents(documents, embeddings)
        print(f"Successfully indexed {len(documents)} chunks in FAISS.")
    else:
        print("No documents found to index.")

def retrieve_context(query: str, k: int = 3):
    """
    Searches the FAISS vector database for the top-k most similar chunks.
    
    Returns:
        tuple: (list_of_string_chunks, list_of_metadata_dicts, average_similarity_score)
    """
    global _vector_store
    if _vector_store is None:
        # Lazy initialize if needed
        initialize_database()
        
    if _vector_store is None:
        return [], [], 0.0
        
    # similarity_search_with_score returns a list of tuples (Document, float_distance)
    # Note: FAISS uses L2 distance by default. A score of 0.0 is exact match.
    results = _vector_store.similarity_search_with_score(query, k=k)
    
    chunks = []
    metadata_list = []
    scores = []
    
    for doc, distance in results:
        chunks.append(doc.page_content)
        metadata_list.append(doc.metadata)
        # Convert L2 distance to similarity score in range [0, 1]
        similarity = 1.0 / (1.0 + distance)
        scores.append(similarity)
        
    avg_score = sum(scores) / len(scores) if scores else 0.0
    return chunks, metadata_list, avg_score

# Initialize on module load
initialize_database()
