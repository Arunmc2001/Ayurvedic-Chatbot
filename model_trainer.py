import tensorflow as tf
import numpy as np
import os
from PIL import Image
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

class AyurvedaModelTrainer:
    def __init__(self, dataset_path="datasets"):
        self.dataset_path = dataset_path
        self.classes = [
            'Acne', 'Carcinoma', 'Cataract', 'Chickenpox', 'Conjunctivitis',
            'Eczema', 'Keratosis', 'Milia', 'Rosacea', 'Eyelid', 'Moles',
            'Psoriasis', 'Impetigo'
        ]
        self.img_size = (224, 224)
        self.model = None
        
    def load_dataset(self):
        """Load and preprocess dataset images"""
        print("Loading dataset...")
        images = []
        labels = []
        
        for class_idx, class_name in enumerate(self.classes):
            class_path = os.path.join(self.dataset_path, class_name)
            if not os.path.exists(class_path):
                print(f"Warning: {class_path} not found, skipping...")
                continue
                
            print(f"Loading {class_name}...")
            image_files = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # Limit to 200 images per class for faster training
            image_files = image_files[:200]
            
            for img_file in image_files:
                try:
                    img_path = os.path.join(class_path, img_file)
                    img = Image.open(img_path).convert('RGB')
                    img = img.resize(self.img_size)
                    img_array = np.array(img) / 255.0
                    
                    images.append(img_array)
                    labels.append(class_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
                    continue
        
        print(f"Loaded {len(images)} images from {len(set(labels))} classes")
        return np.array(images), np.array(labels)
    
    def create_model(self):
        """Create CNN model architecture"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(2, 2),
            
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(2, 2),
            
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(2, 2),
            
            tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(2, 2),
            
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(len(self.classes), activation='softmax')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, epochs=20):
        """Train the model on dataset"""
        # Load data
        X, y = self.load_dataset()
        
        if len(X) == 0:
            print("No data loaded! Check dataset path.")
            return None
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set: {len(X_train)} images")
        print(f"Test set: {len(X_test)} images")
        
        # Create model
        self.model = self.create_model()
        print("Model created successfully!")
        print(self.model.summary())
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            )
        ]
        
        # Train model
        print("Starting training...")
        history = self.model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\nFinal Test Accuracy: {test_accuracy:.4f}")
        
        # Save model
        model_path = "ayurvedic_symptom_model.h5"
        self.model.save(model_path)
        print(f"Model saved as {model_path}")
        
        return history
    
    def plot_training_history(self, history):
        """Plot training history"""
        if history is None:
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy plot
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Loss plot
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.show()

def main():
    """Main training function"""
    print("🌿 Ayurveda Model Training Started")
    print("=" * 50)
    
    # Initialize trainer
    trainer = AyurvedaModelTrainer()
    
    # Train model
    history = trainer.train_model(epochs=15)
    
    # Plot results
    if history:
        trainer.plot_training_history(history)
    
    print("=" * 50)
    print("✅ Training completed!")
    print("Model saved as 'ayurvedic_symptom_model.h5'")

if __name__ == "__main__":
    main()
