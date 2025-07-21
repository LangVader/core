# Sistema modular de frameworks para JavaScript/TypeScript
# Permite a Vader generar código específico para frameworks modernos

from .react import transpilar as transpile_react
from .nextjs import transpilar as transpile_nextjs
from .express import transpilar as transpile_express
from .vue import transpilar as transpile_vue
from .angular import transpilar as transpile_angular
from .svelte import transpilar as transpile_svelte
from .nuxt import transpilar as transpile_nuxt
from .sveltekit import transpilar as transpile_sveltekit
from .solidjs import transpilar as transpile_solidjs
from .remix import transpilar as transpile_remix
from .astro import transpilar as transpile_astro
from .qwik import transpilar as transpile_qwik
from .fastapi import transpilar as transpile_fastapi
from .flask import transpilar as transpile_flask
from .django import transpilar as transpile_django
from .laravel import transpilar as transpile_laravel
from .flutter_web import transpilar as transpile_flutter_web
from .blazor import transpile_blazor
from .spring_boot import transpile_spring_boot
from .r_stats import transpile_r
from .scala import transpile_scala
from .gin_go import transpile_gin
from .actix_rust import transpile_actix

# Diccionario de frameworks disponibles
FRAMEWORKS = {
    # Frontend Frameworks
    'react': {
        'name': 'React',
        'description': 'Biblioteca de JavaScript para construir interfaces de usuario',
        'file': 'react.py',
        'keywords': ['componente react', 'react', 'jsx', 'hooks'],
        'extension': '.jsx'
    },
    'vue': {
        'name': 'Vue.js',
        'description': 'Framework progresivo de JavaScript para construir interfaces de usuario',
        'file': 'vue.py',
        'keywords': ['componente vue', 'vue', 'template', 'script setup'],
        'extension': '.vue'
    },
    'angular': {
        'name': 'Angular',
        'description': 'Plataforma y framework para construir aplicaciones web',
        'file': 'angular.py',
        'keywords': ['componente angular', 'angular', 'typescript', 'decorador'],
        'extension': '.ts'
    },
    'solidjs': {
        'name': 'SolidJS',
        'description': 'Framework reactivo de JavaScript con rendimiento ultra rápido',
        'file': 'solidjs.py',
        'keywords': ['componente solid', 'solidjs', 'solid', 'señal', 'signal'],
        'extension': '.jsx'
    },
    'svelte': {
        'name': 'Svelte',
        'description': 'Framework de JavaScript que compila componentes',
        'file': 'svelte.py',
        'keywords': ['componente svelte', 'svelte', 'reactivo', 'store'],
        'extension': '.svelte'
    },
    
    # Full-Stack Frameworks
    'nextjs': {
        'name': 'Next.js',
        'description': 'Framework de React para aplicaciones web de producción',
        'file': 'nextjs.py',
        'keywords': ['pagina next', 'nextjs', 'next', 'api route'],
        'extension': '.tsx'
    },
    'nuxt': {
        'name': 'Nuxt.js',
        'description': 'Framework de Vue.js para aplicaciones universales',
        'file': 'nuxt.py',
        'keywords': ['pagina nuxt', 'nuxt', 'universal', 'ssr'],
        'extension': '.vue'
    },
    'sveltekit': {
        'name': 'SvelteKit',
        'description': 'Framework full-stack de Svelte',
        'file': 'sveltekit.py',
        'keywords': ['pagina sveltekit', 'sveltekit', 'load', 'action'],
        'extension': '.svelte'
    },
    'remix': {
        'name': 'Remix',
        'description': 'Framework full-stack de React centrado en web standards',
        'file': 'remix.py',
        'keywords': ['pagina remix', 'componente remix', 'remix', 'loader', 'action'],
        'extension': '.tsx'
    },
    'astro': {
        'name': 'Astro',
        'description': 'Framework para sitios web estáticos ultra rápidos',
        'file': 'astro.py',
        'keywords': ['pagina astro', 'componente astro', 'astro', 'frontmatter'],
        'extension': '.astro'
    },
    'qwik': {
        'name': 'Qwik',
        'description': 'Framework de nueva generación con carga instantánea',
        'file': 'qwik.py',
        'keywords': ['componente qwik', 'qwik', 'señal', 'tarea'],
        'extension': '.tsx'
    },
    
    # Backend Frameworks
    'express': {
        'name': 'Express.js',
        'description': 'Framework web minimalista para Node.js',
        'file': 'express.py',
        'keywords': ['servidor express', 'express', 'ruta', 'middleware'],
        'extension': '.js'
    },
    'fastapi': {
        'name': 'FastAPI',
        'description': 'Framework moderno y rápido para construir APIs con Python',
        'file': 'fastapi.py',
        'keywords': ['api fastapi', 'fastapi', 'modelo', 'ruta GET', 'ruta POST'],
        'extension': '.py'
    },
    'flask': {
        'name': 'Flask',
        'description': 'Framework web minimalista para Python',
        'file': 'flask.py',
        'keywords': ['app flask', 'flask', 'ruta GET', 'ruta POST'],
        'extension': '.py'
    },
    'django': {
        'name': 'Django',
        'description': 'Framework web de alto nivel para Python',
        'file': 'django.py',
        'keywords': ['app django', 'django', 'modelo', 'vista', 'controlador'],
        'extension': '.py'
    },
    'laravel': {
        'name': 'Laravel',
        'description': 'Framework web elegante para PHP',
        'file': 'laravel.py',
        'keywords': ['app laravel', 'laravel', 'modelo', 'controlador', 'ruta GET'],
        'extension': '.php'
    },
    
    # Mobile/Cross-Platform
    'flutter_web': {
        'name': 'Flutter Web',
        'description': 'Framework de Google para aplicaciones web con Dart',
        'file': 'flutter_web.py',
        'keywords': ['app flutter', 'flutter', 'widget', 'widget estado'],
        'extension': '.dart'
    },
    'blazor': {
        'name': 'Blazor',
        'description': 'Framework de Microsoft para aplicaciones web con C#',
        'file': 'blazor.py',
        'keywords': ['componente blazor', 'blazor', 'estado', 'servicio'],
        'extension': '.razor'
    },
    'spring_boot': {
        'name': 'Spring Boot',
        'description': 'Framework de Java para aplicaciones backend empresariales',
        'file': 'spring_boot.py',
        'keywords': ['controlador spring', 'servicio spring', 'entidad spring', 'repositorio'],
        'extension': '.java'
    },
    'r_stats': {
        'name': 'R Statistics',
        'description': 'Lenguaje R para análisis estadístico y ciencia de datos',
        'file': 'r_stats.py',
        'keywords': ['cargar datos', 'grafico barras', 'histograma', 'regresion lineal'],
        'extension': '.R'
    },
    'scala': {
        'name': 'Scala',
        'description': 'Lenguaje Scala para programación funcional y big data',
        'file': 'scala.py',
        'keywords': ['objeto scala', 'clase scala', 'funcion pura', 'actor', 'spark'],
        'extension': '.scala'
    },
    'gin': {
        'name': 'Gin (Go)',
        'description': 'Framework web ultra rápido para Go',
        'file': 'gin_go.py',
        'keywords': ['servidor gin', 'ruta get', 'ruta post', 'middleware', 'gin'],
        'extension': '.go'
    },
    'actix': {
        'name': 'Actix-web (Rust)',
        'description': 'Framework web de alto rendimiento para Rust',
        'file': 'actix_rust.py',
        'keywords': ['servidor actix', 'ruta get', 'ruta post', 'actix', 'async'],
        'extension': '.rs'
    }
}

