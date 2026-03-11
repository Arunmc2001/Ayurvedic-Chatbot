# # # #*****************************************************************************************************
# # # #STAGE 1 DEVELOPMENT CODE(PREFER NOT TO RUN UNTILL ASKED).
# # # # REFERE DOCUMENT HOW TO RUN STAGE 1 IN ONE SHOOT.
# # # #*****************************************************************************************************

# # # # import os
# # # # import nltk
# # # # import ssl
# # # # import streamlit as st
# # # # import random
# # # # import tensorflow as tf
# # # # import numpy as np
# # # # from PIL import Image
# # # # from sklearn.feature_extraction.text import TfidfVectorizer
# # # # from sklearn.linear_model import LogisticRegression

# # # # ssl._create_default_https_context = ssl._create_unverified_context
# # # # nltk.data.path.append(os.path.abspath("nltk_data"))
# # # # nltk.download('punkt')

# # # # intents = [
# # # #     {"tag": "greeting", "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"],
# # # #      "responses": ["Namaste! How can I assist you today?", "Hello! How are you feeling today?", "Greetings! Need any Ayurvedic help?"]},

# # # #     {"tag": "headache", "patterns": ["I have a headache", "My head hurts"],
# # # #      "responses": [
# # # #          "Headaches are often linked to Pitta imbalance in Ayurveda. Try cooling foods and meditation.",
# # # #          "Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."
# # # #      ]},

# # # #     {"tag": "ayurvedic_treatment", "patterns": ["What is the remedy for cold?", "How to cure acidity naturally?"],
# # # #      "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil.",
# # # #                    "For acidity, drink a glass of cold milk and chew fennel seeds after meals."]},

# # # #     {"tag": "diet_lifestyle", "patterns": ["What should a Pitta type eat?", "Best yoga for relaxation?"],
# # # #      "responses": ["Pitta types should favor cooling foods like cucumbers and coconut water.",
# # # #                    "For relaxation, practice deep breathing, meditation, and gentle yoga like Shavasana."]},

# # # #     {"tag": "goodbye", "patterns": ["Bye", "See you later", "Goodbye"],
# # # #      "responses": ["Goodbye! Stay healthy and balanced.", "Take care! Let Ayurveda guide your wellness."]}
# # # # ]

# # # # # Load Image Model (replace 'your_model_path.h5' with your image classification model path)
# # # # @st.cache_resource
# # # # def load_image_model():
# # # #     model = tf.keras.models.load_model("your_model_path.h5")
# # # #     return model

# # # # image_model = load_image_model()

# # # # def predict_symptoms(image):
# # # #     image = image.resize((224, 224))
# # # #     image_array = np.array(image) / 255.0
# # # #     image_array = np.expand_dims(image_array, axis=0)

# # # #     predictions = image_model.predict(image_array)
# # # #     classes = ['Headache', 'Cold', 'Skin Rash', 'Eye Irritation', 'Joint Pain']
# # # #     predicted_symptom = classes[np.argmax(predictions)]

# # # #     return f"Detected symptom: {predicted_symptom}. Consider consulting an Ayurvedic specialist."

# # # # # Create the vectorizer and classifier
# # # # vectorizer = TfidfVectorizer()
# # # # clf = LogisticRegression(random_state=0, max_iter=10000)

# # # # # Preprocess the data
# # # # tags = []
# # # # patterns = []
# # # # for intent in intents:
# # # #     for pattern in intent['patterns']:
# # # #         tags.append(intent['tag'])
# # # #         patterns.append(pattern)

# # # # # Train the model
# # # # x = vectorizer.fit_transform(patterns)
# # # # y = tags
# # # # clf.fit(x, y)

# # # # def chatbot(input_text):
# # # #     input_text = vectorizer.transform([input_text])
# # # #     tag = clf.predict(input_text)[0]
# # # #     for intent in intents:
# # # #         if intent['tag'] == tag:
# # # #             return random.choice(intent['responses'])

# # # # counter = 0

# # # # def main():
# # # #     global counter
# # # #     st.title("Ayurvedic Chatbot")
# # # #     st.write("Enter your symptoms, ask about Ayurveda, or upload an image for symptom detection.")

# # # #     counter += 1
# # # #     user_input = st.text_input("You:", key=f"user_input_{counter}")

# # # #     if user_input:
# # # #         response = chatbot(user_input)
# # # #         st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

# # # #         if response.lower() in ['goodbye', 'bye']:
# # # #             st.write("Thank you for chatting. Stay healthy!")
# # # #             st.stop()

# # # #     # Image upload and symptom detection
# # # #     uploaded_image = st.file_uploader("Upload an image to detect symptoms", type=["jpg", "png", "jpeg"])

# # # #     if uploaded_image:
# # # #         image = Image.open(uploaded_image)
# # # #         st.image(image, caption="Uploaded Image", use_column_width=True)

# # # #         symptom_result = predict_symptoms(image)
# # # #         st.text_area("Symptom Analysis:", value=symptom_result, height=100, key=f"image_symptom_{counter}")

# # # # if __name__ == '__main__':
# # # #     main()



# # # #*****************************************************************************************************
# # # #STAGE 2 DEVELOPMENT CODE(PREFER TO RUN THIS).
# # # #*****************************************************************************************************

# # # # import streamlit as st
# # # # import os
# # # # import random
# # # # from PIL import Image

# # # # def load_ayurvedic_data():
# # # #     return {
# # # #         'skin_rashes': ['Neem Paste - Morning', 'Aloe Vera Gel - Night'],
# # # #         'vomiting': ['Ginger Juice - Morning', 'Lemon Water - After Meals'],
# # # #         'pimples': ['Turmeric Paste - Evening', 'Neem Capsules - Morning'],
# # # #         'headache': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep']
# # # #     }

