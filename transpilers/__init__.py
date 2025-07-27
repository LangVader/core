# Transpilers module for Vader
# Provides transpilation to multiple target languages

__version__ = "7.0.0"
__author__ = "Vader Team"

# Import all transpilers
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
from . import html
from . import css
from . import gui_advanced
from . import electron

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
