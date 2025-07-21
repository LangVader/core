# Transpilador Blazor para Vader
# Convierte sintaxis natural a Blazor C# para aplicaciones web

def transpile_blazor(code):
    """Transpila código Vader a Blazor C#"""
    lines = code.split('\n')
    result = []
    
    # Encabezado Blazor
    result.extend([
        '@page "/"',
        '@using Microsoft.AspNetCore.Components',
        '',
        '<PageTitle>Aplicación Blazor</PageTitle>',
        ''
    ])
    
    in_component = False
    component_name = "MiComponente"
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('componente blazor'):
            # Extraer nombre del componente
            if '"' in line:
                component_name = line.split('"')[1]
            in_component = True
            result.append(f'<h3>{component_name}</h3>')
            
        elif line.startswith('estado'):
            # Variables de estado
            var_name = line.replace('estado', '').strip().strip('"')
            result.append(f'@code {{')
            result.append(f'    private string {var_name} = "";')
            result.append(f'}}')
            
        elif line.startswith('mostrar'):
            # Mostrar contenido
            content = line.replace('mostrar', '').strip().strip('"')
            if content.startswith('estado.'):
                var_name = content.replace('estado.', '')
                result.append(f'<p>@{var_name}</p>')
            else:
                result.append(f'<p>{content}</p>')
                
        elif line.startswith('boton'):
            # Botón con evento
            text = line.replace('boton', '').strip().strip('"')
            result.append(f'<button class="btn btn-primary" @onclick="OnButtonClick">{text}</button>')
            
        elif line.startswith('campo'):
            # Campo de entrada
            parts = line.replace('campo', '').strip().split('"')
            if len(parts) >= 3:
                name = parts[1]
                placeholder = parts[3] if len(parts) > 3 else ''
                result.append(f'<input @bind="{name}" placeholder="{placeholder}" class="form-control" />')
                
        elif line.startswith('lista'):
            # Lista de elementos
            result.append('<ul class="list-group">')
            
        elif line.startswith('elemento'):
            # Elemento de lista
            content = line.replace('elemento', '').strip().strip('"')
            result.append(f'    <li class="list-group-item">{content}</li>')
            
        elif line.startswith('fin lista'):
            result.append('</ul>')
            
        elif line.startswith('al hacer_click'):
            # Método de evento
            result.extend([
                '',
                '@code {',
                '    private void OnButtonClick()',
                '    {',
                '        // Lógica del evento'
            ])
            
        elif line.startswith('fin evento'):
            result.extend([
                '    }',
                '}'
            ])
            
        elif line.startswith('servicio'):
            # Inyección de servicios
            service_name = line.replace('servicio', '').strip().strip('"')
            result.append(f'@inject {service_name} {service_name.lower()}Service')
            
        elif line.startswith('navegar_a'):
            # Navegación
            url = line.replace('navegar_a', '').strip().strip('"')
            result.append(f'NavigationManager.NavigateTo("{url}");')
            
        elif line.startswith('formulario'):
            # Formulario
            result.append('<EditForm>')
            
        elif line.startswith('fin formulario'):
            result.append('</EditForm>')
            
        elif line.startswith('validacion'):
            # Validación
            result.append('<DataAnnotationsValidator />')
            result.append('<ValidationSummary />')
    
    return '\n'.join(result)

# Palabras clave específicas de Blazor
BLAZOR_KEYWORDS = [
    'componente blazor', 'estado', 'servicio', 'navegar_a', 'al hacer_click',
    'formulario', 'validacion', 'inyectar'
]

def detect_blazor(code):
    """Detecta si el código contiene sintaxis específica de Blazor"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in BLAZOR_KEYWORDS)