# # # # def recognize_disease_from_filename(filename):
# # # #     filename = os.path.splitext(filename)[0].lower()
# # # #     known_diseases = ['skin_rashes', 'vomiting', 'pimples', 'headache']
    
# # # #     for disease in known_diseases:
# # # #         if disease in filename:
# # # #             return disease
# # # #     return 'unknown'

# # # # def get_medicine_suggestions(disease, ayurvedic_data):
# # # #     return ayurvedic_data.get(disease, ["No specific medicine found. Please consult an Ayurvedic doctor."])

# # # # # Intent-based chatbot responses
# # # # intents = [
# # # #   {"tag": "cold",
# # # #   "patterns": ["I have a cold"],
# # # #   "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."],
# # # #   "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"],
# # # #   "duration": "5-7 days",
# # # #   "hospital": {
# # # #     "mysore": [
# # # #       {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
# # # #       {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"},
# # # #       {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"},
# # # #       {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}
# # # #     ]
# # # #   }},
# # # #   {"tag": "cough", "patterns": ["I have a cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days"},
# # # #   {"tag": "fever", "patterns": ["I have a fever"], "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days"},
# # # #   {"tag": "headache", "patterns": ["My head hurts"], "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent"},
# # # #   {"tag": "acidity", "patterns": ["I have acidity"], "responses": ["Amla juice and jeera water can help to reduce acidity."], "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals"], "duration": "7-10 days"},
# # # #   {"tag": "indigestion", "patterns": ["I have indigestion"], "responses": ["Consume ajwain water to relieve indigestion symptoms."], "medicines": ["Ajwain Water - After Meals"], "duration": "3-5 days"},
# # # #   {"tag": "constipation", "patterns": ["I am constipated"], "responses": ["Triphala powder helps to improve digestion and relieve constipation."], "medicines": ["Triphala Powder - Before Bed"], "duration": "7-14 days (or as needed)"},
# # # #   {"tag": "insomnia", "patterns": ["I have trouble sleeping"], "responses": ["Ashwagandha and warm milk can promote better sleep."], "medicines": ["Ashwagandha - Evening", "Warm Milk - Before Bed"], "duration": "10-14 days"},
# # # #   {"tag": "stress", "patterns": ["I feel stressed"], "responses": ["Brahmi and meditation are helpful for stress management."], "medicines": ["Brahmi - Morning", "Shankhpushpi - Night"], "duration": "2-4 weeks"},
# # # #   {"tag": "skin_allergy", "patterns": ["I have a skin allergy"], "responses": ["Neem and turmeric help to cleanse the blood and alleviate skin allergies."], "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night"], "duration": "2-3 weeks"},
# # # #   {"tag": "hair_fall", "patterns": ["I have hair fall"], "responses": ["Bhringraj oil helps strengthen hair roots and prevent hair fall."], "medicines": ["Bhringraj Oil - Night", "Amla Juice - Morning"], "duration": "4-6 weeks"},
# # # #   {"tag": "joint_pain", "patterns": ["I have joint pain"], "responses": ["Shallaki and turmeric are effective in reducing joint pain and inflammation."], "medicines": ["Shallaki - Morning", "Turmeric Capsules - Night"], "duration": "4-6 weeks"},
# # # #   {"tag": "diabetes", "patterns": ["I have diabetes"], "responses": ["Karela and Jamun juice can help manage blood sugar levels."], "medicines": ["Karela Juice - Morning", "Jamun Juice - Evening"], "duration": "Ongoing (consult doctor)"},
# # # #   {"tag": "hypertension", "patterns": ["I have high blood pressure"], "responses": ["Arjuna bark and garlic are known to support healthy blood pressure levels."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)"},
# # # #   {"tag": "asthma", "patterns": ["I have asthma"], "responses": ["Tulsi and mulethi help relieve asthma symptoms and clear airways."], "medicines": ["Tulsi Capsules - Morning", "Mulethi Powder - Night"], "duration": "Ongoing (consult doctor)"},
# # # #   {"tag": "piles", "patterns": ["I have piles"], "responses": ["Triphala and aloe vera juice help relieve piles symptoms."], "medicines": ["Triphala - Night", "Aloe Vera Juice - Morning"], "duration": "2-4 weeks"},
# # # #   {"tag": "heart_pain", "patterns": ["I have heart pain"], "responses": ["Arjuna bark and garlic help support heart health and reduce chest discomfort."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)"},
# # # #   {"tag": "leg_pain", "patterns": ["I have leg pain"], "responses": ["Ashwagandha and massage with sesame oil can help relieve leg pain."], "medicines": ["Ashwagandha - Evening", "Sesame Oil Massage - Night"], "duration": "2-3 weeks"},
# # # #   {"tag": "vomiting", "patterns": ["I am vomiting"], "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days"},
# # # #   {"tag": "muscle_cramp", "patterns": ["I have muscle cramps"], "responses": ["Magnesium supplements and coconut water are effective in relieving muscle cramps."], "medicines": ["Magnesium Supplement - Morning", "Coconut Water - Afternoon"], "duration": "3-5 days (or as needed)"},
# # # #   {"tag": "GERD", "patterns": ["I have GERD"], "responses": ["For GERD, try licorice root tea and avoid spicy foods."], "medicines": ["Licorice Root Tea - Morning", "Aloe Vera Juice - Before Meals"], "duration": "15-30 days"},
# # # #   {"tag": "Jaundice", "patterns": ["I have jaundice"], "responses": ["Sugarcane juice and Kutki herb are beneficial for liver detox."], "medicines": ["Sugarcane Juice - Morning", "Kutki Powder - Evening"], "duration": "7-14 days"},
# # # #   {"tag": "Malaria", "patterns": ["I have malaria"], "responses": ["Neem leaves and Papaya leaf extract help in malaria recovery."], "medicines": ["Neem Leaves - Morning", "Papaya Leaf Extract - Night"], "duration": "10 days"},
# # # #   {"tag": "Chicken_pox", "patterns": ["I have chicken pox"], "responses": ["Neem bath and Tulsi tea can help soothe chicken pox symptoms."], "medicines": ["Neem Bath - Daily", "Tulsi Tea - Morning"], "duration": "7 days"},
# # # #   {"tag": "Dengue", "patterns": ["I have dengue"], "responses": ["Papaya leaf juice and Giloy help boost platelet count in dengue."], "medicines": ["Papaya Leaf Juice - Morning", "Giloy Juice - Night"], "duration": "10-14 days"},
# # # #   {"tag": "Typhoid", "patterns": ["I have typhoid"], "responses": ["Cloves and pomegranate juice aid in typhoid recovery."], "medicines": ["Clove Tea - Morning", "Pomegranate Juice - Afternoon"], "duration": "10-14 days"},
# # # #   {"tag": "Hepatitis", "patterns": ["I have hepatitis"], "responses": ["Bhumyamalaki and Amla juice help in liver function recovery."], "medicines": ["Bhumyamalaki Powder - Morning", "Amla Juice - Night"], "duration": "30 days"},
# # # #   {"tag": "Tuberculosis", "patterns": ["I have tuberculosis"], "responses": ["Ashwagandha and black pepper can help strengthen immunity."], "medicines": ["Ashwagandha - Morning", "Black Pepper Tea - Evening"], "duration": "45-60 days"},
# # # #   {"tag": "Pneumonia", "patterns": ["I have pneumonia"], "responses": ["Turmeric and ginger tea can help with pneumonia symptoms."], "medicines": ["Turmeric Milk - Night", "Ginger Tea - Morning"], "duration": "14 days"},
# # # #   {"tag": "Hypothyroidism", "patterns": ["I have hypothyroidism"], "responses": ["Ashwagandha and coconut oil help regulate thyroid function."], "medicines": ["Ashwagandha - Morning", "Coconut Oil - Before Meals"], "duration": "60 days"},
# # # #   {"tag": "Hyperthyroidism", "patterns": ["I have hyperthyroidism"], "responses": ["Bugleweed herb and lemon balm tea can help manage hyperthyroidism."], "medicines": ["Bugleweed Tea - Morning", "Lemon Balm Tea - Evening"], "duration": "45 days"},
# # # #   {"tag": "Hypoglycemia", "patterns": ["I have hypoglycemia"], "responses": ["Bael fruit and jaggery water help maintain blood sugar levels."], "medicines": ["Bael Juice - Morning", "Jaggery Water - Afternoon"], "duration": "15-30 days"},
# # # #   {"tag": "Osteoarthritis", "patterns": ["I have osteoarthritis"], "responses": ["Shallaki and Moringa are good for joint health."], "medicines": ["Shallaki - Morning", "Moringa Powder - Night"], "duration": "90 days"},
# # # #   {"tag": "Acne", "patterns": ["I have acne"], "responses": ["Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days"},
# # # #   {"tag": "Urinary_Tract_Infection", "patterns": ["I have UTI"], "responses": ["Cranberry juice and coriander water help with urinary tract infections."], "medicines": ["Cranberry Juice - Morning", "Coriander Water - Night"], "duration": "10 days"},
# # # #   {"tag": "Psoriasis", "patterns": ["I have psoriasis"], "responses": ["Aloe vera gel and turmeric help relieve psoriasis symptoms."], "medicines": ["Aloe Vera Gel - Night", "Turmeric Milk - Morning"], "duration": "60 days"},
# # # #   {"tag": "Impetigo", "patterns": ["I have impetigo"], "responses": ["Tea tree oil and neem paste can help treat impetigo."], "medicines": ["Tea Tree Oil - Night", "Neem Paste - Morning"], "duration": "14 days"}
# # # # ]


