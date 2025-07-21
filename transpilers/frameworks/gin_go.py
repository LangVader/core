# Transpilador Gin (Go) para Vader
# Convierte sintaxis natural a Gin framework para APIs ultra rápidas

def transpile_gin(code):
    """Transpila código Vader a Gin (Go)"""
    lines = code.split('\n')
    result = []
    
    # Imports y setup básico de Gin
    result.extend([
        'package main',
        '',
        'import (',
        '    "net/http"',
        '    "github.com/gin-gonic/gin"',
        '    "github.com/gin-contrib/cors"',
        '    "log"',
        ')',
        '',
        'func main() {',
        '    // Crear router Gin',
        '    r := gin.Default()',
        '',
        '    // Middleware CORS',
        '    r.Use(cors.Default())',
        ''
    ])
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('servidor gin'):
            # Configuración del servidor
            result.append('    // Configuración del servidor Gin')
            
        elif line.startswith('puerto'):
            # Puerto del servidor
            port = line.replace('puerto', '').strip()
            result.append(f'    port := "{port}"')
            
        elif line.startswith('ruta get'):
            # Endpoint GET
            path = line.replace('ruta get', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'Get')
            result.extend([
                f'    r.GET("{path}", {handler_name})',
                ''
            ])
            
        elif line.startswith('ruta post'):
            # Endpoint POST
            path = line.replace('ruta post', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'Post')
            result.extend([
                f'    r.POST("{path}", {handler_name})',
                ''
            ])
            
        elif line.startswith('ruta put'):
            # Endpoint PUT
            path = line.replace('ruta put', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'Put')
            result.extend([
                f'    r.PUT("{path}", {handler_name})',
                ''
            ])
            
        elif line.startswith('ruta delete'):
            # Endpoint DELETE
            path = line.replace('ruta delete', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'Delete')
            result.extend([
                f'    r.DELETE("{path}", {handler_name})',
                ''
            ])
            
        elif line.startswith('middleware'):
            # Middleware personalizado
            middleware_name = line.replace('middleware', '').strip().strip('"')
            result.append(f'    r.Use({middleware_name}())')
            
        elif line.startswith('grupo'):
            # Grupo de rutas
            group_path = line.replace('grupo', '').strip().strip('"')
            result.extend([
                f'    // Grupo de rutas: {group_path}',
                f'    {group_path.replace("/", "")}Group := r.Group("{group_path}")',
                f'    {{',
                ''
            ])
            
        elif line.startswith('fin grupo'):
            result.extend([
                '    }',
                ''
            ])
            
        elif line.startswith('cors'):
            # Configuración CORS
            result.append('    // CORS ya configurado arriba')
            
        elif line.startswith('json'):
            # Respuesta JSON
            data = line.replace('json', '').strip()
            result.append(f'        c.JSON(http.StatusOK, {data})')
            
        elif line.startswith('error'):
            # Respuesta de error
            message = line.replace('error', '').strip().strip('"')
            result.append(f'        c.JSON(http.StatusBadRequest, gin.H{{"error": "{message}"}})')
            
        elif line.startswith('validar'):
            # Validación de datos
            result.extend([
                '        var requestData map[string]interface{}',
                '        if err := c.ShouldBindJSON(&requestData); err != nil {',
                '            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})',
                '            return',
                '        }',
                ''
            ])
    
    # Generar handlers
    result.extend(_generate_handlers())
    
    # Iniciar servidor
    result.extend([
        '    // Iniciar servidor',
        '    log.Printf("Servidor iniciado en puerto %s", port)',
        '    r.Run(":" + port)',
        '}'
    ])
    
    return '\n'.join(result)

def _path_to_handler_name(path, method):
    """Convierte path a nombre de handler"""
    clean_path = path.replace('/', '').replace('-', '').replace('_', '')
    if not clean_path:
        clean_path = 'root'
    return f'handle{method}{clean_path.title()}'

def _generate_handlers():
    """Genera handlers básicos"""
    return [
        '',
        '// Handlers',
        'func handleGetRoot(c *gin.Context) {',
        '    c.JSON(http.StatusOK, gin.H{',
        '        "message": "¡Hola desde Gin!",',
        '        "status": "ok",',
        '    })',
        '}',
        '',
        'func handlePostRoot(c *gin.Context) {',
        '    var data map[string]interface{}',
        '    if err := c.ShouldBindJSON(&data); err != nil {',
        '        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})',
        '        return',
        '    }',
        '    c.JSON(http.StatusCreated, gin.H{',
        '        "message": "Datos recibidos",',
        '        "data": data,',
        '    })',
        '}',
        '',
        'func handleGetUsuarios(c *gin.Context) {',
        '    usuarios := []map[string]interface{}{',
        '        {"id": 1, "nombre": "Juan", "email": "juan@example.com"},',
        '        {"id": 2, "nombre": "María", "email": "maria@example.com"},',
        '    }',
        '    c.JSON(http.StatusOK, usuarios)',
        '}',
        '',
        'func handlePostUsuarios(c *gin.Context) {',
        '    var usuario map[string]interface{}',
        '    if err := c.ShouldBindJSON(&usuario); err != nil {',
        '        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})',
        '        return',
        '    }',
        '    // Aquí guardarías el usuario en la base de datos',
        '    c.JSON(http.StatusCreated, gin.H{',
        '        "message": "Usuario creado exitosamente",',
        '        "usuario": usuario,',
        '    })',
        '}',
        ''
    ]

# Palabras clave específicas de Gin
GIN_KEYWORDS = [
    'servidor gin', 'ruta get', 'ruta post', 'ruta put', 'ruta delete',
    'middleware', 'grupo', 'cors', 'json', 'validar'
]

def detect_gin(code):
    """Detecta si el código contiene sintaxis específica de Gin"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in GIN_KEYWORDS)
