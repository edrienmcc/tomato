import requests
from bs4 import BeautifulSoup
import logging
import time
import random
from urllib.parse import urljoin

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Opcion1Scraper')

class Opcion1Scraper:
    def __init__(self):
        self.base_url = "https://es.pornhub.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def get_categories(self):
        """Obtiene todas las categorías disponibles"""
        try:
            url = urljoin(self.base_url, "/categories")
            logger.info(f"Obteniendo categorías desde: {url}")
            
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"Error al obtener categorías: {response.status_code}")
                return []
            
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            categories = []
            
            category_items = soup.select('#categoriesListingWrapper .catPic')
            
            for item in category_items:
                link_elem = item.select_one('.categoryTitleWrapper a')
                if not link_elem:
                    continue
                
                title_elem = link_elem.select_one('strong')
                if not title_elem:
                    continue
                
                video_count_elem = link_elem.select_one('.videoCount var')
                
                category = {
                    'title': title_elem.text.strip(),
                    'url': link_elem['href'],
                    'count': video_count_elem.text.strip() if video_count_elem else "0"
                }
                categories.append(category)
                
            logger.info(f"Se encontraron {len(categories)} categorías")
            return categories
        
        except Exception as e:
            logger.error(f"Error al obtener categorías: {str(e)}")
            return []
    
    def get_videos(self, category_url):
        """Obtiene videos de una categoría específica"""
        try:
            full_url = urljoin(self.base_url, category_url)
            logger.info(f"Obteniendo videos desde: {full_url}")
            
            response = requests.get(full_url, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"Error al obtener videos: {response.status_code}")
                yield None
                return
            
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # Usar el selector correcto basado en el HTML real
            video_items = soup.select('li.pcVideoListItem')
            
            if not video_items:
                # Selector alternativo
                video_items = soup.select('ul#videoCategory li')
            
            # Filtrar elementos publicitarios
            filtered_items = []
            for item in video_items:
                # Excluir elementos que contienen publicidad
                if self._is_advertisement(item):
                    continue
                filtered_items.append(item)
                
            logger.info(f"Encontrados {len(video_items)} elementos totales, {len(filtered_items)} videos válidos después de filtrar publicidad")
            
            count = 0
            for item in filtered_items:
                video_data = self._extract_video_data_from_real_html(item)
                
                if video_data:
                    count += 1
                    yield video_data
                    # Pequeño delay para evitar ser bloqueado
                    time.sleep(random.uniform(0.1, 0.3))
            
            logger.info(f"Se procesaron {count} videos para {category_url}")
            
        except Exception as e:
            logger.error(f"Error al obtener videos: {str(e)}")
            yield None
    
    def _is_advertisement(self, item):
        """Detecta si un elemento es publicidad"""
        try:
            # Buscar indicadores de publicidad
            ad_indicators = [
                '.tj-inban-container',  # TrafficJunky ads
                '.tj-inban-icon',
                '[data-url*="trafficjunky"]',
                '.mcacdmgrhc',  # Contenedor de anuncios
                '.mbbdfhgfle',  # Otro contenedor de anuncios
                'cbcac',  # Tag de anuncio
                'bdhdd'   # Otro tag de anuncio
            ]
            
            # Verificar si contiene algún indicador de publicidad
            for selector in ad_indicators:
                if item.select(selector):
                    logger.debug("Elemento publicitario detectado y filtrado")
                    return True
            
            # Verificar por texto que indique publicidad
            item_text = item.get_text().lower()
            ad_texts = [
                'ad by traff',
                'traffic junky',
                'advertising',
                'publicidad'
            ]
            
            for ad_text in ad_texts:
                if ad_text in item_text:
                    logger.debug(f"Publicidad detectada por texto: {ad_text}")
                    return True
            
            # Verificar si no tiene estructura de video válida
            # Un video válido debe tener título y enlace
            if not item.select('.title a') and not item.select('a.linkVideoThumb'):
                logger.debug("Elemento sin estructura de video válida")
                return True
            
            # Verificar elementos con clases dinámicas (anuncios suelen tener clases generadas)
            class_names = item.get('class', [])
            for class_name in class_names:
                # Clases con muchos números/caracteres aleatorios suelen ser anuncios
                if len(class_name) > 10 and any(char.isdigit() for char in class_name):
                    # Pero solo si no es pcVideoListItem que sabemos que es válido
                    if class_name != 'pcVideoListItem':
                        logger.debug(f"Posible anuncio detectado por clase dinámica: {class_name}")
                        return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Error verificando publicidad: {str(e)}")
            return False

    def _extract_video_data_from_real_html(self, item):
        """Extrae datos de video del HTML real proporcionado"""
        try:
            # Extraer título desde .title a
            title = ""
            title_elem = item.select_one('.title a')
            if title_elem:
                title = title_elem.get('title', '') or title_elem.text.strip()
            
            # Si no hay título, buscar en data-title del enlace principal
            if not title:
                main_link = item.select_one('a.linkVideoThumb')
                if main_link:
                    title = main_link.get('data-title', '')
            
            # Extraer URL del video
            video_url = ""
            link_elem = item.select_one('.title a')
            if link_elem and link_elem.get('href'):
                video_url = urljoin(self.base_url, link_elem['href'])
            
            # Si no encontramos URL en .title a, buscar en el enlace principal
            if not video_url:
                main_link = item.select_one('a.linkVideoThumb')
                if main_link and main_link.get('href'):
                    video_url = urljoin(self.base_url, main_link['href'])
            
            # Extraer miniatura
            thumbnail = ""
            img_elem = item.select_one('img.thumb')
            if img_elem:
                # Priorizar data-mediumthumb, luego src
                thumbnail = (img_elem.get('data-mediumthumb') or 
                           img_elem.get('src') or 
                           img_elem.get('data-src') or "")
            
            # Extraer duración
            duration = ""
            duration_elem = item.select_one('.duration')
            if duration_elem:
                duration = duration_elem.text.strip()
            
            # Extraer vistas
            views = ""
            views_elem = item.select_one('.views var')
            if views_elem:
                views = views_elem.text.strip()
            
            # Extraer rating
            rating = ""
            rating_elem = item.select_one('.rating-container .value')
            if rating_elem:
                rating = rating_elem.text.strip()
            
            # Extraer canal/uploader
            uploader = ""
            uploader_elem = item.select_one('.usernameWrap a')
            if uploader_elem:
                uploader = uploader_elem.text.strip()
            
            # Solo devolver si tenemos datos mínimos necesarios
            if title and video_url:
                video_data = {
                    'title': title,
                    'url': video_url,
                    'thumbnail': thumbnail,
                    'duration': duration,
                    'views': views,
                    'rating': rating,
                    'uploader': uploader
                }
                
                logger.debug(f"Video extraído: {title[:50]}...")
                return video_data
            else:
                logger.debug(f"Video incompleto - Título: '{title}', URL: '{video_url}'")
                
        except Exception as e:
            logger.debug(f"Error extrayendo datos de video: {str(e)}")
            
        return None