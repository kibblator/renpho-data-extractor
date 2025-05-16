import pytesseract
import cv2
import os
from injector import singleton, inject
from data_extraction import extract_properties
from weight_data_repository import WeightDataRepository

DEBUG_MODE = False

class ImageProcessorService:
    @inject
    @singleton
    def __init__(self, weight_data_repository: WeightDataRepository):
        self.weight_data_repository = weight_data_repository

    def image_to_text(self, image_path):
        print('Processing image')
        img = cv2.imread(image_path)

        resized_img = cv2.resize(img, None, fx=3, fy=2.5, interpolation=cv2.INTER_LANCZOS4)

        gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        final = invert

        if DEBUG_MODE:
            cv2.imwrite('processed_image.png', final)

        height, width = final.shape[:2] 

        column_width = width // 3

        extracted_text = []
        for i in range(3):
            start_x = i * column_width
            end_x = min(start_x + column_width, width)
            column_img = final[:, start_x:end_x]
            column_text = pytesseract.image_to_string(column_img, lang='eng', config='--oem 3 --psm 4 -l eng+num -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.%')
            if DEBUG_MODE:
                print(column_text)
            column_text = self.process_text(column_text)
            extracted_text.append(column_text)

        joined_text = ' '.join(extracted_text)
        joined_text = ''.join(joined_text.split())

        properties = extract_properties(joined_text)

        json_data = {
            "Weight": properties.get("Weight"),
            "FatFreeMass": properties.get("FatFreeMass"),
            "BodyWater": properties.get("BodyWater"),
            "BoneMass": properties.get("BoneMass"),
            "MetabolicAge": properties.get("MetabolicAge"),
            "BMI": properties.get("BMI"),
            "SubcutaneousFat": properties.get("SubcutaneousFat"),
            "SkeletalMuscle": properties.get("SkeletalMuscle"),
            "Protein": properties.get("Protein"),
            "BodyFat": properties.get("BodyFat"),
            "VisceralFat": properties.get("VisceralFat"),
            "MuscleMass": properties.get("MuscleMass"),
            "BMR": properties.get("BMR")
        }

        os.remove(image_path)

        return json_data

    def process_text(self, text):
        lines = text.split('\n')
        lines = list(filter(None, lines))

        processed_text = []

        for line_index, line in enumerate(lines):
            if any(char.isdigit() for char in line):
                line = ''.join(char for char in line if not char.isalpha())

            if DEBUG_MODE:
                print(f'Processed text: {line}')

            if line[0].isalpha():
                processed_text.append(line)
                continue

            next_line_index = line_index + 1
        
            if next_line_index < len(lines):
                next_line = lines[next_line_index]
                if not next_line[0].isalpha():
                    continue

            processed_text.append(line)

        return '\n'.join(processed_text)
