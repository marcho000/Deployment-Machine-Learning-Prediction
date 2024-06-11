import streamlit as st
from PIL import Image
import logging
from prediction_page import display_prediction

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    menu = ['Home', 'Machine Learning Prediction Diamonds']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        display_homepage()
    elif choice == 'Machine Learning Prediction Diamonds':
        display_prediction()

def display_homepage():
    st.subheader('Welcome Homepage Diamonds Prediction')

    # Menyertakan CSS untuk mengatur tampilan halaman
    st.markdown(
        """
        <style>
        .full-width {
            width: 100%;
        }
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }
        .homepage-bg {
            background-color: #34495e; 
            padding: 20px;
            border-radius: 10px;
            color: black; /* Atur warna teks */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Konten homepage
    st.write("""
        Website ini bertujuan untuk melakukan prediksi harga berlian.
        Inputan pada website harus berdasarkan karakteristik dari atribut berlian agar menghasilkan prediksi yang baik.
        Silakan gunakan website ini dengan kenyamanan Anda untuk melakukan prediksi harga berlian.
    """)

    # Tampilkan logo
    image = Image.open('logo.jpeg')
    st.image(image, caption='copyright © 2024 By Insight Squad', use_column_width=True)

    # Fitur Interaktif
    if st.button("To Prediction Diamonds", key="to_prediction"):
        pass  # Biarkan aliran program berlanjut ke bagian selanjutnya

    # Testimonial atau Review
    st.write("""
        "Enjoy Your Life and Happy Prediction"
    """)

if __name__ == '__main__':
    main()