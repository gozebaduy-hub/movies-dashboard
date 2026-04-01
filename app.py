import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Configuración
st.set_page_config(page_title="Dashboard Películas", layout="wide")

# Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Cargar datos
@st.cache_data
def load_data():
    docs = db.collection("movies").stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

df = load_data()

st.title("🎬 Dashboard de Películas")

# ---------------------------
# CHECKBOX → mostrar todos
# ---------------------------
if st.sidebar.checkbox("Mostrar todos los filmes"):
    st.subheader("Listado completo")
    st.dataframe(df)

# ---------------------------
# BUSCAR POR TÍTULO
# ---------------------------
st.sidebar.subheader("Buscar película")

search_text = st.sidebar.text_input("Ingresa título")

if st.sidebar.button("Buscar"):
    result = df[df['name'].str.contains(search_text, case=False, na=False)]
    st.write(result)

# ---------------------------
# FILTRO POR DIRECTOR
# ---------------------------
st.sidebar.subheader("Filtrar por director")

director = st.sidebar.selectbox(
    "Selecciona un director",
    df['director'].dropna().unique()
)

if st.sidebar.button("Filtrar"):
    filtered = df[df['director'] == director]
    st.write(f"Total películas: {len(filtered)}")
    st.dataframe(filtered)

# ---------------------------
# FORMULARIO NUEVO FILME
# ---------------------------
st.sidebar.subheader("Agregar nuevo filme")

with st.sidebar.form("form_movie"):
    name = st.text_input("Nombre")
    director = st.text_input("Director")
    company = st.text_input("Compañía")
    genre = st.text_input("Género")

    submit = st.form_submit_button("Guardar")

    if submit:
        new_movie = {
            "name": name,
            "director": director,
            "company": company,
            "genre": genre
        }

        db.collection("movies").add(new_movie)
        st.success("Película agregada correctamente")