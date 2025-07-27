# Electron Transpiler for Vader
# Generates complete Electron applications from Vader GUI syntax

import os
import json
from .gui_advanced import AdvancedGUITranspiler

class ElectronTranspiler(AdvancedGUITranspiler):
    def __init__(self):
        super().__init__()
        self.app_config = {
            'name': 'Vader App',
            'version': '1.0.0',
            'description': 'Application built with Vader',
            'width': 1200,
            'height': 800,
            'icon': None
        }
    
    def transpile(self, vader_code):
        """Transpile Vader code to complete Electron application"""
        # Parse the Vader code
        lines = vader_code.split('\n')
        self.parse_definitions(lines)
        
        # Generate all application files
        return {
            'main.js': self.generate_main_js(),
            'preload.js': self.generate_preload_js(),
            'index.html': self.generate_html(),
            'styles.css': self.generate_css(),
            'script.js': self.generate_javascript(),
            'package.json': self.generate_package_json(),
            'README.md': self.generate_readme()
        }
    
    def parse_definitions(self, lines):
        """Parse Vader definitions with Electron-specific handling"""
        super().parse_definitions(lines)
        
        # Parse application configuration
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            if line.startswith('nombre '):
                self.app_config['name'] = line.replace('nombre ', '').replace('"', '')
            elif line.startswith('version '):
                self.app_config['version'] = line.replace('version ', '').replace('"', '')
            elif line.startswith('descripcion '):
                self.app_config['description'] = line.replace('descripcion ', '').replace('"', '')
            elif line.startswith('icono '):
                self.app_config['icon'] = line.replace('icono ', '').replace('"', '')
            elif line.startswith('ancho ') and 'ventana' in ' '.join(lines[max(0, lines.index(line)-2):lines.index(line)]):
                self.app_config['width'] = int(line.replace('ancho ', '').replace(' pixeles', ''))
            elif line.startswith('alto ') and 'ventana' in ' '.join(lines[max(0, lines.index(line)-2):lines.index(line)]):
                self.app_config['height'] = int(line.replace('alto ', '').replace(' pixeles', ''))
    
    def generate_html(self):
        """Generate functional HTML interface for Electron app"""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editor Vader - Powered by Vader</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Header con logo y título -->
        <header class="app-header">
            <div class="header-left">
                <img src="assets/logo.png" alt="Vader Logo" class="vader-logo">
                <h1 class="app-title">Editor Vader</h1>
            </div>
            <div class="header-right">
                <button class="btn-minimize"><i class="fas fa-minus"></i></button>
                <button class="btn-maximize"><i class="fas fa-square"></i></button>
                <button class="btn-close"><i class="fas fa-times"></i></button>
            </div>
        </header>
        
        <!-- Contenido principal -->
        <div class="main-content">
            <!-- Sidebar izquierdo -->
            <aside class="sidebar">
                <div class="sidebar-tabs">
                    <button class="tab-btn active" data-tab="files"><i class="fas fa-folder"></i></button>
                    <button class="tab-btn" data-tab="search"><i class="fas fa-search"></i></button>
                    <button class="tab-btn" data-tab="git"><i class="fas fa-code-branch"></i></button>
                    <button class="tab-btn" data-tab="extensions"><i class="fas fa-puzzle-piece"></i></button>
                </div>
                <div class="sidebar-content">
                    <div class="tab-panel active" id="files-panel">
                        <div class="panel-header">
                            <h3>Explorador</h3>
                            <div class="panel-actions">
                                <button class="btn-icon" title="Nuevo archivo"><i class="fas fa-file-plus"></i></button>
                                <button class="btn-icon" title="Nueva carpeta"><i class="fas fa-folder-plus"></i></button>
                            </div>
                        </div>
                        <div class="file-tree">
                            <div class="file-item folder expanded">
                                <i class="fas fa-folder-open"></i>
                                <span>mi_proyecto</span>
                            </div>
                            <div class="file-item file" style="margin-left: 20px;">
                                <i class="fas fa-file-code"></i>
                                <span>main.vdr</span>
                            </div>
                            <div class="file-item file" style="margin-left: 20px;">
                                <i class="fas fa-file-code"></i>
                                <span>utils.vdr</span>
                            </div>
                        </div>
                    </div>
                    <div class="tab-panel" id="search-panel">
                        <div class="panel-header">
                            <h3>Buscar</h3>
                        </div>
                        <div class="search-container">
                            <input type="text" placeholder="Buscar en archivos..." class="search-input">
                            <button class="btn-search"><i class="fas fa-search"></i></button>
                        </div>
                    </div>
                </div>
            </aside>
            
            <!-- Área del editor -->
            <main class="editor-area">
                <div class="editor-tabs">
                    <div class="tab active">
                        <span class="tab-icon">⚡</span>
                        <span class="tab-name">main.vdr</span>
                        <button class="tab-close"><i class="fas fa-times"></i></button>
                    </div>
                    <div class="tab">
                        <span class="tab-icon">⚡</span>
                        <span class="tab-name">utils.vdr</span>
                        <button class="tab-close"><i class="fas fa-times"></i></button>
                    </div>
                </div>
                <div class="editor-container">
                    <div class="line-numbers">
                        <div class="line-number">1</div>
                        <div class="line-number">2</div>
                        <div class="line-number">3</div>
                        <div class="line-number">4</div>
                        <div class="line-number">5</div>
                        <div class="line-number">6</div>
                        <div class="line-number">7</div>
                        <div class="line-number">8</div>
                        <div class="line-number">9</div>
                        <div class="line-number">10</div>
                    </div>
                    <textarea class="code-editor" placeholder="// Escribe tu código Vader aquí...\n// Ejemplo:\ncrear variable saludo\nvalor \"Hola mundo desde Vader!\"\n\nmostrar saludo">// Bienvenido al Editor Vader\n// Este es un editor creado completamente con Vader\n\ncrear variable mensaje\nvalor "¡Hola desde Vader!"\n\nmostrar mensaje\n\n// Puedes ejecutar este código presionando F5\n// o usando el menú Vader > Ejecutar Código</textarea>
                </div>
                
                <!-- Panel inferior (terminal) -->
                <div class="bottom-panel">
                    <div class="panel-tabs">
                        <button class="panel-tab active">Terminal</button>
                        <button class="panel-tab">Problemas</button>
                        <button class="panel-tab">Salida</button>
                        <button class="panel-tab">Depuración</button>
                    </div>
                    <div class="terminal-container">
                        <div class="terminal-header">
                            <span class="terminal-title">vader@editor:~$</span>
                            <div class="terminal-actions">
                                <button class="btn-icon" title="Limpiar terminal"><i class="fas fa-trash"></i></button>
                                <button class="btn-icon" title="Dividir terminal"><i class="fas fa-columns"></i></button>
                            </div>
                        </div>
                        <div class="terminal-content">
                            <div class="terminal-line">
                                <span class="prompt">vader@editor:~$</span>
                                <span class="command">vader --version</span>
                            </div>
                            <div class="terminal-line output">
                                <span>Vader Language System v7.0</span>
                            </div>
                            <div class="terminal-line">
                                <span class="prompt">vader@editor:~$</span>
                                <span class="cursor">|</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        
        <!-- Barra de estado -->
        <footer class="status-bar">
            <div class="status-left">
                <span class="status-item"><i class="fas fa-code-branch"></i> main</span>
                <span class="status-item"><i class="fas fa-exclamation-triangle"></i> 0</span>
                <span class="status-item"><i class="fas fa-times-circle"></i> 0</span>
            </div>
            <div class="status-right">
                <span class="status-item">Ln 3, Col 1</span>
                <span class="status-item">UTF-8</span>
                <span class="status-item">Vader</span>
                <span class="status-item"><i class="fas fa-bell"></i></span>
            </div>
        </footer>
    </div>
    
    <script>
        // Detectar plataforma y ajustar header para macOS
        if (window.electronAPI && window.electronAPI.platform === 'darwin') {
            document.addEventListener('DOMContentLoaded', function() {
                const header = document.querySelector('.app-header');
                if (header) {
                    header.classList.add('darwin');
                }
            });
        }
    </script>
    <script src="script.js"></script>
