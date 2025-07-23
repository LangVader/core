"""
Sistema de frameworks para Vader
Soporte para frameworks modernos de JavaScript/TypeScript y otros lenguajes
"""

from .react import ReactFramework
from .vue import VueFramework
from .angular import AngularFramework
from .nextjs import NextJSFramework
from .express import ExpressFramework
from .svelte import SvelteFramework
from .nuxtjs import NuxtJSFramework
from .sveltekit import SvelteKitFramework

# Lista de frameworks disponibles
FRAMEWORKS = {
    'react': ReactFramework,
    'vue': VueFramework,
    'angular': AngularFramework,
    'nextjs': NextJSFramework,
    'express': ExpressFramework,
    'svelte': SvelteFramework,
    'nuxtjs': NuxtJSFramework,
    'sveltekit': SvelteKitFramework,
}

def get_framework(name):
    """Obtiene un framework por nombre"""
    return FRAMEWORKS.get(name.lower())

def list_frameworks():
    """Lista todos los frameworks disponibles"""
    return list(FRAMEWORKS.keys())

def get_framework_info():
    """Obtiene información detallada de todos los frameworks"""
    info = {}
    for name, framework_class in FRAMEWORKS.items():
        try:
            framework = framework_class()
            info[name] = {
                'name': framework.name,
                'description': framework.description,
                'target_language': framework.target_language,
                'keywords': framework.keywords
            }
        except:
            info[name] = {
                'name': name,
                'description': 'Framework disponible',
                'target_language': 'javascript',
                'keywords': []
            }
    return info
