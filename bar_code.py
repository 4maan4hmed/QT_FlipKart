from pyzbar.pyzbar import decode
import cv2

def barcode_number(img):
    barcode_num_list = []
    barcodes = decode(img)
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        if barcode_data not in barcode_num_list:
            barcode_num_list.append(barcode_data)
    
    return barcode_num_list

# Function to save barcode data to a file
def save_barcode_to_file(barcode_list, file_name="C:/Users/amaan/OneDrive/Desktop/VIT/Semester 5/Flipkart Grid/OCR/Final Code/Output/barcode.txt"):
    with open(file_name, 'a') as file:
        for barcode in barcode_list:
            file.write(f"{barcode}\n")

def barcode_from_video_stream():
    # Open the video stream (0 for default webcam)
    cap = cv2.VideoCapture(0)
    detected_barcodes = set()  # To keep track of barcodes already detected

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # If the frame is not captured correctly, break the loop

        # Get barcodes from the current frame
        barcode_list = barcode_number(frame)
        
        new_barcodes = [bc for bc in barcode_list if bc not in detected_barcodes]
        
        if new_barcodes:
            save_barcode_to_file(new_barcodes)
            detected_barcodes.update(new_barcodes)
            print(f"New barcodes detected and saved: {new_barcodes}")
        
        # Display the video stream
        cv2.imshow('Barcode Scanner', frame)
        
        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()
# Example usage
barcode_from_video_stream()