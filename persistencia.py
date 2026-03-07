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
        
        # Migrar columnas antiguas antes de guardar
        if 'Nombre de la tarea' in df.columns and 'Nombre de la actividad' not in df.columns:
            df = df.rename(columns={'Nombre de la tarea': 'Nombre de la actividad'})
        if 'Fecha recibido' in df.columns and 'Fecha de recepción' not in df.columns:
            df = df.rename(columns={'Fecha recibido': 'Fecha de recepción'})
        
        # Asegurar columnas requeridas con nombres correctos
        columnas_requeridas = [
            'id', 'Nombre de la actividad', 'Materia',
            'Tipo de actividad', 'Fecha de recepción',
            'Fecha de entrega', 'Terminado'
        ]
        for col in columnas_requeridas:
            if col not in df.columns:
                if col == 'Terminado':
                    df[col] = False
                elif col == 'Tipo de actividad':
                    df[col] = 'Tarea'
                else:
                    df[col] = ''
        
        # Convertir DataFrame a lista de diccionarios solo con columnas válidas
        cols_guardar = [c for c in columnas_requeridas if c in df.columns]
        tareas_lista = df[cols_guardar].to_dict('records')
        
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
                'id', 'Nombre de la actividad', 'Materia',
                'Tipo de actividad', 'Fecha de recepción',
                'Fecha de entrega', 'Terminado'
            ])
        
        with open(TAREAS_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        if not datos:
            return pd.DataFrame(columns=[
                'id', 'Nombre de la actividad', 'Materia',
                'Tipo de actividad', 'Fecha de recepción',
                'Fecha de entrega', 'Terminado'
            ])
        
        df = pd.DataFrame(datos)
        
        # Migrar columnas antiguas si existen
        if 'Nombre de la tarea' in df.columns and 'Nombre de la actividad' not in df.columns:
            df.rename(columns={'Nombre de la tarea': 'Nombre de la actividad'}, inplace=True)
        if 'Fecha recibido' in df.columns and 'Fecha de recepción' not in df.columns:
            df.rename(columns={'Fecha recibido': 'Fecha de recepción'}, inplace=True)
        
        # Asegurar columnas necesarias
        columnas_requeridas = [
            'id', 'Nombre de la actividad', 'Materia',
            'Tipo de actividad', 'Fecha de recepción',
            'Fecha de entrega', 'Terminado'
        ]
        for col in columnas_requeridas:
            if col not in df.columns:
                if col == 'Terminado':
                    df[col] = False
                elif col == 'Tipo de actividad':
                    df[col] = 'Tarea'
                else:
                    df[col] = ''
        
        # Asegurar que Terminado sea booleano
        df['Terminado'] = df['Terminado'].apply(lambda x: bool(x) if not isinstance(x, bool) else x)
        
        return df[columnas_requeridas]
    
    except Exception as e:
        print(f"Error al cargar tareas: {e}")
        return pd.DataFrame(columns=[
            'id', 'Nombre de la actividad', 'Materia',
            'Tipo de actividad', 'Fecha de recepción',
            'Fecha de entrega', 'Terminado'
        ])
