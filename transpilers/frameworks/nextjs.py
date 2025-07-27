"""
Framework Next.js para Vader
"""

class NextJSFramework:
    def __init__(self):
        self.name = "Next.js"
        self.description = "Framework React completo con SSR, SSG y funcionalidades avanzadas"
        self.target_language = "javascript"
        self.keywords = [
            'nextjs', 'next', 'pagina', 'ruta', 'api', 'ssr', 'ssg', 'static',
            'server', 'getServerSideProps', 'getStaticProps', 'getStaticPaths',
            'middleware', 'layout', 'head', 'image', 'link', 'router', 'dynamic',
            'auth', 'session', 'cookie', 'redirect', 'revalidate', 'incremental',
            'app', 'pages', 'components', 'styles', 'public', 'config'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Next.js con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_ssr = any('ssr' in line.lower() or 'getServerSideProps' in line.lower() or 'server' in line.lower() for line in lines)
        uses_ssg = any('ssg' in line.lower() or 'getStaticProps' in line.lower() or 'static' in line.lower() for line in lines)
        uses_api = any('api' in line.lower() or 'endpoint' in line.lower() for line in lines)
        uses_auth = any('auth' in line.lower() or 'session' in line.lower() or 'login' in line.lower() for line in lines)
        uses_router = any('router' in line.lower() or 'navegacion' in line.lower() or 'ruta' in line.lower() for line in lines)
        uses_image = any('image' in line.lower() or 'imagen' in line.lower() for line in lines)
        uses_head = any('head' in line.lower() or 'meta' in line.lower() or 'title' in line.lower() for line in lines)
        uses_dynamic = any('dynamic' in line.lower() or 'lazy' in line.lower() for line in lines)
        uses_middleware = any('middleware' in line.lower() for line in lines)
        uses_layout = any('layout' in line.lower() or 'plantilla' in line.lower() for line in lines)
        
        # Detectar elementos de interfaz
        has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
        has_button = any('boton' in line.lower() or 'button' in line.lower() for line in lines)
        
        # Detectar nombre de página/componente
        page_name = "VaderPage"
        for line in lines:
            if 'pagina' in line.lower() or 'page' in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    page_name = parts[1].capitalize() + "Page"
                break
        
        # Construir código Next.js
        nextjs_code = []
        
        # Imports
        imports = ["import React, { useState, useEffect"]
        if uses_router:
            imports.append(", useRouter")
        imports.append(" } from 'react';")
        
        nextjs_code.append(''.join(imports))
        
        if uses_head:
            nextjs_code.append("import Head from 'next/head';")
        
        if uses_image:
            nextjs_code.append("import Image from 'next/image';")
        
        if uses_router:
            nextjs_code.append("import Link from 'next/link';")
        
        if uses_dynamic:
            nextjs_code.append("import dynamic from 'next/dynamic';")
        
        if uses_auth:
            nextjs_code.append("import { useSession, signIn, signOut } from 'next-auth/react';")
        
        nextjs_code.append("")
        
        # Componente dinámico si es necesario
        if uses_dynamic:
            nextjs_code.append("// Componente dinámico (lazy loading)")
            nextjs_code.append("const DynamicComponent = dynamic(() => import('../components/HeavyComponent'), {")
            nextjs_code.append("  loading: () => <p>Cargando componente...</p>,")
            nextjs_code.append("  ssr: false")
            nextjs_code.append("});")
            nextjs_code.append("")
        
        # Función principal del componente
        nextjs_code.append(f"export default function {page_name}({{ initialData }}) {{")
        
        # Estados
        nextjs_code.append("  // Estados del componente")
        nextjs_code.append("  const [data, setData] = useState(initialData || []);")
        nextjs_code.append("  const [loading, setLoading] = useState(false);")
        nextjs_code.append("  const [error, setError] = useState(null);")
        
        if has_form:
            nextjs_code.append("  const [formData, setFormData] = useState({ name: '', email: '' });")
        
        # Hooks
        if uses_router:
            nextjs_code.append("  const router = useRouter();")
        
        if uses_auth:
            nextjs_code.append("  const { data: session, status } = useSession();")
        
        nextjs_code.append("")
        
        # useEffect
        nextjs_code.append("  // Efectos")
        nextjs_code.append("  useEffect(() => {")
        nextjs_code.append("    console.log('Componente montado');")
        if uses_api and not uses_ssr and not uses_ssg:
            nextjs_code.append("    fetchData();")
        nextjs_code.append("  }, []);")
        nextjs_code.append("")
        
        # Funciones
        if uses_api and not uses_ssr and not uses_ssg:
            nextjs_code.append("  // Función para obtener datos")
            nextjs_code.append("  const fetchData = async () => {")
            nextjs_code.append("    try {")
            nextjs_code.append("      setLoading(true);")
            nextjs_code.append("      const response = await fetch('/api/data');")
            nextjs_code.append("      const result = await response.json();")
            nextjs_code.append("      setData(result.data || []);")
            nextjs_code.append("    } catch (err) {")
            nextjs_code.append("      setError('Error al cargar datos');")
            nextjs_code.append("    } finally {")
            nextjs_code.append("      setLoading(false);")
            nextjs_code.append("    }")
            nextjs_code.append("  };")
            nextjs_code.append("")
        
        if has_form:
            nextjs_code.append("  // Manejo de formulario")
            nextjs_code.append("  const handleSubmit = async (e) => {")
            nextjs_code.append("    e.preventDefault();")
            nextjs_code.append("    setLoading(true);")
            nextjs_code.append("    ")
            nextjs_code.append("    try {")
            nextjs_code.append("      const response = await fetch('/api/submit', {")
            nextjs_code.append("        method: 'POST',")
            nextjs_code.append("        headers: { 'Content-Type': 'application/json' },")
            nextjs_code.append("        body: JSON.stringify(formData)")
            nextjs_code.append("      });")
            nextjs_code.append("      ")
            nextjs_code.append("      if (response.ok) {")
            nextjs_code.append("        setFormData({ name: '', email: '' });")
            nextjs_code.append("        alert('Formulario enviado exitosamente');")
            nextjs_code.append("      }")
            nextjs_code.append("    } catch (err) {")
            nextjs_code.append("      setError('Error al enviar formulario');")
            nextjs_code.append("    } finally {")
            nextjs_code.append("      setLoading(false);")
            nextjs_code.append("    }")
            nextjs_code.append("  };")
            nextjs_code.append("")
        
        if has_list:
            nextjs_code.append("  // Función para eliminar elemento")
            nextjs_code.append("  const removeItem = (index) => {")
            nextjs_code.append("    setData(data.filter((_, i) => i !== index));")
            nextjs_code.append("  };")
            nextjs_code.append("")
        
        if uses_router:
            nextjs_code.append("  // Navegación")
            nextjs_code.append("  const handleNavigation = (path) => {")
            nextjs_code.append("    router.push(path);")
            nextjs_code.append("  };")
            nextjs_code.append("")
        
        # Renderizado condicional para autenticación
        if uses_auth:
            nextjs_code.append("  // Verificar autenticación")
            nextjs_code.append("  if (status === 'loading') return <p>Cargando...</p>;")
            nextjs_code.append("  if (status === 'unauthenticated') {")
            nextjs_code.append("    return (")
            nextjs_code.append("      <div className='auth-container'>")
            nextjs_code.append("        <h1>Acceso Requerido</h1>")
            nextjs_code.append("        <button onClick={() => signIn()}>Iniciar Sesión</button>")
            nextjs_code.append("      </div>")
            nextjs_code.append("    );")
            nextjs_code.append("  }")
            nextjs_code.append("")
        
        # JSX Return
        nextjs_code.append("  return (")
        nextjs_code.append("    <>")
        
        # Head section
        if uses_head:
            nextjs_code.append("      <Head>")
            nextjs_code.append("        <title>Vader Next.js App</title>")
            nextjs_code.append("        <meta name='description' content='Aplicación generada desde código Vader' />")
            nextjs_code.append("        <meta name='viewport' content='width=device-width, initial-scale=1' />")
            nextjs_code.append("        <link rel='icon' href='/favicon.ico' />")
            nextjs_code.append("      </Head>")
        
        # Layout wrapper si se usa
        if uses_layout:
            nextjs_code.append("      <Layout>")
        
        nextjs_code.append("        <div className='vader-container'>")
        nextjs_code.append("          <header className='vader-header'>")
        nextjs_code.append("            <h1>Aplicación Next.js desde Vader</h1>")
        
        # Autenticación en header
        if uses_auth:
            nextjs_code.append("            <div className='auth-section'>")
            nextjs_code.append("              <p>Bienvenido, {session?.user?.name || 'Usuario'}</p>")
            nextjs_code.append("              <button onClick={() => signOut()}>Cerrar Sesión</button>")
            nextjs_code.append("            </div>")
        
        nextjs_code.append("          </header>")
        nextjs_code.append("")
        
        # Navegación
        if uses_router:
            nextjs_code.append("          <nav className='vader-nav'>")
            nextjs_code.append("            <Link href='/'>")
            nextjs_code.append("              <a className='nav-link'>Inicio</a>")
            nextjs_code.append("            </Link>")
            nextjs_code.append("            <Link href='/about'>")
            nextjs_code.append("              <a className='nav-link'>Acerca</a>")
            nextjs_code.append("            </Link>")
            nextjs_code.append("            <Link href='/contact'>")
            nextjs_code.append("              <a className='nav-link'>Contacto</a>")
            nextjs_code.append("            </Link>")
            nextjs_code.append("          </nav>")
        
        nextjs_code.append("")
        nextjs_code.append("          <main className='vader-main'>")
        
        # Estados de carga y error
        nextjs_code.append("            {loading && <div className='loading'>Cargando...</div>}")
        nextjs_code.append("            {error && <div className='error'>{error}</div>}")
        nextjs_code.append("")
        
        # Formulario si se detecta
        if has_form:
            nextjs_code.append("            <section className='vader-form-section'>")
            nextjs_code.append("              <h2>Formulario de Contacto</h2>")
            nextjs_code.append("              <form onSubmit={handleSubmit} className='vader-form'>")
            nextjs_code.append("                <div className='form-group'>")
            nextjs_code.append("                  <label htmlFor='name'>Nombre:</label>")
            nextjs_code.append("                  <input")
            nextjs_code.append("                    type='text'")
            nextjs_code.append("                    id='name'")
            nextjs_code.append("                    value={formData.name}")
            nextjs_code.append("                    onChange={(e) => setFormData({...formData, name: e.target.value})}")
            nextjs_code.append("                    required")
            nextjs_code.append("                  />")
            nextjs_code.append("                </div>")
            nextjs_code.append("                <div className='form-group'>")
            nextjs_code.append("                  <label htmlFor='email'>Email:</label>")
            nextjs_code.append("                  <input")
            nextjs_code.append("                    type='email'")
            nextjs_code.append("                    id='email'")
            nextjs_code.append("                    value={formData.email}")
            nextjs_code.append("                    onChange={(e) => setFormData({...formData, email: e.target.value})}")
            nextjs_code.append("                    required")
            nextjs_code.append("                  />")
            nextjs_code.append("                </div>")
            nextjs_code.append("                <button type='submit' disabled={loading}>")
            nextjs_code.append("                  {loading ? 'Enviando...' : 'Enviar'}")
            nextjs_code.append("                </button>")
            nextjs_code.append("              </form>")
            nextjs_code.append("            </section>")
            nextjs_code.append("")
        
        # Lista si se detecta
        if has_list:
            nextjs_code.append("            <section className='vader-list-section'>")
            nextjs_code.append("              <h2>Lista de Elementos</h2>")
            nextjs_code.append("              {data.length > 0 ? (")
            nextjs_code.append("                <ul className='vader-list'>")
            nextjs_code.append("                  {data.map((item, index) => (")
            nextjs_code.append("                    <li key={index} className='list-item'>")
            nextjs_code.append("                      <span>{item.name || item}</span>")
            nextjs_code.append("                      <button onClick={() => removeItem(index)}>Eliminar</button>")
            nextjs_code.append("                    </li>")
            nextjs_code.append("                  ))}")
            nextjs_code.append("                </ul>")
            nextjs_code.append("              ) : (")
            nextjs_code.append("                <p className='empty-state'>No hay elementos para mostrar</p>")
            nextjs_code.append("              )}")
            nextjs_code.append("            </section>")
            nextjs_code.append("")
        
        # Imagen optimizada si se usa
        if uses_image:
            nextjs_code.append("            <section className='vader-image-section'>")
            nextjs_code.append("              <h2>Imagen Optimizada</h2>")
            nextjs_code.append("              <Image")
            nextjs_code.append("                src='/vader-logo.png'")
            nextjs_code.append("                alt='Logo de Vader'")
            nextjs_code.append("                width={300}")
            nextjs_code.append("                height={200}")
            nextjs_code.append("                priority")
            nextjs_code.append("              />")
            nextjs_code.append("            </section>")
            nextjs_code.append("")
        
        # Componente dinámico
        if uses_dynamic:
            nextjs_code.append("            <section className='vader-dynamic-section'>")
            nextjs_code.append("              <h2>Componente Dinámico</h2>")
            nextjs_code.append("              <DynamicComponent />")
            nextjs_code.append("            </section>")
            nextjs_code.append("")
        
        nextjs_code.append("          </main>")
        nextjs_code.append("        </div>")
        
        if uses_layout:
            nextjs_code.append("      </Layout>")
        
        nextjs_code.append("    </>")
        nextjs_code.append("  );")
        nextjs_code.append("}")
        nextjs_code.append("")
        
        # Funciones de Next.js para SSR/SSG
        if uses_ssr:
            nextjs_code.append("// Server-Side Rendering")
            nextjs_code.append("export async function getServerSideProps(context) {")
            nextjs_code.append("  try {")
            nextjs_code.append("    // Obtener datos del servidor en cada request")
            nextjs_code.append("    const res = await fetch(`${process.env.API_URL}/api/data`);")
            nextjs_code.append("    const data = await res.json();")
            nextjs_code.append("    ")
            nextjs_code.append("    return {")
            nextjs_code.append("      props: {")
            nextjs_code.append("        initialData: data.data || []")
            nextjs_code.append("      }")
            nextjs_code.append("    };")
            nextjs_code.append("  } catch (error) {")
            nextjs_code.append("    return {")
            nextjs_code.append("      props: {")
            nextjs_code.append("        initialData: []")
            nextjs_code.append("      }")
            nextjs_code.append("    };")
            nextjs_code.append("  }")
            nextjs_code.append("}")
        
        if uses_ssg:
            nextjs_code.append("// Static Site Generation")
            nextjs_code.append("export async function getStaticProps() {")
            nextjs_code.append("  try {")
            nextjs_code.append("    // Obtener datos en build time")
            nextjs_code.append("    const res = await fetch(`${process.env.API_URL}/api/data`);")
            nextjs_code.append("    const data = await res.json();")
            nextjs_code.append("    ")
            nextjs_code.append("    return {")
            nextjs_code.append("      props: {")
            nextjs_code.append("        initialData: data.data || []")
            nextjs_code.append("      },")
            nextjs_code.append("      revalidate: 60 // Revalidar cada 60 segundos (ISR)")
            nextjs_code.append("    };")
            nextjs_code.append("  } catch (error) {")
            nextjs_code.append("    return {")
            nextjs_code.append("      props: {")
            nextjs_code.append("        initialData: []")
            nextjs_code.append("      }")
            nextjs_code.append("    };")
            nextjs_code.append("  }")
            nextjs_code.append("}")
        
        # Estilos CSS-in-JS
        nextjs_code.append("")
        nextjs_code.append("// Estilos (se puede mover a un archivo .module.css)")
        nextjs_code.append("const styles = `")
        nextjs_code.append("  .vader-container {")
        nextjs_code.append("    max-width: 1200px;")
        nextjs_code.append("    margin: 0 auto;")
        nextjs_code.append("    padding: 20px;")
        nextjs_code.append("    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;")
        nextjs_code.append("  }")
        nextjs_code.append("  .vader-header {")
        nextjs_code.append("    display: flex;")
        nextjs_code.append("    justify-content: space-between;")
        nextjs_code.append("    align-items: center;")
        nextjs_code.append("    margin-bottom: 30px;")
        nextjs_code.append("    padding-bottom: 20px;")
        nextjs_code.append("    border-bottom: 1px solid #eee;")
        nextjs_code.append("  }")
        nextjs_code.append("  .vader-nav {")
        nextjs_code.append("    display: flex;")
        nextjs_code.append("    gap: 20px;")
        nextjs_code.append("    margin-bottom: 30px;")
        nextjs_code.append("  }")
        nextjs_code.append("  .nav-link {")
        nextjs_code.append("    color: #0070f3;")
        nextjs_code.append("    text-decoration: none;")
        nextjs_code.append("    font-weight: 500;")
        nextjs_code.append("  }")
        nextjs_code.append("  .nav-link:hover {")
        nextjs_code.append("    text-decoration: underline;")
        nextjs_code.append("  }")
        nextjs_code.append("  .vader-form {")
        nextjs_code.append("    max-width: 500px;")
        nextjs_code.append("    margin: 20px 0;")
        nextjs_code.append("  }")
        nextjs_code.append("  .form-group {")
        nextjs_code.append("    margin-bottom: 15px;")
        nextjs_code.append("  }")
        nextjs_code.append("  .form-group label {")
        nextjs_code.append("    display: block;")
        nextjs_code.append("    margin-bottom: 5px;")
        nextjs_code.append("    font-weight: 500;")
        nextjs_code.append("  }")
        nextjs_code.append("  .form-group input {")
        nextjs_code.append("    width: 100%;")
        nextjs_code.append("    padding: 10px;")
        nextjs_code.append("    border: 1px solid #ddd;")
        nextjs_code.append("    border-radius: 4px;")
        nextjs_code.append("    font-size: 16px;")
        nextjs_code.append("  }")
        nextjs_code.append("  .vader-list {")
        nextjs_code.append("    list-style: none;")
        nextjs_code.append("    padding: 0;")
        nextjs_code.append("  }")
        nextjs_code.append("  .list-item {")
        nextjs_code.append("    display: flex;")
        nextjs_code.append("    justify-content: space-between;")
        nextjs_code.append("    align-items: center;")
        nextjs_code.append("    padding: 10px;")
        nextjs_code.append("    border: 1px solid #eee;")
        nextjs_code.append("    margin-bottom: 5px;")
        nextjs_code.append("    border-radius: 4px;")
        nextjs_code.append("  }")
        nextjs_code.append("  .loading, .error {")
        nextjs_code.append("    text-align: center;")
        nextjs_code.append("    padding: 20px;")
        nextjs_code.append("    margin: 20px 0;")
        nextjs_code.append("  }")
        nextjs_code.append("  .error {")
        nextjs_code.append("    color: #e00;")
        nextjs_code.append("    background-color: #fee;")
        nextjs_code.append("    border: 1px solid #fcc;")
        nextjs_code.append("    border-radius: 4px;")
        nextjs_code.append("  }")
        nextjs_code.append("`;")        
        
        return '\n'.join(nextjs_code)
