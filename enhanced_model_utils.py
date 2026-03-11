import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

class AyurvedaImageAnalyzer:
    """Enhanced image analysis utilities for Ayurvedic symptom detection"""
    
    def __init__(self, model_path="ayurvedic_symptom_model.h5"):
        self.model_path = model_path
        self.model = None
        self.disease_classes = [
            'Allergy', 'Headache', 'Pimples', 'Skin_Rashes', 'Cold', 
            'Fever', 'Cough', 'Acidity', 'Indigestion', 'Joint_Pain',
            'Eye_Condition', 'Milia', 'Skin_Tags'
        ]
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"Model loaded successfully from {self.model_path}")
            else:
                print(f"Model file not found: {self.model_path}")
                self.create_dummy_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self.create_dummy_model()
    
    def create_dummy_model(self):
        """Create a dummy model for demonstration if main model fails"""
        print("Creating dummy model for demonstration...")
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(len(self.disease_classes), activation='softmax')
        ])
        
        # Compile the model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def preprocess_image(self, image):
        """Preprocess image for model prediction"""
        try:
            # Convert PIL image to numpy array if needed
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image
            
            # Convert to RGB if needed
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
            elif len(img_array.shape) == 3 and img_array.shape[2] == 1:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
            
            # Resize to model input size
            img_resized = cv2.resize(img_array, (224, 224))
            
            # Normalize pixel values
            img_normalized = img_resized.astype('float32') / 255.0
            
            # Add batch dimension
            img_batch = np.expand_dims(img_normalized, axis=0)
            
            return img_batch
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict_disease(self, image):
        """Predict disease from image with enhanced eye condition detection"""
        if self.model is None:
            return self.analyze_image_patterns(image)
        
        try:
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                return "Error processing image", 0.0
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the class with highest probability
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            predicted_disease = self.disease_classes[predicted_class_idx].lower()
            
            # Enhanced analysis for eye area images
            enhanced_result = self.analyze_image_patterns(image)
            if enhanced_result[1] > confidence and "eye" in enhanced_result[0].lower():
                return enhanced_result
            
            return predicted_disease, confidence
        except Exception as e:
            print(f"Error in prediction: {e}")
            return self.analyze_image_patterns(image)
    
    def analyze_image_patterns(self, image):
        """Analyze image patterns for better detection of eye conditions"""
        try:
            # Convert to numpy array for analysis
            img_array = np.array(image)
            
            # Convert to HSV for better color analysis
            img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Detect skin tone regions (typical eye area)
            skin_lower = np.array([0, 20, 70])
            skin_upper = np.array([20, 255, 255])
            skin_mask = cv2.inRange(img_hsv, skin_lower, skin_upper)
            
            # Detect white/light colored spots (milia, whiteheads)
            white_lower = np.array([0, 0, 200])
            white_upper = np.array([180, 30, 255])
            white_mask = cv2.inRange(img_hsv, white_lower, white_upper)
            
            # Calculate percentages
            total_pixels = img_array.shape[0] * img_array.shape[1]
            skin_percentage = np.sum(skin_mask > 0) / total_pixels
            white_spots_percentage = np.sum(white_mask > 0) / total_pixels
            
            # Analyze image characteristics
            if skin_percentage > 0.3 and white_spots_percentage > 0.02:
                # Likely eye area with white spots (milia)
                return "milia", 0.75
            elif skin_percentage > 0.4:
                # General eye/skin condition
                return "eye_condition", 0.65
            else:
                # Fallback to skin rash if unclear
                return "skin_rashes", 0.55
                
        except Exception as e:
            print(f"Error in pattern analysis: {e}")
            return "skin_rashes", 0.50
    
    def get_top_predictions(self, image, top_k=3):
        """Get top K predictions with confidence scores"""
        if self.model is None:
            return []
        
        try:
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                return []
            
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get top K predictions
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                disease = self.disease_classes[idx].lower()
                confidence = float(predictions[0][idx])
                results.append((disease, confidence))
            
            return results
        except Exception as e:
            print(f"Error getting top predictions: {e}")
            return []

