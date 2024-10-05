from pyzbar.pyzbar import decode

def barcode_number(img):
    barcode_num_list = []
    barcodes = decode(img)
    total_barcodes=len(barcodes)
    
    for barcode in  barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_num_list.append(barcode_data)
    return barcode_num_list