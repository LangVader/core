# Transpilador Actix (Rust) para Vader
# Convierte sintaxis natural a Actix-web para APIs de alto rendimiento

def transpile_actix(code):
    """Transpila código Vader a Actix-web (Rust)"""
    lines = code.split('\n')
    result = []
    
    # Imports y setup básico de Actix
    result.extend([
        'use actix_web::{web, App, HttpServer, HttpResponse, Result, middleware::Logger};',
        'use serde::{Deserialize, Serialize};',
        'use std::sync::Mutex;',
        '',
        '#[derive(Serialize, Deserialize)]',
        'struct ApiResponse {',
        '    message: String,',
        '    status: String,',
        '}',
        '',
        '#[derive(Serialize, Deserialize)]',
        'struct Usuario {',
        '    id: Option<u32>,',
        '    nombre: String,',
        '    email: String,',
        '}',
        '',
        '// Estado compartido de la aplicación',
        'struct AppState {',
        '    usuarios: Mutex<Vec<Usuario>>,',
        '}',
        ''
    ])
    
    handlers = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('servidor actix'):
            # Configuración del servidor
            result.append('// Configuración del servidor Actix')
            
        elif line.startswith('puerto'):
            # Puerto del servidor
            port = line.replace('puerto', '').strip()
            result.append(f'const PORT: &str = "{port}";')
            
        elif line.startswith('ruta get'):
            # Endpoint GET
            path = line.replace('ruta get', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'get')
            handlers.append((handler_name, 'GET', path))
            
        elif line.startswith('ruta post'):
            # Endpoint POST
            path = line.replace('ruta post', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'post')
            handlers.append((handler_name, 'POST', path))
            
        elif line.startswith('ruta put'):
            # Endpoint PUT
            path = line.replace('ruta put', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'put')
            handlers.append((handler_name, 'PUT', path))
            
        elif line.startswith('ruta delete'):
            # Endpoint DELETE
            path = line.replace('ruta delete', '').strip().strip('"')
            handler_name = _path_to_handler_name(path, 'delete')
            handlers.append((handler_name, 'DELETE', path))
            
        elif line.startswith('middleware'):
            # Middleware
            middleware_type = line.replace('middleware', '').strip().strip('"')
            if middleware_type == 'logger':
                result.append('// Logger middleware configurado en main')
            elif middleware_type == 'cors':
                result.append('use actix_cors::Cors;')
                
        elif line.startswith('json'):
            # Respuesta JSON
            result.append('    // Respuesta JSON configurada en handlers')
            
        elif line.startswith('estado'):
            # Estado de la aplicación
            result.append('    // Estado compartido configurado arriba')
    
    # Generar handlers
    result.extend(_generate_actix_handlers(handlers))
    
    # Función main
    result.extend([
        '#[actix_web::main]',
        'async fn main() -> std::io::Result<()> {',
        '    env_logger::init();',
        '',
        '    // Estado inicial de la aplicación',
        '    let app_state = web::Data::new(AppState {',
        '        usuarios: Mutex::new(vec![',
        '            Usuario {',
        '                id: Some(1),',
        '                nombre: "Juan".to_string(),',
        '                email: "juan@example.com".to_string(),',
        '            },',
        '            Usuario {',
        '                id: Some(2),',
        '                nombre: "María".to_string(),',
        '                email: "maria@example.com".to_string(),',
        '            },',
        '        ]),',
        '    });',
        '',
        '    println!("🚀 Servidor Actix iniciado en puerto {}", PORT);',
        '',
        '    HttpServer::new(move || {',
        '        App::new()',
        '            .app_data(app_state.clone())',
        '            .wrap(Logger::default())',
    ])
    
    # Registrar rutas
    for handler_name, method, path in handlers:
        if method == 'GET':
            result.append(f'            .route("{path}", web::get().to({handler_name}))')
        elif method == 'POST':
            result.append(f'            .route("{path}", web::post().to({handler_name}))')
        elif method == 'PUT':
            result.append(f'            .route("{path}", web::put().to({handler_name}))')
        elif method == 'DELETE':
            result.append(f'            .route("{path}", web::delete().to({handler_name}))')
    
    result.extend([
        '    })',
        '    .bind(format!("127.0.0.1:{}", PORT))?',
        '    .run()',
        '    .await',
        '}'
    ])
    
    return '\n'.join(result)

def _path_to_handler_name(path, method):
    """Convierte path a nombre de handler"""
    clean_path = path.replace('/', '').replace('-', '_').replace(' ', '_')
    if not clean_path:
        clean_path = 'root'
    return f'{method}_{clean_path}'

def _generate_actix_handlers(handlers):
    """Genera handlers de Actix"""
    result = []
    
    # Handler básico de salud
    result.extend([
        '// Handlers de la API',
        'async fn get_root() -> Result<HttpResponse> {',
        '    Ok(HttpResponse::Ok().json(ApiResponse {',
        '        message: "¡Hola desde Actix-web!".to_string(),',
        '        status: "ok".to_string(),',
        '    }))',
        '}',
        ''
    ])
    
    # Handler para obtener usuarios
    if any('usuarios' in handler[2] and handler[1] == 'GET' for handler in handlers):
        result.extend([
            'async fn get_usuarios(data: web::Data<AppState>) -> Result<HttpResponse> {',
            '    let usuarios = data.usuarios.lock().unwrap();',
            '    Ok(HttpResponse::Ok().json(&*usuarios))',
            '}',
            ''
        ])
    
    # Handler para crear usuario
    if any('usuarios' in handler[2] and handler[1] == 'POST' for handler in handlers):
        result.extend([
            'async fn post_usuarios(',
            '    usuario: web::Json<Usuario>,',
            '    data: web::Data<AppState>,',
            ') -> Result<HttpResponse> {',
            '    let mut usuarios = data.usuarios.lock().unwrap();',
            '    let mut nuevo_usuario = usuario.into_inner();',
            '    nuevo_usuario.id = Some((usuarios.len() + 1) as u32);',
            '    usuarios.push(nuevo_usuario.clone());',
            '',
            '    Ok(HttpResponse::Created().json(ApiResponse {',
            '        message: "Usuario creado exitosamente".to_string(),',
            '        status: "created".to_string(),',
            '    }))',
            '}',
            ''
        ])
    
    # Handler genérico para otras rutas
    for handler_name, method, path in handlers:
        if 'usuarios' not in path and handler_name not in ['get_root']:
            result.extend([
                f'async fn {handler_name}() -> Result<HttpResponse> {{',
                f'    Ok(HttpResponse::Ok().json(ApiResponse {{',
                f'        message: "Endpoint {method} {path} funcionando".to_string(),',
                f'        status: "ok".to_string(),',
                f'    }}))',
                '}',
                ''
            ])
    
    return result

# Palabras clave específicas de Actix
ACTIX_KEYWORDS = [
    'servidor actix', 'ruta get', 'ruta post', 'ruta put', 'ruta delete',
    'middleware', 'estado', 'json', 'async', 'actix'
]

def detect_actix(code):
    """Detecta si el código contiene sintaxis específica de Actix"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in ACTIX_KEYWORDS)
