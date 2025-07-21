def transpile_to_astro(code):
    """Transpila código Vader a Astro con JavaScript/TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_page = False
    in_component = False
    in_frontmatter = False
    in_style = False
    page_name = "MiPagina"
    imports = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Página Astro
        if line.startswith("pagina astro"):
            parts = line.split()
            page_name = parts[2] if len(parts) > 2 else "MiPagina"
            add_line("---")
            add_line("// Frontmatter de Astro")
            in_page = True
            in_frontmatter = True
            continue

        if line == "fin pagina":
            if in_frontmatter:
                add_line("---")
                add_line("")
            in_page = False
            in_frontmatter = False
            continue

        # Componente Astro
        if line.startswith("componente astro"):
            component_name = line.split()[2] if len(line.split()) > 2 else "MiComponente"
            add_line("---")
            add_line(f"// Componente Astro: {component_name}")
            in_component = True
            in_frontmatter = True
            continue

        if line == "fin componente":
            if in_frontmatter:
                add_line("---")
                add_line("")
            in_component = False
            in_frontmatter = False
            continue

        # Frontmatter (script del servidor)
        if line.startswith("servidor"):
            if not in_frontmatter:
                add_line("---")
                in_frontmatter = True
            continue

        if line == "fin servidor":
            if in_frontmatter:
                add_line("---")
                add_line("")
                in_frontmatter = False
            continue

        # Imports en frontmatter
        if in_frontmatter and line.startswith("importar"):
            parts = line.split()
            if "desde" in line:
                # importar { Component } desde './Component.astro'
                import_part = line.split("desde")[0].replace("importar", "").strip()
                from_part = line.split("desde")[1].strip().replace('"', '').replace("'", '')
                add_line(f"import {import_part} from '{from_part}';")
            else:
                # importar Component desde './Component.astro'
                if len(parts) >= 4 and parts[2] == "desde":
                    component = parts[1]
                    path = parts[3].replace('"', '').replace("'", '')
                    add_line(f"import {component} from '{path}';")
            continue

        # Props del componente
        if in_frontmatter and line.startswith("props"):
            props_def = line.replace("props", "").strip()
            if props_def:
                add_line(f"export interface Props {{{props_def}}}")
                add_line("const { ...props } = Astro.props;")
            else:
                add_line("const { ...props } = Astro.props;")
            continue

        # Variables del servidor
        if in_frontmatter and line.startswith("variable"):
            var_def = line.replace("variable", "").strip()
            add_line(f"const {var_def};")
            continue

        # Fetch de datos
        if in_frontmatter and line.startswith("obtener datos"):
            url = line.replace("obtener datos", "").strip()
            add_line(f"const response = await fetch({url});")
            add_line("const data = await response.json();")
            continue

        # Layout
        if line.startswith("layout"):
            layout_path = line.split()[1] if len(line.split()) > 1 else "./Layout.astro"
            add_line(f"import Layout from '{layout_path}';")
            continue

        # SEO/Meta
        if line.startswith("titulo"):
            title = line.replace("titulo", "").strip().replace('"', '')
            add_line(f"const title = '{title}';")
            continue

        if line.startswith("descripcion"):
            desc = line.replace("descripcion", "").strip().replace('"', '')
            add_line(f"const description = '{desc}';")
            continue

        # HTML/JSX content
        if not in_frontmatter:
            # Elementos HTML
            if line.startswith("titulo1"):
                content = line.replace("titulo1", "").strip().replace('"', '')
                add_line(f"<h1>{content}</h1>")
                continue

            if line.startswith("titulo2"):
                content = line.replace("titulo2", "").strip().replace('"', '')
                add_line(f"<h2>{content}</h2>")
                continue

            if line.startswith("titulo3"):
                content = line.replace("titulo3", "").strip().replace('"', '')
                add_line(f"<h3>{content}</h3>")
                continue

            if line.startswith("parrafo"):
                content = line.replace("parrafo", "").strip().replace('"', '')
                add_line(f"<p>{content}</p>")
                continue

            if line.startswith("enlace"):
                parts = line.split("a")
                if len(parts) == 2:
                    text = parts[0].replace("enlace", "").strip().replace('"', '')
                    href = parts[1].strip().replace('"', '')
                    add_line(f"<a href='{href}'>{text}</a>")
                continue

            if line.startswith("imagen"):
                parts = line.split()
                if len(parts) >= 2:
                    src = parts[1].replace('"', '')
                    alt = " ".join(parts[2:]).replace('"', '') if len(parts) > 2 else "Imagen"
                    add_line(f"<img src='{src}' alt='{alt}' />")
                continue

            if line.startswith("boton"):
                content = line.replace("boton", "").strip().replace('"', '')
                add_line(f"<button>{content}</button>")
                continue

            # Contenedores
            if line.startswith("div"):
                classes = ""
                if "clase=" in line:
                    class_part = line.split("clase=")[1].strip().replace('"', '')
                    classes = f' class="{class_part}"'
                add_line(f"<div{classes}>")
                indent += 1
                continue

            if line == "fin div":
                indent -= 1
                add_line("</div>")
                continue

            if line.startswith("seccion"):
                add_line("<section>")
                indent += 1
                continue

            if line == "fin seccion":
                indent -= 1
                add_line("</section>")
                continue

            if line.startswith("articulo"):
                add_line("<article>")
                indent += 1
                continue

            if line == "fin articulo":
                indent -= 1
                add_line("</article>")
                continue

            # Componentes interactivos
            if line.startswith("componente interactivo"):
                framework = line.split()[-1] if len(line.split()) > 2 else "react"
                component_name = line.split()[2] if len(line.split()) > 2 else "MiComponente"
                add_line(f"<{component_name} client:load />")
                continue

            # Componente hidratado
            if line.startswith("componente hidratado"):
                strategy = "load"
                if "visible" in line:
                    strategy = "visible"
                elif "idle" in line:
                    strategy = "idle"
                elif "media" in line:
                    strategy = "media"
                
                component_name = line.split()[2] if len(line.split()) > 2 else "MiComponente"
                add_line(f"<{component_name} client:{strategy} />")
                continue

            # Slot
            if line.startswith("slot"):
                slot_name = line.split()[1] if len(line.split()) > 1 else ""
                if slot_name:
                    add_line(f"<slot name='{slot_name}' />")
                else:
                    add_line("<slot />")
                continue

            # Condicionales
            if line.startswith("si"):
                condition = line.replace("si", "").strip()
                add_line(f"{{({condition}) && (")
                indent += 1
                continue

            if line == "fin si":
                indent -= 1
                add_line(")}}")
                continue

            # Bucles
            if line.startswith("para cada"):
                parts = line.split("en")
                if len(parts) == 2:
                    item = parts[0].replace("para cada", "").strip()
                    array = parts[1].strip()
                    add_line(f"{{{array}.map(({item}) => (")
                    indent += 1
                continue

            if line == "fin para cada":
                indent -= 1
                add_line("))}}")
                continue

        # Estilos
        if line.startswith("estilos"):
            add_line("<style>")
            in_style = True
            continue

        if line == "fin estilos":
            add_line("</style>")
            in_style = False
            continue

        if in_style:
            add_line(line)
            continue

        # Scripts del cliente
        if line.startswith("script cliente"):
            add_line("<script>")
            continue

        if line == "fin script":
            add_line("</script>")
            continue

        # Otras líneas en frontmatter
        if in_frontmatter:
            if "=" in line:
                add_line(f"{line};")
            elif line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"console.log({message});")
            else:
                add_line(f"// {line}")

    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_astro(codigo)

# Funciones auxiliares para el transpilador de Astro
def get_astro_keywords():
    """Retorna las palabras clave de Vader que se mapean a Astro"""
    return {
        'pagina astro': 'Astro page',
        'componente astro': 'Astro component',
        'servidor': 'server-side frontmatter',
        'importar': 'import statement',
        'props': 'component props',
        'variable': 'server variable',
        'obtener datos': 'fetch data',
        'layout': 'layout component',
        'titulo': 'page title',
        'descripcion': 'page description',
        'componente interactivo': 'interactive component',
        'componente hidratado': 'hydrated component',
        'slot': 'component slot',
        'estilos': 'component styles',
        'script cliente': 'client script',
        'titulo1': 'h1 element',
        'titulo2': 'h2 element',
        'titulo3': 'h3 element',
        'parrafo': 'paragraph',
        'enlace': 'link',
        'imagen': 'image',
        'boton': 'button',
        'div': 'div container',
        'seccion': 'section',
        'articulo': 'article'
    }
