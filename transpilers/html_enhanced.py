# Enhanced functions for HTML Transpiler - Professional CSS and JavaScript
# These functions complete the improved Vader HTML transpiler

def generate_professional_styles():
    """Generate professional CSS styles for VaderUI"""
    return '''
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        background: #000;
        color: #fff;
        overflow-x: hidden;
    }
    
    .header-profesional {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #333;
    }
    
    .navegacion-principal {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .logo-vader {
        font-size: 1.5rem;
        color: #10b981;
    }
    
    .logo-texto {
        font-size: 1.25rem;
        font-weight: bold;
        color: #fff;
    }
    
    .menu-navegacion {
        display: flex;
        gap: 2rem;
    }
    
    .nav-link {
        color: #ccc;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
        position: relative;
    }
    
    .nav-link:hover {
        color: #10b981;
    }
    
    .badge-nuevo {
        background: #10b981;
        color: #000;
        padding: 0.125rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    
    .acciones-header {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .btn-tema {
        background: none;
        border: 1px solid #333;
        color: #fff;
        padding: 0.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-tema:hover {
        border-color: #10b981;
    }
    
    .btn-github {
        background: #333;
        border: none;
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-cta {
        background: #10b981;
        border: none;
        color: #000;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-cta:hover {
        background: #059669;
    }
    
    .hero-section {
        padding: 8rem 2rem 4rem;
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
    
    .hero-container {
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }
    
    .hero-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        align-items: center;
    }
    
    .hero-titulo {
        font-size: 3.5rem;
        font-weight: bold;
        line-height: 1.1;
        margin-bottom: 1.5rem;
    }
    
    .texto-gradiente {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-descripcion {
        font-size: 1.25rem;
        color: #ccc;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .highlight {
        color: #10b981;
        font-weight: 600;
    }
    
    .hero-badges {
        margin-bottom: 2rem;
    }
    
    .badge-update {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        color: #10b981;
    }
    
    .badge-nuevo-mini {
        background: #10b981;
        color: #000;
        padding: 0.125rem 0.375rem;
        border-radius: 0.75rem;
        font-size: 0.625rem;
        font-weight: bold;
    }
    
    .hero-acciones {
        display: flex;
        gap: 1rem;
    }
    
    .btn-principal {
        background: #10b981;
        border: none;
        color: #000;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .btn-principal:hover {
        background: #059669;
        transform: translateY(-2px);
    }
    
    .btn-secundario {
        background: transparent;
        border: 1px solid #333;
        color: #fff;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .btn-secundario:hover {
        border-color: #10b981;
        color: #10b981;
    }
    
    .showcase-container {
        display: flex;
        gap: 1rem;
        height: 500px;
    }
    
    .card-showcase {
        flex: 2;
        background: #111;
        border: 1px solid #333;
        border-radius: 1rem;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .card-tag {
        color: #666;
        font-size: 0.875rem;
    }
    
    .card-image {
        flex: 1;
        margin-bottom: 1rem;
    }
    
    .imagen-placeholder {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #ec4899, #3b82f6);
        border-radius: 0.75rem;
        position: relative;
        overflow: hidden;
    }
    
    .gradiente-visual {
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.8), rgba(59, 130, 246, 0.8));
    }
    
    .contenido-visual {
        position: absolute;
        bottom: 1.5rem;
        left: 1.5rem;
        right: 1.5rem;
        color: white;
    }
    
    .contenido-visual h3 {
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .contenido-visual p {
        opacity: 0.9;
        font-size: 0.875rem;
    }
    
    .card-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .btn-card-action {
        flex: 1;
        background: #333;
        border: none;
        color: #fff;
        padding: 0.75rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .btn-card-share {
        background: transparent;
        border: 1px solid #333;
        color: #fff;
        padding: 0.75rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .sidebar-components {
        flex: 1;
        background: #111;
        border: 1px solid #333;
        border-radius: 1rem;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
    }
    
    .sidebar-header h4 {
        color: #fff;
        margin-bottom: 1.5rem;
        font-size: 1.125rem;
    }
    
    .user-profile {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .avatar {
        width: 3rem;
        height: 3rem;
        background: #333;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .user-info {
        flex: 1;
    }
    
    .user-name {
        font-weight: bold;
        color: #fff;
        margin-bottom: 0.25rem;
    }
    
    .user-role {
        color: #666;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .user-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.75rem;
        color: #10b981;
    }
    
    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        background: #10b981;
        border-radius: 50%;
    }
    
    .skills-section {
        margin-bottom: 2rem;
    }
    
    .skill-item {
        margin-bottom: 1rem;
    }
    
    .skill-label {
        display: block;
        color: #ccc;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .skill-bar {
        background: #333;
        height: 0.5rem;
        border-radius: 0.25rem;
        overflow: hidden;
    }
    
    .skill-progress {
        background: #10b981;
        height: 100%;
        transition: width 0.3s;
    }
    
    .sidebar-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: auto;
    }
    
    .btn-portfolio {
        flex: 1;
        background: #333;
        border: none;
        color: #fff;
        padding: 0.75rem;
        border-radius: 0.5rem;
        cursor: pointer;
        font-size: 0.875rem;
    }
    
    .btn-share-mini {
        background: transparent;
        border: 1px solid #333;
        color: #fff;
        padding: 0.75rem;
        border-radius: 0.5rem;
        cursor: pointer;
    }
    
    .features-section {
        padding: 4rem 2rem;
        background: #111;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .feature-item {
        text-align: center;
        padding: 2rem;
        background: #222;
        border-radius: 1rem;
        border: 1px solid #333;
    }
    
    .feature-icono {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-item h3 {
        color: #fff;
        margin-bottom: 1rem;
        font-size: 1.25rem;
    }
    
    .feature-item p {
        color: #ccc;
        line-height: 1.6;
    }
    
    @media (max-width: 768px) {
        .hero-content {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        .hero-titulo {
            font-size: 2.5rem;
        }
        
        .showcase-container {
            flex-direction: column;
            height: auto;
        }
        
        .menu-navegacion {
            display: none;
        }
    }
    '''

def generate_interactive_scripts():
    """Generate interactive JavaScript for VaderUI"""
    return '''
    function cambiarTema() {
        const body = document.body;
        const temaActual = body.classList.contains('tema-oscuro') ? 'oscuro' : 'claro';
        const nuevoTema = temaActual === 'oscuro' ? 'claro' : 'oscuro';
        
        body.className = 'tema-' + nuevoTema;
        
        const btnTema = document.querySelector('.btn-tema');
        btnTema.textContent = nuevoTema === 'oscuro' ? '🌙' : '☀️';
    }
    
    function explorarComponentes() {
        alert('Navegando a la galería de componentes...');
    }
    
    function verTemplates() {
        alert('Navegando a los templates...');
    }
    
    // Animaciones de entrada
    document.addEventListener('DOMContentLoaded', function() {
        const elementos = document.querySelectorAll('.hero-titulo, .hero-descripcion, .card-showcase, .sidebar-components');
        
        elementos.forEach((elemento, index) => {
            elemento.style.opacity = '0';
            elemento.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                elemento.style.transition = 'all 0.6s ease';
                elemento.style.opacity = '1';
                elemento.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });
    '''