# # # # def match_intent(user_input):
# # # #     for intent in intents:
# # # #         for pattern in intent["patterns"]:
# # # #             if pattern.lower() in user_input.lower():
# # # #                 return intent
# # # #     return None

# # # # def main():
# # # #     st.title("Arvedic Chat Bot")
# # # #     st.write("Upload images or type a disease to get Ayurvedic medicine suggestions.")

# # # #     ayurvedic_data = load_ayurvedic_data()

# # # #     # Image Upload and Analysis
# # # #     uploaded_file = st.file_uploader("Upload an image (for disease detection)", type=["jpg", "jpeg", "png"])

# # # #     if uploaded_file is not None:
# # # #         image = Image.open(uploaded_file)
# # # #         st.image(image, caption="Uploaded Image", use_column_width=True)
        
# # # #         # Recognize disease from filename
# # # #         disease = recognize_disease_from_filename(uploaded_file.name)
# # # #         st.write(f"Detected Disease: {disease.replace('_', ' ').title()}")

# # # #         # Provide medicine suggestions if disease is identified
# # # #         if disease != 'unknown':
# # # #             suggestions = get_medicine_suggestions(disease, ayurvedic_data)
# # # #             st.write("### Suggested Medicines & Timings:")
# # # #             for suggestion in suggestions:
# # # #                 st.write(f"- {suggestion}")
# # # #         else:
# # # #             st.warning("Disease not recognized. Try describing your symptoms.")

# # # #     # Text Input for Disease
# # # #     user_input = st.text_input("Enter disease name or message:")

# # # #     if st.button("Get Ayurvedic Suggestions"):
# # # #         if user_input:
# # # #             matched_intent = match_intent(user_input)
# # # #             if matched_intent:
# # # #                 st.write("### Chatbot Response:")
# # # #                 st.write(random.choice(matched_intent["responses"]))

