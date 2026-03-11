import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os
import random
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="Airvedic Chatbot: AI Based Symptom Analysis and Ayurvedic Treatment Suggestions",
    page_icon="🌿",
    layout="wide"
)

# Complete intents from cha2.py - ALL 30+ conditions
intents = [
    {"tag": "cold", "patterns": ["I have a cold", "I have cold", "feeling cold", "cold symptoms", "runny nose", "sneezing", "cold"], "responses": ["I understand you have cold symptoms. For cold, try Tulsi and Ginger tea, and inhale steam with eucalyptus oil."], "medicines": ["Tulsi Tea - Morning & Evening", "Chyawanprash - Before Bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "JSS Ayurveda Hospital", "contact": "0821-2548231", "address": "41/E, Lalithadripura Road, Mysore - 570028", "maps_link": "https://maps.google.com/?q=JSS+Ayurveda+Hospital+Lalithadripura+Road+Mysore"}, {"name": "Sriranga Ayurveda Chikitsa Mandir", "contact": "0821-2345678", "address": "#3394, Near Netaji Circle, 3rd Stage, Dattagalli, Mysore - 570023", "maps_link": "https://maps.google.com/?q=Sriranga+Ayurveda+Chikitsa+Mandir+Dattagalli+Mysore"}]}},
    {"tag": "cough", "patterns": ["I have a cough", "I have cough", "coughing", "cough", "throat irritation"], "responses": ["Let me help with your cough. For cough, consume ginger honey and mulethi for throat relief."], "medicines": ["Ginger Honey - Morning", "Mulethi - After Lunch"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "JSS Ayurveda Hospital", "contact": "0821-2548231", "address": "41/E, Lalithadripura Road, Mysore - 570028", "maps_link": "https://maps.google.com/?q=JSS+Ayurveda+Hospital+Lalithadripura+Road+Mysore"}, {"name": "Mayukha Ayurveda", "contact": "0821-2567890", "address": "#767, 3rd Cross Road, 3rd Stage, Gokulam, Mysuru - 570002", "maps_link": "https://maps.google.com/?q=Mayukha+Ayurveda+Gokulam+3rd+Stage+Mysore"}]}},
    {"tag": "fever", "patterns": ["I have a fever", "I have fever", "fever", "high temperature", "feeling hot"], "responses": ["Fever can be concerning. Giloy juice is beneficial for reducing fever and boosting immunity."], "medicines": ["Giloy Juice - Morning", "Turmeric Milk - Night"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "JSS Ayurveda Hospital", "contact": "0821-2548231", "address": "41/E, Lalithadripura Road, Mysore - 570028", "maps_link": "https://maps.google.com/?q=JSS+Ayurveda+Hospital+Lalithadripura+Road+Mysore"}, {"name": "Govt. Ayurveda Medical College", "contact": "0821-2423456", "address": "New Sayyaji Rao Road, Near Vishvesvaraya Circle, Mysuru - 570001", "maps_link": "https://maps.google.com/?q=Government+Ayurveda+Medical+College+Mysore"}]}},
    {"tag": "headache", "patterns": ["My head hurts", "I have a headache", "I have headache", "headache", "head pain", "migraine"], "responses": ["I understand you're experiencing head pain. Applying peppermint oil to your temples and staying hydrated may help relieve headaches naturally."], "medicines": ["Brahmi Oil Massage - Evening", "Ashwagandha - Before Sleep"], "duration": "As needed or 3-5 days if frequent", "hospital": {"mysore": [{"name": "Suryavedam Ayur Wellness", "contact": "0821-2678901", "address": "#50, Seebinivas, 4th Main, Maruthi Temple Road, Kuvempunagar, Mysuru - 570009", "maps_link": "https://maps.google.com/?q=Suryavedam+Ayur+Wellness+Kuvempunagar+Mysore"}, {"name": "JSS Ayurveda Hospital", "contact": "0821-2548231", "address": "41/E, Lalithadripura Road, Mysore - 570028", "maps_link": "https://maps.google.com/?q=JSS+Ayurveda+Hospital+Lalithadripura+Road+Mysore"}]}},
    {"tag": "acidity", "patterns": ["I have acidity", "acidity", "acid reflux", "heartburn", "stomach burning"], "responses": ["Acidity can be uncomfortable. Amla juice and jeera water can help to reduce acidity."], "medicines": ["Amla Juice - Morning", "Jeera Water - After Meals"], "duration": "7-10 days", "hospital": {"mysore": [{"name": "Indus Valley Ayurvedic Centre", "contact": "0821-2789012", "address": "Lalitadripura Rd, Chamundi Hill, Mysuru - 570028", "maps_link": "https://maps.google.com/?q=Indus+Valley+Ayurvedic+Centre+Chamundi+Hill+Mysore"}, {"name": "Kotian Ayurveda", "contact": "0821-2890123", "address": "18th Cross, Aravinda Nagara, Kuvempunagar, Mysore - 570023", "maps_link": "https://maps.google.com/?q=Kotian+Ayurveda+Aravinda+Nagara+Kuvempunagar+Mysore"}]}},
    {"tag": "indigestion", "patterns": ["I have indigestion", "indigestion", "stomach upset", "digestion problem"], "responses": ["Digestion issues need attention. Consume ajwain water to relieve indigestion symptoms."], "medicines": ["Ajwain Water - After Meals"], "duration": "3-5 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "constipation", "patterns": ["I am constipated", "I have constipation", "constipation", "bowel problem"], "responses": ["Constipation is common. Triphala powder helps to improve digestion and relieve constipation."], "medicines": ["Triphala Powder - Before Bed"], "duration": "7-14 days (or as needed)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "insomnia", "patterns": ["I have trouble sleeping", "I have insomnia", "can't sleep", "insomnia", "sleeplessness"], "responses": ["Sleep issues affect many people. Ashwagandha and warm milk can promote better sleep."], "medicines": ["Ashwagandha - Evening", "Warm Milk - Before Bed"], "duration": "10-14 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "stress", "patterns": ["I feel stressed", "I have stress", "stress", "anxiety", "worried", "tension"], "responses": ["Stress is very common today. Brahmi and meditation are helpful for stress management."], "medicines": ["Brahmi - Morning", "Shankhpushpi - Night"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "skin_allergy", "patterns": ["I have a skin allergy", "skin rash", "itchy skin"], "responses": ["Skin allergies can be frustrating. Neem and turmeric help to cleanse the blood and alleviate skin allergies."], "medicines": ["Neem Capsules - Morning", "Turmeric Water - Night"], "duration": "2-3 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "hair_fall", "patterns": ["I have hair fall", "hair loss", "balding"], "responses": ["Hair fall is a common concern. Bhringraj oil helps strengthen hair roots and prevent hair fall."], "medicines": ["Bhringraj Oil - Night", "Amla Juice - Morning"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "joint_pain", "patterns": ["I have joint pain", "arthritis", "knee pain"], "responses": ["Joint pain can limit mobility. Shallaki and turmeric are effective in reducing joint pain and inflammation."], "medicines": ["Shallaki - Morning", "Turmeric Capsules - Night"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "diabetes", "patterns": ["I have diabetes", "diabetes", "blood sugar", "high glucose"], "responses": ["Diabetes management is crucial. Karela and Jamun juice can help manage blood sugar levels."], "medicines": ["Karela Juice - Morning", "Jamun Juice - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "hypertension", "patterns": ["I have high blood pressure", "hypertension", "BP problem"], "responses": ["High blood pressure needs monitoring. Arjuna bark and garlic are known to support healthy blood pressure levels."], "medicines": ["Arjuna Capsules - Morning", "Garlic Extract - Evening"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "asthma", "patterns": ["I have asthma", "asthma", "breathing problem", "wheezing"], "responses": ["Breathing issues need care. Tulsi and mulethi help relieve asthma symptoms and clear airways."], "medicines": ["Tulsi Capsules - Morning", "Mulethi Powder - Night"], "duration": "Ongoing (consult doctor)", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "acne", "patterns": ["I have acne", "pimples", "skin breakout"], "responses": ["Acne affects confidence. Neem and turmeric paste can help treat acne naturally."], "medicines": ["Neem Paste - Night", "Turmeric Capsules - Morning"], "duration": "30 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "vomiting", "patterns": ["I am vomiting", "I have vomiting", "vomiting", "vomit", "nausea", "feeling sick", "throwing up"], "responses": ["Nausea is uncomfortable. Ginger and lemon juice can soothe the stomach and reduce nausea."], "medicines": ["Ginger Juice - Morning", "Lemon Water - After Meals"], "duration": "2-3 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "chickenpox", "patterns": ["I have chickenpox", "chickenpox", "chicken pox", "varicella"], "responses": ["Chickenpox is a viral infection. Neem leaves and turmeric help reduce itching and promote healing."], "medicines": ["Neem Paste - Apply on affected areas", "Turmeric Milk - Evening"], "duration": "7-10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Sri Dhanvantri Clinic", "contact": "0821-654321", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Sri+Dhanvantri+Clinic+Mysore"}]}},
    {"tag": "carcinoma", "patterns": ["I have carcinoma", "carcinoma", "skin cancer"], "responses": ["This is a serious condition requiring immediate medical attention. Please consult an oncologist immediately."], "medicines": ["Consult Doctor Immediately"], "duration": "Requires medical treatment", "hospital": {"mysore": [{"name": "Kidwai Memorial Institute", "contact": "080-26560000", "address": "Bangalore (Referral Hospital)", "maps_link": "https://maps.google.com/?q=Kidwai+Memorial+Institute+Bangalore"}, {"name": "Apollo Hospital", "contact": "0821-256789", "address": "Mysore", "maps_link": "https://maps.google.com/?q=Apollo+Hospital+Mysore"}]}},
    {"tag": "cataract", "patterns": ["I have cataract", "cataract", "cloudy vision", "blurred vision"], "responses": ["Cataracts affect vision clarity. Triphala eye wash and proper nutrition can help slow progression."], "medicines": ["Triphala Eye Wash - Morning & Evening", "Amla Juice - Daily"], "duration": "Ongoing (may need surgery)", "hospital": {"mysore": [{"name": "Narayana Nethralaya", "contact": "0821-234567", "address": "Mysore Eye Specialist Center", "maps_link": "https://maps.google.com/?q=Narayana+Nethralaya+Mysore"}, {"name": "Eye Care Hospital", "contact": "0821-345678", "address": "Mysore Eye Care Center", "maps_link": "https://maps.google.com/?q=Eye+Care+Hospital+Mysore"}]}},
    {"tag": "conjunctivitis", "patterns": ["I have conjunctivitis", "conjunctivitis", "pink eye", "eye infection"], "responses": ["Conjunctivitis is an eye infection. Rose water and honey drops can provide relief."], "medicines": ["Rose Water - Eye drops 3 times daily", "Honey Drops - Before bed"], "duration": "5-7 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Eye Care Clinic", "contact": "0821-567890", "address": "Mysore Eye Care Clinic", "maps_link": "https://maps.google.com/?q=Eye+Care+Clinic+Mysore"}]}},
    {"tag": "eczema", "patterns": ["I have eczema", "eczema", "atopic dermatitis", "dry itchy skin"], "responses": ["Eczema causes dry, itchy skin. Coconut oil and neem help moisturize and heal the skin."], "medicines": ["Coconut Oil - Apply twice daily", "Neem Capsules - Morning"], "duration": "2-4 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Skin Care Clinic", "contact": "0821-678901", "address": "Mysore Skin Care Center", "maps_link": "https://maps.google.com/?q=Skin+Care+Clinic+Mysore"}]}},
    {"tag": "keratosis", "patterns": ["I have keratosis", "keratosis", "rough skin patches"], "responses": ["Keratosis causes rough skin patches. Aloe vera and turmeric can help smooth the skin."], "medicines": ["Aloe Vera Gel - Apply daily", "Turmeric Paste - Evening"], "duration": "3-4 weeks", "hospital": {"mysore": [{"name": "Dermatology Center", "contact": "0821-789012", "address": "Mysore Dermatology Clinic", "maps_link": "https://maps.google.com/?q=Dermatology+Center+Mysore"}, {"name": "Skin Specialist Clinic", "contact": "0821-890123", "address": "Mysore Skin Specialist Center", "maps_link": "https://maps.google.com/?q=Skin+Specialist+Clinic+Mysore"}]}},
    {"tag": "milia", "patterns": ["I have milia", "milia", "white bumps", "milk spots"], "responses": ["Milia are small white bumps. Gentle exfoliation with oatmeal and honey can help."], "medicines": ["Oatmeal Scrub - Twice weekly", "Honey Mask - Weekly"], "duration": "2-3 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Cosmetic Dermatology", "contact": "0821-901234", "address": "Mysore Cosmetic Dermatology Center", "maps_link": "https://maps.google.com/?q=Cosmetic+Dermatology+Mysore"}]}},
    {"tag": "rosacea", "patterns": ["I have rosacea", "rosacea", "facial redness", "red face"], "responses": ["Rosacea causes facial redness. Cucumber and aloe vera can soothe inflamed skin."], "medicines": ["Cucumber Juice - Apply daily", "Aloe Vera Gel - Morning & Evening"], "duration": "4-6 weeks", "hospital": {"mysore": [{"name": "Skin Care Center", "contact": "0821-012345", "address": "Mysore Skin Care Center", "maps_link": "https://maps.google.com/?q=Skin+Care+Center+Mysore"}, {"name": "Dermatology Clinic", "contact": "0821-123450", "address": "Mysore Dermatology Clinic", "maps_link": "https://maps.google.com/?q=Dermatology+Clinic+Mysore"}]}},
    {"tag": "psoriasis", "patterns": ["I have psoriasis", "psoriasis", "scaly skin", "red patches"], "responses": ["Psoriasis causes scaly red patches. Turmeric and coconut oil help reduce inflammation."], "medicines": ["Turmeric Paste - Daily application", "Coconut Oil - Massage twice daily"], "duration": "6-8 weeks", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Psoriasis Treatment Center", "contact": "0821-234561", "address": "Mysore Psoriasis Treatment Center", "maps_link": "https://maps.google.com/?q=Psoriasis+Treatment+Center+Mysore"}]}},
    {"tag": "impetigo", "patterns": ["I have impetigo", "impetigo", "bacterial skin infection", "crusty sores"], "responses": ["Impetigo is a bacterial skin infection. Neem and turmeric have antibacterial properties."], "medicines": ["Neem Oil - Apply on affected areas", "Turmeric Paste - Twice daily"], "duration": "7-10 days", "hospital": {"mysore": [{"name": "Ayurveda Healing Center", "contact": "0821-123456", "address": "Mysore General Area", "maps_link": "https://maps.google.com/?q=Ayurveda+Healing+Center+Mysore"}, {"name": "Infection Control Clinic", "contact": "0821-345672", "address": "Mysore Infection Control Center", "maps_link": "https://maps.google.com/?q=Infection+Control+Clinic+Mysore"}]}}
]

