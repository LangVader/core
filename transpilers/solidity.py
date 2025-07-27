#!/usr/bin/env python3
"""
Transpilador de Vader a Solidity
Convierte código Vader en español natural a Solidity válido y funcional
"""

import re

class SolidityTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.contract_name = "VaderContract"
        self.current_struct = None
        self.declared_vars = set()
        
    def indent(self):
        return '    ' * self.indent_level
    
    def separate_code_sections(self, lines):
        """Separa el código en funciones, structs y main"""
        functions_code = []
        structs_code = []
        main_code = []
        
        in_function = False
        in_struct = False
        current_block = []
        
        for line in lines:
            stripped = line.strip()
            
            # Detectar inicio de función
            if stripped.startswith('funcion ') or stripped.startswith('función '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_function = True
                in_struct = False
                current_block = [line]
                continue
            
            # Detectar inicio de struct
            elif stripped.startswith('clase '):
                if current_block:
                    main_code.extend(current_block)
                    current_block = []
                in_struct = True
                in_function = False
                current_block = [line]
                continue
            
            # Detectar fin de bloques
            elif stripped in ['fin', 'fin funcion', 'fin función']:
                if in_function:
                    current_block.append(line)
                    functions_code.extend(current_block)
                    functions_code.append('')
                    in_function = False
                    current_block = []
                    continue
            
            elif stripped in ['fin clase']:
                if in_struct:
                    current_block.append(line)
                    structs_code.extend(current_block)
                    structs_code.append('')
                    in_struct = False
                    current_block = []
                    continue
            
            # Agregar líneas al bloque actual
            if in_function or in_struct:
                current_block.append(line)
            else:
                current_block.append(line)
        
        # Agregar código restante a main
        if current_block:
            main_code.extend(current_block)
        
        return functions_code, structs_code, main_code
    
    def transpile(self, vader_code):
        """Transpila código Vader completo a Solidity - VERSIÓN COMPLETA"""
        lines = [line.strip() for line in vader_code.split('\n') if line.strip()]
        
        # Separar código en secciones
        functions_code, structs_code, main_code = self.separate_code_sections(lines)
        
        solidity_lines = [
            '// SPDX-License-Identifier: MIT',
            'pragma solidity ^0.8.0;',
            '',
            'import "@openzeppelin/contracts/utils/math/SafeMath.sol";',
            ''
        ]
        
        # Procesar structs primero
        if structs_code:
            for line in structs_code:
                if line.strip():
                    solidity_line = self.process_code_line(line)
                    if solidity_line:
                        if isinstance(solidity_line, list):
                            solidity_lines.extend(solidity_line)
                        else:
                            solidity_lines.append(solidity_line)
            solidity_lines.append('')
        
        # Iniciar contrato
        solidity_lines.extend([
            f'contract {self.contract_name} {{',
            '    using SafeMath for uint256;',
            '    ',
            '    event Message(string message);',
            '    event NumberResult(uint256 result);',
            '    event Error(string error);',
            ''
        ])
        
        # Procesar funciones
        if functions_code:
            for line in functions_code:
                if line.strip():
                    solidity_line = self.process_code_line(line)
                    if solidity_line:
                        if isinstance(solidity_line, list):
                            solidity_lines.extend(solidity_line)
                        else:
                            solidity_lines.append(solidity_line)
            solidity_lines.append('')
        
        # Procesar función principal
        solidity_lines.append('    function execute() public {')
        self.indent_level = 2
        
        for line in main_code:
            if line.strip():
                if line.startswith('#'):
                    solidity_lines.append(self.indent() + '//' + line[1:])
                else:
                    solidity_line = self.process_code_line(line)
                    if solidity_line:
                        if isinstance(solidity_line, list):
                            solidity_lines.extend(solidity_line)
                        else:
                            solidity_lines.append(solidity_line)
        
        solidity_lines.extend([
            '    }',
            '}'
        ])
        
        return '\n'.join(solidity_lines)
    
    def process_code_line(self, line):
        """Procesa una línea de código - VERSIÓN COMPLETA"""
        # Fin de bloque
        if line in ['fin', 'fin funcion', 'fin función', 'fin clase', 'fin si', 'fin mientras', 'fin repetir']:
            if self.indent_level > 0:
                self.indent_level -= 1
                return '    ' * self.indent_level + '}'
            return None
        
        current_indent = '    ' * self.indent_level
        
        # Variables booleanas
        line = line.replace('verdadero', 'true')
        line = line.replace('falso', 'false')
        line = line.replace('nulo', 'address(0)')
        
        # Operaciones matemáticas con SafeMath
        line = re.sub(r'raiz\(([^)]+)\)', r'sqrt(\1)', line)
        line = re.sub(r'potencia\(([^,]+),\s*([^)]+)\)', r'(\1 ** \2)', line)
        line = re.sub(r'absoluto\(([^)]+)\)', r'abs(\1)', line)
        line = re.sub(r'redondear\(([^)]+)\)', r'\1', line)  # Solidity no tiene decimales nativos
        line = re.sub(r'numero\(([^)]+)\)', r'uint256(\1)', line)
        
        # Definición de funciones avanzadas con tipos
        if line.startswith('funcion ') or line.startswith('función '):
            func_def = line.replace('funcion ', '').replace('función ', '')
            
            # Detectar tipo de retorno
            return_type = ''
            if ' que devuelve ' in func_def:
                parts = func_def.split(' que devuelve ')
                func_def = parts[0]
                return_type_str = parts[1].replace(':', '').strip()
                if return_type_str in ['numero', 'entero']:
                    return_type = ' returns (uint256)'
                elif return_type_str in ['decimal', 'flotante']:
                    return_type = ' returns (uint256)'
                elif return_type_str in ['texto', 'cadena']:
                    return_type = ' returns (string memory)'
                elif return_type_str in ['booleano', 'logico']:
                    return_type = ' returns (bool)'
            
            if ' con ' in func_def:
                name, params = func_def.split(' con ', 1)
                name = name.strip()
                params_str = params.replace(':', '').strip()
                
                # Procesar parámetros con tipos
                typed_params = []
                if params_str:
                    param_list = [p.strip() for p in params_str.replace(' y ', ', ').split(',')]
                    for param in param_list:
                        if ' tipo ' in param:
                            param_parts = param.split(' tipo ')
                            param_name = param_parts[0].strip()
                            param_type = param_parts[1].strip()
                            if param_type in ['numero', 'entero']:
                                typed_params.append(f'uint256 {param_name}')
                            elif param_type in ['decimal', 'flotante']:
                                typed_params.append(f'uint256 {param_name}')
                            elif param_type in ['texto', 'cadena']:
                                typed_params.append(f'string memory {param_name}')
                            elif param_type in ['booleano', 'logico']:
                                typed_params.append(f'bool {param_name}')
                            else:
                                typed_params.append(f'string memory {param_name}')
                        else:
                            typed_params.append(f'string memory {param}')
                
                params_final = ', '.join(typed_params)
                self.indent_level += 1
                return current_indent + f'function {name}({params_final}) public{return_type} {{'
            else:
                name = func_def.replace(':', '').strip()
                self.indent_level += 1
                return current_indent + f'function {name}() public{return_type} {{'
        
        # Retorno de funciones
        if line.startswith('retornar ') or line.startswith('devolver '):
            value = line.replace('retornar ', '').replace('devolver ', '').strip()
            return current_indent + f'return {value};'
        
        # Definición de structs avanzados
        if line.startswith('clase '):
            struct_name = line.replace('clase ', '').replace(':', '').strip()
            self.current_struct = struct_name
            return f'struct {struct_name} {{'
        
        # Atributos de struct
        if line.startswith('atributo '):
            attr_def = line.replace('atributo ', '').strip()
            if ' tipo ' in attr_def:
                attr_parts = attr_def.split(' tipo ')
                attr_name = attr_parts[0].strip()
                attr_type = attr_parts[1].strip()
                if attr_type in ['numero', 'entero']:
                    return f'    uint256 {attr_name};'
                elif attr_type in ['decimal', 'flotante']:
                    return f'    uint256 {attr_name};'
                elif attr_type in ['texto', 'cadena']:
                    return f'    string {attr_name};'
                elif attr_type in ['booleano', 'logico']:
                    return f'    bool {attr_name};'
                else:
                    return f'    string {attr_name};'
            else:
                return f'    string {attr_def};'
        
        # Constructor de struct
        if line.startswith('constructor con '):
            params = line.replace('constructor con ', '').replace(':', '').strip()
            if params:
                # Procesar parámetros con tipos explícitos
                typed_params = []
                param_list = [p.strip() for p in params.replace(' y ', ', ').split(',')]
                for param in param_list:
                    if ' tipo ' in param:
                        param_parts = param.split(' tipo ')
                        param_name = param_parts[0].strip()
                        param_type = param_parts[1].strip()
                        if param_type in ['numero', 'entero']:
                            typed_params.append(f'uint256 _{param_name}')
                        elif param_type in ['decimal', 'flotante']:
                            typed_params.append(f'uint256 _{param_name}')
                        elif param_type in ['texto', 'cadena']:
                            typed_params.append(f'string memory _{param_name}')
                        elif param_type in ['booleano', 'logico']:
                            typed_params.append(f'bool _{param_name}')
                        else:
                            typed_params.append(f'string memory _{param_name}')
                    else:
                        typed_params.append(f'string memory _{param}')
                
                params_final = ', '.join(typed_params)
                constructor_lines = [
                    '}',
                    '',
                    f'contract {self.current_struct}Contract {{',
                    f'    {self.current_struct} public data;',
                    '',
                    f'    constructor({params_final}) {{'
                ]
                self.indent_level += 2
                return constructor_lines
            else:
                constructor_lines = [
                    '}',
                    '',
                    f'contract {self.current_struct}Contract {{',
                    f'    {self.current_struct} public data;',
                    '',
                    f'    constructor() {{'
                ]
                self.indent_level += 2
                return constructor_lines
        
        # Variables con tipos explícitos
        if line.startswith('crear variable ') and ' tipo ' in line:
            var_def = line.replace('crear variable ', '').strip()
            if ' tipo ' in var_def:
                var_parts = var_def.split(' tipo ')
                var_name = var_parts[0].strip()
                var_type = var_parts[1].strip()
                if var_type in ['numero', 'entero']:
                    return current_indent + f'uint256 {var_name};'
                elif var_type in ['decimal', 'flotante']:
                    return current_indent + f'uint256 {var_name};'
                elif var_type in ['texto', 'cadena']:
                    return current_indent + f'string memory {var_name};'
                elif var_type in ['booleano', 'logico']:
                    return current_indent + f'bool {var_name};'
                else:
                    return current_indent + f'string memory {var_name};'
        
        # Crear arrays
        if line.startswith('crear array ') and '[' in line and ']' in line:
            array_def = line.replace('crear array ', '').strip()
            if '[' in array_def and ']' in array_def:
                array_name = array_def.split('[')[0].strip()
                array_size = array_def.split('[')[1].split(']')[0].strip()
                return current_indent + f'uint256[{array_size}] memory {array_name};'
        
        # Crear listas/arrays dinámicos
        if line.startswith('crear lista '):
            list_name = line.replace('crear lista ', '').strip()
            return current_indent + f'string[] memory {list_name} = new string[](0);'
        
        # Crear mappings
        if line.startswith('crear mapa '):
            map_name = line.replace('crear mapa ', '').strip()
            return current_indent + f'mapping(string => string) {map_name};'
        
        # Manejo de errores con require/revert (estilo Solidity)
        if line.startswith('intentar'):
            # En Solidity usamos require para validaciones
            return current_indent + '// Error handling block'
        
        if line.startswith('capturar '):
            exception_type = line.replace('capturar ', '').strip()
            return current_indent + f'// Catch block for {exception_type}'
        
        if line.startswith('finalmente'):
            return current_indent + '// Finally block executed'
        
        if line.startswith('lanzar '):
            exception = line.replace('lanzar ', '').strip()
            return current_indent + f'revert({exception});'
        
        # Condicionales
        if line.startswith('si ') and ('entonces' in line or line.endswith(':')):
            condition = line.replace('si ', '').replace(' entonces', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'if ({condition}) {{'
        
        # Else
        if line == 'sino' or line == 'si no' or line == 'sino:':
            if self.indent_level > 0:
                self.indent_level -= 1
            else_indent = '    ' * self.indent_level
            self.indent_level += 1
            return else_indent + '} else {'
        
        # Bucles for
        if line.startswith('repetir ') and ' veces' in line:
            times = line.replace('repetir ', '').replace(' veces', '').strip()
            self.indent_level += 1
            return current_indent + f'for (uint256 i = 0; i < {times}; i++) {{'
        
        # Bucles while
        if line.startswith('mientras '):
            condition = line.replace('mientras ', '').replace(':', '').strip()
            condition = self.convert_operators(condition)
            self.indent_level += 1
            return current_indent + f'while ({condition}) {{'
        
        # Print statements (emit events)
        if line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            # Detectar si es número o string
            if content.isdigit() or (content.startswith('resultado') and 'matemático' in line):
                return current_indent + f'emit NumberResult({content});'
            else:
                return current_indent + f'emit Message({content});'
        
        # Validaciones con require (manejo de errores Solidity)
        if 'numero(' in line and '"' in line:
            # Convertir validaciones de números a require statements
            return current_indent + 'require(false, "Error al convertir número");'
        
        # Agregar require statements para validaciones
        if line.startswith('uint256("'):
            return current_indent + 'require(false, "Invalid number conversion");'
        
        # Asignación de variables
        if '=' in line and not any(op in line for op in ['==', '!=', '>=', '<=']):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            if var_name not in self.declared_vars:
                self.declared_vars.add(var_name)
                # Inferir tipo basado en el valor
                if value.isdigit():
                    return current_indent + f'uint256 {var_name} = {value};'
                elif value.startswith('"') and value.endswith('"'):
                    return current_indent + f'string memory {var_name} = {value};'
                elif value in ['true', 'false']:
                    return current_indent + f'bool {var_name} = {value};'
                else:
                    return current_indent + f'uint256 {var_name} = {value};'
            else:
                return current_indent + f'{var_name} = {value};'
        
        # Línea de código general
        if line.strip():
            return current_indent + line + ';'
        
        return None
    
    def convert_operators(self, condition):
        """Convierte operadores de Vader a Solidity"""
        condition = condition.replace(' es igual a ', ' == ')
        condition = condition.replace(' es mayor que ', ' > ')
        condition = condition.replace(' es menor que ', ' < ')
        condition = condition.replace(' mayor que ', ' > ')
        condition = condition.replace(' menor que ', ' < ')
        condition = condition.replace(' igual a ', ' == ')
        condition = condition.replace(' y ', ' && ')
        condition = condition.replace(' o ', ' || ')
        condition = condition.replace(' no ', ' ! ')
        return condition

def transpile_to_solidity(vader_code):
    transpiler = SolidityTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_solidity(vader_code)
