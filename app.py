import streamlit as st
import json
import os

# Función para cargar datos
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Función para guardar datos
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Cargar datos existentes
data = load_data()

st.title("Aplicación de Viviendas y Habitaciones")

# Seleccionar o crear una vivienda
viviendas = list(data.keys())
vivienda = st.sidebar.selectbox("Selecciona una vivienda", ["Crear nueva vivienda"] + viviendas)

if vivienda == "Crear nueva vivienda":
    nueva_vivienda = st.sidebar.text_input("Nombre de la nueva vivienda")
    if st.sidebar.button("Crear vivienda"):
        if nueva_vivienda:
            data[nueva_vivienda] = {}
            save_data(data)
            st.rerun()
else:
    st.header(f"Vivienda: {vivienda}")

    # Seleccionar o crear una habitación
    habitaciones = list(data[vivienda].keys())
    habitacion = st.selectbox("Selecciona una habitación", ["Crear nueva habitación"] + habitaciones)

    if habitacion == "Crear nueva habitación":
        nueva_habitacion = st.text_input("Nombre de la nueva habitación")
        if st.button("Crear habitación"):
            if nueva_habitacion:
                data[vivienda][nueva_habitacion] = []
                save_data(data)
                st.rerun()
    else:
        st.subheader(f"Habitación: {habitacion}")

        # Añadir enlaces (muebles)
        nuevo_enlace = st.text_input("Agregar enlace de un mueble")
        if st.button("Agregar mueble"):
            if nuevo_enlace:
                data[vivienda][habitacion].append(nuevo_enlace)
                save_data(data)

        # Mostrar enlaces en la habitación
        st.write("**Muebles en esta habitación:**")
        for enlace in data[vivienda][habitacion]:
            st.write(f"- [{enlace}]({enlace})")

# Opciones para guardar y compartir
st.sidebar.markdown("---")
st.sidebar.subheader("Opciones")

# Botón para exportar datos
if st.sidebar.button("Exportar datos"):
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
    save_data(data)
    st.rerun()
