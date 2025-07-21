def transpile_to_julia(code):
    """Transpila código Vader a Julia"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_function = False
    in_struct = False
    in_module = False
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 4
        output.append(" " * current_indent + text)
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Módulo Julia
        if line.startswith("modulo"):
            module_name = line.split()[1] if len(line.split()) > 1 else "MiModulo"
            add_line(f"module {module_name}")
            in_module = True
            indent += 1
            continue

        if line == "fin modulo":
            add_line("end")
            in_module = False
            indent -= 1
            continue

        # Funciones
        if line.startswith("funcion"):
            parts = line.split()
            func_name = parts[1] if len(parts) > 1 else "mi_funcion"
            
            params = ""
            if "(" in line and ")" in line:
                param_part = line[line.find("(")+1:line.find(")")]
                if param_part:
                    julia_params = []
                    for param in param_part.split(","):
                        param = param.strip()
                        if param:
                            # Agregar tipos si se especifican
                            if ":" in param:
                                name, tipo = param.split(":")
                                julia_params.append(f"{name.strip()}::{tipo.strip()}")
                            else:
                                julia_params.append(param)
                    params = ", ".join(julia_params)
            
            if params:
                add_line(f"function {func_name}({params})")
            else:
                add_line(f"function {func_name}()")
            
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            add_line("end")
            in_function = False
            indent -= 1
            continue

        # Structs (tipos)
        if line.startswith("struct") or line.startswith("tipo"):
            struct_name = line.split()[1] if len(line.split()) > 1 else "MiTipo"
            add_line(f"struct {struct_name}")
            in_struct = True
            indent += 1
            continue

        if line == "fin struct" or line == "fin tipo":
            add_line("end")
            in_struct = False
            indent -= 1
            continue

        # Campos de struct
        if in_struct and line.startswith("campo"):
            parts = line.split(":")
            if len(parts) == 2:
                field_name = parts[0].replace("campo", "").strip()
                field_type = parts[1].strip()
                
                # Mapear tipos de Vader a Julia
                type_mapping = {
                    "numero": "Int64",
                    "decimal": "Float64",
                    "texto": "String",
                    "booleano": "Bool",
                    "lista": "Vector",
                    "matriz": "Matrix",
                    "diccionario": "Dict"
                }
                
                julia_type = type_mapping.get(field_type, field_type)
                add_line(f"{field_name}::{julia_type}")
            continue

        # Arrays y matrices
        if line.startswith("array"):
            elements = line.replace("array", "").strip()
            if elements:
                add_line(f"[{elements}]")
            else:
                add_line("[]")
            continue

        if line.startswith("matriz"):
            dimensions = line.replace("matriz", "").strip()
            if "x" in dimensions:
                dims = dimensions.split("x")
                if len(dims) == 2:
                    rows, cols = dims[0].strip(), dims[1].strip()
                    add_line(f"zeros({rows}, {cols})")
            continue

        # Operaciones matemáticas
        if line.startswith("suma"):
            expr = line.replace("suma", "").strip()
            add_line(f"sum({expr})")
            continue

        if line.startswith("promedio"):
            expr = line.replace("promedio", "").strip()
            add_line(f"mean({expr})")
            continue

        if line.startswith("maximo"):
            expr = line.replace("maximo", "").strip()
            add_line(f"maximum({expr})")
            continue

        if line.startswith("minimo"):
            expr = line.replace("minimo", "").strip()
            add_line(f"minimum({expr})")
            continue

        # Álgebra lineal
        if line.startswith("transponer"):
            matrix = line.replace("transponer", "").strip()
            add_line(f"transpose({matrix})")
            continue

        if line.startswith("determinante"):
            matrix = line.replace("determinante", "").strip()
            add_line(f"det({matrix})")
            continue

        if line.startswith("inversa"):
            matrix = line.replace("inversa", "").strip()
            add_line(f"inv({matrix})")
            continue

        # Estadísticas
        if line.startswith("desviacion"):
            data = line.replace("desviacion", "").strip()
            add_line(f"std({data})")
            continue

        if line.startswith("varianza"):
            data = line.replace("varianza", "").strip()
            add_line(f"var({data})")
            continue

        if line.startswith("correlacion"):
            data = line.replace("correlacion", "").strip()
            add_line(f"cor({data})")
            continue

        # Bucles
        if line.startswith("para"):
            parts = line.split("en")
            if len(parts) == 2:
                var = parts[0].replace("para", "").strip()
                range_expr = parts[1].strip()
                add_line(f"for {var} in {range_expr}")
                indent += 1
            continue

        if line.startswith("mientras"):
            condition = line.replace("mientras", "").strip()
            add_line(f"while {condition}")
            indent += 1
            continue

        if line == "fin para" or line == "fin mientras":
            indent -= 1
            add_line("end")
            continue

        # Condicionales
        if line.startswith("si"):
            condition = line.replace("si", "").strip()
            add_line(f"if {condition}")
            indent += 1
            continue

        if line.startswith("sino si"):
            condition = line.replace("sino si", "").strip()
            indent -= 1
            add_line(f"elseif {condition}")
            indent += 1
            continue

        if line.startswith("sino"):
            indent -= 1
            add_line("else")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line("end")
            continue

        # Try/catch
        if line.startswith("intentar"):
            add_line("try")
            indent += 1
            continue

        if line.startswith("capturar"):
            error_type = line.replace("capturar", "").strip()
            indent -= 1
            if error_type:
                add_line(f"catch {error_type}")
            else:
                add_line("catch")
            indent += 1
            continue

        if line == "fin intentar":
            indent -= 1
            add_line("end")
            continue

        # Paquetes
        if line.startswith("usar"):
            package = line.replace("usar", "").strip()
            add_line(f"using {package}")
            continue

        if line.startswith("importar"):
            package = line.replace("importar", "").strip()
            add_line(f"import {package}")
            continue

        # Plotting (si se usa Plots.jl)
        if line.startswith("grafico"):
            data = line.replace("grafico", "").strip()
            add_line(f"plot({data})")
            continue

        if line.startswith("histograma"):
            data = line.replace("histograma", "").strip()
            add_line(f"histogram({data})")
            continue

        if line.startswith("scatter"):
            data = line.replace("scatter", "").strip()
            add_line(f"scatter({data})")
            continue

        # DataFrames
        if line.startswith("dataframe"):
            data = line.replace("dataframe", "").strip()
            if data:
                add_line(f"DataFrame({data})")
            else:
                add_line("DataFrame()")
            continue

        if line.startswith("leer csv"):
            file_path = line.replace("leer csv", "").strip()
            add_line(f"CSV.read({file_path}, DataFrame)")
            continue

        if line.startswith("escribir csv"):
            parts = line.split("a")
            if len(parts) == 2:
                df = parts[0].replace("escribir csv", "").strip()
                file_path = parts[1].strip()
                add_line(f"CSV.write({file_path}, {df})")
            continue

        # Machine Learning
        if line.startswith("entrenar modelo"):
            model_data = line.replace("entrenar modelo", "").strip()
            add_line(f"fit!({model_data})")
            continue

        if line.startswith("predecir"):
            model_data = line.replace("predecir", "").strip()
            add_line(f"predict({model_data})")
            continue

        # Paralelización
        if line.startswith("paralelo"):
            add_line("@threads for i in 1:Threads.nthreads()")
            indent += 1
            continue

        if line == "fin paralelo":
            indent -= 1
            add_line("end")
            continue

        # Macros
        if line.startswith("tiempo"):
            expr = line.replace("tiempo", "").strip()
            add_line(f"@time {expr}")
            continue

        if line.startswith("benchmark"):
            expr = line.replace("benchmark", "").strip()
            add_line(f"@benchmark {expr}")
            continue

        # IO
        if line.startswith("imprimir"):
            message = line.replace("imprimir", "").strip()
            add_line(f"println({message})")
            continue

        if line.startswith("leer archivo"):
            file_path = line.replace("leer archivo", "").strip()
            add_line(f"read({file_path}, String)")
            continue

        if line.startswith("escribir archivo"):
            parts = line.split("contenido")
            if len(parts) == 2:
                file_path = parts[0].replace("escribir archivo", "").strip()
                content = parts[1].strip()
                add_line(f"write({file_path}, {content})")
            continue

        # Variables y asignaciones
        if "=" in line and not line.startswith("//"):
            julia_line = line
            add_line(julia_line)
            continue

        # Otras líneas (comentarios)
        if in_function or in_module or in_struct:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"println({message})")
            else:
                add_line(f"# {line}")

    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_julia(codigo)

# Funciones auxiliares para el transpilador de Julia
def get_julia_keywords():
    """Retorna las palabras clave de Vader que se mapean a Julia"""
    return {
        'modulo': 'module',
        'funcion': 'function',
        'struct': 'struct type',
        'tipo': 'struct type',
        'campo': 'struct field',
        'array': 'array/vector',
        'matriz': 'matrix',
        'suma': 'sum function',
        'promedio': 'mean function',
        'maximo': 'maximum function',
        'minimo': 'minimum function',
        'transponer': 'transpose',
        'determinante': 'determinant',
        'inversa': 'matrix inverse',
        'desviacion': 'standard deviation',
        'varianza': 'variance',
        'correlacion': 'correlation',
        'para': 'for loop',
        'mientras': 'while loop',
        'si': 'if conditional',
        'sino si': 'elseif',
        'sino': 'else',
        'intentar': 'try block',
        'capturar': 'catch block',
        'usar': 'using package',
        'importar': 'import package',
        'grafico': 'plot',
        'histograma': 'histogram',
        'scatter': 'scatter plot',
        'dataframe': 'DataFrame',
        'leer csv': 'read CSV',
        'escribir csv': 'write CSV',
        'entrenar modelo': 'train model',
        'predecir': 'predict',
        'paralelo': 'parallel execution',
        'tiempo': '@time macro',
        'benchmark': '@benchmark macro',
        'imprimir': 'println',
        'leer archivo': 'read file',
        'escribir archivo': 'write file'
    }
