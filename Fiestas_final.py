import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Cargar los datos desde un archivo CSV
@st.cache_data
def load_data():
    return pd.read_csv("fiestas.csv", encoding="latin1")

data = load_data()

# Renombrar columnas para mayor claridad
data.columns = [
    "Fiesta", "Mes", "Dia", "Departamento", "Provincia", 
    "Distrito", "Latitud", "Longitud", "Extra1", "Extra2", "Extra3"
]

# Seleccionar solo las columnas necesarias
data = data[["Fiesta", "Mes", "Dia", "Departamento", "Provincia", "Distrito", "Latitud", "Longitud"]]

# Convertir coordenadas a valores numéricos
data["Latitud"] = pd.to_numeric(data["Latitud"], errors="coerce")
data["Longitud"] = pd.to_numeric(data["Longitud"], errors="coerce")

# Filtrar filas con datos válidos
data = data.dropna(subset=["Latitud", "Longitud"])

# Título de la aplicación
st.title("Fiestas Tradicionales del Perú")

# Filtros de selección
departamento = st.selectbox("Selecciona un Departamento", options=data["Departamento"].unique())
provincia = st.selectbox(
    "Selecciona una Provincia", 
    options=data[data["Departamento"] == departamento]["Provincia"].unique()
)
distrito = st.selectbox(
    "Selecciona un Distrito",
    options=data[(data["Departamento"] == departamento) & (data["Provincia"] == provincia)]["Distrito"].unique()
)

# Filtrar los datos según las selecciones
filtered_data = data[
    (data["Departamento"] == departamento) &
    (data["Provincia"] == provincia) &
    (data["Distrito"] == distrito)
]

# Mostrar información de la fiesta seleccionada
if not filtered_data.empty:
    fiesta = filtered_data.iloc[0]
    st.subheader(f"Fiesta Seleccionada: {fiesta['Fiesta']}")
    st.write(f"Fecha: {fiesta['Dia']} de {fiesta['Mes']}")
    st.write(f"Ubicación: {fiesta['Distrito']}, {fiesta['Provincia']}, {fiesta['Departamento']}")

    # Crear mapa con Folium
    map = folium.Map(location=[fiesta["Latitud"], fiesta["Longitud"]], zoom_start=12)
    folium.Marker(
        [fiesta["Latitud"], fiesta["Longitud"]],
        popup=f"{fiesta['Fiesta']} ({fiesta['Dia']} de {fiesta['Mes']})",
        tooltip="Haz clic para más información"
    ).add_to(map)

    # Mostrar el mapa en la aplicación
    folium_static(map)
else:
    st.warning("No se encontraron fiestas para esta selección.")

