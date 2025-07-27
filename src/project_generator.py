#!/usr/bin/env python3
"""
Generador de Proyectos Completos para Vader
Crea proyectos completos con estructura, dependencias, documentación y configuración
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app_generator import VaderAppGenerator
from transpilers.python import PythonTranspiler
from transpilers.javascript import JavaScriptTranspiler
from transpilers.java import JavaTranspiler

class VaderProjectGenerator:
    def __init__(self):
        self.app_generator = VaderAppGenerator()
        self.supported_languages = {
            'python': {'transpiler': PythonTranspiler, 'extension': '.py'},
            'javascript': {'transpiler': JavaScriptTranspiler, 'extension': '.js'},
            'java': {'transpiler': JavaTranspiler, 'extension': '.java'}
        }
    
    def generate_complete_project(self, vader_code, project_name, output_dir="./", 
                                target_languages=['python'], project_type='web_app'):
        """Genera un proyecto completo con múltiples lenguajes y configuraciones"""
        
        print(f"🚀 Generando proyecto completo: {project_name}")
        print(f"📁 Directorio: {output_dir}")
        print(f"🎯 Lenguajes: {', '.join(target_languages)}")
        
        # Crear estructura base del proyecto
        project_dir = Path(output_dir) / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear estructura de directorios
        self._create_project_structure(project_dir, target_languages)
        
        # Generar código para cada lenguaje
        for language in target_languages:
            if language in self.supported_languages:
                self._generate_language_code(project_dir, vader_code, language)
        
        # Generar archivos de configuración
        self._generate_config_files(project_dir, project_name, target_languages, project_type)
        
        # Generar documentación
        self._generate_documentation(project_dir, project_name, vader_code, target_languages)
        
        # Generar tests básicos
        self._generate_basic_tests(project_dir, target_languages)
        
        print(f"✅ Proyecto {project_name} generado exitosamente en {project_dir}")
        return project_dir
    
    def _create_project_structure(self, project_dir, target_languages):
        """Crea la estructura de directorios del proyecto"""
        
        dirs_to_create = ['src', 'tests', 'docs', 'config', 'assets']
        
        # Directorios por lenguaje
        for language in target_languages:
            dirs_to_create.extend([f'src/{language}', f'tests/{language}'])
        
        # Crear directorios
        for dir_path in dirs_to_create:
            (project_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def _generate_language_code(self, project_dir, vader_code, language):
        """Genera código para un lenguaje específico"""
        
        lang_config = self.supported_languages[language]
        transpiler = lang_config['transpiler']()
        
        # Transpilar código
        transpiled_code = transpiler.transpile(vader_code)
        
        # Determinar nombre del archivo
        if language == 'python':
            filename = 'main.py'
        elif language == 'javascript':
            filename = 'main.js'
        elif language == 'java':
            filename = 'VaderProgram.java'
        
        # Escribir código transpilado
        code_file = project_dir / 'src' / language / filename
        
        # Agregar header al código
        header = f"""# Código generado automáticamente por Vader
# Lenguaje: {language.title()}
# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if language == 'java':
            header = header.replace('#', '//')
        elif language == 'javascript':
            header = header.replace('#', '//')
        
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(header + transpiled_code)
        
        print(f"  ✅ Código {language} generado: {code_file}")
    
    def _generate_config_files(self, project_dir, project_name, target_languages, project_type):
        """Genera archivos de configuración para cada lenguaje"""
        
        if 'python' in target_languages:
            # requirements.txt
            requirements = ["# Dependencias Python", "pytest==7.4.0"]
            if project_type == 'web_app':
                requirements.append("Flask==2.3.3")
            
            with open(project_dir / 'requirements.txt', 'w') as f:
                f.write('\n'.join(requirements))
        
        if 'javascript' in target_languages:
            # package.json
            package_json = {
                "name": project_name.lower().replace(' ', '-'),
                "version": "1.0.0",
                "description": f"Proyecto {project_name} generado con Vader",
                "main": "src/javascript/main.js",
                "scripts": {"test": "jest", "start": "node src/javascript/main.js"},
                "devDependencies": {"jest": "^29.0.0"}
            }
            
            with open(project_dir / 'package.json', 'w') as f:
                json.dump(package_json, f, indent=2)
        
        if 'java' in target_languages:
            # pom.xml básico
            pom_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.vader</groupId>
    <artifactId>{project_name.lower().replace(' ', '-')}</artifactId>
    <version>1.0.0</version>
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
</project>'''
            
            with open(project_dir / 'pom.xml', 'w') as f:
                f.write(pom_xml)
    
    def _generate_documentation(self, project_dir, project_name, vader_code, target_languages):
        """Genera documentación completa del proyecto"""
        
        # README.md principal
        readme_content = f'''# {project_name}

