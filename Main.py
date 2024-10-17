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
        print("PaddleOCR initialized successfully.")

    def process_ocr_result(self, result):
        """Process OCR result with correct format handling."""
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

                cv2.imshow('OCR Detection (Press Q to quit)', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:

            cap.release()
            cv2.destroyAllWindows()
            self.save_results()

    def save_results(self):
        """Save results sorted by frequency and confidence."""
        if not self.text_frequencies:
            print("No text detected.")
            return

        try:
            # Combine frequency and confidence data
            results = []
            for text, freq in self.text_frequencies.items():
                conf = self.best_confidences.get(text, 0.0)
                results.append((text, freq, conf))

            # Sort by frequency (primary) and confidence (secondary)
            sorted_results = sorted(results, key=lambda x: (-x[1], -x[2]))

            # Save top results to file
            with open('output_ocr_text.txt', 'w', encoding='utf-8') as f:
                f.write("=== OCR Results ===\n\n")

                for text, freq, conf in sorted_results[:10]:
                    if freq > 1:
                        f.write(f"{text} ")

            # Print summary of top results
            print("\nTop detected texts:")
            print("------------------")
            for text, freq, conf in sorted_results[:5]:
                print(f"'{text}': {freq} times (conf: {conf:.2f})")
            
            print("\nFull results saved to output_ocr_text.txt")
            
        except Exception as e:
            print(f"Error saving results: {e}")


if __name__ == "__main__":
    try:
        # Initialize and run OCR processor
        processor = OCRProcessor()
        processor.run()

        # After processing, read saved OCR results
        with open('output_ocr_text.txt', 'r', encoding='utf-8') as f:
            ocr_text = f.read().strip()
            if ocr_text:
                # Compare OCR text with stored data
                print(f"{compare(ocr_text)}\n{compare(ocr_text)}\n{compare(ocr_text)}\n{compare(ocr_text)}\n{compare(ocr_text)}\n{compare(ocr_text)}")
            else:
                print("No OCR text found to compare.")
            
    except Exception as e:
        print(f"An error occurred: {e}") 