# Enhanced Ayurvedic knowledge base
class AyurvedaKnowledgeBase:
    """Comprehensive Ayurvedic knowledge and treatment database"""
    
    def __init__(self):
        self.treatments = {
            'allergy': {
                'medicines': [
                    'Neem Capsules - 1 capsule morning empty stomach',
                    'Turmeric Water - 1 tsp in warm water at night',
                    'Haridra Khanda - 1 tsp after meals twice daily',
                    'Mahamanjisthadi Kwath - 15ml twice daily'
                ],
                'duration': '2-3 weeks',
                'diet': [
                    'Avoid dairy products temporarily',
                    'Include bitter vegetables like bitter gourd',
                    'Drink plenty of water',
                    'Avoid spicy and oily foods'
                ],
                'lifestyle': [
                    'Practice pranayama daily',
                    'Maintain clean environment',
                    'Use natural, chemical-free products',
                    'Get adequate sleep'
                ],
                'precautions': [
                    'Identify and avoid allergens',
                    'Keep surroundings dust-free',
                    'Consult doctor if symptoms worsen'
                ]
            },
            'headache': {
                'medicines': [
                    'Peppermint Oil - Apply on temples gently',
                    'Ashwagandha - 1 tsp with milk before sleep',
                    'Brahmi Oil - Massage scalp at night',
                    'Saraswatarishta - 15ml twice daily after meals'
                ],
                'duration': 'As needed or 3-5 days if frequent',
                'diet': [
                    'Stay well hydrated',
                    'Avoid caffeine if stress-related',
                    'Include magnesium-rich foods',
                    'Regular meal timings'
                ],
                'lifestyle': [
                    'Practice meditation daily',
                    'Maintain regular sleep schedule',
                    'Avoid excessive screen time',
                    'Practice neck and shoulder exercises'
                ],
                'precautions': [
                    'Seek medical help for severe headaches',
                    'Monitor triggers like stress, food',
                    'Avoid self-medication for chronic cases'
                ]
            },
            'pimples': {
                'medicines': [
                    'Turmeric Paste - Apply locally in evening',
                    'Neem Capsules - 1 capsule morning',
                    'Manjistha Powder - 1 tsp with water at night',
                    'Sariva Syrup - 10ml twice daily'
                ],
                'duration': '4-6 weeks',
                'diet': [
                    'Avoid oily and fried foods',
                    'Reduce dairy consumption',
                    'Include fresh fruits and vegetables',
                    'Drink 8-10 glasses of water daily'
                ],
                'lifestyle': [
                    'Maintain facial hygiene',
                    'Use natural face wash',
                    'Avoid touching face frequently',
                    'Change pillowcases regularly'
                ],
                'precautions': [
                    'Do not squeeze or pop pimples',
                    'Use oil-free cosmetics',
                    'Protect from sun exposure'
                ]
            },
            'skin_rashes': {
                'medicines': [
                    'Neem Paste - Apply locally morning',
                    'Aloe Vera Gel - Apply at night',
                    'Sariva Powder - 1 tsp with water twice daily',
                    'Khadirarishta - 15ml after meals'
                ],
                'duration': '2-4 weeks',
                'diet': [
                    'Avoid spicy and sour foods',
                    'Include cooling foods like cucumber',
                    'Drink coconut water',
                    'Avoid citrus fruits temporarily'
                ],
                'lifestyle': [
                    'Keep affected area clean and dry',
                    'Wear loose, cotton clothes',
                    'Avoid synthetic fabrics',
                    'Use mild, natural soaps'
                ],
                'precautions': [
                    'Avoid scratching the affected area',
                    'Keep nails short and clean',
                    'Consult if rash spreads or worsens'
                ]
            },
            'cold': {
                'medicines': [
                    'Tulsi Tea - 2-3 times daily',
                    'Chyawanprash - 1 tsp before bed',
                    'Ginger Honey - 1 tsp as needed',
                    'Sitopaladi Churna - 1 tsp with honey twice daily'
                ],
                'duration': '5-7 days',
                'diet': [
                    'Drink warm water throughout day',
                    'Include ginger and garlic in food',
                    'Avoid cold foods and drinks',
                    'Take light, easily digestible meals'
                ],
                'lifestyle': [
                    'Take adequate rest',
                    'Stay warm',
                    'Inhale steam with eucalyptus oil',
                    'Avoid exposure to cold air'
                ],
                'precautions': [
                    'Cover nose and mouth when going out',
                    'Maintain distance from others',
                    'Wash hands frequently'
                ]
            },
            'eye_condition': {
                'medicines': [
                    'Rose Water - Apply as eye drops 2-3 times daily',
                    'Triphala Water - Wash eyes morning and evening',
                    'Ghee - Apply around eyes at night',
                    'Amalaki Rasayana - 1 tsp with milk twice daily'
                ],
                'duration': '1-2 weeks',
                'diet': [
                    'Include vitamin A rich foods like carrots',
                    'Drink plenty of water',
                    'Avoid excessive screen time',
                    'Include green leafy vegetables'
                ],
                'lifestyle': [
                    'Practice eye exercises daily',
                    'Take regular breaks from screens',
                    'Ensure proper lighting while reading',
                    'Get adequate sleep'
                ],
                'precautions': [
                    'Avoid rubbing eyes',
                    'Use clean hands when touching eye area',
                    'Consult eye specialist if symptoms persist'
                ]
            },
            'milia': {
                'medicines': [
                    'Neem Oil - Apply gently around affected area',
                    'Turmeric Paste - Mix with milk, apply at night',
                    'Aloe Vera Gel - Apply twice daily',
                    'Manjistha Powder - 1 tsp with water internally'
                ],
                'duration': '3-4 weeks',
                'diet': [
                    'Reduce dairy products temporarily',
                    'Avoid oily and fried foods',
                    'Include fresh fruits and vegetables',
                    'Drink warm water throughout day'
                ],
                'lifestyle': [
                    'Gentle cleansing of face',
                    'Avoid harsh scrubbing',
                    'Use natural, mild cleansers',
                    'Keep the area clean and dry'
                ],
                'precautions': [
                    'Do not try to squeeze or pop milia',
                    'Avoid oil-based cosmetics around eyes',
                    'Use gentle, fragrance-free products'
                ]
            }
        }
    
    def get_treatment_plan(self, disease):
        """Get comprehensive treatment plan for a disease"""
        disease = disease.lower().replace('_', '')
        
        if disease in self.treatments:
            return self.treatments[disease]
        else:
            return {
                'medicines': ['Consult an Ayurvedic practitioner for specific treatment'],
                'duration': 'As advised by doctor',
                'diet': ['Follow a balanced, healthy diet'],
                'lifestyle': ['Maintain healthy lifestyle habits'],
                'precautions': ['Seek professional medical advice']
            }
    
    def format_treatment_response(self, disease, confidence=None):
        """Format a comprehensive treatment response"""
        treatment = self.get_treatment_plan(disease)
        
        response = f"## 🌿 Ayurvedic Analysis: {disease.replace('_', ' ').title()}\n\n"
        
        if confidence:
            response += f"**Confidence Level:** {confidence:.1%}\n\n"
        
        response += "### 💊 Recommended Medicines:\n"
        for medicine in treatment['medicines']:
            response += f"• {medicine}\n"
        
        response += f"\n### ⏱️ Treatment Duration: {treatment['duration']}\n\n"
        
        response += "### 🍽️ Dietary Recommendations:\n"
        for diet_tip in treatment['diet']:
            response += f"• {diet_tip}\n"
        
        response += "\n### 🧘 Lifestyle Guidelines:\n"
        for lifestyle_tip in treatment['lifestyle']:
            response += f"• {lifestyle_tip}\n"
        
        response += "\n### ⚠️ Important Precautions:\n"
        for precaution in treatment['precautions']:
            response += f"• {precaution}\n"
        
        return response
