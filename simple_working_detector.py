
# simple_working_detector.py - Simple but Effective Object Counter
import os
import cv2
import numpy as np
import time
import logging
from collections import deque

class SimpleWorkingDetector:
    """
    Simple but highly effective object detection system
    """

    def __init__(self):
        self.count_history = deque(maxlen=10)
        self.confidence_history = deque(maxlen=10)
        self.session_start = time.time()
        self.total_images = 0

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SIMPLE_FACTORY - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def detect_objects(self, img_path):
        """
        Simple but effective object detection
        """
        try:
            img = cv2.imread(img_path)
            if img is None:
                self.logger.error(f"Could not load image: {img_path}")
                return 0, [], {}

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Apply adaptive thresholding
            h, w = gray.shape
            block_size = max(11, min(h, w) // 20)
            if block_size % 2 == 0:
                block_size += 1

            binary = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, block_size, 2
            )

            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter valid objects
            valid_objects = []
            img_area = h * w
            min_area = max(100, int(img_area * 0.0005))
            max_area = int(img_area * 0.05)

            for contour in contours:
                area = cv2.contourArea(contour)

                if area < min_area or area > max_area:
                    continue

                # Get bounding box
                x, y, width, height = cv2.boundingRect(contour)

                # Edge filtering
                margin = 10
                if (x < margin or y < margin or 
                    x + width > w - margin or y + height > h - margin):
                    continue

                # Calculate features
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue

                aspect_ratio = width / float(height)
                extent = area / float(width * height)
                circularity = 4 * np.pi * area / (perimeter * perimeter)

                # Filter based on shape
                if (0.3 < aspect_ratio < 3.0 and 
                    extent > 0.2 and 
                    circularity > 0.1):

                    # Calculate confidence
                    confidence = min(1.0, (area / 500.0) * circularity * extent)
                    confidence = max(0.3, min(0.95, confidence))

                    # Simple classification
                    if 0.6 < aspect_ratio < 1.4 and circularity > 0.4:
                        obj_type = 'nuts'
                    elif aspect_ratio > 2.0:
                        obj_type = 'screws'
                    elif circularity > 0.6:
                        obj_type = 'washers'
                    else:
                        obj_type = 'bolts'

                    valid_objects.append({
                        'bbox': (x, y, width, height),
                        'area': float(area),
                        'confidence': float(confidence),
                        'type': obj_type,
                        'circularity': float(circularity),
                        'aspect_ratio': float(aspect_ratio)
                    })

            # Sort by confidence
            valid_objects.sort(key=lambda x: x['confidence'], reverse=True)

            # Calculate classifications
            classifications = {'nuts': 0, 'bolts': 0, 'screws': 0, 'washers': 0}
            for obj in valid_objects:
                classifications[obj['type']] += 1

            self.logger.info(f"Detected {len(valid_objects)} objects")
            return len(valid_objects), valid_objects, classifications, img

        except Exception as e:
            self.logger.error(f"Detection failed: {e}")
            return 0, [], {}, None

    def analyze_vibration_method(self, current_count):
        """
        Simple vibration analysis
        """
        self.count_history.append(current_count)

        if len(self.count_history) < 2:
            return {
                'most_frequent_count': current_count,
                'consistency_score': 0.5,
                'recommendation': 'Take more images after vibrating the plate'
            }

        # Find most frequent count
        from collections import Counter
        count_freq = Counter(self.count_history)
        most_frequent_count, frequency = count_freq.most_common(1)[0]
        consistency_score = frequency / len(self.count_history)

        if consistency_score > 0.7:
            recommendation = "Excellent! Vibration method is working perfectly."
        elif consistency_score > 0.5:
            recommendation = "Good consistency. Continue using vibration method."
        else:
            recommendation = "Try more vibration to separate objects better."

        return {
            'most_frequent_count': most_frequent_count,
            'consistency_score': consistency_score,
            'recommendation': recommendation
        }

    def get_session_stats(self):
        """
        Simple session statistics
        """
        session_duration = time.time() - self.session_start

        if not self.count_history:
            return {
                'total_images': self.total_images,
                'session_duration_minutes': round(session_duration / 60, 1),
                'average_count': 0,
                'min_count': 0,
                'max_count': 0
            }

        counts = list(self.count_history)
        return {
            'total_images': len(counts),
            'session_duration_minutes': round(session_duration / 60, 1),
            'average_count': round(np.mean(counts), 1),
            'min_count': min(counts),
            'max_count': max(counts)
        }

    def reset_session(self):
        """Reset all session data"""
        self.count_history.clear()
        self.confidence_history.clear()
        self.session_start = time.time()
        self.total_images = 0
        self.logger.info("Session reset completed")

# Global detector instance
simple_detector = SimpleWorkingDetector()

def analyze_image_simple(input_path, output_path, min_confidence=0.3):
    """
    Simple image analysis function
    """
    global simple_detector

    try:
        count, objects, classifications, img = simple_detector.detect_objects(input_path)

        if img is None:
            return 0, [], {}, {}, {}

        # Filter by confidence
        valid_objects = [obj for obj in objects if obj['confidence'] >= min_confidence]
        final_count = len(valid_objects)

        # Update classifications
        final_classifications = {'nuts': 0, 'bolts': 0, 'screws': 0, 'washers': 0}
        for obj in valid_objects:
            final_classifications[obj['type']] += 1

        # Calculate average confidence
        avg_confidence = np.mean([obj['confidence'] for obj in valid_objects]) if valid_objects else 0.0
        simple_detector.confidence_history.append(avg_confidence)
        simple_detector.total_images += 1

        # Vibration analysis
        vibration_results = simple_detector.analyze_vibration_method(final_count)

        # Draw results on image
        draw = img.copy()
        h, w = img.shape[:2]

        # Color coding for different types
        type_colors = {
            'nuts': (0, 255, 0),      # Green
            'bolts': (255, 0, 0),     # Blue  
            'screws': (0, 0, 255),    # Red
            'washers': (255, 255, 0)  # Cyan
        }

        # Draw bounding boxes
        for i, obj in enumerate(valid_objects):
            x, y, width, height = obj['bbox']
            obj_type = obj['type']
            confidence = obj['confidence']

            color = type_colors.get(obj_type, (128, 128, 128))
            thickness = 3

            # Draw rectangle
            cv2.rectangle(draw, (x, y), (x + width, y + height), color, thickness)

            # Draw label
            label = f"{obj_type.upper()}#{i+1}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(draw, (x, y-20), (x + label_size[0] + 5, y), color, -1)
            cv2.putText(draw, label, (x+2, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        # Add summary text
        summary_color = (0, 255, 255)
        cv2.putText(draw, f"Objects Detected: {final_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, summary_color, 2)
        cv2.putText(draw, f"Most Frequent: {vibration_results['most_frequent_count']}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, summary_color, 2)
        cv2.putText(draw, f"Confidence: {avg_confidence:.1%}", 
                   (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, summary_color, 2)

        # Save result image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, draw)

        # Get session stats
        session_stats = simple_detector.get_session_stats()

        simple_detector.logger.info(f"Analysis complete: {final_count} objects detected")

        return final_count, valid_objects, final_classifications, session_stats, vibration_results

    except Exception as e:
        simple_detector.logger.error(f"Analysis failed: {e}")
        return 0, [], {}, {}, {}
