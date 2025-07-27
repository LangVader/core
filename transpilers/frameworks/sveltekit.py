"""
Framework SvelteKit para Vader
"""

class SvelteKitFramework:
    def __init__(self):
        self.name = "SvelteKit"
        self.description = "Framework full-stack de Svelte con SSR, SSG y API routes"
        self.target_language = "javascript"
        self.keywords = [
            'sveltekit', 'kit', 'fullstack', 'ssr', 'ssg', 'prerender', 'hydrate',
            'load', 'preload', 'api', 'endpoint', 'route', 'layout', 'error',
            'page', 'server', 'client', 'adapter', 'vite', 'hooks', 'session',
            'platform', 'env', 'params', 'url', 'fetch', 'request', 'response',
            'get', 'post', 'put', 'delete', 'patch', 'head', 'options'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a SvelteKit con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_ssr = any('ssr' in line.lower() or 'server' in line.lower() or 'load' in line.lower() for line in lines)
        uses_api = any('api' in line.lower() or 'endpoint' in line.lower() or 'get' in line.lower() or 'post' in line.lower() for line in lines)
        uses_prerender = any('prerender' in line.lower() or 'ssg' in line.lower() or 'static' in line.lower() for line in lines)
        uses_layout = any('layout' in line.lower() or 'navigation' in line.lower() for line in lines)
        uses_error = any('error' in line.lower() or 'catch' in line.lower() for line in lines)
        uses_session = any('session' in line.lower() or 'auth' in line.lower() or 'user' in line.lower() for line in lines)
        uses_stores = any('store' in line.lower() or 'writable' in line.lower() for line in lines)
        
        # Detectar elementos de interfaz
        has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
        has_navigation = any('navegacion' in line.lower() or 'menu' in line.lower() or 'nav' in line.lower() for line in lines)
        
        # Generar múltiples archivos para SvelteKit
        files = {}
        
        # 1. Página principal (+page.svelte)
        page_code = []
        page_code.append("<script>")
        
        # Imports
        imports = []
        if uses_stores:
            imports.append("import { page } from '$app/stores';")
            imports.append("import { goto } from '$app/navigation';")
        if uses_session:
            imports.append("import { browser } from '$app/environment';")
        
        if imports:
            page_code.extend(imports)
            page_code.append("")
        
        # Props from load function
        if uses_ssr:
            page_code.append("  export let data;")
            page_code.append("")
        
        # Component state
        page_code.append("  let title = 'Aplicación SvelteKit desde Vader';")
        page_code.append("  let loading = false;")
        page_code.append("  let error = null;")
        
        if has_form:
            page_code.append("  let formData = { name: '', email: '', message: '' };")
        
        if has_list:
            page_code.append("  let items = data?.items || ['Item 1', 'Item 2', 'Item 3'];")
            page_code.append("  let newItem = '';")
        
        page_code.append("")
        
        # Functions
        if has_form:
            page_code.append("  async function handleSubmit() {")
            page_code.append("    loading = true;")
            page_code.append("    error = null;")
            page_code.append("    try {")
            page_code.append("      const response = await fetch('/api/submit', {")
            page_code.append("        method: 'POST',")
            page_code.append("        headers: { 'Content-Type': 'application/json' },")
            page_code.append("        body: JSON.stringify(formData)")
            page_code.append("      });")
            page_code.append("      if (!response.ok) throw new Error('Error en el envío');")
            page_code.append("      const result = await response.json();")
            page_code.append("      formData = { name: '', email: '', message: '' };")
            page_code.append("      alert('Formulario enviado exitosamente');")
            page_code.append("    } catch (err) {")
            page_code.append("      error = err.message;")
            page_code.append("    } finally {")
            page_code.append("      loading = false;")
            page_code.append("    }")
            page_code.append("  }")
            page_code.append("")
        
        if has_list:
            page_code.append("  function addItem() {")
            page_code.append("    if (newItem.trim()) {")
            page_code.append("      items = [...items, newItem.trim()];")
            page_code.append("      newItem = '';")
            page_code.append("    }")
            page_code.append("  }")
            page_code.append("")
            page_code.append("  function removeItem(index) {")
            page_code.append("    items = items.filter((_, i) => i !== index);")
            page_code.append("  }")
            page_code.append("")
        
        page_code.append("</script>")
        page_code.append("")
        
        # Head section
        page_code.append("<svelte:head>")
        page_code.append("  <title>{title}</title>")
        page_code.append("  <meta name='description' content='Aplicación SvelteKit generada desde código Vader' />")
        page_code.append("</svelte:head>")
        page_code.append("")
        
        # HTML Template
        page_code.append("<main class='sveltekit-app'>")
        page_code.append("  <header class='app-header'>")
        page_code.append("    <h1>{title}</h1>")
        
        if uses_session:
            page_code.append("    <div class='user-info'>")
            page_code.append("      {#if data?.user}")
            page_code.append("        <span>Bienvenido, {data.user.name}</span>")
            page_code.append("        <a href='/auth/logout'>Cerrar Sesión</a>")
            page_code.append("      {:else}")
            page_code.append("        <a href='/auth/login'>Iniciar Sesión</a>")
            page_code.append("      {/if}")
            page_code.append("    </div>")
        
        page_code.append("  </header>")
        page_code.append("")
        
        if has_navigation:
            page_code.append("  <nav class='app-nav'>")
            page_code.append("    <a href='/' class:active={$page.url.pathname === '/'}>Inicio</a>")
            page_code.append("    <a href='/about' class:active={$page.url.pathname === '/about'}>Acerca</a>")
            page_code.append("    <a href='/contact' class:active={$page.url.pathname === '/contact'}>Contacto</a>")
            page_code.append("  </nav>")
            page_code.append("")
        
        # Content sections
        if error:
            page_code.append("  {#if error}")
            page_code.append("    <div class='error'>Error: {error}</div>")
            page_code.append("  {/if}")
        
        if has_form:
            page_code.append("  <section class='form-section'>")
            page_code.append("    <h2>Formulario de Contacto</h2>")
            page_code.append("    <form on:submit|preventDefault={handleSubmit}>")
            page_code.append("      <input bind:value={formData.name} placeholder='Nombre' required />")
            page_code.append("      <input bind:value={formData.email} type='email' placeholder='Email' required />")
            page_code.append("      <textarea bind:value={formData.message} placeholder='Mensaje' required></textarea>")
            page_code.append("      <button type='submit' disabled={loading}>")
            page_code.append("        {loading ? 'Enviando...' : 'Enviar'}")
            page_code.append("      </button>")
            page_code.append("    </form>")
            page_code.append("  </section>")
        
        if has_list:
            page_code.append("  <section class='list-section'>")
            page_code.append("    <h2>Lista Dinámica</h2>")
            page_code.append("    <div class='add-item'>")
            page_code.append("      <input bind:value={newItem} placeholder='Nuevo elemento' />")
            page_code.append("      <button on:click={addItem}>Agregar</button>")
            page_code.append("    </div>")
            page_code.append("    <ul class='items-list'>")
            page_code.append("      {#each items as item, index}")
            page_code.append("        <li class='list-item'>")
            page_code.append("          <span>{item}</span>")
            page_code.append("          <button on:click={() => removeItem(index)}>&times;</button>")
            page_code.append("        </li>")
            page_code.append("      {/each}")
            page_code.append("    </ul>")
            page_code.append("  </section>")
        
        page_code.append("</main>")
        page_code.append("")
        
        # Styles
        page_code.append("<style>")
        page_code.append("  .sveltekit-app { max-width: 1200px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }")
        page_code.append("  .app-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #ff3e00; }")
        page_code.append("  .app-header h1 { color: #ff3e00; font-size: 2.5rem; margin: 0; }")
        page_code.append("  .user-info a { color: #ff3e00; text-decoration: none; font-weight: 500; }")
        page_code.append("  .app-nav { display: flex; gap: 20px; margin-bottom: 30px; }")
        page_code.append("  .app-nav a { color: #666; text-decoration: none; padding: 8px 16px; border-radius: 4px; transition: all 0.2s; }")
        page_code.append("  .app-nav a:hover, .app-nav a.active { background: #ff3e00; color: white; }")
        page_code.append("  .form-section, .list-section { margin: 30px 0; padding: 25px; border: 1px solid #e1e5e9; border-radius: 8px; background: white; }")
        page_code.append("  .form-section input, .form-section textarea { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }")
        page_code.append("  .form-section button { background: #ff3e00; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }")
        page_code.append("  .form-section button:disabled { background: #ccc; cursor: not-allowed; }")
        page_code.append("  .add-item { display: flex; gap: 10px; margin-bottom: 20px; }")
        page_code.append("  .add-item input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }")
        page_code.append("  .add-item button { background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }")
        page_code.append("  .items-list { list-style: none; padding: 0; }")
        page_code.append("  .list-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border: 1px solid #e9ecef; margin-bottom: 8px; border-radius: 6px; background: #f8f9fa; }")
        page_code.append("  .list-item button { background: #dc3545; color: white; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; }")
        page_code.append("  .error { color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; padding: 15px; margin: 15px 0; }")
        page_code.append("</style>")
        
        files['+page.svelte'] = '\n'.join(page_code)
        
        # 2. Load function (+page.js o +page.server.js)
        if uses_ssr:
            load_code = []
            load_code.append("import { error } from '@sveltejs/kit';")
            load_code.append("")
            load_code.append("export async function load({ fetch, params, url, route }) {")
            load_code.append("  try {")
            load_code.append("    // Server-side data loading")
            load_code.append("    const response = await fetch('/api/data');")
            load_code.append("    ")
            load_code.append("    if (!response.ok) {")
            load_code.append("      throw error(response.status, 'Failed to load data');")
            load_code.append("    }")
            load_code.append("    ")
            load_code.append("    const data = await response.json();")
            load_code.append("    ")
            load_code.append("    return {")
            load_code.append("      items: data.items || [],")
            load_code.append("      user: data.user || null,")
            load_code.append("      timestamp: new Date().toISOString()")
            load_code.append("    };")
            load_code.append("  } catch (err) {")
            load_code.append("    console.error('Load error:', err);")
            load_code.append("    return {")
            load_code.append("      items: [],")
            load_code.append("      user: null,")
            load_code.append("      error: err.message")
            load_code.append("    };")
            load_code.append("  }")
            load_code.append("}")
            
            if uses_prerender:
                load_code.append("")
                load_code.append("export const prerender = true;")
            
            files['+page.server.js'] = '\n'.join(load_code)
        
        # 3. API Route (+server.js)
        if uses_api:
            api_code = []
            api_code.append("import { json } from '@sveltejs/kit';")
            api_code.append("")
            api_code.append("// GET /api/data")
            api_code.append("export async function GET({ url, request }) {")
            api_code.append("  try {")
            api_code.append("    // Simulate database query")
            api_code.append("    const data = {")
            api_code.append("      items: ['API Item 1', 'API Item 2', 'API Item 3'],")
            api_code.append("      user: { id: 1, name: 'Usuario Vader', email: 'user@vader.com' },")
            api_code.append("      timestamp: new Date().toISOString()")
            api_code.append("    };")
            api_code.append("    ")
            api_code.append("    return json(data);")
            api_code.append("  } catch (error) {")
            api_code.append("    return json({ error: error.message }, { status: 500 });")
            api_code.append("  }")
            api_code.append("}")
            api_code.append("")
            api_code.append("// POST /api/submit")
            api_code.append("export async function POST({ request }) {")
            api_code.append("  try {")
            api_code.append("    const formData = await request.json();")
            api_code.append("    ")
            api_code.append("    // Validate form data")
            api_code.append("    if (!formData.name || !formData.email) {")
            api_code.append("      return json({ error: 'Name and email are required' }, { status: 400 });")
            api_code.append("    }")
            api_code.append("    ")
            api_code.append("    // Simulate form processing")
            api_code.append("    console.log('Form submitted:', formData);")
            api_code.append("    ")
            api_code.append("    return json({ ")
            api_code.append("      success: true, ")
            api_code.append("      message: 'Form submitted successfully',")
            api_code.append("      id: Math.random().toString(36).substr(2, 9)")
            api_code.append("    });")
            api_code.append("  } catch (error) {")
            api_code.append("    return json({ error: error.message }, { status: 500 });")
            api_code.append("  }")
            api_code.append("}")
            
            files['api/+server.js'] = '\n'.join(api_code)
        
        # 4. Layout (+layout.svelte)
        if uses_layout:
            layout_code = []
            layout_code.append("<script>")
            layout_code.append("  import { page } from '$app/stores';")
            layout_code.append("  import { onMount } from 'svelte';")
            layout_code.append("  ")
            layout_code.append("  let mounted = false;")
            layout_code.append("  ")
            layout_code.append("  onMount(() => {")
            layout_code.append("    mounted = true;")
            layout_code.append("  });")
            layout_code.append("</script>")
            layout_code.append("")
            layout_code.append("<svelte:head>")
            layout_code.append("  <meta charset='utf-8' />")
            layout_code.append("  <meta name='viewport' content='width=device-width, initial-scale=1' />")
            layout_code.append("</svelte:head>")
            layout_code.append("")
            layout_code.append("<div class='app-layout'>")
            layout_code.append("  <header class='global-header'>")
            layout_code.append("    <nav class='global-nav'>")
            layout_code.append("      <a href='/' class:active={$page.url.pathname === '/'}>Vader App</a>")
            layout_code.append("      <div class='nav-links'>")
            layout_code.append("        <a href='/about' class:active={$page.url.pathname === '/about'}>Acerca</a>")
            layout_code.append("        <a href='/contact' class:active={$page.url.pathname === '/contact'}>Contacto</a>")
            layout_code.append("      </div>")
            layout_code.append("    </nav>")
            layout_code.append("  </header>")
            layout_code.append("  ")
            layout_code.append("  <main class='main-content'>")
            layout_code.append("    <slot />")
            layout_code.append("  </main>")
            layout_code.append("  ")
            layout_code.append("  <footer class='global-footer'>")
            layout_code.append("    <p>&copy; 2024 Vader SvelteKit App. Generado automáticamente.</p>")
            layout_code.append("  </footer>")
            layout_code.append("</div>")
            layout_code.append("")
            layout_code.append("<style>")
            layout_code.append("  .app-layout { min-height: 100vh; display: flex; flex-direction: column; }")
            layout_code.append("  .global-header { background: #ff3e00; color: white; padding: 1rem 0; }")
            layout_code.append("  .global-nav { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }")
            layout_code.append("  .global-nav a { color: white; text-decoration: none; font-weight: 600; }")
            layout_code.append("  .nav-links { display: flex; gap: 20px; }")
            layout_code.append("  .nav-links a { padding: 8px 16px; border-radius: 4px; transition: background 0.2s; }")
            layout_code.append("  .nav-links a:hover, .nav-links a.active { background: rgba(255,255,255,0.2); }")
            layout_code.append("  .main-content { flex: 1; }")
            layout_code.append("  .global-footer { background: #f8f9fa; text-align: center; padding: 20px; border-top: 1px solid #e9ecef; }")
            layout_code.append("</style>")
            
            files['+layout.svelte'] = '\n'.join(layout_code)
        
        # 5. Error page (+error.svelte)
        if uses_error:
            error_code = []
            error_code.append("<script>")
            error_code.append("  import { page } from '$app/stores';")
            error_code.append("</script>")
            error_code.append("")
            error_code.append("<svelte:head>")
            error_code.append("  <title>Error {$page.error?.status || 500}</title>")
            error_code.append("</svelte:head>")
            error_code.append("")
            error_code.append("<div class='error-page'>")
            error_code.append("  <h1>Error {$page.error?.status || 500}</h1>")
            error_code.append("  <p>{$page.error?.message || 'Ha ocurrido un error inesperado'}</p>")
            error_code.append("  <a href='/'>Volver al inicio</a>")
            error_code.append("</div>")
            error_code.append("")
            error_code.append("<style>")
            error_code.append("  .error-page { text-align: center; padding: 100px 20px; }")
            error_code.append("  .error-page h1 { color: #dc3545; font-size: 4rem; margin: 0; }")
            error_code.append("  .error-page p { font-size: 1.2rem; margin: 20px 0; }")
            error_code.append("  .error-page a { color: #ff3e00; text-decoration: none; font-weight: 600; }")
            error_code.append("</style>")
            
            files['+error.svelte'] = '\n'.join(error_code)
        
        # Retornar el archivo principal o todos los archivos
        if len(files) == 1:
            return list(files.values())[0]
        else:
            # Retornar estructura de archivos como comentarios
            result = ["<!-- SvelteKit App Structure -->"]
            for filename, content in files.items():
                result.append(f"<!-- File: {filename} -->")
                result.append(content)
                result.append("")
            return '\n'.join(result)
