import streamlit as st
import random

# Configure Streamlit page
st.set_page_config(
    page_title="Simple Ayurveda Chatbot",
    page_icon="🌿",
    layout="centered"
)

# Intent-based chatbot responses (from cha2.py)
intents = [
    {"tag": "cold", "patterns": ["I have a cold"], "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "cough", "patterns": ["I have a cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "fever", "patterns": ["I have a fever"], "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "headache", "patterns": ["My head hurts", "I have a headache"], "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "acidity", "patterns": ["I have acidity"], "responses": ["Amla juice and jeera water can help to reduce acidity."], "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals"], "duration": "7-10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "indigestion", "patterns": ["I have indigestion"], "responses": ["Consume ajwain water to relieve indigestion symptoms."], "medicines": ["Ajwain Water - After Meals"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "constipation", "patterns": ["I am constipated"], "responses": ["Triphala powder helps to improve digestion and relieve constipation."], "medicines": ["Triphala Powder - Before Bed"], "duration": "7-14 days (or as needed)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "insomnia", "patterns": ["I have trouble sleeping"], "responses": ["Ashwagandha and warm milk can promote better sleep."], "medicines": ["Ashwagandha - Evening", "Warm Milk - Before Bed"], "duration": "10-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "stress", "patterns": ["I feel stressed"], "responses": ["Brahmi and meditation are helpful for stress management."], "medicines": ["Brahmi - Morning", "Shankhpushpi - Night"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "skin_allergy", "patterns": ["I have a skin allergy"], "responses": ["Neem and turmeric help to cleanse the blood and alleviate skin allergies."], "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night"], "duration": "2-3 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "hair_fall", "patterns": ["I have hair fall"], "responses": ["Bhringraj oil helps strengthen hair roots and prevent hair fall."], "medicines": ["Bhringraj Oil - Night", "Amla Juice - Morning"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "joint_pain", "patterns": ["I have joint pain"], "responses": ["Shallaki and turmeric are effective in reducing joint pain and inflammation."], "medicines": ["Shallaki - Morning", "Turmeric Capsules - Night"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "diabetes", "patterns": ["I have diabetes"], "responses": ["Karela and Jamun juice can help manage blood sugar levels."], "medicines": ["Karela Juice - Morning", "Jamun Juice - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "hypertension", "patterns": ["I have high blood pressure"], "responses": ["Arjuna bark and garlic are known to support healthy blood pressure levels."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "asthma", "patterns": ["I have asthma"], "responses": ["Tulsi and mulethi help relieve asthma symptoms and clear airways."], "medicines": ["Tulsi Capsules - Morning", "Mulethi Powder - Night"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "acne", "patterns": ["I have acne", "I have pimples"], "responses": ["Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "vomiting", "patterns": ["I am vomiting"], "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}}
]

def match_intent(user_input):
    """Match user input to intent patterns"""
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input.lower():
                return intent
    return None

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def add_to_chat_history(message, sender):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'message': message,
        'sender': sender
    })

def display_chat_history():
    """Display chat history"""
    for chat in st.session_state.chat_history[-10:]:  # Show last 10 messages
        if chat['sender'] == 'user':
            st.write(f"**You:** {chat['message']}")
        else:
            st.write(f"**Ayurveda Bot:** {chat['message']}")

def main():
    st.title("🌿 Simple Ayurveda Chatbot")
    st.write("Ask about your symptoms and get Ayurvedic treatment suggestions.")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Chat History")
        display_chat_history()
        st.divider()
    
    # Text input for user message
    user_input = st.text_input("Type your message:", placeholder="e.g., 'I have a headache' or 'I feel stressed'")
    
    # Send button
    if st.button("Send", type="primary") and user_input.strip():
        # Add user message to history
        add_to_chat_history(user_input, 'user')
        
        # Match intent and get response
        matched_intent = match_intent(user_input)
        
        if matched_intent:
            # Get random response
            response = random.choice(matched_intent["responses"])
            add_to_chat_history(response, 'bot')
            
            # Display treatment information
            st.success("✅ Treatment plan found!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💊 Medicines & Timings")
                for medicine in matched_intent["medicines"]:
                    st.write(f"• {medicine}")
                
                st.subheader("⏰ Duration")
                st.write(matched_intent["duration"])
            
            with col2:
                st.subheader("🏥 Recommended Hospitals")
                for hospital in matched_intent["hospital"]["mysore"]:
                    st.write(f"• **{hospital['name']}**")
                    st.write(f"  📞 {hospital['contact']}")
        else:
            fallback_msg = "I couldn't find specific treatment for that. Please try describing your symptoms more clearly (e.g., 'I have a headache', 'I feel stressed', 'I have acne')."
            add_to_chat_history(fallback_msg, 'bot')
            st.warning(fallback_msg)
        
        # Refresh to show updated chat
        st.rerun()
    
    # Clear chat history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()
