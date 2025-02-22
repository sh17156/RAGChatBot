# Dr. Hafeez's AI Assistant - Professional RAG Chatbot

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.0-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0.2-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

</div>

A professional RAG-based AI assistant specializing in Dr. Salman Hafeez's expertise in Embedded Software for Controls and Robotics Systems. Built with LangChain and Flask, featuring multi-model support and a professional web interface.

## 🚀 Features

### Document Processing
- Support for multiple formats (PDF, DOCX, TXT, XLSX)
- Intelligent text chunking and embedding generation
- Local FAISS vector store for efficient retrieval

### LLM Integration
- OpenAI GPT Models (default: gpt-3.5-turbo)
- DeepSeek Models
- Claude Models
- Easy provider switching

### Professional Interface
- Clean, responsive design
- Real-time chat interactions
- Professional styling and animations
- Loading states and error handling

## 🛠️ Local Development Setup

1. Clone the repository and create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```bash
OPENAI_API_KEY="your-openai-key"
DEEPSEEK_API_KEY="your-deepseek-key"
ANTHROPIC_API_KEY="your-anthropic-key"
```

4. Create required directories:
```bash
mkdir -p data/documents data/vector_store
```

5. Add documents to `data/documents/`

6. Run the application:
```bash
python wsgi.py
```

## 🌐 Deployment on Render

1. Prepare Your Repository:
   - Push your code to GitHub
   - Make sure you have `render.yaml` in your root directory:
   ```yaml
   services:
     - type: web
       name: dr-hafeez-ai-assistant
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn wsgi:app
       envVars:
         - key: PYTHON_VERSION
           value: 3.9.0
   ```

2. Deploy on Render:
   - Sign up at render.com
   - Click "New Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Render will automatically detect the configuration
   - Add your environment variables:
     - OPENAI_API_KEY
     - DEEPSEEK_API_KEY
     - ANTHROPIC_API_KEY
   - Click "Create Web Service"

3. Your app will be available at: `https://dr-hafeez-ai-assistant.onrender.com`

## 🔧 Troubleshooting

1. **Document Processing Issues**
   - Verify document formats are supported
   - Check file permissions
   - Ensure documents are in data/documents/

2. **API Connection**
   - Verify API keys in environment variables
   - Check API service status
   - Monitor rate limits

3. **Web Interface**
   - Clear browser cache
   - Check browser console for errors
   - Verify server logs in Render dashboard

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [Render Documentation](https://render.com/docs)

---
<div align="center">
Developed for Dr. Salman Hafeez's Professional Knowledge Base
</div>