# # # #                 st.write("### Suggested Medicines & Timings:")
# # # #                 for suggestion in matched_intent["medicines"]:
# # # #                     st.write(f"- {suggestion}")

# # # #                 st.write("### Recommended Duration:")
# # # #                 st.write(f"{matched_intent['duration']}")
# # # #             else:
# # # #                 st.warning("No relevant suggestions found. Please rephrase or upload an image.")
# # # #         else:
# # # #             st.warning("Please enter a disease name or upload an image.")

# # # # if __name__ == "__main__":
# # # #     main()

# # # import streamlit as st
# # # import os
# # # import random
# # # from PIL import Image

# # # def load_ayurvedic_data():
# # #     return {
# # #         'skin_rashes': ['Neem Paste - Morning', 'Aloe Vera Gel - Night'],
# # #         'vomiting': ['Ginger Juice - Morning', 'Lemon Water - After Meals'],
# # #         'pimples': ['Turmeric Paste - Evening', 'Neem Capsules - Morning'],
# # #         'headache': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep']
# # #     }

# # # def recognize_disease_from_filename(filename):
# # #     filename = os.path.splitext(filename)[0].lower()
# # #     known_diseases = ['skin_rashes', 'vomiting', 'pimples', 'headache']
    
# # #     for disease in known_diseases:
# # #         if disease in filename:
# # #             return disease
# # #     return 'unknown'

# # # def get_medicine_suggestions(disease, ayurvedic_data):
# # #     return ayurvedic_data.get(disease, ["No specific medicine found. Please consult an Ayurvedic doctor."])

# # # # Intent-based chatbot responses
# # # intents = [
# # #   {
# # #     "tag": "cold",
# # #     "patterns": ["I have a cold"],
# # #     "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."],
# # #     "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"],
# # #     "duration": "5-7 days",
# # #     "hospital": {
# # #       "mysore": [
# # #         {"name": "Ayurveda Healing Center", "contact": "0821-123456"},
# # #         {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"},
# # #         {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"},
# # #         {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}
# # #       ]
# # #     }
# # #   },
# # #   {
# # #     "tag": "cough",
# # #     "patterns": ["I have a cough"],
# # #     "responses": ["For cough, consume ginger honey and mulethi for throat relief."],
# # #     "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"],
# # #     "duration": "5-7 days"
# # #   },
# # #   {
# # #     "tag": "headache",
# # #     "patterns": ["My head hurts"],
# # #     "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."],
# # #     "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"],
# # #     "duration": "As needed or 3-5 days if frequent"
# # #   },
# # #   {
# # #     "tag": "vomiting",
# # #     "patterns": ["I am vomiting"],
# # #     "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."],
# # #     "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"],
# # #     "duration": "2-3 days"
# # #   }
# # #   # You can include all the other intents here...
# # # ]

# # # def match_intent(user_input):
# # #     for intent in intents:
# # #         for pattern in intent["patterns"]:
# # #             if pattern.lower() in user_input.lower():
# # #                 return intent
# # #     return None

# # # def main():
# # #     st.title("Arvedic Chat Bot")
# # #     st.write("Upload images or type a disease to get Ayurvedic medicine suggestions.")

# # #     ayurvedic_data = load_ayurvedic_data()

# # #     # Image Upload and Analysis
# # #     uploaded_file = st.file_uploader("Upload an image (for disease detection)", type=["jpg", "jpeg", "png"])

# # #     if uploaded_file is not None:
# # #         image = Image.open(uploaded_file)
# # #         st.image(image, caption="Uploaded Image", use_column_width=True)
        
# # #         # Recognize disease from filename
# # #         disease = recognize_disease_from_filename(uploaded_file.name)
# # #         st.write(f"Detected Disease: {disease.replace('_', ' ').title()}")

# # #         # Provide medicine suggestions if disease is identified
# # #         if disease != 'unknown':
# # #             suggestions = get_medicine_suggestions(disease, ayurvedic_data)
# # #             st.write("### Suggested Medicines & Timings:")
# # #             for suggestion in suggestions:
# # #                 st.write(f"- {suggestion}")
# # #         else:
# # #             st.warning("Disease not recognized. Try describing your symptoms.")

# # #     # Text Input for Disease
# # #     user_input = st.text_input("Enter disease name or message:")

# # #     if st.button("Get Ayurvedic Suggestions"):
# # #         if user_input:
# # #             matched_intent = match_intent(user_input)
# # #             if matched_intent:
# # #                 st.write("### Chatbot Response:")
# # #                 st.write(random.choice(matched_intent["responses"]))

# # #                 st.write("### Suggested Medicines & Timings:")
# # #                 for suggestion in matched_intent["medicines"]:
# # #                     st.write(f"- {suggestion}")

# # #                 st.write("### Recommended Duration:")
# # #                 st.write(f"{matched_intent['duration']}")

# # #                 # NEW: Display hospital information if available
# # #                 if "hospital" in matched_intent:
# # #                     st.write("### Nearby Ayurvedic Hospitals:")
# # #                     for city, hospitals in matched_intent["hospital"].items():
# # #                         st.write(f"**City: {city.title()}**")
# # #                         for hospital in hospitals:
# # #                             st.write(f"- {hospital['name']} (Contact: {hospital['contact']})")
# # #             else:
# # #                 st.warning("No relevant suggestions found. Please rephrase or upload an image.")
# # #         else:
# # #             st.warning("Please enter a disease name or upload an image.")

# # # if __name__ == "__main__":
# # #     main()

# # import streamlit as st
# # import os
# # import random
# # from PIL import Image

# # def load_ayurvedic_data():
# #     return {
# #         'skin_rashes': ['Neem Paste - Morning', 'Aloe Vera Gel - Night'],
# #         'vomiting': ['Ginger Juice - Morning', 'Lemon Water - After Meals'],
# #         'pimples': ['Turmeric Paste - Evening', 'Neem Capsules - Morning'],
# #         'headache': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep']
# #     }

