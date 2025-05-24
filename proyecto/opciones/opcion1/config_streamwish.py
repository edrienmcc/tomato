import os
import json
from pathlib import Path

class StreamWishConfig:
    """
    Maneja la configuración de StreamWish
    """
    
    def __init__(self):
        self.config_file = Path.home() / ".pornhub_downloader" / "streamwish_config.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Carga la configuración desde el archivo
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Configuración por defecto
        return {
            'api_key': '',
            'auto_upload': False,
            'delete_after_upload': False,  # AÑADIDO: Por defecto no eliminar
            'upload_settings': {
                'file_public': 1,
                'file_adult': 1,
                'tags': 'pornhub, hd, video',
                'fld_id': None,
                'cat_id': None
            }
        }
    
    def _save_config(self):
        """
        Guarda la configuración al archivo
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {str(e)}")
            return False
    
    def set_api_key(self, api_key):
        """
        Establece la API key
        """
        self.config['api_key'] = api_key
        return self._save_config()
    
    def get_api_key(self):
        """
        Obtiene la API key
        """
        return self.config.get('api_key', '')
    
    def set_auto_upload(self, enabled):
        """
        Habilita/deshabilita upload automático
        """
        self.config['auto_upload'] = enabled
        return self._save_config()
    
    def is_auto_upload_enabled(self):
        """
        Verifica si el upload automático está habilitado
        """
        return self.config.get('auto_upload', False)
    
    def set_delete_after_upload(self, enabled):
        """
        Habilita/deshabilita eliminación después del upload
        """
        self.config['delete_after_upload'] = enabled
        return self._save_config()
    
    def is_delete_after_upload_enabled(self):
        """
        Verifica si se debe eliminar el archivo después del upload
        """
        return self.config.get('delete_after_upload', False)
    
    def update_upload_settings(self, settings):
        """
        Actualiza configuración de upload
        """
        self.config['upload_settings'].update(settings)
        return self._save_config()
    
    def get_upload_settings(self):
        """
        Obtiene configuración de upload
        """
        return self.config.get('upload_settings', {})
    
    def is_configured(self):
        """
        Verifica si StreamWish está configurado
        """
        api_key = self.get_api_key()
        return api_key and len(api_key) > 10