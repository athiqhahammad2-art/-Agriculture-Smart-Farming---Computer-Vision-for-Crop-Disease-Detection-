import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import sys
sys.path.append('..')
from utils.image_processor import ImageProcessor

class ModelTrainer:
    """Train disease detection model"""
    
    def __init__(self, dataset_path='data/dataset', output_path='models'):
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.image_processor = ImageProcessor()
        self.classes = self._get_classes()
        os.makedirs(output_path, exist_ok=True)
    
    def _get_classes(self):
        """Get disease classes from dataset directory"""
        if os.path.exists(self.dataset_path):
            return sorted([d for d in os.listdir(self.dataset_path) 
                          if os.path.isdir(os.path.join(self.dataset_path, d))])
        return ['Early Blight', 'Healthy', 'Late Blight', 'Powdery Mildew', 'Septoria']
    
    def load_dataset(self):
        """Load and preprocess dataset"""
        images = []
        labels = []
        
        for class_idx, disease in enumerate(self.classes):
            disease_path = os.path.join(self.dataset_path, disease)
            
            if not os.path.exists(disease_path):
                print(f"Warning: {disease_path} not found")
                continue
            
            for img_file in os.listdir(disease_path):
                if img_file.endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(disease_path, img_file)
                    try:
                        img = self.image_processor.preprocess(img_path)
                        images.append(img)
                        labels.append(class_idx)
                    except Exception as e:
                        print(f"Error processing {img_path}: {e}")
        
        return np.array(images), np.array(labels)
    
    def build_model(self):
        """Build transfer learning model"""
        base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
        base_model.trainable = False
        
        inputs = tf.keras.Input(shape=(224, 224, 3))
        x = base_model(inputs, training=False)
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        outputs = Dense(len(self.classes), activation='softmax')(x)
        
        model = Model(inputs, outputs)
        return model
    
    def train(self, epochs=50, batch_size=32, validation_split=0.2):
        """Train the model"""
        print("Loading dataset...")
        X, y = self.load_dataset()
        
        if len(X) == 0:
            print("No images found. Please provide dataset in data/dataset/{disease_name}/ folders")
            return None
        
        # Convert labels to one-hot
        from tensorflow.keras.utils import to_categorical
        y = to_categorical(y, num_classes=len(self.classes))
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=validation_split, random_state=42)
        
        print(f"Training set size: {len(X_train)}")
        print(f"Validation set size: {len(X_val)}")
        
        # Build and compile model
        model = self.build_model()
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        # Data augmentation
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2]
        )
        
        # Callbacks
        callbacks = [
            ModelCheckpoint(os.path.join(self.output_path, 'best_model.h5'), monitor='val_accuracy', save_best_only=True),
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)
        ]
        
        # Train model
        history = model.fit(
            train_datagen.flow(X_train, y_train, batch_size=batch_size),
            validation_data=(X_val, y_val),
            epochs=epochs,
            callbacks=callbacks
        )
        
        # Save final model
        model.save_weights(os.path.join(self.output_path, 'disease_model.h5'))
        print(f"Model saved to {os.path.join(self.output_path, 'disease_model.h5')}")
        
        return history

if __name__ == '__main__':
    import tensorflow as tf
    trainer = ModelTrainer()
    trainer.train(epochs=50, batch_size=32)