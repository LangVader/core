# Contribuir a Vader

¡Gracias por tu interés en contribuir a Vader! Este documento te guiará a través del proceso de contribución.

## 🚀 Comenzando

### Prerrequisitos
- Python 3.8 o superior
- Git
- Conocimientos básicos de programación

### Configuración del Entorno de Desarrollo

1. **Fork del repositorio**
   ```bash
   # Haz fork del repositorio en GitHub, luego clónalo
   git clone https://github.com/tu-usuario/vader.git
   cd vader
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Verificar instalación**
   ```bash
   python src/vader.py --version
   python test_transpilers.py
   ```

## 🎯 Tipos de Contribuciones

### 🐛 Reportar Bugs
- Usa el template de bug report
- Incluye información del sistema
- Proporciona código Vader que reproduce el problema
- Incluye la salida del error completa

### ✨ Solicitar Características
- Usa el template de feature request
- Explica el caso de uso
- Proporciona ejemplos de código
- Considera el impacto en el ecosistema

### 🔧 Contribuciones de Código

#### Nuevos Transpiladores
Para agregar soporte a un nuevo lenguaje:

1. **Crear el transpilador**
   ```bash
   # Crear archivo en transpilers/nuevo_lenguaje.py
   touch transpilers/nuevo_lenguaje.py
   ```

2. **Implementar la clase**
   ```python
   class NuevoLenguajeTranspiler:
       def __init__(self):
           self.indent_level = 0
           
       def transpile(self, vader_code):
           # Implementar lógica de transpilación
           pass
   ```

3. **Agregar tests**
   ```bash
   # Crear tests en test_nuevo_lenguaje.py
   python -m pytest test_nuevo_lenguaje.py -v
   ```

4. **Actualizar documentación**
   - Agregar ejemplos
   - Actualizar README.md
   - Documentar sintaxis específica

#### Mejoras a Transpiladores Existentes
1. Identificar el problema o mejora
2. Escribir tests que fallen
3. Implementar la solución
4. Verificar que todos los tests pasen
5. Actualizar documentación si es necesario

#### Generadores de Aplicaciones
Para nuevos tipos de aplicaciones:

1. **Crear generador**
   ```python
   # En src/app_generator.py
   def generate_nueva_app(self, vader_code, output_dir):
       # Implementar generación
       pass
   ```

2. **Agregar tests**
   ```python
   # En test_app_generator.py
   def test_generate_nueva_app():
       # Implementar tests
       pass
   ```

## 📋 Proceso de Desarrollo

### 1. Crear Branch
```bash
git checkout -b feature/nueva-caracteristica
# o
git checkout -b fix/corregir-bug
```

### 2. Hacer Cambios
- Sigue las convenciones de código
- Escribe tests para nuevas características
- Actualiza documentación

### 3. Ejecutar Tests
```bash
# Tests básicos
python test_transpilers.py
python test_new_transpilers.py
python test_flask_app_generator.py

# Tests con pytest
pytest -v --cov=src/ --cov=transpilers/

# Verificar calidad de código
black --check src/ transpilers/
flake8 src/ transpilers/
```

### 4. Commit y Push
```bash
git add .
git commit -m "feat: agregar transpilador para Kotlin"
git push origin feature/nueva-caracteristica
```

### 5. Crear Pull Request
- Usa el template de PR
- Describe los cambios claramente
- Incluye tests y documentación
- Vincula issues relacionados

## 📝 Convenciones de Código

### Estilo de Código
- Usar **Black** para formateo automático
- Seguir **PEP 8** para Python
- Usar **type hints** cuando sea posible
- Documentar funciones y clases

### Convenciones de Commit
Usar [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: agregar nueva característica
fix: corregir bug
docs: actualizar documentación
test: agregar o corregir tests
refactor: refactorizar código
style: cambios de formato
chore: tareas de mantenimiento
```

### Estructura de Archivos
```
vader/
├── src/                    # Código principal
├── transpilers/           # Transpiladores por lenguaje
├── examples/              # Ejemplos de código Vader
├── tests/                 # Tests adicionales
├── docs/                  # Documentación
├── templates/             # Plantillas para generadores
└── .github/              # Configuración GitHub
```

## 🧪 Testing

### Ejecutar Tests Localmente
```bash
# Todos los tests
python -m pytest

# Tests específicos
python test_transpilers.py
python test_new_transpilers.py

# Con coverage
pytest --cov=src/ --cov=transpilers/ --cov-report=html
```

### Escribir Tests
```python
def test_nueva_caracteristica():
    """Test para nueva característica"""
    # Arrange
    vader_code = "codigo de prueba"
    
    # Act
    resultado = transpilador.transpile(vader_code)
    
    # Assert
    assert "resultado esperado" in resultado
```

## 📚 Documentación

### Actualizar Documentación
- README.md para cambios principales
- Archivos en docs/ para documentación detallada
- Comentarios en código para funciones complejas
- Ejemplos en examples/ para nuevas características

### Generar Documentación
```bash
mkdocs serve  # Servidor local
mkdocs build  # Generar sitio estático
```

## 🔍 Code Review

### Como Autor
- Asegúrate de que todos los tests pasen
- Incluye descripción clara de los cambios
- Responde a comentarios constructivamente
- Mantén el PR enfocado en un solo tema

### Como Reviewer
- Sé constructivo y específico
- Verifica que los tests cubran los casos importantes
- Revisa que la documentación esté actualizada
- Considera el impacto en el ecosistema completo

## 🏷️ Releases

Los releases siguen [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Cambios incompatibles
- **MINOR** (0.X.0): Nuevas características compatibles
- **PATCH** (0.0.X): Correcciones de bugs

## 🤝 Comunidad

### Comunicación
- GitHub Issues para bugs y características
- GitHub Discussions para preguntas generales
- Pull Requests para contribuciones de código

### Código de Conducta
- Sé respetuoso y constructivo
- Ayuda a otros contribuidores
- Mantén un ambiente inclusivo y acogedor

## ❓ Preguntas Frecuentes

### ¿Cómo agregar un nuevo lenguaje objetivo?
1. Crear transpilador en `transpilers/`
2. Implementar tests
3. Actualizar CLI principal
4. Agregar documentación y ejemplos

### ¿Cómo reportar un bug de seguridad?
Para vulnerabilidades de seguridad, envía un email privado en lugar de crear un issue público.

### ¿Puedo contribuir sin saber programar?
¡Sí! Puedes contribuir con:
- Documentación
- Traduciones
- Ejemplos de código Vader
- Reportes de bugs
- Sugerencias de mejoras

## 🙏 Reconocimientos

¡Gracias a todos los contribuidores que hacen posible Vader!

---

¿Tienes preguntas? ¡No dudes en crear un issue o iniciar una discusión!
