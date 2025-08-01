#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 8.0 - MOTOR UNIVERSAL
===========================
Motor principal que integra sintaxis ultra-natural con conectores universales

Características:
- Procesamiento de lenguaje ultra-natural
- Detección automática de dominios tecnológicos
- Generación de código específico para cada tecnología
- Integración completa del ecosistema Vader
- Soporte para TODAS las tecnologías del mundo

Autor: Vader Team
Versión: 8.0.0 "Universal Engine"
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

# Importar módulos de Vader
try:
    from vader_ultra_natural_syntax import VaderUltraNaturalSyntax
    from vader_universal_connectors import VaderUniversalConnectors, ConnectorResult
    from vader_universal_parser import VaderUniversalParser
except ImportError:
    print("⚠️  Algunos módulos de Vader no están disponibles. Continuando con funcionalidad básica.")

@dataclass
class UniversalResult:
    """Resultado del procesamiento universal"""
    success: bool
    original_text: str
    detected_domains: List[str]
    natural_syntax_used: bool
    generated_code: Dict[str, str]
    dependencies: List[str]
    hardware_required: List[str]
    api_keys_needed: List[str]
    instructions: List[str]
    execution_ready: bool

class VaderUniversalEngine:
    """Motor universal de Vader que integra toda la funcionalidad"""
    
    def __init__(self):
        print("🚀 Iniciando Vader Universal Engine...")
        self.natural_syntax = VaderUltraNaturalSyntax()
        self.connectors = VaderUniversalConnectors()
        self.parser = None
        
        try:
            self.parser = VaderUniversalParser()
        except:
            print("⚠️  Parser universal no disponible, usando funcionalidad básica")
        
        self.session_context = {
            'variables': {},
            'functions': {},
            'imports': set(),
            'current_domain': None,
            'execution_history': []
        }
        
        print("✅ Vader Universal Engine iniciado correctamente")
    
    def process_universal_code(self, input_text: str) -> UniversalResult:
        """Procesa código universal de Vader"""
        print(f"\n🔄 Procesando: {input_text[:50]}...")
        
        # 1. Detectar dominios tecnológicos
        detected_domains = self.connectors.detect_domain(input_text)
        print(f"📡 Dominios detectados: {detected_domains}")
        
        # 2. Procesar sintaxis natural
        natural_parsed = self.natural_syntax.parse_natural_text(input_text)
        natural_syntax_used = len(natural_parsed) > 0
        
        if natural_syntax_used:
            print(f"🗣️  Sintaxis natural detectada: {len(natural_parsed)} patrones")
        
        # 3. Generar código para cada dominio
        generated_code = {}
        all_dependencies = set()
        all_hardware = set()
        all_api_keys = set()
        all_instructions = []
        
        if detected_domains:
            for domain in detected_domains:
                print(f"⚙️  Generando código para dominio: {domain}")
                result = self.connectors.generate_code(input_text, domain)
                
                if result.success:
                    generated_code[domain] = result.code
                    all_dependencies.update(result.dependencies)
                    all_hardware.update(result.hardware_required)
                    all_api_keys.update(result.api_keys_needed)
                    all_instructions.append(f"{domain.upper()}: {result.instructions}")
        
        # 4. Generar código base de Vader si hay sintaxis natural
        if natural_syntax_used:
            vader_code = self.natural_syntax.generate_code(input_text)
            generated_code['vader'] = vader_code
            print("💻 Código Vader base generado")
        
        # 5. Usar parser universal si está disponible
        if self.parser:
            try:
                parser_result = self.parser.parse_universal_input(input_text)
                if parser_result and parser_result.get('generated_code'):
                    generated_code.update(parser_result['generated_code'])
                    print("🔧 Parser universal aplicado")
            except Exception as e:
                print(f"⚠️  Error en parser universal: {e}")
        
        # 6. Determinar si está listo para ejecución
        execution_ready = self._is_execution_ready(generated_code, all_dependencies)
        
        result = UniversalResult(
            success=len(generated_code) > 0,
            original_text=input_text,
            detected_domains=detected_domains,
            natural_syntax_used=natural_syntax_used,
            generated_code=generated_code,
            dependencies=list(all_dependencies),
            hardware_required=list(all_hardware),
            api_keys_needed=list(all_api_keys),
            instructions=all_instructions,
            execution_ready=execution_ready
        )
        
        # 7. Actualizar contexto de sesión
        self._update_session_context(result)
        
        return result
    
    def _is_execution_ready(self, generated_code: Dict[str, str], dependencies: List[str]) -> bool:
        """Determina si el código está listo para ejecutar"""
        if not generated_code:
            return False
        
        # Verificar dependencias básicas
        basic_deps = ['os', 'sys', 'json', 're']
        missing_deps = [dep for dep in dependencies if dep not in basic_deps]
        
        return len(missing_deps) == 0 or 'vader' in generated_code
    
    def _update_session_context(self, result: UniversalResult):
        """Actualiza el contexto de la sesión"""
        self.session_context['execution_history'].append({
            'input': result.original_text,
            'domains': result.detected_domains,
            'success': result.success,
            'timestamp': self._get_timestamp()
        })
        
        # Mantener solo los últimos 10 elementos
        if len(self.session_context['execution_history']) > 10:
            self.session_context['execution_history'] = self.session_context['execution_history'][-10:]
    
    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def execute_generated_code(self, result: UniversalResult, domain: str = 'vader') -> Dict[str, Any]:
        """Ejecuta el código generado para un dominio específico"""
        if domain not in result.generated_code:
            return {'success': False, 'error': f'No hay código para el dominio {domain}'}
        
        code = result.generated_code[domain]
        execution_result = {
            'success': False,
            'output': '',
            'error': '',
            'domain': domain
        }
        
        try:
            print(f"🚀 Ejecutando código {domain}...")
            
            # Crear un namespace seguro para la ejecución
            safe_namespace = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip
                }
            }
            
            # Ejecutar el código
            exec(code, safe_namespace)
            
            execution_result['success'] = True
            execution_result['output'] = f'Código {domain} ejecutado exitosamente'
            print(f"✅ Código {domain} ejecutado correctamente")
            
        except Exception as e:
            execution_result['error'] = str(e)
            print(f"❌ Error ejecutando código {domain}: {e}")
        
        return execution_result
    
    def get_available_domains(self) -> List[str]:
        """Obtiene lista de dominios disponibles"""
        return list(self.connectors.connectors.keys())
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la sesión actual"""
        history = self.session_context['execution_history']
        
        return {
            'total_executions': len(history),
            'successful_executions': sum(1 for h in history if h['success']),
            'domains_used': list(set(domain for h in history for domain in h['domains'])),
            'current_variables': len(self.session_context['variables']),
            'current_functions': len(self.session_context['functions']),
            'last_execution': history[-1] if history else None
        }
    
    def generate_installation_script(self, result: UniversalResult) -> str:
        """Genera script de instalación para las dependencias"""
        if not result.dependencies:
            return "# No se requieren dependencias adicionales"
        
        script = "#!/bin/bash\n"
        script += "# Script de instalación generado por Vader Universal Engine\n\n"
        script += "echo '🚀 Instalando dependencias para Vader Universal...'\n\n"
        
        # Dependencias de Python
        python_deps = [dep for dep in result.dependencies if not dep.startswith('npm:')]
        if python_deps:
            script += "# Dependencias de Python\n"
            script += f"pip install {' '.join(python_deps)}\n\n"
        
        # Dependencias de Node.js
        npm_deps = [dep.replace('npm:', '') for dep in result.dependencies if dep.startswith('npm:')]
        if npm_deps:
            script += "# Dependencias de Node.js\n"
            script += f"npm install {' '.join(npm_deps)}\n\n"
        
        # Instrucciones adicionales
        if result.api_keys_needed:
            script += "# Configurar variables de entorno para API keys:\n"
            for key in result.api_keys_needed:
                script += f"# export {key}='tu_api_key_aqui'\n"
            script += "\n"
        
        if result.hardware_required:
            script += "# Hardware requerido:\n"
            for hw in result.hardware_required:
                script += f"# - {hw}\n"
            script += "\n"
        
        script += "echo '✅ Instalación completada'\n"
        return script
    
    def save_project(self, result: UniversalResult, project_name: str, output_dir: str = "vader_projects") -> bool:
        """Guarda un proyecto completo de Vader"""
        try:
            import os
            
            # Crear directorio del proyecto
            project_path = os.path.join(output_dir, project_name)
            os.makedirs(project_path, exist_ok=True)
            
            # Guardar código generado
            for domain, code in result.generated_code.items():
                filename = f"{project_name}_{domain}.py" if domain != 'vader' else f"{project_name}.vdr"
                filepath = os.path.join(project_path, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# Código {domain} generado por Vader Universal Engine\n")
                    f.write(f"# Proyecto: {project_name}\n")
                    f.write(f"# Entrada original: {result.original_text}\n\n")
                    f.write(code)
            
            # Guardar metadatos del proyecto
            metadata = {
                'project_name': project_name,
                'created_by': 'Vader Universal Engine 8.0',
                'original_input': result.original_text,
                'detected_domains': result.detected_domains,
                'dependencies': result.dependencies,
                'hardware_required': result.hardware_required,
                'api_keys_needed': result.api_keys_needed,
                'instructions': result.instructions,
                'execution_ready': result.execution_ready
            }
            
            metadata_path = os.path.join(project_path, 'vader_project.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Guardar script de instalación
            install_script = self.generate_installation_script(result)
            install_path = os.path.join(project_path, 'install.sh')
            with open(install_path, 'w', encoding='utf-8') as f:
                f.write(install_script)
            
            # Hacer el script ejecutable
            os.chmod(install_path, 0o755)
            
            # Crear README
            readme_content = f"""# {project_name}

