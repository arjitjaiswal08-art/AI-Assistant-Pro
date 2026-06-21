import streamlit as st
from groq import Groq
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer
from datetime import datetime

# ---- SETUP ----
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdf(file):
    """Extract text from uploaded PDF"""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500):
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def save_chat_to_history():
    """Save current chat to history"""
    if st.session_state.messages:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        first_message = st.session_state.messages[0]["content"][:50] + "..." if len(st.session_state.messages[0]["content"]) > 50 else st.session_state.messages[0]["content"]
        
        chat_entry = {
            "timestamp": timestamp,
            "title": first_message,
            "messages": st.session_state.messages.copy()
        }
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.insert(0, chat_entry)
        
        # Keep only last 20 chats
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[:20]

def load_chat_from_history(index):
    """Load a chat from history"""
    if "chat_history" in st.session_state and index < len(st.session_state.chat_history):
        st.session_state.messages = st.session_state.chat_history[index]["messages"].copy()
        st.rerun()

def start_new_chat():
    """Start a new chat"""
    if st.session_state.messages:
        save_chat_to_history()
    st.session_state.messages = []
    st.rerun()

# ---- PAGE CONFIGURATION ----
st.set_page_config(
    page_title="AI Assistant Pro | Enterprise Edition", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state FIRST
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []

if "pdf_embeddings" not in st.session_state:
    st.session_state.pdf_embeddings = None

# Custom CSS with Watermark
st.markdown("""
    <style>
    /* Watermark Badge */
    .watermark {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        padding: 10px 20px;
        border-radius: 50px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid #e2e8f0;
        font-size: 13px;
        font-weight: 600;
        color: #0f172a;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .watermark:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    .watermark-icon {
        font-size: 16px;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    </style>
    
    <div class="watermark">
        <span class="watermark-icon">✨</span>
        <span>Made by Arjit Jaiswal</span>
    </div>
""", unsafe_allow_html=True)

st.title("🤖 AI Assistant Pro")
st.caption("☁️ Cloud Edition • Powered by Groq")

# ---- SIDEBAR ----
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Input
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get your free API key from console.groq.com",
        value=st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key to use the chatbot")
        st.info("🔑 Get a free API key at [console.groq.com](https://console.groq.com/)")

    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    selected_model = st.selectbox("Choose AI Model", models)

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a professional AI assistant with expertise across multiple domains. Provide clear, accurate, and helpful responses.",
        height=100
    )

    st.divider()
    
    # New Chat Button
    st.markdown("### 💬 Chat Management")
    if st.button("✨ New Chat", use_container_width=True, type="primary"):
        start_new_chat()
    
    # Chat History
    if st.session_state.chat_history:
        st.markdown("##### 📜 Chat History")
        st.caption(f"{len(st.session_state.chat_history)} saved conversations")
        
        with st.expander("View History", expanded=False):
            for idx, chat in enumerate(st.session_state.chat_history):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"💬 {chat['title'][:30]}...\n🕐 {chat['timestamp']}", 
                        key=f"chat_{idx}",
                        use_container_width=True
                    ):
                        load_chat_from_history(idx)
                with col2:
                    if st.button("🗑️", key=f"del_{idx}", help="Delete"):
                        st.session_state.chat_history.pop(idx)
                        st.rerun()
    
    st.divider()
    
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("Reading and indexing PDF..."):
            text = load_pdf(uploaded_file)
            st.session_state.pdf_chunks = chunk_text(text)
            st.session_state.pdf_embeddings = embedder.encode(st.session_state.pdf_chunks)
        st.success(f"✅ Indexed {len(st.session_state.pdf_chunks)} chunks!")

    st.divider()
    
    # Stats
    if st.session_state.messages:
        st.markdown("### 📊 Chat Stats")
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Your Messages", len([m for m in st.session_state.messages if m["role"] == "user"]))
        st.metric("AI Responses", len([m for m in st.session_state.messages if m["role"] == "assistant"]))

# ---- CHAT ----
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask me anything..."):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar")
        st.stop()
    
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            groq_client = Groq(api_key=api_key)

            # If a PDF was uploaded, find relevant chunks
            if st.session_state.pdf_chunks and st.session_state.pdf_embeddings is not None:
                query_embedding = embedder.encode([user_input])
                import numpy as np
                scores = np.dot(st.session_state.pdf_embeddings, query_embedding.T).flatten()
                top_indices = scores.argsort()[-3:][::-1]
                relevant_chunks = [st.session_state.pdf_chunks[i] for i in top_indices]
                context = "\n\n".join(relevant_chunks)
                
                rag_prompt = f"""Use the following context to answer the question.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {user_input}"""
                messages_to_send = [{"role": "system", "content": system_prompt}] + \
                                   st.session_state.messages[:-1] + \
                                   [{"role": "user", "content": rag_prompt}]
            else:
                messages_to_send = [{"role": "system", "content": system_prompt}] + \
                                   st.session_state.messages

            stream = groq_client.chat.completions.create(
                model=selected_model,
                messages=messages_to_send,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure your API key is correct")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": full_response})
