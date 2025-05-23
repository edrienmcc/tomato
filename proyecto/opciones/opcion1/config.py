import os
from pathlib import Path

class DownloadConfig:
    # Configuración de descarga
    DEFAULT_DOWNLOAD_FOLDER = Path.home() / "Downloads" / "PornhubVideos"
    
    # Calidades preferidas (en orden de prioridad)
    QUALITY_PRIORITY = ['1080', '720', '480', '240']
    
    # Headers para requests
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://es.pornhub.com/'
    }
    
    # Configuración de descarga
    CHUNK_SIZE = 8192  # 8KB chunks
    MAX_FILENAME_LENGTH = 100
    
    # Extensiones de video soportadas
    SUPPORTED_EXTENSIONS = ['.mp4', '.webm', '.avi', '.mkv']
    
    # Patrones de búsqueda para URLs de video
    VIDEO_URL_PATTERNS = [
        r'"videoUrl":"([^"]+)"',
        r'videoUrl:\s*"([^"]+)"',
        r'"url":"(https://[^"]*\.mp4[^"]*)"',
        r'"1080":"([^"]+)"',
        r'"720":"([^"]+)"',
        r'"480":"([^"]+)"',
        r'"240":"([^"]+)"'
    ]
    
    @staticmethod
    def get_download_folder():
        """Obtiene la carpeta de descarga y la crea si no existe"""
        folder = DownloadConfig.DEFAULT_DOWNLOAD_FOLDER
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    
    @staticmethod
    def clean_filename(filename):
        """Limpia un nombre de archivo para que sea válido"""
        # Caracteres no permitidos
        invalid_chars = '<>:"/\\|?*'
        
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limitar longitud
        if len(filename) > DownloadConfig.MAX_FILENAME_LENGTH:
            filename = filename[:DownloadConfig.MAX_FILENAME_LENGTH]
        
        return filename.strip()