from urllib.parse import urljoin

def normalize_url(base_url, path):
    """
    Normaliza una URL asegurándose de que tenga el formato correcto
    """
    # Asegurarse de que la base_url termina con /
    if not base_url.endswith('/'):
        base_url += '/'
    
    # Eliminar / del inicio de path si existe
    if path.startswith('/'):
        path = path[1:]
    
    return urljoin(base_url, path)

def format_video_count(count_text):
    """
    Formatea el contador de videos para mostrarlo de manera más legible
    """
    try:
        # Eliminar comas y convertir a entero
        count = int(count_text.replace(',', ''))
        
        if count >= 1000000:
            return f"{count/1000000:.1f}M"
        elif count >= 1000:
            return f"{count/1000:.1f}K"
        else:
            return str(count)
    except:
        return count_text