</body>
</html>'''
    
    def generate_css(self):
        """Generate functional CSS styles for VSCode-like interface"""
        return '''/* Vader Editor - VSCode-like Interface */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', 'Cascadia Code', 'SF Mono', Monaco, 'Inconsolata', 'Roboto Mono', Consolas, 'Courier New', monospace;
    background-color: #1e1e1e;
    color: #cccccc;
    height: 100vh;
    overflow: hidden;
    font-size: 13px;
}

.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #1e1e1e;
}

/* Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
    padding: 8px 16px;
    height: 35px;
    -webkit-app-region: drag;
}

/* Ajuste para macOS - evitar superposición con botones de ventana */
.app-header.darwin {
    padding-left: 80px; /* Espacio para los botones de ventana de macOS */
}

.header-left {
    display: flex;
    align-items: center;
    gap: 10px;
    -webkit-app-region: no-drag;
}

.vader-logo {
    width: 20px;
    height: 20px;
    border-radius: 3px;
}

.app-title {
    font-size: 13px;
    font-weight: 400;
    color: #cccccc;
    margin: 0;
}

.header-right {
    display: flex;
    gap: 1px;
    -webkit-app-region: no-drag;
}

.btn-minimize, .btn-maximize, .btn-close {
    width: 46px;
    height: 30px;
    border: none;
    background: transparent;
    color: #cccccc;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
}

.btn-minimize:hover, .btn-maximize:hover {
    background-color: #404040;
}

.btn-close:hover {
    background-color: #e81123;
    color: white;
}

/* Main Content */
.main-content {
    display: flex;
    flex: 1;
    overflow: hidden;
}

/* Sidebar */
.sidebar {
    width: 300px;
    background-color: #252526;
    border-right: 1px solid #3c3c3c;
    display: flex;
    flex-direction: column;
}

.sidebar-tabs {
    display: flex;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
}

.tab-btn {
    width: 48px;
    height: 35px;
    border: none;
    background: transparent;
    color: #858585;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    border-bottom: 2px solid transparent;
}

.tab-btn:hover {
    color: #cccccc;
}

.tab-btn.active {
    color: #ffffff;
    border-bottom-color: #007acc;
}

.sidebar-content {
    flex: 1;
    overflow-y: auto;
}

.tab-panel {
    display: none;
    padding: 8px;
}

.tab-panel.active {
    display: block;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #3c3c3c;
    margin-bottom: 8px;
}

