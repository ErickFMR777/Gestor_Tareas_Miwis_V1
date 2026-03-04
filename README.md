# 📚 Gestor de Tareas Miwis - Aplicación Profesional

## 🎯 Descripción

**Gestor de Tareas Miwis** es una aplicación web moderna y profesional para gestionar tareas académicas. Fue completamente rediseñada con interfaz elegante, funcionalidad mejorada y mejor experiencia de usuario.

### ✨ Características Principales

- **🔐 Autenticación Segura**: Sistema de código de acceso con hash SHA-256
- **📋 Gestión de Tareas**: Agregar, marcar completadas y eliminar tareas
- **📊 Estadísticas en Tiempo Real**: Dashboard con métricas de tareas
- **💾 Persistencia de Datos**: Almacenamiento en JSON con sincronización automática
- **🎨 Interfaz Elegante**: Diseño moderno con tema oscuro profesional
- **⚡ Rendimiento Optimizado**: Código eficiente y sin dependencias frágiles
- **📱 Responsive**: Funciona perfectamente en desktop, tablet y móvil
- **🌙 Modo Oscuro**: Tema oscuro con acentos en color índigo profesional

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes acceso al repositorio
   git clone <url-del-repositorio>
   cd gestor-tareas-miwis
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

4. **Acceder a la aplicación**
   - Abre tu navegador en: `http://localhost:8501`
   - Usa el código de acceso inicial: `0000`

---

## 📖 Guía de Uso

### 1. Acceso a la Aplicación

```
🔐 Código de acceso inicial: 0000
```

- Ingresa el código en la pantalla de login
- Haz clic en "🔓 Entrar"

### 2. Agregar Tareas

1. Ve a la pestaña **"➕ Agregar Tarea"**
2. Completa los campos:
   - **📝 Nombre de la tarea**: Descripción clara de la actividad
   - **📚 Materia**: Asignatura relacionada
   - **📅 Fecha de recepción**: Cuándo recibiste la tarea
   - **📅 Fecha de entrega**: Cuándo debes entregarla
3. Haz clic en **"➕ Agregar Tarea"**

### 3. Gestionar Tareas

En la pestaña **"📋 Mis Tareas"** puedes:

- **Ver todas tus tareas** en una tabla clara y organizada
- **Marcar como completada**: Selecciona una tarea pendiente y haz clic en "✅ Marcar como completada"
- **Eliminar tarea**: Selecciona la tarea y haz clic en "🗑️ Eliminar tarea" (confirma al hacer clic nuevamente)

### 4. Configuración de Seguridad

En la pestaña **"⚙️ Configuración"**:

- **Cambiar Código de Acceso**: 
  - Ingresa el código actual
  - Define un nuevo código (4 dígitos)
  - Confirma el nuevo código
  - Haz clic en "🔄 Actualizar Código"

- **Ver Estadísticas**: 
  - Total de tareas
  - Tareas completadas
  - Tareas pendientes

---

## 🏗️ Estructura del Proyecto

```
gestor-tareas-miwis/
├── app.py                 # Aplicación principal de Streamlit
├── persistencia.py        # Módulo de almacenamiento de datos
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
└── data/
    └── tareas.json       # Archivo de almacenamiento (se crea automáticamente)
```

---

## 🔧 Detalles Técnicos

### Arquitectura

La aplicación sigue una arquitectura limpia y modular:

```
┌─────────────────────────────────────────┐
│   Interfaz de Usuario (Streamlit)       │
├─────────────────────────────────────────┤
│   GestorAutenticacion                   │
│   GestorTareas                          │
├─────────────────────────────────────────┤
│   persistencia.py (JSON)                │
└─────────────────────────────────────────┘
```

### Clases Principales

#### `GestorAutenticacion`
- `hash_codigo()`: Hashea códigos con SHA-256
- `verificar_codigo()`: Valida el código de acceso
- `cambiar_codigo()`: Actualiza el código de forma segura

#### `GestorTareas`
- `inicializar()`: Carga datos al iniciar
- `agregar_tarea()`: Crea una nueva tarea
- `toggle_terminada()`: Marca/desmarca como completada
- `eliminar_tarea()`: Elimina una tarea
- `obtener_estadisticas()`: Retorna métricas