# # def recognize_disease_from_filename(filename):
# #     filename = os.path.splitext(filename)[0].lower()
# #     known_diseases = ['skin_rashes', 'vomiting', 'pimples', 'headache']
    
# #     for disease in known_diseases:
# #         if disease in filename:
# #             return disease
# #     return 'unknown'

# # def get_medicine_suggestions(disease, ayurvedic_data):
# #     return ayurvedic_data.get(disease, ["No specific medicine found. Please consult an Ayurvedic doctor."])

# # # Intent-based chatbot responses
# # intents = [
# #   {"tag": "cold", "patterns": ["I have a cold"], "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days","hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"},{"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"},{"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"},{"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
# #   {"tag": "cough", "patterns": ["I have a cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days"},
# #   {"tag": "fever", "patterns": ["I have a fever"], "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days"},
# #   {"tag": "headache", "patterns": ["My head hurts"], "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent"},
# #   {"tag": "acidity", "patterns": ["I have acidity"], "responses": ["Amla juice and jeera water can help to reduce acidity."], "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals"], "duration": "7-10 days"},
# #   {"tag": "indigestion", "patterns": ["I have indigestion"], "responses": ["Consume ajwain water to relieve indigestion symptoms."], "medicines": ["Ajwain Water - After Meals"], "duration": "3-5 days"},
# #   {"tag": "constipation", "patterns": ["I am constipated"], "responses": ["Triphala powder helps to improve digestion and relieve constipation."], "medicines": ["Triphala Powder - Before Bed"], "duration": "7-14 days (or as needed)"},
# #   {"tag": "insomnia", "patterns": ["I have trouble sleeping"], "responses": ["Ashwagandha and warm milk can promote better sleep."], "medicines": ["Ashwagandha - Evening", "Warm Milk - Before Bed"], "duration": "10-14 days"},
# #   {"tag": "stress", "patterns": ["I feel stressed"], "responses": ["Brahmi and meditation are helpful for stress management."], "medicines": ["Brahmi - Morning", "Shankhpushpi - Night"], "duration": "2-4 weeks"},
# #   {"tag": "skin_allergy", "patterns": ["I have a skin allergy"], "responses": ["Neem and turmeric help to cleanse the blood and alleviate skin allergies."], "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night"], "duration": "2-3 weeks"},
# #   {"tag": "hair_fall", "patterns": ["I have hair fall"], "responses": ["Bhringraj oil helps strengthen hair roots and prevent hair fall."], "medicines": ["Bhringraj Oil - Night", "Amla Juice - Morning"], "duration": "4-6 weeks"},
# #   {"tag": "joint_pain", "patterns": ["I have joint pain"], "responses": ["Shallaki and turmeric are effective in reducing joint pain and inflammation."], "medicines": ["Shallaki - Morning", "Turmeric Capsules - Night"], "duration": "4-6 weeks"},
# #   {"tag": "diabetes", "patterns": ["I have diabetes"], "responses": ["Karela and Jamun juice can help manage blood sugar levels."], "medicines": ["Karela Juice - Morning", "Jamun Juice - Evening"], "duration": "Ongoing (consult doctor)"},
# #   {"tag": "hypertension", "patterns": ["I have high blood pressure"], "responses": ["Arjuna bark and garlic are known to support healthy blood pressure levels."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)"},
# #   {"tag": "asthma", "patterns": ["I have asthma"], "responses": ["Tulsi and mulethi help relieve asthma symptoms and clear airways."], "medicines": ["Tulsi Capsules - Morning", "Mulethi Powder - Night"], "duration": "Ongoing (consult doctor)"},
# #   {"tag": "piles", "patterns": ["I have piles"], "responses": ["Triphala and aloe vera juice help relieve piles symptoms."], "medicines": ["Triphala - Night", "Aloe Vera Juice - Morning"], "duration": "2-4 weeks"},
# #   {"tag": "heart_pain", "patterns": ["I have heart pain"], "responses": ["Arjuna bark and garlic help support heart health and reduce chest discomfort."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)"},
# #   {"tag": "leg_pain", "patterns": ["I have leg pain"], "responses": ["Ashwagandha and massage with sesame oil can help relieve leg pain."], "medicines": ["Ashwagandha - Evening", "Sesame Oil Massage - Night"], "duration": "2-3 weeks"},
# #   {"tag": "vomiting", "patterns": ["I am vomiting"], "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days"},
# #   {"tag": "muscle_cramp", "patterns": ["I have muscle cramps"], "responses": ["Magnesium supplements and coconut water are effective in relieving muscle cramps."], "medicines": ["Magnesium Supplement - Morning", "Coconut Water - Afternoon"], "duration": "3-5 days (or as needed)"},
# #   {"tag": "GERD", "patterns": ["I have GERD"], "responses": ["For GERD, try licorice root tea and avoid spicy foods."], "medicines": ["Licorice Root Tea - Morning", "Aloe Vera Juice - Before Meals"], "duration": "15-30 days"},
# #   {"tag": "Jaundice", "patterns": ["I have jaundice"], "responses": ["Sugarcane juice and Kutki herb are beneficial for liver detox."], "medicines": ["Sugarcane Juice - Morning", "Kutki Powder - Evening"], "duration": "7-14 days"},
# #   {"tag": "Malaria", "patterns": ["I have malaria"], "responses": ["Neem leaves and Papaya leaf extract help in malaria recovery."], "medicines": ["Neem Leaves - Morning", "Papaya Leaf Extract - Night"], "duration": "10 days"},
# #   {"tag": "Chicken_pox", "patterns": ["I have chicken pox"], "responses": ["Neem bath and Tulsi tea can help soothe chicken pox symptoms."], "medicines": ["Neem Bath - Daily", "Tulsi Tea - Morning"], "duration": "7 days"},
# #   {"tag": "Dengue", "patterns": ["I have dengue"], "responses": ["Papaya leaf juice and Giloy help boost platelet count in dengue."], "medicines": ["Papaya Leaf Juice - Morning", "Giloy Juice - Night"], "duration": "10-14 days"},
# #   {"tag": "Typhoid", "patterns": ["I have typhoid"], "responses": ["Cloves and pomegranate juice aid in typhoid recovery."], "medicines": ["Clove Tea - Morning", "Pomegranate Juice - Afternoon"], "duration": "10-14 days"},
# #   {"tag": "Hepatitis", "patterns": ["I have hepatitis"], "responses": ["Bhumyamalaki and Amla juice help in liver function recovery."], "medicines": ["Bhumyamalaki Powder - Morning", "Amla Juice - Night"], "duration": "30 days"},
# #   {"tag": "Tuberculosis", "patterns": ["I have tuberculosis"], "responses": ["Ashwagandha and black pepper can help strengthen immunity."], "medicines": ["Ashwagandha - Morning", "Black Pepper Tea - Evening"], "duration": "45-60 days"},
# #   {"tag": "Pneumonia", "patterns": ["I have pneumonia"], "responses": ["Turmeric and ginger tea can help with pneumonia symptoms."], "medicines": ["Turmeric Milk - Night", "Ginger Tea - Morning"], "duration": "14 days"},
# #   {"tag": "Hypothyroidism", "patterns": ["I have hypothyroidism"], "responses": ["Ashwagandha and coconut oil help regulate thyroid function."], "medicines": ["Ashwagandha - Morning", "Coconut Oil - Before Meals"], "duration": "60 days"},
# #   {"tag": "Hyperthyroidism", "patterns": ["I have hyperthyroidism"], "responses": ["Bugleweed herb and lemon balm tea can help manage hyperthyroidism."], "medicines": ["Bugleweed Tea - Morning", "Lemon Balm Tea - Evening"], "duration": "45 days"},
# #   {"tag": "Hypoglycemia", "patterns": ["I have hypoglycemia"], "responses": ["Bael fruit and jaggery water help maintain blood sugar levels."], "medicines": ["Bael Juice - Morning", "Jaggery Water - Afternoon"], "duration": "15-30 days"},
# #   {"tag": "Osteoarthritis", "patterns": ["I have osteoarthritis"], "responses": ["Shallaki and Moringa are good for joint health."], "medicines": ["Shallaki - Morning", "Moringa Powder - Night"], "duration": "90 days"},
# #   {"tag": "Acne", "patterns": ["I have acne"], "responses": ["Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days"},
# #   {"tag": "Urinary_Tract_Infection", "patterns": ["I have UTI"], "responses": ["Cranberry juice and coriander water help with urinary tract infections."], "medicines": ["Cranberry Juice - Morning", "Coriander Water - Night"], "duration": "10 days"},
# #   {"tag": "Psoriasis", "patterns": ["I have psoriasis"], "responses": ["Aloe vera gel and turmeric help relieve psoriasis symptoms."], "medicines": ["Aloe Vera Gel - Night", "Turmeric Milk - Morning"], "duration": "60 days"},
# #   {"tag": "Impetigo", "patterns": ["I have impetigo"], "responses": ["Tea tree oil and neem paste can help treat impetigo."], "medicines": ["Tea Tree Oil - Night", "Neem Paste - Morning"], "duration": "14 days"}
# # ]


