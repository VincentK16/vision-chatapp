# 🖼️ Azure Vision Chat App

A powerful Streamlit web application that enables interactive conversations about images using Azure AI/OpenAI vision models. Upload any image URL and ask questions to get detailed AI-powered analysis and insights.

## ✨ Features

### 🔍 **Image Analysis**
- **Dynamic Image Input**: Load any publicly accessible image via URL
- **Real-time Preview**: Instant image validation and display
- **Multi-format Support**: JPG, PNG, GIF, WebP images
- **Smart Format Detection**: Automatic MIME type detection for accurate image encoding

### 💬 **Interactive Chat Interface**
- **One-Click Question Buttons**: Pre-built suggestion buttons for common queries
- **Custom Question Input**: Type your own questions about the image
- **AI-Powered Responses**: Detailed analysis using Azure OpenAI/Foundry models
- **Session State Management**: Questions and URLs persist across interactions
- **Error Handling**: Graceful error messages and user validation

### 🎯 **Quick Question Categories**
- 🔍 **General Analysis** - "What do you see in this image?"
- 📝 **Detailed Description** - Comprehensive image overview
- 🎨 **Colors & Composition** - Visual design and color analysis
- 🌟 **Notable Features** - Interesting details and highlights
- 😊 **Mood & Atmosphere** - Emotional tone and atmosphere assessment
- 🏷️ **Object Identification** - Recognition and listing of subjects

### 🖼️ **Sample Images**
Quick-start with pre-configured sample images:
- 🍊 **Orange** - Food/object analysis demo
- 🏞️ **Landscape** - Nature scene photography
- 🐱 **Cat** - Animal photography example

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure AI/OpenAI account with vision model access
- Streamlit

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd gen-ai-vision/python
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit azure-identity azure-ai-projects
   ```

3. **Configure secrets** - Create `.streamlit/secrets.toml`
   ```toml
   MODEL_DEPLOYMENT = "Phi-4-multimodal-instruct"
   PROJECT_CONNECTION = "https://your-endpoint.services.ai.azure.com/models"
   ```

4. **Run the application**
   ```bash
   streamlit run chat-app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📋 Configuration

### Required Secrets

Configure these values in `.streamlit/secrets.toml`:

| Key | Description | Example |
|-----|-------------|---------|
| `MODEL_DEPLOYMENT` | Azure AI model deployment name | `"Phi-4-multimodal-instruct"` |
| `PROJECT_CONNECTION` | Azure AI Project endpoint URL | `"https://your-endpoint.services.ai.azure.com/models"` |

### Azure Setup

1. **Create an Azure AI resource** or use existing Azure OpenAI
2. **Deploy a vision-capable model**
   - GPT-4 Vision
   - GPT-4o
   - Phi-4 multimodal
   - Claude 3 Vision (via Foundry)
3. **Obtain credentials**
   - Get endpoint URL from Azure portal
   - Get model deployment name
4. **Configure authentication**
   - Use Azure CLI: `az login`
   - Or configure managed identity
   - DefaultAzureCredential handles the rest

## 🎮 How to Use

### Basic Workflow
1. **Enter an Image URL** - Paste any publicly accessible image URL
2. **Preview the Image** - Verify it loads correctly in the app
3. **Choose a Question** - Click a suggestion button or type your own
4. **Get AI Response** - Click "Ask AI" for detailed analysis

### Example Use Cases

**Object Recognition**
- "What objects are in this image?"
- "Can you identify and list all the items?"

**Scene Analysis**
- "Describe the colors and composition"
- "What's the mood or atmosphere?"

**Detailed Descriptions**
- "Please provide a detailed description of everything you see"
- "What are the most interesting details?"

**Technical Analysis**
- "What's the lighting setup?"
- "What's the background and foreground?"

## 🔧 Project Structure

```
├── chat-app.py                 # Main Azure Vision Chat application
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml           # Configuration secrets (git ignored)
└── README.md                  # This file
```

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web application
- **Backend**: Azure AI Project Client
- **AI Model**: Azure OpenAI/Foundry vision models
- **Authentication**: Azure DefaultAzureCredential

### Image Processing
- URLs are fetched and base64 encoded
- Smart MIME type detection from HTTP headers or file extension
- Support for multiple image formats
- Automatic format fallback to JPEG if detection fails

### Key Technologies
- **Streamlit** (1.28+) - Web application framework
- **Azure Identity** - Azure authentication
- **Azure AI Projects** - Azure AI client library
- **Python 3.8+** - Programming language

## 🔒 Security Considerations

- **Secrets Management**: Never commit `secrets.toml` to version control (included in `.gitignore`)
- **Image URLs**: Only use publicly accessible images
- **Azure Authentication**: Uses DefaultAzureCredential for secure access
- **Rate Limits**: Monitor Azure API usage and quota limits
- **API Versioning**: Uses API version `2024-10-21` for compatibility

## 🐛 Troubleshooting

### Common Issues

**"Image won't load"**
- Verify URL is publicly accessible
- Check image format (JPG, PNG, GIF, WebP)
- Ensure URL points directly to image file
- Try a different image source

**"AI responses fail"**
- Check Azure endpoint configuration in `secrets.toml`
- Verify model deployment name matches your deployment
- Confirm Azure authentication is working (`az login`)
- Check Azure subscription quota/limits
- Review Azure Portal for service status

**"Streamlit errors"**
- Ensure all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+): `python --version`
- Verify `secrets.toml` location: `.streamlit/secrets.toml`
- Check `.streamlit/config.toml` for deprecated options

**"Deprecation warnings"**
- Update your `.streamlit/config.toml` to remove deprecated options
- Ensure Streamlit is up to date: `pip install --upgrade streamlit`

### Debug Mode

Add verbose logging (optional):
```toml
# .streamlit/secrets.toml
debug = true
```

## 📚 Resources

- **[Streamlit Documentation](https://docs.streamlit.io/)**
- **[Azure AI Services](https://learn.microsoft.com/azure/ai-services/)**
- **[Azure OpenAI Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)**
- **[Azure AI Projects](https://learn.microsoft.com/azure/ai-studio/)**
- **[Unsplash](https://unsplash.com)** - Free stock photos
- **[Pexels](https://pexels.com)** - Free stock images

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Add more sample questions
- Improve documentation

## 📄 License

This project is provided for educational and demonstration purposes under the Microsoft Learn curriculum.

## 👤 Author

Created as part of the **Microsoft Learn AI-102 Certification Training**

---

## 📦 Installation Summary

```bash
# Clone the repository
git clone <repository-url>
cd gen-ai-vision/python

# Create virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install streamlit azure-identity azure-ai-projects

# Configure Azure credentials
az login

# Create .streamlit/secrets.toml with your Azure details

# Run the app
streamlit run chat-app.py
```

## 🚀 Deployment

### Run Locally
```bash
streamlit run chat-app.py
```

### Deploy to Streamlit Cloud
1. Push to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in Streamlit Cloud dashboard
4. Deploy!

### Deploy to Azure
Consider deploying to:
- **Azure Container Instances** (ACI)
- **Azure App Service**
- **Azure Kubernetes Service** (AKS)

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Compatibility**: Python 3.8+, Streamlit 1.28+

Made with ❤️ using **Streamlit** and **Azure AI** 🚀
