def transpile_to_svelte(code):
    """Transpila código Vader a Svelte con JavaScript/TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_script = False
    in_style = False
    component_name = "MiComponente"
    stores_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def detect_svelte_features(line):
        """Detecta características de Svelte en el código"""
        if "store" in line or "tienda" in line:
            stores_used.add("writable")
        if "readable" in line or "legible" in line:
            stores_used.add("readable")
        if "derived" in line or "derivado" in line:
            stores_used.add("derived")

    # Estructura básica del componente Svelte
    script_content = []
    template_content = []
    style_content = []
    
    current_section = "template"  # Por defecto asumimos template
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_svelte_features(line)

        # Componente Svelte
        if line.startswith("componente svelte"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            in_component = True
            continue

        if line == "fin componente":
            in_component = False
            continue

        # Script section
        if line.startswith("script") or line.startswith("logica"):
            current_section = "script"
            in_script = True
            continue

        if line == "fin script" or line == "fin logica":
            current_section = "template"
            in_script = False
            continue

        # Style section
        if line.startswith("estilos") or line.startswith("style"):
            current_section = "style"
            in_style = True
            continue

        if line == "fin estilos" or line == "fin style":
            current_section = "template"
            in_style = False
            continue

        # Procesar contenido según la sección
        if current_section == "script":
            script_content.append(process_script_line(line))
        elif current_section == "style":
            style_content.append(line)
        else:
            template_content.append(process_template_line(line))

    # Generar script
    if script_content or stores_used:
        add_line("<script>")
        
        # Agregar imports de Svelte stores si se usan
        if stores_used:
            stores_list = ", ".join(sorted(stores_used))
            add_line(f"  import {{ {stores_list} }} from 'svelte/store';")
            add_line("")
        
        # Agregar contenido del script
        for line in script_content:
            if line:
                add_line(f"  {line}")
        
        add_line("</script>")
        add_line("")
    
    # Generar template
    for line in template_content:
        if line:
            add_line(line)
    
    # Generar estilos si existen
    if style_content:
        add_line("")
        add_line("<style>")
        for line in style_content:
            if line:
                add_line(f"  {line}")
        add_line("</style>")
    
    return "\n".join(output)

def process_template_line(line):
    """Procesa una línea del template Svelte"""
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
        if "on:click" in line:
            handler = line.split("on:click")[1].strip()
            return f"<button on:click={{{handler}}}>{content}</button>"
        elif "onclick" in line:
            handler = line.split("onclick")[1].strip()
            return f"<button on:click={{{handler}}}>{content}</button>"
        else:
            return f"<button>{content}</button>"
    
    if line.startswith("input"):
        input_type = "text"
        placeholder = ""
        bind_value = ""
        
        if "tipo" in line:
            input_type = line.split("tipo")[1].split()[0].strip()
        if "placeholder" in line:
            placeholder = line.split("placeholder")[1].split()[0].strip()
        if "bind:value" in line:
            bind_value = line.split("bind:value")[1].split()[0].strip()
        elif "enlazar" in line:
            bind_value = line.split("enlazar")[1].split()[0].strip()
        
        props = [f'type="{input_type}"']
        if placeholder:
            props.append(f'placeholder="{placeholder}"')
        if bind_value:
            props.append(f'bind:value={{{bind_value}}}')
        
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
    
    # Directivas Svelte
    if line.startswith("{#if") or line.startswith("si"):
        condition = line.split("si")[1].strip() if "si" in line else line.split("{#if")[1].strip()
        return f'{{#if {condition}}}'
    
    if line.startswith("{:else}") or line == "sino":
        return '{:else}'
    
    if line.startswith("{/if}") or line == "fin si":
        return '{/if}'
    
    if line.startswith("{#each") or line.startswith("para cada"):
        if "para cada" in line:
            parts = line.split("para cada")[1].strip().split(" en ")
            item = parts[0].strip()
            collection = parts[1].strip()
            return f'{{#each {collection} as {item}}}'
        else:
            loop_expr = line.split("{#each")[1].strip()
            return f'{{#each {loop_expr}}}'
    
    if line.startswith("{/each}") or line == "fin cada":
        return '{/each}'
    
    if line.startswith("{#await") or line.startswith("esperar"):
        promise = line.split("esperar")[1].strip() if "esperar" in line else line.split("{#await")[1].strip()
        return f'{{#await {promise}}}'
    
    if line.startswith("{:then}") or line == "entonces":
        return '{:then}'
    
    if line.startswith("{:catch}") or line == "capturar":
        return '{:catch}'
    
    if line.startswith("{/await}") or line == "fin esperar":
        return '{/await}'
    
    # Binding de eventos
    if line.startswith("on:"):
        return line
    
    # Binding de propiedades
    if line.startswith("bind:"):
        return line
    
    # Interpolación
    if "{" in line and "}" in line:
        return line
    
    # Slots
    if line.startswith("slot"):
        slot_name = line.split()[1] if len(line.split()) > 1 else ""
        if slot_name:
            return f'<slot name="{slot_name}"></slot>'
        else:
            return '<slot></slot>'
    
    return line

def process_script_line(line):
    """Procesa una línea del script Svelte"""
    if not line.strip():
        return ""
    
    # Variables reactivas
    if line.startswith("let ") or line.startswith("variable "):
        var_decl = line.replace("variable ", "let ").strip()
        return f"{var_decl};"
    
    # Reactive statements
    if line.startswith("reactivo") or line.startswith("$:"):
        if line.startswith("reactivo"):
            statement = line[8:].strip()
            return f"$: {statement};"
        else:
            return f"{line};"
    
    # Stores
    if line.startswith("store") or line.startswith("tienda"):
        parts = line.split()
        if len(parts) >= 2:
            store_name = parts[1]
            initial_value = "null"
            if "=" in line:
                initial_value = line.split("=", 1)[1].strip()
            return f"const {store_name} = writable({initial_value});"
    
    if line.startswith("store legible") or line.startswith("readable"):
        parts = line.split()
        store_name = parts[2] if len(parts) > 2 else parts[1]
        initial_value = "null"
        if "=" in line:
            initial_value = line.split("=", 1)[1].strip()
        return f"const {store_name} = readable({initial_value});"
    
    if line.startswith("store derivado") or line.startswith("derived"):
        parts = line.split()
        store_name = parts[2] if len(parts) > 2 else parts[1]
        if "desde" in line:
            source_stores = line.split("desde")[1].split("=")[0].strip()
            callback = line.split("=")[1].strip() if "=" in line else "($values) => $values"
            return f"const {store_name} = derived({source_stores}, {callback});"
    
    # Suscripción a stores
    if line.startswith("suscribir"):
        store_name = line.split()[1] if len(line.split()) > 1 else "store"
        return f"const unsubscribe = {store_name}.subscribe(value => {{"
    
    if line == "fin suscripcion":
        return "});"
    
    # Props (export let)
    if line.startswith("prop") or line.startswith("export let"):
        if line.startswith("prop"):
            prop_decl = line[4:].strip()
            return f"export let {prop_decl};"
        else:
            return f"{line};"
    
    # Funciones
    if line.startswith("funcion"):
        parts = line.split()
        if len(parts) >= 2:
            func_name = parts[1]
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                return f"function {func_name}({params_part}) {{"
            else:
                return f"function {func_name}() {{"
    
    if line == "fin funcion":
        return "}"
    
    # Lifecycle hooks
    if line.startswith("onMount") or line.startswith("al montar"):
        return "onMount(() => {"
    
    if line.startswith("onDestroy") or line.startswith("al destruir"):
        return "onDestroy(() => {"
    
    if line.startswith("beforeUpdate") or line.startswith("antes de actualizar"):
        return "beforeUpdate(() => {"
    
    if line.startswith("afterUpdate") or line.startswith("despues de actualizar"):
        return "afterUpdate(() => {"
    
    if line == "fin lifecycle" or line == "fin ciclo":
        return "});"
    
    # Dispatch de eventos personalizados
    if line.startswith("dispatch") or line.startswith("despachar"):
        event_name = line.split()[1] if len(line.split()) > 1 else "evento"
        detail = line.split()[2:] if len(line.split()) > 2 else ""
        detail_str = " ".join(detail) if detail else "null"
        return f"dispatch('{event_name}', {detail_str});"
    
    # Context API
    if line.startswith("setContext") or line.startswith("establecer contexto"):
        key = line.split()[2] if len(line.split()) > 2 else "'key'"
        value = line.split()[3] if len(line.split()) > 3 else "value"
        return f"setContext({key}, {value});"
    
    if line.startswith("getContext") or line.startswith("obtener contexto"):
        key = line.split()[2] if len(line.split()) > 2 else "'key'"
        return f"const context = getContext({key});"
    
    # Tick
    if line.startswith("tick") or line.startswith("esperar tick"):
        return "await tick();"
    
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
    return transpile_to_svelte(codigo)

# Funciones auxiliares para el transpilador de Svelte
def get_svelte_keywords():
    """Retorna las palabras clave de Vader que se mapean a Svelte"""
    return {
        'componente svelte': 'Svelte component',
        'script': 'script section',
        'logica': 'script section',
        'estilos': 'style section',
        'variable': 'let declaration',
        'reactivo': 'reactive statement ($:)',
        'store': 'writable store',
        'tienda': 'writable store',
        'store legible': 'readable store',
        'store derivado': 'derived store',
        'suscribir': 'store subscription',
        'prop': 'export let (props)',
        'funcion': 'function',
        'al montar': 'onMount',
        'al destruir': 'onDestroy',
        'antes de actualizar': 'beforeUpdate',
        'despues de actualizar': 'afterUpdate',
        'despachar': 'dispatch event',
        'establecer contexto': 'setContext',
        'obtener contexto': 'getContext',
        'esperar tick': 'await tick()',
        'si': '{#if} block',
        'sino': '{:else} block',
        'fin si': '{/if}',
        'para cada': '{#each} block',
        'fin cada': '{/each}',
        'esperar': '{#await} block',
        'entonces': '{:then}',
        'capturar': '{:catch}',
        'fin esperar': '{/await}',
        'slot': 'slot element',
        'bind:value': 'two-way binding',
        'enlazar': 'bind directive',
        'on:click': 'event handler'
    }
