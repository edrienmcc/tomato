import requests
import logging
import json
import os
from pathlib import Path
import time
from PyQt5.QtCore import QObject, pyqtSignal

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('StreamWishUploader')

class UploadProgressReporter(QObject):
    """Señales para reportar progreso de upload"""
    upload_progress = pyqtSignal(int)  # 0-100
    status_changed = pyqtSignal(str)   # Mensaje de estado

class StreamWishUploader(QObject):
    """
    Cliente para subir videos a StreamWish usando su API
    """
    
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key
        self.server_info_url = "https://streamhgapi.com/api/upload/server"
        self.upload_url = None  # Se obtendrá dinámicamente
        
        # Reporter de progreso
        self.progress_reporter = UploadProgressReporter()
        
        # Headers para las requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Configuración por defecto
        self.default_config = {
            'file_public': 1,      # Público por defecto
            'file_adult': 1,       # Contenido adulto
            'tags': 'pornhub, video, hd',
            'fld_id': None,        # Carpeta (opcional)
            'cat_id': None         # Categoría (opcional)
        }
    
    def set_api_key(self, api_key):
        """
        Establece la clave API
        """
        self.api_key = api_key
        logger.info("✅ API key configurada")
    
    def get_upload_server(self):
        """
        Obtiene la URL del servidor de upload dinámicamente
        """
        try:
            if not self.api_key:
                logger.error("❌ API key no configurada")
                return None
            
            params = {'key': self.api_key}
            logger.info(f"🌐 Obteniendo servidor de upload...")
            
            response = requests.get(
                self.server_info_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            logger.info(f"📊 Respuesta servidor: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    logger.info(f"📋 Info del servidor: {result}")
                    
                    if result.get('status') == 200 and result.get('result'):
                        upload_url = result['result']
                        logger.info(f"✅ Servidor de upload obtenido: {upload_url}")
                        return upload_url
                    else:
                        logger.error(f"❌ Error en respuesta del servidor: {result}")
                        return None
                        
                except json.JSONDecodeError:
                    logger.error(f"❌ Respuesta no JSON: {response.text[:300]}")
                    return None
            else:
                logger.error(f"❌ Error HTTP obteniendo servidor: {response.status_code}")
                logger.error(f"❌ Respuesta: {response.text[:300]}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error obteniendo servidor de upload: {str(e)}")
            return None
    
    def test_connection(self):
        """
        Prueba la conexión con la API obteniendo la info del servidor
        """
        try:
            if not self.api_key:
                logger.error("❌ API key no configurada para test")
                return False
            
            logger.info("🔍 Validando API key...")
            logger.info(f"🌐 Probando conexión con API key: {self.api_key[:8]}...")
            
            # En lugar de subir un archivo, solo obtener la info del servidor
            upload_url = self.get_upload_server()
            
            if upload_url:
                self.upload_url = upload_url
                logger.info("✅ API key válida - Conexión exitosa")
                return True
            else:
                logger.error("❌ API key inválida o error de conexión")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en validación de API key: {str(e)}")
            return False
    
    def validate_api_key_format(self):
        """
        Valida el formato básico de la API key
        """
        if not self.api_key:
            logger.error("❌ No hay API key para validar")
            return False
        
        # Verificaciones básicas de formato
        if len(self.api_key) < 10:
            logger.error("❌ API key demasiado corta")
            return False
        
        if len(self.api_key) > 50:
            logger.error("❌ API key demasiado larga")
            return False
        
        logger.info("✅ Formato de API key válido")
        return True
    
    def upload_video(self, video_path, video_data=None, custom_config=None):
        """
        Sube un video a StreamWish con progreso
        
        Args:
            video_path: Ruta al archivo de video
            video_data: Datos del video (título, descripción, etc.)
            custom_config: Configuración personalizada
            
        Returns:
            dict: Respuesta de la API con información del video subido
        """
        try:
            if not self.api_key:
                logger.error("❌ API key no configurada")
                return None
            
            if not os.path.exists(video_path):
                logger.error(f"❌ Archivo no encontrado: {video_path}")
                return None
            
            # Validar que sea un archivo de video
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
            file_ext = os.path.splitext(video_path)[1].lower()
            
            if file_ext not in video_extensions:
                logger.error(f"❌ Formato de archivo no soportado: {file_ext}")
                logger.error("❌ StreamWish solo acepta archivos de video")
                return None
            
            # Obtener URL de upload si no la tenemos
            if not self.upload_url:
                self.progress_reporter.status_changed.emit("🌐 Obteniendo servidor...")
                self.upload_url = self.get_upload_server()
                if not self.upload_url:
                    logger.error("❌ No se pudo obtener servidor de upload")
                    return None
            
            # Preparar datos del video
            upload_data = self._prepare_upload_data(video_data, custom_config)
            
            logger.info(f"📤 Iniciando upload: {os.path.basename(video_path)}")
            logger.info(f"📊 Tamaño del archivo: {self._get_file_size_mb(video_path):.1f} MB")
            logger.info(f"🎬 Formato: {file_ext}")
            
            self.progress_reporter.status_changed.emit("📤 Subiendo video...")
            
            # Realizar upload
            response = self._upload_to_server_with_progress(self.upload_url, upload_data, video_path)
            
            if response:
                result = self._process_response(response)
                if result:
                    self.progress_reporter.upload_progress.emit(100)
                    self.progress_reporter.status_changed.emit("✅ Upload completado!")
                return result
            else:
                logger.error("❌ Upload falló")
                self.progress_reporter.status_changed.emit("❌ Error en upload")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error durante el upload: {str(e)}")
            self.progress_reporter.status_changed.emit(f"❌ Error: {str(e)}")
            return None
    
    def _prepare_upload_data(self, video_data, custom_config):
        """
        Prepara los datos para el upload
        """
        upload_data = {'key': self.api_key}
        
        # Configuración por defecto
        upload_data.update(self.default_config)
        
        # Configuración personalizada
        if custom_config:
            upload_data.update(custom_config)
        
        # Datos del video
        if video_data:
            if video_data.get('title'):
                upload_data['file_title'] = self._clean_title(video_data['title'])
            
            if video_data.get('description'):
                upload_data['file_descr'] = video_data['description']
            
            # Agregar tags adicionales basados en el video
            additional_tags = self._generate_tags(video_data)
            if additional_tags:
                existing_tags = upload_data.get('tags', '')
                upload_data['tags'] = f"{existing_tags}, {additional_tags}"
        
        logger.info(f"📋 Datos de upload preparados: {list(upload_data.keys())}")
        return upload_data
    
    def _upload_to_server_with_progress(self, url, data, video_path):
        """
        Realiza el upload al servidor con progreso
        """
        try:
            logger.info(f"🌐 Subiendo a: {url}")
            
            file_size = os.path.getsize(video_path)
            uploaded = 0
            
            # Crear clase personalizada para monitorear progreso
            class ProgressFile:
                def __init__(self, file_path, progress_callback):
                    self.file = open(file_path, 'rb')
                    self.progress_callback = progress_callback
                    self.uploaded = 0
                    self.total_size = os.path.getsize(file_path)
                
                def read(self, size=-1):
                    chunk = self.file.read(size)
                    if chunk:
                        self.uploaded += len(chunk)
                        progress = int((self.uploaded / self.total_size) * 100)
                        self.progress_callback(progress)
                    return chunk
                
                def close(self):
                    self.file.close()
                
                def __enter__(self):
                    return self
                
                def __exit__(self, *args):
                    self.close()
            
            # Función callback para progreso
            def progress_callback(progress):
                self.progress_reporter.upload_progress.emit(progress)
                if progress % 10 == 0 and progress > 0:
                    mb_uploaded = (progress / 100) * (file_size / (1024*1024))
                    mb_total = file_size / (1024*1024)
                    logger.info(f"📤 Upload: {progress}% ({mb_uploaded:.1f}/{mb_total:.1f} MB)")
            
            # Preparar archivo con monitoreo de progreso
            with ProgressFile(video_path, progress_callback) as progress_file:
                files = {
                    'file': (os.path.basename(video_path), progress_file, 'video/mp4')
                }
                
                # Realizar upload
                response = requests.post(
                    url,
                    data=data,
                    files=files,
                    headers=self.headers,
                    timeout=600,  # 10 minutos timeout para videos grandes
                )
            
            if response.status_code == 200:
                logger.info("✅ Upload completado exitosamente")
                return response
            else:
                logger.error(f"❌ Error HTTP: {response.status_code}")
                logger.error(f"❌ Respuesta: {response.text[:500]}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout durante el upload (el video puede ser muy grande)")
            self.progress_reporter.status_changed.emit("❌ Timeout en upload")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("❌ Error de conexión durante upload")
            self.progress_reporter.status_changed.emit("❌ Error de conexión")
            return None
        except Exception as e:
            logger.error(f"❌ Error en upload: {str(e)}")
            self.progress_reporter.status_changed.emit(f"❌ Error upload: {str(e)}")
            return None
    
    def _process_response(self, response):
        """
        Procesa la respuesta del servidor
        """
        try:
            # Intentar parsear como JSON
            try:
                result = response.json()
                logger.info("📋 Respuesta JSON recibida")
                logger.info(f"📊 Contenido: {result}")
            except json.JSONDecodeError:
                # Si no es JSON, puede ser HTML redirect
                result = {
                    'status': 200,
                    'msg': 'Upload successful (HTML response)',
                    'html_response': response.text[:1000]
                }
                logger.info("📋 Respuesta HTML recibida")
                logger.info(f"📄 Contenido: {response.text[:500]}")
            
            # Procesar resultado
            if result.get('status') == 200 or result.get('msg') == 'OK':
                logger.info("✅ Upload exitoso!")
                
                # Mostrar información de archivos subidos
                if 'files' in result:
                    for file_info in result['files']:
                        filecode = file_info.get('filecode', 'N/A')
                        filename = file_info.get('filename', 'N/A')
                        file_status = file_info.get('status', 'N/A')
                        
                        logger.info(f"📁 Archivo: {filename}")
                        logger.info(f"🔗 Código: {filecode}")
                        logger.info(f"📊 Estado: {file_status}")
                        
                        # Construir URLs de acceso
                        if filecode != 'N/A':
                            view_url = f"https://streamwish.to/{filecode}"
                            embed_url = f"https://streamwish.to/e/{filecode}"
                            
                            logger.info(f"🌐 Ver: {view_url}")
                            logger.info(f"📺 Embed: {embed_url}")
                elif 'html_response' in result:
                    # Buscar códigos de archivo en respuesta HTML
                    html_content = result['html_response']
                    logger.info("🔍 Buscando códigos de archivo en respuesta HTML...")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error procesando respuesta: {str(e)}")
            return None
    
    def _clean_title(self, title):
        """
        Limpia el título para StreamWish
        """
        # Eliminar caracteres especiales
        clean_title = title.replace('\n', ' ').replace('\r', ' ')
        
        # Limitar longitud
        if len(clean_title) > 100:
            clean_title = clean_title[:97] + "..."
        
        return clean_title.strip()
    
    def _generate_tags(self, video_data):
        """
        Genera tags adicionales basados en los datos del video
        """
        tags = []
        
        # Tags basados en duración
        if video_data.get('duration'):
            duration = video_data['duration']
            if ':' in duration:
                try:
                    parts = duration.split(':')
                    minutes = int(parts[-2]) if len(parts) > 1 else 0
                    if minutes > 30:
                        tags.append('long')
                    elif minutes > 15:
                        tags.append('medium')
                    else:
                        tags.append('short')
                except:
                    pass
        
        # Tags basados en uploader
        if video_data.get('uploader'):
            uploader = video_data['uploader'].lower()
            if any(word in uploader for word in ['premium', 'official', 'verified']):
                tags.append('premium')
        
        return ', '.join(tags)
    
    def _get_file_size_mb(self, file_path):
        """
        Obtiene el tamaño del archivo en MB
        """
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except:
            return 0