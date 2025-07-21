def transpile_to_solidity(code):
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_contract = False
    in_function = False
    in_modifier = False
    contract_name = "MiContrato"
    pragma_added = False
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 4
        output.append(" " * current_indent + text)
    
    # Agregar pragma si no existe
    if not pragma_added:
        add_line("// SPDX-License-Identifier: MIT")
        add_line("pragma solidity ^0.8.0;")
        add_line("")
        pragma_added = True

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Contratos (equivalente a clases en Solidity)
        if line.startswith("contrato") or line.startswith("clase"):
            parts = line.split()
            contract_name = parts[1]
            
            # Herencia
            if len(parts) > 3 and parts[2] == "hereda":
                parent = parts[3]
                add_line(f"contract {contract_name} is {parent} {{")
            else:
                add_line(f"contract {contract_name} {{")
            in_contract = True
            indent += 1
            continue

        if line == "fin contrato" or line == "fin clase":
            indent -= 1
            add_line("}")
            in_contract = False
            continue

        # Variables de estado (atributos)
        if line.startswith("atributo") or line.startswith("variable_estado"):
            parts = line.split()
            name = parts[1]
            
            # Detectar tipo y visibilidad
            visibility = "public"
            sol_type = "uint256"
            
            if len(parts) > 3 and parts[2] == "tipo":
                tipo = parts[3]
                type_map = {
                    'numero': 'uint256',
                    'entero': 'int256',
                    'direccion': 'address',
                    'texto': 'string',
                    'booleano': 'bool',
                    'bytes': 'bytes32',
                    'dinero': 'uint256'
                }
                sol_type = type_map.get(tipo, tipo)
            
            if "privado" in line:
                visibility = "private"
            elif "interno" in line:
                visibility = "internal"
            
            if "=" in line:
                value = line.split("=", 1)[1].strip()
                add_line(f"{sol_type} {visibility} {name} = {value};")
            else:
                add_line(f"{sol_type} {visibility} {name};")
            continue

        # Constructor
        if line.startswith("constructor"):
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        type_map = {
                            'numero': 'uint256',
                            'direccion': 'address',
                            'texto': 'string',
                            'booleano': 'bool'
                        }
                        sol_type = type_map.get(param_type.strip(), param_type.strip())
                        params.append(f"{sol_type} {param_name.strip()}")
                    else:
                        params.append(f"uint256 {param.strip()}")
                add_line(f"constructor({', '.join(params)}) {{")
            else:
                add_line("constructor() {")
            indent += 1
            continue

        if line == "fin constructor":
            indent -= 1
            add_line("}")
            continue

        # Funciones
        if line.startswith("funcion"):
            func_decl = line[len("funcion"):].strip()
            
            # Detectar visibilidad y modificadores
            visibility = "public"
            state_mutability = ""
            
            if "privada" in line:
                visibility = "private"
            elif "interna" in line:
                visibility = "internal"
            elif "externa" in line:
                visibility = "external"
            
            if "pura" in line:
                state_mutability = "pure"
            elif "vista" in line:
                state_mutability = "view"
            elif "pagable" in line:
                state_mutability = "payable"
            
            if "(" in func_decl and ")" in func_decl:
                name = func_decl.split("(")[0].strip()
                params_part = func_decl.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        type_map = {
                            'numero': 'uint256',
                            'direccion': 'address',
                            'texto': 'string',
                            'booleano': 'bool',
                            'bytes': 'bytes32'
                        }
                        sol_type = type_map.get(param_type.strip(), param_type.strip())
                        params.append(f"{sol_type} {param_name.strip()}")
                    else:
                        params.append(f"uint256 {param.strip()}")
                
                # Detectar tipo de retorno
                return_type = ""
                if "->" in func_decl:
                    ret_type = func_decl.split("->")[1].strip()
                    type_map = {
                        'numero': 'uint256',
                        'direccion': 'address',
                        'texto': 'string',
                        'booleano': 'bool',
                        'bytes': 'bytes32'
                    }
                    return_type = f"returns ({type_map.get(ret_type, ret_type)})"
                
                modifiers = f"{visibility} {state_mutability}".strip()
                add_line(f"function {name}({', '.join(params)}) {modifiers} {return_type} {{")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                modifiers = f"{visibility} {state_mutability}".strip()
                add_line(f"function {name}() {modifiers} {{")
            
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            indent -= 1
            add_line("}")
            in_function = False
            continue

        # Modificadores
        if line.startswith("modificador"):
            name = line.split()[1]
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        type_map = {
                            'numero': 'uint256',
                            'direccion': 'address',
                            'texto': 'string',
                            'booleano': 'bool'
                        }
                        sol_type = type_map.get(param_type.strip(), param_type.strip())
                        params.append(f"{sol_type} {param_name.strip()}")
                    else:
                        params.append(f"uint256 {param.strip()}")
                add_line(f"modifier {name}({', '.join(params)}) {{")
            else:
                add_line(f"modifier {name}() {{")
            in_modifier = True
            indent += 1
            continue

        if line == "fin modificador":
            add_line("_;")  # Placeholder del modificador
            indent -= 1
            add_line("}")
            in_modifier = False
            continue

        # Eventos
        if line.startswith("evento"):
            parts = line.split()
            name = parts[1]
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        type_map = {
                            'numero': 'uint256',
                            'direccion': 'address',
                            'texto': 'string',
                            'booleano': 'bool'
                        }
                        sol_type = type_map.get(param_type.strip(), param_type.strip())
                        indexed = "indexed " if "indexado" in param else ""
                        params.append(f"{indexed}{sol_type} {param_name.strip()}")
                    else:
                        params.append(f"uint256 {param.strip()}")
                add_line(f"event {name}({', '.join(params)});")
            else:
                add_line(f"event {name}();")
            continue

        # Emitir eventos
        if line.startswith("emitir"):
            event_call = line[len("emitir"):].strip()
            add_line(f"emit {event_call};")
            continue

        # Require (validaciones)
        if line.startswith("requerir"):
            condition = line[len("requerir"):].strip()
            if " mensaje " in condition:
                parts = condition.split(" mensaje ", 1)
                cond = parts[0].strip()
                msg = parts[1].strip()
                add_line(f"require({cond}, {msg});")
            else:
                add_line(f"require({condition});")
            continue

        # Assert
        if line.startswith("afirmar"):
            condition = line[len("afirmar"):].strip()
            add_line(f"assert({condition});")
            continue

        # Revert
        if line.startswith("revertir"):
            message = line[len("revertir"):].strip()
            if message:
                add_line(f"revert({message});")
            else:
                add_line("revert();")
            continue

        # Transferencias de Ether
        if line.startswith("transferir"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "a":
                amount = parts[1]
                recipient = parts[3]
                add_line(f"payable({recipient}).transfer({amount});")
            continue

        if line.startswith("enviar"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "a":
                amount = parts[1]
                recipient = parts[3]
                add_line(f"payable({recipient}).send({amount});")
            continue

        # Llamadas a otros contratos
        if line.startswith("llamar_contrato"):
            call = line[len("llamar_contrato"):].strip()
            add_line(f"{call};")
            continue

        # Mapeos
        if line.startswith("mapeo"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_part = parts[0][len("mapeo"):].strip()
                mapping_def = parts[1].strip()
                # Ejemplo: mapeo balances = direccion => numero
                if "=>" in mapping_def:
                    key_type, value_type = mapping_def.split("=>", 1)
                    type_map = {
                        'numero': 'uint256',
                        'direccion': 'address',
                        'texto': 'string',
                        'booleano': 'bool'
                    }
                    key_sol = type_map.get(key_type.strip(), key_type.strip())
                    value_sol = type_map.get(value_type.strip(), value_type.strip())
                    add_line(f"mapping({key_sol} => {value_sol}) public {var_part};")
            continue

        # Arrays
        if line.startswith("array"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("array"):].strip()
                array_def = parts[1].strip()
                if "tipo" in array_def:
                    tipo = array_def.split("tipo")[1].strip()
                    type_map = {
                        'numero': 'uint256',
                        'direccion': 'address',
                        'texto': 'string',
                        'booleano': 'bool'
                    }
                    sol_type = type_map.get(tipo, tipo)
                    add_line(f"{sol_type}[] public {var_name};")
            continue

        # Estructuras
        if line.startswith("estructura") or line.startswith("struct"):
            name = line.split()[1]
            add_line(f"struct {name} {{")
            indent += 1
            continue

        if line == "fin estructura" or line == "fin struct":
            indent -= 1
            add_line("}")
            continue

        # Enums
        if line.startswith("enum"):
            name = line.split()[1]
            add_line(f"enum {name} {{")
            indent += 1
            continue

        if line == "fin enum":
            indent -= 1
            add_line("}")
            continue

        # Condicionales
        if line.startswith("si "):
            condition = line[len("si "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" y también ", " && ")
            condition = condition.replace(" o también ", " || ")
            add_line(f"if ({condition}) {{")
            indent += 1
            continue

        if line == "sino" or line == "si no":
            indent -= 1
            add_line("} else {")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line("}")
            continue

        # Bucles
        if line.startswith("repetir ") and " veces" in line:
            times = line.split()[1]
            add_line(f"for (uint256 i = 0; i < {times}; i++) {{")
            indent += 1
            continue

        if line.startswith("repetir mientras "):
            condition = line[len("repetir mientras "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            add_line(f"while ({condition}) {{")
            indent += 1
            continue

        if line == "fin repetir":
            indent -= 1
            add_line("}")
            continue

        # Return
        if line.startswith("retornar") or line.startswith("devolver"):
            value = line.split(None, 1)[1] if len(line.split()) > 1 else ""
            add_line(f"return {value};")
            continue

        # Variables especiales de Solidity
        if line.startswith("msg_sender"):
            add_line("msg.sender")
            continue

        if line.startswith("msg_value"):
            add_line("msg.value")
            continue

        if line.startswith("block_timestamp"):
            add_line("block.timestamp")
            continue

        if line.startswith("block_number"):
            add_line("block.number")
            continue

        if line.startswith("tx_origin"):
            add_line("tx.origin")
            continue

        # Conversiones de unidades
        if line.startswith("wei"):
            value = line[len("wei"):].strip()
            add_line(f"{value} wei")
            continue

        if line.startswith("gwei"):
            value = line[len("gwei"):].strip()
            add_line(f"{value} gwei")
            continue

        if line.startswith("ether"):
            value = line[len("ether"):].strip()
            add_line(f"{value} ether")
            continue

        # Importaciones
        if line.startswith("importar"):
            module = line[len("importar"):].strip()
            add_line(f"import \"{module}\";")
            continue

        # Interfaces
        if line.startswith("interfaz"):
            name = line.split()[1]
            add_line(f"interface {name} {{")
            indent += 1
            continue

        if line == "fin interfaz":
            indent -= 1
            add_line("}")
            continue

        # Librerías
        if line.startswith("libreria"):
            name = line.split()[1]
            add_line(f"library {name} {{")
            indent += 1
            continue

        if line == "fin libreria":
            indent -= 1
            add_line("}")
            continue

        # Using para librerías
        if line.startswith("usar"):
            parts = line.split(" para ")
            if len(parts) == 2:
                library = parts[0][len("usar"):].strip()
                target = parts[1].strip()
                add_line(f"using {library} for {target};")
            continue

        # Asignaciones y expresiones
        if "=" in line:
            add_line(f"{line};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")
    
    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_solidity(codigo)

# Funciones auxiliares para el transpilador de Solidity
def get_solidity_keywords():
    """Retorna las palabras clave de Vader que se mapean a Solidity"""
    return {
        'contrato': 'contract',
        'interfaz': 'interface',
        'libreria': 'library',
        'estructura': 'struct',
        'enum': 'enum',
        'funcion': 'function',
        'modificador': 'modifier',
        'evento': 'event',
        'constructor': 'constructor',
        'si': 'if',
        'sino': 'else',
        'repetir': 'for',
        'mientras': 'while',
        'retornar': 'return',
        'requerir': 'require',
        'afirmar': 'assert',
        'revertir': 'revert',
        'emitir': 'emit',
        'transferir': 'transfer',
        'enviar': 'send',
        'importar': 'import',
        'usar': 'using',
        'mapeo': 'mapping',
        'array': 'array',
        'msg_sender': 'msg.sender',
        'msg_value': 'msg.value',
        'block_timestamp': 'block.timestamp',
        'block_number': 'block.number',
        'tx_origin': 'tx.origin',
        'wei': 'wei',
        'gwei': 'gwei',
        'ether': 'ether',
        'publico': 'public',
        'privado': 'private',
        'interno': 'internal',
        'externo': 'external',
        'pura': 'pure',
        'vista': 'view',
        'pagable': 'payable'
    }
