import mysql.connector
from mysql.connector import Error
import logging
from .config import DatabaseConfig

logger = logging.getLogger(__name__)

class CategoryManager:
    """Maneja las categorías desde la base de datos MySQL"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def get_categories_from_database(self):
        """
        Obtiene las categorías desde la base de datos siguiendo el flujo:
        1. Buscar en FNfxR_term_taxonomy donde taxonomy = 'category'
        2. Obtener los term_id de esos registros
        3. Buscar en FNfxR_terms los nombres correspondientes a esos term_id
        """
        connection = None
        categories = []
        
        try:
            connection = self.db_config.get_connection()
            if not connection:
                logger.error("❌ No se pudo establecer conexión con la base de datos")
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            # Query para obtener categorías con JOIN
            query = """
            SELECT 
                t.term_id,
                t.name,
                t.slug,
                tt.count,
                tt.description
            FROM FNfxR_terms t
            INNER JOIN FNfxR_term_taxonomy tt ON t.term_id = tt.term_id
            WHERE tt.taxonomy = 'category'
            AND tt.count > 0
            ORDER BY t.name ASC
            """
            
            logger.info("🔍 Consultando categorías en la base de datos...")
            cursor.execute(query)
            results = cursor.fetchall()
            
            for row in results:
                category = {
                    'id': row['term_id'],
                    'title': row['name'],
                    'slug': row['slug'],
                    'count': row['count'] if row['count'] else 0,
                    'description': row['description'] if row['description'] else '',
                    'url': f"/category/{row['slug']}"  # URL relativa
                }
                categories.append(category)
            
            logger.info(f"✅ Se encontraron {len(categories)} categorías en la base de datos")
            
        except Error as e:
            logger.error(f"❌ Error ejecutando consulta de categorías: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error general obteniendo categorías: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                logger.debug("🔌 Conexión a base de datos cerrada")
        
        return categories
    
    def get_category_by_id(self, term_id):
        """
        Obtiene una categoría específica por su term_id
        """
        connection = None
        
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                t.term_id,
                t.name,
                t.slug,
                tt.count,
                tt.description
            FROM FNfxR_terms t
            INNER JOIN FNfxR_term_taxonomy tt ON t.term_id = tt.term_id
            WHERE tt.taxonomy = 'category' AND t.term_id = %s
            """
            
            cursor.execute(query, (term_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'id': result['term_id'],
                    'title': result['name'],
                    'slug': result['slug'],
                    'count': result['count'] if result['count'] else 0,
                    'description': result['description'] if result['description'] else '',
                    'url': f"/category/{result['slug']}"
                }
            
        except Error as e:
            logger.error(f"❌ Error obteniendo categoría por ID: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        
        return None
    
    def search_categories(self, search_term):
        """
        Busca categorías que coincidan con un término de búsqueda
        """
        connection = None
        categories = []
        
        try:
            connection = self.db_config.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                t.term_id,
                t.name,
                t.slug,
                tt.count,
                tt.description
            FROM FNfxR_terms t
            INNER JOIN FNfxR_term_taxonomy tt ON t.term_id = tt.term_id
            WHERE tt.taxonomy = 'category'
            AND (t.name LIKE %s OR t.slug LIKE %s)
            ORDER BY t.name ASC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            results = cursor.fetchall()
            
            for row in results:
                category = {
                    'id': row['term_id'],
                    'title': row['name'],
                    'slug': row['slug'],
                    'count': row['count'] if row['count'] else 0,
                    'description': row['description'] if row['description'] else '',
                    'url': f"/category/{row['slug']}"
                }
                categories.append(category)
            
        except Error as e:
            logger.error(f"❌ Error buscando categorías: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
        
        return categories