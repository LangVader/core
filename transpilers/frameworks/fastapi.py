def transpile_to_fastapi(code):
    """Transpila código Vader a FastAPI con Python"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_api = False
    in_model = False
    in_route = False
    api_name = "MiAPI"
    imports = set()
    models = []
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de FastAPI
    add_import("from fastapi import FastAPI, HTTPException, Depends, status")
    add_import("from pydantic import BaseModel")
    add_import("from typing import List, Optional")
    add_import("import uvicorn")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # API FastAPI
        if line.startswith("api fastapi"):
            parts = line.split()
            api_name = parts[2] if len(parts) > 2 else "MiAPI"
            add_line("")
            add_line(f"app = FastAPI(title='{api_name}', version='1.0.0')")
            add_line("")
            in_api = True
            continue

        if line == "fin api":
            in_api = False
            # Agregar código de inicio del servidor
            add_line("")
            add_line("if __name__ == '__main__':")
            add_line("    uvicorn.run(app, host='0.0.0.0', port=8000)")
            continue

        # Modelos Pydantic
        if line.startswith("modelo"):
            model_name = line.split()[1] if len(line.split()) > 1 else "MiModelo"
            models.append(model_name)
            add_line(f"class {model_name}(BaseModel):")
            in_model = True
            indent += 1
            continue

        if line == "fin modelo":
            add_line("")
            in_model = False
            indent -= 1
            continue

        # Atributos del modelo
        if in_model and line.startswith("atributo"):
            parts = line.split(":")
            if len(parts) == 2:
                attr_name = parts[0].replace("atributo", "").strip()
                attr_type = parts[1].strip()
                
                # Mapear tipos de Vader a Python
                type_mapping = {
                    "string": "str",
                    "texto": "str",
                    "numero": "int",
                    "decimal": "float",
                    "booleano": "bool",
                    "lista": "List[str]",
                    "opcional": "Optional[str]"
                }
                
                python_type = type_mapping.get(attr_type, attr_type)
                add_line(f"{attr_name}: {python_type}")
            continue

        # Rutas HTTP
        if line.startswith("ruta GET"):
            path = line.split("GET")[1].strip() if "GET" in line else "/"
            add_line(f"@app.get('{path}')")
            add_line(f"async def get{path.replace('/', '_').replace(':', '_param_')}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta POST"):
            path = line.split("POST")[1].strip() if "POST" in line else "/"
            add_line(f"@app.post('{path}', status_code=status.HTTP_201_CREATED)")
            add_line(f"async def post{path.replace('/', '_').replace(':', '_param_')}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta PUT"):
            path = line.split("PUT")[1].strip() if "PUT" in line else "/"
            add_line(f"@app.put('{path}')")
            add_line(f"async def put{path.replace('/', '_').replace(':', '_param_')}():")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta DELETE"):
            path = line.split("DELETE")[1].strip() if "DELETE" in line else "/"
            add_line(f"@app.delete('{path}')")
            add_line(f"async def delete{path.replace('/', '_').replace(':', '_param_')}():")
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
                add_line(f"return {json_data}")
            else:
                add_line(f"return {data}")
            continue

        if line.startswith("respuesta error"):
            parts = line.split()
            status_code = parts[2] if len(parts) > 2 else "400"
            message = " ".join(parts[3:]) if len(parts) > 3 else "Error"
            message = message.replace('"', '')
            add_line(f"raise HTTPException(status_code={status_code}, detail='{message}')")
            continue

        # Parámetros de ruta
        if line.startswith("parametro"):
            param_name = line.split()[1] if len(line.split()) > 1 else "param"
            add_line(f"{param_name} = {param_name}")
            continue

        # Cuerpo de petición
        if line.startswith("cuerpo peticion"):
            model_name = line.split()[-1] if len(line.split()) > 2 else "dict"
            add_line(f"data: {model_name}")
            continue

        # Validaciones
        if line.startswith("validar"):
            field = line.split()[1] if len(line.split()) > 1 else "field"
            add_line(f"if not {field}:")
            add_line(f"    raise HTTPException(status_code=400, detail='{field} es requerido')")
            continue

        # Middleware
        if line.startswith("middleware"):
            middleware_name = line.split()[1] if len(line.split()) > 1 else "middleware"
            add_line(f"@app.middleware('http')")
            add_line(f"async def {middleware_name}(request: Request, call_next):")
            indent += 1
            continue

        if line == "fin middleware":
            add_line("response = await call_next(request)")
            add_line("return response")
            indent -= 1
            add_line("")
            continue

        # Dependencias
        if line.startswith("dependencia"):
            dep_name = line.split()[1] if len(line.split()) > 1 else "dependency"
            add_line(f"def {dep_name}():")
            indent += 1
            continue

        if line == "fin dependencia":
            indent -= 1
            add_line("")
            continue

        # Base de datos (simulada)
        if line.startswith("base datos"):
            add_line("# Simulación de base de datos")
            add_line("fake_db = []")
            continue

        # CORS
        if line.startswith("cors"):
            add_import("from fastapi.middleware.cors import CORSMiddleware")
            add_line("app.add_middleware(")
            add_line("    CORSMiddleware,")
            add_line("    allow_origins=['*'],")
            add_line("    allow_credentials=True,")
            add_line("    allow_methods=['*'],")
            add_line("    allow_headers=['*'],")
            add_line(")")
            continue

        # Autenticación JWT
        if line.startswith("jwt auth"):
            add_import("from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials")
            add_import("import jwt")
            add_line("security = HTTPBearer()")
            add_line("")
            add_line("def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):")
            add_line("    try:")
            add_line("        payload = jwt.decode(credentials.credentials, 'secret', algorithms=['HS256'])")
            add_line("        return payload")
            add_line("    except jwt.PyJWTError:")
            add_line("        raise HTTPException(status_code=401, detail='Token inválido')")
            add_line("")
            continue

        # Documentación automática
        if line.startswith("documentacion"):
            description = line.replace("documentacion", "").strip().replace('"', '')
            add_line(f"app.description = '{description}'")
            continue

        # Otras líneas (comentarios o código Python)
        if in_route or in_model:
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
    
    # Agregar modelos al inicio (después de imports)
    result_lines = import_lines + output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_fastapi(codigo)

# Funciones auxiliares para el transpilador de FastAPI
def get_fastapi_keywords():
    """Retorna las palabras clave de Vader que se mapean a FastAPI"""
    return {
        'api fastapi': 'FastAPI application',
        'modelo': 'Pydantic model',
        'atributo': 'model field',
        'ruta GET': 'GET endpoint',
        'ruta POST': 'POST endpoint',
        'ruta PUT': 'PUT endpoint',
        'ruta DELETE': 'DELETE endpoint',
        'respuesta json': 'JSON response',
        'respuesta error': 'HTTP exception',
        'parametro': 'path parameter',
        'cuerpo peticion': 'request body',
        'validar': 'validation',
        'middleware': 'middleware function',
        'dependencia': 'dependency',
        'cors': 'CORS middleware',
        'jwt auth': 'JWT authentication',
        'documentacion': 'API documentation',
        'base datos': 'database simulation'
    }
