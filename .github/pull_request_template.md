## 📋 Descripción

Describe brevemente los cambios realizados en este PR.

## 🎯 Tipo de Cambio

- [ ] 🐛 Bug fix (cambio que corrige un problema)
- [ ] ✨ Nueva característica (cambio que agrega funcionalidad)
- [ ] 💥 Breaking change (cambio que rompe compatibilidad)
- [ ] 📚 Documentación (cambios solo en documentación)
- [ ] 🔧 Refactoring (cambio que no corrige bugs ni agrega características)
- [ ] 🧪 Tests (agregar o corregir tests)
- [ ] 🏗️ Build/CI (cambios en build o CI)

## 🔗 Issues Relacionados

Fixes #(número de issue)
Closes #(número de issue)
Related to #(número de issue)

## 📝 Cambios Realizados

### Archivos Modificados
- [ ] `src/vader.py` - Descripción del cambio
- [ ] `transpilers/nuevo_lenguaje.py` - Descripción del cambio
- [ ] `test_nuevo_transpilador.py` - Descripción del cambio

### Nuevos Archivos
- [ ] `transpilers/nuevo_lenguaje.py` - Nuevo transpilador para X
- [ ] `examples/ejemplo_nuevo.vdr` - Ejemplo de uso

## 🧪 Testing

### Tests Ejecutados
- [ ] `python test_transpilers.py` ✅
- [ ] `python test_new_transpilers.py` ✅
- [ ] `python test_flask_app_generator.py` ✅
- [ ] `pytest -v --cov=src/ --cov=transpilers/` ✅

### Nuevos Tests Agregados
- [ ] Tests unitarios para nueva funcionalidad
- [ ] Tests de integración
- [ ] Tests de regresión

### Cobertura de Tests
- Cobertura actual: ___%
- Cobertura después de cambios: ___%

## 📚 Documentación

- [ ] README.md actualizado
- [ ] Documentación técnica actualizada
- [ ] Ejemplos agregados/actualizados
- [ ] CHANGELOG.md actualizado
- [ ] Comentarios en código agregados

## ✅ Checklist

### Código
- [ ] El código sigue las convenciones del proyecto
- [ ] He ejecutado `black` para formatear el código
- [ ] He ejecutado `flake8` y no hay errores de linting
- [ ] He agregado type hints donde es apropiado
- [ ] El código es legible y está bien comentado

### Tests
- [ ] Todos los tests existentes pasan
- [ ] He agregado tests para la nueva funcionalidad
- [ ] Los tests cubren casos edge importantes
- [ ] He probado manualmente la funcionalidad

### Documentación
- [ ] He actualizado la documentación relevante
- [ ] He agregado ejemplos de uso
- [ ] Los comentarios en el código están actualizados

### Compatibilidad
- [ ] Los cambios son compatibles con versiones anteriores
- [ ] Si hay breaking changes, están documentados
- [ ] He considerado el impacto en otros transpiladores

## 🖥️ Entorno de Pruebas

- **OS**: [ej. macOS 14.0, Ubuntu 22.04]
- **Python**: [ej. 3.10.8]
- **Dependencias**: [versiones relevantes]

## 📸 Capturas de Pantalla (si aplica)

<!-- Agregar capturas de pantalla para cambios en UI o salida visual -->

## 🔍 Notas Adicionales

<!-- Cualquier información adicional que los reviewers deberían saber -->

## 📋 Para Reviewers

### Áreas de Enfoque
- [ ] Lógica de transpilación correcta
- [ ] Manejo de errores robusto
- [ ] Performance aceptable
- [ ] Cobertura de tests adecuada
- [ ] Documentación clara

### Preguntas Específicas
1. ¿La implementación maneja correctamente los casos edge?
2. ¿Los tests cubren todos los escenarios importantes?
3. ¿La documentación es clara y completa?

---

**Nota**: Por favor revisa todos los items del checklist antes de solicitar review.
