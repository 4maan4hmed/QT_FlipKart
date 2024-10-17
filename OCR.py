from paddleocr import PaddleOCR
from collections import defaultdict
import numpy as np
import cv2

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)#keep gpu usuage false if cuda isnt setup
        self.text_frequencies = defaultdict(int)  # Track text frequencies
        self.best_confidences = {}  # Track best confidence for each text
        self.accumulated_text = ""  # Store accumulated OCR text
        print("PaddleOCR initialized successfully.")

    def process_ocr_result(self, result):
        """Process OCR result and update frequencies and confidences."""
        if not result or not isinstance(result, list):
            return

        # PaddleOCR returns: [[[box, (text, confidence)], ...]]
        try:
            for detection in result[0]:  # First level of nesting
                box, (text, confidence) = detection

                # Clean the text remove unwated spaces etc
                text = text.strip()
                if not text:
                    continue

                # Update frequency
                self.text_frequencies[text] += 1

                # Update best confidence
                if text not in self.best_confidences or confidence > self.best_confidences[text]:
                    self.best_confidences[text] = confidence
                    self.accumulated_text += f"{text} "  # Append the text to accumulated_text
                    print(f"Text: {text} | Confidence: {confidence:.2f} | Count: {self.text_frequencies[text]}")

        except Exception as e:
            print(f"Error processing detection: {e}")

    def process_image(self, image):
        """Takes in an image, performs OCR, and updates text file."""
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.ocr.ocr(np.array(img_rgb), cls=True)
        if result:
            self.process_ocr_result(result)
            

        # Save results in real-time
        self.save_results()
        return self.accumulated_text

    def save_results(self):
        """Save accumulated OCR text to file."""
        try:
            with open('output_ocr_text.txt', 'w', encoding='utf-8') as f:
                f.write("=== Accumulated OCR Results ===\n\n")
                f.write(self.accumulated_text.strip())
            print("Results updated in output_ocr_text.txt")
            

        except Exception as e:
            print(f"Error saving results: {e}")

    def reset_accumulated_text(self):
        """Reset the accumulated OCR text."""
        self.accumulated_text = ""
        print("Accumulated text reset.")


# Usage in your main code
# processor = OCRProcessor()
# processor.process_image(image)  # Pass an image frame to process
