=======
# Inventory Management System

A Streamlit-based inventory management system that combines OCR (Optical Character Recognition) and barcode scanning capabilities. The system allows users to identify items, manage inventory, and add new items through a user-friendly web interface.

## Features

- Real-time item identification using OCR
- Barcode scanning integration
- Item database management
- Three main functionalities:
  - Item Identifier: Real-time item detection through camera
  - List Checker: View and verify item details
  - Add New Item: Add new items to the inventory database

## Prerequisites

- Python 3.6 or higher
- Webcam or USB camera
- CUDA-compatible GPU (optional, for faster OCR processing)

## Installation

1. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install streamlit
pip install opencv-python
pip install paddleocr
pip install pyzbar
```

3. Additional system dependencies for Linux:
```bash
# Ubuntu/Debian
sudo apt-get install libzbar0
sudo apt-get install libgl1-mesa-glx

# Fedora
sudo dnf install zbar
```

## Project Structure

```
inventory-system/
│
├── main.py              # Main Streamlit application
├── comparision.py       # Item comparison functionality
├── data_operation.py    # Data operations helper
├── data.json           # Item database
└── output_ocr_text.txt # OCR output storage
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. The application will open in your default web browser with three main sections:

### Item Identifier
- Shows real-time camera feed
- Automatically detects and identifies items using OCR
- Displays detected item details
- "Next Item" button to reset detection

### List Checker
- View all items in the database
- Select and check detailed information about specific items
- Verify item details and inventory status

### Add New Item
- Capture new items through the camera
- Add item details:
  - Item name
  - Quantity
  - Description
- OCR text is automatically captured and stored
- Items are saved to the database (data.json)

## Components

### OCRProcessor Class
- Handles OCR processing using PaddleOCR
- Maintains text frequencies and confidences
- Processes images and accumulates detected text
- Identifies items based on accumulated text

### Key Functions

`initialize_session_state()`
- Initializes Streamlit session state variables
- Sets up video capture and OCR processor

`item_identifier()`
- Manages the item identification interface
- Handles real-time video processing and display
- Shows detected item information

`add_new_item()`
- Handles the new item addition interface
- Captures OCR data and item details
- Saves items to the database

`list_checker()`
- Manages the item verification interface
- Displays database items and their details

## Data Storage

- Items are stored in `data.json` with the following structure:
```json
{
    "item_name": "Example Item",
    "quantity": 1,
    "description": "Item description",
    "ocr_text": "Detected OCR text"
}
```

## Troubleshooting

1. Camera Issues:
   - Ensure webcam permissions are granted to the application
   - Check if another application is using the camera
   - Try changing the camera index in `cv2.VideoCapture(0)`

2. OCR Detection Issues:
   - Ensure proper lighting
   - Hold items steady
   - Adjust item position to ensure text is clearly visible

3. Database Issues:
   - Check write permissions for data.json
   - Verify JSON file format if manually edited
   - Ensure unique item names when adding new items

## Error Handling

The application includes error handling for:
- Camera capture failures
- OCR processing errors
- Database read/write operations
- Duplicate item prevention

## Performance Considerations

- OCR processing speed depends on hardware capabilities
- GPU acceleration can be enabled by setting `use_gpu=True` in PaddleOCR initialization
- Consider adjusting `min_confidence` threshold in OCRProcessor for detection accuracy

## Notes

- The system maintains real-time OCR text accumulation for accurate item identification
- Item matching uses frequency-based text comparison
- The interface is designed for ease of use with clear visual feedback
- All data is stored locally in JSON format for easy access and modification
