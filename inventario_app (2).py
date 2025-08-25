
import streamlit as st
import pandas as pd
import os
from datetime import datetime, time

# Configuración de la página
st.set_page_config(page_title="INVENTARIO LUBRIREPUESTOS THE GARAGE", layout="wide")
st.markdown("<h1 style='text-align: center; color: #333;'>INVENTARIO LUBRIREPUESTOS THE GARAGE</h1>", unsafe_allow_html=True)

# Estilo personalizado
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f2f2f2;
    }
    .css-1v3fvcr {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Función para mostrar los pasos
def mostrar_pasos():
    st.markdown("### Pasos para usar la app:")
    pasos = [
        "1. Subir archivo de inventario.",
        "2. Presionar el botón 'Analizar'.",
        "3. Esperar que se procese.",
        "4. Elegir una categoría.",
        "5. Revisar los productos."
    ]
    for paso in pasos:
        st.markdown(f"- {paso}")

mostrar_pasos()

# Subida de archivos
st.markdown("### Subir archivo de inventario")
uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])

# Guardar archivo con fecha si se sube
if uploaded_file:
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"inventario_{fecha_actual}.xlsx"
    with open(nombre_archivo, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Archivo guardado como {nombre_archivo}")

# Mostrar archivos disponibles
archivos = [f for f in os.listdir() if f.startswith("inventario_") and f.endswith(".xlsx")]
archivo_seleccionado = st.selectbox("Selecciona un archivo para analizar", archivos)

# Botón Analizar
if st.button("Analizar", type="primary"):
    with st.spinner("Analizando..."):
        df = pd.read_excel(archivo_seleccionado, engine="openpyxl")
        st.success("¡Análisis completo!")

        # Mostrar resumen de ganancias
        if "Categoría" in df.columns and "Ganancia" in df.columns:
            resumen = df.groupby("Categoría")["Ganancia"].sum().reset_index()
            st.markdown("### Resumen de ganancias por categoría")
            st.dataframe(resumen)
            resumen.to_excel("Resumen_Ganancias.xlsx", index=False)
            st.download_button("Descargar resumen", data=open("Resumen_Ganancias.xlsx", "rb").read(), file_name="Resumen_Ganancias.xlsx")

        # Menú de categorías
        if "Categoría" in df.columns:
            categorias = df["Categoría"].unique().tolist()
            categoria_seleccionada = st.selectbox("Selecciona una categoría", categorias)
            productos_categoria = df[df["Categoría"] == categoria_seleccionada]
            st.markdown(f"### Productos en la categoría: {categoria_seleccionada}")
            st.dataframe(productos_categoria)

            # Alertas de bajo inventario (solo entre 8am y 6pm)
            hora_actual = datetime.now().time()
            if time(8, 0) <= hora_actual <= time(18, 0):
                bajo_stock = productos_categoria[productos_categoria["Cantidad"] <= 1]
                if not bajo_stock.empty:
                    st.warning("⚠️ Alerta: Hay productos con 1 o 0 unidades disponibles.")
                    st.dataframe(bajo_stock)