Proyecto generado por **Vader Universal Engine 8.0**

## Descripción
{result.original_text}

## Dominios detectados
{', '.join(result.detected_domains) if result.detected_domains else 'Ninguno'}

## Archivos generados
{chr(10).join([f'- {project_name}_{domain}.py' for domain in result.generated_code.keys()])}

## Instalación
```bash
chmod +x install.sh
./install.sh
```

## Dependencias
{chr(10).join([f'- {dep}' for dep in result.dependencies]) if result.dependencies else 'Ninguna'}

## Hardware requerido
{chr(10).join([f'- {hw}' for hw in result.hardware_required]) if result.hardware_required else 'Ninguno'}

## API Keys necesarias
{chr(10).join([f'- {key}' for key in result.api_keys_needed]) if result.api_keys_needed else 'Ninguna'}

## Instrucciones
{chr(10).join([f'- {inst}' for inst in result.instructions]) if result.instructions else 'Ejecutar directamente'}

---
Generado con ❤️ por Vader Universal Engine
"""
            
            readme_path = os.path.join(project_path, 'README.md')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"✅ Proyecto '{project_name}' guardado en: {project_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando proyecto: {e}")
            return False

def demo_vader_universal():
    """Demostración del motor universal de Vader"""
    print("🚀 DEMO: VADER UNIVERSAL ENGINE 8.0")
    print("=" * 60)
    
    engine = VaderUniversalEngine()
    
    # Casos de prueba que cubren múltiples dominios
    test_cases = [
        "crear una app web con base de datos para controlar sensores IoT",
        "entrenar un modelo de IA para predecir precios de criptomonedas",
        "hacer un juego donde el robot evite obstáculos usando sensores",
        "analizar datos de ventas y mostrar gráficos en una página web",
        "crear un smart contract para votar y conectarlo con una app móvil",
        "que temperatura sea leer sensor y si temperatura > 25 encender ventilador",
        "repetir 10 veces: mover robot adelante 5cm y girar 36 grados"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 PRUEBA {i}: {test_case}")
        print("-" * 50)
        
        # Procesar con el motor universal
        result = engine.process_universal_code(test_case)
        
        # Mostrar resultados
        print(f"✅ Éxito: {result.success}")
        print(f"📡 Dominios: {', '.join(result.detected_domains)}")
        print(f"🗣️  Sintaxis natural: {'Sí' if result.natural_syntax_used else 'No'}")
        print(f"💻 Código generado para: {', '.join(result.generated_code.keys())}")
        
        if result.dependencies:
            print(f"📦 Dependencias: {', '.join(result.dependencies[:3])}{'...' if len(result.dependencies) > 3 else ''}")
        
        if result.hardware_required:
            print(f"🔧 Hardware: {', '.join(result.hardware_required[:2])}{'...' if len(result.hardware_required) > 2 else ''}")
        
        print(f"🚀 Listo para ejecutar: {'Sí' if result.execution_ready else 'No'}")
        
        # Guardar proyecto de ejemplo
        if i <= 2:  # Solo guardar los primeros 2 proyectos
            project_name = f"demo_proyecto_{i}"
            engine.save_project(result, project_name)
    
    # Mostrar estadísticas finales
    print("\n📊 ESTADÍSTICAS DE LA SESIÓN")
    print("-" * 30)
    stats = engine.get_session_stats()
    for key, value in stats.items():
        if key != 'last_execution':
            print(f"{key}: {value}")

if __name__ == "__main__":
    demo_vader_universal()
