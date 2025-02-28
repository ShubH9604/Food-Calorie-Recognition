import streamlit as st
from PIL import Image
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import os

model = load_model('FoodCalorieRecognition.h5')

labels = {
    0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
    7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
    14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce', 19: 'mango', 20: 'onion', 21: 'orange',
    22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish',
    29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'
}

fruits = [
    'Apple', 'Banana', 'Bell Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Mango', 'Orange',
    'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon'
]

vegetables = [
    'Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
    'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
    'Tomato', 'Turnip'
]

calorie_data = {
    'Apple': '52 calories per 100g', 'Banana': '96 calories per 100g', 'Beetroot': '43 calories per 100g',
    'Bell Pepper': '20 calories per 100g', 'Cabbage': '25 calories per 100g', 'Capsicum': '20 calories per 100g',
    'Carrot': '41 calories per 100g', 'Cauliflower': '25 calories per 100g', 'Chilli Pepper': '40 calories per 100g',
    'Corn': '86 calories per 100g', 'Cucumber': '15 calories per 100g', 'Eggplant': '25 calories per 100g',
    'Garlic': '149 calories per 100g', 'Ginger': '80 calories per 100g', 'Grapes': '69 calories per 100g',
    'Jalepeno': '29 calories per 100g', 'Kiwi': '61 calories per 100g', 'Lemon': '29 calories per 100g',
    'Lettuce': '15 calories per 100g', 'Mango': '60 calories per 100g', 'Onion': '40 calories per 100g',
    'Orange': '47 calories per 100g', 'Paprika': '282 calories per 100g', 'Pear': '57 calories per 100g',
    'Peas': '81 calories per 100g', 'Pineapple': '50 calories per 100g', 'Pomegranate': '83 calories per 100g',
    'Potato': '77 calories per 100g', 'Raddish': '16 calories per 100g', 'Soy Beans': '446 calories per 100g',
    'Spinach': '23 calories per 100g', 'Sweetcorn': '86 calories per 100g', 'Sweetpotato': '86 calories per 100g',
    'Tomato': '18 calories per 100g', 'Turnip': '28 calories per 100g', 'Watermelon': '30 calories per 100g'
}

def get_calories(food):
    return calorie_data.get(food, "Calorie information not available")

def prepare_image(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    y_class = prediction.argmax(axis=-1)[0]
    res = labels[y_class]

    return res.capitalize()

def run():
    st.title("🍍 Food Calorie Recognition 🍅")

    img_file = st.file_uploader("Choose an Image", type=["jpg", "png", "jpeg"])

    if img_file is not None:
        col1, col2 = st.columns([1, 1.5])

        with col1:
            img = Image.open(img_file).resize((300, 300))
            st.image(img, use_container_width=False)

            if not os.path.exists('./upload_images'):
                os.makedirs('./upload_images')

            save_image_path = f'./upload_images/{img_file.name}'
            with open(save_image_path, "wb") as f:
                f.write(img_file.getbuffer())

            result = prepare_image(save_image_path)

        with col2:
            st.subheader("Prediction Results")
            st.success(f"**Predicted: {result}**")

            if result in vegetables:
                st.info('**Category: Vegetable**')
                category = 'Vegetable'
            else:
                st.info('**Category: Fruit**')
                category = 'Fruit'

            calories = get_calories(result)
            st.warning(f"**{calories}**")

if __name__ == '__main__':
    run()