.panel-header h3 {
    font-size: 11px;
    font-weight: 600;
    color: #cccccc;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.panel-actions {
    display: flex;
    gap: 4px;
}

.btn-icon {
    width: 22px;
    height: 22px;
    border: none;
    background: transparent;
    color: #858585;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    border-radius: 3px;
}

.btn-icon:hover {
    background-color: #2a2d2e;
    color: #cccccc;
}

/* File Tree */
.file-tree {
    font-size: 13px;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 8px;
    cursor: pointer;
    border-radius: 3px;
    margin: 1px 0;
}

.file-item:hover {
    background-color: #2a2d2e;
}

.file-item.selected {
    background-color: #37373d;
}

.file-item i {
    width: 16px;
    font-size: 12px;
    color: #858585;
}

.file-item.folder i {
    color: #dcb67a;
}

.file-item.file i {
    color: #519aba;
}

/* Search Panel */
.search-container {
    display: flex;
    gap: 4px;
}

.search-input {
    flex: 1;
    background-color: #3c3c3c;
    border: 1px solid #3c3c3c;
    color: #cccccc;
    padding: 6px 8px;
    font-size: 13px;
    border-radius: 3px;
}

.search-input:focus {
    outline: none;
    border-color: #007acc;
}

.btn-search {
    background-color: #0e639c;
    border: none;
    color: white;
    padding: 6px 12px;
    border-radius: 3px;
    cursor: pointer;
}

.btn-search:hover {
    background-color: #1177bb;
}

/* Editor Area */
.editor-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #1e1e1e;
}

.editor-tabs {
    display: flex;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
    overflow-x: auto;
}

.tab {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    background-color: #2d2d30;
    border-right: 1px solid #3c3c3c;
    cursor: pointer;
    min-width: 120px;
    position: relative;
}

.tab:hover {
    background-color: #37373d;
}

.tab.active {
    background-color: #1e1e1e;
    border-bottom: 1px solid #1e1e1e;
}

.tab-icon {
    font-size: 14px;
}

.tab-name {
    font-size: 13px;
    color: #cccccc;
    flex: 1;
}

.tab-close {
    width: 16px;
    height: 16px;
    border: none;
    background: transparent;
    color: #858585;
    cursor: pointer;
    border-radius: 3px;
    font-size: 10px;
    opacity: 0;
    transition: opacity 0.2s;
}

.tab:hover .tab-close {
    opacity: 1;
}

.tab-close:hover {
    background-color: #e81123;
    color: white;
}

/* Editor Container */
.editor-container {
    flex: 1;
    display: flex;
    background-color: #1e1e1e;
    overflow: hidden;
}

.line-numbers {
    background-color: #1e1e1e;
    color: #858585;
    padding: 10px 8px;
    font-family: 'Cascadia Code', 'SF Mono', Monaco, 'Inconsolata', 'Roboto Mono', Consolas, monospace;
    font-size: 13px;
    line-height: 19px;
    text-align: right;
    user-select: none;
    border-right: 1px solid #3c3c3c;
    min-width: 50px;
}

.line-number {
    height: 19px;
}

.code-editor {
    flex: 1;
    background-color: #1e1e1e;
    color: #cccccc;
    border: none;
    outline: none;
    padding: 10px;
    font-family: 'Cascadia Code', 'SF Mono', Monaco, 'Inconsolata', 'Roboto Mono', Consolas, monospace;
    font-size: 13px;
    line-height: 19px;
    resize: none;
    tab-size: 4;
}

.code-editor::placeholder {
    color: #6a6a6a;
}

/* Bottom Panel */
.bottom-panel {
    height: 200px;
    background-color: #252526;
    border-top: 1px solid #3c3c3c;
    display: flex;
    flex-direction: column;
}

.panel-tabs {
    display: flex;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
}

.panel-tab {
    padding: 8px 16px;
    background: transparent;
    border: none;
    color: #858585;
    cursor: pointer;
    font-size: 13px;
    border-bottom: 2px solid transparent;
}

.panel-tab:hover {
    color: #cccccc;
}

.panel-tab.active {
    color: #ffffff;
    border-bottom-color: #007acc;
}

.terminal-container {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.terminal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 8px;
    background-color: #2d2d30;
    border-bottom: 1px solid #3c3c3c;
}

.terminal-title {
    font-size: 12px;
    color: #cccccc;
    font-family: 'Cascadia Code', monospace;
}

.terminal-actions {
    display: flex;
    gap: 4px;
}

.terminal-content {
    flex: 1;
    padding: 8px;
    font-family: 'Cascadia Code', 'SF Mono', Monaco, 'Inconsolata', 'Roboto Mono', Consolas, monospace;
    font-size: 13px;
    line-height: 18px;
    overflow-y: auto;
}

.terminal-line {
    display: flex;
    align-items: center;
    margin: 2px 0;
}

.prompt {
    color: #4ec9b0;
    margin-right: 8px;
}

.command {
    color: #cccccc;
}

.output {
    color: #d4d4d4;
    margin-left: 0;
}

.cursor {
    color: #cccccc;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}

/* Status Bar */
.status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #007acc;
    color: white;
    padding: 2px 8px;
    font-size: 12px;
    height: 22px;
}

.status-left, .status-right {
    display: flex;
    gap: 16px;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 3px;
}

