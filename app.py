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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Variables de color */
    :root {
        --primary: #7c3aed;
        --primary-dark: #6d28d9;
        --primary-light: #a78bfa;
        --primary-glow: rgba(124, 58, 237, 0.35);
        --accent: #06b6d4;
        --accent-glow: rgba(6, 182, 212, 0.25);
        --success: #10b981;
        --success-light: rgba(16, 185, 129, 0.15);
        --danger: #f43f5e;
        --danger-light: rgba(244, 63, 94, 0.15);
        --warning: #f59e0b;
        --warning-light: rgba(245, 158, 11, 0.15);
        --dark-bg: #0a0e1a;
        --dark-bg-2: #111827;
        --card-bg: rgba(17, 24, 39, 0.7);
        --card-bg-solid: #111827;
        --glass-bg: rgba(17, 24, 39, 0.45);
        --glass-border: rgba(255, 255, 255, 0.08);
        --border-color: rgba(255, 255, 255, 0.06);
        --border-hover: rgba(124, 58, 237, 0.4);
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
        --shadow-md: 0 8px 24px rgba(0,0,0,0.3);
        --shadow-lg: 0 16px 48px rgba(0,0,0,0.4);
        --shadow-glow: 0 0 40px var(--primary-glow);
    }
    
    /* Fondo global con patrón sutil */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--dark-bg);
        background-image:
            radial-gradient(ellipse 80% 60% at 50% -20%, rgba(124,58,237,0.12) 0%, transparent 70%),
            radial-gradient(ellipse 60% 50% at 80% 50%, rgba(6,182,212,0.06) 0%, transparent 70%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        -webkit-font-smoothing: antialiased;
    }
    
    .main {
        background: transparent;
        padding: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: transparent;
    }
    
    /* Contenedor principal */
    [data-testid="stMainBlockContainer"] {
        padding: 1.5rem 2.5rem !important;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Ocultar header y footer de Streamlit */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    footer {
        display: none !important;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', 'Poppins', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
    }
    
    /* ===================== LOGIN ===================== */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        padding: 2rem;
        animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .login-brand {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-brand .brand-icon {
        width: 72px;
        height: 72px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 12px 32px var(--primary-glow);
    }
    
    .login-brand h1 {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    
    .login-brand p {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    .login-glass {
        background: var(--glass-bg);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 2.5rem 2rem;
        max-width: 380px;
        width: 100%;
        box-shadow: var(--shadow-lg), 0 0 60px rgba(124,58,237,0.08);
    }
    
    .login-glass h2 {
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 0.25rem;
        color: var(--text-primary);
    }
    
    .login-glass p {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    
    /* ===================== HERO BANNER ===================== */
    .hero-banner {
        background: linear-gradient(135deg, var(--primary) 0%, #4f46e5 50%, var(--accent) 150%);
        border-radius: var(--radius-xl);
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-md), 0 0 60px var(--primary-glow);
        border: 1px solid rgba(255, 255, 255, 0.12);
        position: relative;
        overflow: hidden;
        animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .hero-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .hero-text h1 {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
        color: white;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    
    .hero-text p {
        font-size: 0.9rem;
        opacity: 0.9;
        color: rgba(255, 255, 255, 0.85);
        margin: 0;
        font-weight: 400;
    }
    
    .hero-stats {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }
    
    .stat-badge {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(12px);
        padding: 0.6rem 1.2rem;
        border-radius: var(--radius-md);
        border: 1px solid rgba(255, 255, 255, 0.18);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.15rem;
        font-weight: 500;
        font-size: 0.8rem;
        min-width: 90px;
        transition: transform 0.2s ease;
    }
    
    .stat-badge:hover {
        transform: translateY(-2px);
    }
    
    .stat-badge strong {
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .stat-badge span {
        font-size: 0.7rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ===================== CARDS ===================== */
    .card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: var(--shadow-sm);
    }
    
    .card:hover {
        border-color: var(--border-hover);
        box-shadow: var(--shadow-md), 0 0 30px rgba(124,58,237,0.08);
        transform: translateY(-3px);
    }
    
    /* ===================== INPUTS ===================== */
    input[type="text"], input[type="password"], input[type="date"] {
        background: rgba(10, 14, 26, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        padding: 14px 16px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
    }
    
    input[type="text"]:focus, 
    input[type="password"]:focus, 
    input[type="date"]:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-glow), 0 0 20px rgba(124,58,237,0.1) !important;
        outline: none !important;
    }
    
    input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Labels */
    .stTextInput > label, .stDateInput > label, .stSelectbox > label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.01em !important;
    }
    
    /* ===================== BOTONES ===================== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', 'Poppins', sans-serif !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 16px var(--primary-glow) !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px var(--primary-glow), 0 0 40px rgba(124,58,237,0.15) !important;
        filter: brightness(1.08) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Botones secundarios */
    .stButton > button[kind="secondary"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--glass-border) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--border-hover) !important;
        box-shadow: var(--shadow-md), 0 0 20px rgba(124,58,237,0.1) !important;
    }
    
    /* form submit */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', 'Poppins', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 16px var(--primary-glow) !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px var(--primary-glow) !important;
        filter: brightness(1.08) !important;
    }
    
    /* ===================== TABS ===================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border-radius: var(--radius-lg);
        padding: 4px;
        border: 1px solid var(--glass-border);
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md);
        padding: 10px 24px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
        color: var(--text-muted);
        border: none;
        background: transparent;
        transition: all 0.25s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        background: rgba(124,58,237,0.08);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px var(--primary-glow);
    }
    
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* ===================== TABLA ===================== */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
    }
    
    .dataframe {
        border-collapse: collapse !important;
        background: var(--card-bg-solid) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        color: var(--primary-light) !important;
        padding: 14px 16px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        text-align: left !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    .dataframe td {
        border: 1px solid rgba(255,255,255,0.03) !important;
        padding: 12px 16px !important;
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(124, 58, 237, 0.06) !important;
    }
    
    /* ===================== CHECKBOX ===================== */
    .stCheckbox label span {
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
    }
    
    /* ===================== SELECTBOX ===================== */
    [data-baseweb="select"] > div {
        background: rgba(10, 14, 26, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-baseweb="select"] > div:hover {
        border-color: var(--primary) !important;
    }
    
    /* ===================== DIVIDER ===================== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(124,58,237,0.3), transparent) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* ===================== ALERTS ===================== */
    [data-testid="stAlertContainer"] {
        border-radius: var(--radius-md) !important;
        border: none !important;
    }
    
    [data-testid="stAlert"] {
        background: var(--success-light) !important;
        border: 1px solid var(--success) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.9rem 1rem !important;
        backdrop-filter: blur(8px) !important;
    }
    
    [data-testid="stWarningAlert"] {
        background: var(--warning-light) !important;
        border: 1px solid var(--warning) !important;
    }
    
    [data-testid="stErrorAlert"] {
        background: var(--danger-light) !important;
        border: 1px solid var(--danger) !important;
    }
    
    /* ===================== SIDEBAR ===================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-bg-2) 0%, var(--dark-bg) 100%) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    /* ===================== EXPANDER ===================== */
    [data-testid="stExpander"] {
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
    }
    
    [data-testid="stExpander"] > div > button {
        color: var(--text-primary) !important;
        padding: 1rem !important;
    }
    
    /* ===================== ANIMACIONES ===================== */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(24px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* ===================== RESPONSIVE ===================== */
    @media (max-width: 768px) {
        .hero-content {
            flex-direction: column;
            text-align: center;
        }
        
        .hero-text h1 {
            font-size: 1.4rem;
        }
        
        .hero-stats {
            justify-content: center;
        }
        
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 1rem !important;
        }
        
        .login-glass {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
        
        .stat-badge {
            min-width: 75px;
            padding: 0.5rem 0.8rem;
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
    
    # Espaciador superior mínimo para centrar visualmente
    st.markdown('<div style="height: 4vh;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        # Branding
        st.markdown("""
        <div class="login-wrapper">
            <div class="login-brand">
                <div class="brand-icon">📚</div>
                <h1>Miwis</h1>
                <p>Gestor de Tareas Académicas</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Card de login con glass effect
        st.markdown("""
        <div class="login-glass" style="margin: -1rem auto 0 auto;">
            <h2>Bienvenido de vuelta</h2>
            <p>Ingresa tu código para continuar</p>
        </div>
        """, unsafe_allow_html=True)
        
        codigo = st.text_input(
            "Código de acceso",
            type="password",
            placeholder="****",
            max_chars=4,
            label_visibility="collapsed"
        )
        
        if st.button("🔓 Ingresar", use_container_width=True):
            if GestorAutenticacion.verificar_codigo(codigo):
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("❌ Código incorrecto. Intenta nuevamente.")

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
                <h1>📚 Tareas Miwis</h1>
                <p>Control de actividades académicas de Miwiwita · {fecha_actual}</p>
            </div>
            <div class="hero-stats">
                <div class="stat-badge">
                    <strong>{stats['total']}</strong>
                    <span>Total</span>
                </div>
                <div class="stat-badge">
                    <strong>{stats['terminadas']}</strong>
                    <span>Hechas</span>
                </div>
                <div class="stat-badge">
                    <strong>{stats['pendientes']}</strong>
                    <span>Pendientes</span>
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
        df = st.session_state["tareas"]
        
        if df.empty:
            st.markdown("""
            <div class="card" style="text-align: center; padding: 3rem 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">No hay tareas registradas</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">¡Crea una nueva tarea para comenzar!</div>
            </div>
            """, unsafe_allow_html=True)
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
                    width="stretch",
                    hide_index=True,
                    height=400
                )
            
            st.divider()
            
            # Sección de acciones
            st.subheader("⚙️ Gestionar Tareas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Cambiar estado de tarea:**")
                # Mostrar TODAS las tareas para poder marcar/desmarcar
                opciones_estado = df['Nombre de la tarea'].tolist()
                if opciones_estado:
                    tarea_marcar = st.selectbox(
                        "Selecciona una tarea",
                        options=opciones_estado,
                        label_visibility="collapsed",
                        key="select_marcar"
                    )
                    
                    # Determinar estado actual de la tarea seleccionada
                    fila = df[df['Nombre de la tarea'] == tarea_marcar].iloc[0]
                    esta_terminada = fila['Terminado']
                    
                    if esta_terminada:
                        if st.button("🔄 Marcar como pendiente", use_container_width=True, key="btn_marcar"):
                            GestorTareas.toggle_terminada(fila['id'])
                    else:
                        if st.button("✅ Marcar como completada", use_container_width=True, key="btn_marcar"):
                            GestorTareas.toggle_terminada(fila['id'])
                else:
                    st.info("No hay tareas registradas.")
            
            with col2:
                st.write("**Eliminar tarea:**")
                opciones_eliminar = df['Nombre de la tarea'].tolist()
                if opciones_eliminar:
                    tarea_eliminar = st.selectbox(
                        "Selecciona una tarea",
                        options=opciones_eliminar,
                        label_visibility="collapsed",
                        key="select_eliminar"
                    )
                    
                    confirmar = st.checkbox(
                        f"Confirmo eliminar: **{tarea_eliminar}**",
                        key="check_confirmar_eliminar"
                    )
                    
                    if st.button("🗑️ Eliminar tarea", use_container_width=True, key="btn_eliminar", type="secondary"):
                        if confirmar:
                            task_id = df[df['Nombre de la tarea'] == tarea_eliminar]['id'].iloc[0]
                            GestorTareas.eliminar_tarea(task_id)
                        else:
                            st.warning("⚠️ Marca la casilla de confirmación antes de eliminar.")
                else:
                    st.info("No hay tareas para eliminar.")
    
    # ========================================================================
    # TAB: AGREGAR TAREA
    # ========================================================================
    with tab_agregar:
        st.markdown("""
        <div class="card" style="margin-bottom: 1.5rem;">
            <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">
                📝 Completa el formulario para registrar una nueva tarea académica.
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
            
            porcentaje = stats['porcentaje']
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; padding: 1.5rem 1rem;">
                    <div style="font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.25rem;">
                        {stats['total']}
                    </div>
                    <div style="color: var(--text-muted); margin-bottom: 1.5rem; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Total de tareas</div>
                    
                    <div style="background: rgba(255,255,255,0.04); border-radius: 10px; height: 6px; margin-bottom: 1.5rem; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, var(--primary), var(--accent)); height: 100%; border-radius: 10px; width: {porcentaje}%; transition: width 0.5s ease;"></div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div style="background: var(--success-light); border-radius: 12px; padding: 1rem;">
                            <div style="font-size: 1.8rem; font-weight: 700; color: var(--success); margin-bottom: 0.2rem;">
                                {stats['terminadas']}
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em;">Completadas</div>
                        </div>
                        <div style="background: var(--warning-light); border-radius: 12px; padding: 1rem;">
                            <div style="font-size: 1.8rem; font-weight: 700; color: var(--warning); margin-bottom: 0.2rem;">
                                {stats['pendientes']}
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em;">Pendientes</div>
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
