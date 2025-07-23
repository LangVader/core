# Solidity Transpiler for Vader
# Converts Vader syntax to Solidity code

class SolidityTranspiler:
    def __init__(self):
        self.indent_level = 0
        self.contract_name = "VaderContract"
    
    def transpile(self, vader_code):
        """Transpile Vader code to Solidity"""
        lines = vader_code.split('\n')
        solidity_lines = [
            '// SPDX-License-Identifier: MIT',
            'pragma solidity ^0.8.0;',
            '',
            f'contract {self.contract_name} {{',
            '    event Message(string message);',
            '',
            '    function execute() public {'
        ]
        
        self.indent_level = 2
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            solidity_line = self.transpile_line(line)
            if solidity_line:
                solidity_lines.append(solidity_line)
        
        solidity_lines.extend([
            '    }',
            '}'
        ])
        
        return '\n'.join(solidity_lines)
    
    def transpile_line(self, line):
        """Transpile a single line"""
        # Print statements (emit events in Solidity)
        if line.startswith('decir ') or line.startswith('mostrar '):
            content = line.split(' ', 1)[1]
            return self.indent() + f'emit Message({content});'
        
        # Variable declarations
        if ' = ' in line and not line.startswith('if'):
            return self.indent() + 'string memory ' + line + ';'
        
        return self.indent() + line + ';'
    
    def indent(self):
        return '    ' * self.indent_level

def transpile_to_solidity(vader_code):
    transpiler = SolidityTranspiler()
    return transpiler.transpile(vader_code)

def transpilar(vader_code):
    """Alias for CLI compatibility"""
    return transpile_to_solidity(vader_code)
