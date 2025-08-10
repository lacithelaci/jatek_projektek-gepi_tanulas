import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model # pyright: ignore[reportMissingImports]
import pickle

MODEL_PATH = 'model/my_model.h5'
SCALER_PATH = 'model/scaler.pkl'

@st.cache_resource
def load_artifacts():
    model = load_model(MODEL_PATH)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_artifacts()

st.markdown("# 🌾 Búzafajta osztályozó")
st.markdown("Add meg az értékeket az oldalsávon, majd kattints a predikció gombra.")

with st.sidebar:
    st.header("🔧 Paraméterek")
    terulet = st.slider('Terület', 10.0, 22.0, 15.0, 0.1)
    kerulet = st.slider('Kerület', 12.0, 18.0, 14.5, 0.1)
    kompakt = st.slider('Kompaktság', 0.8, 0.92, 0.87, 0.001)
    szemhossz = st.slider('Szemhossz', 4.8, 6.7, 5.6, 0.01)
    szem_szelesseg = st.slider('Szem szélesség', 2.6, 4.1, 3.25, 0.01)
    asszim = st.slider('Asszimetria együttható', 0.7, 8.5, 3.7, 0.01)
    barazdahossz = st.slider('Barázdahossz', 4.5, 6.6, 5.4, 0.01)

input_data = np.array([[terulet, kerulet, kompakt, szemhossz, szem_szelesseg, asszim, barazdahossz]])
input_scaled = scaler.transform(input_data)

if st.button("📊 Predikció"):
    with st.spinner("Modellezés folyamatban..."):
        pred_proba = model.predict(input_scaled)[0]
        pred_class = np.argmax(pred_proba)
        class_names = ['Kama', 'Rosa', 'Canadian']
        st.success(f"A predikált búzafajta: **{class_names[pred_class]}**")
