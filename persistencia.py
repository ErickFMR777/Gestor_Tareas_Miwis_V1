"""
Módulo de persistencia para guardar y cargar tareas
Utiliza JSON para almacenamiento local
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Directorio de datos
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
TAREAS_FILE = DATA_DIR / "tareas.json"


def guardar_tareas(df: pd.DataFrame) -> bool:
    """
    Guarda el DataFrame de tareas en JSON
    
    Args:
        df: DataFrame con las tareas
        
    Returns:
        bool: True si se guardó exitosamente
    """
    try:
        if df.empty:
            # Crear archivo vacío si no hay tareas
            with open(TAREAS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return True
        
        # Convertir DataFrame a lista de diccionarios
        tareas_lista = df.to_dict('records')
        
        # Guardar en JSON
        with open(TAREAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tareas_lista, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error al guardar tareas: {e}")
        return False


def cargar_tareas() -> pd.DataFrame:
    """
    Carga las tareas desde JSON
    
    Returns:
        pd.DataFrame: DataFrame con las tareas, vacío si no existen
    """
    try:
        if not TAREAS_FILE.exists():
            return pd.DataFrame(columns=[
                'id', 'Nombre de la tarea', 'Materia', 
                'Fecha recibido', 'Fecha de entrega', 'Terminado'
            ])
        
        with open(TAREAS_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        if not datos:
            return pd.DataFrame(columns=[
                'id', 'Nombre de la tarea', 'Materia', 
                'Fecha recibido', 'Fecha de entrega', 'Terminado'
            ])
        
        df = pd.DataFrame(datos)
        
        # Asegurar columnas necesarias
        columnas_requeridas = [
            'id', 'Nombre de la tarea', 'Materia', 
            'Fecha recibido', 'Fecha de entrega', 'Terminado'
        ]
        for col in columnas_requeridas:
            if col not in df.columns:
                df[col] = '' if col != 'Terminado' else ''
        
        return df[columnas_requeridas]
    
    except Exception as e:
        print(f"Error al cargar tareas: {e}")
        return pd.DataFrame(columns=[
            'id', 'Nombre de la tarea', 'Materia', 
            'Fecha recibido', 'Fecha de entrega', 'Terminado'
        ])