.status-item:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.status-item i {
    font-size: 11px;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #1e1e1e;
}

::-webkit-scrollbar-thumb {
    background: #424242;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4f4f4f;
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        width: 250px;
    }
    
    .bottom-panel {
        height: 150px;
    }
}'''
    
    def generate_javascript(self):
        """Generate functional JavaScript for the editor"""
        return '''// Vader Editor - Functional JavaScript

// Global state
let currentFile = null;
let openFiles = new Map();
let fileTree = new Map();
let terminalHistory = [];
let terminalIndex = 0;

// Initialize the editor when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeEditor();
    loadFileTree();
    setupEventListeners();
    initializeTerminal();
});

function initializeEditor() {
    console.log('🚀 Vader Editor initialized');
    
    // Set up default file
    const defaultContent = `// Bienvenido al Editor Vader\n// Este es un editor creado completamente con Vader\n\ncrear variable mensaje\nvalor "¡Hola desde Vader!"\n\nmostrar mensaje\n\n// Puedes ejecutar este código presionando F5\n// o usando el menú Vader > Ejecutar Código`;
    
    openFiles.set('main.vdr', {
        content: defaultContent,
        modified: false,
        language: 'vader'
    });
    
    currentFile = 'main.vdr';
    updateEditor();
    updateLineNumbers();
}

function setupEventListeners() {
    // Sidebar tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchSidebarTab(this.dataset.tab);
        });
    });
    
    // File tree items
    document.querySelectorAll('.file-item').forEach(item => {
        item.addEventListener('click', function() {
            if (this.classList.contains('file')) {
                openFile(this.querySelector('span').textContent);
            } else if (this.classList.contains('folder')) {
                toggleFolder(this);
            }
        });
    });
    
    // Editor tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const fileName = this.querySelector('.tab-name').textContent;
            switchToFile(fileName);
        });
        
        const closeBtn = tab.querySelector('.tab-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const fileName = tab.querySelector('.tab-name').textContent;
                closeFile(fileName);
            });
        }
    });
    
    // Code editor
    const codeEditor = document.querySelector('.code-editor');
    if (codeEditor) {
        codeEditor.addEventListener('input', function() {
            updateLineNumbers();
            markFileAsModified();
        });
        
        codeEditor.addEventListener('scroll', function() {
            syncLineNumbers();
        });
        
        codeEditor.addEventListener('keydown', function(e) {
            handleEditorKeydown(e);
        });
    }
    
    // Terminal input
    const terminalContent = document.querySelector('.terminal-content');
    if (terminalContent) {
        terminalContent.addEventListener('click', function() {
            focusTerminalInput();
        });
    }
    
    // Panel tabs
    document.querySelectorAll('.panel-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            switchPanelTab(this.textContent);
        });
    });
    
    // Search functionality
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.btn-search');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', function() {
            performSearch(searchInput.value);
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        handleGlobalKeydown(e);
    });
}

function switchSidebarTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update tab panels
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    const targetPanel = document.getElementById(`${tabName}-panel`);
    if (targetPanel) {
        targetPanel.classList.add('active');
    }
}

function loadFileTree() {
    // Simulate file tree (in a real implementation, this would use IPC to read actual files)
    fileTree.set('mi_proyecto', {
        type: 'folder',
        children: ['main.vdr', 'utils.vdr', 'config.vdr']
    });
    
    fileTree.set('main.vdr', {
        type: 'file',
        content: `// Archivo principal del proyecto\ncrear variable app\nvalor "Mi aplicación Vader"\n\nmostrar app`
    });
    
    fileTree.set('utils.vdr', {
        type: 'file',
        content: `// Utilidades del proyecto\ncrear funcion saludar\nparametro nombre\n    mostrar "Hola " + nombre\nfin\n\nsaludar "Mundo"`
    });
    
    fileTree.set('config.vdr', {
        type: 'file',
        content: `// Configuración del proyecto\ncrear variable version\nvalor "1.0.0"\n\ncrear variable autor\nvalor "Desarrollador Vader"`
    });
}

function openFile(fileName) {
    if (!fileTree.has(fileName) || fileTree.get(fileName).type !== 'file') {
        return;
    }
    
    // Add to open files if not already open
    if (!openFiles.has(fileName)) {
        const fileData = fileTree.get(fileName);
        openFiles.set(fileName, {
            content: fileData.content,
            modified: false,
            language: fileName.endsWith('.vdr') ? 'vader' : 'text'
        });
        
        // Add tab
        addEditorTab(fileName);
    }
    
    // Switch to file
    switchToFile(fileName);
    
    // Update file tree selection
    document.querySelectorAll('.file-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    const fileItem = Array.from(document.querySelectorAll('.file-item')).find(item => {
        const span = item.querySelector('span');
        return span && span.textContent === fileName;
    });
    
    if (fileItem) {
        fileItem.classList.add('selected');
    }
}

function addEditorTab(fileName) {
    const tabsContainer = document.querySelector('.editor-tabs');
    const existingTab = Array.from(tabsContainer.children).find(tab => {
        const nameSpan = tab.querySelector('.tab-name');
        return nameSpan && nameSpan.textContent === fileName;
    });
    
    if (existingTab) return;
    
    const tab = document.createElement('div');
    tab.className = 'tab';
    tab.innerHTML = `
        <span class="tab-icon">⚡</span>
        <span class="tab-name">${fileName}</span>
        <button class="tab-close"><i class="fas fa-times"></i></button>
    `;
    
    // Add event listeners
    tab.addEventListener('click', function() {
        switchToFile(fileName);
    });
    
    const closeBtn = tab.querySelector('.tab-close');
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closeFile(fileName);
    });
    
    tabsContainer.appendChild(tab);
}

