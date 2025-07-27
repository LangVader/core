"""
Framework Vue.js para Vader
"""

class VueFramework:
    def __init__(self):
        self.name = "Vue.js"
        self.description = "Framework progresivo completo para interfaces de usuario"
        self.target_language = "javascript"
        self.keywords = [
            'vue', 'componente', 'reactivo', 'template', 'composition', 'setup',
            'ref', 'reactive', 'computed', 'watch', 'router', 'ruta', 'navegacion',
            'store', 'vuex', 'pinia', 'estado', 'mutacion', 'accion', 'getter',
            'slot', 'directiva', 'v-model', 'v-if', 'v-for', 'emit', 'props'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Vue.js con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_composition = any('composition' in line.lower() or 'setup' in line.lower() for line in lines)
        uses_router = any('router' in line.lower() or 'ruta' in line.lower() or 'navegacion' in line.lower() for line in lines)
        uses_store = any('store' in line.lower() or 'vuex' in line.lower() or 'pinia' in line.lower() for line in lines)
        uses_computed = any('computed' in line.lower() or 'calculado' in line.lower() for line in lines)
        uses_watch = any('watch' in line.lower() or 'observar' in line.lower() for line in lines)
        
        # Detectar componente
        component_name = "VaderComponent"
        for line in lines:
            if 'componente' in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    component_name = parts[1].capitalize()
                break
        
        # Detectar elementos de interfaz
        has_input = any('pedir' in line.lower() or 'input' in line.lower() for line in lines)
        has_button = any('boton' in line.lower() or 'button' in line.lower() for line in lines)
        has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
        
        # Construir template
        template_code = []
        template_code.append("<template>")
        template_code.append("  <div class='vader-component'>")
        template_code.append("    <h1>{{ title }}</h1>")
        
        # Formulario si se detecta
        if has_form or has_input or has_button:
            template_code.append("    <form @submit.prevent='handleSubmit' class='vader-form'>")
            
            if has_input:
                template_code.append("      <div class='form-group'>")
                template_code.append("        <label for='userInput'>Entrada:</label>")
                template_code.append("        <input")
                template_code.append("          id='userInput'")
                template_code.append("          v-model='formData.input'")
                template_code.append("          type='text'")
                template_code.append("          placeholder='Ingresa texto'")
                template_code.append("          class='vader-input'")
                template_code.append("          :disabled='loading'")
                template_code.append("        />")
                template_code.append("      </div>")
            
            if has_button:
                template_code.append("      <button")
                template_code.append("        type='submit'")
                template_code.append("        :disabled='loading || !isFormValid'")
                template_code.append("        class='vader-button'")
                template_code.append("      >")
                template_code.append("        {{ loading ? 'Cargando...' : 'Enviar' }}")
                template_code.append("      </button>")
            
            template_code.append("    </form>")
        
        # Lista si se detecta
        if has_list:
            template_code.append("    <div class='vader-list'>")
            template_code.append("      <h3>Lista de elementos:</h3>")
            template_code.append("      <ul>")
            template_code.append("        <li v-for='(item, index) in items' :key='index' class='list-item'>")
            template_code.append("          {{ item }}")
            template_code.append("          <button @click='removeItem(index)' class='remove-btn'>×</button>")
            template_code.append("        </li>")
            template_code.append("      </ul>")
            template_code.append("      <div v-if='items.length === 0' class='empty-state'>")
            template_code.append("        No hay elementos en la lista")
            template_code.append("      </div>")
            template_code.append("    </div>")
        
        # Estado y resultados
        template_code.append("    <div class='vader-status'>")
        template_code.append("      <p>Estado: {{ computedStatus }}</p>")
        template_code.append("      <p v-if='result'>Resultado: {{ result }}</p>")
        template_code.append("      <p v-if='error' class='error'>Error: {{ error }}</p>")
        template_code.append("    </div>")
        
        # Router navigation si se usa
        if uses_router:
            template_code.append("    <nav class='vader-nav'>")
            template_code.append("      <router-link to='/'>Inicio</router-link>")
            template_code.append("      <router-link to='/about'>Acerca</router-link>")
            template_code.append("      <button @click='navigateToPage' class='nav-button'>Navegar</button>")
            template_code.append("    </nav>")
        
        template_code.append("  </div>")
        template_code.append("</template>")
        
        # Construir script
        script_code = []
        script_code.append("")
        script_code.append("<script>")
        
        # Imports
        if uses_composition:
            imports = ["import { ref, reactive, computed, watch, onMounted, onUnmounted"]
            if uses_store:
                imports.append(", inject")
            imports.append(" } from 'vue'")
            if uses_router:
                script_code.append("import { useRouter, useRoute } from 'vue-router'")
            if uses_store:
                script_code.append("import { useStore } from 'vuex' // o 'pinia'")
            script_code.append(''.join(imports))
            script_code.append("")
        
        # Composition API o Options API
        if uses_composition:
            script_code.append("export default {")
            script_code.append(f"  name: '{component_name}',")
            script_code.append("  setup() {")
            
            # Router y Store en Composition API
            if uses_router:
                script_code.append("    const router = useRouter()")
                script_code.append("    const route = useRoute()")
            
            if uses_store:
                script_code.append("    const store = useStore()")
            
            # Estado reactivo
            script_code.append("    // Estado reactivo")
            script_code.append("    const title = ref('Componente Vue Avanzado')")
            script_code.append("    const loading = ref(false)")
            script_code.append("    const error = ref(null)")
            script_code.append("    const result = ref('')")
            script_code.append("    const formData = reactive({")
            script_code.append("      input: ''")
            script_code.append("    })")
            
            if has_list:
                script_code.append("    const items = ref(['Elemento 1', 'Elemento 2', 'Elemento 3'])")
            
            script_code.append("")
            
            # Computed properties
            script_code.append("    // Propiedades computadas")
            script_code.append("    const computedStatus = computed(() => {")
            script_code.append("      if (loading.value) return 'Cargando...'")
            script_code.append("      if (error.value) return 'Error'")
            script_code.append("      return formData.input ? formData.input.toUpperCase() : 'Sin datos'")
            script_code.append("    })")
            
            script_code.append("    const isFormValid = computed(() => {")
            script_code.append("      return formData.input.length > 0")
            script_code.append("    })")
            script_code.append("")
            
            # Watchers
            if uses_watch:
                script_code.append("    // Watchers")
                script_code.append("    watch(() => formData.input, (newValue, oldValue) => {")
                script_code.append("      console.log('Input cambió:', { newValue, oldValue })")
                script_code.append("      if (newValue.length > 10) {")
                script_code.append("        error.value = 'Texto demasiado largo'")
                script_code.append("      } else {")
                script_code.append("        error.value = null")
                script_code.append("      }")
                script_code.append("    })")
                script_code.append("")
            
            # Métodos
            script_code.append("    // Métodos")
            script_code.append("    const handleSubmit = async () => {")
            script_code.append("      loading.value = true")
            script_code.append("      error.value = null")
            script_code.append("      ")
            script_code.append("      try {")
            script_code.append("        // Simular operación async")
            script_code.append("        await new Promise(resolve => setTimeout(resolve, 1000))")
            script_code.append("        result.value = `Procesado: ${formData.input}`")
            
            if uses_store:
                script_code.append("        // Actualizar store")
                script_code.append("        store.commit('updateData', formData.input)")
            
            script_code.append("      } catch (err) {")
            script_code.append("        error.value = err.message")
            script_code.append("      } finally {")
            script_code.append("        loading.value = false")
            script_code.append("      }")
            script_code.append("    }")
            script_code.append("")
            
            if has_list:
                script_code.append("    const removeItem = (index) => {")
                script_code.append("      items.value.splice(index, 1)")
                script_code.append("    }")
                script_code.append("")
            
            if uses_router:
                script_code.append("    const navigateToPage = () => {")
                script_code.append("      router.push('/about')")
                script_code.append("    }")
                script_code.append("")
            
            # Lifecycle hooks
            script_code.append("    // Lifecycle hooks")
            script_code.append("    onMounted(() => {")
            script_code.append("      console.log('Componente montado')")
            script_code.append("    })")
            script_code.append("")
            script_code.append("    onUnmounted(() => {")
            script_code.append("      console.log('Componente desmontado')")
            script_code.append("    })")
            script_code.append("")
            
            # Return para Composition API
            script_code.append("    return {")
            script_code.append("      title,")
            script_code.append("      loading,")
            script_code.append("      error,")
            script_code.append("      result,")
            script_code.append("      formData,")
            script_code.append("      computedStatus,")
            script_code.append("      isFormValid,")
            script_code.append("      handleSubmit,")
            
            if has_list:
                script_code.append("      items,")
                script_code.append("      removeItem,")
            
            if uses_router:
                script_code.append("      navigateToPage,")
            
            script_code.append("    }")
            script_code.append("  }")
            script_code.append("}")
        
        else:
            # Options API
            script_code.append("export default {")
            script_code.append(f"  name: '{component_name}',")
            
            # Data
            script_code.append("  data() {")
            script_code.append("    return {")
            script_code.append("      title: 'Componente Vue Avanzado',")
            script_code.append("      loading: false,")
            script_code.append("      error: null,")
            script_code.append("      result: '',")
            script_code.append("      formData: {")
            script_code.append("        input: ''")
            script_code.append("      },")
            
            if has_list:
                script_code.append("      items: ['Elemento 1', 'Elemento 2', 'Elemento 3']")
            
            script_code.append("    }")
            script_code.append("  },")
            script_code.append("")
            
            # Computed
            script_code.append("  computed: {")
            script_code.append("    computedStatus() {")
            script_code.append("      if (this.loading) return 'Cargando...'")
            script_code.append("      if (this.error) return 'Error'")
            script_code.append("      return this.formData.input ? this.formData.input.toUpperCase() : 'Sin datos'")
            script_code.append("    },")
            script_code.append("    isFormValid() {")
            script_code.append("      return this.formData.input.length > 0")
            script_code.append("    }")
            script_code.append("  },")
            script_code.append("")
            
            # Watch
            if uses_watch:
                script_code.append("  watch: {")
                script_code.append("    'formData.input'(newValue, oldValue) {")
                script_code.append("      console.log('Input cambió:', { newValue, oldValue })")
                script_code.append("      if (newValue.length > 10) {")
                script_code.append("        this.error = 'Texto demasiado largo'")
                script_code.append("      } else {")
                script_code.append("        this.error = null")
                script_code.append("      }")
                script_code.append("    }")
                script_code.append("  },")
                script_code.append("")
            
            # Methods
            script_code.append("  methods: {")
            script_code.append("    async handleSubmit() {")
            script_code.append("      this.loading = true")
            script_code.append("      this.error = null")
            script_code.append("      ")
            script_code.append("      try {")
            script_code.append("        await new Promise(resolve => setTimeout(resolve, 1000))")
            script_code.append("        this.result = `Procesado: ${this.formData.input}`")
            
            if uses_store:
                script_code.append("        this.$store.commit('updateData', this.formData.input)")
            
            script_code.append("      } catch (err) {")
            script_code.append("        this.error = err.message")
            script_code.append("      } finally {")
            script_code.append("        this.loading = false")
            script_code.append("      }")
            script_code.append("    },")
            
            if has_list:
                script_code.append("    removeItem(index) {")
                script_code.append("      this.items.splice(index, 1)")
                script_code.append("    },")
            
            if uses_router:
                script_code.append("    navigateToPage() {")
                script_code.append("      this.$router.push('/about')")
                script_code.append("    },")
            
            script_code.append("  },")
            script_code.append("")
            
            # Lifecycle
            script_code.append("  mounted() {")
            script_code.append("    console.log('Componente montado')")
            script_code.append("  },")
            script_code.append("")
            script_code.append("  beforeUnmount() {")
            script_code.append("    console.log('Componente desmontado')")
            script_code.append("  }")
            script_code.append("}")
        
        script_code.append("</script>")
        
        # Estilos
        style_code = []
        style_code.append("")
        style_code.append("<style scoped>")
        style_code.append(".vader-component {")
        style_code.append("  max-width: 600px;")
        style_code.append("  margin: 0 auto;")
        style_code.append("  padding: 20px;")
        style_code.append("  font-family: Arial, sans-serif;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-form {")
        style_code.append("  margin: 20px 0;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".form-group {")
        style_code.append("  margin-bottom: 15px;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".form-group label {")
        style_code.append("  display: block;")
        style_code.append("  margin-bottom: 5px;")
        style_code.append("  font-weight: bold;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-input {")
        style_code.append("  width: 100%;")
        style_code.append("  padding: 10px;")
        style_code.append("  border: 1px solid #ddd;")
        style_code.append("  border-radius: 4px;")
        style_code.append("  font-size: 16px;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-button {")
        style_code.append("  padding: 10px 20px;")
        style_code.append("  background-color: #42b883;")
        style_code.append("  color: white;")
        style_code.append("  border: none;")
        style_code.append("  border-radius: 4px;")
        style_code.append("  cursor: pointer;")
        style_code.append("  font-size: 16px;")
        style_code.append("  transition: background-color 0.3s;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-button:hover {")
        style_code.append("  background-color: #369870;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-button:disabled {")
        style_code.append("  background-color: #6c757d;")
        style_code.append("  cursor: not-allowed;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-list ul {")
        style_code.append("  list-style: none;")
        style_code.append("  padding: 0;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".list-item {")
        style_code.append("  display: flex;")
        style_code.append("  justify-content: space-between;")
        style_code.append("  align-items: center;")
        style_code.append("  padding: 8px;")
        style_code.append("  border: 1px solid #eee;")
        style_code.append("  margin-bottom: 5px;")
        style_code.append("  border-radius: 4px;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".remove-btn {")
        style_code.append("  background: #dc3545;")
        style_code.append("  color: white;")
        style_code.append("  border: none;")
        style_code.append("  border-radius: 50%;")
        style_code.append("  width: 25px;")
        style_code.append("  height: 25px;")
        style_code.append("  cursor: pointer;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-nav a {")
        style_code.append("  margin-right: 15px;")
        style_code.append("  text-decoration: none;")
        style_code.append("  color: #42b883;")
        style_code.append("  font-weight: bold;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".vader-nav a.router-link-active {")
        style_code.append("  color: #369870;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".error {")
        style_code.append("  color: #dc3545;")
        style_code.append("  font-weight: bold;")
        style_code.append("}")
        style_code.append("")
        style_code.append(".empty-state {")
        style_code.append("  text-align: center;")
        style_code.append("  color: #6c757d;")
        style_code.append("  font-style: italic;")
        style_code.append("}")
        style_code.append("</style>")
        
        # Combinar todo
        return '\n'.join(template_code + script_code + style_code)
