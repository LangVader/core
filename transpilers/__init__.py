# Transpilers module for Vader
# Provides transpilation to multiple target languages

__version__ = "7.0.0"
__author__ = "Vader Team"

# Import all transpilers with error handling
try:
    from . import python
    from . import javascript
    from . import java
    from . import csharp
    from . import go
    from . import rust
    from . import swift
    from . import kotlin
    from . import typescript
    from . import dart
    from . import php
    from . import ruby
    from . import solidity
    from . import vader_html as html  # Usar vader_html para evitar conflicto
    from . import css
    from . import gui_advanced
    from . import electron
except ImportError as e:
    print(f"Warning: Some transpilers could not be imported: {e}")
    # Crear módulos de respaldo
    class DummyTranspiler:
        def transpile_to_python(self, code): return code
        def transpile_to_javascript(self, code): return code
        def transpilar(self, code): return code
    
    python = javascript = java = csharp = go = rust = swift = kotlin = DummyTranspiler()
    typescript = dart = php = ruby = solidity = html = css = gui_advanced = electron = DummyTranspiler()

# Available transpilers
AVAILABLE_TRANSPILERS = {
    'python': python,
    'javascript': javascript,
    'js': javascript,
    'java': java,
    'csharp': csharp,
    'cs': csharp,
    'go': go,
    'rust': rust,
    'swift': swift,
    'kotlin': kotlin,
    'typescript': typescript,
    'ts': typescript,
    'dart': dart,
    'php': php,
    'ruby': ruby,
    'solidity': solidity,
    'sol': solidity,
    'html': html,
    'css': css,
    'gui': gui_advanced,
    'electron': electron
}

def get_transpiler(target_language):
    """Get transpiler for target language"""
    return AVAILABLE_TRANSPILERS.get(target_language.lower())

def list_available_languages():
    """List all available target languages"""
    return list(AVAILABLE_TRANSPILERS.keys())
