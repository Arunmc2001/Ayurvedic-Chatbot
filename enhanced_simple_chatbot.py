import streamlit as st
import random
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Enhanced Ayurveda Chatbot",
    page_icon="🌿",
    layout="centered"
)

# Complete intents from cha2.py with enhanced patterns for natural conversation
intents = [
    {"tag": "cold", "patterns": ["I have a cold", "feeling cold", "cold symptoms", "runny nose", "sneezing"], "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "cough", "patterns": ["I have a cough", "coughing", "throat irritation", "dry cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "fever", "patterns": ["I have a fever", "high temperature", "feeling hot", "body heat"], "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "headache", "patterns": ["My head hurts", "I have a headache", "head pain", "migraine"], "responses": ["I understand you're experiencing head pain. Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "acidity", "patterns": ["I have acidity", "acid reflux", "heartburn", "stomach burning"], "responses": ["I can help with acidity issues. Amla juice and jeera water can help to reduce acidity."], "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals"], "duration": "7-10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "stress", "patterns": ["I feel stressed", "anxiety", "worried", "tension", "mental stress"], "responses": ["I understand you're feeling stressed. Brahmi and meditation are helpful for stress management."], "medicines": ["Brahmi - Morning", "Shankhpushpi - Night"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "acne", "patterns": ["I have acne", "pimples", "skin breakout", "facial acne"], "responses": ["Acne can be frustrating. Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "diabetes", "patterns": ["I have diabetes", "blood sugar", "high glucose", "diabetic"], "responses": ["Managing diabetes is important. Karela and Jamun juice can help manage blood sugar levels."], "medicines": ["Karela Juice - Morning", "Jamun Juice - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "hypertension", "patterns": ["I have high blood pressure", "hypertension", "BP problem"], "responses": ["High blood pressure needs attention. Arjuna bark and garlic are known to support healthy blood pressure levels."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "indigestion", "patterns": ["I have indigestion", "stomach upset", "digestion problem"], "responses": ["Consume ajwain water to relieve indigestion symptoms."], "medicines": ["Ajwain Water - After Meals"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "constipation", "patterns": ["I am constipated", "constipation", "bowel problem"], "responses": ["Triphala powder helps to improve digestion and relieve constipation."], "medicines": ["Triphala Powder - Before Bed"], "duration": "7-14 days (or as needed)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "insomnia", "patterns": ["I have trouble sleeping", "can't sleep", "insomnia", "sleepless"], "responses": ["Ashwagandha and warm milk can promote better sleep."], "medicines": ["Ashwagandha - Evening", "Warm Milk - Before Bed"], "duration": "10-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "skin_allergy", "patterns": ["I have a skin allergy", "skin rash", "itchy skin", "allergic reaction"], "responses": ["Neem and turmeric help to cleanse the blood and alleviate skin allergies."], "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night"], "duration": "2-3 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "hair_fall", "patterns": ["I have hair fall", "hair loss", "balding", "thinning hair"], "responses": ["Bhringraj oil helps strengthen hair roots and prevent hair fall."], "medicines": ["Bhringraj Oil - Night", "Amla Juice - Morning"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "joint_pain", "patterns": ["I have joint pain", "arthritis", "knee pain", "joint ache"], "responses": ["Shallaki and turmeric are effective in reducing joint pain and inflammation."], "medicines": ["Shallaki - Morning", "Turmeric Capsules - Night"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "asthma", "patterns": ["I have asthma", "breathing problem", "wheezing", "shortness of breath"], "responses": ["Tulsi and mulethi help relieve asthma symptoms and clear airways."], "medicines": ["Tulsi Capsules - Morning", "Mulethi Powder - Night"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "vomiting", "patterns": ["I am vomiting", "nausea", "feeling sick", "throwing up"], "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "piles", "patterns": ["I have piles", "hemorrhoids", "anal pain"], "responses": ["Triphala and aloe vera juice help relieve piles symptoms."], "medicines": ["Triphala - Night", "Aloe Vera Juice - Morning"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "GERD", "patterns": ["I have GERD", "acid reflux", "gastric problem"], "responses": ["For GERD, try licorice root tea and avoid spicy foods."], "medicines": ["Licorice Root Tea - Morning", "Aloe Vera Juice - Before Meals"], "duration": "15-30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "Jaundice", "patterns": ["I have jaundice", "yellow eyes", "liver problem"], "responses": ["Sugarcane juice and Kutki herb are beneficial for liver detox."], "medicines": ["Sugarcane Juice - Morning", "Kutki Powder - Evening"], "duration": "7-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "Chicken_pox", "patterns": ["I have chicken pox", "chickenpox", "pox"], "responses": ["Neem bath and Tulsi tea can help soothe chicken pox symptoms."], "medicines": ["Neem Bath - Daily", "Tulsi Tea - Morning"], "duration": "7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "Psoriasis", "patterns": ["I have psoriasis", "skin patches", "scaly skin"], "responses": ["Aloe vera gel and turmeric help relieve psoriasis symptoms."], "medicines": ["Aloe Vera Gel - Night", "Turmeric Milk - Morning"], "duration": "60 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}}
]

def enhanced_match_intent(user_input):
    """Enhanced pattern matching for natural conversation"""
    user_input_lower = user_input.lower()
    
    # Direct keyword matching with scoring
    best_match = None
    best_score = 0
    
    for intent in intents:
        score = 0
        for pattern in intent["patterns"]:
            pattern_lower = pattern.lower()
            
            # Exact match gets highest score
            if pattern_lower in user_input_lower:
                score += 10
            
            # Partial word matching
            pattern_words = pattern_lower.split()
            user_words = user_input_lower.split()
            
            for pattern_word in pattern_words:
                for user_word in user_words:
                    if pattern_word in user_word or user_word in pattern_word:
                        score += 5
        
        if score > best_score:
            best_score = score
            best_match = intent
    
    return best_match if best_score > 0 else None

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False

def add_to_chat_history(message, sender, intent_data=None):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'message': message,
        'sender': sender,
        'intent_data': intent_data
    })

def display_chat_history():
    """Display chat history in conversational format"""
    for chat in st.session_state.chat_history[-10:]:
        if chat['sender'] == 'user':
            st.markdown(f"**You:** {chat['message']}")
        else:
            st.markdown(f"**Dr. Ayurveda:** {chat['message']}")
            
            # Display treatment plan if available
            if chat.get('intent_data'):
                intent = chat['intent_data']
                with st.expander("📋 Treatment Details", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**💊 Medicines:**")
                        for medicine in intent["medicines"]:
                            st.write(f"• {medicine}")
                        
                        st.write(f"**⏰ Duration:** {intent['duration']}")
                    
                    with col2:
                        st.write("**🏥 Hospitals in Mysore:**")
                        for hospital in intent["hospital"]["mysore"][:2]:  # Show first 2
                            st.write(f"• {hospital['name']}")
                            st.write(f"  📞 {hospital['contact']}")

def main():
    st.title("🌿 Dr. Ayurveda - Your Personal Health Assistant")
    
    # Welcome message
    if not st.session_state.conversation_started:
        st.markdown("""
        **Welcome! I'm Dr. Ayurveda, your personal Ayurvedic health assistant.**
        
        I can help you with natural remedies for various health conditions. Just describe how you're feeling in your own words.
        
        *Examples: "I'm feeling cold", "My head hurts", "I have acne problems"*
        """)
        st.session_state.conversation_started = True
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        display_chat_history()
        st.markdown("---")
    
    # Text input
    user_input = st.text_input(
        "How are you feeling today?", 
        placeholder="Describe your symptoms naturally...",
        key="user_input"
    )
    
    # Send button
    if st.button("💬 Send", type="primary") and user_input.strip():
        # Add user message
        add_to_chat_history(user_input, 'user')
        
        # Match intent with enhanced matching
        matched_intent = enhanced_match_intent(user_input)
        
        if matched_intent:
            # Get response
            response = random.choice(matched_intent["responses"])
            add_to_chat_history(response, 'bot', matched_intent)
            
            st.success("✅ Treatment recommendation ready!")
            
        else:
            # Fallback response
            fallback_responses = [
                "I understand you're not feeling well. Could you describe your symptoms more specifically?",
                "I want to help you feel better. Can you tell me more about what's bothering you?",
                "Let me help you with that. Could you be more specific about your symptoms?"
            ]
            fallback_msg = random.choice(fallback_responses)
            add_to_chat_history(fallback_msg, 'bot')
        
        # Refresh to show updated chat
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Start New Conversation"):
            st.session_state.chat_history = []
            st.session_state.conversation_started = False
            st.rerun()

if __name__ == "__main__":
    main()
