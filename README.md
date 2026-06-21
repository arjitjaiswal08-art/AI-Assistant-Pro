# 🤖 AI Assistant Pro

A professional, enterprise-grade AI chatbot with document intelligence capabilities.

![Made by Arjit Jaiswal](https://img.shields.io/badge/Made%20by-Arjit%20Jaiswal-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)

## ✨ Features

- 💬 **Intelligent Chat** - Powered by Groq's fast AI models
- 📄 **Document Intelligence** - Upload PDFs and ask questions about them (RAG)
- 📜 **Chat History** - Save and restore previous conversations
- 🎨 **Professional UI** - Clean, modern interface
- 🔒 **Privacy Options** - Local (Ollama) or Cloud (Groq) deployment
- ⚡ **Real-time Streaming** - See responses as they're generated

## 🚀 Quick Start

### Local Setup (with Ollama)

```bash
# Install Ollama
brew install ollama

# Start Ollama and download a model
ollama serve
ollama pull llama3.2

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Cloud Deployment (with Groq)

See [DEPLOY_STEPS.md](DEPLOY_STEPS.md) for detailed instructions.

Quick version:
1. Get Groq API key from [console.groq.com](https://console.groq.com/)
2. Use `app_cloud.py` as your main file
3. Deploy to [Streamlit Cloud](https://share.streamlit.io/)

## 📋 Requirements

- Python 3.10+
- Streamlit
- Ollama (for local) or Groq API key (for cloud)
- PyMuPDF
- Sentence Transformers
- ChromaDB (local) or NumPy (cloud)

## 🎯 Use Cases

- **Research Assistant** - Upload research papers and ask questions
- **Document Analysis** - Analyze contracts, reports, or any PDF
- **General AI Chat** - Get help with coding, writing, or any task
- **Learning Tool** - Ask questions and get detailed explanations

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **AI Models:** 
  - Local: Ollama (Llama, Mistral, etc.)
  - Cloud: Groq (Llama 3.3, Mixtral)
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB (local) or In-memory (cloud)
- **PDF Processing:** PyMuPDF

## 📂 Project Structure

```
ai-assistant-pro/
├── app.py                    # Main app (Ollama/local)
├── app_cloud.py              # Cloud-ready version (Groq)
├── app_online.py             # Advanced cloud version
├── requirements.txt          # Python dependencies
├── requirements_cloud.txt    # Cloud dependencies
├── DEPLOY_STEPS.md          # Deployment guide
├── DEPLOYMENT_CHECKLIST.md  # Deployment checklist
└── README.md                # This file
```

## 🎨 Screenshots

[Add screenshots here]

## 🔐 Environment Variables

For cloud deployment, add these secrets:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

## 📝 License

MIT License - feel free to use this project however you like!

## 👨‍💻 Author

**Arjit Jaiswal**

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show Your Support

Give a ⭐️ if you like this project!

## 📞 Support

Need help? Open an issue or contact me.

---

**Made with ❤️ by Arjit Jaiswal**
# AI-Assistant-Pro