Proyecto generado automáticamente por **Vader**.

## 📋 Descripción

{project_name} fue creado desde código Vader y transpilado a múltiples lenguajes.

## 🚀 Lenguajes Soportados

{chr(10).join([f"- **{lang.title()}**: `src/{lang}/`" for lang in target_languages])}

## 🛠️ Ejecución

### Python
```bash
pip install -r requirements.txt
python src/python/main.py
```

### JavaScript
```bash
npm install
npm start
```

### Java
```bash
mvn compile exec:java
```

## 📝 Código Vader Original

```vader
{vader_code.strip()}
```

## 🏗️ Estructura del Proyecto

```
{project_name}/
├── src/                    # Código fuente
{chr(10).join([f"│   ├── {lang}/" for lang in target_languages])}
├── tests/                  # Pruebas
├── docs/                   # Documentación
└── config/                 # Configuración
```

## 🧪 Testing

```bash
# Python: pytest tests/
# JavaScript: npm test
# Java: mvn test
```

---

**Generado con Vader** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
        
        with open(project_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Guía de desarrollo
        dev_guide = f'''# Guía de Desarrollo - {project_name}

## 🔧 Configuración del Entorno

### Herramientas Recomendadas
- Visual Studio Code
- Git
- Gestores de dependencias por lenguaje

## 🏗️ Arquitectura

El proyecto mantiene la misma lógica en cada lenguaje, adaptada a las convenciones específicas.

## 🧪 Testing

Cada lenguaje tiene su suite de tests:
- **Python**: pytest
- **JavaScript**: Jest
- **Java**: JUnit

## 🚀 Despliegue

### Desarrollo
Cada lenguaje puede ejecutarse independientemente para desarrollo.

### Producción
Se recomienda containerizar con Docker para despliegue uniforme.

## 📝 Convenciones

- **Python**: PEP 8
- **JavaScript**: ESLint
- **Java**: Google Style Guide
'''
        
        with open(project_dir / 'docs' / 'development.md', 'w', encoding='utf-8') as f:
            f.write(dev_guide)
    
    def _generate_basic_tests(self, project_dir, target_languages):
        """Genera tests básicos para cada lenguaje"""
        
        if 'python' in target_languages:
            python_test = '''#!/usr/bin/env python3
import unittest

class TestVaderCode(unittest.TestCase):
    def test_basic(self):
        """Test básico de funcionalidad"""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''
            with open(project_dir / 'tests' / 'python' / 'test_main.py', 'w') as f:
                f.write(python_test)
        
        if 'javascript' in target_languages:
            js_test = '''describe('Vader Code Tests', () => {
    test('funcionalidad básica', () => {
        expect(true).toBe(true);
    });
});
'''
            with open(project_dir / 'tests' / 'javascript' / 'main.test.js', 'w') as f:
                f.write(js_test)
        
        if 'java' in target_languages:
            java_test = '''import org.junit.Test;
import static org.junit.Assert.*;

public class VaderTest {
    @Test
    public void testBasic() {
        assertTrue("Test básico", true);
    }
}
'''
            with open(project_dir / 'tests' / 'java' / 'VaderTest.java', 'w') as f:
                f.write(java_test)

# Función de utilidad para uso directo
def generate_project(vader_code, project_name, output_dir="./", target_languages=['python']):
    """Función de conveniencia para generar proyectos"""
    generator = VaderProjectGenerator()
    return generator.generate_complete_project(vader_code, project_name, output_dir, target_languages)
