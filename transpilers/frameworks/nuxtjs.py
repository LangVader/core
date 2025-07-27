"""
Framework Nuxt.js para Vader
"""

class NuxtJSFramework:
    def __init__(self):
        self.name = "Nuxt.js"
        self.description = "Framework Vue.js completo con SSR, SSG, SPA y funcionalidades avanzadas"
        self.target_language = "javascript"
        self.keywords = [
            'nuxt', 'nuxtjs', 'universal', 'ssr', 'ssg', 'spa', 'static',
            'server', 'asyncData', 'fetch', 'middleware', 'layout', 'plugin',
            'store', 'vuex', 'pinia', 'auth', 'session', 'cookie', 'meta',
            'head', 'router', 'dynamic', 'lazy', 'generate', 'build',
            'nitro', 'serverless', 'edge', 'composition', 'auto-import'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Nuxt.js con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_ssr = any('ssr' in line.lower() or 'asyncData' in line.lower() or 'server' in line.lower() for line in lines)
        uses_auth = any('auth' in line.lower() or 'session' in line.lower() or 'login' in line.lower() for line in lines)
        uses_meta = any('meta' in line.lower() or 'head' in line.lower() or 'title' in line.lower() for line in lines)
        uses_router = any('router' in line.lower() or 'navegacion' in line.lower() or 'ruta' in line.lower() for line in lines)
        uses_fetch = any('fetch' in line.lower() or 'api' in line.lower() for line in lines)
        uses_store = any('store' in line.lower() or 'vuex' in line.lower() or 'pinia' in line.lower() for line in lines)
        
        # Detectar elementos de interfaz
        has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
        
        # Construir código Nuxt.js
        nuxt_code = []
        
        # Template
        nuxt_code.append("<template>")
        nuxt_code.append("  <div class='vader-container'>")
        nuxt_code.append("    <header class='vader-header'>")
        nuxt_code.append("      <h1>{{ title }}</h1>")
        
        if uses_auth:
            nuxt_code.append("      <div v-if='$auth.loggedIn' class='user-info'>")
            nuxt_code.append("        <span>Bienvenido, {{ $auth.user.name }}</span>")
            nuxt_code.append("        <button @click='logout'>Cerrar Sesión</button>")
            nuxt_code.append("      </div>")
            nuxt_code.append("      <button v-else @click='login'>Iniciar Sesión</button>")
        
        nuxt_code.append("    </header>")
        
        if uses_router:
            nuxt_code.append("    <nav class='vader-nav'>")
            nuxt_code.append("      <NuxtLink to='/' active-class='active'>Inicio</NuxtLink>")
            nuxt_code.append("      <NuxtLink to='/about' active-class='active'>Acerca</NuxtLink>")
            nuxt_code.append("    </nav>")
        
        nuxt_code.append("    <main class='vader-main'>")
        nuxt_code.append("      <div v-if='$fetchState.pending'>Cargando...</div>")
        nuxt_code.append("      <div v-else-if='$fetchState.error' class='error'>Error: {{ $fetchState.error.message }}</div>")
        nuxt_code.append("      <div v-else>")
        
        if has_form:
            nuxt_code.append("        <form @submit.prevent='handleSubmit' class='vader-form'>")
            nuxt_code.append("          <input v-model='formData.name' placeholder='Nombre' required />")
            nuxt_code.append("          <input v-model='formData.email' type='email' placeholder='Email' required />")
            nuxt_code.append("          <button type='submit' :disabled='loading'>{{ loading ? 'Enviando...' : 'Enviar' }}</button>")
            nuxt_code.append("        </form>")
        
        if has_list:
            nuxt_code.append("        <ul v-if='data.length > 0' class='vader-list'>")
            nuxt_code.append("          <li v-for='(item, index) in data' :key='index' class='list-item'>")
            nuxt_code.append("            <span>{{ item.name || item }}</span>")
            nuxt_code.append("            <button @click='removeItem(index)'>&times;</button>")
            nuxt_code.append("          </li>")
            nuxt_code.append("        </ul>")
            nuxt_code.append("        <p v-else>No hay elementos para mostrar</p>")
        
        if uses_store:
            nuxt_code.append("        <div class='store-section'>")
            nuxt_code.append("          <p>Contador: {{ $store.state.counter }}</p>")
            nuxt_code.append("          <button @click='$store.commit(\"increment\")'>+</button>")
            nuxt_code.append("          <button @click='$store.commit(\"decrement\")'>-</button>")
            nuxt_code.append("        </div>")
        
        nuxt_code.append("      </div>")
        nuxt_code.append("    </main>")
        nuxt_code.append("  </div>")
        nuxt_code.append("</template>")
        nuxt_code.append("")
        
        # Script
        nuxt_code.append("<script>")
        nuxt_code.append("export default {")
        nuxt_code.append("  name: 'VaderPage',")
        
        if uses_meta:
            nuxt_code.append("  head() {")
            nuxt_code.append("    return {")
            nuxt_code.append("      title: 'Vader Nuxt.js App',")
            nuxt_code.append("      meta: [{ name: 'description', content: 'Aplicación generada desde código Vader' }]")
            nuxt_code.append("    };")
            nuxt_code.append("  },")
        
        nuxt_code.append("  data() {")
        nuxt_code.append("    return {")
        nuxt_code.append("      data: [],")
        nuxt_code.append("      loading: false,")
        nuxt_code.append("      error: null,")
        if has_form:
            nuxt_code.append("      formData: { name: '', email: '' },")
        nuxt_code.append("    };")
        nuxt_code.append("  },")
        
        nuxt_code.append("  computed: {")
        nuxt_code.append("    title() {")
        nuxt_code.append("      return this.loading ? 'Cargando...' : 'Aplicación Nuxt.js desde Vader';")
        nuxt_code.append("    }")
        nuxt_code.append("  },")
        
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
            nuxt_code.append("      await this.$auth.loginWith('local');")
            nuxt_code.append("    },")
            nuxt_code.append("    async logout() {")
            nuxt_code.append("      await this.$auth.logout();")
            nuxt_code.append("    },")
        
        nuxt_code.append("  }")
        
        if uses_ssr:
            nuxt_code.append(",")
            nuxt_code.append("  async asyncData({ $axios }) {")
            nuxt_code.append("    try {")
            nuxt_code.append("      const { data } = await $axios.get('/api/data');")
            nuxt_code.append("      return { data: data.data || [] };")
            nuxt_code.append("    } catch (err) {")
            nuxt_code.append("      return { data: [] };")
            nuxt_code.append("    }")
            nuxt_code.append("  }")
        
        if uses_fetch:
            nuxt_code.append(",")
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
        nuxt_code.append(".vader-container { max-width: 1200px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }")
        nuxt_code.append(".vader-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #e5e7eb; }")
        nuxt_code.append(".vader-nav { display: flex; gap: 20px; margin-bottom: 30px; }")
        nuxt_code.append(".vader-nav a { color: #10b981; text-decoration: none; font-weight: 500; padding: 8px 16px; border-radius: 4px; transition: all 0.2s; }")
        nuxt_code.append(".vader-nav a:hover { background-color: #f3f4f6; }")
        nuxt_code.append(".vader-nav a.active { background-color: #10b981; color: white; }")
        nuxt_code.append(".vader-form { max-width: 500px; margin: 20px 0; }")
        nuxt_code.append(".vader-form input { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 16px; }")
        nuxt_code.append(".vader-form button { background-color: #10b981; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }")
        nuxt_code.append(".vader-form button:hover { background-color: #059669; }")
        nuxt_code.append(".vader-form button:disabled { background-color: #9ca3af; cursor: not-allowed; }")
        nuxt_code.append(".vader-list { list-style: none; padding: 0; }")
        nuxt_code.append(".list-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border: 1px solid #e5e7eb; margin-bottom: 8px; border-radius: 6px; background-color: #f9fafb; }")
        nuxt_code.append(".list-item button { background: #ef4444; color: white; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; }")
        nuxt_code.append(".error { color: #e00; background-color: #fee; border: 1px solid #fcc; border-radius: 4px; padding: 15px; margin: 15px 0; }")
        nuxt_code.append("</style>")
        
        return '\n'.join(nuxt_code)