### Seguridad

- ✅ Códigos de acceso hasheados con SHA-256
- ✅ Validación de todas las entradas
- ✅ Sin almacenamiento de contraseñas en texto plano
- ✅ Manejo seguro de sesiones

---

## 🎨 Diseño y UX

### Paleta de Colores

| Color | Código | Uso |
|-------|--------|-----|
| Primario | `#6366f1` | Botones, acentos principales |
| Éxito | `#10b981` | Confirmaciones, estados completados |
| Peligro | `#ef4444` | Acciones destructivas |
| Fondo | `#0f172a` | Fondo principal |
| Card | `#1e293b` | Fondos de tarjetas |

### Tipografía

- **Display**: Poppins (encabezados)
- **Body**: Inter (texto)
- Ambas optimizadas para legibilidad en pantallas

### Animaciones

- Fade-in suave al cargar elementos
- Hover effects en botones y cards
- Transiciones suaves entre pantallas

---

## 🐛 Solución de Problemas

### "No puedo acceder a la aplicación"
- Verifica que Streamlit esté instalado: `pip install streamlit`
- Asegúrate de estar en el directorio correcto
- Comprueba que el puerto 8501 esté disponible

### "Las tareas no se guardan"
- Verifica que el directorio `data/` tenga permisos de escritura
- Comprueba el archivo `data/tareas.json`
- Intenta eliminar el archivo y reinicia la app

### "Olvidé el código de acceso"
- Abre el archivo `app.py`
- En la función `GestorAutenticacion.inicializar_sesion()`, el código inicial es `0000`
- Para resetear: elimina `st.session_state["codigo_hash"]` o reinicia la aplicación

---

## 📝 Cambios Principales vs. Versión Original

### ✅ Mejoras Implementadas

1. **Interfaz Moderna**: Rediseño completo con colores profesionales
2. **CSS Limpio**: Reemplazo de CSS complejo y redundante
3. **Funcionalidad Robusta**: Eliminación de JavaScript frágil
4. **Componentes Streamlit Nativos**: Uso de tabs, forms, dataframe nativo
5. **Seguridad Mejorada**: Hash de códigos de acceso
6. **Validación de Entradas**: Verificación en todos los formularios
7. **Mejor Organización**: Código modular con clases
8. **Documentación**: Comentarios y docstrings
9. **Sin Dependencias Externas**: Solo Streamlit y Pandas
10. **Responsivo**: Funciona en todos los dispositivos

### 🗑️ Lo que se Eliminó

- HTML/JavaScript complejo y frágil
- CSS redundante y conflictivo
- Uso de `st.experimental_rerun()` (deprecado)
- Módulo `streamlit_extras` innecesario
- Métodos de callback sin usar

---

## 🚀 Deployment

### Streamlit Cloud (Recomendado)

1. Sube tu proyecto a GitHub
2. Abre [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta tu repositorio
4. Selecciona `app.py` como archivo principal
5. Haz clic en "Deploy"

### Otros Servidores

```bash
# En un servidor Linux/macOS
streamlit run app.py --server.port 80 --server.address 0.0.0.0
```

---

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT.

---

## 👨‍💻 Desarrollo

### Para contribuir

1. Crea una rama: `git checkout -b feature/mi-mejora`
2. Realiza tus cambios
3. Commit: `git commit -m "Agrego mejora X"`
4. Push: `git push origin feature/mi-mejora`
5. Abre un Pull Request

---

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:

1. Abre un issue en GitHub
2. Proporciona detalles:
   - Sistema operativo
   - Versión de Python
   - Pasos para reproducir el problema
   - Screenshots si es relevante

---

## 🎓 Notas Académicas

Esta aplicación fue diseñada específicamente para gestionar tareas académicas de estudiantes. Características especialmente útiles:

- 📅 Seguimiento de fechas de entrega
- ✅ Control de tareas completadas
- 📊 Visualización de progreso
- 🎯 Priorización por materia

¡Usa esta herramienta para mejorar tu productividad académica! 📚

---

**Última actualización**: 2024
**Versión**: 2.0.0 (Rediseño Profesional)
