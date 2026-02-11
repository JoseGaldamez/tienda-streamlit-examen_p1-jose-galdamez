import streamlit as st
import pandas as pd
from datetime import date


st.set_page_config(page_title="ElectroHogar - Examen I Parcial", page_icon="🏪")


PRODUCTOS = [
    {"Nombre": "Refrigeradora LG 14 pies", "Precio": 12500.00, "Categoría": "Línea Blanca"},
    {"Nombre": "Lavadora Whirlpool 18kg", "Precio": 9800.00, "Categoría": "Línea Blanca"},
    {"Nombre": "Microondas Panasonic", "Precio": 3200.00, "Categoría": "Cocina"},
    {"Nombre": "Licuadora Oster", "Precio": 1500.00, "Categoría": "Cocina"},
    {"Nombre": "Aire Acondicionado 12000 BTU", "Precio": 8500.00, "Categoría": "Climatización"},
    {"Nombre": "Plancha Black+Decker", "Precio": 650.00, "Categoría": "Hogar"},
    {"Nombre": "Televisor Samsung 55' 4K", "Precio": 14000.00, "Categoría": "Entretenimiento"},
    {"Nombre": "Cafetera Hamilton Beach", "Precio": 1200.00, "Categoría": "Cocina"},
    {"Nombre": "Estufa de Gas 4 Quemadores", "Precio": 5500.00, "Categoría": "Cocina"},
    {"Nombre": "Ventilador de Pedestal", "Precio": 900.00, "Categoría": "Climatización"}
]


df_productos = pd.DataFrame(PRODUCTOS)


st.title("ElectroHogar - Tienda de Electrodomésticos")
st.subheader("Examen Parcial I - José Galdámez")
st.markdown("---")


st.sidebar.header("Datos del Cliente")
nombre_cliente = st.sidebar.text_input("Nombre del Cliente")
rtn_cliente = st.sidebar.text_input("RTN / Identidad")
fecha_factura = st.sidebar.date_input("Fecha", value=date.today())


st.header("Catálogo de Productos")


st.markdown("### Filtros")
    
precio_max = int(df_productos["Precio"].max())
precio_min = int(df_productos["Precio"].min())
rango_precio = st.slider(
    "Filtrar por Precio Máximo (L.)",
        min_value=precio_min,
        max_value=precio_max,
        value=precio_max,
        step=500
    )

df_filtrado = df_productos[df_productos["Precio"] <= rango_precio]
st.markdown(f"### Productos Disponibles ({len(df_filtrado)})")
st.dataframe(
    df_filtrado.style.format({"Precio": "L. {:,.2f}"}),
    use_container_width=True,
    hide_index=True
    )


st.markdown("---")


st.header("Selección de Compra")

col_compra1, col_compra2 = st.columns(2)

with col_compra1:
    
    producto_seleccionado_nombre = st.selectbox(
        "Seleccione un producto:",
        options=df_productos["Nombre"].tolist()
    )
    
    
    producto_info = df_productos[df_productos["Nombre"] == producto_seleccionado_nombre].iloc[0]
    precio_unitario = producto_info["Precio"]
    categoria_prod = producto_info["Categoría"]

with col_compra2:

    cantidad = st.number_input("Cantidad:", min_value=1, value=1, step=1)
    subtotal_producto = precio_unitario * cantidad


st.info(f"""
**Producto:** {producto_seleccionado_nombre} ({categoria_prod})  
**Precio Unitario:** L. {precio_unitario:,.2f}  
**Subtotal:** L. {subtotal_producto:,.2f}
""")

st.markdown("---")


st.header("Resumen de Facturación")

if nombre_cliente and rtn_cliente:
    # Cálculos Finales
    subtotal_general = subtotal_producto
    impuesto_isv = subtotal_general * 0.15
    total_pagar = subtotal_general + impuesto_isv

    # Diseño de la factura
    with st.container(border=True):
        st.markdown(f"### Factura Comercial")
        st.markdown(f"**Fecha:** {fecha_factura}")
        st.markdown(f"**Cliente:** {nombre_cliente}")
        st.markdown(f"**RTN:** {rtn_cliente}")
        st.divider()
        
        # Detalle
        col_det1, col_det2, col_det3, col_det4 = st.columns([3, 1, 2, 2])
        col_det1.markdown("**Producto**")
        col_det2.markdown("**Cant.**")
        col_det3.markdown("**Precio Unit.**")
        col_det4.markdown("**Total**")
        
        col_det1.write(producto_seleccionado_nombre)
        col_det2.write(cantidad)
        col_det3.write(f"L. {precio_unitario:,.2f}")
        col_det4.write(f"L. {subtotal_producto:,.2f}")
        
        st.divider()
        
        # Totales
        col_tot1, col_tot2 = st.columns([3, 1])
        col_tot2.markdown(f"**Subtotal:** L. {subtotal_general:,.2f}")
        col_tot2.markdown(f"**ISV (15%):** L. {impuesto_isv:,.2f}")
        col_tot2.markdown(f"### Total: L. {total_pagar:,.2f}")

    st.success("Cálculo de facturación generado exitosamente.")

else:
    st.warning("Por favor ingresa el **Nombre del Cliente** y **RTN** en la barra lateral para generar la factura.")