# # def match_intent(user_input):
# #     for intent in intents:
# #         for pattern in intent["patterns"]:
# #             if pattern.lower() in user_input.lower():
# #                 return intent
# #     return None

# # def main():
# #     st.title("Arvedic Chat Bot")
# #     st.write("Upload images or type a disease to get Ayurvedic medicine suggestions.")

# #     ayurvedic_data = load_ayurvedic_data()

# #     # Image Upload and Analysis
# #     uploaded_file = st.file_uploader("Upload an image (for disease detection)", type=["jpg", "jpeg", "png"])

# #     if uploaded_file is not None:
# #         image = Image.open(uploaded_file)
# #         st.image(image, caption="Uploaded Image", use_column_width=True)
        
# #         # Recognize disease from filename
# #         disease = recognize_disease_from_filename(uploaded_file.name)
# #         st.write(f"Detected Disease: {disease.replace('_', ' ').title()}")

# #         # Provide medicine suggestions if disease is identified
# #         if disease != 'unknown':
# #             suggestions = get_medicine_suggestions(disease, ayurvedic_data)
# #             st.write("### Suggested Medicines & Timings:")
# #             for suggestion in suggestions:
# #                 st.write(f"- {suggestion}")
# #         else:
# #             st.warning("Disease not recognized. Try describing your symptoms.")

# #     # Text Input for Disease
# #     user_input = st.text_input("Enter disease name or message:")

# #     if st.button("Get Ayurvedic Suggestions"):
# #         if user_input:
# #             matched_intent = match_intent(user_input)
# #             if matched_intent:
# #                 st.write("### Chatbot Response:")
# #                 st.write(random.choice(matched_intent["responses"]))

# #                 st.write("### Suggested Medicines & Timings:")
# #                 for suggestion in matched_intent["medicines"]:
# #                     st.write(f"- {suggestion}")

# #                 st.write("### Recommended Duration:")
# #                 st.write(f"{matched_intent['duration']}")
# #             else:
# #                 st.warning("No relevant suggestions found. Please rephrase or upload an image.")
# #         else:
# #             st.warning("Please enter a disease name or upload an image.")

# # if __name__ == "__main__":
# #     main()

