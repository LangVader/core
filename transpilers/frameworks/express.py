def transpile_to_express(code):
    """Transpila código Vader a Express.js para APIs y aplicaciones web"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_route = False
    in_middleware = False
    app_created = False
    imports = set()
    middlewares_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def ensure_app():
        nonlocal app_created
        if not app_created:
            add_import("const express = require('express');")
            add_line("const app = express();")
            add_line("")
            app_created = True

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Crear aplicación Express
        if line.startswith("aplicacion express") or line.startswith("app express"):
            ensure_app()
            continue

        # Configurar puerto
        if line.startswith("puerto"):
            port = line.split()[1] if len(line.split()) > 1 else "3000"
            add_line(f"const PORT = process.env.PORT || {port};")
            continue

        # Iniciar servidor
        if line.startswith("iniciar servidor") or line.startswith("escuchar"):
            ensure_app()
            add_line("app.listen(PORT, () => {")
            add_line(f"  console.log(`Servidor ejecutándose en puerto ${{PORT}}`);")
            add_line("});")
            continue

        # Middleware
        if line.startswith("usar middleware"):
            ensure_app()
            middleware_name = line.split()[2] if len(line.split()) > 2 else "express.json()"
            
            # Middlewares comunes
            if middleware_name == "json":
                add_line("app.use(express.json());")
                middlewares_used.add("json")
            elif middleware_name == "urlencoded":
                add_line("app.use(express.urlencoded({ extended: true }));")
                middlewares_used.add("urlencoded")
            elif middleware_name == "cors":
                add_import("const cors = require('cors');")
                add_line("app.use(cors());")
                middlewares_used.add("cors")
            elif middleware_name == "morgan":
                add_import("const morgan = require('morgan');")
                add_line("app.use(morgan('combined'));")
                middlewares_used.add("morgan")
            elif middleware_name == "helmet":
                add_import("const helmet = require('helmet');")
                add_line("app.use(helmet());")
                middlewares_used.add("helmet")
            elif middleware_name == "estaticos":
                directory = line.split()[3] if len(line.split()) > 3 else "public"
                add_line(f"app.use(express.static('{directory}'));")
            else:
                add_line(f"app.use({middleware_name});")
            continue

        # Middleware personalizado
        if line.startswith("middleware"):
            middleware_name = line.split()[1] if len(line.split()) > 1 else "customMiddleware"
            add_line(f"const {middleware_name} = (req, res, next) => {{")
            in_middleware = True
            indent += 1
            continue

        if line == "fin middleware":
            add_line("next();")
            indent -= 1
            add_line("};")
            add_line("")
            in_middleware = False
            continue

        # Rutas HTTP
        if line.startswith("ruta GET") or line.startswith("get"):
            ensure_app()
            path = line.split()[2] if len(line.split()) > 2 else "/"
            add_line(f"app.get('{path}', (req, res) => {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta POST") or line.startswith("post"):
            ensure_app()
            path = line.split()[2] if len(line.split()) > 2 else "/"
            add_line(f"app.post('{path}', (req, res) => {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta PUT") or line.startswith("put"):
            ensure_app()
            path = line.split()[2] if len(line.split()) > 2 else "/"
            add_line(f"app.put('{path}', (req, res) => {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta DELETE") or line.startswith("delete"):
            ensure_app()
            path = line.split()[2] if len(line.split()) > 2 else "/"
            add_line(f"app.delete('{path}', (req, res) => {{")
            in_route = True
            indent += 1
            continue

        if line == "fin ruta":
            indent -= 1
            add_line("});")
            add_line("")
            in_route = False
            continue

        # Respuestas HTTP
        if line.startswith("responder"):
            if "json" in line:
                data = line.split("json")[1].strip() if "json" in line else "{}"
                add_line(f"res.json({data});")
            elif "texto" in line:
                text = line.split("texto")[1].strip() if "texto" in line else "'Hola mundo'"
                add_line(f"res.send({text});")
            elif "estado" in line:
                status = line.split("estado")[1].split()[0].strip()
                message = " ".join(line.split("estado")[1].split()[1:]) if len(line.split("estado")[1].split()) > 1 else "'OK'"
                add_line(f"res.status({status}).send({message});")
            else:
                data = line[9:].strip() if len(line) > 9 else "'Respuesta'"
                add_line(f"res.send({data});")
            continue

        if line.startswith("responder json"):
            data = line[14:].strip() if len(line) > 14 else "{}"
            add_line(f"res.json({data});")
            continue

        if line.startswith("responder error"):
            status = "500"
            message = line[15:].strip() if len(line) > 15 else "'Error interno del servidor'"
            if "404" in line:
                status = "404"
            elif "400" in line:
                status = "400"
            elif "401" in line:
                status = "401"
            elif "403" in line:
                status = "403"
            
            add_line(f"res.status({status}).json({{ error: {message} }});")
            continue

        # Parámetros de ruta
        if line.startswith("parametro"):
            param_name = line.split()[1] if len(line.split()) > 1 else "id"
            add_line(f"const {param_name} = req.params.{param_name};")
            continue

        # Query parameters
        if line.startswith("query"):
            query_name = line.split()[1] if len(line.split()) > 1 else "q"
            add_line(f"const {query_name} = req.query.{query_name};")
            continue

        # Body de la petición
        if line.startswith("cuerpo"):
            add_line("const body = req.body;")
            continue

        if line.startswith("obtener del cuerpo"):
            field_name = line.split()[3] if len(line.split()) > 3 else "data"
            add_line(f"const {field_name} = req.body.{field_name};")
            continue

        # Headers
        if line.startswith("header"):
            header_name = line.split()[1] if len(line.split()) > 1 else "authorization"
            add_line(f"const {header_name} = req.headers['{header_name}'];")
            continue

        if line.startswith("establecer header"):
            parts = line.split()
            header_name = parts[2] if len(parts) > 2 else "Content-Type"
            header_value = parts[3] if len(parts) > 3 else "application/json"
            add_line(f"res.setHeader('{header_name}', '{header_value}');")
            continue

        # Cookies
        if line.startswith("obtener cookie"):
            cookie_name = line.split()[2] if len(line.split()) > 2 else "session"
            add_import("const cookieParser = require('cookie-parser');")
            add_line(f"const {cookie_name} = req.cookies.{cookie_name};")
            continue

        if line.startswith("establecer cookie"):
            parts = line.split()
            cookie_name = parts[2] if len(parts) > 2 else "session"
            cookie_value = parts[3] if len(parts) > 3 else "value"
            options = "{ httpOnly: true }"
            if "opciones" in line:
                options = line.split("opciones")[1].strip()
            add_line(f"res.cookie('{cookie_name}', {cookie_value}, {options});")
            continue

        # Sesiones
        if line.startswith("usar sesiones"):
            add_import("const session = require('express-session');")
            add_line("app.use(session({")
            add_line("  secret: process.env.SESSION_SECRET || 'mi-secreto',")
            add_line("  resave: false,")
            add_line("  saveUninitialized: false")
            add_line("}));")
            continue

        if line.startswith("obtener sesion"):
            session_key = line.split()[2] if len(line.split()) > 2 else "user"
            add_line(f"const {session_key} = req.session.{session_key};")
            continue

        if line.startswith("establecer sesion"):
            parts = line.split()
            session_key = parts[2] if len(parts) > 2 else "user"
            session_value = parts[3] if len(parts) > 3 else "value"
            add_line(f"req.session.{session_key} = {session_value};")
            continue

        # Base de datos (MongoDB con Mongoose)
        if line.startswith("conectar mongodb"):
            connection_string = line.split()[2] if len(line.split()) > 2 else "process.env.MONGODB_URI"
            add_import("const mongoose = require('mongoose');")
            add_line(f"mongoose.connect({connection_string});")
            continue

        if line.startswith("modelo"):
            model_name = line.split()[1] if len(line.split()) > 1 else "User"
            add_import("const mongoose = require('mongoose');")
            add_line(f"const {model_name}Schema = new mongoose.Schema({{")
            indent += 1
            continue

        if line == "fin modelo":
            indent -= 1
            add_line("});")
            add_line("")
            continue

        # Validación
        if line.startswith("validar"):
            field_name = line.split()[1] if len(line.split()) > 1 else "email"
            validation_type = line.split()[2] if len(line.split()) > 2 else "required"
            
            if validation_type == "requerido":
                add_line(f"if (!{field_name}) {{")
                add_line(f"  return res.status(400).json({{ error: '{field_name} es requerido' }});")
                add_line("}")
            elif validation_type == "email":
                add_line(f"const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;")
                add_line(f"if (!emailRegex.test({field_name})) {{")
                add_line(f"  return res.status(400).json({{ error: 'Email inválido' }});")
                add_line("}")
            continue

        # Autenticación JWT
        if line.startswith("generar token"):
            payload = line.split()[2] if len(line.split()) > 2 else "{ userId: user.id }"
            add_import("const jwt = require('jsonwebtoken');")
            add_line(f"const token = jwt.sign({payload}, process.env.JWT_SECRET, {{ expiresIn: '24h' }});")
            continue

        if line.startswith("verificar token"):
            add_import("const jwt = require('jsonwebtoken');")
            add_line("const token = req.headers.authorization?.split(' ')[1];")
            add_line("if (!token) {")
            add_line("  return res.status(401).json({ error: 'Token requerido' });")
            add_line("}")
            add_line("try {")
            add_line("  const decoded = jwt.verify(token, process.env.JWT_SECRET);")
            add_line("  req.user = decoded;")
            add_line("} catch (error) {")
            add_line("  return res.status(401).json({ error: 'Token inválido' });")
            add_line("}")
            continue

        # Subida de archivos
        if line.startswith("subir archivo"):
            add_import("const multer = require('multer');")
            add_line("const upload = multer({ dest: 'uploads/' });")
            continue

        # Manejo de errores
        if line.startswith("manejar errores"):
            add_line("app.use((err, req, res, next) => {")
            add_line("  console.error(err.stack);")
            add_line("  res.status(500).json({ error: 'Error interno del servidor' });")
            add_line("});")
            continue

        # Ruta 404
        if line.startswith("ruta 404") or line.startswith("no encontrado"):
            add_line("app.use('*', (req, res) => {")
            add_line("  res.status(404).json({ error: 'Ruta no encontrada' });")
            add_line("});")
            continue

        # Variables de entorno
        if line.startswith("cargar env"):
            add_import("require('dotenv').config();")
            continue

        # CORS personalizado
        if line.startswith("cors personalizado"):
            origins = line.split("origins")[1].strip() if "origins" in line else "['http://localhost:3000']"
            add_import("const cors = require('cors');")
            add_line(f"app.use(cors({{ origin: {origins} }}));")
            continue

        # Rate limiting
        if line.startswith("limite velocidad"):
            max_requests = line.split()[2] if len(line.split()) > 2 else "100"
            window_ms = line.split()[3] if len(line.split()) > 3 else "900000"
            add_import("const rateLimit = require('express-rate-limit');")
            add_line("const limiter = rateLimit({")
            add_line(f"  windowMs: {window_ms},")
            add_line(f"  max: {max_requests}")
            add_line("});")
            add_line("app.use(limiter);")
            continue

        # Logging
        if line.startswith("log"):
            message = line[3:].strip() if len(line) > 3 else "'Log message'"
            add_line(f"console.log({message});")
            continue

        # Asignaciones y expresiones JavaScript normales
        if "=" in line:
            add_line(f"{line};")
            continue

        # Llamadas a funciones
        if line.startswith("llamar"):
            call = line[6:].strip()
            add_line(f"{call};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")

    # Agregar imports necesarios
    import_lines = []
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(sorted(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    else:
        result_lines = output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_express(codigo)

# Funciones auxiliares para el transpilador de Express.js
def get_express_keywords():
    """Retorna las palabras clave de Vader que se mapean a Express.js"""
    return {
        'aplicacion express': 'express app',
        'puerto': 'port configuration',
        'iniciar servidor': 'app.listen',
        'usar middleware': 'app.use middleware',
        'middleware': 'custom middleware',
        'ruta GET': 'app.get',
        'ruta POST': 'app.post',
        'ruta PUT': 'app.put',
        'ruta DELETE': 'app.delete',
        'responder': 'res.send',
        'responder json': 'res.json',
        'responder error': 'error response',
        'parametro': 'req.params',
        'query': 'req.query',
        'cuerpo': 'req.body',
        'header': 'req.headers',
        'establecer header': 'res.setHeader',
        'obtener cookie': 'req.cookies',
        'establecer cookie': 'res.cookie',
        'usar sesiones': 'express-session',
        'obtener sesion': 'req.session',
        'establecer sesion': 'req.session',
        'conectar mongodb': 'mongoose.connect',
        'modelo': 'mongoose schema',
        'validar': 'validation',
        'generar token': 'jwt.sign',
        'verificar token': 'jwt.verify',
        'subir archivo': 'multer',
        'manejar errores': 'error handler',
        'ruta 404': '404 handler',
        'cargar env': 'dotenv',
        'cors personalizado': 'cors options',
        'limite velocidad': 'rate limiting',
        'log': 'console.log'
    }