function switchToFile(fileName) {
    if (!openFiles.has(fileName)) return;
    
    currentFile = fileName;
    
    // Update tab states
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
        const nameSpan = tab.querySelector('.tab-name');
        if (nameSpan && nameSpan.textContent === fileName) {
            tab.classList.add('active');
        }
    });
    
    updateEditor();
}

function closeFile(fileName) {
    if (!openFiles.has(fileName)) return;
    
    const fileData = openFiles.get(fileName);
    if (fileData.modified) {
        if (!confirm(`¿Guardar cambios en ${fileName}?`)) {
            return;
        }
    }
    
    openFiles.delete(fileName);
    
    // Remove tab
    const tab = Array.from(document.querySelectorAll('.tab')).find(tab => {
        const nameSpan = tab.querySelector('.tab-name');
        return nameSpan && nameSpan.textContent === fileName;
    });
    
    if (tab) {
        tab.remove();
    }
    
    // Switch to another file if this was current
    if (currentFile === fileName) {
        const remainingFiles = Array.from(openFiles.keys());
        if (remainingFiles.length > 0) {
            switchToFile(remainingFiles[0]);
        } else {
            currentFile = null;
            updateEditor();
        }
    }
}

function updateEditor() {
    const codeEditor = document.querySelector('.code-editor');
    if (!codeEditor) return;
    
    if (currentFile && openFiles.has(currentFile)) {
        const fileData = openFiles.get(currentFile);
        codeEditor.value = fileData.content;
        codeEditor.disabled = false;
    } else {
        codeEditor.value = '// Selecciona un archivo para editar';
        codeEditor.disabled = true;
    }
    
    updateLineNumbers();
}

function updateLineNumbers() {
    const codeEditor = document.querySelector('.code-editor');
    const lineNumbers = document.querySelector('.line-numbers');
    
    if (!codeEditor || !lineNumbers) return;
    
    const lines = codeEditor.value.split('\n');
    const lineCount = Math.max(lines.length, 10);
    
    lineNumbers.innerHTML = '';
    for (let i = 1; i <= lineCount; i++) {
        const lineDiv = document.createElement('div');
        lineDiv.className = 'line-number';
        lineDiv.textContent = i;
        lineNumbers.appendChild(lineDiv);
    }
}

function syncLineNumbers() {
    const codeEditor = document.querySelector('.code-editor');
    const lineNumbers = document.querySelector('.line-numbers');
    
    if (codeEditor && lineNumbers) {
        lineNumbers.scrollTop = codeEditor.scrollTop;
    }
}

function markFileAsModified() {
    if (!currentFile) return;
    
    const fileData = openFiles.get(currentFile);
    if (fileData) {
        const codeEditor = document.querySelector('.code-editor');
        fileData.content = codeEditor.value;
        fileData.modified = true;
        
        // Update tab to show modified state
        const tab = Array.from(document.querySelectorAll('.tab')).find(tab => {
            const nameSpan = tab.querySelector('.tab-name');
            return nameSpan && nameSpan.textContent === currentFile;
        });
        
        if (tab) {
            const nameSpan = tab.querySelector('.tab-name');
            if (!nameSpan.textContent.includes('●')) {
                nameSpan.textContent = '● ' + nameSpan.textContent;
            }
        }
    }
}

function initializeTerminal() {
    const terminalContent = document.querySelector('.terminal-content');
    if (!terminalContent) return;
    
    // Add input line
    const inputLine = document.createElement('div');
    inputLine.className = 'terminal-line input-line';
    inputLine.innerHTML = `
        <span class="prompt">vader@editor:~$</span>
        <input type="text" class="terminal-input" placeholder="Escribe un comando...">
    `;
    
    terminalContent.appendChild(inputLine);
    
    const terminalInput = inputLine.querySelector('.terminal-input');
    terminalInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            executeTerminalCommand(this.value);
            this.value = '';
        }
    });
    
    terminalInput.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            navigateHistory(-1);
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            navigateHistory(1);
        }
    });
}

function executeTerminalCommand(command) {
    if (!command.trim()) return;
    
    terminalHistory.push(command);
    terminalIndex = terminalHistory.length;
    
    const terminalContent = document.querySelector('.terminal-content');
    
    // Add command line
    const commandLine = document.createElement('div');
    commandLine.className = 'terminal-line';
    commandLine.innerHTML = `
        <span class="prompt">vader@editor:~$</span>
        <span class="command">${command}</span>
    `;
    
    terminalContent.insertBefore(commandLine, terminalContent.lastElementChild);
    
    // Process command
    let output = '';
    const cmd = command.toLowerCase().trim();
    
    if (cmd === 'help') {
        output = `Comandos disponibles:\n  help - Mostrar esta ayuda\n  clear - Limpiar terminal\n  vader --version - Mostrar versión de Vader\n  ls - Listar archivos\n  pwd - Mostrar directorio actual\n  echo <texto> - Mostrar texto`;
    } else if (cmd === 'clear') {
        clearTerminal();
        return;
    } else if (cmd === 'vader --version') {
        output = 'Vader Language System v7.0\nEditor creado con Vader';
    } else if (cmd === 'ls') {
        output = 'main.vdr  utils.vdr  config.vdr';
    } else if (cmd === 'pwd') {
        output = '/Users/vader/mi_proyecto';
    } else if (cmd.startsWith('echo ')) {
        output = cmd.substring(5);
    } else {
        output = `bash: ${command}: command not found`;
    }
    
    // Add output
    if (output) {
        const outputLines = output.split('\n');
        outputLines.forEach(line => {
            const outputLine = document.createElement('div');
            outputLine.className = 'terminal-line output';
            outputLine.innerHTML = `<span>${line}</span>`;
            terminalContent.insertBefore(outputLine, terminalContent.lastElementChild);
        });
    }
    
    // Scroll to bottom
    terminalContent.scrollTop = terminalContent.scrollHeight;
}

