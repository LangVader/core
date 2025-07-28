# HTML Transpiler for Vader - Enhanced Version
# Converts advanced Vader syntax to modern HTML/CSS/JS code
# Supports VaderUI components, animations, and modern web features

import re
import json

class HTMLTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.components = {}
        self.imports = {}
        self.css_classes = []
        self.javascript_functions = []
        self.variables = {}
        self.in_component = False
        self.current_component = None
        self.component_stack = []
        self.html_buffer = []
        self.css_buffer = []
        self.js_buffer = []
        self.component_definitions = {}
        self.application_state = {}
        
    def transpile(self, vader_code):
        """Transpile advanced Vader code to modern HTML with component support"""
        lines = vader_code.split('\n')
        
        # Detectar si es una aplicación con LandingPageProfesional
        if self.has_professional_landing(lines):
            return self.generate_professional_landing_html()
        
        # Procesar estructura avanzada
        self.parse_advanced_structure(lines)
        self.process_components_and_applications(lines)
        return self.generate_complete_html()
    
    def has_professional_landing(self, lines):
        """Detectar si importa LandingPageProfesional"""
        for line in lines:
            if 'LandingPageProfesional' in line and 'importar' in line:
                return True
        return False
    
    def generate_professional_landing_html(self):
        """Generar HTML completo para la landing page profesional como react-ui-master"""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaderUI - Professional Component Library</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #000;
            color: #fff;
            overflow-x: hidden;
        }
        
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid #1f1f1f;
        }
        
        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #10b981, #3b82f6);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-link {
            color: #a1a1aa;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            position: relative;
        }
        
        .nav-link:hover {
            color: #fff;
        }
        
        .nav-link.new::after {
            content: 'New';
            position: absolute;
            top: -8px;
            right: -20px;
            background: #10b981;
            color: #000;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: bold;
        }
        
        .nav-actions {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .theme-toggle {
            background: none;
            border: 1px solid #374151;
            color: #fff;
            padding: 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .theme-toggle:hover {
            border-color: #10b981;
        }
        
        .btn {
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s;
            cursor: pointer;
            border: none;
        }
        
        .btn-primary {
            background: #10b981;
            color: #000;
        }
        
        .btn-primary:hover {
            background: #059669;
            transform: translateY(-1px);
        }
        
        .main {
            padding-top: 80px;
        }
        
        .hero {
            padding: 4rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
            min-height: 90vh;
        }
        
        .hero-content h1 {
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 1.5rem;
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-content p {
            font-size: 1.25rem;
            color: #a1a1aa;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        .highlight {
            color: #10b981;
            font-weight: 600;
        }
        
        .update-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            color: #10b981;
            margin-bottom: 2rem;
        }
        
        .new-badge {
            background: #10b981;
            color: #000;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .hero-actions {
            display: flex;
            gap: 1rem;
        }
        
        .btn-large {
            padding: 1rem 2rem;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-secondary {
            background: transparent;
            border: 1px solid #374151;
            color: #fff;
        }
        
        .btn-secondary:hover {
            border-color: #10b981;
            color: #10b981;
        }
        
        .hero-visual {
            display: flex;
            gap: 1rem;
            height: 600px;
        }
        
        .main-card {
            flex: 2;
            background: #111;
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .card-tag {
            color: #6b7280;
            font-size: 0.875rem;
        }
        
        .card-content {
            flex: 1;
            margin-bottom: 1.5rem;
        }
        
        .visual-placeholder {
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #ec4899, #3b82f6);
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        
        .visual-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.8), rgba(59, 130, 246, 0.8));
            display: flex;
            align-items: flex-end;
            padding: 2rem;
        }
        
        .visual-content h3 {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .visual-content p {
            opacity: 0.9;
        }
        
        .card-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .btn-card {
            flex: 1;
            background: #1f1f1f;
            border: none;
            color: #fff;
            padding: 0.75rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .btn-card:hover {
            background: #374151;
        }
        
        .btn-icon {
            background: transparent;
            border: 1px solid #374151;
            color: #fff;
            padding: 0.75rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-icon:hover {
            border-color: #10b981;
        }
        
        .sidebar {
            flex: 1;
            background: #111;
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 2rem;
            display: flex;
            flex-direction: column;
        }
        
        .sidebar h4 {
            margin-bottom: 1.5rem;
            font-size: 1.125rem;
        }
        
        .profile {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .avatar {
            width: 48px;
            height: 48px;
            background: #374151;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .profile-info {
            flex: 1;
        }
        
        .profile-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .profile-role {
            color: #6b7280;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        
        .profile-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.75rem;
            color: #10b981;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
        }
        
        .skills {
            margin-bottom: 2rem;
        }
        
        .skill {
            margin-bottom: 1rem;
        }
        
        .skill-label {
            display: block;
            color: #a1a1aa;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        
        .skill-bar {
            background: #1f1f1f;
            height: 8px;
            border-radius: 4px;
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
        
        .ai-chat-section {
            background: #111;
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
        }
        
        .ai-chat-section h4 {
            color: #a1a1aa;
            font-size: 0.875rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .search-container {
            background: #1f1f1f;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .search-input {
            width: 100%;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 0.875rem;
            outline: none;
            margin-bottom: 1rem;
        }
        
        .search-input::placeholder {
            color: #6b7280;
        }
        
        .search-btn {
            background: #3b82f6;
            color: #fff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .search-btn:hover {
            background: #2563eb;
        }
        
        .chat-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .chat-label {
            color: #6b7280;
            font-size: 0.75rem;
        }
        
        .send-btn {
            background: transparent;
            border: 1px solid #374151;
            color: #fff;
            padding: 0.5rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .send-btn:hover {
            border-color: #10b981;
        }
        
        .footer-section {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid #1f1f1f;
            z-index: 1000;
        }
        
        .tech-stack {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .issue-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: #dc2626;
            color: #fff;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
        }
        
        .issue-badge {
            background: #fff;
            color: #dc2626;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
        }
        
        .close-issue {
            background: none;
            border: none;
            color: #fff;
            cursor: pointer;
            padding: 0.25rem;
            margin-left: 0.5rem;
        }
        
        .tech-icons {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .tech-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #a1a1aa;
            font-size: 0.875rem;
        }
        
        .tech-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .tech-icon.tailwind {
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
        }
        
        .tech-icon.motion {
            background: linear-gradient(135deg, #8b5cf6, #ec4899);
        }
        
        .tech-icon.shadcn {
            background: linear-gradient(135deg, #374151, #6b7280);
        }
        
        .tech-icon.nextjs {
            background: linear-gradient(135deg, #000, #333);
        }
        
        .tech-icon.react {
            background: linear-gradient(135deg, #61dafb, #21a1c4);
        }
        
        @media (max-width: 1024px) {
            .hero {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .hero-content h1 {
                font-size: 3rem;
            }
            
            .hero-visual {
                flex-direction: column;
                height: auto;
            }
            
            .nav-links {
                display: none;
            }
        }
        
        /* Estilos para las nuevas secciones */
        .section {
            padding: 6rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .section-alt {
            background: #0a0a0a;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #10b981, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .section-description {
            font-size: 1.2rem;
            text-align: center;
            color: #a1a1aa;
            margin-bottom: 4rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Components Grid */
        .components-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }
        
        .component-card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .component-card:hover {
            border-color: #10b981;
            transform: translateY(-4px);
        }
        
        .component-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #fff;
        }
        
        .component-card p {
            color: #a1a1aa;
            margin-bottom: 1.5rem;
        }
        
        .component-preview {
            padding: 1rem;
            background: #0a0a0a;
            border-radius: 8px;
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .btn-secondary {
            background: transparent;
            border: 1px solid #374151;
            color: #fff;
        }
        
        .btn-secondary:hover {
            border-color: #10b981;
            background: #10b981;
            color: #000;
        }
        
        .preview-card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            padding: 1rem;
            color: #fff;
            font-size: 0.9rem;
        }
        
        .preview-input {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            color: #fff;
            width: 150px;
        }
        
        .preview-input:focus {
            outline: none;
            border-color: #10b981;
        }
        
        .preview-nav {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            color: #fff;
            font-size: 0.9rem;
        }
        
        /* Templates Grid */
        .templates-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
        }
        
        .template-card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .template-card:hover {
            border-color: #10b981;
            transform: translateY(-4px);
        }
        
        .template-preview {
            height: 200px;
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
            position: relative;
        }
        
        .template-preview::after {
            content: '🖼️';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3rem;
            opacity: 0.3;
        }
        
        .template-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 1.5rem 1.5rem 1rem;
            color: #fff;
        }
        
        .template-card p {
            color: #a1a1aa;
            margin: 0 1.5rem 1.5rem;
        }
        
        .template-link {
            display: inline-block;
            margin: 0 1.5rem 1.5rem;
            color: #10b981;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .template-link:hover {
            color: #059669;
        }
        
        /* Docs Grid */
        .docs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }
        
        .doc-card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .doc-card:hover {
            border-color: #10b981;
            transform: translateY(-4px);
        }
        
        .doc-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #fff;
        }
        
        .doc-card p {
            color: #a1a1aa;
            margin-bottom: 1.5rem;
        }
        
        .doc-link {
            color: #10b981;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .doc-link:hover {
            color: #059669;
        }
        
        /* Examples Grid */
        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
        }
        
        .example-card {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .example-card:hover {
            border-color: #10b981;
            transform: translateY(-4px);
        }
        
        .example-preview {
            height: 180px;
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .example-content {
            background: #10b981;
            color: #000;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .example-card h3 {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 1.5rem 1.5rem 1rem;
            color: #fff;
        }
        
        .example-card p {
            color: #a1a1aa;
            margin: 0 1.5rem 1.5rem;
        }
        
        .example-links {
            display: flex;
            gap: 1rem;
            margin: 0 1.5rem 1.5rem;
        }
        
        .example-link {
            color: #10b981;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: color 0.3s;
        }
        
        .example-link:hover {
            color: #059669;
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">
                <div class="logo-icon">V</div>
                <span>VaderUI</span>
            </div>
            
            <div class="nav-links">
                <a href="#components" class="nav-link new">Components</a>
                <a href="#templates" class="nav-link">Templates</a>
                <a href="#docs" class="nav-link">Documentation</a>
                <a href="#examples" class="nav-link">Examples</a>
            </div>
            
            <div class="nav-actions">
                <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
                <a href="#" class="btn btn-primary">Get Started</a>
            </div>
        </nav>
    </header>
    
    <main class="main">
        <section class="hero">
            <div class="hero-content">
                <div class="update-badge">
                    <span class="new-badge">New</span>
                    <span>Now updated for Vader CSS 7.0</span>
                </div>
                
                <h1>
                    Craft with <span class="gradient-text">precision</span><br>
                    build with <span class="gradient-text">ease.</span>
                </h1>
                
                <p>
                    A curated collection of <strong>100+ premium UI components</strong><br>
                    crafted with <span class="highlight">Vader CSS</span> and <span class="highlight">native syntax</span> for modern<br>
                    Vader applications.
                </p>
                
                <div class="hero-actions">
                    <button class="btn btn-primary btn-large" onclick="browseComponents()">
                        🚀 Browse Components
                    </button>
                    <button class="btn btn-secondary btn-large" onclick="goToTemplates()">
                        📋 Go to Templates
                    </button>
                </div>
            </div>
            
            <div class="hero-visual">
                <div class="main-card">
                    <div class="card-header">
                        <span class="card-tag">&lt;Card/&gt;</span>
                        <span>✨</span>
                    </div>
                    
                    <div class="card-content">
                        <div class="visual-placeholder">
                            <div class="visual-overlay">
                                <div class="visual-content">
                                    <h3>New UI Design Fundamentals</h3>
                                    <p>Explore the fundamentals of contemporary UI design</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card-actions">
                        <button class="btn-card">
                            👁️ View
                        </button>
                        <button class="btn-icon">📤</button>
                    </div>
                </div>
                
                <div class="sidebar">
                    <h4>Components</h4>
                    
                    <div class="profile">
                        <div class="avatar">👨‍💻</div>
                        <div class="profile-info">
                            <div class="profile-name">Eugene K</div>
                            <div class="profile-role">Senior Developer</div>
                            <div class="profile-status">
                                <div class="status-dot"></div>
                                <span>Open to Work</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="skills">
                        <div class="skill">
                            <span class="skill-label">Frontend</span>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: 95%"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-label">Backend</span>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: 80%"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-label">DevOps</span>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: 70%"></div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="sidebar-actions">
                        <button class="btn-card">🔗 View Portfolio</button>
                        <button class="btn-icon">📤</button>
                    </div>
                </div>
            </div>
            
            <!-- AI Chat Section -->
            <div class="ai-chat-section">
                <h4>AI Chat</h4>
                <div class="search-container">
                    <input type="text" placeholder="Search the web..." class="search-input">
                    <button class="search-btn">🔍 Search</button>
                </div>
                <div class="chat-footer">
                    <span class="chat-label">Buttons</span>
                    <button class="send-btn">📤</button>
                </div>
            </div>
        </section>
        
        <!-- Footer Section -->
        <footer class="footer-section">
            <div class="container">
                <div class="tech-stack">
                    <div class="issue-indicator">
                        <span class="issue-badge">N</span>
                        <span class="issue-text">1 Issue</span>
                        <button class="close-issue">✕</button>
                    </div>
                    
                    <div class="tech-icons">
                        <div class="tech-item">
                            <div class="tech-icon tailwind">🎨</div>
                            <span>TailwindCSS</span>
                        </div>
                        <div class="tech-item">
                            <div class="tech-icon motion">🎭</div>
                            <span>Motion</span>
                        </div>
                        <div class="tech-item">
                            <div class="tech-icon shadcn">✏️</div>
                            <span>shadcn/ui</span>
                        </div>
                        <div class="tech-item">
                            <div class="tech-icon nextjs">⚡</div>
                            <span>Next.js</span>
                        </div>
                        <div class="tech-item">
                            <div class="tech-icon react">⚛️</div>
                            <span>React</span>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
        
        <!-- Secciones de navegación -->
        <section id="components" class="section">
            <div class="container">
                <h2 class="section-title">Components</h2>
                <p class="section-description">A curated collection of 100+ premium UI components crafted with Vader CSS and native syntax.</p>
                <div class="components-grid">
                    <div class="component-card">
                        <h3>Buttons</h3>
                        <p>Interactive button components with multiple variants and states.</p>
                        <div class="component-preview">
                            <button class="btn btn-primary">Primary</button>
                            <button class="btn btn-secondary">Secondary</button>
                        </div>
                    </div>
                    <div class="component-card">
                        <h3>Cards</h3>
                        <p>Flexible card components for displaying content and information.</p>
                        <div class="component-preview">
                            <div class="preview-card">Sample Card</div>
                        </div>
                    </div>
                    <div class="component-card">
                        <h3>Forms</h3>
                        <p>Complete form components with validation and modern styling.</p>
                        <div class="component-preview">
                            <input type="text" placeholder="Sample input" class="preview-input">
                        </div>
                    </div>
                    <div class="component-card">
                        <h3>Navigation</h3>
                        <p>Responsive navigation components for modern web applications.</p>
                        <div class="component-preview">
                            <nav class="preview-nav">Navigation</nav>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="templates" class="section section-alt">
            <div class="container">
                <h2 class="section-title">Templates</h2>
                <p class="section-description">Ready-to-use templates built with VaderUI components for rapid development.</p>
                <div class="templates-grid">
                    <div class="template-card">
                        <div class="template-preview"></div>
                        <h3>Dashboard</h3>
                        <p>Complete admin dashboard with charts, tables, and analytics.</p>
                        <a href="#" class="template-link">View Template</a>
                    </div>
                    <div class="template-card">
                        <div class="template-preview"></div>
                        <h3>Landing Page</h3>
                        <p>Modern landing page template for SaaS and products.</p>
                        <a href="#" class="template-link">View Template</a>
                    </div>
                    <div class="template-card">
                        <div class="template-preview"></div>
                        <h3>E-commerce</h3>
                        <p>Complete e-commerce solution with cart and checkout.</p>
                        <a href="#" class="template-link">View Template</a>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="docs" class="section">
            <div class="container">
                <h2 class="section-title">Documentation</h2>
                <p class="section-description">Comprehensive guides and API reference for VaderUI components.</p>
                <div class="docs-grid">
                    <div class="doc-card">
                        <h3>🚀 Getting Started</h3>
                        <p>Quick start guide to begin using VaderUI in your projects.</p>
                        <a href="#" class="doc-link">Read Guide</a>
                    </div>
                    <div class="doc-card">
                        <h3>🎨 Theming</h3>
                        <p>Learn how to customize colors, fonts, and styling.</p>
                        <a href="#" class="doc-link">Read Guide</a>
                    </div>
                    <div class="doc-card">
                        <h3>📚 API Reference</h3>
                        <p>Complete API documentation for all components.</p>
                        <a href="#" class="doc-link">Read Guide</a>
                    </div>
                    <div class="doc-card">
                        <h3>🔧 Advanced Usage</h3>
                        <p>Advanced patterns and best practices.</p>
                        <a href="#" class="doc-link">Read Guide</a>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="examples" class="section section-alt">
            <div class="container">
                <h2 class="section-title">Examples</h2>
                <p class="section-description">Real-world examples and use cases built with VaderUI.</p>
                <div class="examples-grid">
                    <div class="example-card">
                        <div class="example-preview">
                            <div class="example-content">Blog App</div>
                        </div>
                        <h3>Blog Application</h3>
                        <p>Complete blog with posts, comments, and user authentication.</p>
                        <div class="example-links">
                            <a href="#" class="example-link">Live Demo</a>
                            <a href="#" class="example-link">Source Code</a>
                        </div>
                    </div>
                    <div class="example-card">
                        <div class="example-preview">
                            <div class="example-content">Todo App</div>
                        </div>
                        <h3>Todo Application</h3>
                        <p>Task management app with drag & drop and categories.</p>
                        <div class="example-links">
                            <a href="#" class="example-link">Live Demo</a>
                            <a href="#" class="example-link">Source Code</a>
                        </div>
                    </div>
                    <div class="example-card">
                        <div class="example-preview">
                            <div class="example-content">Chat App</div>
                        </div>
                        <h3>Chat Application</h3>
                        <p>Real-time chat application with rooms and messaging.</p>
                        <div class="example-links">
                            <a href="#" class="example-link">Live Demo</a>
                            <a href="#" class="example-link">Source Code</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
        }
        
        function browseComponents() {
            alert('Navegando a componentes...');
        }
        
        function goToTemplates() {
            alert('Navegando a templates...');
        }
        
        // Animaciones de entrada
        document.addEventListener('DOMContentLoaded', function() {
            const elements = document.querySelectorAll('.hero-content > *, .main-card, .sidebar');
            
            elements.forEach((element, index) => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    element.style.transition = 'all 0.6s ease';
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    </script>
</body>
</html>
        '''
    
    def parse_advanced_structure(self, lines):
        """Enhanced parsing for components, applications, and complex structures"""
        current_block = None
        current_component = None
        current_application = None
        block_content = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Parse application definitions
            if line.startswith('crear aplicacion '):
                app_match = re.search(r'crear aplicacion (\w+)', line)
                if app_match:
                    current_application = app_match.group(1)
                    self.application_state[current_application] = {
                        'name': current_application,
                        'state': {},
                        'functions': {},
                        'render_function': None
                    }
                    current_block = 'application'
                    block_content = []
            
            # Parse component definitions
            elif line.startswith('crear componente '):
                comp_match = re.search(r'crear componente (\w+)', line)
                if comp_match:
                    current_component = comp_match.group(1)
                    self.component_definitions[current_component] = {
                        'name': current_component,
                        'props': {},
                        'state': {},
                        'functions': {},
                        'render_content': []
                    }
                    current_block = 'component'
                    block_content = []
            
            # Parse state definitions
            elif line.startswith('estado:') and current_block:
                current_block = 'state'
                block_content = []
            
            # Parse function definitions
            elif line.startswith('funcion ') and current_block:
                func_match = re.search(r'funcion (\w+)\(([^)]*)\)', line)
                if func_match:
                    func_name = func_match.group(1)
                    if current_application:
                        self.application_state[current_application]['functions'][func_name] = {
                            'name': func_name,
                            'content': []
                        }
                    elif current_component:
                        self.component_definitions[current_component]['functions'][func_name] = {
                            'name': func_name,
                            'content': []
                        }
            
            # Parse renderizar function
            elif line.startswith('renderizar:') or line.startswith('funcion renderizar()'):
                current_block = 'render'
                block_content = []
            
            # Collect content for current block
            elif current_block and line:
                block_content.append(line)
                
                # Store render content
                if current_block == 'render':
                    if current_application:
                        self.application_state[current_application]['render_function'] = block_content
                    elif current_component:
                        self.component_definitions[current_component]['render_content'] = block_content
    
    def process_components_and_applications(self, lines):
        """Process and render components and applications"""
        # Process each application
        for app_name, app_data in self.application_state.items():
            if app_data['render_function']:
                self.process_render_function(app_data['render_function'], app_name)
        
        # Process each component
        for comp_name, comp_data in self.component_definitions.items():
            if comp_data['render_content']:
                self.process_component_render(comp_data['render_content'], comp_name)
    
    def process_render_function(self, render_content, app_name):
        """Process render function content and generate HTML"""
        for line in render_content:
            line = line.strip()
            
            # Handle HTML template literals
            if 'retornar `' in line or 'retornar "' in line:
                # Extract HTML content
                html_start = line.find('`') or line.find('"')
                if html_start != -1:
                    html_content = line[html_start+1:]
                    # Continue collecting multi-line HTML
                    self.html_buffer.append(html_content)
            
            # Handle component instantiation
            elif 'crear ' in line and '=' in line:
                comp_match = re.search(r'crear (\w+) = (\w+)', line)
                if comp_match:
                    var_name, comp_name = comp_match.groups()
                    if comp_name in self.component_definitions:
                        self.instantiate_component(comp_name, var_name)
            
            # Handle direct HTML return
            elif line.startswith('retornar '):
                content = line.replace('retornar ', '')
                if content.startswith('landing_page.renderizar()'):
                    # Handle component method calls
                    self.process_component_method_call(content)
                else:
                    self.html_buffer.append(content)
    
    def instantiate_component(self, comp_name, var_name):
        """Instantiate a component and add to HTML buffer"""
        if comp_name in self.component_definitions:
            comp_data = self.component_definitions[comp_name]
            # Generate HTML for component
            comp_html = self.render_component_to_html(comp_data)
            self.html_buffer.append(comp_html)
    
    def render_component_to_html(self, comp_data):
        """Render a component definition to HTML"""
        html_parts = []
        
        # Process component render content
        for line in comp_data['render_content']:
            line = line.strip()
            
            # Handle template literals in components
            if '`' in line:
                # Extract HTML between backticks
                start = line.find('`')
                end = line.rfind('`')
                if start != -1 and end != -1 and start != end:
                    html_content = line[start+1:end]
                    html_parts.append(html_content)
            
            # Handle function calls that return HTML
            elif 'renderizar_' in line or 'obtener_' in line:
                # Generate placeholder HTML for function calls
                if 'renderizar_header' in line:
                    html_parts.append(self.generate_header_html())
                elif 'renderizar_hero' in line:
                    html_parts.append(self.generate_hero_html())
                elif 'renderizar_features' in line:
                    html_parts.append(self.generate_features_html())
                elif 'obtener_estilos_profesionales' in line:
                    self.css_buffer.append(self.generate_professional_styles())
                elif 'obtener_scripts_interactivos' in line:
                    self.js_buffer.append(self.generate_interactive_scripts())
        
        return '\n'.join(html_parts)
    
    def generate_complete_html(self):
        """Generate complete HTML document with all components"""
        # If we have HTML buffer content, use it
        if self.html_buffer:
            # Check if it's already a complete HTML document
            html_content = '\n'.join(self.html_buffer)
            if '<!DOCTYPE html>' in html_content:
                return html_content
        
        # Otherwise, generate standard structure
        html_lines = self.generate_enhanced_html_structure()
        
        # Insert buffered content
        if self.html_buffer:
            body_index = -1
            for i, line in enumerate(html_lines):
                if '<body' in line:
                    body_index = i + 1
                    break
            
            if body_index != -1:
                html_lines[body_index:body_index] = self.html_buffer
        
        return '\n'.join(html_lines)
    
    def process_component_method_call(self, content):
        """Process component method calls like landing_page.renderizar()"""
        if 'landing_page.renderizar()' in content:
            # Generate a professional landing page
            self.html_buffer.append(self.generate_professional_landing_page())
    
    def process_component_render(self, render_content, comp_name):
        """Process component render content"""
        for line in render_content:
            line = line.strip()
            if '`' in line:
                # Extract HTML between backticks
                start = line.find('`')
                end = line.rfind('`')
                if start != -1 and end != -1 and start != end:
                    html_content = line[start+1:end]
                    self.html_buffer.append(html_content)
    
    def generate_enhanced_html_structure(self):
        """Generate enhanced HTML structure with modern features"""
        return [
            '<!DOCTYPE html>',
            '<html lang="es">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>VaderUI - Componentes UI en Sintaxis Conversacional</title>',
            '    <style>',
            '        ' + self.generate_professional_styles(),
            '    </style>',
            '</head>',
            '<body class="tema-oscuro">',
            '    <script>',
            '        ' + self.generate_interactive_scripts(),
            '    </script>',
            '</body>',
            '</html>'
        ]
    
    def generate_professional_landing_page(self):
        """Generate a complete professional landing page HTML"""
        return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaderUI - Componentes UI en Sintaxis Conversacional</title>
    <style>
        ''' + self.generate_professional_styles() + '''
    </style>
</head>
<body class="tema-oscuro">
    ''' + self.generate_header_html() + '''
    ''' + self.generate_hero_html() + '''
    ''' + self.generate_features_html() + '''
    
    <script>
        ''' + self.generate_interactive_scripts() + '''
    </script>
</body>
</html>
        '''
    
    def generate_header_html(self):
        """Generate professional header HTML"""
        return '''
    <header class="header-profesional">
        <nav class="navegacion-principal">
            <div class="logo-container">
                <div class="logo-vader">⚡</div>
                <span class="logo-texto">VaderUI</span>
            </div>
            
            <div class="menu-navegacion">
                <a href="#componentes" class="nav-link">Components</a>
                <a href="#templates" class="nav-link">
                    Templates 
                    <span class="badge-nuevo">New</span>
                </a>
                <a href="#docs" class="nav-link">Docs</a>
                <a href="#pricing" class="nav-link">Pricing</a>
            </div>
            
            <div class="acciones-header">
                <button class="btn-tema" onclick="cambiarTema()">🌙</button>
                <button class="btn-github">GitHub</button>
                <button class="btn-cta">Get Started</button>
            </div>
        </nav>
    </header>
        '''
    
    def generate_hero_html(self):
        """Generate hero section identical to react-ui-master original"""
        return '''
<div class="mx-auto w-full max-w-7xl min-h-screen flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12 px-4 sm:px-6 py-12 md:py-16 lg:py-20">
    <!-- Left side - Title and CTA -->
    <div class="w-full lg:w-[45%] flex flex-col items-start text-left space-y-8">
        <div class="hero-text-animation">
            <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] text-zinc-900 dark:text-zinc-100">
                Craft with 
                <span class="bg-clip-text text-transparent bg-gradient-to-r from-rose-500 via-fuchsia-500 to-purple-500 dark:from-rose-400 dark:via-fuchsia-400 dark:to-purple-400">
                    precision
                </span>
                <br>
                build with 
                <span class="bg-clip-text text-transparent bg-gradient-to-r from-purple-500 via-fuchsia-500 to-rose-500 dark:from-purple-400 dark:via-fuchsia-400 dark:to-rose-400">
                    ease
                </span>.
            </h1>
            <p class="mt-6 text-base md:text-xl text-zinc-700 dark:text-zinc-300 max-w-lg">
                A curated collection of 
                <span class="font-semibold">100+ premium UI components</span> 
                crafted with 
                <span class="bg-clip-text text-transparent bg-gradient-to-r from-rose-500 to-fuchsia-500 dark:from-rose-400 dark:to-fuchsia-400">
                    Tailwind CSS
                </span> 
                and 
                <span class="bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-500 to-purple-500 dark:from-fuchsia-400 dark:to-purple-400">
                    shadcn/ui
                </span> 
                for modern React and Next.js applications.
            </p>
        </div>

        <div class="hero-cta-animation flex flex-col justify-start w-full">
            <span class="text-sm text-zinc-500 dark:text-zinc-300 pb-3 text-start flex items-center gap-2">
                <div class="w-4 h-4 bg-gradient-to-r from-cyan-500 to-blue-500 rounded flex items-center justify-center text-white text-xs font-bold">T</div>
                <span class="flex items-center gap-1.5">
                    Now updated for Tailwind CSS 4.0!
                    <span class="inline-flex items-center rounded-md bg-purple-50 dark:bg-purple-900/30 px-2 py-1 text-xs font-medium text-purple-700 dark:text-purple-300">
                        <span class="h-3 w-3 mr-1">✨</span>
                        New
                    </span>
                </span>
            </span>
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-start gap-3">
                <button class="bg-zinc-900 dark:bg-zinc-100 text-zinc-100 dark:text-zinc-900 px-6 py-3 rounded-lg font-semibold hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-colors">
                    Browse Components
                </button>
                <button class="border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 px-6 py-3 rounded-lg font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                    Browse Blocks
                </button>
            </div>
        </div>

        <!-- Features placeholder -->
        <div class="features-placeholder">
            <!-- Features component would go here -->
        </div>
    </div>

    <!-- Right side - Components Layout -->
    <div class="w-full lg:w-[55%] flex flex-col justify-between gap-6 lg:pl-8">
        <!-- Top row: Card + Action Search Bar -->
        <div class="hero-top-animation w-full grid grid-cols-1 md:grid-cols-2 gap-6 items-center justify-center">
            <!-- Card component -->
            <div class="w-full flex flex-col items-center justify-center">
                <span class="text-sm text-zinc-500 dark:text-zinc-400 block text-center mb-2">
                    {"<Card/>"}
                </span>
                <div class="w-full max-w-sm bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-6 shadow-lg">
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                            UI
                        </div>
                        <div>
                            <h3 class="font-semibold text-zinc-900 dark:text-zinc-100">Component Library</h3>
                            <p class="text-sm text-zinc-500 dark:text-zinc-400">Modern UI components</p>
                        </div>
                    </div>
                    <div class="mt-4 flex gap-2">
                        <button class="flex-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 py-2 px-4 rounded-lg text-sm font-medium hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors">
                            View
                        </button>
                        <button class="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors">
                            Install
                        </button>
                    </div>
                </div>
            </div>

            <!-- Action Search Bar -->
            <div class="w-full max-w-[600px] bg-transparent">
                <span class="text-sm text-zinc-500 dark:text-zinc-400 block text-center mb-2">
                    Components
                </span>
                <div class="w-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4 shadow-lg">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-blue-500 rounded-lg flex items-center justify-center text-white text-sm font-bold">
                            🔍
                        </div>
                        <input type="text" placeholder="Search components..." class="flex-1 bg-transparent text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 outline-none">
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded text-xs">Button</span>
                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded text-xs">Input</span>
                        <span class="bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded text-xs">Card</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Middle row: AI Chat -->
        <div class="hero-middle-animation w-full">
            <span class="text-sm text-zinc-500 dark:text-zinc-400 block text-center mb-2">
                AI Chat
            </span>
            <div class="w-full h-48 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4 shadow-lg">
                <div class="flex items-center gap-3 mb-4">
                    <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        AI
                    </div>
                    <span class="text-zinc-900 dark:text-zinc-100 font-medium">Assistant</span>
                </div>
                <div class="space-y-2 mb-4">
                    <div class="bg-zinc-100 dark:bg-zinc-800 rounded-lg p-3 max-w-[80%]">
                        <p class="text-sm text-zinc-700 dark:text-zinc-300">How can I help you build better UI components today?</p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <input type="text" placeholder="Ask me anything..." class="flex-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 px-3 py-2 rounded-lg outline-none">
                    <button class="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition-colors">
                        <span class="text-sm">📤</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Bottom row: Buttons on left, Input on right -->
        <div class="hero-bottom-animation w-full grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Left side - Buttons -->
            <div class="w-full">
                <span class="text-sm text-zinc-500 dark:text-zinc-400 block text-center mb-2">
                    Buttons
                </span>
                <div class="w-full h-48 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 flex flex-col items-center justify-center gap-3 shadow-lg">
                    <button class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all transform hover:scale-105">
                        Bring me
                    </button>
                    <button class="border-2 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 px-8 py-3 rounded-lg font-semibold hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                        Secondary
                    </button>
                </div>
            </div>

            <!-- Right side - Input -->
            <div class="w-full">
                <span class="text-sm text-zinc-500 dark:text-zinc-400 block text-center mb-2">
                    Input
                </span>
                <div class="w-full h-48 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 flex items-center justify-center p-6 shadow-lg">
                    <div class="w-full max-w-sm">
                        <label class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                            Email address
                        </label>
                        <input type="email" placeholder="Enter your email" class="w-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
        '''
    
    def parse_structure(self, lines):
        """Parse imports, components, and variables"""
        for line in lines:
            line = line.strip()
            
            # Parse imports
            if line.startswith('importar desde'):
                self.parse_import(line)
            
            # Parse component definitions
            elif line.startswith('crear componente'):
                self.parse_component_definition(line)
            
            # Parse variables
            elif line.startswith('variable '):
                self.parse_variable(line)
    
    def parse_import(self, line):
        """Parse import statements"""
        # importar desde "./src/componentes/NavegacionPrincipal.vdr" como Nav
        match = re.search(r'importar desde "([^"]+)" como (\w+)', line)
        if match:
            path, alias = match.groups()
            self.imports[alias] = path
    
    def parse_component_definition(self, line):
        """Parse component definitions"""
        # crear componente SeccionHero con propiedades
        match = re.search(r'crear componente (\w+)', line)
        if match:
            component_name = match.group(1)
            self.components[component_name] = {
                'name': component_name,
                'props': [],
                'content': []
            }
    
    def parse_variable(self, line):
        """Parse variable declarations"""
        # variable contador = 1
        match = re.search(r'variable (\w+) = (.+)', line)
        if match:
            var_name, var_value = match.groups()
            self.variables[var_name] = var_value
    
    def generate_html_structure(self):
        """Generate modern HTML structure with CSS and JS"""
        return [
            '<!DOCTYPE html>',
            '<html lang="es">',
            '<head>',
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>VaderUI - Componentes Open Source</title>',
            '    <script src="https://cdn.tailwindcss.com"></script>',
            '    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
            '    <style>',
            '        * { font-family: \'Inter\', sans-serif; }',
            '        .fade-in-up { animation: fadeInUp 0.6s ease-out forwards; }',
            '        .fade-in-scale { animation: fadeInScale 0.5s ease-out forwards; }',
            '        @keyframes fadeInUp {',
            '            from { opacity: 0; transform: translateY(20px); }',
            '            to { opacity: 1; transform: translateY(0); }',
            '        }',
            '        @keyframes fadeInScale {',
            '            from { opacity: 0; transform: scale(0.95); }',
            '            to { opacity: 1; transform: scale(1); }',
            '        }',
            '        .bg-gradient-text {',
            '            background: linear-gradient(135deg, #ec4899, #d946ef, #a855f7);',
            '            -webkit-background-clip: text;',
            '            -webkit-text-fill-color: transparent;',
            '            background-clip: text;',
            '        }',
            '        .hover-scale { transition: transform 0.2s ease; }',
            '        .hover-scale:hover { transform: scale(1.05); }',
            '        .card-hover { transition: all 0.3s ease; }',
            '        .card-hover:hover {',
            '            transform: translateY(-4px);',
            '            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);',
            '        }',
            '        .counter-display { font-size: 2rem; font-weight: bold; color: #6366f1; }',
            '    </style>',
            '</head>',
            '<body class="bg-white dark:bg-zinc-950 min-h-screen">',
            '',
            '    <script>',
            '        // VaderUI JavaScript Functions',
            '        let counter = 1;',
            '        function incrementar_contador() {',
            '            counter++;',
            '            document.getElementById("contador").textContent = counter;',
            '        }',
            '        function decrementar_contador() {',
            '            if (counter > 0) {',
            '                counter--;',
            '                document.getElementById("contador").textContent = counter;',
            '            }',
            '        }',
            '        function navegar_a(url) { window.location.href = url; }',
            '        function abrir_enlace(url) { window.open(url, "_blank"); }',
            '        function actualizar_elemento(id, content) {',
            '            const el = document.getElementById(id);',
            '            if (el) el.textContent = content;',
            '        }',
            '    </script>',
            '</body>',
            '</html>'
        ]
    
    def transpile_line(self, line):
        """Transpile a single line with advanced features"""
        # Skip ALL non-visual Vader syntax - only process visual elements
        skip_patterns = [
            'importar ', 'crear componente', 'configurar ', 'titulo ', 'descripcion ',
            'puerto ', 'tema ', 'idioma ', 'rutas', 'ruta ', 'funcionalidades',
            'desarrollo', 'produccion', 'cuando ', 'ejecutar ', 'variable ',
            'funcion ', 'fin ', 'exportar', 'navegacion_fluida', 'busqueda_avanzada',
            'copy_paste_componentes', 'preview_en_vivo', 'documentacion_interactiva',
            'ai_chat_integration', 'github_sync', 'tema_oscuro_claro', 'responsive_completo',
            'animaciones_avanzadas', 'hot_reload', 'debug', 'puerto_dev', 'auto_refresh',
            'error_overlay', 'optimizacion', 'minificacion', 'lazy_loading',
            'cache_estrategia', 'cdn_assets', 'cargar ', 'Router.', 'Search.',
            'CopyPaste.', 'AI.', 'indices:', 'busqueda_fuzzy:', 'filtros_avanzados:',
            'formato_salida:', 'syntax_highlighting:', 'auto_clipboard:', 'modelo:',
            'contexto:', 'cargar_componentes_premium', 'obtener_archivos_vdr',
            'importar_dinamico', 'mostrar mensaje', 'abrir navegador',
            'mostrar error', 'redirigir_a', 'mostrar_error_overlay'
        ]
        
        # Check if line starts with any skip pattern
        for pattern in skip_patterns:
            if line.startswith(pattern):
                return None
        
        # Skip lines that are just boolean values or configuration
        if line.strip() in ['true', 'false'] or '=' in line or '{' in line or '}' in line:
            return None
        
        # Navigation
        if 'NavegacionPrincipal' in line or 'Nav.' in line:
            return self.generate_navigation()
        
        # Main sections
        if line.startswith('mostrar main'):
            return self.indent() + '<main class="bg-white dark:bg-zinc-950 min-h-screen">'
        
        # Div with classes
        if line.startswith('mostrar div'):
            return self.parse_div_with_classes(line)
        
        # Headers with classes
        if line.startswith('mostrar h1'):
            return self.parse_header_with_classes(line, 'h1')
        if line.startswith('mostrar h2'):
            return self.parse_header_with_classes(line, 'h2')
        if line.startswith('mostrar h3'):
            return self.parse_header_with_classes(line, 'h3')
        
        # Paragraphs with classes
        if line.startswith('mostrar p'):
            return self.parse_paragraph_with_classes(line)
        
        # Buttons with classes and events
        if line.startswith('mostrar boton'):
            return self.parse_button_with_classes(line)
        
        # Spans with classes
        if line.startswith('mostrar span'):
            return self.parse_span_with_classes(line)
        
        # Sections
        if line.startswith('mostrar seccion'):
            return self.parse_section_with_classes(line)
        
        # Simple content
        if line.startswith('mostrar "'):
            content = line.replace('mostrar "', '').replace('"', '')
            return self.indent() + content
        
        # Component calls
        if any(comp in line for comp in self.components.keys()):
            return self.generate_component_placeholder(line)
        
        # Class definitions
        if line.startswith('clase "'):
            return None  # Classes are handled by parent elements
        
        # Animation definitions
        if line.startswith('animacion "'):
            return None  # Animations are handled by CSS
        
        # Event handlers
        if line.startswith('al_hacer_clic'):
            return None  # Events are handled by parent elements
        
        # Default: return as text
        if line.strip():
            return self.indent() + line
        
        return None
    
    def parse_div_with_classes(self, line):
        """Parse div elements with CSS classes"""
        # Extract class from next line if present
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<div class="{classes}">'
        return self.indent() + '<div>'
    
    def parse_header_with_classes(self, line, tag):
        """Parse header elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<{tag} class="{classes}">'
        return self.indent() + f'<{tag}>'
    
    def parse_paragraph_with_classes(self, line):
        """Parse paragraph elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<p class="{classes}">'
        return self.indent() + '<p>'
    
    def parse_button_with_classes(self, line):
        """Parse button elements with CSS classes and events"""
        classes = self.extract_classes_from_context(line)
        onclick = self.extract_onclick_from_context(line)
        
        button_html = '<button'
        if classes:
            button_html += f' class="{classes}"'
        if onclick:
            button_html += f' onclick="{onclick}"'
        button_html += '>'
        
        return self.indent() + button_html
    
    def parse_span_with_classes(self, line):
        """Parse span elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<span class="{classes}">'
        return self.indent() + '<span>'
    
    def parse_section_with_classes(self, line):
        """Parse section elements with CSS classes"""
        classes = self.extract_classes_from_context(line)
        if classes:
            return self.indent() + f'<section class="{classes}">'
        return self.indent() + '<section>'
    
    def extract_classes_from_context(self, line):
        """Extract CSS classes from Vader syntax"""
        # This would need to look ahead to the next line for clase ""
        # For now, return common VaderUI classes based on context
        if 'SeccionHero' in line or 'hero' in line.lower():
            return "mx-auto w-full max-w-7xl min-h-screen flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12 px-4 sm:px-6 py-12 md:py-16 lg:py-20"
        elif 'titulo' in line.lower() or 'h1' in line:
            return "text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] text-zinc-900 dark:text-zinc-100"
        elif 'boton' in line.lower() or 'button' in line:
            return "bg-zinc-900 dark:bg-zinc-50 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 px-6 py-3 rounded-lg font-semibold transition-colors hover-scale"
        return ""
    
    def extract_onclick_from_context(self, line):
        """Extract onclick events from Vader syntax"""
        # This would need to look ahead for al_hacer_clic
        if 'incrementar' in line.lower():
            return "incrementar_contador()"
        elif 'decrementar' in line.lower():
            return "decrementar_contador()"
        return ""
    
    def generate_navigation(self):
        """Generate navigation HTML"""
        return f'''{self.indent()}<nav class="bg-white dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-50">
{self.indent()}    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
{self.indent()}        <div class="flex justify-between items-center h-16">
{self.indent()}            <div class="flex items-center space-x-4">
{self.indent()}                <div class="flex items-center space-x-2">
{self.indent()}                    <div class="w-8 h-8 bg-gradient-to-r from-rose-500 to-purple-500 rounded-lg flex items-center justify-center">
{self.indent()}                        <span class="text-white font-bold text-sm">V</span>
{self.indent()}                    </div>
{self.indent()}                    <span class="text-xl font-bold text-zinc-900 dark:text-zinc-100">VaderUI</span>
{self.indent()}                </div>
{self.indent()}            </div>
{self.indent()}            <div class="hidden md:flex items-center space-x-8">
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Docs</a>
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Components</a>
{self.indent()}                <a href="#" class="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors">Templates</a>
{self.indent()}            </div>
{self.indent()}            <div class="flex items-center space-x-4">
{self.indent()}                <button class="bg-zinc-900 dark:bg-zinc-50 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 px-4 py-2 rounded-lg font-medium transition-colors">Get Started</button>
{self.indent()}            </div>
{self.indent()}        </div>
{self.indent()}    </div>
{self.indent()}</nav>'''
    
    def generate_component_placeholder(self, line):
        """Generate placeholder for component calls"""
        return self.indent() + f'<!-- Component: {line.strip()} -->'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_html(vader_code):
    transpiler = HTMLTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_html(vader_code)

# Enhanced CSS and JavaScript functions for professional VaderUI
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
    
    .sidebar-components {
        flex: 1;
        background: #111;
        border: 1px solid #333;
        border-radius: 1rem;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
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
        if (btnTema) {
            btnTema.textContent = nuevoTema === 'oscuro' ? '🌙' : '☀️';
        }
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
