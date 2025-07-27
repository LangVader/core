"""
Implementación completa del método transpile para Nuxt.js
"""

def transpile_nuxt_complete(vader_code):
    """Transpila código Vader a Nuxt.js con funcionalidades avanzadas"""
    lines = vader_code.strip().split('\n')
    
    # Detectar funcionalidades avanzadas
    uses_ssr = any('ssr' in line.lower() or 'asyncData' in line.lower() or 'server' in line.lower() for line in lines)
    uses_ssg = any('ssg' in line.lower() or 'generate' in line.lower() or 'static' in line.lower() for line in lines)
    uses_composition = any('composition' in line.lower() or 'setup' in line.lower() for line in lines)
    uses_store = any('store' in line.lower() or 'vuex' in line.lower() or 'pinia' in line.lower() for line in lines)
    uses_auth = any('auth' in line.lower() or 'session' in line.lower() or 'login' in line.lower() for line in lines)
    uses_meta = any('meta' in line.lower() or 'head' in line.lower() or 'title' in line.lower() for line in lines)
    uses_router = any('router' in line.lower() or 'navegacion' in line.lower() or 'ruta' in line.lower() for line in lines)
    uses_fetch = any('fetch' in line.lower() or 'api' in line.lower() for line in lines)
    
    # Detectar elementos de interfaz
    has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
    has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
    
    # Detectar nombre de página/componente
    page_name = "VaderPage"
    for line in lines:
        if 'pagina' in line.lower() or 'page' in line.lower():
            parts = line.split()
            if len(parts) > 1:
                page_name = parts[1].capitalize() + "Page"
            break
    
    # Construir código Nuxt.js
    nuxt_code = []
    
    # Template
    nuxt_code.append("<template>")
    nuxt_code.append("  <div class='vader-container'>")
    nuxt_code.append("    <header class='vader-header'>")
    nuxt_code.append("      <h1>{{ title }}</h1>")
    
    # Autenticación en header
    if uses_auth:
        nuxt_code.append("      <div class='auth-section'>")
        nuxt_code.append("        <div v-if='$auth.loggedIn' class='user-info'>")
        nuxt_code.append("          <span>Bienvenido, {{ $auth.user.name }}</span>")
        nuxt_code.append("          <button @click='logout' class='auth-btn'>Cerrar Sesión</button>")
        nuxt_code.append("        </div>")
        nuxt_code.append("        <div v-else>")
        nuxt_code.append("          <button @click='login' class='auth-btn'>Iniciar Sesión</button>")
        nuxt_code.append("        </div>")
        nuxt_code.append("      </div>")
    
    nuxt_code.append("    </header>")
    
    # Navegación
    if uses_router:
        nuxt_code.append("    <nav class='vader-nav'>")
        nuxt_code.append("      <NuxtLink to='/' class='nav-link' active-class='active'>Inicio</NuxtLink>")
        nuxt_code.append("      <NuxtLink to='/about' class='nav-link' active-class='active'>Acerca</NuxtLink>")
        nuxt_code.append("      <NuxtLink to='/contact' class='nav-link' active-class='active'>Contacto</NuxtLink>")
        nuxt_code.append("    </nav>")
    
    # Main content
    nuxt_code.append("    <main class='vader-main'>")
    nuxt_code.append("      <div v-if='$fetchState.pending' class='loading'>Cargando...</div>")
    nuxt_code.append("      <div v-else-if='$fetchState.error' class='error'>")
    nuxt_code.append("        Error: {{ $fetchState.error.message }}")
    nuxt_code.append("      </div>")
    nuxt_code.append("      <div v-else>")
    
    # Formulario si se detecta
    if has_form:
        nuxt_code.append("        <section class='vader-form-section'>")
        nuxt_code.append("          <h2>Formulario de Contacto</h2>")
        nuxt_code.append("          <form @submit.prevent='handleSubmit' class='vader-form'>")
        nuxt_code.append("            <div class='form-group'>")
        nuxt_code.append("              <label for='name'>Nombre:</label>")
        nuxt_code.append("              <input v-model='formData.name' type='text' id='name' required class='form-input' />")
        nuxt_code.append("            </div>")
        nuxt_code.append("            <div class='form-group'>")
        nuxt_code.append("              <label for='email'>Email:</label>")
        nuxt_code.append("              <input v-model='formData.email' type='email' id='email' required class='form-input' />")
        nuxt_code.append("            </div>")
        nuxt_code.append("            <button type='submit' :disabled='loading' class='submit-btn'>")
        nuxt_code.append("              {{ loading ? 'Enviando...' : 'Enviar' }}")
        nuxt_code.append("            </button>")
        nuxt_code.append("          </form>")
        nuxt_code.append("        </section>")
    
    # Lista si se detecta
    if has_list:
        nuxt_code.append("        <section class='vader-list-section'>")
        nuxt_code.append("          <h2>Lista de Elementos</h2>")
        nuxt_code.append("          <div v-if='data.length > 0'>")
        nuxt_code.append("            <TransitionGroup name='list' tag='ul' class='vader-list'>")
        nuxt_code.append("              <li v-for='(item, index) in data' :key='item.id || index' class='list-item'>")
        nuxt_code.append("                <span>{{ item.name || item }}</span>")
        nuxt_code.append("                <button @click='removeItem(index)' class='remove-btn'>&times;</button>")
        nuxt_code.append("              </li>")
        nuxt_code.append("            </TransitionGroup>")
        nuxt_code.append("          </div>")
        nuxt_code.append("          <div v-else class='empty-state'>No hay elementos para mostrar</div>")
        nuxt_code.append("        </section>")
    
    # Store data si se usa
    if uses_store:
        nuxt_code.append("        <section class='vader-store-section'>")
        nuxt_code.append("          <h2>Estado Global</h2>")
        nuxt_code.append("          <p>Contador: {{ $store.state.counter }}</p>")
        nuxt_code.append("          <button @click='$store.commit(\"increment\")' class='counter-btn'>+</button>")
        nuxt_code.append("          <button @click='$store.commit(\"decrement\")' class='counter-btn'>-</button>")
        nuxt_code.append("        </section>")
    
    nuxt_code.append("      </div>")
    nuxt_code.append("    </main>")
    nuxt_code.append("  </div>")
    nuxt_code.append("</template>")
    nuxt_code.append("")
    
    # Script - Options API
    nuxt_code.append("<script>")
    nuxt_code.append("export default {")
    nuxt_code.append(f"  name: '{page_name}',")
    
    # Meta tags
    if uses_meta:
        nuxt_code.append("  head() {")
        nuxt_code.append("    return {")
        nuxt_code.append("      title: 'Vader Nuxt.js App',")
        nuxt_code.append("      meta: [")
        nuxt_code.append("        { name: 'description', content: 'Aplicación generada desde código Vader' },")
        nuxt_code.append("        { property: 'og:title', content: 'Vader Nuxt.js App' }")
        nuxt_code.append("      ]")
        nuxt_code.append("    };")
        nuxt_code.append("  },")
    
    # Data
    nuxt_code.append("  data() {")
    nuxt_code.append("    return {")
    nuxt_code.append("      data: [],")
    nuxt_code.append("      loading: false,")
    nuxt_code.append("      error: null,")
    if has_form:
        nuxt_code.append("      formData: { name: '', email: '' },")
    nuxt_code.append("    };")
    nuxt_code.append("  },")
    
    # Computed
    nuxt_code.append("  computed: {")
    nuxt_code.append("    title() {")
    nuxt_code.append("      return this.loading ? 'Cargando...' : 'Aplicación Nuxt.js desde Vader';")
    nuxt_code.append("    }")
    nuxt_code.append("  },")
    
    # Methods
    nuxt_code.append("  methods: {")
    if has_form:
        nuxt_code.append("    async handleSubmit() {")
        nuxt_code.append("      this.loading = true;")
        nuxt_code.append("      try {")
        nuxt_code.append("        await this.$axios.post('/api/submit', this.formData);")
        nuxt_code.append("        this.formData = { name: '', email: '' };")
        nuxt_code.append("        this.$toast.success('Formulario enviado exitosamente');")
        nuxt_code.append("      } catch (err) {")
        nuxt_code.append("        this.error = err.message;")
        nuxt_code.append("        this.$toast.error('Error al enviar formulario');")
        nuxt_code.append("      } finally {")
        nuxt_code.append("        this.loading = false;")
        nuxt_code.append("      }")
        nuxt_code.append("    },")
    
    if has_list:
        nuxt_code.append("    removeItem(index) {")
        nuxt_code.append("      this.data.splice(index, 1);")
        nuxt_code.append("    },")
    
    if uses_auth:
        nuxt_code.append("    async login() {")
        nuxt_code.append("      try {")
        nuxt_code.append("        await this.$auth.loginWith('local');")
        nuxt_code.append("      } catch (err) {")
        nuxt_code.append("        this.$toast.error('Error en login');")
        nuxt_code.append("      }")
        nuxt_code.append("    },")
        nuxt_code.append("    async logout() {")
        nuxt_code.append("      await this.$auth.logout();")
        nuxt_code.append("    },")
    
    nuxt_code.append("  }")
    
    # Lifecycle hooks para SSR/SSG
    if uses_ssr:
        nuxt_code.append(",")
        nuxt_code.append("  // Server-Side Rendering")
        nuxt_code.append("  async asyncData({ $axios, params, error }) {")
        nuxt_code.append("    try {")
        nuxt_code.append("      const { data } = await $axios.get('/api/data');")
        nuxt_code.append("      return { data: data.data || [] };")
        nuxt_code.append("    } catch (err) {")
        nuxt_code.append("      error({ statusCode: 500, message: 'Error al cargar datos' });")
        nuxt_code.append("    }")
        nuxt_code.append("  }")
    
    if uses_fetch:
        nuxt_code.append(",")
        nuxt_code.append("  // Fetch hook")
        nuxt_code.append("  async fetch() {")
        nuxt_code.append("    try {")
        nuxt_code.append("      const { data } = await this.$axios.get('/api/data');")
        nuxt_code.append("      this.data = data.data || [];")
        nuxt_code.append("    } catch (err) {")
        nuxt_code.append("      this.error = err.message;")
        nuxt_code.append("    }")
        nuxt_code.append("  }")
    
    nuxt_code.append("};")
    nuxt_code.append("</script>")
    nuxt_code.append("")
    
    # Estilos
    nuxt_code.append("<style scoped>")
    nuxt_code.append(".vader-container { max-width: 1200px; margin: 0 auto; padding: 20px; }")
    nuxt_code.append(".vader-header { display: flex; justify-content: space-between; margin-bottom: 30px; }")
    nuxt_code.append(".vader-nav { display: flex; gap: 20px; margin-bottom: 30px; }")
    nuxt_code.append(".nav-link { color: #10b981; text-decoration: none; font-weight: 500; }")
    nuxt_code.append(".nav-link.active { background-color: #10b981; color: white; padding: 8px 16px; border-radius: 4px; }")
    nuxt_code.append(".vader-form { max-width: 500px; margin: 20px 0; }")
    nuxt_code.append(".form-group { margin-bottom: 15px; }")
    nuxt_code.append(".form-input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }")
    nuxt_code.append(".submit-btn { background: #10b981; color: white; padding: 12px 24px; border: none; border-radius: 4px; }")
    nuxt_code.append(".vader-list { list-style: none; padding: 0; }")
    nuxt_code.append(".list-item { display: flex; justify-content: space-between; padding: 12px; border: 1px solid #eee; margin-bottom: 8px; border-radius: 4px; }")
    nuxt_code.append(".remove-btn { background: #ef4444; color: white; border: none; border-radius: 50%; width: 28px; height: 28px; }")
    nuxt_code.append(".loading, .error { text-align: center; padding: 20px; margin: 20px 0; }")
    nuxt_code.append(".error { color: #e00; background: #fee; border: 1px solid #fcc; border-radius: 4px; }")
    nuxt_code.append("</style>")
    
    return '\n'.join(nuxt_code)