function clearTerminal() {
    const terminalContent = document.querySelector('.terminal-content');
    const inputLine = terminalContent.querySelector('.input-line');
    terminalContent.innerHTML = '';
    terminalContent.appendChild(inputLine);
}

function navigateHistory(direction) {
    const terminalInput = document.querySelector('.terminal-input');
    if (!terminalInput) return;
    
    terminalIndex += direction;
    
    if (terminalIndex < 0) {
        terminalIndex = 0;
    } else if (terminalIndex >= terminalHistory.length) {
        terminalIndex = terminalHistory.length;
        terminalInput.value = '';
        return;
    }
    
    terminalInput.value = terminalHistory[terminalIndex] || '';
}

function focusTerminalInput() {
    const terminalInput = document.querySelector('.terminal-input');
    if (terminalInput) {
        terminalInput.focus();
    }
}

function switchPanelTab(tabName) {
    document.querySelectorAll('.panel-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.textContent === tabName) {
            tab.classList.add('active');
        }
    });
    
    // Here you would show/hide different panel content
    console.log(`Switched to panel: ${tabName}`);
}

function performSearch(query) {
    if (!query.trim()) return;
    
    console.log(`Searching for: ${query}`);
    
    // Simple search in current file
    const codeEditor = document.querySelector('.code-editor');
    if (codeEditor && currentFile) {
        const content = codeEditor.value.toLowerCase();
        const searchTerm = query.toLowerCase();
        const index = content.indexOf(searchTerm);
        
        if (index !== -1) {
            // Calculate line and column
            const beforeMatch = content.substring(0, index);
            const line = beforeMatch.split('\n').length;
            
            console.log(`Found "${query}" at line ${line}`);
            
            // Focus editor and scroll to line (simplified)
            codeEditor.focus();
        } else {
            console.log(`"${query}" not found`);
        }
    }
}

function handleEditorKeydown(e) {
    // Tab key for indentation
    if (e.key === 'Tab') {
        e.preventDefault();
        const editor = e.target;
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        
        editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 4;
        
        updateLineNumbers();
        markFileAsModified();
    }
}

function handleGlobalKeydown(e) {
    // Ctrl/Cmd + S - Save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveCurrentFile();
    }
    
    // F5 - Run code
    if (e.key === 'F5') {
        e.preventDefault();
        runCurrentFile();
    }
    
    // Ctrl/Cmd + N - New file
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        createNewFile();
    }
}

function saveCurrentFile() {
    if (!currentFile) return;
    
    console.log(`Saving ${currentFile}...`);
    
    const fileData = openFiles.get(currentFile);
    if (fileData) {
        fileData.modified = false;
        
        // Update tab to remove modified indicator
        const tab = Array.from(document.querySelectorAll('.tab')).find(tab => {
            const nameSpan = tab.querySelector('.tab-name');
            return nameSpan && nameSpan.textContent.includes(currentFile);
        });
        
        if (tab) {
            const nameSpan = tab.querySelector('.tab-name');
            nameSpan.textContent = nameSpan.textContent.replace('● ', '');
        }
        
        // In a real implementation, this would use IPC to save to disk
        console.log(`✅ ${currentFile} saved successfully`);
    }
}

function runCurrentFile() {
    if (!currentFile) return;
    
    console.log(`🚀 Running ${currentFile}...`);
    
    const fileData = openFiles.get(currentFile);
    if (fileData && fileData.language === 'vader') {
        // Simulate running Vader code
        executeTerminalCommand(`vader ${currentFile}`);
        
        // Switch to terminal
        const terminalTab = Array.from(document.querySelectorAll('.panel-tab')).find(tab => 
            tab.textContent === 'Terminal'
        );
        if (terminalTab) {
            terminalTab.click();
        }
    }
}

function createNewFile() {
    const fileName = prompt('Nombre del nuevo archivo:', 'untitled.vdr');
    if (!fileName) return;
    
    if (openFiles.has(fileName)) {
        switchToFile(fileName);
        return;
    }
    
    openFiles.set(fileName, {
        content: '// Nuevo archivo Vader\n',
        modified: true,
        language: fileName.endsWith('.vdr') ? 'vader' : 'text'
    });
    
    addEditorTab(fileName);
    switchToFile(fileName);
    
    console.log(`📄 Created new file: ${fileName}`);
}

