# 🌿 AI Ayurveda Assistant

A modern ChatGPT-like Ayurvedic health assistant powered by AI image analysis and comprehensive symptom detection.

## ✨ Features

- **🤖 AI-Powered Image Analysis**: Upload images for instant symptom detection using deep learning
- **💬 Natural Language Chat**: Conversational interface similar to ChatGPT
- **🌿 Comprehensive Ayurvedic Database**: 30+ conditions with detailed treatment plans
- **💊 Personalized Medicine Recommendations**: Dosages, timings, and precautions
- **🏥 Hospital Directory**: Nearby Ayurvedic centers and contacts
- **📊 Chat History & Analytics**: Track consultations and download records
- **📱 Modern UI/UX**: Responsive design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
```bash
cd "d:\New folder\editting last\ai ayurveda"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run advanced_chatbot.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
ai-ayurveda/
├── advanced_chatbot.py          # Main ChatGPT-like application
├── ayurveda_chatbot.py          # Alternative simpler version
├── enhanced_model_utils.py      # AI model utilities and knowledge base
├── cha2.py                      # Original development file
├── ayurvedic_symptom_model.h5   # Pre-trained AI model (9.6MB)
├── requirements.txt             # Python dependencies
├── datasets/                    # Sample medical images
│   ├── Allergy.jpg
│   ├── headache.jpg
│   ├── pimples.jpg
│   └── skin_rashes.jpg
└── README.md                    # This file
```

## 🎯 How to Use

### 1. Text-Based Consultation
- Type symptoms naturally: "I have a headache and feel nauseous"
- Use quick symptom buttons for common conditions
- Get detailed Ayurvedic treatment plans with medicines and lifestyle advice

### 2. Image Analysis
- Upload clear photos of affected areas
- AI analyzes and provides confidence-based predictions
- Receive comprehensive treatment protocols

### 3. Chat Features
- View conversation history
- Download consultation records
- Clear chat when needed
- Real-time typing indicators

## 🧠 AI Model Information

The application uses a pre-trained TensorFlow model (`ayurvedic_symptom_model.h5`) that can detect:

- Allergies and skin reactions
- Headaches and migraines  
- Acne and pimples
- Skin rashes and irritations
- Cold and flu symptoms
- Digestive issues
- Joint pain and inflammation

**Model Specifications:**
- Input: 224x224 RGB images
- Architecture: Convolutional Neural Network
- Framework: TensorFlow/Keras
- Size: 9.6MB

## 🌿 Ayurvedic Knowledge Base

The system includes comprehensive treatment protocols for:

### Conditions Covered
- **Respiratory**: Cold, cough, fever, asthma
- **Digestive**: Acidity, indigestion, constipation, GERD
- **Skin**: Acne, rashes, allergies, psoriasis, eczema
- **Neurological**: Headaches, migraines, stress, insomnia
- **Musculoskeletal**: Joint pain, arthritis, muscle cramps
- **Systemic**: Diabetes, hypertension, thyroid disorders

### Treatment Information
- **Medicines**: Traditional Ayurvedic formulations with dosages
- **Duration**: Recommended treatment periods
- **Diet**: Specific dietary guidelines and restrictions
- **Lifestyle**: Daily routine and behavioral modifications
- **Precautions**: Important safety considerations

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web interface framework
- **TensorFlow**: AI model inference
- **OpenCV**: Image processing
- **Pillow**: Image handling
- **NumPy**: Numerical computations

### Performance
- **Image Analysis**: ~2-3 seconds per image
- **Chat Response**: Instant text processing
- **Memory Usage**: ~500MB with model loaded
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge

## 🎨 User Interface

### ChatGPT-Like Features
- **Bubble Chat Interface**: Modern messaging design
- **Typing Indicators**: Shows when AI is processing
- **Smooth Animations**: Slide-in effects for messages
- **Responsive Design**: Works on desktop and mobile
- **Dark/Light Themes**: Automatic theme detection

### Advanced UI Elements
- **Confidence Bars**: Visual representation of AI certainty
- **Medicine Cards**: Highlighted treatment recommendations
- **Hospital Cards**: Contact information display
- **Progress Indicators**: Real-time analysis feedback

## 📊 Analytics & Tracking

- **Message Count**: Track conversation length
- **Analysis History**: Review past image analyses
- **Confidence Metrics**: Monitor AI prediction accuracy
- **Export Options**: Download chat logs as JSON

## ⚠️ Important Disclaimers

1. **Medical Advice**: This AI provides general Ayurvedic guidance only
2. **Professional Consultation**: Always consult qualified healthcare providers
3. **Emergency Situations**: Seek immediate medical help for serious conditions
4. **AI Limitations**: Predictions may not be 100% accurate
5. **Traditional Medicine**: Ayurvedic treatments are complementary to modern medicine

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your device
- **No Data Storage**: Images and chats are not permanently stored
- **Session-Based**: Data cleared when browser closes
- **No External APIs**: Fully offline operation after initial setup

## 🛠️ Troubleshooting

### Common Issues

**1. Model Loading Error**
```
Error: Model file not found
Solution: Ensure ayurvedic_symptom_model.h5 is in the project directory
```

**2. Image Upload Issues**
```
Error: Cannot process image
Solution: Use JPG, PNG formats with clear, well-lit photos
```

**3. Slow Performance**
```
Issue: App running slowly
Solution: Close other applications, ensure sufficient RAM (4GB+)
```

**4. Dependencies Error**
```
Error: Module not found
Solution: Run 'pip install -r requirements.txt' again
```

### Performance Optimization
- Use images under 5MB for faster processing
- Close unused browser tabs
- Restart app if memory usage is high
- Use latest Python version (3.8+)

## 🚀 Advanced Usage

### Custom Model Integration
Replace `ayurvedic_symptom_model.h5` with your own trained model:
1. Ensure same input dimensions (224x224x3)
2. Update `DISEASE_CLASSES` in `enhanced_model_utils.py`
3. Modify treatment database accordingly

### Adding New Conditions
1. Update `enhanced_intents` in `advanced_chatbot.py`
2. Add treatment protocols in `AyurvedaKnowledgeBase`
3. Include new patterns for natural language matching

## 📞 Support

For technical issues or questions:
- Check troubleshooting section above
- Review code comments for implementation details
- Ensure all dependencies are properly installed

## 📄 License

This project is for educational and research purposes. Please consult healthcare professionals for medical advice.

---

**Built with ❤️ using Python, Streamlit, and TensorFlow**

*Combining ancient Ayurvedic wisdom with modern AI technology*
