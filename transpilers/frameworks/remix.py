def transpile_to_remix(code):
    """Transpila código Vader a Remix con JavaScript/TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_loader = False
    in_action = False
    component_name = "MiComponente"
    imports = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de Remix
    add_import("import { json, redirect } from '@remix-run/node'")
    add_import("import { useLoaderData, useActionData, Form, useFetcher } from '@remix-run/react'")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Componente/Página Remix
        if line.startswith("pagina remix") or line.startswith("componente remix"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiPagina"
            add_line("")
            add_line(f"export default function {component_name}() {{")
            in_component = True
            indent += 1
            continue

        if line == "fin pagina" or line == "fin componente":
            add_line("}")
            in_component = False
            indent -= 1
            continue

        # Loader (datos del servidor)
        if line.startswith("loader"):
            add_import("import type { LoaderFunctionArgs } from '@remix-run/node'")
            add_line("")
            add_line("export async function loader({ request, params }: LoaderFunctionArgs) {")
            in_loader = True
            indent += 1
            continue

        if line == "fin loader":
            add_line("}")
            add_line("")
            in_loader = False
            indent -= 1
            continue

        # Action (manejo de formularios)
        if line.startswith("action"):
            add_import("import type { ActionFunctionArgs } from '@remix-run/node'")
            add_line("")
            add_line("export async function action({ request, params }: ActionFunctionArgs) {")
            in_action = True
            indent += 1
            continue

        if line == "fin action":
            add_line("}")
            add_line("")
            in_action = False
            indent -= 1
            continue

        # Obtener datos del loader
        if line.startswith("datos loader"):
            var_name = line.split()[-1] if len(line.split()) > 2 else "data"
            add_line(f"const {var_name} = useLoaderData<typeof loader>();")
            continue

        # Obtener datos del action
        if line.startswith("datos action"):
            var_name = line.split()[-1] if len(line.split()) > 2 else "actionData"
            add_line(f"const {var_name} = useActionData<typeof action>();")
            continue

        # Respuestas JSON
        if line.startswith("respuesta json"):
            data = line.replace("respuesta json", "").strip()
            if "status=" in data:
                parts = data.split("status=")
                json_data = parts[0].strip()
                status_code = parts[1].strip()
                add_line(f"return json({json_data}, {{ status: {status_code} }});")
            else:
                add_line(f"return json({data});")
            continue

        # Redirecciones
        if line.startswith("redirigir a"):
            url = line.replace("redirigir a", "").strip().replace('"', '').replace("'", '')
            add_line(f"return redirect('{url}');")
            continue

        # Formularios
        if line.startswith("formulario"):
            method = "post"
            action_url = ""
            
            if "metodo=" in line:
                method = line.split("metodo=")[1].split()[0].replace('"', '').replace("'", '')
            
            if "accion=" in line:
                action_url = line.split("accion=")[1].split()[0].replace('"', '').replace("'", '')
                action_url = f' action="{action_url}"'
            
            add_line(f"<Form method='{method}'{action_url}>")
            indent += 1
            continue

        if line == "fin formulario":
            indent -= 1
            add_line("</Form>")
            continue

        # Campos de formulario
        if line.startswith("campo"):
            parts = line.split()
            if len(parts) >= 3:
                field_type = parts[1]  # text, email, password, etc.
                field_name = parts[2]
                
                placeholder = ""
                required = ""
                
                if "placeholder=" in line:
                    placeholder_text = line.split("placeholder=")[1].split()[0].replace('"', '').replace("'", '')
                    placeholder = f' placeholder="{placeholder_text}"'
                
                if "requerido" in line:
                    required = " required"
                
                add_line(f"<input type='{field_type}' name='{field_name}'{placeholder}{required} />")
            continue

        if line.startswith("textarea"):
            name = line.split()[1] if len(line.split()) > 1 else "mensaje"
            placeholder = ""
            
            if "placeholder=" in line:
                placeholder_text = line.split("placeholder=")[1].split()[0].replace('"', '').replace("'", '')
                placeholder = f' placeholder="{placeholder_text}"'
            
            add_line(f"<textarea name='{name}'{placeholder}></textarea>")
            continue

        if line.startswith("boton enviar"):
            text = line.replace("boton enviar", "").strip().replace('"', '') or "Enviar"
            add_line(f"<button type='submit'>{text}</button>")
            continue

        # Fetcher para formularios optimistas
        if line.startswith("fetcher"):
            fetcher_name = line.split()[1] if len(line.split()) > 1 else "fetcher"
            add_line(f"const {fetcher_name} = useFetcher();")
            continue

        # Meta tags
        if line.startswith("meta"):
            add_import("import type { MetaFunction } from '@remix-run/node'")
            add_line("")
            add_line("export const meta: MetaFunction = () => {")
            add_line("  return [")
            indent += 2
            continue

        if line == "fin meta":
            add_line("  ];")
            add_line("};")
            add_line("")
            indent -= 2
            continue

        if line.startswith("titulo"):
            title = line.replace("titulo", "").strip().replace('"', '')
            add_line(f"{{ title: '{title}' }},")
            continue

        if line.startswith("descripcion"):
            desc = line.replace("descripcion", "").strip().replace('"', '')
            add_line(f"{{ name: 'description', content: '{desc}' }},")
            continue

        # Links (CSS, etc.)
        if line.startswith("links"):
            add_import("import type { LinksFunction } from '@remix-run/node'")
            add_line("")
            add_line("export const links: LinksFunction = () => {")
            add_line("  return [")
            indent += 2
            continue

        if line == "fin links":
            add_line("  ];")
            add_line("};")
            add_line("")
            indent -= 2
            continue

        if line.startswith("css"):
            css_path = line.replace("css", "").strip().replace('"', '').replace("'", '')
            add_line(f"{{ rel: 'stylesheet', href: '{css_path}' }},")
            continue

        # Error Boundary
        if line.startswith("error boundary"):
            add_import("import { isRouteErrorResponse, useRouteError } from '@remix-run/react'")
            add_line("")
            add_line("export function ErrorBoundary() {")
            add_line("  const error = useRouteError();")
            add_line("")
            add_line("  if (isRouteErrorResponse(error)) {")
            add_line("    return (")
            add_line("      <div>")
            add_line(f"        <h1>{error.status} {error.statusText}</h1>")
            add_line(f"        <p>{error.data}</p>")
            add_line("      </div>")
            add_line("    );")
            add_line("  }")
            add_line("")
            add_line("  return (")
            add_line("    <div>")
            add_line("      <h1>Error inesperado</h1>")
            add_line("      <p>Lo sentimos, algo salió mal.</p>")
            add_line("    </div>")
            add_line("  );")
            add_line("}")
            continue

        # Elementos JSX
        if line.startswith("div"):
            classes = ""
            if "clase=" in line:
                class_part = line.split("clase=")[1].strip().replace('"', '')
                classes = f' className="{class_part}"'
            add_line(f"<div{classes}>")
            indent += 1
            continue

        if line == "fin div":
            indent -= 1
            add_line("</div>")
            continue

        if line.startswith("titulo1"):
            content = line.replace("titulo1", "").strip()
            if "{" in content:
                add_line(f"<h1>{content}</h1>")
            else:
                content = content.replace('"', '')
                add_line(f"<h1>{content}</h1>")
            continue

        if line.startswith("titulo2"):
            content = line.replace("titulo2", "").strip()
            if "{" in content:
                add_line(f"<h2>{content}</h2>")
            else:
                content = content.replace('"', '')
                add_line(f"<h2>{content}</h2>")
            continue

        if line.startswith("parrafo"):
            content = line.replace("parrafo", "").strip()
            if "{" in content:
                add_line(f"<p>{content}</p>")
            else:
                content = content.replace('"', '')
                add_line(f"<p>{content}</p>")
            continue

        if line.startswith("enlace"):
            parts = line.split("a")
            if len(parts) == 2:
                text = parts[0].replace("enlace", "").strip().replace('"', '')
                href = parts[1].strip().replace('"', '')
                add_import("import { Link } from '@remix-run/react'")
                add_line(f"<Link to='{href}'>{text}</Link>")
            continue

        # Condicionales
        if line.startswith("si"):
            condition = line.replace("si", "").strip()
            add_line(f"{{{condition} && (")
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

        # Renderizar
        if line.startswith("renderizar"):
            add_line("return (")
            indent += 1
            continue

        if line == "fin renderizar":
            indent -= 1
            add_line(");")
            continue

        # Otras líneas (comentarios o código JavaScript)
        if in_component or in_loader or in_action:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"console.log({message});")
            elif "=" in line and not line.startswith("//"):
                add_line(f"{line};")
            else:
                add_line(f"// {line}")

    # Agregar imports al inicio
    import_lines = []
    if imports:
        import_lines.extend(sorted(imports))
        import_lines.append("")
    
    result_lines = import_lines + output
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_remix(codigo)

# Funciones auxiliares para el transpilador de Remix
def get_remix_keywords():
    """Retorna las palabras clave de Vader que se mapean a Remix"""
    return {
        'pagina remix': 'Remix page component',
        'componente remix': 'Remix component',
        'loader': 'server-side data loader',
        'action': 'form action handler',
        'datos loader': 'useLoaderData hook',
        'datos action': 'useActionData hook',
        'respuesta json': 'JSON response',
        'redirigir a': 'redirect response',
        'formulario': 'Remix Form',
        'campo': 'form field',
        'textarea': 'textarea field',
        'boton enviar': 'submit button',
        'fetcher': 'useFetcher hook',
        'meta': 'meta function',
        'links': 'links function',
        'css': 'CSS link',
        'error boundary': 'error boundary',
        'titulo': 'page title',
        'descripcion': 'page description',
        'titulo1': 'h1 element',
        'titulo2': 'h2 element',
        'parrafo': 'paragraph',
        'enlace': 'Link component',
        'div': 'div container',
        'renderizar': 'component render'
    }
