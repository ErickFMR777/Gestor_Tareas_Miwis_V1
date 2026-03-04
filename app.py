"""
GESTOR DE TAREAS ACADÉMICAS MIWIS
================================
Aplicación profesional para gestionar tareas académicas
con autenticación segura e interfaz elegante
"""

import streamlit as st
import pandas as pd
import hashlib
from persistencia import cargar_tareas, guardar_tareas
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Gestor de Tareas Miwis",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ESTILOS CSS - DISEÑO ELEGANTE Y PROFESIONAL
# ============================================================================

def aplicar_estilos():
    """Aplica estilos CSS profesionales a la aplicación"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Variables de color */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #818cf8;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
        --border-color: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
    }
    
    /* Fondo y tipografía global */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1f35 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    .main {
        background: transparent;
        padding: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1f35 100%);
    }
    
    /* Contenedor principal */
    [data-testid="stMainBlockContainer"] {
        padding: 2rem 2.5rem !important;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slideDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .hero-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .hero-text h1 {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .hero-text p {
        font-size: 1rem;
        opacity: 0.95;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
    }
    
    .hero-stats {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .stat-badge strong {
        font-size: 1.3rem;
    }
    
    /* Cards */
    .card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .card:hover {
        border-color: var(--primary);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }
    
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .card-subtitle {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin: 0;
    }
    
    /* Login Container */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1f35 100%);
    }
    
    .login-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 3rem;
        max-width: 400px;
        width: 100%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .login-card h2 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        text-align: center;
        color: var(--primary);
    }
    
    .login-card p {
        text-align: center;
        color: var(--text-muted);
        margin-bottom: 2rem;
        font-size: 0.95rem;
    }
    
    /* Inputs mejorados */
    input[type="text"], input[type="password"], input[type="date"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    
    input[type="text"]:focus, 
    input[type="password"]:focus, 
    input[type="date"]:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }
    
    input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Botones secundarios */
    .stButton > button[kind="secondary"] {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Tabla personalizada */
    .dataframe {
        border-collapse: collapse !important;
        background: var(--card-bg) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(79, 70, 229, 0.2) 100%) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--primary-light) !important;
        padding: 12px 16px !important;
        font-weight: 700 !important;
        font-family: 'Poppins', sans-serif !important;
        text-align: left !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe td {
        border: 1px solid var(--border-color) !important;
        padding: 12px 16px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Columnas */
    .stColumn {
        gap: 1rem;
    }
    
    /* Alert/Info boxes */
    [data-testid="stAlertContainer"] {
        border-radius: 12px !important;
        border: none !important;
    }
    
    [data-testid="stAlert"] {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid var(--success) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    [data-testid="stWarningAlert"] {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid var(--warning) !important;
    }
    
    [data-testid="stErrorAlert"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid var(--danger) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Expandersidebar */
    [data-testid="stExpander"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        background: var(--card-bg) !important;
    }
    
    [data-testid="stExpander"] > div > button {
        color: var(--text-primary) !important;
        padding: 1rem !important;
    }
    
    /* Animaciones */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-content {
            flex-direction: column;
            text-align: center;
        }
        
        .hero-text h1 {
            font-size: 1.6rem;
        }
        
        .hero-stats {
            justify-content: center;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 1.5rem !important;
        }
        
        .login-card {
            margin: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

aplicar_estilos()

# ============================================================================
# GESTIÓN DE AUTENTICACIÓN
# ============================================================================

class GestorAutenticacion:
    """Maneja autenticación con código de acceso"""
    
    @staticmethod
    def hash_codigo(codigo: str) -> str:
        """Hashea el código de acceso"""
        return hashlib.sha256(codigo.encode()).hexdigest()
    
    @staticmethod
    def inicializar_sesion():
        """Inicializa variables de sesión de autenticación"""
        if "autenticado" not in st.session_state:
            st.session_state["autenticado"] = False
        if "codigo_hash" not in st.session_state:
            # Código inicial: "0000"
            st.session_state["codigo_hash"] = GestorAutenticacion.hash_codigo("0000")
    
    @staticmethod
    def verificar_codigo(codigo: str) -> bool:
        """Verifica si el código es correcto"""
        return GestorAutenticacion.hash_codigo(codigo) == st.session_state.get("codigo_hash", "")
    
    @staticmethod
    def cambiar_codigo(codigo_actual: str, codigo_nuevo: str) -> tuple[bool, str]:
        """
        Cambia el código de acceso
        
        Returns:
            (éxito, mensaje)
        """
        if not GestorAutenticacion.verificar_codigo(codigo_actual):
            return False, "❌ Código actual incorrecto"
        
        if len(codigo_nuevo) != 4 or not codigo_nuevo.isdigit():
            return False, "❌ El código debe tener exactamente 4 dígitos"
        
        st.session_state["codigo_hash"] = GestorAutenticacion.hash_codigo(codigo_nuevo)
        return True, "✅ Código de acceso actualizado correctamente"

# ============================================================================
# GESTIÓN DE TAREAS
# ============================================================================

class GestorTareas:
    """Maneja operaciones con tareas"""
    
    @staticmethod
    def inicializar():
        """Inicializa el DataFrame de tareas en session_state"""
        if "tareas" not in st.session_state:
            st.session_state["tareas"] = cargar_tareas()
    
    @staticmethod
    def agregar_tarea(nombre: str, materia: str, fecha_recibido: str, fecha_entrega: str) -> tuple[bool, str]:
        """
        Agrega una nueva tarea
        
        Returns:
            (éxito, mensaje)
        """
        # Validaciones
        if not nombre.strip():
            return False, "❌ El nombre de la tarea no puede estar vacío"
        if not materia.strip():
            return False, "❌ La materia no puede estar vacía"
        if len(nombre) > 200:
            return False, "❌ El nombre es demasiado largo (máx. 200 caracteres)"
        
        nueva_tarea = {
            "id": str(uuid4()),
            "Nombre de la tarea": nombre.strip(),
            "Materia": materia.strip(),
            "Fecha recibido": fecha_recibido,
            "Fecha de entrega": fecha_entrega,
            "Terminado": False
        }
        
        df = st.session_state["tareas"]
        st.session_state["tareas"] = pd.concat(
            [df, pd.DataFrame([nueva_tarea])],
            ignore_index=True
        )
        guardar_tareas(st.session_state["tareas"])
        return True, "✅ Tarea agregada correctamente"
    
    @staticmethod
    def toggle_terminada(task_id: str):
        """Marca/desmarca una tarea como terminada"""
        df = st.session_state["tareas"]
        mask = df['id'] == task_id
        if mask.any():
            idx = df[mask].index[0]
            df.at[idx, 'Terminado'] = not df.at[idx, 'Terminado']
            st.session_state["tareas"] = df
            guardar_tareas(df)
            st.rerun()
    
    @staticmethod
    def eliminar_tarea(task_id: str):
        """Elimina una tarea"""
        df = st.session_state["tareas"]
        st.session_state["tareas"] = df[df['id'] != task_id].reset_index(drop=True)
        guardar_tareas(st.session_state["tareas"])
        st.rerun()
    
    @staticmethod
    def obtener_estadisticas() -> dict:
        """Obtiene estadísticas de tareas"""
        df = st.session_state["tareas"]
        total = len(df)
        terminadas = len(df[df['Terminado'] == True])
        pendientes = total - terminadas
        
        return {
            "total": total,
            "terminadas": terminadas,
            "pendientes": pendientes,
            "porcentaje": (terminadas / total * 100) if total > 0 else 0
        }

# ============================================================================
# PANTALLA DE LOGIN
# ============================================================================

def pantalla_login():
    """Renderiza la pantalla de login"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <h2>🔐 Acceso Seguro</h2>
            <p>Ingresa tu código de acceso para continuar</p>
        </div>
        """, unsafe_allow_html=True)
        
        codigo = st.text_input(
            "Código de acceso",
            type="password",
            placeholder="0000",
            max_chars=4
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔓 Entrar", use_container_width=True):
                if GestorAutenticacion.verificar_codigo(codigo):
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("❌ Código incorrecto. Intenta nuevamente.")
        
        with col_b:
            if st.button("ℹ️ Código inicial", use_container_width=True):
                st.info("💡 El código de acceso inicial es: **0000**")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PANTALLA PRINCIPAL
# ============================================================================

def pantalla_principal():
    """Renderiza la pantalla principal de la aplicación"""
    
    # Inicializar datos
    GestorAutenticacion.inicializar_sesion()
    GestorTareas.inicializar()
    
    # Obtener estadísticas
    stats = GestorTareas.obtener_estadisticas()
    fecha_actual = datetime.now().strftime("%d de %B de %Y")
    
    # Hero Banner
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-content">
            <div class="hero-text">
                <h1>📚 Gestor de Tareas Miwis</h1>
                <p>Control de actividades académicas de Miwiwita</p>
            </div>
            <div class="hero-stats">
                <div class="stat-badge">
                    <span>📅 Hoy:</span>
                    <strong>{fecha_actual}</strong>
                </div>
                <div class="stat-badge">
                    <span>📊 Total:</span>
                    <strong>{stats['total']}</strong>
                </div>
                <div class="stat-badge">
                    <span>✅ Completadas:</span>
                    <strong>{stats['terminadas']}</strong>
                </div>
                <div class="stat-badge">
                    <span>⏳ Pendientes:</span>
                    <strong>{stats['pendientes']}</strong>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs principales
    tab_tareas, tab_agregar, tab_config = st.tabs([
        "📋 Mis Tareas",
        "➕ Agregar Tarea",
        "⚙️ Configuración"
    ])
    
    # ========================================================================
    # TAB: MIS TAREAS
    # ========================================================================
    with tab_tareas:
        st.subheader("📋 Tareas Registradas")
        
        df = st.session_state["tareas"]
        
        if df.empty:
            st.info("📭 No hay tareas registradas. ¡Crea una nueva para comenzar!")
        else:
            # Crear tabla personalizada con columnas adicionales
            df_display = df.copy()
            df_display['Fecha recibido'] = pd.to_datetime(df_display['Fecha recibido']).dt.strftime('%d/%m/%Y')
            df_display['Fecha de entrega'] = pd.to_datetime(df_display['Fecha de entrega']).dt.strftime('%d/%m/%Y')
            df_display['Estado'] = df_display['Terminado'].apply(
                lambda x: "✅ Completada" if x else "⏳ Pendiente"
            )
            
            # Reordenar columnas para display
            columnas_display = [
                'Nombre de la tarea',
                'Materia',
                'Fecha recibido',
                'Fecha de entrega',
                'Estado'
            ]
            
            # Mostrar tabla
            col_tabla = st.container()
            with col_tabla:
                # Crear dos sub-columnas para tabla y acciones
                st.dataframe(
                    df_display[columnas_display],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
            
            st.divider()
            
            # Sección de acciones
            st.subheader("⚙️ Gestionar Tareas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Marcar como completada:**")
                tarea_marcar = st.selectbox(
                    "Selecciona una tarea",
                    options=df[~df['Terminado']]['Nombre de la tarea'].tolist() if len(df[~df['Terminado']]) > 0 else ["No hay tareas pendientes"],
                    label_visibility="collapsed",
                    key="select_marcar"
                )
                
                if tarea_marcar != "No hay tareas pendientes":
                    if st.button("✅ Marcar como completada", use_container_width=True, key="btn_marcar"):
                        task_id = df[df['Nombre de la tarea'] == tarea_marcar]['id'].iloc[0]
                        GestorTareas.toggle_terminada(task_id)
            
            with col2:
                st.write("**Eliminar tarea:**")
                tarea_eliminar = st.selectbox(
                    "Selecciona una tarea",
                    options=df['Nombre de la tarea'].tolist(),
                    label_visibility="collapsed",
                    key="select_eliminar"
                )
                
                if st.button("🗑️ Eliminar tarea", use_container_width=True, key="btn_eliminar", type="secondary"):
                    if st.session_state.get("confirmar_eliminar", False):
                        task_id = df[df['Nombre de la tarea'] == tarea_eliminar]['id'].iloc[0]
                        GestorTareas.eliminar_tarea(task_id)
                    else:
                        st.session_state["confirmar_eliminar"] = True
                        st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar: **{tarea_eliminar}**? Haz clic nuevamente para confirmar.")
                        st.session_state["confirmar_eliminar"] = False
    
    # ========================================================================
    # TAB: AGREGAR TAREA
    # ========================================================================
    with tab_agregar:
        st.subheader("➕ Agregar Nueva Tarea")
        
        st.markdown("""
        <div class="card" style="margin-bottom: 2rem;">
            <p style="margin: 0; color: var(--text-secondary);">
                📝 Completa el formulario para registrar una nueva tarea académica. 
                Asegúrate de ingresar correctamente las fechas de recepción y entrega.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_agregar_tarea", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input(
                    "📝 Nombre de la tarea",
                    placeholder="Ej: Ensayo sobre fotosíntesis",
                    max_chars=200
                )
                
                fecha_recibido = st.date_input(
                    "📅 Fecha de recepción",
                    value=datetime.now(),
                    format="DD/MM/YYYY"
                )
            
            with col2:
                materia = st.text_input(
                    "📚 Materia",
                    placeholder="Ej: Biología",
                    max_chars=100
                )
                
                fecha_entrega = st.date_input(
                    "📅 Fecha de entrega",
                    value=datetime.now() + timedelta(days=7),
                    format="DD/MM/YYYY"
                )
            
            # Validación de fechas
            if fecha_entrega < fecha_recibido:
                st.warning("⚠️ La fecha de entrega no puede ser anterior a la de recepción")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                agregar = st.form_submit_button(
                    "➕ Agregar Tarea",
                    use_container_width=True
                )
            
            if agregar:
                exito, mensaje = GestorTareas.agregar_tarea(
                    nombre,
                    materia,
                    fecha_recibido.strftime("%d/%m/%Y"),
                    fecha_entrega.strftime("%d/%m/%Y")
                )
                
                if exito:
                    st.success(mensaje)
                    st.balloons()
                else:
                    st.error(mensaje)
    
    # ========================================================================
    # TAB: CONFIGURACIÓN
    # ========================================================================
    with tab_config:
        st.subheader("⚙️ Configuración de la Cuenta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 🔐 Cambiar Código de Acceso")
            
            st.markdown("""
            <div class="card" style="margin-bottom: 1.5rem;">
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">
                    ⚠️ Por seguridad, debes ingresar el código actual antes de crear uno nuevo.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("form_cambiar_codigo"):
                codigo_actual = st.text_input(
                    "Código actual",
                    type="password",
                    placeholder="••••",
                    max_chars=4
                )
                
                codigo_nuevo = st.text_input(
                    "Nuevo código (4 dígitos)",
                    type="password",
                    placeholder="••••",
                    max_chars=4
                )
                
                codigo_confirmacion = st.text_input(
                    "Confirmar nuevo código",
                    type="password",
                    placeholder="••••",
                    max_chars=4
                )
                
                cambiar = st.form_submit_button(
                    "🔄 Actualizar Código",
                    use_container_width=True
                )
                
                if cambiar:
                    if not codigo_actual or not codigo_nuevo or not codigo_confirmacion:
                        st.error("❌ Todos los campos son obligatorios")
                    elif codigo_nuevo != codigo_confirmacion:
                        st.error("❌ Los códigos nuevos no coinciden")
                    else:
                        exito, mensaje = GestorAutenticacion.cambiar_codigo(
                            codigo_actual,
                            codigo_nuevo
                        )
                        if exito:
                            st.success(mensaje)
                        else:
                            st.error(mensaje)
        
        with col2:
            st.write("### 📊 Estadísticas Generales")
            
            stats = GestorTareas.obtener_estadisticas()
            
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">
                        {stats['total']}
                    </div>
                    <div style="color: var(--text-secondary); margin-bottom: 1.5rem;">Total de tareas</div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700; color: var(--success); margin-bottom: 0.25rem;">
                                {stats['terminadas']}
                            </div>
                            <div style="font-size: 0.85rem; color: var(--text-muted);">Completadas</div>
                        </div>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700; color: var(--warning); margin-bottom: 0.25rem;">
                                {stats['pendientes']}
                            </div>
                            <div style="font-size: 0.85rem; color: var(--text-muted);">Pendientes</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
                st.session_state["autenticado"] = False
                st.rerun()

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    
    # Inicializar autenticación
    GestorAutenticacion.inicializar_sesion()
    
    # Mostrar pantalla correspondiente
    if not st.session_state.get("autenticado", False):
        pantalla_login()
    else:
        pantalla_principal()

if __name__ == "__main__":
    main()
