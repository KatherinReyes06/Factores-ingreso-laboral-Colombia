import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title='Ingreso Laboral Colombia - GEIH 2025',
    layout='wide'
)

# Estilos personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f7ed;
    }
    h1 {
        color: #243e36;
        text-align: center;
    }
    div[data-baseweb="select"] > div {
        border-color: #7ca982 !important;
    }
    div[data-baseweb="popover"] {
        border-color: #7ca982 !important;
    }        
    div[data-testid="stCaptionContainer"] {
        text-align: center;
    }        
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button[kind="secondary"] {
        width: 100%;
        border: 1.5px solid #243e36;
        background-color: transparent;
        color: #243e36;
        border-radius: 8px;
        padding: 2px 5px;
        font-size: 11px;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button[kind="secondary"]:hover {
        background-color: #7ca982;
        color: white;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] button[kind="primary"] {
        width: 100%;
        background-color: #243e36;
        color: white;
        border: 1.5px solid #243e36;
        border-radius: 8px;
        padding: 2px 5px;
        font-size: 11px;
    }
    </style>
""", unsafe_allow_html=True)


# Cargar datos
datos = pd.read_csv('geih_limpio.csv')

# Título
st.title('Factores que determinan el ingreso laboral en Colombia')
st.caption('Fuente: GEIH 2025 — DANE | Primer semestre (Enero - Junio)')

# Filtro de mes con botones
if 'mes_seleccionado' not in st.session_state:
    st.session_state.mes_seleccionado = 'Global'

meses_opciones = ['Global', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
cols_mes = st.columns(len(meses_opciones))

for i, mes in enumerate(meses_opciones):
    with cols_mes[i]:
        if mes == st.session_state.mes_seleccionado:
            st.button(mes, key=f'btn_{mes}', use_container_width=True, type="primary", disabled=True)
        else:
            if st.button(mes, key=f'btn_{mes}', use_container_width=True):
                st.session_state.mes_seleccionado = mes
                st.experimental_rerun()

if st.session_state.mes_seleccionado == 'Global':
    datos_filtrados = datos.copy()
else:
    datos_filtrados = datos[datos['MES'] == st.session_state.mes_seleccionado].copy()

# Indicadores principales
mediana = f'${datos_filtrados["INGLABO"].median():,.0f}'
encuestados = f'{len(datos_filtrados):,}'
departamentos = f'{datos_filtrados["DEPARTAMENTO"].nunique()}'

st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 50px; margin: 20px 0;">
        <div style="background-color: #243e36; padding: 20px 40px; border-radius: 10px; text-align: center; min-width: 200px;">
            <p style="color: #7ca982; margin: 0; font-size: 14px;">Mediana del ingreso</p>
            <p style="color: white; margin: 0; font-size: 28px; font-weight: bold;">{mediana}</p>
        </div>
        <div style="background-color: #243e36; padding: 20px 40px; border-radius: 10px; text-align: center; min-width: 200px;">
            <p style="color: #7ca982; margin: 0; font-size: 14px;">Encuestados</p>
            <p style="color: white; margin: 0; font-size: 28px; font-weight: bold;">{encuestados}</p>
        </div>
        <div style="background-color: #243e36; padding: 20px 40px; border-radius: 10px; text-align: center; min-width: 200px;">
            <p style="color: #7ca982; margin: 0; font-size: 14px;">Departamentos</p>
            <p style="color: white; margin: 0; font-size: 28px; font-weight: bold;">{departamentos}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# ============================================================
# FILA 1
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">¿Cuánto ganan los colombianos?</h4>
            <p style="color: #7ca982; text-align: center; font-size: 12px; margin: 0;">Por rango de SMLV + auxilio ($1.623.500)</p>
        </div>
    """, unsafe_allow_html=True)
    
    smlv = 1_623_500
    bins = [0, smlv, smlv*3, smlv*6, float('inf')]
    labels = ['< 1 SMLV', '1 - 3 SMLV', '4 - 6 SMLV', '> 6 SMLV']
    
    datos_filtrados['RANGO_INGRESO'] = pd.cut(datos_filtrados['INGLABO'], bins=bins, labels=labels)
    conteo = datos_filtrados['RANGO_INGRESO'].value_counts().reindex(labels).reset_index()
    conteo.columns = ['Rango', 'Cantidad']
    
    colores_torta = ['#243e36', '#3a7a5e', '#7ca982', '#bdd5c4']
    
    fig1 = px.pie(
        conteo, values='Cantidad', names='Rango',
        color_discrete_sequence=colores_torta
    )
    fig1.update_traces(
        text=[f'{p:.1f}%\n({c:,})' for p, c in zip(
            conteo['Cantidad'] / conteo['Cantidad'].sum() * 100, 
            conteo['Cantidad']
        )],
        textinfo='text',
        textposition='outside',
        textfont=dict(size=13, color='#243e36'),
        marker=dict(line=dict(width=0)),
        hovertemplate='%{label}<br>Cantidad: %{value:,}<extra></extra>'
    )
    fig1.update_layout(
        paper_bgcolor='white',
        font=dict(color='#243e36', size=10),
        margin=dict(t=20, b=30, l=10, r=10),
        height=420,
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.02,
            font=dict(size=13)
        )
    )
    
    st.markdown('<div style="margin-top: 36px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">Mediana del ingreso por factor</h4>
        </div>
    """, unsafe_allow_html=True)
    
    factor = st.selectbox('Factor', [
        'NIVEL_EDUCATIVO', 'POSICION',
        'TIENE_CONTRATO', 'CLASE', 'TAMAÑO_EMPRESA'
    ], label_visibility='collapsed')
    
    resumen_factor = datos_filtrados.groupby(factor).agg(
        Mediana=('INGLABO', 'median'),
        Encuestados=('INGLABO', 'count')
    ).sort_values('Mediana').reset_index()
    resumen_factor.columns = ['Factor', 'Mediana', 'Encuestados']
    resumen_factor['Texto'] = resumen_factor.apply(
        lambda row: f'${row["Mediana"]:,.0f} ({row["Encuestados"]:,})', axis=1
    )
    
    fig2 = px.bar(
        resumen_factor, x='Mediana', y='Factor',
        orientation='h', text='Texto',
        color_discrete_sequence=['#7ca982']
    )
    fig2.update_traces(textposition='outside', marker_line_width=0)
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis_title='', yaxis_title='',
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, resumen_factor['Mediana'].max() * 1.4]),
        font=dict(color='#243e36', size=10),
        margin=dict(t=20, b=30, l=10, r=10),
        height=420
    )
    st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# FILA 2
# ============================================================
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">Brecha salarial por sexo y nivel educativo</h4>
            <p style="color: #7ca982; text-align: center; font-size: 12px; margin: 0;"</p>
        </div>
    """, unsafe_allow_html=True)
    
    orden_educacion = [
        'Ninguno', 'Preescolar', 'Básica primaria (1°-5°)', 'Básica secundaria (6°-9°)',
        'Media académica', 'Media técnica', 'Normalista',
        'Técnica profesional', 'Tecnológica', 'Universitaria',
        'Especialización', 'Maestría', 'Doctorado'
    ]
    
    brecha = datos_filtrados.groupby(['NIVEL_EDUCATIVO', 'SEXO'])['INGLABO'].median().unstack()
    brecha = brecha.reindex(orden_educacion).dropna().reset_index()
    
    import plotly.graph_objects as go
    
    fig3 = go.Figure()
    
    # Hombres hacia la izquierda (valores negativos)
    fig3.add_trace(go.Bar(
        y=brecha['NIVEL_EDUCATIVO'],
        x=-brecha['Hombre'],
        orientation='h',
        name='Hombre',
        marker_color='#243e36',
        text=[f'${v:,.0f}' for v in brecha['Hombre']],
        textposition='outside',
        textfont=dict(size=8)
    ))
    
    # Mujeres hacia la derecha
    fig3.add_trace(go.Bar(
        y=brecha['NIVEL_EDUCATIVO'],
        x=brecha['Mujer'],
        orientation='h',
        name='Mujer',
        marker_color='#7ca982',
        text=[f'${v:,.0f}' for v in brecha['Mujer']],
        textposition='outside',
        textfont=dict(size=8)
    ))
    
    max_val = max(brecha['Hombre'].max(), brecha['Mujer'].max()) * 1.3
    
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        barmode='overlay',
        xaxis=dict(
            showgrid=False, showticklabels=False,
            range=[-max_val, max_val],
            zeroline=True, zerolinecolor='#243e36', zerolinewidth=1
        ),
        yaxis_title='',
        font=dict(color='#243e36', size=9),
        margin=dict(t=20, b=30, l=10, r=10),
        height=420,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
    )
    
    st.markdown('<div style="margin-top: 55px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">Horas trabajadas y antigüedad vs ingreso</h4>
        </div>
    """, unsafe_allow_html=True)
    
    variable_tiempo = st.selectbox('Variable', ['Horas por semana', 'Antigüedad en la empresa'], 
                                    label_visibility='collapsed', key='select_tiempo')
    
    if variable_tiempo == 'Horas por semana':
        bins_t = [0, 10, 20, 30, 40, 46, 60, 200]
        labels_t = ['1-10', '11-20', '21-30', '31-40', '41-46', '47-60', '> 60']
        datos_filtrados['RANGO_T'] = pd.cut(datos_filtrados['HORAS_SEMANA'], bins=bins_t, labels=labels_t)
    else:
        bins_t = [0, 6, 12, 24, 60, 120, 240, 1000]
        labels_t = ['0-6m', '7-12m', '1-2a', '2-5a', '5-10a', '10-20a', '> 20a']
        datos_filtrados['RANGO_T'] = pd.cut(datos_filtrados['ANTIGUEDAD_MESES'], bins=bins_t, labels=labels_t, include_lowest=True)
    
    resumen_t = datos_filtrados.groupby('RANGO_T')['INGLABO'].median().reset_index()
    resumen_t.columns = ['Rango', 'Mediana']
    
    import plotly.graph_objects as go
    
    fig4 = go.Figure()
    
    fig4.add_trace(go.Scatter(
        x=resumen_t['Rango'], y=resumen_t['Mediana'],
        mode='lines+markers+text',
        line=dict(color='#243e36', width=2),
        marker=dict(color='#243e36', size=8),
        text=[f'${v:,.0f}' for v in resumen_t['Mediana']],
        textposition='top center',
        textfont=dict(size=9, color='#243e36'),
        fill='tozeroy',
        fillcolor='rgba(124, 169, 130, 0.2)',
        cliponaxis=False
    ))
    
    fig4.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis_title='', yaxis_title='',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        font=dict(color='#243e36', size=10),
        margin=dict(t=20, b=30, l=60, r=60),
        height=420,
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# FILA 3 — TABLA DE SECTORES + MAPA
# ============================================================
col5, col6 = st.columns(2)

with col5:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">Mediana del ingreso por sector económico</h4>
        </div>
    """, unsafe_allow_html=True)
    
    resumen_sector = datos_filtrados.groupby('SECTOR_ECONOMICO').agg(
        Mediana=('INGLABO', 'median'),
        Encuestados=('INGLABO', 'count')
    ).sort_values('Mediana', ascending=False).reset_index()
    
    resumen_sector['Mediana'] = resumen_sector['Mediana'].apply(lambda x: f'${x:,.0f}')
    resumen_sector['Encuestados'] = resumen_sector['Encuestados'].apply(lambda x: f'{x:,}')
    resumen_sector.columns = ['Sector', 'Mediana ingreso', 'Encuestados']
    
    st.markdown("""
        <style>
        .tabla-container {
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            height: 750px;
            overflow-y: auto;
        }
        .tabla-sector {
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            color: #243e36;
        }
        .tabla-sector thead {
            position: sticky;
            top: 0;
            z-index: 1;
        }
        .tabla-sector th {
            background-color: #243e36;
            color: white;
            padding: 8px 10px;
            text-align: left;
        }
        .tabla-sector td {
            padding: 6px 10px;
            border-bottom: 1px solid #dceae0;
        }
        .tabla-sector tr:hover {
            background-color: #f1f7ed;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tabla_html = '<table class="tabla-sector"><thead><tr><th>Sector</th><th>Mediana</th><th>Enc.</th></tr></thead><tbody>'
    for _, row in resumen_sector.iterrows():
        tabla_html += f'<tr><td>{row["Sector"]}</td><td>{row["Mediana ingreso"]}</td><td>{row["Encuestados"]}</td></tr>'
    tabla_html += '</tbody></table>'

    st.markdown('<div style="margin-top: 5px;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tabla-container">{tabla_html}</div>', unsafe_allow_html=True)

with col6:
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px;">
            <h4 style="color: #243e36; text-align: center; margin: 0;">Ingreso por departamento</h4>
        </div>
    """, unsafe_allow_html=True)
    
    resumen_dpto = datos_filtrados.groupby('DEPARTAMENTO').agg(
        mediana_ingreso=('INGLABO', 'median'),
        Encuestados=('INGLABO', 'count'),
        LATITUD=('LATITUD', 'first'),
        LONGITUD=('LONGITUD', 'first')
    ).reset_index()
    
    fig_mapa = px.scatter_mapbox(
        resumen_dpto,
        lat='LATITUD', lon='LONGITUD',
        size='mediana_ingreso',
        color='mediana_ingreso',
        hover_name='DEPARTAMENTO',
        hover_data={'mediana_ingreso': ':,.0f', 'Encuestados': ':,', 'LATITUD': False, 'LONGITUD': False},
        labels={'mediana_ingreso': 'Mediana ingreso'},
        color_continuous_scale=[
            [0, '#f1f7ed'],
            [0.2, '#bdd5c4'],
            [0.4, '#7ca982'],
            [0.6, '#3a7a5e'],
            [0.8, '#243e36'],
            [1, '#0f1f18']
        ],
        size_max=30,
        zoom=4.5,
        center={'lat': 4.5, 'lon': -74},
        mapbox_style='carto-positron'
    )
    fig_mapa.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=750,
        paper_bgcolor='white',
        title={
            'text': '',
        }
    )
    st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_mapa, use_container_width=True)