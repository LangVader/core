def transpile_to_nextjs(code):
    """Transpila código Vader a Next.js con App Router y Server Components"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_page = False
    in_component = False
    in_api = False
    in_layout = False
    page_name = "page"
    imports = set()
    is_server_component = False
    is_client_component = False
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Páginas de Next.js
        if line.startswith("pagina"):
            parts = line.split()
            page_name = parts[1] if len(parts) > 1 else "page"
            
            # Detectar si es server o client component
            if "servidor" in line:
                is_server_component = True
                add_line("// Server Component")
            elif "cliente" in line:
                is_client_component = True
                add_line("'use client';")
                add_line("")
            
            add_line(f"export default function {page_name.capitalize()}() {{")
            in_page = True
            indent += 1
            continue

        if line == "fin pagina":
            indent -= 1
            add_line("}")
            in_page = False
            continue

        # Layout de Next.js
        if line.startswith("layout"):
            add_line("export default function RootLayout({ children }) {")
            in_layout = True
            indent += 1
            continue

        if line == "fin layout":
            indent -= 1
            add_line("}")
            in_layout = False
            continue

        # API Routes
        if line.startswith("api"):
            method = "GET"
            if "POST" in line.upper():
                method = "POST"
            elif "PUT" in line.upper():
                method = "PUT"
            elif "DELETE" in line.upper():
                method = "DELETE"
            
            add_line(f"export async function {method}(request) {{")
            in_api = True
            indent += 1
            continue

        if line == "fin api":
            indent -= 1
            add_line("}")
            in_api = False
            continue

        # Metadata para SEO
        if line.startswith("metadata"):
            metadata_content = line[8:].strip()
            add_line(f"export const metadata = {metadata_content};")
            continue

        # Server Actions
        if line.startswith("accion servidor"):
            action_name = line.split()[2] if len(line.split()) > 2 else "serverAction"
            add_line("'use server';")
            add_line("")
            add_line(f"export async function {action_name}(formData) {{")
            indent += 1
            continue

        if line == "fin accion servidor":
            indent -= 1
            add_line("}")
            continue

        # Navegación con Next.js
        if line.startswith("navegar a"):
            route = line[9:].strip()
            add_import("import { useRouter } from 'next/navigation';")
            add_line("const router = useRouter();")
            add_line(f"router.push('{route}');")
            continue

        if line.startswith("enlace a"):
            parts = line.split()
            href = parts[2] if len(parts) > 2 else "/"
            text = " ".join(parts[3:]) if len(parts) > 3 else "Enlace"
            add_import("import Link from 'next/link';")
            add_line(f"<Link href=\"{href}\">{text}</Link>")
            continue

        # Imágenes optimizadas
        if line.startswith("imagen"):
            src = ""
            alt = "Imagen"
            width = "500"
            height = "300"
            
            if "src" in line:
                src = line.split("src")[1].split()[0].strip()
            if "alt" in line:
                alt = line.split("alt")[1].split()[0].strip()
            if "ancho" in line:
                width = line.split("ancho")[1].split()[0].strip()
            if "alto" in line:
                height = line.split("alto")[1].split()[0].strip()
            
            add_import("import Image from 'next/image';")
            add_line(f"<Image src=\"{src}\" alt={alt} width={{{width}}} height={{{height}}} />")
            continue

        # Formularios con Server Actions
        if line.startswith("formulario servidor"):
            action_name = line.split()[2] if len(line.split()) > 2 else "handleSubmit"
            add_line(f"<form action={{{action_name}}}>")
            indent += 1
            continue

        # Middleware
        if line.startswith("middleware"):
            add_line("import { NextResponse } from 'next/server';")
            add_line("")
            add_line("export function middleware(request) {")
            indent += 1
            continue

        if line == "fin middleware":
            indent -= 1
            add_line("}")
            add_line("")
            add_line("export const config = {")
            add_line("  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],")
            add_line("}")
            continue

        # Configuración de Next.js
        if line.startswith("configuracion"):
            add_line("/** @type {import('next').NextConfig} */")
            add_line("const nextConfig = {")
            indent += 1
            continue

        if line == "fin configuracion":
            indent -= 1
            add_line("}")
            add_line("")
            add_line("export default nextConfig;")
            continue

        # Datos estáticos (getStaticProps equivalente)
        if line.startswith("datos estaticos"):
            add_line("// Esta función se ejecuta en build time")
            add_line("async function getData() {")
            indent += 1
            continue

        if line == "fin datos estaticos":
            indent -= 1
            add_line("}")
            continue

        # Datos dinámicos (getServerSideProps equivalente)
        if line.startswith("datos dinamicos"):
            add_line("// Esta función se ejecuta en cada request")
            add_line("async function getData() {")
            indent += 1
            continue

        if line == "fin datos dinamicos":
            indent -= 1
            add_line("}")
            continue

        # Fetch con Next.js
        if line.startswith("obtener datos"):
            url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
            cache_option = "force-cache"  # default
            
            if "sin cache" in line:
                cache_option = "no-store"
            elif "revalidar" in line:
                revalidate_time = line.split("revalidar")[1].strip()
                add_line(f"const data = await fetch({url}, {{ next: {{ revalidate: {revalidate_time} }} }});")
                continue
            
            add_line(f"const data = await fetch({url}, {{ cache: '{cache_option}' }});")
            add_line("const result = await data.json();")
            continue

        # Suspense y Loading
        if line.startswith("suspense"):
            add_import("import { Suspense } from 'react';")
            fallback = line.split("fallback")[1].strip() if "fallback" in line else "<div>Cargando...</div>"
            add_line(f"<Suspense fallback={{{fallback}}}>")
            indent += 1
            continue

        if line == "fin suspense":
            indent -= 1
            add_line("</Suspense>")
            continue

        if line.startswith("loading"):
            add_line("export default function Loading() {")
            indent += 1
            add_line("return <div>Cargando...</div>;")
            indent -= 1
            add_line("}")
            continue

        # Error Boundaries
        if line.startswith("error"):
            add_line("'use client';")
            add_line("")
            add_line("export default function Error({ error, reset }) {")
            indent += 1
            continue

        if line == "fin error":
            indent -= 1
            add_line("}")
            continue

        # Not Found
        if line.startswith("no encontrado"):
            add_line("import { notFound } from 'next/navigation';")
            add_line("")
            add_line("export default function NotFound() {")
            indent += 1
            add_line("return <div>Página no encontrada</div>;")
            indent -= 1
            add_line("}")
            continue

        # Cookies
        if line.startswith("obtener cookie"):
            cookie_name = line.split()[2] if len(line.split()) > 2 else "session"
            add_import("import { cookies } from 'next/headers';")
            add_line(f"const cookieStore = cookies();")
            add_line(f"const {cookie_name} = cookieStore.get('{cookie_name}');")
            continue

        if line.startswith("establecer cookie"):
            parts = line.split()
            cookie_name = parts[2] if len(parts) > 2 else "session"
            cookie_value = parts[3] if len(parts) > 3 else "value"
            add_import("import { cookies } from 'next/headers';")
            add_line(f"cookies().set('{cookie_name}', {cookie_value});")
            continue

        # Headers
        if line.startswith("obtener headers"):
            add_import("import { headers } from 'next/headers';")
            add_line("const headersList = headers();")
            continue

        # Redirect
        if line.startswith("redirigir a"):
            url = line.split()[2] if len(line.split()) > 2 else "/"
            add_import("import { redirect } from 'next/navigation';")
            add_line(f"redirect('{url}');")
            continue

        # Parámetros de ruta
        if line.startswith("parametros"):
            add_line("export default function Page({ params }) {")
            indent += 1
            continue

        # Search params
        if line.startswith("parametros busqueda"):
            add_line("export default function Page({ searchParams }) {")
            indent += 1
            continue

        # Generar rutas estáticas
        if line.startswith("generar rutas"):
            add_line("export async function generateStaticParams() {")
            indent += 1
            continue

        if line == "fin generar rutas":
            indent -= 1
            add_line("}")
            continue

        # Componentes del sistema React (heredados)
        if line.startswith("componente"):
            parts = line.split()
            component_name = parts[1] if len(parts) > 1 else "MiComponente"
            
            if "cliente" in line:
                add_line("'use client';")
                add_line("")
            
            add_line(f"export default function {component_name}() {{")
            in_component = True
            indent += 1
            continue

        if line == "fin componente":
            indent -= 1
            add_line("}")
            in_component = False
            continue

        # Estados (solo para client components)
        if line.startswith("estado"):
            if not is_client_component:
                add_line("'use client';")
                add_line("")
                is_client_component = True
            
            parts = line.split()
            if len(parts) >= 2:
                state_name = parts[1]
                initial_value = "null"
                if "=" in line:
                    initial_value = line.split("=", 1)[1].strip()
                
                add_import("import { useState } from 'react';")
                setter_name = f"set{state_name.capitalize()}"
                add_line(f"const [{state_name}, {setter_name}] = useState({initial_value});")
            continue

        # JSX básico (heredado de React)
        if line.startswith("renderizar") or line.startswith("retornar jsx"):
            add_line("return (")
            indent += 1
            continue

        if line == "fin renderizar" or line == "fin jsx":
            indent -= 1
            add_line(");")
            continue

        # Elementos JSX básicos
        if line.startswith("div"):
            content = line[3:].strip() if len(line) > 3 else ""
            if content:
                add_line(f"<div>{content}</div>")
            else:
                add_line("<div>")
                indent += 1
            continue

        if line == "fin div":
            indent -= 1
            add_line("</div>")
            continue

        # Respuestas de API
        if in_api:
            if line.startswith("responder"):
                response_data = line[9:].strip()
                add_line(f"return Response.json({response_data});")
                continue
            
            if line.startswith("error"):
                error_message = line[5:].strip()
                status_code = "500"
                if "404" in line:
                    status_code = "404"
                elif "400" in line:
                    status_code = "400"
                elif "401" in line:
                    status_code = "401"
                
                add_line(f"return Response.json({{ error: {error_message} }}, {{ status: {status_code} }});")
                continue

        # Asignaciones y expresiones JavaScript normales
        if "=" in line:
            add_line(f"{line};")
            continue

        # Llamadas a funciones
        if line.startswith("llamar"):
            call = line[6:].strip()
            add_line(f"{call};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")

    # Agregar imports necesarios
    import_lines = []
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(sorted(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    else:
        result_lines = output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_nextjs(codigo)

# Funciones auxiliares para el transpilador de Next.js
def get_nextjs_keywords():
    """Retorna las palabras clave de Vader que se mapean a Next.js"""
    return {
        'pagina': 'Next.js page',
        'layout': 'Next.js layout',
        'api': 'API route',
        'metadata': 'page metadata',
        'accion servidor': 'server action',
        'navegar a': 'router.push',
        'enlace a': 'Link component',
        'imagen': 'Image component',
        'formulario servidor': 'form with server action',
        'middleware': 'Next.js middleware',
        'datos estaticos': 'static data fetching',
        'datos dinamicos': 'dynamic data fetching',
        'obtener datos': 'fetch with Next.js',
        'suspense': 'Suspense component',
        'loading': 'loading.js',
        'error': 'error.js',
        'no encontrado': 'not-found.js',
        'obtener cookie': 'cookies().get',
        'establecer cookie': 'cookies().set',
        'redirigir a': 'redirect',
        'parametros': 'route params',
        'parametros busqueda': 'search params',
        'generar rutas': 'generateStaticParams'
    }