# Dataset classes matching your folders
DATASET_CLASSES = [
    'Acne', 'Carcinoma', 'Cataract', 'Chickenpox', 'Conjunctivitis', 
    'Eczema', 'Keratosis', 'Milia', 'Rosacea', 'Eyelid', 'Moles', 
    'Psoriasis', 'Impetigo'
]

# Comprehensive Medicine Database with descriptions and images
MEDICINE_DATABASE = {
    "Tulsi Tea": {
        "description": "Holy Basil tea is a powerful adaptogen that boosts immunity, reduces stress, and helps fight respiratory infections. Rich in antioxidants and has antimicrobial properties.",
        "benefits": ["Boosts immunity", "Reduces cold symptoms", "Anti-inflammatory", "Stress relief"],
        "preparation": "Boil fresh tulsi leaves in water for 5-10 minutes. Add honey if desired."
    },
    "Chyawanprash": {
        "description": "A traditional Ayurvedic herbal jam made with amla and over 40 herbs. Excellent for building immunity, improving digestion, and providing energy.",
        "benefits": ["Immunity booster", "Rich in Vitamin C", "Improves digestion", "Anti-aging properties"],
        "preparation": "Take 1-2 teaspoons with warm milk or water"
    },
    "Ginger Honey": {
        "description": "A natural combination that soothes throat irritation, reduces cough, and has antimicrobial properties. Ginger aids digestion while honey provides antibacterial benefits.",
        "benefits": ["Soothes throat", "Reduces cough", "Antimicrobial", "Aids digestion"],
        "preparation": "Mix fresh ginger juice with pure honey in 1:1 ratio"
    },
    "Mulethi": {
        "description": "Licorice root is excellent for respiratory health, soothes throat inflammation, and helps with cough relief. Has natural expectorant properties.",
        "benefits": ["Throat soother", "Expectorant", "Anti-inflammatory", "Respiratory health"],
        "preparation": "Chew small piece or make powder and mix with honey"
    },
    "Giloy Juice": {
        "description": "Tinospora cordifolia is known as 'Amrita' in Ayurveda. Powerful immunity booster, helps reduce fever, and has anti-inflammatory properties.",
        "benefits": ["Fever reducer", "Immunity booster", "Anti-inflammatory", "Detoxifies body"],
        "preparation": "Take 15-30ml fresh juice on empty stomach"
    },
    "Turmeric Milk": {
        "description": "Golden milk with turmeric has powerful anti-inflammatory and antimicrobial properties. Helps with healing, immunity, and better sleep.",
        "benefits": ["Anti-inflammatory", "Immunity booster", "Better sleep", "Healing properties"],
        "preparation": "Add 1/2 tsp turmeric powder to warm milk with a pinch of black pepper"
    },
    "Brahmi Oil Massage": {
        "description": "Brahmi oil is excellent for head massage, reduces stress, improves circulation, and helps with headaches and mental clarity.",
        "benefits": ["Reduces headaches", "Stress relief", "Improves circulation", "Mental clarity"],
        "preparation": "Gently massage on scalp and temples in circular motions"
    },
    "Ashwagandha": {
        "description": "Winter cherry is a powerful adaptogen that reduces stress, improves sleep quality, and boosts energy levels. Helps with anxiety and fatigue.",
        "benefits": ["Stress reducer", "Better sleep", "Energy booster", "Anxiety relief"],
        "preparation": "Take 300-500mg powder with warm milk before bed"
    },
    "Amla Juice": {
        "description": "Indian gooseberry is the richest source of Vitamin C. Excellent for immunity, digestion, hair health, and overall vitality.",
        "benefits": ["Rich in Vitamin C", "Immunity booster", "Hair health", "Digestive aid"],
        "preparation": "Take 15-30ml fresh juice on empty stomach"
    },
    "Jeera Water": {
        "description": "Cumin water aids digestion, reduces acidity, and helps with bloating. Has carminative properties and improves metabolism.",
        "benefits": ["Aids digestion", "Reduces acidity", "Improves metabolism", "Reduces bloating"],
        "preparation": "Soak 1 tsp cumin seeds overnight, strain and drink in morning"
    },
    "Ajwain Water": {
        "description": "Carom seeds water is excellent for digestive issues, reduces gas, and helps with indigestion. Has antimicrobial properties.",
        "benefits": ["Digestive aid", "Reduces gas", "Antimicrobial", "Relieves indigestion"],
        "preparation": "Boil 1 tsp ajwain in water, strain and drink warm"
    },
    "Triphala Powder": {
        "description": "A combination of three fruits (Amalaki, Bibhitaki, Haritaki) that promotes digestive health, detoxification, and regular bowel movements.",
        "benefits": ["Digestive health", "Detoxification", "Laxative", "Antioxidant"],
        "preparation": "Mix 1/2 tsp powder in warm water before bed"
    },
    "Warm Milk": {
        "description": "Warm milk with natural herbs promotes better sleep, provides calcium, and has a calming effect on the nervous system.",
        "benefits": ["Better sleep", "Calcium source", "Calming effect", "Muscle relaxation"],
        "preparation": "Heat milk gently, add a pinch of nutmeg or cardamom"
    },
    "Brahmi": {
        "description": "Bacopa monnieri enhances memory, reduces anxiety, and improves cognitive function. Known as a brain tonic in Ayurveda.",
        "benefits": ["Memory enhancer", "Reduces anxiety", "Cognitive function", "Brain tonic"],
        "preparation": "Take 300mg powder with ghee or honey"
    },
    "Shankhpushpi": {
        "description": "Convolvulus pluricaulis is excellent for mental health, reduces stress, and improves sleep quality. Natural brain tonic.",
        "benefits": ["Mental health", "Stress reducer", "Better sleep", "Brain tonic"],
        "preparation": "Take 1-2 tsp powder with milk before bed"
    },
    "Neem Capsules": {
        "description": "Neem has powerful antibacterial, antifungal, and blood purifying properties. Excellent for skin health and immunity.",
        "benefits": ["Blood purifier", "Antibacterial", "Skin health", "Immunity booster"],
        "preparation": "Take 1-2 capsules with water after meals"
    },
    "Turmeric Water": {
        "description": "Turmeric water has anti-inflammatory and antioxidant properties. Helps with skin health and overall immunity.",
        "benefits": ["Anti-inflammatory", "Antioxidant", "Skin health", "Immunity"],
        "preparation": "Mix 1/2 tsp turmeric in warm water with honey"
    },
    "Bhringraj Oil": {
        "description": "Eclipta alba oil is the king of hair oils. Prevents hair fall, promotes hair growth, and nourishes the scalp.",
        "benefits": ["Prevents hair fall", "Hair growth", "Scalp nourishment", "Premature graying"],
        "preparation": "Massage gently on scalp, leave overnight, wash in morning"
    },
    "Shallaki": {
        "description": "Boswellia serrata is excellent for joint health, reduces inflammation, and helps with arthritis pain.",
        "benefits": ["Joint health", "Anti-inflammatory", "Arthritis relief", "Pain reducer"],
        "preparation": "Take 300-400mg capsules with meals"
    },
    "Turmeric Capsules": {
        "description": "Concentrated turmeric with curcumin provides powerful anti-inflammatory benefits and supports joint health.",
        "benefits": ["Anti-inflammatory", "Joint support", "Antioxidant", "Pain relief"],
        "preparation": "Take 1-2 capsules with meals and black pepper"
    },
    "Karela Juice": {
        "description": "Bitter gourd juice helps regulate blood sugar levels, improves insulin sensitivity, and supports diabetes management.",
        "benefits": ["Blood sugar control", "Insulin sensitivity", "Diabetes support", "Liver health"],
        "preparation": "Take 30ml fresh juice on empty stomach"
    },
    "Jamun Juice": {
        "description": "Black plum juice is excellent for diabetes management, helps control blood sugar, and supports pancreatic health.",
        "benefits": ["Diabetes control", "Blood sugar regulation", "Pancreatic health", "Antioxidant"],
        "preparation": "Take 15-30ml juice twice daily before meals"
    },
    "Arjuna Capsules": {
        "description": "Terminalia arjuna supports heart health, helps regulate blood pressure, and strengthens cardiac muscles.",
        "benefits": ["Heart health", "Blood pressure control", "Cardiac strength", "Cholesterol management"],
        "preparation": "Take 1-2 capsules twice daily with water"
    },
    "Garlic Extract": {
        "description": "Garlic extract helps lower blood pressure, supports cardiovascular health, and has antimicrobial properties.",
        "benefits": ["Blood pressure control", "Heart health", "Antimicrobial", "Cholesterol reduction"],
        "preparation": "Take 1 capsule with meals or as directed"
    },
    "Tulsi Capsules": {
        "description": "Holy basil capsules provide concentrated adaptogenic benefits, support respiratory health, and boost immunity.",
        "benefits": ["Respiratory health", "Immunity booster", "Stress relief", "Adaptogenic"],
        "preparation": "Take 1-2 capsules twice daily with water"
    },
    "Mulethi Powder": {
        "description": "Licorice root powder soothes respiratory passages, reduces cough, and has anti-inflammatory properties.",
        "benefits": ["Respiratory health", "Cough relief", "Anti-inflammatory", "Throat soother"],
        "preparation": "Mix 1/2 tsp powder with honey before bed"
    },
    "Neem Paste": {
        "description": "Fresh neem paste has powerful antibacterial and antifungal properties, excellent for treating skin conditions naturally.",
        "benefits": ["Antibacterial", "Antifungal", "Skin healing", "Acne treatment"],
        "preparation": "Apply fresh neem paste on affected areas, wash after 20 minutes"
    },
    "Ginger Juice": {
        "description": "Fresh ginger juice aids digestion, reduces nausea, and has anti-inflammatory properties. Natural remedy for stomach issues.",
        "benefits": ["Digestive aid", "Reduces nausea", "Anti-inflammatory", "Stomach soother"],
        "preparation": "Take 1 tsp fresh ginger juice with honey"
    },
    "Lemon Water": {
        "description": "Lemon water provides Vitamin C, aids digestion, helps with nausea, and supports detoxification.",
        "benefits": ["Vitamin C source", "Digestive aid", "Nausea relief", "Detoxification"],
        "preparation": "Mix fresh lemon juice in warm water with a pinch of salt"
    },
    "Triphala Eye Wash": {
        "description": "Triphala eye wash helps with eye health, reduces inflammation, and may help slow cataract progression naturally.",
        "benefits": ["Eye health", "Reduces inflammation", "Vision support", "Natural cleanser"],
        "preparation": "Soak triphala overnight, strain and use as eye wash"
    },
    "Rose Water": {
        "description": "Pure rose water has cooling and anti-inflammatory properties, excellent for eye infections and skin care.",
        "benefits": ["Cooling effect", "Anti-inflammatory", "Eye care", "Skin soother"],
        "preparation": "Use pure rose water as eye drops 2-3 times daily"
    },
    "Honey Drops": {
        "description": "Pure honey has antimicrobial properties and helps with eye infections when used as drops in diluted form.",
        "benefits": ["Antimicrobial", "Eye infection relief", "Natural healer", "Soothing"],
        "preparation": "Dilute 1 drop honey in 10 drops clean water"
    },
    "Coconut Oil": {
        "description": "Virgin coconut oil moisturizes skin, has antimicrobial properties, and helps heal dry and irritated skin conditions.",
        "benefits": ["Skin moisturizer", "Antimicrobial", "Healing properties", "Natural emollient"],
        "preparation": "Apply virgin coconut oil gently on affected areas"
    },
    "Aloe Vera Gel": {
        "description": "Fresh aloe vera gel soothes inflammation, moisturizes skin, and promotes healing of various skin conditions.",
        "benefits": ["Anti-inflammatory", "Skin moisturizer", "Healing properties", "Cooling effect"],
        "preparation": "Apply fresh aloe vera gel directly on affected areas"
    },
    "Turmeric Paste": {
        "description": "Fresh turmeric paste has powerful anti-inflammatory and antimicrobial properties, excellent for skin conditions.",
        "benefits": ["Anti-inflammatory", "Antimicrobial", "Skin healing", "Natural antiseptic"],
        "preparation": "Mix turmeric powder with water or milk to make paste"
    },
    "Oatmeal Scrub": {
        "description": "Gentle oatmeal scrub exfoliates dead skin cells, unclogs pores, and helps with various skin conditions naturally.",
        "benefits": ["Gentle exfoliation", "Pore cleansing", "Skin softening", "Natural cleanser"],
        "preparation": "Mix ground oats with water to make gentle scrub"
    },
    "Honey Mask": {
        "description": "Pure honey mask has antimicrobial and moisturizing properties, helps heal skin and provides natural glow.",
        "benefits": ["Antimicrobial", "Moisturizing", "Skin healing", "Natural glow"],
        "preparation": "Apply raw honey as face mask for 15-20 minutes"
    },
    "Cucumber Juice": {
        "description": "Fresh cucumber juice has cooling and anti-inflammatory properties, excellent for soothing irritated and inflamed skin.",
        "benefits": ["Cooling effect", "Anti-inflammatory", "Skin soother", "Hydrating"],
        "preparation": "Apply fresh cucumber juice with cotton pad on affected areas"
    },
    "Neem Oil": {
        "description": "Pure neem oil has powerful antibacterial and antifungal properties, excellent for treating bacterial skin infections.",
        "benefits": ["Antibacterial", "Antifungal", "Skin infection treatment", "Natural antiseptic"],
        "preparation": "Apply diluted neem oil on affected areas twice daily"
    }
}

