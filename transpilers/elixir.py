def transpile_to_elixir(code):
    """Transpila código Vader a Elixir"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_module = False
    in_function = False
    in_genserver = False
    module_name = "MiModulo"
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Módulo Elixir
        if line.startswith("modulo"):
            module_name = line.split()[1] if len(line.split()) > 1 else "MiModulo"
            add_line(f"defmodule {module_name} do")
            in_module = True
            indent += 1
            continue

        if line == "fin modulo":
            add_line("end")
            in_module = False
            indent -= 1
            continue

        # GenServer
        if line.startswith("genserver"):
            server_name = line.split()[1] if len(line.split()) > 1 else "MiServidor"
            add_line(f"defmodule {server_name} do")
            add_line("  use GenServer")
            add_line("")
            add_line("  # Client API")
            add_line("  def start_link(initial_state \\\\ %{}) do")
            add_line(f"    GenServer.start_link(__MODULE__, initial_state, name: __MODULE__)")
            add_line("  end")
            add_line("")
            add_line("  def get_state do")
            add_line("    GenServer.call(__MODULE__, :get_state)")
            add_line("  end")
            add_line("")
            add_line("  # Server Callbacks")
            add_line("  @impl true")
            add_line("  def init(initial_state) do")
            add_line("    {:ok, initial_state}")
            add_line("  end")
            add_line("")
            in_genserver = True
            indent += 1
            continue

        if line == "fin genserver":
            add_line("end")
            in_genserver = False
            indent -= 1
            continue

        # Funciones
        if line.startswith("funcion"):
            parts = line.split()
            func_name = parts[1] if len(parts) > 1 else "mi_funcion"
            
            # Extraer parámetros si existen
            params = ""
            if "(" in line and ")" in line:
                param_part = line[line.find("(")+1:line.find(")")]
                if param_part:
                    # Convertir parámetros de Vader a Elixir
                    elixir_params = []
                    for param in param_part.split(","):
                        param = param.strip()
                        if param:
                            elixir_params.append(param)
                    params = ", ".join(elixir_params)
            
            if params:
                add_line(f"def {func_name}({params}) do")
            else:
                add_line(f"def {func_name} do")
            
            in_function = True
            indent += 1
            continue

        # Función privada
        if line.startswith("funcion privada"):
            parts = line.split()
            func_name = parts[2] if len(parts) > 2 else "mi_funcion_privada"
            
            params = ""
            if "(" in line and ")" in line:
                param_part = line[line.find("(")+1:line.find(")")]
                if param_part:
                    elixir_params = []
                    for param in param_part.split(","):
                        param = param.strip()
                        if param:
                            elixir_params.append(param)
                    params = ", ".join(elixir_params)
            
            if params:
                add_line(f"defp {func_name}({params}) do")
            else:
                add_line(f"defp {func_name} do")
            
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            add_line("end")
            in_function = False
            indent -= 1
            continue

        # Pattern matching
        if line.startswith("coincidir"):
            expression = line.replace("coincidir", "").strip()
            add_line(f"case {expression} do")
            indent += 1
            continue

        if line.startswith("patron"):
            pattern = line.replace("patron", "").strip()
            add_line(f"{pattern} ->")
            indent += 1
            continue

        if line == "fin patron":
            indent -= 1
            continue

        if line == "fin coincidir":
            indent -= 1
            add_line("end")
            continue

        # Condicionales
        if line.startswith("si"):
            condition = line.replace("si", "").strip()
            add_line(f"if {condition} do")
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

        # Bucles y enumeración
        if line.startswith("enumerar"):
            collection = line.replace("enumerar", "").strip()
            add_line(f"Enum.each({collection}, fn item ->")
            indent += 1
            continue

        if line.startswith("mapear"):
            parts = line.split("en")
            if len(parts) == 2:
                collection = parts[1].strip()
                add_line(f"Enum.map({collection}, fn item ->")
                indent += 1
            continue

        if line.startswith("filtrar"):
            parts = line.split("en")
            if len(parts) == 2:
                collection = parts[1].strip()
                add_line(f"Enum.filter({collection}, fn item ->")
                indent += 1
            continue

        if line.startswith("reducir"):
            parts = line.split("en")
            if len(parts) == 2:
                collection = parts[1].strip()
                add_line(f"Enum.reduce({collection}, fn item, acc ->")
                indent += 1
            continue

        if line == "fin enumerar" or line == "fin mapear" or line == "fin filtrar" or line == "fin reducir":
            indent -= 1
            add_line("end)")
            continue

        # Procesos y concurrencia
        if line.startswith("spawn"):
            func_call = line.replace("spawn", "").strip()
            add_line(f"spawn(fn -> {func_call} end)")
            continue

        if line.startswith("enviar"):
            parts = line.split("a")
            if len(parts) == 2:
                message = parts[0].replace("enviar", "").strip()
                process = parts[1].strip()
                add_line(f"send({process}, {message})")
            continue

        if line.startswith("recibir"):
            add_line("receive do")
            indent += 1
            continue

        if line == "fin recibir":
            indent -= 1
            add_line("end")
            continue

        # Tuplas y listas
        if line.startswith("tupla"):
            elements = line.replace("tupla", "").strip()
            add_line(f"{{{elements}}}")
            continue

        if line.startswith("lista"):
            elements = line.replace("lista", "").strip()
            add_line(f"[{elements}]")
            continue

        # Mapas
        if line.startswith("mapa"):
            elements = line.replace("mapa", "").strip()
            if elements:
                add_line(f"%{{{elements}}}")
            else:
                add_line("%{}")
            continue

        # Atoms
        if line.startswith("atom"):
            atom_name = line.replace("atom", "").strip()
            add_line(f":{atom_name}")
            continue

        # Pipes
        if line.startswith("tuberia"):
            pipe_expr = line.replace("tuberia", "").strip()
            add_line(pipe_expr.replace(" | ", " |> "))
            continue

        # Try/catch
        if line.startswith("intentar"):
            add_line("try do")
            indent += 1
            continue

        if line.startswith("capturar"):
            error_type = line.replace("capturar", "").strip()
            indent -= 1
            add_line(f"catch")
            add_line(f"  {error_type} ->")
            indent += 1
            continue

        if line == "fin intentar":
            indent -= 1
            add_line("end")
            continue

        # GenServer callbacks
        if in_genserver:
            if line.startswith("handle_call"):
                request = line.split()[1] if len(line.split()) > 1 else ":request"
                add_line("@impl true")
                add_line(f"def handle_call({request}, _from, state) do")
                indent += 1
                continue

            if line.startswith("handle_cast"):
                request = line.split()[1] if len(line.split()) > 1 else ":request"
                add_line("@impl true")
                add_line(f"def handle_cast({request}, state) do")
                indent += 1
                continue

            if line.startswith("handle_info"):
                message = line.split()[1] if len(line.split()) > 1 else ":message"
                add_line("@impl true")
                add_line(f"def handle_info({message}, state) do")
                indent += 1
                continue

        # Respuestas
        if line.startswith("responder"):
            response = line.replace("responder", "").strip()
            add_line(f"{{:reply, {response}, state}}")
            continue

        if line.startswith("no_responder"):
            add_line("{:noreply, state}")
            continue

        if line.startswith("devolver"):
            value = line.replace("devolver", "").strip()
            add_line(value)
            continue

        # IO
        if line.startswith("imprimir"):
            message = line.replace("imprimir", "").strip()
            add_line(f"IO.puts({message})")
            continue

        if line.startswith("inspeccionar"):
            value = line.replace("inspeccionar", "").strip()
            add_line(f"IO.inspect({value})")
            continue

        # Variables
        if "=" in line and not line.startswith("//"):
            # Convertir asignaciones de Vader a Elixir
            elixir_line = line
            add_line(elixir_line)
            continue

        # Otras líneas (comentarios)
        if in_function or in_module:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"IO.puts({message})")
            else:
                add_line(f"# {line}")

    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_elixir(codigo)

# Funciones auxiliares para el transpilador de Elixir
def get_elixir_keywords():
    """Retorna las palabras clave de Vader que se mapean a Elixir"""
    return {
        'modulo': 'defmodule',
        'genserver': 'GenServer module',
        'funcion': 'def function',
        'funcion privada': 'defp private function',
        'coincidir': 'case pattern matching',
        'patron': 'pattern case',
        'si': 'if conditional',
        'sino': 'else',
        'enumerar': 'Enum.each',
        'mapear': 'Enum.map',
        'filtrar': 'Enum.filter',
        'reducir': 'Enum.reduce',
        'spawn': 'spawn process',
        'enviar': 'send message',
        'recibir': 'receive block',
        'tupla': 'tuple',
        'lista': 'list',
        'mapa': 'map',
        'atom': 'atom',
        'tuberia': 'pipe operator',
        'intentar': 'try block',
        'capturar': 'catch block',
        'handle_call': 'GenServer handle_call',
        'handle_cast': 'GenServer handle_cast',
        'handle_info': 'GenServer handle_info',
        'responder': 'reply response',
        'no_responder': 'noreply response',
        'devolver': 'return value',
        'imprimir': 'IO.puts',
        'inspeccionar': 'IO.inspect'
    }
