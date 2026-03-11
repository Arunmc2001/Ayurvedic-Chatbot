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

# Configure Streamlit page
st.set_page_config(
    page_title="AI Ayurveda Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like interface
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        margin-right: 20%;
    }
    
    .image-analysis {
        border: 2px dashed #28a745;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .medicine-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .hospital-card {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("ayurvedic_symptom_model.h5")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Disease classes (update based on your model's training)
DISEASE_CLASSES = [
    'Allergy', 'Headache', 'Pimples', 'Skin_Rashes', 'Cold', 'Fever', 
    'Cough', 'Acidity', 'Indigestion', 'Joint_Pain'
]

# Comprehensive Ayurvedic knowledge base
def load_ayurvedic_data():
    return {
        'allergy': {
            'medicines': ['Neem Capsules - Morning', 'Turmeric Water - Night', 'Haridra Khanda - After Meals'],
            'duration': '2-3 weeks',
            'advice': 'Avoid allergens, maintain clean environment, practice pranayama'
        },
        'headache': {
            'medicines': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep', 'Brahmi Oil - Night'],
            'duration': 'As needed or 3-5 days if frequent',
            'advice': 'Stay hydrated, practice meditation, avoid stress'
        },
        'pimples': {
            'medicines': ['Turmeric Paste - Evening', 'Neem Capsules - Morning', 'Manjistha - Night'],
            'duration': '4-6 weeks',
            'advice': 'Maintain facial hygiene, avoid oily foods, drink plenty of water'
        },
        'skin_rashes': {
            'medicines': ['Neem Paste - Morning', 'Aloe Vera Gel - Night', 'Sariva - After Meals'],
            'duration': '2-4 weeks',
            'advice': 'Keep affected area clean and dry, wear loose cotton clothes'
        },
        'cold': {
            'medicines': ['Tulsi Tea - Morning & Evening', 'Chyawanprash - Before Bed', 'Ginger Honey - As needed'],
            'duration': '5-7 days',
            'advice': 'Rest well, stay warm, inhale steam with eucalyptus oil'
        }
    }

# Comprehensive intents database
intents = [
    {
        "tag": "greeting",
        "patterns": ["hi", "hello", "namaste", "good morning", "good evening", "hey"],
        "responses": [
            "Namaste! 🙏 I'm your AI Ayurveda Assistant. How can I help you today?",
            "Hello! Welcome to your personal Ayurvedic health companion. What brings you here?",
            "Greetings! I'm here to provide Ayurvedic guidance. Please share your concerns."
        ]
    },
    {
        "tag": "cold",
        "patterns": ["I have a cold", "cold symptoms", "runny nose", "sneezing"],
        "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."],
        "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed", "Ginger Honey - As needed"],
        "duration": "5-7 days",
        "hospitals": [
            {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
            {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}
        ]
    },
    {
        "tag": "headache",
        "patterns": ["headache", "my head hurts", "migraine", "head pain"],
        "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."],
        "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep", "Peppermint Oil - As needed"],
        "duration": "As needed or 3-5 days if frequent",
        "hospitals": [
            {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
            {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}
        ]
    },
    {
        "tag": "fever",
        "patterns": ["fever", "high temperature", "body heat"],
        "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."],
        "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night", "Tulsi Tea - 3 times daily"],
        "duration": "3-5 days",
        "hospitals": [
            {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
            {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}
        ]
    },
    {
        "tag": "acidity",
        "patterns": ["acidity", "acid reflux", "heartburn", "stomach burn"],
        "responses": ["Amla juice and jeera water can help to reduce acidity."],
        "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals", "Coconut Water - Afternoon"],
        "duration": "7-10 days",
        "hospitals": [
            {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
            {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}
        ]
    },
    {
        "tag": "skin_problems",
        "patterns": ["skin rash", "skin allergy", "itching", "skin irritation", "pimples", "acne"],
        "responses": ["Neem and turmeric help to cleanse the blood and alleviate skin problems."],
        "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night", "Aloe Vera Gel - Topical"],
        "duration": "2-4 weeks",
        "hospitals": [
            {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
            {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}
        ]
    }
]

def preprocess_image(image):
    """Preprocess image for model prediction"""
    try:
        # Convert PIL image to numpy array
        img_array = np.array(image)
        
        # Resize to model input size (assuming 224x224, adjust based on your model)
        img_resized = cv2.resize(img_array, (224, 224))
        
        # Normalize pixel values
        img_normalized = img_resized.astype('float32') / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
    except Exception as e:
        st.error(f"Error preprocessing image: {e}")
        return None

def predict_disease_from_image(image, model):
    """Predict disease from uploaded image using the trained model"""
    if model is None:
        return "Model not available", 0.0
    
    try:
        processed_image = preprocess_image(image)
        if processed_image is None:
            return "Error processing image", 0.0
        
        # Make prediction
        predictions = model.predict(processed_image)
        
        # Get the class with highest probability
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        predicted_disease = DISEASE_CLASSES[predicted_class_idx].lower()
        
        return predicted_disease, confidence
    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return "Error in prediction", 0.0

def match_intent(user_input):
    """Match user input to predefined intents"""
    user_input = user_input.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input:
                return intent
    return None

