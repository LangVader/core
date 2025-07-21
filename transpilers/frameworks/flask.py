def transpile_to_flask(code):
    """Transpila código Vader a Flask con Python"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_app = False
    in_route = False
    app_name = "MiApp"
    imports = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de Flask
    add_import("from flask import Flask, request, jsonify, render_template, redirect, url_for, session")
    add_import("from flask_cors import CORS")
    add_import("import os")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Aplicación Flask
        if line.startswith("app flask"):
            parts = line.split()
            app_name = parts[2] if len(parts) > 2 else "MiApp"
            add_line("")
            add_line(f"app = Flask(__name__)")
            add_line(f"app.secret_key = os.environ.get('SECRET_KEY', 'clave-secreta-desarrollo')")
            add_line("CORS(app)")
            add_line("")
            in_app = True
            continue

        if line == "fin app":
            in_app = False
            # Agregar código de inicio del servidor
            add_line("")
            add_line("if __name__ == '__main__':")
            add_line("    app.run(debug=True, host='0.0.0.0', port=5000)")
            continue

        # Rutas HTTP
        if line.startswith("ruta GET"):
            path = line.split("GET")[1].strip() if "GET" in line else "/"
            add_line(f"@app.route('{path}', methods=['GET'])")
            func_name = path.replace('/', '_').replace(':', '_param_').replace('<', '').replace('>', '')
            if func_name.startswith('_'):
                func_name = 'index' + func_name
            if not func_name or func_name == '_':
                func_name = 'index'
            add_line(f"def {func_name}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta POST"):
            path = line.split("POST")[1].strip() if "POST" in line else "/"
            add_line(f"@app.route('{path}', methods=['POST'])")
            func_name = path.replace('/', '_').replace(':', '_param_').replace('<', '').replace('>', '')
            if func_name.startswith('_'):
                func_name = 'post' + func_name
            if not func_name or func_name == '_':
                func_name = 'post_index'
            add_line(f"def {func_name}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta PUT"):
            path = line.split("PUT")[1].strip() if "PUT" in line else "/"
            add_line(f"@app.route('{path}', methods=['PUT'])")
            func_name = path.replace('/', '_').replace(':', '_param_').replace('<', '').replace('>', '')
            if func_name.startswith('_'):
                func_name = 'put' + func_name
            if not func_name or func_name == '_':
                func_name = 'put_index'
            add_line(f"def {func_name}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta DELETE"):
            path = line.split("DELETE")[1].strip() if "DELETE" in line else "/"
            add_line(f"@app.route('{path}', methods=['DELETE'])")
            func_name = path.replace('/', '_').replace(':', '_param_').replace('<', '').replace('>', '')
            if func_name.startswith('_'):
                func_name = 'delete' + func_name
            if not func_name or func_name == '_':
                func_name = 'delete_index'
            add_line(f"def {func_name}():")
            in_route = True
            indent += 1
            continue

        if line == "fin ruta":
            add_line("")
            in_route = False
            indent -= 1
            continue

        # Respuestas
        if line.startswith("respuesta json"):
            data = line.replace("respuesta json", "").strip()
            if "status=" in data:
                parts = data.split("status=")
                json_data = parts[0].strip()
                status_code = parts[1].strip()
                add_line(f"return jsonify({json_data}), {status_code}")
            else:
                add_line(f"return jsonify({data})")
            continue

        if line.startswith("respuesta plantilla"):
            template = line.replace("respuesta plantilla", "").strip()
            if "con" in template:
                parts = template.split("con")
                template_name = parts[0].strip().replace('"', '').replace("'", '')
                context = parts[1].strip()
                add_line(f"return render_template('{template_name}', {context})")
            else:
                template_name = template.replace('"', '').replace("'", '')
                add_line(f"return render_template('{template_name}')")
            continue

        if line.startswith("redirigir a"):
            endpoint = line.replace("redirigir a", "").strip().replace('"', '').replace("'", '')
            add_line(f"return redirect(url_for('{endpoint}'))")
            continue

        if line.startswith("respuesta error"):
            parts = line.split()
            status_code = parts[2] if len(parts) > 2 else "400"
            message = " ".join(parts[3:]) if len(parts) > 3 else "Error"
            message = message.replace('"', '')
            add_line(f"return jsonify({{'error': '{message}'}}), {status_code}")
            continue

        # Parámetros de ruta
        if line.startswith("parametro"):
            param_name = line.split()[1] if len(line.split()) > 1 else "param"
            add_line(f"{param_name} = request.view_args.get('{param_name}')")
            continue

        # Datos de formulario/JSON
        if line.startswith("datos formulario"):
            add_line("data = request.form.to_dict()")
            continue

        if line.startswith("datos json"):
            add_line("data = request.get_json()")
            continue

        if line.startswith("cuerpo peticion"):
            add_line("data = request.get_json() or request.form.to_dict()")
            continue

        # Archivos subidos
        if line.startswith("archivo subido"):
            file_name = line.split()[-1] if len(line.split()) > 2 else "file"
            add_line(f"{file_name} = request.files.get('{file_name}')")
            continue

        # Sesiones
        if line.startswith("guardar sesion"):
            parts = line.split("=")
            if len(parts) == 2:
                key = parts[0].replace("guardar sesion", "").strip()
                value = parts[1].strip()
                add_line(f"session['{key}'] = {value}")
            continue

        if line.startswith("obtener sesion"):
            key = line.replace("obtener sesion", "").strip()
            add_line(f"session.get('{key}')")
            continue

        if line.startswith("limpiar sesion"):
            add_line("session.clear()")
            continue

        # Cookies
        if line.startswith("establecer cookie"):
            parts = line.split("=")
            if len(parts) == 2:
                key = parts[0].replace("establecer cookie", "").strip()
                value = parts[1].strip()
                add_line(f"response = jsonify({{'success': True}})")
                add_line(f"response.set_cookie('{key}', {value})")
                add_line("return response")
            continue

        if line.startswith("obtener cookie"):
            key = line.replace("obtener cookie", "").strip()
            add_line(f"request.cookies.get('{key}')")
            continue

        # Base de datos (simulada)
        if line.startswith("base datos"):
            add_line("# Simulación de base de datos")
            add_line("fake_db = []")
            continue

        # Validaciones
        if line.startswith("validar"):
            field = line.split()[1] if len(line.split()) > 1 else "field"
            add_line(f"if not data.get('{field}'):")
            add_line(f"    return jsonify({{'error': '{field} es requerido'}}), 400")
            continue

        # Middleware/Before request
        if line.startswith("antes peticion"):
            add_line("@app.before_request")
            add_line("def before_request():")
            indent += 1
            continue

        if line == "fin antes":
            indent -= 1
            add_line("")
            continue

        # After request
        if line.startswith("despues peticion"):
            add_line("@app.after_request")
            add_line("def after_request(response):")
            indent += 1
            continue

        if line == "fin despues":
            add_line("return response")
            indent -= 1
            add_line("")
            continue

        # Error handlers
        if line.startswith("manejar error"):
            error_code = line.split()[-1] if len(line.split()) > 2 else "404"
            add_line(f"@app.errorhandler({error_code})")
            add_line(f"def handle_{error_code}(error):")
            indent += 1
            continue

        if line == "fin manejar":
            indent -= 1
            add_line("")
            continue

        # Configuración
        if line.startswith("configuracion"):
            parts = line.split("=")
            if len(parts) == 2:
                key = parts[0].replace("configuracion", "").strip()
                value = parts[1].strip()
                add_line(f"app.config['{key.upper()}'] = {value}")
            continue

        # Otras líneas (comentarios o código Python)
        if in_route:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"print({message})")
            elif "=" in line:
                add_line(f"{line}")
            else:
                add_line(f"# {line}")

    # Agregar imports al inicio
    import_lines = []
    if imports:
        import_lines.extend(sorted(imports))
        import_lines.append("")
    
    result_lines = import_lines + output
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_flask(codigo)

# Funciones auxiliares para el transpilador de Flask
def get_flask_keywords():
    """Retorna las palabras clave de Vader que se mapean a Flask"""
    return {
        'app flask': 'Flask application',
        'ruta GET': 'GET route',
        'ruta POST': 'POST route',
        'ruta PUT': 'PUT route',
        'ruta DELETE': 'DELETE route',
        'respuesta json': 'JSON response',
        'respuesta plantilla': 'template response',
        'redirigir a': 'redirect',
        'respuesta error': 'error response',
        'parametro': 'route parameter',
        'datos formulario': 'form data',
        'datos json': 'JSON data',
        'cuerpo peticion': 'request body',
        'archivo subido': 'uploaded file',
        'guardar sesion': 'save session',
        'obtener sesion': 'get session',
        'limpiar sesion': 'clear session',
        'establecer cookie': 'set cookie',
        'obtener cookie': 'get cookie',
        'validar': 'validation',
        'antes peticion': 'before request',
        'despues peticion': 'after request',
        'manejar error': 'error handler',
        'configuracion': 'configuration'
    }