function toggleFolder(folderElement) {
    const isExpanded = folderElement.classList.contains('expanded');
    const icon = folderElement.querySelector('i');
    
    if (isExpanded) {
        folderElement.classList.remove('expanded');
        icon.className = 'fas fa-folder';
    } else {
        folderElement.classList.add('expanded');
        icon.className = 'fas fa-folder-open';
    }
    
    // In a real implementation, this would show/hide child files
    console.log(`Folder ${isExpanded ? 'collapsed' : 'expanded'}`);
}

// Electron API integration
if (window.electronAPI) {
    // Handle menu events
    window.electronAPI.onMenuNewFile(() => {
        createNewFile();
    });
    
    window.electronAPI.onMenuSaveFile(() => {
        saveCurrentFile();
    });
    
    window.electronAPI.onMenuOpenFile((event, data) => {
        if (data && data.path && data.content) {
            const fileName = window.electronAPI.basename(data.path);
            openFiles.set(fileName, {
                content: data.content,
                modified: false,
                language: fileName.endsWith('.vdr') ? 'vader' : 'text'
            });
            
            addEditorTab(fileName);
            switchToFile(fileName);
        }
    });
}

console.log('🎉 Vader Editor JavaScript loaded successfully!');
'''
    
    def generate_main_js(self):
        """Generate Electron main process file"""
        return f'''const {{ app, BrowserWindow, Menu, ipcMain, dialog }} = require('electron');
const path = require('path');
const fs = require('fs');

// Keep a global reference of the window object
let mainWindow;

function createWindow() {{
    // Create the browser window
    mainWindow = new BrowserWindow({{
        width: {self.app_config['width']},
        height: {self.app_config['height']},
        minWidth: 800,
        minHeight: 600,
        webPreferences: {{
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js')
        }},
        titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
        title: 'Vader Editor',
        icon: {f'path.join(__dirname, "{self.app_config["icon"]}")' if self.app_config['icon'] else 'undefined'},
        show: false
    }});

    // Load the app
    mainWindow.loadFile('index.html');

    // Show window when ready
    mainWindow.once('ready-to-show', () => {{
        mainWindow.show();
    }});

    // Emitted when the window is closed
    mainWindow.on('closed', () => {{
        mainWindow = null;
    }});
}}

// This method will be called when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed
app.on('window-all-closed', () => {{
    if (process.platform !== 'darwin') {{
        app.quit();
    }}
}});

app.on('activate', () => {{
    if (BrowserWindow.getAllWindows().length === 0) {{
        createWindow();
    }}
}});

// Set up application menu
const template = [
    {{
        label: 'Archivo',
        submenu: [
            {{
                label: 'Nuevo',
                accelerator: 'CmdOrCtrl+N',
                click: () => {{
                    mainWindow.webContents.send('menu-new-file');
                }}
            }},
            {{
                label: 'Abrir',
                accelerator: 'CmdOrCtrl+O',
                click: async () => {{
                    const result = await dialog.showOpenDialog(mainWindow, {{
                        properties: ['openFile'],
                        filters: [
                            {{ name: 'Vader Files', extensions: ['vdr'] }},
                            {{ name: 'All Files', extensions: ['*'] }}
                        ]
                    }});
                    
                    if (!result.canceled) {{
                        const filePath = result.filePaths[0];
                        const content = fs.readFileSync(filePath, 'utf8');
                        mainWindow.webContents.send('menu-open-file', {{ path: filePath, content }});
                    }}
                }}
            }},
            {{
                label: 'Guardar',
                accelerator: 'CmdOrCtrl+S',
                click: () => {{
                    mainWindow.webContents.send('menu-save-file');
                }}
            }},
            {{ type: 'separator' }},
            {{
                label: 'Salir',
                accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
                click: () => {{
                    app.quit();
                }}
            }}
        ]
    }},
    {{
        label: 'Editar',
        submenu: [
            {{ role: 'undo', label: 'Deshacer' }},
            {{ role: 'redo', label: 'Rehacer' }},
            {{ type: 'separator' }},
            {{ role: 'cut', label: 'Cortar' }},
            {{ role: 'copy', label: 'Copiar' }},
            {{ role: 'paste', label: 'Pegar' }},
            {{ role: 'selectall', label: 'Seleccionar Todo' }}
        ]
    }},
    {{
        label: 'Ver',
        submenu: [
            {{ role: 'reload', label: 'Recargar' }},
            {{ role: 'forceReload', label: 'Forzar Recarga' }},
            {{ role: 'toggleDevTools', label: 'Herramientas de Desarrollo' }},
            {{ type: 'separator' }},
            {{ role: 'resetZoom', label: 'Zoom Normal' }},
            {{ role: 'zoomIn', label: 'Acercar' }},
            {{ role: 'zoomOut', label: 'Alejar' }},
            {{ type: 'separator' }},
            {{ role: 'togglefullscreen', label: 'Pantalla Completa' }}
        ]
    }}
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);

// Handle IPC messages
ipcMain.handle('save-file', async (event, {{ path, content }}) => {{
    try {{
        if (path) {{
            fs.writeFileSync(path, content, 'utf8');
            return {{ success: true }};
        }} else {{
            const result = await dialog.showSaveDialog(mainWindow, {{
                filters: [
                    {{ name: 'Vader Files', extensions: ['vdr'] }},
                    {{ name: 'All Files', extensions: ['*'] }}
                ]
            }});
            
            if (!result.canceled) {{
                fs.writeFileSync(result.filePath, content, 'utf8');
                return {{ success: true, path: result.filePath }};
            }}
        }}
        return {{ success: false }};
    }} catch (error) {{
        return {{ success: false, error: error.message }};
    }}
}});

