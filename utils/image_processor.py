import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class ImageProcessor:
    """Handle image preprocessing and augmentation"""
    
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        self.augmenter = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest'
        )
    
    def preprocess(self, image_path):
        """Load and preprocess image"""
        # Load image
        img = Image.open(image_path).convert('RGB')
        
        # Resize
        img = img.resize(self.target_size, Image.Resampling.LANCZOS)
        
        # Convert to array
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize
        img_array = img_array / 255.0
        
        return img_array
    
    def augment_image(self, image_array, num_augmentations=5):
        """Generate augmented images for training"""
        augmented_images = []
        
        for _ in range(num_augmentations):
            aug_image = self.augmenter.random_transform(image_array)
            augmented_images.append(aug_image)
        
        return np.array(augmented_images)
    
    def batch_preprocess(self, image_paths):
        """Preprocess batch of images"""
        processed_images = []
        for path in image_paths:
            processed_images.append(self.preprocess(path))
        return np.array(processed_images)
    
    def extract_features(self, image_array):
        """Extract hand-crafted features from image"""
        # Convert to HSV for better color representation
        hsv = cv2.cvtColor((image_array * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
        
        # Calculate histograms
        hist_h = cv2.calcHist([hsv], [0], None, [50], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [50], [0, 256])
        hist_v = cv2.calcHist([hsv], [2], None, [50], [0, 256])
        
        features = np.concatenate([hist_h.flatten(), hist_s.flatten(), hist_v.flatten()])
        
        return features / (features.sum() + 1e-6)