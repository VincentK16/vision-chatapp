import streamlit as st
from urllib.request import urlopen, Request
from urllib.parse import urlparse
import base64
import mimetypes

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Get configuration settings from Streamlit secrets
def get_config():
    project_endpoint = st.secrets.get("PROJECT_CONNECTION", "")
    model_deployment = st.secrets.get("MODEL_DEPLOYMENT", "")
    return project_endpoint, model_deployment

# Main app
st.title("🖼️ Azure Vision Chat App")
st.markdown("Upload an image URL and ask questions about it!")

# Sidebar with instructions
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Enter an image URL** in the text input below
    2. **Preview the image** to make sure it loaded correctly
    3. **Ask a question** about the image
    4. **Click "Ask AI"** to get an AI-powered response
    
    **Supported formats:** JPG, PNG, GIF, WebP
    
    **Tips:**
    - Use direct image URLs (ending in .jpg, .png, etc.)
    - Make sure the image is publicly accessible
    - Try the sample images for quick testing
    """)
    
    st.markdown("---")
    st.markdown("**🔗 Quick Image Sources:**")
    st.markdown("- [Unsplash](https://unsplash.com)")
    st.markdown("- [Pexels](https://pexels.com)")
    st.markdown("- [GitHub raw images](https://github.com)")

# Image URL input
default_image_url = "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/gen-ai-vision/orange.jpeg"

# Initialize session state for image URL
if 'image_url' not in st.session_state:
    st.session_state.image_url = default_image_url

# Check if a sample URL was selected
if 'sample_url' in st.session_state:
    st.session_state.image_url = st.session_state.sample_url
    del st.session_state.sample_url

image_url = st.text_input("Enter image URL:", 
                         value=st.session_state.image_url,
                         key="url_input",
                         placeholder="https://example.com/image.jpg")

# Update session state when URL changes
if image_url != st.session_state.image_url:
    st.session_state.image_url = image_url

# Display the image if URL is provided
current_image_url = None
if image_url:
    try:
        st.image(image_url, caption="Your Image", width=400)
        current_image_url = image_url
        st.success("✅ Image loaded successfully!")
    except Exception as e:
        st.error(f"❌ Could not load image: {str(e)}")
        st.info("Please check the URL and make sure it's a valid image link.")

st.markdown("---")

# Question suggestion buttons
st.markdown("**💡 Quick Questions - Click to use:**")
col1, col2, col3 = st.columns(3)

# Initialize session state for the question
if 'selected_question' not in st.session_state:
    st.session_state.selected_question = ""

with col1:
    if st.button("🔍 What do you see?", use_container_width=True):
        st.session_state.selected_question = "What do you see in this image?"
        st.rerun()
    
    if st.button("🎨 Describe colors", use_container_width=True):
        st.session_state.selected_question = "Describe the colors and composition of this image"
        st.rerun()

with col2:
    if st.button("📝 Detailed description", use_container_width=True):
        st.session_state.selected_question = "Please provide a detailed description of everything you can see in this image"
        st.rerun()
    
    if st.button("🌟 What stands out?", use_container_width=True):
        st.session_state.selected_question = "What are the most interesting or notable details in this image?"
        st.rerun()

with col3:
    if st.button("😊 Mood & atmosphere", use_container_width=True):
        st.session_state.selected_question = "What's the mood or atmosphere of this image?"
        st.rerun()
    
    if st.button("🏷️ Identify objects", use_container_width=True):
        st.session_state.selected_question = "Can you identify and list all the objects or subjects in this image?"
        st.rerun()

# Text input for questions - will be populated by button clicks
user_question = st.text_input("Enter your question about the image:", 
                             value=st.session_state.selected_question,
                             placeholder="What can you tell me about this image?")

# Update session state when user types manually
if user_question != st.session_state.selected_question:
    st.session_state.selected_question = user_question

# Button to submit
if st.button("Ask AI", type="primary"):
    if user_question and current_image_url:
        with st.spinner("Getting AI response..."):
            try:
                # Get config
                project_endpoint, model_deployment = get_config()
                
                # Initialize the project client
                project_client = AIProjectClient(            
                    credential=DefaultAzureCredential(
                        exclude_environment_credential=True,
                        exclude_managed_identity_credential=True
                    ),
                    endpoint=project_endpoint,
                )

                # Get a chat client
                openai_client = project_client.inference.get_azure_openai_client(api_version="2024-10-21")

                # Prepare image data with improved format detection
                request = Request(current_image_url, headers={"User-Agent": "Mozilla/5.0"})
                image_response = urlopen(request)
                image_data = base64.b64encode(image_response.read()).decode("utf-8")
                
                # Detect image format
                content_type = image_response.headers.get('content-type', '')
                if content_type.startswith('image/'):
                    mime_type = content_type
                else:
                    # Fallback to URL-based detection
                    parsed_url = urlparse(current_image_url)
                    path = parsed_url.path.lower()
                    if path.endswith(('.jpg', '.jpeg')):
                        mime_type = 'image/jpeg'
                    elif path.endswith('.png'):
                        mime_type = 'image/png'
                    elif path.endswith('.gif'):
                        mime_type = 'image/gif'
                    elif path.endswith('.webp'):
                        mime_type = 'image/webp'
                    else:
                        mime_type = 'image/jpeg'  # Default fallback
                
                data_url = f"data:{mime_type};base64,{image_data}"

                # Get AI response
                response = openai_client.chat.completions.create(
                    model=model_deployment,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant that analyzes images and provides detailed, helpful responses about what you see."},
                        {"role": "user", "content": [  
                            {"type": "text", "text": user_question},
                            {"type": "image_url", "image_url": {"url": data_url}}
                        ]} 
                    ]
                )
                
                # Display response
                st.success("AI Response:")
                st.write(response.choices[0].message.content)
                
            except Exception as ex:
                st.error(f"Error: {str(ex)}")
    elif not user_question:
        st.warning("Please enter a question first!")
    elif not current_image_url:
        st.warning("Please provide a valid image URL first!")

# Add some example questions and sample images
st.markdown("---")

# Sample image URLs
st.markdown("**Try these sample images:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍊 Orange"):
        st.session_state.sample_url = "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/gen-ai-vision/orange.jpeg"
        st.rerun()

with col2:
    if st.button("🏞️ Landscape"):
        st.session_state.sample_url = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        st.rerun()

with col3:
    if st.button("🐱 Cat"):
        st.session_state.sample_url = "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400"
        st.rerun()

# No need for the sample URL display message anymore since it auto-populates

st.markdown("**🎯 Pro Tips:**")
st.info("💡 Use the question buttons above for quick suggestions, or type your own custom questions!")

# Show connection status
with st.expander("Connection Info"):
    project_endpoint, model_deployment = get_config()
    st.write(f"**Endpoint:** {project_endpoint}")
    st.write(f"**Model:** {model_deployment}")