def get_ayurvedic_response(disease, confidence=None):
    """Get comprehensive Ayurvedic response for a disease"""
    ayurvedic_data = load_ayurvedic_data()
    
    if disease in ayurvedic_data:
        data = ayurvedic_data[disease]
        response = f"**Detected Condition:** {disease.replace('_', ' ').title()}"
        
        if confidence:
            response += f" (Confidence: {confidence:.2%})"
        
        response += f"\n\n**Recommended Ayurvedic Treatment:**\n"
        for medicine in data['medicines']:
            response += f"• {medicine}\n"
        
        response += f"\n**Duration:** {data['duration']}"
        response += f"\n\n**Additional Advice:** {data['advice']}"
        
        return response
    else:
        return f"I detected {disease.replace('_', ' ').title()}, but I don't have specific Ayurvedic recommendations for this condition. Please consult an Ayurvedic practitioner."

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False

def add_to_chat_history(message, sender):
    """Add message to chat history"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        'message': message,
        'sender': sender,
        'timestamp': timestamp
    })

def display_chat_history():
    """Display chat history in ChatGPT-like format"""
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            if chat['sender'] == 'user':
                st.markdown(f'<div class="user-message">{chat["message"]} <small>({chat["timestamp"]})</small></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{chat["message"]} <small>({chat["timestamp"]})</small></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🌿 AI Ayurveda Assistant</h1>', unsafe_allow_html=True)
    st.markdown("**Your Personal Ayurvedic Health Companion with AI-Powered Image Analysis**")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Features")
        st.write("• AI-powered symptom analysis")
        st.write("• Image-based disease detection")
        st.write("• Personalized Ayurvedic recommendations")
        st.write("• Medicine dosage & timing")
        st.write("• Hospital recommendations")
        
        st.header("📋 Quick Actions")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("📥 Download Chat"):
            chat_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="Download as JSON",
                data=chat_data,
                file_name=f"ayurveda_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat history
        display_chat_history()
        
        # Chat input
        user_input = st.text_input("Type your symptoms or health concerns:", placeholder="e.g., I have a headache and fever...")
        
        if st.button("Send Message") and user_input:
            # Add user message to history
            add_to_chat_history(user_input, 'user')
            
            # Process user input
            matched_intent = match_intent(user_input)
            
            if matched_intent:
                response = random.choice(matched_intent["responses"])
                
                # Create detailed response
                detailed_response = f"**{response}**\n\n"
                
                if "medicines" in matched_intent:
                    detailed_response += "**Recommended Medicines:**\n"
                    for medicine in matched_intent["medicines"]:
                        detailed_response += f"• {medicine}\n"
                
                if "duration" in matched_intent:
                    detailed_response += f"\n**Treatment Duration:** {matched_intent['duration']}\n"
                
                if "hospitals" in matched_intent:
                    detailed_response += "\n**Recommended Ayurvedic Centers:**\n"
                    for hospital in matched_intent["hospitals"]:
                        detailed_response += f"• {hospital['name']} - {hospital['contact']}\n"
                
                add_to_chat_history(detailed_response, 'bot')
            else:
                fallback_response = "I understand you're experiencing some health concerns. Could you please provide more specific symptoms? You can also upload an image for analysis, or try phrases like 'I have a headache' or 'I have fever'."
                add_to_chat_history(fallback_response, 'bot')
            
            st.rerun()
    
    with col2:
        st.subheader("📸 Image Analysis")
        st.markdown('<div class="image-analysis">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload an image for AI analysis",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected area for AI-powered diagnosis"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Load model and make prediction
            model = load_model()
            
            with st.spinner("🔍 Analyzing image with AI..."):
                predicted_disease, confidence = predict_disease_from_image(image, model)
            
            if confidence > 0.5:  # Only show results if confidence is reasonable
                st.success(f"**Analysis Complete!**")
                
                # Get Ayurvedic recommendations
                ayurvedic_response = get_ayurvedic_response(predicted_disease, confidence)
                
                # Add to chat history
                image_analysis_message = f"📸 **Image Analysis Result:**\n\n{ayurvedic_response}"
                add_to_chat_history(image_analysis_message, 'bot')
                
                # Display medicine recommendations in a card
                st.markdown('<div class="medicine-card">', unsafe_allow_html=True)
                st.markdown("**🌿 Ayurvedic Treatment Plan**")
                st.write(ayurvedic_response)
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.warning("⚠️ Low confidence in analysis. Please upload a clearer image or describe your symptoms in the chat.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick symptom buttons
        st.subheader("🚀 Quick Symptoms")
        quick_symptoms = ["Headache", "Fever", "Cold", "Acidity", "Skin Rash"]
        
        for symptom in quick_symptoms:
            if st.button(f"I have {symptom}", key=f"quick_{symptom}"):
                add_to_chat_history(f"I have {symptom.lower()}", 'user')
                
                matched_intent = match_intent(symptom.lower())
                if matched_intent:
                    response = random.choice(matched_intent["responses"])
                    detailed_response = f"**{response}**\n\n"
                    
                    if "medicines" in matched_intent:
                        detailed_response += "**Recommended Medicines:**\n"
                        for medicine in matched_intent["medicines"]:
                            detailed_response += f"• {medicine}\n"
                    
                    add_to_chat_history(detailed_response, 'bot')
                
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**⚠️ Disclaimer:** This AI assistant provides general Ayurvedic guidance only. "
        "Always consult qualified healthcare professionals for serious health conditions."
    )

if __name__ == "__main__":
    main()
