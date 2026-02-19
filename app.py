from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f]

# Full info dictionary for all 10 classes
info = {
    "eczema": {
        "symptoms": "Itching, dry skin, red patches",
        "precautions": "Use moisturizers, avoid irritants",
        "medicines": "Topical corticosteroids, antihistamines",
        "consultation": "See a dermatologist if condition worsens"
    },
    "melanoma": {
        "symptoms": "New or changing mole, irregular borders",
        "precautions": "Avoid sun exposure, use sunscreen",
        "medicines": "Surgical removal, immunotherapy",
        "consultation": "Immediate consultation required"
    },
    "atopic dermatitis": {
        "symptoms": "Red, itchy rash often behind knees or elbows",
        "precautions": "Avoid allergens, use gentle skin care",
        "medicines": "Steroid creams, moisturizers",
        "consultation": "Dermatologist visit if persistent"
    },
    "basal cell carcinoma (bcc)": {
        "symptoms": "Shiny bumps or scars, non-healing sores",
        "precautions": "Sun protection, regular skin checks",
        "medicines": "Excision surgery, topical therapy",
        "consultation": "Required for diagnosis and treatment"
    },
    "melanocytic nevi (nv)": {
        "symptoms": "Small brown or black moles",
        "precautions": "Monitor for changes, avoid excessive sun",
        "medicines": "Usually not required unless atypical",
        "consultation": "Optional, unless changes occur"
    },
    "benign keratosis-like lesions (bkl)": {
        "symptoms": "Waxy, raised, brown or black spots",
        "precautions": "Sun protection",
        "medicines": "Cryotherapy or curettage if bothersome",
        "consultation": "Optional, cosmetic or if irritated"
    },
    "psoriasis": {
        "symptoms": "Thick, red patches with silvery scales",
        "precautions": "Moisturize, reduce stress",
        "medicines": "Topical corticosteroids, biologics",
        "consultation": "Recommended for long-term management"
    },
    "seborrheic keratoses": {
        "symptoms": "Brown, black, or pale warty growths",
        "precautions": "Generally harmless, monitor appearance",
        "medicines": "Cryotherapy, curettage if needed",
        "consultation": "Not usually required unless concerning"
    },
    "tinea ringworm candidiasis": {
        "symptoms": "Itchy, red, ring-shaped rash or white patches",
        "precautions": "Keep skin dry and clean",
        "medicines": "Antifungal creams or oral antifungals",
        "consultation": "Consultation recommended if persistent"
    },
    "warts molluscum": {
        "symptoms": "Small, skin-colored or white bumps",
        "precautions": "Avoid contact, don't scratch",
        "medicines": "Cryotherapy, topical treatments",
        "consultation": "Optional unless widespread"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']

    # Preprocess image
    img = Image.open(image).convert("RGB").resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    prediction = np.argmax(output_data)
    label = labels[prediction].strip()
    clean_label = label.lower()


    print(f"Predicted index: {prediction}, Label: {label}")

    result = info.get(clean_label, {
        "symptoms": "Unknown",
        "precautions": "Consult a doctor",
        "medicines": "Unknown",
        "consultation": "Required"
    })

    return jsonify(label=label, **result)

if __name__ == '__main__':
    app.run(debug=True)


