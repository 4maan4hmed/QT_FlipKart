import cv2
from paddleocr import PaddleOCR
from collections import defaultdict
import numpy as np
from comparision import compare

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        self.text_frequencies = defaultdict(int)  # Track text frequencies
        self.best_confidences = {}  # Track best confidence for each text
        self.accumulated_text = ""  # Store accumulated text over multiple frames
        self.frame_count = 0  # Keep track of processed frames
        self.text_threshold = 20  # Adjust this for how much text to accumulate before output
        print("PaddleOCR initialized successfully.")

    def process_ocr_result(self, result):
        """Process OCR result, accumulate text, and trigger output after Enter key is pressed."""
        if not result or not isinstance(result, list):
            return
            
        # PaddleOCR returns: [[[box, (text, confidence)], ...]]
        try:
            for detection in result[0]:  # First level of nesting
                box, (text, confidence) = detection
                
                # Clean the text
                text = text.strip()
                if not text:
                    continue
                    
                # Update frequency
                self.text_frequencies[text] += 1
                
                # Update best confidence
                if text not in self.best_confidences or confidence > self.best_confidences[text]:
                    self.best_confidences[text] = confidence
                    print(f"Text: {text} | Confidence: {confidence:.2f} | Count: {self.text_frequencies[text]}")
                
                # Accumulate detected text
                self.accumulated_text += text + " "

        except Exception as e:
            print(f"Error processing detection: {e}")

    def run(self):
        """Run the OCR processor on camera feed."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Error: Unable to access the camera.")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = self.ocr.ocr(np.array(img), cls=True)
                
                if result:
                    self.process_ocr_result(result)

                # Display the frame
                cv2.imshow('OCR Detection (Press Enter to output, Q to quit)', frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    break

                # Press Enter to output results and reset detection
                if key == 13:  # 13 is the Enter key
                    if len(self.accumulated_text.split()) >= self.text_threshold:  # If we have enough text
                        self.perform_comparison()

                    self.reset_detection()

        finally:
            cap.release()
            cv2.destroyAllWindows()

    def perform_comparison(self):
        """Perform comparison of accumulated text and save results."""
        try:
            if self.accumulated_text.strip():
                print("\nComparing accumulated OCR text with database...")
                compare(self.accumulated_text.strip())
                self.save_results()

        except Exception as e:
            print(f"Error during comparison: {e}")

    def reset_detection(self):
        """Reset the accumulated text and frequencies for the next object detection."""
        print("\nResetting detection for the next object...")
        self.accumulated_text = ""
        self.text_frequencies.clear()
        self.best_confidences.clear()

    def save_results(self):
            """Save accumulated results to file."""
    try:
        # Write accumulated OCR results to 'output_ocr_text.txt'
        with open('output_ocr_text.txt', 'w', encoding='utf-8') as f:
            f.write("=== Accumulated OCR Results ===\n\n")
            f.write(self.accumulated_text.strip())
        
        # Read the contents of 'output_ocr_text.txt' and pass to compare function
        with open('output_ocr_text.txt', 'r', encoding='utf-8') as f:
            detected_text = f.read().strip()
        
        # Save the results of comparison to 'items_detected.txt'
        with open('items_detected.txt', 'w', encoding='utf-8') as f2:
            f2.write(compare(detected_text))

        print("\nResults saved to output_ocr_text.txt and items_detected.txt")

    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    try:
        # Initialize and run OCR processor
        processor = OCRProcessor()
        processor.run()

    except Exception as e:
        print(f"An error occurred: {e}")
