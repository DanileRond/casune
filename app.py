import streamlit as st
import json
import os

# Inicializar el estado de la sesión
if 'data' not in st.session_state:
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = {}

data = st.session_state.data

st.title("Aplicación de Viviendas y Habitaciones")

# Seleccionar o crear una vivienda
viviendas = list(data.keys())
vivienda = st.sidebar.selectbox("Selecciona una vivienda", ["Crear nueva vivienda"] + viviendas, key='vivienda_select')

if vivienda == "Crear nueva vivienda":
    nueva_vivienda = st.sidebar.text_input("Nombre de la nueva vivienda", key='nueva_vivienda')
    if st.sidebar.button("Crear vivienda", key='crear_vivienda'):
        if nueva_vivienda:
            data[nueva_vivienda] = {}
            with open('data.json', 'w') as f:
                json.dump(data, f)
            st.session_state.vivienda_select = nueva_vivienda  # Actualizar selección
            st.rerun()
else:
    st.header(f"Vivienda: {vivienda}")

    # Seleccionar o crear una habitación
    habitaciones = list(data[vivienda].keys())
    habitacion = st.selectbox("Selecciona una habitación", ["Crear nueva habitación"] + habitaciones, key='habitacion_select')

    if habitacion == "Crear nueva habitación":
        nueva_habitacion = st.text_input("Nombre de la nueva habitación", key='nueva_habitacion')
        if st.button("Crear habitación", key='crear_habitacion'):
            if nueva_habitacion:
                data[vivienda][nueva_habitacion] = []
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                st.session_state.habitacion_select = nueva_habitacion  # Actualizar selección
                st.rerun()
    elif habitacion:
        st.subheader(f"Habitación: {habitacion}")

        # Añadir enlaces (muebles)
        nuevo_enlace = st.text_input("Agregar enlace de un mueble", key='nuevo_enlace')
        if st.button("Agregar mueble", key='agregar_mueble'):
            if nuevo_enlace:
                data[vivienda][habitacion].append(nuevo_enlace)
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                st.rerun()

        # Mostrar enlaces en la habitación
        st.write("**Muebles en esta habitación:**")
        for enlace in data[vivienda][habitacion]:
            st.write(f"- [{enlace}]({enlace})")

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
    with open('data.json', 'w') as f:
        json.dump(data, f)
    st.rerun()