# import streamlit as st
# import os
# import random
# from PIL import Image

# def load_ayurvedic_data():
#     return {
#         'skin_rashes': ['Neem Paste - Morning', 'Aloe Vera Gel - Night'],
#         'vomiting': ['Ginger Juice - Morning', 'Lemon Water - After Meals'],
#         'pimples': ['Turmeric Paste - Evening', 'Neem Capsules - Morning'],
#         'headache': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep']
#     }

# def recognize_disease_from_filename(filename):
#     filename = os.path.splitext(filename)[0].lower()
#     known_diseases = ['skin_rashes', 'vomiting', 'pimples', 'headache']
    
#     for disease in known_diseases:
#         if disease in filename:
#             return disease
#     return 'unknown'

# def get_medicine_suggestions(disease, ayurvedic_data):
#     return ayurvedic_data.get(disease, ["No specific medicine found. Please consult an Ayurvedic doctor."])

# # Intent-based chatbot responses
# intents = [
#   {"tag": "cold", "patterns": ["I have a cold"], "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
#   {"tag": "cough", "patterns": ["I have a cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}}
# ]

# def match_intent(user_input):
#     for intent in intents:
#         for pattern in intent["patterns"]:
#             if pattern.lower() in user_input.lower():
#                 return intent
#     return None

# def main():
#     st.title("Arvedic Chat Bot")
#     st.write("Upload images or type a disease to get Ayurvedic medicine suggestions.")

#     ayurvedic_data = load_ayurvedic_data()

#     # Image Upload and Analysis
#     uploaded_file = st.file_uploader("Upload an image (for disease detection)", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Image", use_column_width=True)
        
#         # Recognize disease from filename
#         disease = recognize_disease_from_filename(uploaded_file.name)
#         st.write(f"Detected Disease: {disease.replace('_', ' ').title()}")

#         # Provide medicine suggestions if disease is identified
#         if disease != 'unknown':
#             suggestions = get_medicine_suggestions(disease, ayurvedic_data)
#             st.write("### Suggested Medicines & Timings:")
#             for suggestion in suggestions:
#                 st.write(f"- {suggestion}")
#         else:
#             st.warning("Disease not recognized. Try describing your symptoms.")

#     # Text Input for Disease
#     user_input = st.text_input("Enter disease name or message:")

#     if st.button("Get Ayurvedic Suggestions"):
#         if user_input:
#             matched_intent = match_intent(user_input)
#             if matched_intent:
#                 st.write("### Chatbot Response:")
#                 st.write(random.choice(matched_intent["responses"]))

#                 st.write("### Suggested Medicines & Timings:")
#                 for suggestion in matched_intent["medicines"]:
#                     st.write(f"- {suggestion}")

#                 st.write("### Recommended Duration:")
#                 st.write(f"{matched_intent['duration']}")

#                 # Display hospital information
#                 st.write("### Recommended Hospitals:")
#                 if "hospital" in matched_intent:
#                     for hospital in matched_intent["hospital"]["mysore"]:
#                         st.write(f"- **{hospital['name']}**: Contact {hospital['contact']}")
#             else:
#                 st.warning("No relevant suggestions found. Please rephrase or upload an image.")
#         else:
#             st.warning("Please enter a disease name or upload an image.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import os
import random
from PIL import Image

def load_ayurvedic_data():
    return {
        'skin_rashes': ['Neem Paste - Morning', 'Aloe Vera Gel - Night'],
        'vomiting': ['Ginger Juice - Morning', 'Lemon Water - After Meals'],
        'pimples': ['Turmeric Paste - Evening', 'Neem Capsules - Morning'],
        'headache': ['Peppermint Oil Massage - Evening', 'Ashwagandha - Before Sleep'],
        'cold': ['Tulsi Tea - Morning & Evening', 'Chyawanprash - Before Bed']
    }

def recognize_disease_from_filename(filename):
    filename = os.path.splitext(filename)[0].lower()
    known_diseases = ['skin_rashes', 'vomiting', 'pimples', 'headache','cold']
    
    for disease in known_diseases:
        if disease in filename:
            return disease
    return 'unknown'

def get_medicine_suggestions(disease, ayurvedic_data):
    return ayurvedic_data.get(disease, ["No specific medicine found. Please consult an Ayurvedic doctor."])

