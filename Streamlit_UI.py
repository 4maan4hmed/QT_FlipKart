import streamlit as st
import cv2
from paddleocr import PaddleOCR
from collections import defaultdict
import numpy as np
from comparision import compare
import data_operation as dt
import os
from pathlib import Path
import json

path = "output_ocr_text.txt"

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        self.text_frequencies = defaultdict(int)
        self.best_confidences = {}
        self.detected_item = ""
        self.accumulated_text = ""

    def process_ocr_result(self, result):
        if not result or not isinstance(result, list):
            return
        
        if result[0]:  
            for detection in result[0]:
                if detection is None or len(detection) != 2:
                    continue
                box, text_info = detection
                if text_info is None or len(text_info) != 2:
                    continue
                text, confidence = text_info
                text = text.strip()
                if not text:
                    continue
                
                self.text_frequencies[text] += 1
                
                if text not in self.best_confidences or confidence > self.best_confidences[text]:
                    self.best_confidences[text] = confidence
                    if text not in self.accumulated_text:
                        self.accumulated_text += f"{text} "

    def process_image(self, frame):
        """Process a single frame and return detected text"""
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.ocr.ocr(np.array(img), cls=True)

        if result:
            self.process_ocr_result(result)
            self.save_results()
            return self.accumulated_text.strip()
        return None

    def run(self, frame):
        """Process frame and update detected item"""
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
        except Exception as e:
            st.error(f"Error saving results: {e}")

    def reset(self):
        """Reset all OCR data"""
        self.text_frequencies.clear()
        self.best_confidences.clear()
        self.detected_item = ""
        self.accumulated_text = ""
        if os.path.exists(path):
            os.remove(path)

def initialize_session_state():
    """Initialize session state variables"""
    if 'processor' not in st.session_state:
        st.session_state.processor = OCRProcessor()
    if 'video_capture' not in st.session_state:
        st.session_state.video_capture = cv2.VideoCapture(0)

def item_identifier():
    st.title("Item Identifier")

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

    while True:
        ret, frame = st.session_state.video_capture.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            break

        # Process the frame and accumulate OCR text
        processor.process_image(frame)

        # Identify the item based on accumulated text
        matched_item = processor.identify_item()

        # Display the video feed
        with col1:
            video_placeholder.image(frame, channels="BGR", use_column_width=True)

        # Display the detected item
        with col2:
            if matched_item:
                item_placeholder.markdown(f"""
                <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #1f77b4; margin-bottom: 10px;">Detected Item</h2>
                    <p style="font-size: 24px; font-weight: bold; color: #ffffff;">{matched_item['item_name']}</p>
                    <p style="font-size: 18px; color: #ffffff;">Quantity: {matched_item['quantity']}</p>
                    <p style="font-size: 18px; color: #ffffff;">Description: {matched_item['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                item_placeholder.markdown(f"""
                <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #1f77b4; margin-bottom: 10px;">Detected Item</h2>
                    <p style="font-size: 18px; color: #ffffff;">Waiting for detection...</p>
                </div>  
                """, unsafe_allow_html=True)

        # Check if the Streamlit script is no longer running
        if not st.runtime.exists():
            break

    # Release the video capture when the Streamlit app is closed
    st.session_state.video_capture.release()
def add_new_item():
    st.title("Add New Item")
    initialize_session_state()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_placeholder = st.empty()
        
    with col2:
        text_placeholder = st.empty()

    with st.form("new_item_form"):
        item_name = st.text_input("Item Name:")
        item_quantity = st.number_input("Quantity:", min_value=1)
        item_description = st.text_area("Description:")
        submitted = st.form_submit_button("Capture and Add Item")

        if submitted:
            try:
                ret, frame = st.session_state.video_capture.read()
                if not ret:
                    st.error("Failed to capture frame from camera")
                    return

                detected_text = st.session_state.processor.process_image(frame)
                
                if detected_text:
                    new_item = {
                        "item_name": item_name,
                        "quantity": item_quantity,
                        "description": item_description,
                        "ocr_text": detected_text
                    }

                    # Read existing data first
                    data_file = Path("data.json")
                    try:
                        if data_file.exists():
                            with open(data_file, 'r') as f:
                                data = json.load(f)
                        else:
                            data = []
                            
                        # Check for duplicate item names
                        if any(item["item_name"] == item_name for item in data):
                            st.error(f"An item with name '{item_name}' already exists!")
                            return
                            
                        # Append new item to existing data
                        data.append(new_item)
                        
                        # Write back all data
                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        st.success("Item added successfully!")
                        st.session_state.processor.reset()
                        
                    except json.JSONDecodeError:
                        st.error("Error reading existing data. File might be corrupted.")
                        # Create new file with just the new item
                        with open(data_file, 'w') as f:
                            json.dump([new_item], f, indent=4)
                        st.warning("Created new data file with current item.")
                else:
                    st.warning("No text detected in the captured image.")
            
            except Exception as e:
                st.error(f"Error adding item: {e}")

    try:
        while True:
            ret, frame = st.session_state.video_capture.read()
            if not ret:
                st.error("Failed to capture frame from camera")
                break

            with col1:
                video_placeholder.image(frame, channels="BGR", use_column_width=True)

            with col2:
                if st.session_state.processor.accumulated_text:
                    text_placeholder.markdown(f"""
                    <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #1f77b4; margin-bottom: 10px;">Detected Text</h2>
                        <p style="font-size: 18px; color: #ffffff;">{st.session_state.processor.accumulated_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    text_placeholder.markdown(f"""
                    <div style="background-color: #000000; padding: 20px; border-radius: 10px;">
                        <h2 style="color: #1f77b4; margin-bottom: 10px;">Detected Text</h2>
                        <p style="font-size: 18px; color: #ffffff;">Waiting for detection...</p>
                    </div>
                    """, unsafe_allow_html=True)

            if not st.runtime.exists():
                break

    except Exception as e:
        st.error(f"Error in video processing: {e}")

def list_checker():
    st.title("List Checker")
    
    try:
        data_file = Path("data.json")
        if data_file.exists():
            with open(data_file, 'r') as f:
                items = json.load(f)
            
            item_names = [item["item_name"] for item in items]
            selected_item = st.selectbox("Select an item to check:", item_names)
            
            if st.button("Check Item", key="check_item_btn"):
                item = next((item for item in items if item["item_name"] == selected_item), None)
                if item:
                    st.write("Item Details:")
                    st.json(item)
                else:
                    st.warning("Item not found")
        else:
            st.warning("No items in database")
    
    except Exception as e:
        st.error(f"Error loading items: {e}")

def main():
    st.set_page_config(page_title="Inventory Management System", layout="wide")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ['Item Identifier', 'List Checker', 'Add New Item'])

    if page == 'Item Identifier':
        item_identifier()
    elif page == 'List Checker':
        list_checker()
    elif page == 'Add New Item':
        add_new_item()

if __name__ == "__main__":
    main()