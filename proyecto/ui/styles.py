dark_style_sheet = """
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: "Segoe UI", Arial, sans-serif;
    }
    
    QMainWindow {
        background-color: #1e1e1e;
    }
    
    #sidebar {
        background-color: #252525;
        border-right: 1px solid #3a3a3a;
    }
    
    #sidebar-button {
        background-color: transparent;
        border: none;
        text-align: left;
        padding: 8px;
        font-size: 14px;
    }
    
    #sidebar-button:hover {
        background-color: #3a3a3a;
    }
    
    #sidebar-header {
        color: #a0a0a0;
        font-size: 12px;
        padding: 8px 0;
    }
    
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    
    #category-button {
        background-color: transparent;
        border: none;
        text-align: left;
        padding: 5px;
        font-size: 13px;
        color: #bebebe;
    }
    
    #category-button:hover {
        color: white;
    }
    
    #search-bar {
        background-color: #2a2a2a;
        border-bottom: 1px solid #3a3a3a;
    }
    
    #search-input {
        background-color: #333333;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 8px;
        color: white;
    }
    
    QPushButton {
        background-color: #404040;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        color: white;
    }
    
    QPushButton:hover {
        background-color: #505050;
    }
    
    #search-action-button {
        background-color: #6a6aff;
    }
    
    #search-action-button:hover {
        background-color: #8080ff;
    }
    
    #reset-button {
        background-color: transparent;
        border: 1px solid #404040;
    }
    
    #filters-panel {
        background-color: #252525;
        border-left: 1px solid #3a3a3a;
    }
    
    /* NUEVO: Estilos para panel de categorías de BD */
    #db-categories-panel {
        background-color: #252525;
        border-left: 1px solid #3a3a3a;
    }
    
    #db-panel-title {
        background-color: #2a2a2a;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    #db-category-button {
        background-color: transparent;
        border: 1px solid #404040;
        border-radius: 4px;
        text-align: left;
        padding: 8px 12px;
        font-size: 13px;
        color: #e0e0e0;
        margin: 2px 0;
    }
    
    #db-category-button:hover {
        background-color: #404040;
        border-color: #606060;
        color: white;
    }
    
    #db-category-button:pressed {
        background-color: #505050;
    }
    
    #reload-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: bold;
    }
    
    #reload-button:hover {
        background-color: #45a049;
    }
    
    #reload-button:disabled {
        background-color: #666666;
        color: #cccccc;
    }
    
    QLabel#filter-label {
        color: #a0a0a0;
        font-size: 12px;
    }
    
    QLineEdit {
        background-color: #333333;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 8px;
        color: white;
    }
    
    QComboBox {
        background-color: #333333;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 8px;
        color: white;
    }
    
    QComboBox::drop-down {
        width: 20px;
        border-left: 1px solid #505050;
    }
    
    QComboBox::down-arrow {
        width: 10px;
        height: 10px;
    }
    
    #collapsible-header {
        font-weight: bold;
        padding: 10px 0;
        border-bottom: 1px solid #404040;
    }
    
    #video-card {
        background-color: #252525;
        border-radius: 6px;
        padding: 0;
    }
    
    #video-title {
        font-weight: bold;
        margin-top: 5px;
        color: white;
    }
    
    #thumbnail-container {
        background-color: #1a1a1a;
        border-radius: 4px;
    }
    
    /* Estilos para QSplitter */
    QSplitter::handle {
        background-color: #3a3a3a;
        width: 2px;
        height: 2px;
    }
    
    QSplitter::handle:hover {
        background-color: #505050;
    }
"""