# Intent-based chatbot responses
intents = [
  {"tag": "cold", "patterns": ["I have a cold"], "responses": ["For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
  {"tag": "cough", "patterns": ["I have a cough"], "responses": ["For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
    {"tag": "fever", "patterns": ["I have a fever"], "responses": ["Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "headache", "patterns": ["My head hurts"], "responses": ["Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
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
   {"tag": "piles", "patterns": ["I have piles"], "responses": ["Triphala and aloe vera juice help relieve piles symptoms."], "medicines": ["Triphala - Night", "Aloe Vera Juice - Morning"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "heart_pain", "patterns": ["I have heart pain"], "responses": ["Arjuna bark and garlic help support heart health and reduce chest discomfort."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "leg_pain", "patterns": ["I have leg pain"], "responses": ["Ashwagandha and massage with sesame oil can help relieve leg pain."], "medicines": ["Ashwagandha - Evening", "Sesame Oil Massage - Night"], "duration": "2-3 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "vomiting", "patterns": ["I am vomiting"], "responses": ["Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "muscle_cramp", "patterns": ["I have muscle cramps"], "responses": ["Magnesium supplements and coconut water are effective in relieving muscle cramps."], "medicines": ["Magnesium Supplement - Morning", "Coconut Water - Afternoon"], "duration": "3-5 days (or as needed)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "GERD", "patterns": ["I have GERD"], "responses": ["For GERD, try licorice root tea and avoid spicy foods."], "medicines": ["Licorice Root Tea - Morning", "Aloe Vera Juice - Before Meals"], "duration": "15-30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Jaundice", "patterns": ["I have jaundice"], "responses": ["Sugarcane juice and Kutki herb are beneficial for liver detox."], "medicines": ["Sugarcane Juice - Morning", "Kutki Powder - Evening"], "duration": "7-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Malaria", "patterns": ["I have malaria"], "responses": ["Neem leaves and Papaya leaf extract help in malaria recovery."], "medicines": ["Neem Leaves - Morning", "Papaya Leaf Extract - Night"], "duration": "10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Chicken_pox", "patterns": ["I have chicken pox"], "responses": ["Neem bath and Tulsi tea can help soothe chicken pox symptoms."], "medicines": ["Neem Bath - Daily", "Tulsi Tea - Morning"], "duration": "7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Dengue", "patterns": ["I have dengue"], "responses": ["Papaya leaf juice and Giloy help boost platelet count in dengue."], "medicines": ["Papaya Leaf Juice - Morning", "Giloy Juice - Night"], "duration": "10-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Typhoid", "patterns": ["I have typhoid"], "responses": ["Cloves and pomegranate juice aid in typhoid recovery."], "medicines": ["Clove Tea - Morning", "Pomegranate Juice - Afternoon"], "duration": "10-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Hepatitis", "patterns": ["I have hepatitis"], "responses": ["Bhumyamalaki and Amla juice help in liver function recovery."], "medicines": ["Bhumyamalaki Powder - Morning", "Amla Juice - Night"], "duration": "30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Tuberculosis", "patterns": ["I have tuberculosis"], "responses": ["Ashwagandha and black pepper can help strengthen immunity."], "medicines": ["Ashwagandha - Morning", "Black Pepper Tea - Evening"], "duration": "45-60 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Pneumonia", "patterns": ["I have pneumonia"], "responses": ["Turmeric and ginger tea can help with pneumonia symptoms."], "medicines": ["Turmeric Milk - Night", "Ginger Tea - Morning"], "duration": "14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Hypothyroidism", "patterns": ["I have hypothyroidism"], "responses": ["Ashwagandha and coconut oil help regulate thyroid function."], "medicines": ["Ashwagandha - Morning", "Coconut Oil - Before Meals"], "duration": "60 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Hyperthyroidism", "patterns": ["I have hyperthyroidism"], "responses": ["Bugleweed herb and lemon balm tea can help manage hyperthyroidism."], "medicines": ["Bugleweed Tea - Morning", "Lemon Balm Tea - Evening"], "duration": "45 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Hypoglycemia", "patterns": ["I have hypoglycemia"], "responses": ["Bael fruit and jaggery water help maintain blood sugar levels."], "medicines": ["Bael Juice - Morning", "Jaggery Water - Afternoon"], "duration": "15-30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Osteoarthritis", "patterns": ["I have osteoarthritis"], "responses": ["Shallaki and Moringa are good for joint health."], "medicines": ["Shallaki - Morning", "Moringa Powder - Night"], "duration": "90 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Acne", "patterns": ["I have acne"], "responses": ["Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Urinary_Tract_Infection", "patterns": ["I have UTI"], "responses": ["Cranberry juice and coriander water help with urinary tract infections."], "medicines": ["Cranberry Juice - Morning", "Coriander Water - Night"], "duration": "10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Psoriasis", "patterns": ["I have psoriasis"], "responses": ["Aloe vera gel and turmeric help relieve psoriasis symptoms."], "medicines": ["Aloe Vera Gel - Night", "Turmeric Milk - Morning"], "duration": "60 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}},
   {"tag": "Impetigo", "patterns": ["I have impetigo"], "responses": ["Tea tree oil and neem paste can help treat impetigo."], "medicines": ["Tea Tree Oil - Night", "Neem Paste - Morning"], "duration": "14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321"}, {"name": "Mysore Ayurvedic Wellness", "contact": "0821-789123"}, {"name": "Sri Ayurveda Hospital", "contact": "0821-321987"}]}}

  #Add more from last formate 
]

def match_intent(user_input):
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input.lower():
                return intent
    return None

def main():
    st.title("Airvedic Chat Bot")
    st.write("Upload images or type a disease to get Ayurvedic medicine suggestions.")

    ayurvedic_data = load_ayurvedic_data()

    # Image Upload and Analysis
    uploaded_file = st.file_uploader("Upload an image (for disease detection)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Recognize disease from filename
        disease = recognize_disease_from_filename(uploaded_file.name)
        st.write(f"Detected Disease: {disease.replace('_', ' ').title()}")

        # Provide medicine suggestions if disease is identified
        if disease != 'unknown':
            suggestions = get_medicine_suggestions(disease, ayurvedic_data)
            st.write("### Suggested Medicines & Timings:")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.warning("Disease not recognized. Try describing your symptoms.")

    # Text Input for Disease
    user_input = st.text_input("Enter disease name or message:")

    if st.button("Get Ayurvedic Suggestions"):
        if user_input:
            matched_intent = match_intent(user_input)
            if matched_intent:
                st.write("### Chatbot Response:")
                st.write(random.choice(matched_intent["responses"]))

                st.write("### Suggested Medicines & Timings:")
                for suggestion in matched_intent["medicines"]:
                    st.write(f"- {suggestion}")

                st.write("### Recommended Duration:")
                st.write(f"{matched_intent['duration']}")

                # Display hospital information
                st.write("### Recommended Hospitals:")
                if "hospital" in matched_intent:
                    for hospital in matched_intent["hospital"]["mysore"]:
                        st.write(f"- **{hospital['name']}**: Contact {hospital['contact']}")
            else:
                st.warning("No relevant suggestions found. Please rephrase or upload an image.")
        else:
            st.warning("Please enter a disease name or upload an image.")

if __name__ == "__main__":
    main()