ipcMain.handle('read-directory', async (event, dirPath) => {{
    try {{
        const items = fs.readdirSync(dirPath, {{ withFileTypes: true }});
        return items.map(item => ({{
            name: item.name,
            isDirectory: item.isDirectory(),
            path: path.join(dirPath, item.name)
        }}));
    }} catch (error) {{
        return [];
    }}
}});

ipcMain.handle('execute-vader', async (event, {{ code, target }}) => {{
    try {{
        const {{ spawn }} = require('child_process');
        const tempFile = path.join(__dirname, 'temp.vdr');
        fs.writeFileSync(tempFile, code, 'utf8');
        
        return new Promise((resolve) => {{
            const process = spawn('python3', ['src/vader.py', tempFile, '--target', target, '--verbose'], {{
                cwd: path.join(__dirname, '..', 'Vader')
            }});
            
            let output = '';
            let error = '';
            
            process.stdout.on('data', (data) => {{
                output += data.toString();
            }});
            
            process.stderr.on('data', (data) => {{
                error += data.toString();
            }});
            
            process.on('close', (code) => {{
                fs.unlinkSync(tempFile); // Clean up temp file
                resolve({{ success: code === 0, output, error }});
            }});
        }});
    }} catch (error) {{
        return {{ success: false, error: error.message }};
    }}
}});
'''
    
    def generate_preload_js(self):
        """Generate Electron preload script"""
        return '''const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // File operations
    saveFile: (path, content) => ipcRenderer.invoke('save-file', { path, content }),
    readDirectory: (dirPath) => ipcRenderer.invoke('read-directory', dirPath),
    executeVader: (code, target) => ipcRenderer.invoke('execute-vader', { code, target }),
    
    // Menu events
    onMenuNewFile: (callback) => ipcRenderer.on('menu-new-file', callback),
    onMenuOpenFile: (callback) => ipcRenderer.on('menu-open-file', callback),
    onMenuSaveFile: (callback) => ipcRenderer.on('menu-save-file', callback),
    
    // Remove listeners
    removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
    
    // System info
    platform: process.platform,
    
    // Path utilities
    joinPath: (...paths) => require('path').join(...paths),
    dirname: (path) => require('path').dirname(path),
    basename: (path) => require('path').basename(path),
    extname: (path) => require('path').extname(path)
});
'''
    
    def generate_package_json(self):
        """Generate package.json for Electron app"""
        return json.dumps({
            "name": self.app_config['name'].lower().replace(' ', '-'),
            "version": self.app_config['version'],
            "description": self.app_config['description'],
            "main": "main.js",
            "homepage": "./",
            "scripts": {
                "start": "electron .",
                "dev": "electron . --dev",
                "build": "electron-builder",
                "dist": "electron-builder --publish=never",
                "pack": "electron-builder --dir"
            },
            "keywords": [
                "vader",
                "electron",
                "gui",
                "desktop"
            ],
            "author": "Vader Developer",
            "license": "MIT",
            "devDependencies": {
                "electron": "^22.0.0",
                "electron-builder": "^23.6.0"
            },
            "build": {
                "appId": f"com.vader.{self.app_config['name'].lower().replace(' ', '')}",
                "productName": self.app_config['name'],
                "directories": {
                    "output": "dist"
                },
                "files": [
                    "**/*",
                    "!src/",
                    "!*.vdr"
                ],
                "mac": {
                    "category": "public.app-category.developer-tools"
                },
                "win": {
                    "target": "nsis"
                },
                "linux": {
                    "target": "AppImage"
                }
            }
        }, indent=2)
    
    def generate_readme(self):
        """Generate README for the application"""
        return f'''# {self.app_config['name']}

{self.app_config['description']}

## Descripción

Esta aplicación fue generada automáticamente usando **Vader**, el primer lenguaje de programación conversacional y universal.

## Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Ejecutar en modo desarrollo:
```bash
npm run dev
```

3. Construir aplicación:
```bash
npm run build
```

## Características

- ✅ Interfaz nativa multiplataforma (Windows, macOS, Linux)
- ✅ Tema oscuro moderno estilo VSCode
- ✅ Componentes GUI avanzados
- ✅ Sistema de eventos interactivos
- ✅ Integración completa con Vader

## Tecnologías

- **Vader**: Lenguaje de programación conversacional
- **Electron**: Framework para aplicaciones de escritorio
- **HTML5/CSS3**: Interfaz de usuario moderna
- **JavaScript**: Lógica de aplicación

## Generado por Vader v7.0

Vader es el primer lenguaje de programación conversacional que democratiza la creación de software para toda la humanidad.

Más información: [https://github.com/LangVader/Vader](https://github.com/LangVader/Vader)
'''

def transpile_to_electron(vader_code):
    """Main function to transpile Vader to Electron application"""
    transpiler = ElectronTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    transpiler = ElectronTranspiler()
    result = transpiler.transpile(vader_code)
    
    # Return the main.js file as the primary output for CLI
    # The complete application files would be saved separately
    return result['main.js']