class ImageAnalyzer:
    def __init__(self):
        self.model = self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        model_path = "ayurvedic_symptom_model.h5"
        if os.path.exists(model_path):
            try:
                return tf.keras.models.load_model(model_path)
            except:
                return self.create_new_model()
        else:
            return self.create_new_model()
    
    def create_new_model(self):
        """Create a new CNN model for image classification"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(DATASET_CLASSES), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def preprocess_image(self, image):
        """Preprocess image for model prediction"""
        img_array = np.array(image.convert('RGB'))
        img_resized = cv2.resize(img_array, (224, 224))
        img_normalized = img_resized.astype('float32') / 255.0
        return np.expand_dims(img_normalized, axis=0)
    
    def predict_condition(self, image):
        """Predict medical condition from image"""
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_condition = DATASET_CLASSES[predicted_class_idx]
        return predicted_condition, confidence

def enhanced_match_intent(user_input):
    """Enhanced pattern matching for natural conversation"""
    user_input_lower = user_input.lower().strip()
    best_match = None
    best_score = 0
    
    for intent in intents:
        max_intent_score = 0
        
        for pattern in intent["patterns"]:
            pattern_lower = pattern.lower().strip()
            score = 0
            
            # Exact phrase match gets highest priority
            if pattern_lower == user_input_lower:
                score = 1000
            elif pattern_lower in user_input_lower and len(pattern_lower) > 3:
                # Full pattern contained in user input
                score = 500
            else:
                # Word-by-word matching
                pattern_words = pattern_lower.split()
                user_words = user_input_lower.split()
                
                # Count exact word matches
                exact_matches = 0
                total_pattern_words = len(pattern_words)
                
                for pattern_word in pattern_words:
                    if pattern_word in user_words:
                        exact_matches += 1
                
                # Calculate match percentage
                match_percentage = exact_matches / total_pattern_words if total_pattern_words > 0 else 0
                
                # Only consider if we have good word overlap
                if match_percentage >= 0.5:  # At least 50% of pattern words must match
                    # Give higher score for key medical terms
                    key_terms = ['acne', 'fever', 'headache', 'cold', 'cough', 'diabetes', 'asthma']
                    has_key_term = any(term in pattern_lower for term in key_terms)
                    
                    if has_key_term and match_percentage >= 0.8:
                        score = 300 + (exact_matches * 20)
                    elif match_percentage >= 0.8:
                        score = 200 + (exact_matches * 15)
                    else:
                        score = 100 + (exact_matches * 10)
            
            # Keep track of the best score for this intent
            max_intent_score = max(max_intent_score, score)
        
        # Update best match if this intent scored higher
        if max_intent_score > best_score:
            best_score = max_intent_score
            best_match = intent
    
    return best_match if best_score >= 100 else None

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ImageAnalyzer()

def add_to_chat_history(message, sender, intent_data=None):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'message': message,
        'sender': sender,
        'intent_data': intent_data,
        'timestamp': datetime.now().strftime("%H:%M")
    })

def display_chat_history():
    """Display chat history in ChatGPT style"""
    for chat in st.session_state.chat_history[-10:]:
        if chat['sender'] == 'user':
            st.markdown(f"""
            <div style='text-align: right; margin: 10px 0;'>
                <div style='background-color: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;'>
                    {chat['message']}
                </div>
                <div style='font-size: 12px; color: #666; margin-top: 5px;'>You • {chat['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: left; margin: 10px 0;'>
                <div style='background-color: #f1f1f1; color: black; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;'>
                    🌿 {chat['message']}
                </div>
                <div style='font-size: 12px; color: #666; margin-top: 5px;'>Dr. Ayurveda • {chat['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if chat.get('intent_data'):
                intent = chat['intent_data']
                display_treatment_details(intent)

def get_medicine_name(medicine_text):
    """Extract medicine name from medicine text (e.g., 'Tulsi Tea - Morning & Evening' -> 'Tulsi Tea')"""
    return medicine_text.split(' - ')[0].strip()

def display_treatment_details(intent):
    """Display detailed treatment information"""
    st.markdown("---")
    st.subheader(f"🌿 Treatment Details for {intent['tag'].title()}")
    
    # Medicine Details Section
    st.write("**💊 Recommended Medicines:**")
    
    for medicine_text in intent["medicines"]:
        medicine_name = get_medicine_name(medicine_text)
        
        if medicine_name in MEDICINE_DATABASE:
            medicine_info = MEDICINE_DATABASE[medicine_name]
            
            # Create expandable section for each medicine
            with st.expander(f"📋 {medicine_text}", expanded=False):
                st.write(f"**Description:** {medicine_info['description']}")
                st.write("**Benefits:**")
                for benefit in medicine_info['benefits']:
                    st.write(f"• {benefit}")
                st.write(f"**How to prepare:** {medicine_info['preparation']}")
        else:
            # Fallback for medicines not in database
            st.write(f"• {medicine_text}")
    
    # Duration and Hospital Information
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**⏰ Treatment Duration:** {intent['duration']}")
        st.info("💡 **Note:** Always consult with a qualified Ayurvedic practitioner before starting any treatment.")
    
    with col2:
        st.write("**🏥 Recommended Hospitals in Mysore:**")
        for hospital in intent["hospital"]["mysore"]:
            st.write(f"• **{hospital['name']}**")
            st.write(f"  📞 {hospital['contact']}")
            if 'address' in hospital:
                st.write(f"  📍 {hospital['address']}")
            if 'maps_link' in hospital:
                st.markdown(f"  🗺️ [View on Google Maps]({hospital['maps_link']})")
            st.write("")

def main():
    st.title("🌿 Airvedic Chatbot: AI Based Symptom Analysis and Ayurvedic Treatment Suggestions")
    st.markdown("*Your personal AI chatbot for Ayurvedic health consultation with image analysis*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat with Dr. Ayurveda")
        
        # Display chat history
        if st.session_state.chat_history:
            display_chat_history()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 20px; color: #666;'>
                👋 Hello! I'm Dr. Ayurveda, your AI health assistant.<br>
                Tell me how you're feeling or upload an image for analysis.
            </div>
            """, unsafe_allow_html=True)
        
        # Text input (submit with Enter) and auto-clear after submit
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message:", 
                placeholder="e.g., 'I'm feeling cold', 'My head hurts', 'I have acne'...",
                key="user_input"
            )
            submitted = st.form_submit_button("💬 Send", type="primary")
            if submitted and user_input.strip():
                add_to_chat_history(user_input, 'user')
                
                matched_intent = enhanced_match_intent(user_input)
                if matched_intent:
                    response = random.choice(matched_intent["responses"])
                    add_to_chat_history(response, 'bot', matched_intent)
                else:
                    fallback_responses = [
                        "I'd like to help you better. Could you describe your symptoms more specifically?",
                        "Tell me more about what you're experiencing so I can provide the right treatment.",
                        "I'm here to help. Can you be more specific about your health concern?"
                    ]
                    fallback_msg = random.choice(fallback_responses)
                    add_to_chat_history(fallback_msg, 'bot')
                
                st.rerun()
    
    with col2:
        st.subheader("📸 Image Analysis")
        
        uploaded_file = st.file_uploader(
            "Upload medical image:",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected area"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("🤖 AI is analyzing..."):
                    condition, confidence = st.session_state.analyzer.predict_condition(image)
                    
                    if confidence >= 0.75:
                        analysis_msg = f"Image analysis shows: {condition} (confidence: {confidence:.1%})"
                        add_to_chat_history(analysis_msg, 'bot')
                        
                        # Try to match with intents
                        matched_intent = enhanced_match_intent(condition.lower())
                        if matched_intent:
                            response = f"Based on the image analysis, {random.choice(matched_intent['responses'])}"
                            add_to_chat_history(response, 'bot', matched_intent)
                        
                        st.success(f"✅ Detected: {condition}")
                        st.progress(confidence)
                    else:
                        low_conf_msg = f"Image analysis uncertain (confidence: {confidence:.1%}). Please upload a clearer image or describe your symptoms."
                        add_to_chat_history(low_conf_msg, 'bot')
                        st.warning("⚠️ Low confidence - please try a clearer image")
                
                st.rerun()
        
        # Quick symptom buttons
        st.subheader("🚀 Quick Symptoms")
        quick_symptoms = ["Cold", "Headache", "Fever", "Acne", "Stress", "Joint Pain"]
        
        for symptom in quick_symptoms:
            if st.button(f"{symptom}", key=f"quick_{symptom}"):
                add_to_chat_history(f"I have {symptom.lower()}", 'user')
                matched_intent = enhanced_match_intent(symptom.lower())
                if matched_intent:
                    response = random.choice(matched_intent["responses"])
                    add_to_chat_history(response, 'bot', matched_intent)
                st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()
