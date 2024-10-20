import streamlit as st
import cv2
from paddleocr import PaddleOCR
from collections import defaultdict
import numpy as np
from comparision import compare
import data_operation as dt
import os

path = "output_ocr_text.txt"

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        self.text_frequencies = defaultdict(int)
        self.best_confidences = {}
        self.detected_item = ""

    def process_ocr_result(self, result):
        if not result or not isinstance(result, list):
            return
        
        
        if result[0]:  
            for detection in result[0]:
                if detection is None or len(detection) != 2:
                    continue  # Skip invalid detections
                box, text_info = detection
                if text_info is None or len(text_info) != 2:
                    continue  # Skip invalid text info
                text, confidence = text_info
                text = text.strip()
                if not text:
                    continue
                
                self.text_frequencies[text] += 1
                
                if text not in self.best_confidences or confidence > self.best_confidences[text]:
                    self.best_confidences[text] = confidence
        

    def run(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.ocr.ocr(np.array(img), cls=True)

        if result:
            self.process_ocr_result(result)
            current_ocr_text = " ".join(self.text_frequencies.keys()).strip()
            if current_ocr_text:
                detected_item_num = compare(current_ocr_text)
                self.detected_item = dt.get_item_details(detected_item_num)['item_name']

    def save_results(self):
        if not self.text_frequencies:
            st.warning("No text detected.")
            return

        try:
            results = []
            for text, freq in self.text_frequencies.items():
                conf = self.best_confidences.get(text, 0.0)
                results.append((text, freq, conf))

            sorted_results = sorted(results, key=lambda x: (-x[1], -x[2]))

            with open(path, 'w', encoding='utf-8') as f:
                f.write("=== OCR Results ===\n\n")
                for text, freq, conf in sorted_results[:10]:
                    if freq > 1:
                        f.write(f"{text} ")

            st.success("OCR results saved successfully.")
        except Exception as e:
            st.error(f"Error saving results: {e}")

    def reset(self):
        self.text_frequencies.clear()
        self.best_confidences.clear()
        self.detected_item = ""
        if os.path.exists(path):
            os.remove(path)
        st.success("OCR data reset. Ready for next item.")

def main():
    st.set_page_config(page_title="Real-time OCR Item Detection", layout="wide")
    st.title("Real-time OCR Item Detection")

    processor = OCRProcessor()

    # Initialize session state for video capture
    if 'video_capture' not in st.session_state:
        st.session_state.video_capture = cv2.VideoCapture(0)

    # Create two columns
    col1, col2 = st.columns([3, 1])

    with col1:
        # Create a placeholder for the video feed
        video_placeholder = st.empty()

    with col2:
        # Create a placeholder for the detected item
        item_placeholder = st.empty()
        
        # Next Item button
        if st.button("Next Item", key="next_item_button", help="Reset OCR data for next item"):
            processor.reset()

    # Add custom CSS to style the button
    st.markdown("""
        <style>
        div.stButton{
            margin-left: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    while True:
        ret, frame = st.session_state.video_capture.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            break

        processor.run(frame)

        # Display the video feed
        with col1:
            video_placeholder.image(frame, channels="BGR", use_column_width=True)

        # Display the detected item
        with col2:
            if processor.detected_item:
                item_placeholder.markdown(f"""
                <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #1f77b4; margin-bottom: 10px;">Detected Item</h2>
                    <p style="font-size: 24px; font-weight: bold;"color: #000000;">{processor.detected_item}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                item_placeholder.markdown(f"""
                <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #1f77b4; margin-bottom: 10px;">   Detected Item</h2>
                    <p style="font-size: 18px;">Waiting for detection...</p>
                </div>  
                """, unsafe_allow_html=True)

        # Check if the Streamlit script is no longer running
        if not st.runtime.exists():
            break

    # Release the video capture when the Streamlit app is closed
    st.session_state.video_capture.release()

if __name__ == "__main__":
    main()  