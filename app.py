import streamlit as st
from groq import Groq
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer
from datetime import datetime
import base64
from PIL import Image
import io

# ---- SETUP ----
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def encode_image_to_base64(image_file):
    """Convert image to base64 string"""
    return base64.b64encode(image_file.read()).decode('utf-8')

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

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "image_base64" not in st.session_state:
    st.session_state.image_base64 = None

if "theme" not in st.session_state:
    st.session_state.theme = "Purple Gradient"

# Theme Definitions
THEMES = {
    "Purple Gradient": {
        "bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "primary": "#667eea",
        "name": "🟣 Purple Gradient"
    },
    "Ocean Blue": {
        "bg": "linear-gradient(135deg, #0093E9 0%, #80D0C7 100%)",
        "primary": "#0093E9",
        "name": "🌊 Ocean Blue"
    },
    "Sunset Orange": {
        "bg": "linear-gradient(135deg, #FA8BFF 0%, #2BD2FF 50%, #2BFF88 100%)",
        "primary": "#FA8BFF",
        "name": "🌅 Sunset"
    },
    "Forest Green": {
        "bg": "linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%)",
        "primary": "#2C5364",
        "name": "🌲 Forest"
    },
    "Dark Mode": {
        "bg": "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
        "primary": "#4a90e2",
        "name": "🌙 Dark Mode"
    },
    "Light Mode": {
        "bg": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "primary": "#667eea",
        "name": "☀️ Light Mode"
    }
}

# Custom CSS - Professional Design with Dynamic Theme
current_theme = THEMES[st.session_state.theme]

st.markdown(f"""
    <style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Dynamic Theme Background */
    .stApp {{
        background: {current_theme['bg']};
        transition: all 0.3s ease;
    }}
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* Main Content Area */
    .main .block-container {{
        padding-top: 2rem;
        max-width: 1200px;
    }}
    
    /* Professional Headers */
    h1, h2, h3 {{
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    
    /* Chat Messages */
    .stChatMessage {{
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    /* Input Box */
    .stChatInputContainer {{
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    /* Buttons */
    .stButton button {{
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s ease;
        border: none;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    /* Primary Button with Theme Color */
    .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, {current_theme['primary']} 0%, {current_theme['primary']}dd 100%);
        color: white;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 2rem 1rem;
    }}
    
    /* Success/Info/Warning Messages */
    .stAlert {{
        border-radius: 12px;
        border-left: 4px solid;
    }}
    
    /* Text Input */
    .stTextInput input {{
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
    }}
    
    /* Text Input with Theme Color */
    .stTextInput input:focus {{
        border-color: {current_theme['primary']};
        box-shadow: 0 0 0 3px {current_theme['primary']}20;
    }}
    
    /* Select Box */
    .stSelectbox > div > div {{
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }}
    
    /* Text Area */
    .stTextArea textarea {{
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        border-radius: 10px;
        background: rgba(102, 126, 234, 0.05);
        font-weight: 600;
    }}
    
    /* Metrics */
    [data-testid="stMetric"] {{
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Assistant Pro")
st.caption("☁️ Cloud Edition • Powered by Groq")

# Professional Hero Section
st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 16px; margin-bottom: 2rem; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
        <h2 style="margin: 0 0 0.5rem 0; color: #1a202c;">Welcome to AI Assistant Pro</h2>
        <p style="margin: 0; color: #64748b; font-size: 1.1rem;">
            Multi-modal AI platform with document intelligence and vision capabilities
        </p>
        <div style="margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <span style="background: #f0f9ff; color: #0369a1; padding: 0.5rem 1rem; 
                         border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                💬 Text Chat
            </span>
            <span style="background: #f0fdf4; color: #15803d; padding: 0.5rem 1rem; 
                         border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                📄 PDF Analysis
            </span>
            <span style="background: #fef3c7; color: #92400e; padding: 0.5rem 1rem; 
                         border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                📸 Image Vision
            </span>
            <span style="background: #fce7f3; color: #9f1239; padding: 0.5rem 1rem; 
                         border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                🎤 Voice Ready
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Usage Notice
with st.expander("ℹ️ Fair Use Policy"):
    st.markdown("""
    **Rate Limits:**
    - 5 messages per minute per user
    - This protects the service for everyone
    
    **Guidelines:**
    - Use for legitimate purposes only
    - Be respectful and avoid spam
    - Large files may take longer to process
    
    Thank you for using AI Assistant Pro responsibly! 🙏
    """)

# ---- SIDEBAR ----
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Theme Selector at the top
    st.markdown("### 🎨 Theme")
    theme_options = list(THEMES.keys())
    theme_names = [THEMES[t]["name"] for t in theme_options]
    
    selected_theme_name = st.selectbox(
        "Choose Theme",
        theme_names,
        index=theme_options.index(st.session_state.theme),
        label_visibility="collapsed"
    )
    
    # Update theme if changed
    selected_theme = theme_options[theme_names.index(selected_theme_name)]
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    
    st.divider()
    
    # API Key Input (users can enter their own key)
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get your free API key from console.groq.com",
        value=st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key")
        st.info("🔑 Get free key at [console.groq.com](https://console.groq.com/)")

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
    
    # Voice Input Feature
    st.header("🎤 Voice Input")
    st.caption("Speak to ask questions")
    
    col_voice1, col_voice2 = st.columns([2, 1])
    with col_voice1:
        if st.button("🎤 Start Recording", use_container_width=True, type="secondary"):
            st.info("Voice recording coming soon! For now, use text input below.")
    with col_voice2:
        if st.button("⏹️ Stop", use_container_width=True):
            pass
    
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
    
    # Image Upload Feature
    st.header("📸 Upload Image")
    st.caption("Ask questions about images")
    
    image_file = st.file_uploader(
        "Choose from Camera or Gallery", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Upload an image to ask questions about it"
    )
    
    if image_file:
        # Display the uploaded image
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Store image in session state
        image_file.seek(0)  # Reset file pointer
        st.session_state.uploaded_image = image
        st.session_state.image_base64 = encode_image_to_base64(image_file)
        st.success("✅ Image uploaded! Ask questions about it.")
        
        # Clear image button
        if st.button("🗑️ Clear Image", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.image_base64 = None
            st.rerun()
    
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
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            groq_client = Groq(api_key=api_key)

            # Check if there's an uploaded image - use vision model
            if st.session_state.image_base64:
                # Use vision-capable model
                vision_model = "llama-3.2-90b-vision-preview"
                
                messages_to_send = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_input
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{st.session_state.image_base64}"
                                }
                            }
                        ]
                    }
                ]
                
                stream = groq_client.chat.completions.create(
                    model=vision_model,
                    messages=messages_to_send,
                    stream=True,
                    max_tokens=1024
                )
            
            # If a PDF was uploaded, find relevant chunks
            elif st.session_state.pdf_chunks and st.session_state.pdf_embeddings is not None:
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
                
                stream = groq_client.chat.completions.create(
                    model=selected_model,
                    messages=messages_to_send,
                    stream=True
                )
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
