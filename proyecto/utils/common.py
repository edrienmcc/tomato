import os
import logging
import time
import random
from PyQt5.QtGui import QPixmap, QImage
import requests
from io import BytesIO

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Configura y devuelve un logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Crear un formateador
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Crear un manejador para stdout
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Si se especifica un archivo de log, crear un manejador para él
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def load_image_from_url(url, default_pixmap=None):
    """
    Carga una imagen desde una URL y devuelve un QPixmap
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        # Si la URL es relativa, no intentar cargarla
        if not url.startswith(('http://', 'https://')):
            return default_pixmap if default_pixmap else QPixmap()
            
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            image = QImage()
            image.loadFromData(response.content)
            if not image.isNull():
                return QPixmap.fromImage(image)
                
    except Exception as e:
        print(f"Error al cargar imagen desde {url}: {str(e)}")
    
    return default_pixmap if default_pixmap else QPixmap()

def add_delay(min_seconds=0.5, max_seconds=2.0):
    """
    Añade un retraso aleatorio para evitar ser bloqueado por servidores
    """
    time.sleep(random.uniform(min_seconds, max_seconds))

def create_directory_if_not_exists(directory_path):
    """
    Crea un directorio si no existe
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False

def normalize_image_url(url, base_url):
    """
    Normaliza una URL de imagen para asegurar que sea completa
    """
    if not url:
        return ""
    
    if url.startswith('//'):
        return 'https:' + url
    elif url.startswith('/'):
        return base_url.rstrip('/') + url
    elif url.startswith('http'):
        return url
    else:
        return base_url.rstrip('/') + '/' + url

def save_to_file(content, file_path):
    """
    Guarda contenido en un archivo
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Error al guardar archivo {file_path}: {str(e)}")
        return False

def load_from_file(file_path):
    """
    Carga contenido desde un archivo
    """
    try:
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error al cargar archivo {file_path}: {str(e)}")
        return None