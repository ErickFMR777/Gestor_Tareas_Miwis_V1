# 📚 Gestor de Actividades Académicas — Miwiwita

## 🎯 Descripción

Aplicación web para gestionar actividades académicas (tareas y evaluaciones) con interfaz elegante, filtros avanzados y estadísticas en tiempo real.

### ✨ Características

- **🔐 Autenticación segura** con código de acceso (SHA-256)
- **📋 Gestión de actividades**: Agregar, completar y eliminar tareas y evaluaciones
- **🏷️ Tipos de actividad**: Diferencia entre **Tarea** y **Evaluación**
- **📚 18 materias preconfiguradas**: Artística, Matemáticas, Inglés, etc.
- **🔍 Filtros avanzados**: Por materia, tipo, estado y rango de fechas de entrega
- **📊 Estadísticas**: Dashboard con métricas globales y desglose por materia
- **💾 Persistencia en JSON** con sincronización automática
- **🎨 Diseño moderno**: Tema oscuro profesional, responsive
- **⌨️ Acceso rápido**: Login con Enter

---

## 🚀 Instalación

### Requisitos

- Python 3.8+
- pip

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/ErickFMR777/Gestor_Tareas_Miwis_V1.git
cd Gestor_Tareas_Miwis_V1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501` — Código de acceso inicial: **0000**

---

## 📖 Uso

### Agregar Actividad

1. Ve a **"➕ Agregar Actividad"**
2. Llena: nombre, materia (desplegable), tipo (Tarea/Evaluación), fechas
3. Clic en **"➕ Agregar Actividad"**

### Mis Actividades

- Filtra por materia, tipo, estado o rango de fechas
- Marca actividades como completadas (✅) o pendientes (🔄)
- Elimina actividades (🗑️)

### Configuración

- Cambia tu código de acceso (4 dígitos)
- Cierra sesión

---

## 🏗️ Estructura

```
Gestor_Tareas_Miwis_V1/
├── app.py                 # Aplicación principal (Streamlit)
├── persistencia.py        # Módulo de almacenamiento (JSON)
├── requirements.txt       # Dependencias
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml        # Configuración de tema Streamlit
└── data/
    └── tareas.json        # Datos (se crea automáticamente)
```

---

## 🚀 Deploy en Streamlit Cloud

1. Sube el proyecto a GitHub
2. Abre [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta el repositorio y selecciona `app.py`
4. Deploy

---

## 📄 Licencia

MIT

---

**Versión**: 2.1.0  
**Última actualización**: Marzo 2026
