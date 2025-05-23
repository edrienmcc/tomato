import mysql.connector
from mysql.connector import Error
import logging
import time

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Configuración de la base de datos MySQL"""
    
    def __init__(self):
        # Configuración de la base de datos - MODIFICA ESTOS VALORES
        self.config = {
            'host': '154.12.238.207',
            'database': 'xpleasure_xl',
            'user': 'xpleasure_xl',
            'password': 'aT6L3Ma6U1',
            'port': 3306,
            'charset': 'utf8mb4',
            'autocommit': True,
            'connection_timeout': 10,  # Timeout de conexión
            'auth_plugin': 'mysql_native_password',  # Plugin de autenticación
            'raise_on_warnings': False,
            'use_unicode': True,
            'buffered': True
        }
    
    def get_connection(self, retries=3, delay=1):
        """
        Establece y devuelve una conexión a la base de datos con reintentos
        """
        last_error = None
        
        for attempt in range(retries):
            try:
                logger.info(f"🔄 Intento de conexión {attempt + 1}/{retries} a {self.config['host']}:{self.config['port']}")
                
                connection = mysql.connector.connect(**self.config)
                
                if connection.is_connected():
                    db_info = connection.get_server_info()
                    logger.info(f"✅ Conexión establecida - MySQL Server versión: {db_info}")
                    return connection
                    
            except Error as e:
                last_error = e
                error_code = getattr(e, 'errno', 'N/A')
                error_msg = str(e)
                
                logger.warning(f"❌ Intento {attempt + 1} falló - Error {error_code}: {error_msg}")
                
                # Diagnóstico específico según el tipo de error
                if error_code == 2003:  # Can't connect to MySQL server
                    logger.error("🔧 Error 2003: No se puede conectar al servidor MySQL")
                    logger.error("   - Verifica que el host y puerto sean correctos")
                    logger.error("   - Verifica que el servidor MySQL esté ejecutándose")
                    logger.error("   - Verifica la conectividad de red")
                elif error_code == 1045:  # Access denied
                    logger.error("🔧 Error 1045: Acceso denegado")
                    logger.error("   - Verifica el usuario y contraseña")
                    logger.error("   - Verifica los permisos del usuario")
                elif error_code == 1049:  # Unknown database
                    logger.error("🔧 Error 1049: Base de datos desconocida")
                    logger.error(f"   - Verifica que la base de datos '{self.config['database']}' exista")
                elif error_code == 2005:  # Unknown host
                    logger.error("🔧 Error 2005: Host desconocido")
                    logger.error(f"   - Verifica que el host '{self.config['host']}' sea correcto")
                
                if attempt < retries - 1:
                    logger.info(f"⏳ Esperando {delay} segundos antes del siguiente intento...")
                    time.sleep(delay)
                    delay *= 2  # Backoff exponencial
            
            except Exception as e:
                last_error = e
                logger.error(f"❌ Error inesperado: {str(e)}")
                break
        
        logger.error(f"💥 Falló conexión después de {retries} intentos. Último error: {last_error}")
        return None
    
    def test_connection(self):
        """
        Prueba la conexión a la base de datos con diagnóstico detallado
        """
        logger.info("🧪 Iniciando test de conexión...")
        
        # Test básico de conectividad
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.config['host'], self.config['port']))
            sock.close()
            
            if result != 0:
                logger.error(f"🌐 Error de conectividad de red al host {self.config['host']}:{self.config['port']}")
                return False
            else:
                logger.info(f"🌐 Conectividad de red OK al host {self.config['host']}:{self.config['port']}")
        except Exception as e:
            logger.error(f"🌐 Error verificando conectividad: {e}")
            return False
        
        # Test de conexión MySQL
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Test básico
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                logger.info(f"✅ Query test exitoso: {result}")
                
                # Test de base de datos
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()
                logger.info(f"📂 Base de datos actual: {db_name[0] if db_name else 'None'}")
                
                # Test de permisos
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                logger.info(f"📋 Tablas encontradas: {len(tables)}")
                
                cursor.close()
                connection.close()
                logger.info("✅ Test de conexión completamente exitoso")
                return True
                
            except Error as e:
                logger.error(f"❌ Error en test de base de datos: {e}")
                if connection.is_connected():
                    connection.close()
                return False
        
        return False
    
    def get_connection_info(self):
        """
        Obtiene información detallada de la conexión
        """
        info = {
            'host': self.config['host'],
            'port': self.config['port'],
            'database': self.config['database'],
            'user': self.config['user'],
            'connection_status': False,
            'server_version': None,
            'tables_count': 0,
            'error': None
        }
        
        try:
            connection = self.get_connection()
            if connection:
                info['connection_status'] = True
                info['server_version'] = connection.get_server_info()
                
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                info['tables_count'] = len(tables)
                
                cursor.close()
                connection.close()
                
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def diagnose_connection(self):
        """
        Diagnóstico completo de la conexión
        """
        print("\n" + "="*60)
        print("🔍 DIAGNÓSTICO DE CONEXIÓN A BASE DE DATOS")
        print("="*60)
        
        print(f"🖥️  Host: {self.config['host']}")
        print(f"🔢 Puerto: {self.config['port']}")
        print(f"📂 Base de datos: {self.config['database']}")
        print(f"👤 Usuario: {self.config['user']}")
        print(f"🔒 Contraseña: {'*' * len(self.config['password'])}")
        
        # Test de conectividad de red
        print(f"\n🌐 Test de conectividad de red...")
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.config['host'], self.config['port']))
            sock.close()
            
            if result == 0:
                print("   ✅ Conectividad de red: OK")
            else:
                print("   ❌ Conectividad de red: FALLO")
                print("   💡 Verifica firewall, host y puerto")
                return False
        except Exception as e:
            print(f"   ❌ Error de red: {e}")
            return False
        
        # Test de conexión MySQL
        print(f"\n🔗 Test de conexión MySQL...")
        connection = self.get_connection(retries=1)
        if connection:
            try:
                cursor = connection.cursor()
                
                # Información del servidor
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"   ✅ Versión del servidor: {version[0]}")
                
                # Base de datos actual
                cursor.execute("SELECT DATABASE()")
                db = cursor.fetchone()
                print(f"   ✅ Base de datos: {db[0] if db else 'None'}")
                
                # Tablas
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"   ✅ Tablas encontradas: {len(tables)}")
                
                if tables:
                    print("   📋 Tablas:")
                    for table in tables[:10]:  # Mostrar máximo 10 tablas
                        print(f"      - {table[0]}")
                    if len(tables) > 10:
                        print(f"      ... y {len(tables) - 10} más")
                
                cursor.close()
                connection.close()
                print("   ✅ Conexión: EXITOSA")
                return True
                
            except Error as e:
                print(f"   ❌ Error de MySQL: {e}")
                if connection.is_connected():
                    connection.close()
                return False
        else:
            print("   ❌ Conexión: FALLIDA")
            return False
    
    def create_test_table(self):
        """
        Crea una tabla de test para verificar permisos de escritura
        """
        connection = self.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Crear tabla de test
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    test_data VARCHAR(100)
                )
            """)
            
            # Insertar datos de test
            cursor.execute("""
                INSERT INTO connection_test (test_data) 
                VALUES ('Test connection successful')
            """)
            
            # Leer datos
            cursor.execute("SELECT * FROM connection_test ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            
            # Limpiar tabla de test
            cursor.execute("DROP TABLE connection_test")
            
            cursor.close()
            connection.close()
            
            logger.info(f"✅ Test de escritura exitoso: {result}")
            return True
            
        except Error as e:
            logger.error(f"❌ Error en test de escritura: {e}")
            if connection.is_connected():
                connection.close()
            return False