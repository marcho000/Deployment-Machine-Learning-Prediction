import streamlit as st
import pandas as pd
import pickle
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fungsi bantuan untuk memuat model machine learning dengan error handling
def load_model(model_file):
    try:
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        logging.info(f"Model {model_file} loaded successfully.")
        return model
    except FileNotFoundError:
        st.error(f"Model file {model_file} not found.")
        logging.error(f"Model file {model_file} not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        logging.error(f"An error occurred while loading the model {model_file}: {e}")
        return None

# Fungsi untuk memuat model, encoder, dan scaler dengan error handling
def load_pickle_files():
    encoders = load_model('LabelEncoder_encoders.pkl')
    scaler = load_model('RXrobust_Scaler.pkl')
    model = load_model('catboost_model.pkl')
    return encoders, scaler, model

# Fungsi untuk menampilkan form input dan memproses prediksi
def display_prediction():
    st.subheader('Welcome To Diamond Price Prediction')
    st.expander("Attribute Info").markdown(attribute_info)

    # Form untuk input pengguna
    with st.form("prediction_form"):
        carat = st.number_input('Carat', min_value=0.2, max_value=5.01, step=0.01)
        cut = st.selectbox('Cut', ['Ideal', 'Premium', 'Good', 'Very Good', 'Fair'])
        color = st.selectbox('Color', ['E', 'I', 'J', 'H', 'F', 'G', 'D'])
        clarity = st.selectbox('Clarity', ['SI2', 'SI1', 'VS1', 'VS2', 'VVS2', 'VVS1', 'I1', 'IF'])
        depth = st.number_input('Depth', min_value=43.0, max_value=79.0, step=0.1)
        table = st.number_input('Table', min_value=43.0, max_value=95.0, step=0.1)
        panjang_berlian = st.number_input('Panjang Berlian', min_value=0.0, max_value=10.74, step=0.01)
        lebar_berlian = st.number_input('Lebar Berlian', min_value=0.0, max_value=58.9, step=0.01)
        kedalaman_berlian = st.number_input('Kedalaman Berlian', min_value=0.0, max_value=31.8, step=0.01)

        # Ganti koma dengan titik pada input pengguna (jika berlaku)
        carat = str(carat).replace(',', '.')
        depth = str(depth).replace(',', '.')
        table = str(table).replace(',', '.')
        panjang_berlian = str(panjang_berlian).replace(',', '.')
        lebar_berlian = str(lebar_berlian).replace(',', '.')
        kedalaman_berlian = str(kedalaman_berlian).replace(',', '.')

        submit = st.form_submit_button("Predict")

        if submit:
            new_data = pd.DataFrame({
                'carat': [carat],
                'cut': [cut],
                'color': [color],
                'clarity': [clarity],
                'depth': [depth],
                'table': [table],
                'panjang_berlian': [panjang_berlian],
                'lebar_berlian': [lebar_berlian],
                'kedalaman_berlian': [kedalaman_berlian]
            })

            # Memuat model, encoder, dan scaler
            encoders, scaler, model = load_pickle_files()

            # Cek apakah model, encoder, dan scaler berhasil dimuat
            if encoders is None or scaler is None or model is None:
                st.error("Failed to load model, encoders, or scaler. Please check the files and try again.")
                logging.error("Failed to load model, encoders, or scaler.")
                return

            # Proses label encoding untuk kolom kategorikal
            object_cols = ['cut', 'color', 'clarity']
            try:
                for col in object_cols:
                    new_data[col] = encoders[col].transform(new_data[col])
                logging.info("Label encoding applied successfully.")
            except Exception as e:
                st.error(f"An error occurred during label encoding: {e}")
                logging.error(f"An error occurred during label encoding: {e}")
                return

            # Proses scaling
            try:
                new_data_scaled = scaler.transform(new_data)
                logging.info("Data scaling applied successfully.")
            except Exception as e:
                st.error(f"An error occurred during data scaling: {e}")
                logging.error(f"An error occurred during data scaling: {e}")
                return

            # Melakukan prediksi
            try:
                prediction = model.predict(new_data_scaled)
                st.success(f"Your Diamond Price Prediction: ${str(prediction[0]).replace(',', '.'):s}")
                logging.info("Prediction made successfully.")

                # Menampilkan saran pada pengguna
                if prediction[0] > 5000:
                    st.info("Harga berlian ini menunjukkan nilai yang signifikan. Sebelum melakukan pembelian, disarankan untuk melakukan pengecekan lebih lanjut terhadap kualitas dan keaslian berlian.")
                else:
                    st.info("Harga berlian ini tergolong dalam kisaran yang rendah. Namun, penting untuk memilih berlian yang sesuai dengan kebutuhan dan preferensi Anda.")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
                logging.error(f"An error occurred during prediction: {e}")

attribute_info = """
- Carat (0.2-5.01): Carat adalah berat fisik berlian yang diukur dalam karat.
- Cut : (Ideal, Premium, Good, Very Good, Fair): Model Potongan berlian.
- Color : warna berlian (['E' 'I' 'J' 'H' 'F' 'G' 'D'])
- Clarity (['SI2' 'SI1' 'VS1' 'VS2' 'VVS2' 'VVS1' 'I1' 'IF'])
- Depth (43-79) merupakan tinggi berlian
- Table (43-95): Ini adalah lebar bagian ukuran atas berlian relatif terhadap titik terlebar.
- Panjang berlian : (0 - 10.74 ukuran mm)
- Lebar berlian : (0 - 58.9 ukuran mm)
- Kedalaman berlian : (0 - 31.8 mm)
"""

if __name__ == '__main__':
    display_prediction()