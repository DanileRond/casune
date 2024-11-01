import streamlit as st
import json
import os
import requests
from PIL import Image
from io import BytesIO

# Inicializar el estado de la sesión
if 'data' not in st.session_state:
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = {}

data = st.session_state.data

st.title("Aplicación de Viviendas y Habitaciones")

# Función para guardar datos
def save_data():
    with open('data.json', 'w') as f:
        json.dump(st.session_state.data, f)

# Manejo del estado de la vivienda seleccionada
if 'vivienda_actual' not in st.session_state:
    st.session_state.vivienda_actual = "Crear nueva vivienda"

# Listado de viviendas
viviendas = list(data.keys())
vivienda_options = ["Crear nueva vivienda"] + viviendas

# Obtener índice de la vivienda seleccionada
if st.session_state.vivienda_actual in vivienda_options:
    vivienda_index = vivienda_options.index(st.session_state.vivienda_actual)
else:
    vivienda_index = 0  # Por defecto, "Crear nueva vivienda"

# Seleccionar o crear una vivienda
vivienda = st.sidebar.selectbox("Selecciona una vivienda", vivienda_options, index=vivienda_index)

if vivienda == "Crear nueva vivienda":
    nueva_vivienda = st.sidebar.text_input("Nombre de la nueva vivienda")
    if st.sidebar.button("Crear vivienda"):
        if nueva_vivienda and nueva_vivienda not in viviendas:
            data[nueva_vivienda] = {}
            save_data()
            st.session_state.vivienda_actual = nueva_vivienda
            st.rerun()
        else:
            st.sidebar.error("El nombre de la vivienda ya existe o es inválido.")
else:
    st.session_state.vivienda_actual = vivienda
    st.header(f"Vivienda: {vivienda}")

    # Manejo del estado de la habitación seleccionada
    if 'habitacion_actual' not in st.session_state:
        st.session_state.habitacion_actual = "Crear nueva habitación"

    # Listado de habitaciones
    habitaciones = list(data[vivienda].keys())
    habitacion_options = ["Crear nueva habitación"] + habitaciones

    # Obtener índice de la habitación seleccionada
    if st.session_state.habitacion_actual in habitacion_options:
        habitacion_index = habitacion_options.index(st.session_state.habitacion_actual)
    else:
        habitacion_index = 0  # Por defecto, "Crear nueva habitación"

    # Seleccionar o crear una habitación
    habitacion = st.selectbox("Selecciona una habitación", habitacion_options, index=habitacion_index)

    if habitacion == "Crear nueva habitación":
        nueva_habitacion = st.text_input("Nombre de la nueva habitación")
        if st.button("Crear habitación"):
            if nueva_habitacion and nueva_habitacion not in habitaciones:
                data[vivienda][nueva_habitacion] = []
                save_data()
                st.session_state.habitacion_actual = nueva_habitacion
                st.rerun()
            else:
                st.error("El nombre de la habitación ya existe o es inválido.")
    else:
        st.session_state.habitacion_actual = habitacion
        st.subheader(f"Habitación: {habitacion}")

        # Añadir enlaces (muebles)
        nuevo_enlace = st.text_input("Agregar enlace de un mueble")
        if st.button("Agregar mueble"):
            if nuevo_enlace:
                data[vivienda][habitacion].append(nuevo_enlace)
                save_data()
                st.rerun()

        # Mostrar enlaces en la habitación
        st.write("**Muebles en esta habitación:**")
        for enlace in data[vivienda][habitacion]:
            st.write(f"- [{enlace}]({enlace})")
            # Intentar mostrar una miniatura
            try:
                if enlace.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    st.image(enlace, width=150)
                else:
                    # Intentar obtener la imagen del sitio web
                    response = requests.get(enlace, timeout=5)
                    if response.status_code == 200:
                        # Esto es un simplificación; obtener una imagen de un sitio web requiere parsing
                        # Para mantenerlo simple, no lo implementaremos aquí
                        pass
            except Exception as e:
                st.write("No se pudo cargar la miniatura.")

# Opciones para guardar y compartir
st.sidebar.markdown("---")
st.sidebar.subheader("Opciones")

# Botón para exportar datos
st.sidebar.download_button(
    label="Descargar datos",
    data=json.dumps(data),
    file_name='data.json',
    mime='application/json'
)

# Botón para importar datos
archivo_subido = st.sidebar.file_uploader("Importar datos", type=['json'])
if archivo_subido is not None:
    data = json.load(archivo_subido)
    st.session_state.data = data
    save_data()
    st.rerun()
