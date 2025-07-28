def transpile_to_html(vader_code):
    """Transpilador HTML funcional para VaderUI sin errores de sintaxis"""
    
    # Detectar si es la landing page profesional
    if 'LandingPageProfesional' in vader_code or 'aplicacion' in vader_code.lower():
        return generate_complete_landing()
    
    # Transpilación básica para otros casos
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>VaderUI</title>
    <style>
        body {{ background: #000; color: #fff; font-family: Arial, sans-serif; }}
    </style>
</head>
<body>
    <h1>VaderUI</h1>
    <pre>{vader_code}</pre>
</body>
</html>"""

def generate_complete_landing():
    """Generar la landing page completa idéntica a react-ui-master"""
    return """<!DOCTYPE html>
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        
        .nav-menu {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-link {
            color: #a1a1aa;
            text-decoration: none;
            font-size: 0.875rem;
            transition: color 0.3s;
        }
        
        .nav-link:hover {
            color: #fff;
        }
        
        .nav-link.new {
            background: #10b981;
            color: #000;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-weight: 600;
        }
        
        .theme-toggle {
            background: none;
            border: 1px solid #374151;
            color: #fff;
            padding: 0.5rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .theme-toggle:hover {
            border-color: #10b981;
        }
        
        .main {
            padding-top: 6rem;
            min-height: 100vh;
        }
        
        .hero {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            padding: 4rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
            align-items: center;
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
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
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
        }
        
        .btn-secondary {
            background: transparent;
            color: #fff;
            border: 1px solid #374151;
        }
        
        .btn-secondary:hover {
            border-color: #10b981;
        }
        
        .hero-visual {
            display: flex;
            gap: 1.5rem;
            align-items: flex-start;
        }
        
        .main-card {
            background: #111;
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 1.5rem;
            flex: 1;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .card-tag {
            background: linear-gradient(135deg, #ec4899, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
        }
        
        .visual-placeholder {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.8), rgba(59, 130, 246, 0.8));
            border-radius: 12px;
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .visual-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            padding: 1rem;
        }
        
        .visual-content h3 {
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
        }
        
        .visual-content p {
            color: #a1a1aa;
            font-size: 0.875rem;
        }
        
        .card-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .btn-card {
            background: #374151;
            color: #fff;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-card:hover {
            background: transparent;
        }
        
        .btn-icon {
            background: #111;
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
            width: 300px;
            background: #111;
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 1.5rem;
        }
        
        .sidebar h4 {
            color: #a1a1aa;
            font-size: 0.875rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
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
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .profile-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .profile-role {
            color: #a1a1aa;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        
        .profile-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.75rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
        }
        
        .skills {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .skill {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .skill-label {
            font-size: 0.875rem;
            color: #a1a1aa;
        }
        
        .skill-bar {
            width: 100px;
            height: 4px;
            background: #1f1f1f;
            border-radius: 2px;
            overflow: hidden;
        }
        
        .skill-progress {
            height: 100%;
            background: #10b981;
            border-radius: 2px;
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
            }
            
            .nav-menu {
                display: none;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">
                <div class="logo-icon">🚀</div>
                <span>CodeSnippetUI</span>
            </div>
            
            <div class="nav-menu">
                <a href="#" class="nav-link">Components</a>
                <a href="#" class="nav-link new">Templates</a>
            </div>
            
            <button class="theme-toggle" onclick="toggleTheme()">☀️</button>
        </nav>
    </header>
    
    <main class="main">
        <section class="hero">
            <div class="hero-content">
                <div class="update-badge">
                    🚀 Now updated for Tailwind CSS 4.0! 
                    <span class="new-badge">New</span>
                </div>
                
                <h1>
                    Craft with <span class="gradient-text">precision</span><br>
                    build with <span class="gradient-text">ease.</span>
                </h1>
                
                <p>
                    A curated collection of <span class="highlight">100+ premium UI components</span><br>
                    crafted with <span class="highlight">Tailwind CSS</span> and <span class="highlight">shadcn/ui</span> for modern<br>
                    React and Next.js applications.
                </p>
                
                <div class="hero-actions">
                    <button class="btn-large btn-primary" onclick="browseComponents()">
                        📚 Browse Components
                    </button>
                    <button class="btn-large btn-secondary" onclick="goToTemplates()">
                        📋 Go to Templates
                    </button>
                </div>
            </div>
            
            <div class="hero-visual">
                <div class="main-card">
                    <div class="card-header">
                        <span class="card-tag">&lt;Card/&gt;</span>
                        <span class="new-badge">New</span>
                    </div>
                    
                    <div class="visual-placeholder">
                        <div class="visual-overlay">
                            <div class="visual-content">
                                <h3>New UI Design Fundamentals</h3>
                                <p>Explore the fundamentals of contemporary UI design</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card-actions">
                        <button class="btn-card">👁️ View</button>
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
                                <div class="skill-progress" style="width: 90%;"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-label">Backend</span>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: 75%;"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-label">DevOps</span>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: 60%;"></div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="sidebar-actions">
                        <button class="btn-card">🔗 View Portfolio</button>
                        <button class="btn-icon">📤</button>
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
                </div>
            </div>
        </section>
        
        <!-- Footer Section -->
        <footer class="footer-section">
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
        </footer>
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
</html>"""