def get_available_frameworks():
    """Retorna la lista de frameworks disponibles"""
    return list(FRAMEWORKS.keys())

def get_framework_info(framework_name):
    """Retorna información sobre un framework específico"""
    return FRAMEWORKS.get(framework_name.lower())

def transpile_with_framework(code, framework):
    """Transpila código usando un framework específico"""
    if framework not in FRAMEWORKS:
        raise ValueError(f"Framework '{framework}' no soportado. Frameworks disponibles: {list(FRAMEWORKS.keys())}")
    
    # Mapeo de frameworks a sus transpiladores
    transpiler_map = {
        'react': transpile_react,
        'vue': transpile_vue,
        'angular': transpile_angular,
        'solidjs': transpile_solidjs,
        'svelte': transpile_svelte,
        'nextjs': transpile_nextjs,
        'nuxt': transpile_nuxt,
        'sveltekit': transpile_sveltekit,
        'remix': transpile_remix,
        'astro': transpile_astro,
        'qwik': transpile_qwik,
        'express': transpile_express,
        'fastapi': transpile_fastapi,
        'flask': transpile_flask,
        'django': transpile_django,
        'laravel': transpile_laravel,
        'flutter_web': transpile_flutter_web,
        'blazor': transpile_blazor,
        'spring_boot': transpile_spring_boot,
        'r_stats': transpile_r,
        'scala': transpile_scala,
        'gin': transpile_gin,
        'actix': transpile_actix
    }
    
    transpiler = transpiler_map.get(framework)
    if not transpiler:
        raise ValueError(f"Transpilador para '{framework}' no encontrado")
    
    try:
        return transpiler(code)
    except Exception as e:
        raise ValueError(f"Error transpilando con {framework}: {str(e)}")

def detect_framework(code):
    """Detecta automáticamente el framework basado en palabras clave"""
    code_lower = code.lower()
    
    # Puntuación para cada framework
    scores = {}
    
    for framework_name, framework_info in FRAMEWORKS.items():
        score = 0
        for keyword in framework_info['keywords']:
            score += code_lower.count(keyword)
        scores[framework_name] = score
    
    # Retorna el framework con mayor puntuación
    if scores:
        best_framework = max(scores, key=scores.get)
        if scores[best_framework] > 0:
            return best_framework
    
def list_frameworks():
    """Lista todos los frameworks disponibles con sus descripciones"""
    print("\n=== FRAMEWORKS DISPONIBLES EN VADER ===")
    print("Vader ahora soporta los siguientes frameworks modernos:\n")
    
    for name, info in FRAMEWORKS.items():
        print(f"📦 {info['name']} ({name})")
        print(f"   {info['description']}")
        print(f"   Extensión: {info['extension']}")
        print(f"   Palabras clave: {', '.join(info['keywords'])}")
        print()
    
    print("💡 Uso: python vader.py archivo.vdr --framework <nombre>")
    print("💡 Ejemplo: python vader.py mi_app.vdr --framework react")

def get_framework_keywords():
    """Retorna todas las palabras clave de todos los frameworks"""
    all_keywords = {}
    for framework_name, framework_info in FRAMEWORKS.items():
        all_keywords[framework_name] = framework_info['keywords']
    return all_keywords

__all__ = [
    'FRAMEWORKS',
    'get_available_frameworks',
    'get_framework_info',
    'transpile_with_framework',
    'detect_framework',
    'list_frameworks',
    'get_framework_keywords'
]
