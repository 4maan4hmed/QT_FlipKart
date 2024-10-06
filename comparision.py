from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dictionary of pre-saved OCR data
def compare(text):
    ocr_data = {
        "Odonil": "MIST Odonil Lavender Lavende Odoni Odon ROON Lavend 85.5g/150m Laver your home ROOM SPRA ovenderMIST one leel special.",
        "Lays": "Layz Salt Lay Salted Potto Chips Lay Salt Papto Crisp Chlps 120g Crunchy L Potatoes",
        "Colgate Toothpaste": "Coegate Coolgate Clastic Paste Tolgate Totpaste 100g For yourr Smile",
        "Dove Shampoo": "Doove Shampoo Hair Treamnet Dove Smooth Haair Sooth Treem 250ml Shappo",
        "Maggi Noodles": "Magi 2-minute Neodle Masala Nodle 70g Packets Fast Cook Easy Meel",
        "Tata Salt": "Taata Slat Pure Tataslod 1kg Lodine Your Healthy Choice Pure Lodized Salts",
        "Pepsi": "Pepsy Pepsi Can Refresh Peepi 330ml Carbonated Drink Cold Sippa",
        "Pantene Shampoo": "Pantee Pantten Smooth Hair Spa Smoothen Pantinne Treatmnt Hairfall Control Shampoo",
        "Coca-Cola": "Coca Colaa Coke Coc Cola Refreshing Sparkle 500ml Carbonnated Beverage Cak",
        "Surf Excel": "Surrf Exel Surf Detargnt Excel Quick Wash Powdr Detergat Sur 1kg Pack",
        "Parle-G": "Parle G Biscuuit Parc-G Gluco Bisccuit Snacky Light Biscut ParleG Pockets 150g",
        "KitKat": "KitKat Chokolate KatKat Crisp 4 Finger Chocolte Break Share KtKat Bar 45g",
        "Nescafe Coffee": "Neskafee Coffe Nest Caffee Classik 100g Jar Refrehing Rich Taste",
        "Dettol Soap": "Dettol Soop Antiseptic Soap Bar Protect Detoll 75g Cleann Hygiene Skin",
        "Red Bull": "RedBul Energy Drink Redbul Power Bull 250ml Energjy Can Refresh Youu",
        "Hershey's Syrup": "Hershys Choko Syup Hershey Syrup Rich Chocolatey Sauce Dessrt Drzzle 680g",
        "Amul Butter": "Amool Buttarr Amul Pasteurized Butter 100g Fresh Creamy Milky Spread",
        "Britannia Rusk": "Britania Rusks Tea Time Slices Britann Ruskk Toasty Crispy 200g Pack",
        "Lux Soap": "Lax Soap Luux Beautyy Soap Bar Silky Smooth 125g Forr Soft Skin",
        "Sprite": "Spright Sprite Lemon Lime Lemony Fresh Spright Drink 500ml Can Zesty Fizz",
        "Kellogg's Corn Flakes": "Kelogs Corn Flakes Breakfasst Cereal Crunchy Crnflakes Box 250g Healthy",
        "Vaseline": "Vasilne Vaslin Petroleum Jelly Skin Carre Moistur Vasil 50ml Jelly",
        "Bournvita": "Bourvitaa Cadbury Bourne Vita Health Drink Chocolte Flavour Nutritio 500g",
        "Head & Shoulders Shampoo": "Hedd Shoulder Anti Dandruff Head Shouldrs Shampoo 180ml Clean Hairr Scalp",
        "HK Vital Iron Pills":"hkvitals hk vitals ron+Folic Acid Iron+Folic ron+ Folic Acid hkvitals. HEALTH SUPPLEMENT FOR WOMEN Folic Acid Iron+Folic A +Folic Acid vitals. ",
        "Nestle Milk": "Nestlee Milkk Nesle Full Cream Millk Pure 1 Litre Fresh Pack Homogenisd",
        "Biotique":"Sunscreen ALOEVERA BIOTIQUE 100% UVA SUN SHIEL OTIQUE SHIELD SUN SHIELD BIOTIQU LOEVERA Protective Lotion AYURVEDIC RECPE PA+- SOOL ",
        "Nivia Facewash":"NIVEA MEN AirCool CONTROL Mint Crystal 110 FACE WASH FACEWASH 710 005808 ",
        "Toothpaste":"SENSODYNE Fresh Gel Net wt. FOR DENTAL USE ONLY DENTIST RECOMMENDED BRAND 150 g FORDENTAL USE ONLY DENTIST RECOMMENDED SRAND A . ",
        "Minimalist":"Minimalist Salicylic HideNothing. 02% CLEANSER Acid+LHA Acid +LHA reduces sebum &acne "

    }


    # OCR result from camera (with errors)
    ocr_camera_result = text

    # Combine all texts
    texts = list(ocr_data.values())
    texts.append(ocr_camera_result)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer().fit_transform(texts)
    vectors = vectorizer.toarray()

    # Cosine similarity between camera result and all pages
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()

    # Find the page with the highest similarity score
    most_similar_index = cosine_similarities.argmax() # +1 for page number
    most_similar_item = list(ocr_data.keys())[most_similar_index]
    similarity_score = cosine_similarities.max()

    # Output result
    print(f"The page is most likely: {most_similar_item} with similarity: {similarity_score:.2f}")
    return most_similar_item
