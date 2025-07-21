def transpile_to_vue(code):
    """Transpila código Vader a Vue.js con Composition API"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_template = False
    in_script = False
    in_style = False
    component_name = "MiComponente"
    imports = set()
    composables_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def detect_composables(line):
        """Detecta composables de Vue en el código"""
        if "reactivo" in line or "ref" in line:
            composables_used.add("ref")
        if "computed" in line or "computado" in line:
            composables_used.add("computed")
        if "watch" in line or "observar" in line:
            composables_used.add("watch")
        if "onMounted" in line or "al montar" in line:
            composables_used.add("onMounted")
        if "onUnmounted" in line or "al desmontar" in line:
            composables_used.add("onUnmounted")

    # Estructura básica del componente Vue
    add_line("<template>")
    template_content = []
    script_content = []
    style_content = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_composables(line)

        # Componente Vue
        if line.startswith("componente vue"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            in_component = True
            continue

        if line == "fin componente":
            in_component = False
            continue

        # Template section
        if line.startswith("template") or line.startswith("plantilla"):
            in_template = True
            continue

        if line == "fin template" or line == "fin plantilla":
            in_template = False
            continue

        # Script section
        if line.startswith("script") or line.startswith("logica"):
            in_script = True
            continue

        if line == "fin script" or line == "fin logica":
            in_script = False
            continue

        # Style section
        if line.startswith("estilos") or line.startswith("style"):
            in_style = True
            continue

        if line == "fin estilos" or line == "fin style":
            in_style = False
            continue

        # Procesar contenido según la sección
        if in_template:
            template_content.append(process_template_line(line))
        elif in_script:
            script_content.append(process_script_line(line))
        elif in_style:
            style_content.append(line)
        else:
            # Si no está en una sección específica, asumir que es template
            template_content.append(process_template_line(line))

    # Generar template
    indent = 1
    for line in template_content:
        if line:
            add_line(line)
    
    add_line("</template>")
    add_line("")
    
    # Generar script
    add_line("<script setup>")
    
    # Agregar imports de Vue
    if composables_used:
        composables_list = ", ".join(sorted(composables_used))
        add_line(f"import {{ {composables_list} }} from 'vue';")
        add_line("")
    
    # Agregar imports personalizados
    if imports:
        for imp in sorted(imports):
            add_line(imp)
        add_line("")
    
    # Agregar contenido del script
    for line in script_content:
        if line:
            add_line(line)
    
    add_line("</script>")
    
    # Generar estilos si existen
    if style_content:
        add_line("")
        add_line("<style scoped>")
        for line in style_content:
            if line:
                add_line(line)
        add_line("</style>")
    
    return "\n".join(output)

def process_template_line(line):
    """Procesa una línea del template Vue"""
    if not line.strip():
        return ""
    
    # Elementos HTML básicos
    if line.startswith("div"):
        content = line[3:].strip() if len(line) > 3 else ""
        if content:
            return f"<div>{content}</div>"
        else:
            return "<div>"
    
    if line == "fin div":
        return "</div>"
    
    if line.startswith("boton"):
        content = line[5:].strip() if len(line) > 5 else "Botón"
        if "@click" in line:
            handler = line.split("@click")[1].strip()
            return f"<button @click=\"{handler}\">{content}</button>"
        elif "onclick" in line:
            handler = line.split("onclick")[1].strip()
            return f"<button @click=\"{handler}\">{content}</button>"
        else:
            return f"<button>{content}</button>"
    
    if line.startswith("input"):
        input_type = "text"
        placeholder = ""
        v_model = ""
        
        if "tipo" in line:
            input_type = line.split("tipo")[1].split()[0].strip()
        if "placeholder" in line:
            placeholder = line.split("placeholder")[1].split()[0].strip()
        if "v-model" in line:
            v_model = line.split("v-model")[1].split()[0].strip()
        elif "modelo" in line:
            v_model = line.split("modelo")[1].split()[0].strip()
        
        props = [f'type="{input_type}"']
        if placeholder:
            props.append(f'placeholder="{placeholder}"')
        if v_model:
            props.append(f'v-model="{v_model}"')
        
        return f"<input {' '.join(props)} />"
    
    if line.startswith("texto"):
        content = line[5:].strip() if len(line) > 5 else ""
        return f"<p>{content}</p>"
    
    if line.startswith("titulo"):
        level = "1"
        content = line[6:].strip() if len(line) > 6 else "Título"
        if line.startswith("titulo1"):
            level = "1"
            content = line[7:].strip()
        elif line.startswith("titulo2"):
            level = "2"
            content = line[7:].strip()
        elif line.startswith("titulo3"):
            level = "3"
            content = line[7:].strip()
        
        return f"<h{level}>{content}</h{level}>"
    
    # Directivas Vue
    if line.startswith("v-if") or line.startswith("si"):
        condition = line.split("si")[1].strip() if "si" in line else line.split("v-if")[1].strip()
        return f'<div v-if="{condition}">'
    
    if line.startswith("v-else") or line == "sino":
        return '<div v-else>'
    
    if line.startswith("v-for") or line.startswith("para cada"):
        if "para cada" in line:
            parts = line.split("para cada")[1].strip().split(" en ")
            item = parts[0].strip()
            collection = parts[1].strip()
            return f'<div v-for="{item} in {collection}" :key="{item}.id">'
        else:
            loop_expr = line.split("v-for")[1].strip()
            return f'<div v-for="{loop_expr}">'
    
    if line.startswith("v-show") or line.startswith("mostrar si"):
        condition = line.split("mostrar si")[1].strip() if "mostrar si" in line else line.split("v-show")[1].strip()
        return f'<div v-show="{condition}">'
    
    # Interpolación
    if "{{" in line and "}}" in line:
        return line
    
    # Binding de atributos
    if line.startswith(":") or line.startswith("bind"):
        return line
    
    # Eventos
    if line.startswith("@") or line.startswith("on"):
        return line
    
    return line

def process_script_line(line):
    """Procesa una línea del script Vue"""
    if not line.strip():
        return ""
    
    # Variables reactivas
    if line.startswith("reactivo"):
        parts = line.split()
        if len(parts) >= 2:
            var_name = parts[1]
            initial_value = "null"
            if "=" in line:
                initial_value = line.split("=", 1)[1].strip()
            return f"const {var_name} = ref({initial_value});"
    
    # Computed properties
    if line.startswith("computado"):
        parts = line.split()
        if len(parts) >= 2:
            computed_name = parts[1]
            if "=" in line:
                expression = line.split("=", 1)[1].strip()
                return f"const {computed_name} = computed(() => {expression});"
            else:
                return f"const {computed_name} = computed(() => {{"
    
    if line == "fin computado":
        return "});"
    
    # Watchers
    if line.startswith("observar"):
        parts = line.split()
        if len(parts) >= 2:
            watched_var = parts[1]
            return f"watch({watched_var}, (newValue, oldValue) => {{"
    
    if line == "fin observar":
        return "});"
    
    # Lifecycle hooks
    if line.startswith("al montar") or line.startswith("onMounted"):
        return "onMounted(() => {"
    
    if line.startswith("al desmontar") or line.startswith("onUnmounted"):
        return "onUnmounted(() => {"
    
    if line == "fin lifecycle" or line == "fin ciclo":
        return "});"
    
    # Métodos/funciones
    if line.startswith("metodo") or line.startswith("funcion"):
        parts = line.split()
        if len(parts) >= 2:
            method_name = parts[1]
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                return f"const {method_name} = ({params_part}) => {{"
            else:
                return f"const {method_name} = () => {{"
    
    if line == "fin metodo" or line == "fin funcion":
        return "};"
    
    # Props
    if line.startswith("props"):
        props_def = line[5:].strip()
        return f"const props = defineProps({props_def});"
    
    # Emits
    if line.startswith("emits") or line.startswith("eventos"):
        emits_def = line.split()[1:] if len(line.split()) > 1 else "[]"
        return f"const emit = defineEmits({emits_def});"
    
    if line.startswith("emitir"):
        event_name = line.split()[1] if len(line.split()) > 1 else "event"
        payload = line.split()[2:] if len(line.split()) > 2 else ""
        payload_str = " ".join(payload) if payload else ""
        return f"emit('{event_name}'{', ' + payload_str if payload_str else ''});"
    
    # Composables personalizados
    if line.startswith("usar"):
        composable_name = line.split()[1] if len(line.split()) > 1 else "useComposable"
        return f"const {{ }} = {composable_name}();"
    
    # Importaciones
    if line.startswith("importar"):
        if " desde " in line:
            parts = line.split(" desde ")
            what = parts[0][len("importar"):].strip()
            from_where = parts[1].strip()
            return f"import {what} from {from_where};"
        else:
            module = line[len("importar"):].strip()
            return f"import {module};"
    
    # Asignaciones y expresiones JavaScript normales
    if "=" in line:
        return f"{line};"
    
    # Llamadas a funciones
    if line.startswith("llamar"):
        call = line[6:].strip()
        return f"{call};"
    
    return f"// {line}"

def transpilar(codigo):
    return transpile_to_vue(codigo)

# Funciones auxiliares para el transpilador de Vue.js
def get_vue_keywords():
    """Retorna las palabras clave de Vader que se mapean a Vue.js"""
    return {
        'componente vue': 'Vue component',
        'template': 'template section',
        'plantilla': 'template section',
        'script': 'script section',
        'logica': 'script section',
        'estilos': 'style section',
        'reactivo': 'ref',
        'computado': 'computed',
        'observar': 'watch',
        'al montar': 'onMounted',
        'al desmontar': 'onUnmounted',
        'metodo': 'method',
        'props': 'defineProps',
        'emits': 'defineEmits',
        'eventos': 'defineEmits',
        'emitir': 'emit',
        'usar': 'composable',
        'v-if': 'v-if directive',
        'si': 'v-if directive',
        'v-else': 'v-else directive',
        'sino': 'v-else directive',
        'v-for': 'v-for directive',
        'para cada': 'v-for directive',
        'v-show': 'v-show directive',
        'mostrar si': 'v-show directive',
        'v-model': 'v-model directive',
        'modelo': 'v-model directive'
    }
