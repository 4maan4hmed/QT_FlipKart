import cv2
from OCR import OCRProcessor  # Import the OCRProcessor class from OCR module
from comparision import compare

# Changed to relative path
path = "./Output/output_ocr_text.txt"

def main():
    # Initialize the OCR processor
    ocr_processor = OCRProcessor()

    # Capture video from webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Error: Unable to access the camera.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ocr_output=ocr_processor.process_image(frame)
            print(f'ocr output:  {ocr_output}!!!!!!!')

            Item_detected=compare(ocr_output)
            print(f'Item Detected: {Item_detected}!!!!!!!!!!')

            # Display the live feed with the frame
            cv2.imshow('OCR Detection (Press Q to quit, Enter to reset)', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  
            elif key == 13:  
                ocr_processor.reset_accumulated_text()  

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
