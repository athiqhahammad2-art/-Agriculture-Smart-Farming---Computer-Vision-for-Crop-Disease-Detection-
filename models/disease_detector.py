import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import numpy as np
import os

class DiseaseDetector:
    """MobileNetV2-based disease detection model"""
    
    def __init__(self, model_path='models/disease_model.h5'):
        self.classes = ['Early Blight', 'Healthy', 'Late Blight', 'Powdery Mildew', 'Septoria']
        self.model_path = model_path
        self.model = self._build_model()
        
        if os.path.exists(model_path):
            self.model.load_weights(model_path)
    
    def _build_model(self):
        """Build transfer learning model with MobileNetV2"""
        base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
        base_model.trainable = False
        
        inputs = tf.keras.Input(shape=(224, 224, 3))
        x = base_model(inputs, training=False)
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.3)(x)
        outputs = Dense(len(self.classes), activation='softmax')(x)
        
        model = Model(inputs, outputs)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        return model
    
    def predict(self, image_array):
        """Predict disease from preprocessed image"""
        predictions = self.model.predict(np.expand_dims(image_array, axis=0))
        class_idx = np.argmax(predictions[0])
        confidence = predictions[0][class_idx]
        
        return {
            'disease': self.classes[class_idx],
            'confidence': float(confidence),
            'all_predictions': {self.classes[i]: float(predictions[0][i]) for i in range(len(self.classes))}
        }
    
    def save_model(self, path):
        """Save trained model"""
        self.model.save_weights(path)
        print(f"Model saved to {path}")
    
    def get_classes(self):
        """Return disease classes"""
        return self.classes