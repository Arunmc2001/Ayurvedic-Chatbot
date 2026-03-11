import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os
import random
import json
from datetime import datetime
import base64
from enhanced_model_utils import AyurvedaImageAnalyzer, AyurvedaKnowledgeBase

# Configure Streamlit page
st.set_page_config(
    page_title="AI Ayurveda Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern ChatGPT-like interface
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #2E8B57, #228B22);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 8px 0;
        margin-left: 15%;
        text-align: right;
        box-shadow: 0 2px 5px rgba(0,123,255,0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #e9ecef, #f8f9fa);
        color: #333;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 8px 0;
        margin-right: 15%;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .image-analysis {
        border: 3px dashed #28a745;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 15px 0;
        background: linear-gradient(135deg, #f8fff8, #e8f5e8);
        transition: all 0.3s ease;
    }
    
    .image-analysis:hover {
        border-color: #20c997;
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.2);
    }
    
    .medicine-card {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border-left: 5px solid #ffc107;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(255, 193, 7, 0.2);
    }
    
    .hospital-card {
        background: linear-gradient(135deg, #d1ecf1, #a8dadc);
        border-left: 5px solid #17a2b8;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(23, 162, 184, 0.2);
    }
    
    .quick-symptom-btn {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 25px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(40, 167, 69, 0.3);
    }
    
    .quick-symptom-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(40, 167, 69, 0.4);
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        margin: 10px 0;
        color: #666;
    }
    
    .typing-dots {
        display: inline-flex;
        margin-left: 10px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #28a745;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    .confidence-bar {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #dc3545, #ffc107, #28a745);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize AI components"""
    analyzer = AyurvedaImageAnalyzer()
    knowledge_base = AyurvedaKnowledgeBase()
    return analyzer, knowledge_base

# Enhanced intents with more natural language patterns
enhanced_intents = [
    {
        "tag": "greeting",
        "patterns": [
            "hi", "hello", "namaste", "good morning", "good evening", "hey", 
            "greetings", "howdy", "what's up", "how are you", "start", "begin"
        ],
        "responses": [
            "🙏 Namaste! I'm your AI Ayurveda Assistant. I can analyze symptoms through text or images. How may I help you today?",
            "Hello! Welcome to your personal Ayurvedic health companion. Feel free to describe your symptoms or upload an image for analysis.",
            "Greetings! I'm here to provide personalized Ayurvedic guidance. What health concerns would you like to discuss?"
        ]
    },
    {
        "tag": "help",
        "patterns": [
            "help", "what can you do", "features", "how to use", "guide", "instructions"
        ],
        "responses": [
            "I can help you with:\n• 🔍 AI-powered symptom analysis from images\n• 💬 Text-based health consultations\n• 🌿 Personalized Ayurvedic treatment plans\n• 💊 Medicine recommendations with dosages\n• 🏥 Hospital and clinic suggestions\n\nJust describe your symptoms or upload an image!"
        ]
    },
    {
        "tag": "cold_flu",
        "patterns": [
            "cold", "flu", "runny nose", "sneezing", "congestion", "stuffy nose", 
            "sore throat", "cough", "fever with cold", "seasonal flu"
        ],
        "responses": [
            "For cold and flu symptoms, Ayurveda recommends warming herbs and immunity boosters."
        ],
        "disease": "cold"
    },
    {
        "tag": "headache_migraine",
        "patterns": [
            "headache", "migraine", "head pain", "temple pain", "tension headache",
            "cluster headache", "my head hurts", "head ache", "cranial pain"
        ],
        "responses": [
            "Headaches often indicate Pitta or Vata imbalance. Let me suggest some Ayurvedic remedies."
        ],
        "disease": "headache"
    },
    {
        "tag": "skin_issues",
        "patterns": [
            "acne", "pimples", "skin rash", "rashes", "skin allergy", "itching",
            "skin irritation", "eczema", "dermatitis", "skin problems", "breakouts"
        ],
        "responses": [
            "Skin issues often relate to blood impurities in Ayurveda. Here are some natural treatments."
        ],
        "disease": "pimples"
    },
    {
        "tag": "digestive_issues",
        "patterns": [
            "acidity", "acid reflux", "heartburn", "indigestion", "stomach pain",
            "gastric", "bloating", "gas", "constipation", "diarrhea"
        ],
        "responses": [
            "Digestive issues indicate Agni (digestive fire) imbalance. Let me recommend some Ayurvedic solutions."
        ],
        "disease": "acidity"
    },
    {
        "tag": "general_pain",
        "patterns": [
            "joint pain", "body pain", "muscle pain", "back pain", "knee pain",
            "arthritis", "stiffness", "inflammation", "swelling"
        ],
        "responses": [
            "Pain and inflammation suggest Vata dosha imbalance. Here are some Ayurvedic anti-inflammatory treatments."
        ],
        "disease": "joint_pain"
    }
]

def match_enhanced_intent(user_input):
    """Enhanced intent matching with fuzzy matching"""
    user_input = user_input.lower()
    
    # Direct pattern matching
    for intent in enhanced_intents:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return intent
    
    # Keyword-based matching for symptoms
    symptom_keywords = {
        "cold": ["cold", "cough", "sneez", "runny", "congest"],
        "headache": ["head", "migrain", "temple", "cranial"],
        "skin": ["skin", "rash", "acne", "pimple", "itch", "allerg"],
        "digestive": ["stomach", "acid", "digest", "gas", "bloat"],
        "pain": ["pain", "ache", "hurt", "sore", "stiff"]
    }
    
    for category, keywords in symptom_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            for intent in enhanced_intents:
                if intent.get("disease") and category in intent["disease"]:
                    return intent
    
    return None

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    if 'typing' not in st.session_state:
        st.session_state.typing = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []

def add_to_chat_history(message, sender, metadata=None):
    """Add message to chat history with metadata"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        'message': message,
        'sender': sender,
        'timestamp': timestamp,
        'metadata': metadata or {}
    })

def display_confidence_bar(confidence):
    """Display confidence level as a visual bar"""
    confidence_percent = confidence * 100
    color = "#dc3545" if confidence < 0.5 else "#ffc107" if confidence < 0.8 else "#28a745"
    
    return f"""
    <div class="confidence-bar">
        <div class="confidence-fill" style="width: {confidence_percent}%; background-color: {color};">
        </div>
    </div>
    <small>Confidence: {confidence_percent:.1f}%</small>
    """

def display_chat_history():
    """Display enhanced chat history"""
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for i, chat in enumerate(st.session_state.chat_history):
            if chat['sender'] == 'user':
                st.markdown(
                    f'<div class="user-message">'
                    f'{chat["message"]} '
                    f'<br><small style="opacity: 0.8;">You • {chat["timestamp"]}</small>'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="bot-message">'
                    f'{chat["message"]} '
                    f'<br><small style="opacity: 0.8;">AI Assistant • {chat["timestamp"]}</small>'
                    f'</div>', 
                    unsafe_allow_html=True
                )
        
        # Show typing indicator if AI is processing
        if st.session_state.typing:
            st.markdown(
                '<div class="typing-indicator">'
                'AI is analyzing...'
                '<div class="typing-dots">'
                '<span></span><span></span><span></span>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

def process_text_input(user_input, knowledge_base):
    """Process text input and generate response"""
    matched_intent = match_enhanced_intent(user_input)
    
    if matched_intent:
        if matched_intent["tag"] in ["greeting", "help"]:
            return random.choice(matched_intent["responses"])
        elif "disease" in matched_intent:
            disease = matched_intent["disease"]
            response = random.choice(matched_intent["responses"])
            treatment_plan = knowledge_base.format_treatment_response(disease)
            return f"{response}\n\n{treatment_plan}"
    
    # Fallback response with suggestions
    return """I understand you have health concerns. For the best analysis, you can:

🔍 **Upload an image** of the affected area for AI-powered analysis
💬 **Describe specific symptoms** like "I have a headache" or "skin rash on my arm"
🚀 **Use quick symptom buttons** below for common conditions

I'm trained to help with conditions like headaches, skin problems, digestive issues, cold/flu, and joint pain."""

def main():
    # Initialize components
    analyzer, knowledge_base = initialize_components()
    initialize_session_state()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-header">🌿 AI Ayurveda Assistant</h1>', unsafe_allow_html=True)
    
    # Subtitle with features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🔍 AI Image Analysis**")
    with col2:
        st.markdown("**💬 Smart Conversations**")
    with col3:
        st.markdown("**🌿 Personalized Ayurveda**")
    
    st.markdown("---")
    
    # Sidebar with enhanced features
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Statistics
        if st.session_state.chat_history:
            st.metric("💬 Messages", len(st.session_state.chat_history))
            st.metric("🔍 Analyses", len(st.session_state.analysis_results))
        
        st.markdown("### 🔧 Features")
        st.markdown("""
        • **AI Image Recognition** - Upload photos for instant analysis
        • **Natural Conversations** - Chat naturally about symptoms  
        • **Comprehensive Plans** - Get detailed treatment protocols
        • **Medicine Guidance** - Dosages, timings, and precautions
        • **Hospital Directory** - Find nearby Ayurvedic centers
        """)
        
        st.markdown("### 📋 Quick Actions")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.analysis_results = []
            st.rerun()
        
        if st.button("📊 View Analytics", use_container_width=True):
            if st.session_state.analysis_results:
                st.write("Recent Analyses:")
                for result in st.session_state.analysis_results[-3:]:
                    st.write(f"• {result['disease']} ({result['confidence']:.1%})")
        
        if st.session_state.chat_history:
            chat_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="📥 Download Chat",
                data=chat_data,
                file_name=f"ayurveda_consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    # Main interface with two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("💬 Intelligent Chat Interface")
        
        # Display chat history
        display_chat_history()
        
        # Chat input with enhanced UX
        user_input = st.text_input(
            "💭 Share your health concerns:",
            placeholder="e.g., 'I have a persistent headache and feel nauseous' or 'Upload image for analysis'",
            key="chat_input"
        )
        
        col_send, col_clear = st.columns([4, 1])
        
        with col_send:
            send_clicked = st.button("📤 Send Message", use_container_width=True, type="primary")
        
        with col_clear:
            if st.button("🔄", help="Clear input"):
                st.session_state.chat_input = ""
                st.rerun()
        
        if send_clicked and user_input:
            # Add user message
            add_to_chat_history(user_input, 'user')
            
            # Show typing indicator
            st.session_state.typing = True
            st.rerun()
            
            # Process input
            response = process_text_input(user_input, knowledge_base)
            add_to_chat_history(response, 'bot')
            
            # Clear typing indicator
            st.session_state.typing = False
            st.rerun()
    
    with col2:
        st.subheader("📸 AI Image Analysis")
        
        # Enhanced image upload area
        st.markdown('<div class="image-analysis">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "🖼️ Upload Medical Image",
            type=["jpg", "jpeg", "png", "bmp"],
            help="Upload a clear image of symptoms for AI analysis"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Image", use_column_width=True)
            
            # Analysis button
            if st.button("🔍 Analyze with AI", use_container_width=True, type="primary"):
                with st.spinner("🤖 AI is analyzing your image..."):
                    # Get top predictions
                    top_predictions = analyzer.get_top_predictions(image, top_k=3)
                    
                    if top_predictions:
                        st.success("✅ Analysis Complete!")
                        
                        # Display results
                        for i, (disease, confidence) in enumerate(top_predictions):
                            if i == 0:  # Primary prediction
                                st.markdown(f"### 🎯 Primary Detection: {disease.replace('_', ' ').title()}")
                                st.markdown(display_confidence_bar(confidence), unsafe_allow_html=True)
                                
                                # Get treatment plan
                                treatment_response = knowledge_base.format_treatment_response(disease, confidence)
                                
                                # Add to chat history
                                analysis_message = f"📸 **Image Analysis Result:**\n\n{treatment_response}"
                                add_to_chat_history(analysis_message, 'bot', {'type': 'image_analysis', 'disease': disease, 'confidence': confidence})
                                
                                # Store analysis result
                                st.session_state.analysis_results.append({
                                    'disease': disease,
                                    'confidence': confidence,
                                    'timestamp': datetime.now()
                                })
                                
                                # Display treatment in card
                                st.markdown('<div class="medicine-card">', unsafe_allow_html=True)
                                st.markdown(treatment_response)
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            else:  # Alternative predictions
                                st.markdown(f"**Alternative {i}:** {disease.replace('_', ' ').title()} ({confidence:.1%})")
                    
                    else:
                        st.error("❌ Unable to analyze image. Please try a clearer photo.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick symptom selection
        st.markdown("### 🚀 Quick Symptom Selection")
        
        quick_symptoms = [
            ("🤕", "Headache"), ("🤧", "Cold/Flu"), ("🔥", "Fever"),
            ("🍽️", "Acidity"), ("🦵", "Joint Pain"), ("😷", "Skin Rash")
        ]
        
        cols = st.columns(2)
        for i, (emoji, symptom) in enumerate(quick_symptoms):
            with cols[i % 2]:
                if st.button(f"{emoji} {symptom}", key=f"quick_{symptom}", use_container_width=True):
                    # Process quick symptom
                    quick_input = f"I have {symptom.lower()}"
                    add_to_chat_history(quick_input, 'user')
                    
                    response = process_text_input(quick_input, knowledge_base)
                    add_to_chat_history(response, 'bot')
                    
                    st.rerun()
    
    # Enhanced footer
    st.markdown("---")
    
    # Emergency notice
    st.error("""
    🚨 **Emergency Notice**: This AI assistant provides general Ayurvedic guidance only. 
    For serious symptoms, severe pain, or emergency conditions, please consult qualified healthcare professionals immediately.
    """)
    
    # Additional info
    with st.expander("ℹ️ About This AI Assistant"):
        st.markdown("""
        **AI Ayurveda Assistant** combines modern AI technology with traditional Ayurvedic wisdom:
        
        - **Image Recognition**: Advanced deep learning models trained on medical imagery
        - **Natural Language Processing**: Understands symptoms described in natural language
        - **Ayurvedic Database**: Comprehensive knowledge of traditional treatments and medicines
        - **Personalized Recommendations**: Tailored advice based on individual symptoms
        
        **Accuracy Note**: AI predictions are based on visual patterns and may not be 100% accurate. 
        Always verify with qualified practitioners.
        """)

if __name__ == "__main__":
    main()
