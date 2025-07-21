# Sistema de Inteligencia Artificial Integrada para Vader
# Genera código automáticamente, sugiere mejoras y detecta errores

import re
import json
from typing import List, Dict, Tuple, Optional

class VaderAIAssistant:
    """Asistente de IA integrado para Vader"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.suggestions_db = self._load_suggestions()
        self.error_patterns = self._load_error_patterns()
    
    def _load_patterns(self) -> Dict:
        """Cargar patrones de código comunes"""
        return {
            # Patrones de aplicaciones web
            "sitio web": {
                "template": "web_basica",
                "components": ["navegacion", "contenido", "pie_pagina"],
                "styles": ["responsive", "moderno"]
            },
            "tienda online": {
                "template": "ecommerce",
                "components": ["productos", "carrito", "checkout"],
                "styles": ["profesional", "responsive"]
            },
            "blog": {
                "template": "blog",
                "components": ["articulos", "comentarios", "sidebar"],
                "styles": ["limpio", "legible"]
            },
            
            # Patrones de aplicaciones móviles
            "app movil": {
                "frameworks": ["flutter", "react_native"],
                "components": ["navegacion", "pantallas", "formularios"],
                "features": ["offline", "notificaciones"]
            },
            
            # Patrones de APIs
            "api rest": {
                "frameworks": ["fastapi", "express", "spring_boot"],
                "components": ["rutas", "modelos", "autenticacion"],
                "features": ["cors", "validacion", "documentacion"]
            },
            
            # Patrones de análisis de datos
            "analisis datos": {
                "frameworks": ["r_stats", "python"],
                "components": ["carga_datos", "visualizacion", "estadisticas"],
                "features": ["graficos", "exportacion", "reportes"]
            }
        }
    
    def _load_suggestions(self) -> Dict:
        """Cargar base de datos de sugerencias"""
        return {
            "mejores_practicas": {
                "variables": [
                    "Usa nombres descriptivos: 'edad_usuario' en lugar de 'x'",
                    "Evita nombres muy largos: 'edad' en lugar de 'edad_del_usuario_actual'",
                    "Usa español consistente en todo el código"
                ],
                "funciones": [
                    "Una función debe hacer una sola cosa bien",
                    "Usa nombres de función que describan qué hace: 'calcular_precio' no 'procesar'",
                    "Mantén las funciones cortas (menos de 20 líneas)"
                ],
                "clases": [
                    "Usa nombres de clase en singular: 'Usuario' no 'Usuarios'",
                    "Agrupa funcionalidad relacionada en la misma clase",
                    "Usa herencia solo cuando tenga sentido lógico"
                ]
            },
            "optimizacion": {
                "rendimiento": [
                    "Usa bucles 'repetir con cada' para listas grandes",
                    "Evita consultas de base de datos dentro de bucles",
                    "Considera usar cache para datos que no cambian frecuentemente"
                ],
                "memoria": [
                    "Libera recursos cuando no los necesites",
                    "Evita crear objetos innecesarios en bucles",
                    "Usa generadores para procesar datos grandes"
                ]
            },
            "seguridad": [
                "Siempre valida los datos de entrada del usuario",
                "Usa HTTPS para todas las comunicaciones",
                "No hardcodees contraseñas o claves API en el código",
                "Sanitiza datos antes de guardarlos en la base de datos"
            ]
        }
    
    def _load_error_patterns(self) -> List[Dict]:
        """Cargar patrones de errores comunes"""
        return [
            {
                "pattern": r"mostrar\s+[^\"']",
                "error": "Falta comillas en el texto a mostrar",
                "suggestion": "Usa comillas: mostrar \"tu mensaje\"",
                "severity": "error"
            },
            {
                "pattern": r"si\s+.*\s+entonces",
                "error": "No uses 'entonces' en Vader",
                "suggestion": "Usa solo 'si condicion' sin 'entonces'",
                "severity": "warning"
            },
            {
                "pattern": r"for\s+.*\s+in\s+",
                "error": "Sintaxis de otros lenguajes detectada",
                "suggestion": "Usa 'repetir con cada elemento en lista'",
                "severity": "error"
            },
            {
                "pattern": r"function\s+\w+",
                "error": "Sintaxis de JavaScript detectada",
                "suggestion": "Usa 'funcion nombre_funcion'",
                "severity": "error"
            },
            {
                "pattern": r"def\s+\w+",
                "error": "Sintaxis de Python detectada",
                "suggestion": "Usa 'funcion nombre_funcion'",
                "severity": "error"
            },
            {
                "pattern": r"fin\s+(?!si|funcion|clase|repetir|con|estilos|pagina|componente)",
                "error": "Palabra 'fin' sin contexto válido",
                "suggestion": "Usa 'fin si', 'fin funcion', 'fin clase', etc.",
                "severity": "warning"
            }
        ]
    
    def generate_code_from_description(self, description: str) -> str:
        """Genera código Vader basado en una descripción en español"""
        description_lower = description.lower()
        
        # Detectar tipo de aplicación
        app_type = self._detect_app_type(description_lower)
        
        if app_type == "sitio_web":
            return self._generate_website_code(description)
        elif app_type == "app_movil":
            return self._generate_mobile_app_code(description)
        elif app_type == "api":
            return self._generate_api_code(description)
        elif app_type == "analisis_datos":
            return self._generate_data_analysis_code(description)
        else:
            return self._generate_generic_code(description)
    
    def _detect_app_type(self, description: str) -> str:
        """Detecta el tipo de aplicación basado en la descripción"""
        web_keywords = ["sitio", "web", "página", "tienda", "blog", "ecommerce"]
        mobile_keywords = ["app", "móvil", "celular", "teléfono", "android", "ios"]
        api_keywords = ["api", "servicio", "backend", "servidor", "rest"]
        data_keywords = ["datos", "análisis", "estadística", "gráfico", "reporte"]
        
        if any(keyword in description for keyword in web_keywords):
            return "sitio_web"
        elif any(keyword in description for keyword in mobile_keywords):
            return "app_movil"
        elif any(keyword in description for keyword in api_keywords):
            return "api"
        elif any(keyword in description for keyword in data_keywords):
            return "analisis_datos"
        else:
            return "generico"
    
    def _generate_website_code(self, description: str) -> str:
        """Genera código para un sitio web"""
        return '''# Sitio web generado automáticamente por Vader AI
usar plantilla "web_basica" con titulo="Mi Sitio Web", descripcion="Sitio creado con IA", autor="Usuario Vader"

# Contenido personalizado
seccion id="inicio"
    titulo1 "Bienvenido a Mi Sitio"
    parrafo "Este sitio fue generado automáticamente por la IA de Vader."
    
    usar componente "boton_moderno" con texto="Empezar", color="azul", tamaño="grande"
fin seccion

seccion id="servicios"
    titulo2 "Nuestros Servicios"
    
    div clase="servicios-grid"
        usar componente "tarjeta_producto" con nombre="Servicio 1", precio="99", descripcion="Descripción del servicio", disponible="true"
        usar componente "tarjeta_producto" con nombre="Servicio 2", precio="149", descripcion="Descripción del servicio", disponible="true"
        usar componente "tarjeta_producto" con nombre="Servicio 3", precio="199", descripcion="Descripción del servicio", disponible="true"
    fin div
fin seccion

# Estilos automáticos
estilos
    .servicios-grid
        display "grid"
        grid_template_columns "repeat(auto-fit, minmax(300px, 1fr))"
        gap "2rem"
        relleno "2rem 0"
    fin .servicios-grid
    
    en_movil
        .servicios-grid
            grid_template_columns "1fr"
        fin .servicios-grid
    fin en_movil
fin estilos'''
    
    def _generate_mobile_app_code(self, description: str) -> str:
        """Genera código para una aplicación móvil"""
        return '''# Aplicación móvil generada automáticamente por Vader AI
app flutter "MiApp"
    widget "HomePage"
        estado "contador" = 0
        estado "usuario" = ""
        
        scaffold
            appBar "Mi Aplicación"
            body
                columna
                    relleno "2rem"
                    
                    texto "¡Bienvenido a tu app!"
                        estilo tamaño=24, peso="bold"
                    fin texto
                    
                    espacio altura="2rem"
                    
                    campo_texto
                        placeholder "Ingresa tu nombre"
                        onChanged (valor) => setState(() => usuario = valor)
                    fin campo_texto
                    
                    espacio altura="2rem"
                    
                    si usuario != ""
                        texto "¡Hola $usuario!"
                            estilo color="azul", tamaño=18
                        fin texto
                    fin si
                    
                    espacio altura="2rem"
                    
                    texto "Contador: $contador"
                        estilo tamaño=20
                    fin texto
                    
                    espacio altura="1rem"
                    
                    boton "Incrementar"
                        onPressed () => setState(() => contador++)
                        estilo color="verde", relleno="1rem 2rem"
                    fin boton
                fin columna
            fin body
        fin scaffold
    fin widget
fin app'''
    
    def _generate_api_code(self, description: str) -> str:
        """Genera código para una API REST"""
        return '''# API REST generada automáticamente por Vader AI
servidor fastapi
    titulo "Mi API Generada"
    version "1.0.0"
    descripcion "API creada automáticamente por Vader AI"
    
    # Modelo de datos
    modelo "Usuario"
        campo "id" entero opcional
        campo "nombre" texto requerido
        campo "email" email requerido
        campo "activo" booleano default=verdadero
    fin modelo
    
    # Base de datos en memoria (para demo)
    variable "usuarios_db" = []
    
    # Rutas de la API
    ruta get "/"
        retornar {
            "mensaje": "¡API funcionando!",
            "version": "1.0.0",
            "generada_por": "Vader AI"
        }
    fin ruta
    
    ruta get "/usuarios"
        retornar usuarios_db
    fin ruta
    
    ruta post "/usuarios"
        usuario = obtener_datos_json()
        usuario["id"] = len(usuarios_db) + 1
        usuarios_db.append(usuario)
        retornar {"mensaje": "Usuario creado", "usuario": usuario}
    fin ruta
    
    ruta get "/usuarios/{id}"
        id_usuario = obtener_parametro("id")
        usuario = buscar_en(usuarios_db, "id", id_usuario)
        si usuario
            retornar usuario
        sino
            retornar_error(404, "Usuario no encontrado")
        fin si
    fin ruta
    
    ruta put "/usuarios/{id}"
        id_usuario = obtener_parametro("id")
        datos = obtener_datos_json()
        usuario = actualizar_en(usuarios_db, "id", id_usuario, datos)
        si usuario
            retornar {"mensaje": "Usuario actualizado", "usuario": usuario}
        sino
            retornar_error(404, "Usuario no encontrado")
        fin si
    fin ruta
    
    ruta delete "/usuarios/{id}"
        id_usuario = obtener_parametro("id")
        eliminado = eliminar_de(usuarios_db, "id", id_usuario)
        si eliminado
            retornar {"mensaje": "Usuario eliminado"}
        sino
            retornar_error(404, "Usuario no encontrado")
        fin si
    fin ruta
fin servidor'''
    
    def _generate_data_analysis_code(self, description: str) -> str:
        """Genera código para análisis de datos"""
        return '''# Análisis de datos generado automáticamente por Vader AI
# Cargar y analizar datos

cargar datos "datos.csv" como "dataset"

# Información básica del dataset
mostrar "=== INFORMACIÓN DEL DATASET ==="
mostrar resumen dataset
mostrar dimensiones dataset

# Estadísticas descriptivas
mostrar "=== ESTADÍSTICAS DESCRIPTIVAS ==="
estadisticas dataset

# Visualizaciones automáticas
mostrar "=== GENERANDO GRÁFICOS ==="

# Histograma de variables numéricas
columnas_numericas = obtener_columnas_numericas(dataset)
repetir con cada columna en columnas_numericas
    histograma columna
    guardar_grafico "histograma_" + columna + ".png"
fin repetir

# Gráfico de barras para variables categóricas
columnas_categoricas = obtener_columnas_categoricas(dataset)
repetir con cada columna en columnas_categoricas
    grafico_barras columna
    guardar_grafico "barras_" + columna + ".png"
fin repetir

# Matriz de correlación
si len(columnas_numericas) > 1
    matriz_correlacion columnas_numericas
    guardar_grafico "correlacion.png"
fin si

# Análisis avanzado
mostrar "=== ANÁLISIS AVANZADO ==="

# Detectar valores faltantes
valores_faltantes = contar_valores_faltantes(dataset)
si valores_faltantes > 0
    mostrar "Valores faltantes encontrados: " + str(valores_faltantes)
    grafico_valores_faltantes dataset
    guardar_grafico "valores_faltantes.png"
fin si

# Detectar outliers
outliers = detectar_outliers(dataset, columnas_numericas)
si len(outliers) > 0
    mostrar "Outliers detectados: " + str(len(outliers))
    grafico_outliers dataset, columnas_numericas
    guardar_grafico "outliers.png"
fin si

# Generar reporte
generar_reporte_html dataset, "reporte_analisis.html"
mostrar "=== ANÁLISIS COMPLETADO ==="
mostrar "Revisa los archivos generados y el reporte HTML"'''
    
    def _generate_generic_code(self, description: str) -> str:
        """Genera código genérico basado en la descripción"""
        return f'''# Código generado automáticamente por Vader AI
# Basado en: "{description}"

# Programa principal
funcion principal
    mostrar "¡Hola! Este programa fue generado por Vader AI"
    mostrar "Descripción: {description}"
    
    # Aquí puedes agregar tu lógica específica
    # La IA de Vader ha preparado la estructura básica
    
    preguntar "¿Cómo te llamas?" guardar la respuesta en nombre
    mostrar "¡Hola " + nombre + "! Tu programa está listo."
fin funcion

# Ejecutar programa
principal()'''
    
    def analyze_code(self, code: str) -> Dict:
        """Analiza el código y proporciona sugerencias"""
        analysis = {
            "errors": [],
            "warnings": [],
            "suggestions": [],
            "metrics": {},
            "score": 0
        }
        
        # Detectar errores de sintaxis
        for error_pattern in self.error_patterns:
            matches = re.finditer(error_pattern["pattern"], code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                error_info = {
                    "line": line_num,
                    "message": error_pattern["error"],
                    "suggestion": error_pattern["suggestion"],
                    "severity": error_pattern["severity"],
                    "position": match.span()
                }
                
                if error_pattern["severity"] == "error":
                    analysis["errors"].append(error_info)
                else:
                    analysis["warnings"].append(error_info)
        
        # Calcular métricas
        lines = code.split('\n')
        analysis["metrics"] = {
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
            "functions": len(re.findall(r'funcion\s+\w+', code, re.IGNORECASE)),
            "classes": len(re.findall(r'clase\s+\w+', code, re.IGNORECASE)),
            "complexity_score": self._calculate_complexity(code)
        }
        
        # Generar sugerencias
        analysis["suggestions"] = self._generate_suggestions(code, analysis["metrics"])
        
        # Calcular score general
        analysis["score"] = self._calculate_code_score(analysis)
        
        return analysis
    
    def _calculate_complexity(self, code: str) -> int:
        """Calcula la complejidad del código"""
        complexity = 0
        
        # Contar estructuras de control
        complexity += len(re.findall(r'\bsi\b', code, re.IGNORECASE))
        complexity += len(re.findall(r'\brepetir\b', code, re.IGNORECASE))
        complexity += len(re.findall(r'\bintentarb', code, re.IGNORECASE))
        
        # Contar funciones y clases
        complexity += len(re.findall(r'\bfuncion\b', code, re.IGNORECASE)) * 2
        complexity += len(re.findall(r'\bclase\b', code, re.IGNORECASE)) * 3
        
        return complexity
    
    def _generate_suggestions(self, code: str, metrics: Dict) -> List[str]:
        """Genera sugerencias de mejora"""
        suggestions = []
        
        # Sugerencias basadas en métricas
        if metrics["comment_lines"] / max(metrics["code_lines"], 1) < 0.1:
            suggestions.append("Considera agregar más comentarios para explicar tu código")
        
        if metrics["complexity_score"] > 20:
            suggestions.append("El código parece complejo. Considera dividirlo en funciones más pequeñas")
        
        # Sugerencias basadas en patrones
        if "mostrar" in code and "preguntar" not in code:
            suggestions.append("Podrías hacer tu programa más interactivo agregando entrada del usuario")
        
        if "funcion" not in code and metrics["code_lines"] > 10:
            suggestions.append("Considera organizar tu código en funciones para mejor legibilidad")
        
        if "clase" not in code and metrics["code_lines"] > 30:
            suggestions.append("Para código más largo, considera usar programación orientada a objetos")
        
        return suggestions
    
    def _calculate_code_score(self, analysis: Dict) -> int:
        """Calcula un score de calidad del código (0-100)"""
        score = 100
        
        # Penalizar errores
        score -= len(analysis["errors"]) * 10
        score -= len(analysis["warnings"]) * 5
        
        # Penalizar complejidad alta
        if analysis["metrics"]["complexity_score"] > 30:
            score -= 20
        elif analysis["metrics"]["complexity_score"] > 20:
            score -= 10
        
        # Bonificar buenas prácticas
        if analysis["metrics"]["comment_lines"] > 0:
            score += 5
        
        if analysis["metrics"]["functions"] > 0:
            score += 10
        
        return max(0, min(100, score))
    
    def suggest_improvements(self, code: str) -> List[str]:
        """Sugiere mejoras específicas para el código"""
        improvements = []
        
        # Detectar patrones mejorables
        if re.search(r'mostrar\s+".*"\s*\+', code):
            improvements.append("Usa interpolación de strings: mostrar \"Hola {nombre}\" en lugar de concatenación")
        
        if re.search(r'repetir\s+\w+\s+desde\s+1\s+hasta\s+\d+', code):
            improvements.append("Para listas, usa 'repetir con cada elemento en lista' que es más eficiente")
        
        if re.search(r'si.*\n\s*mostrar', code) and not re.search(r'sino', code):
            improvements.append("Considera agregar casos 'sino' para manejar todas las posibilidades")
        
        return improvements

# Funciones de utilidad para detección de sintaxis
def detect_ai_assistance_needed(code: str) -> bool:
    """Detecta si el código necesita asistencia de IA"""
    ai_keywords = [
        "ayuda", "generar", "crear automáticamente", "sugerir", "mejorar",
        "optimizar", "corregir", "completar", "ai", "inteligencia artificial"
    ]
    
    return any(keyword in code.lower() for keyword in ai_keywords)

def extract_user_intent(code: str) -> str:
    """Extrae la intención del usuario del código"""
    # Buscar comentarios que indiquen intención
    intent_patterns = [
        r'#\s*quiero\s+(.*)',
        r'#\s*necesito\s+(.*)',
        r'#\s*crear\s+(.*)',
        r'#\s*hacer\s+(.*)'
    ]
    
    for pattern in intent_patterns:
        match = re.search(pattern, code, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return "código genérico"

# Instancia global del asistente
vader_ai = VaderAIAssistant()
