import pytesseract
from PIL import Image
import cv2
import numpy as np 
import os

def fake_forgery_check(image_path):
	# Check for tampering: detect too much contrast (simulating tampering)
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 100, 200)
	edges_density = np.sum(edges > 0) / edges.size
	return edges_density < 0.05 #Threshold: lower density = less likely forged

def extract_text_from_image(image_path):
	img = Image.open(image_path)
	text = pytesseract.image_to_string(img)
	return text

def fake_ai_verify(image_path):
	text = extract_text_from_image(image_path)
	is_genuine = fake_forgery_check(image_path)

	return {
		"text": text,
		"verified": bool(text.strip()) and is_genuine,
		"reason": "Clear text found and no tampering detected" if is_genuine else "Possible tampering or unclear text"
	}