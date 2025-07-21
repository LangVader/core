# Transpilador Spring Boot para Vader
# Convierte sintaxis natural a Spring Boot Java para aplicaciones backend

def transpile_spring_boot(code):
    """Transpila código Vader a Spring Boot Java"""
    lines = code.split('\n')
    result = []
    
    # Imports y anotaciones básicas de Spring Boot
    result.extend([
        'package com.vader.app;',
        '',
        'import org.springframework.boot.SpringApplication;',
        'import org.springframework.boot.autoconfigure.SpringBootApplication;',
        'import org.springframework.web.bind.annotation.*;',
        'import org.springframework.stereotype.Service;',
        'import org.springframework.beans.factory.annotation.Autowired;',
        'import org.springframework.data.jpa.repository.JpaRepository;',
        'import javax.persistence.*;',
        'import java.util.List;',
        '',
        '@SpringBootApplication',
        'public class VaderApplication {',
        '    public static void main(String[] args) {',
        '        SpringApplication.run(VaderApplication.class, args);',
        '    }',
        '}',
        ''
    ])
    
    in_controller = False
    in_service = False
    in_entity = False
    controller_name = "MiController"
    service_name = "MiService"
    entity_name = "MiEntidad"
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('controlador spring'):
            # Controlador REST
            if '"' in line:
                controller_name = line.split('"')[1]
            in_controller = True
            result.extend([
                '@RestController',
                '@RequestMapping("/api")',
                f'public class {controller_name} {{',
                ''
            ])
            
        elif line.startswith('servicio spring'):
            # Servicio de negocio
            if '"' in line:
                service_name = line.split('"')[1]
            in_service = True
            result.extend([
                '@Service',
                f'public class {service_name} {{',
                ''
            ])
            
        elif line.startswith('entidad spring'):
            # Entidad JPA
            if '"' in line:
                entity_name = line.split('"')[1]
            in_entity = True
            result.extend([
                '@Entity',
                '@Table(name = "' + entity_name.lower() + '")',
                f'public class {entity_name} {{',
                '    @Id',
                '    @GeneratedValue(strategy = GenerationType.IDENTITY)',
                '    private Long id;',
                ''
            ])
            
        elif line.startswith('ruta get'):
            # Endpoint GET
            path = line.replace('ruta get', '').strip().strip('"')
            result.extend([
                f'    @GetMapping("{path}")',
                f'    public ResponseEntity<?> get{path.replace("/", "").title()}() {{',
                '        // Lógica del endpoint GET',
                '        return ResponseEntity.ok().build();',
                '    }',
                ''
            ])
            
        elif line.startswith('ruta post'):
            # Endpoint POST
            path = line.replace('ruta post', '').strip().strip('"')
            result.extend([
                f'    @PostMapping("{path}")',
                f'    public ResponseEntity<?> post{path.replace("/", "").title()}(@RequestBody Object data) {{',
                '        // Lógica del endpoint POST',
                '        return ResponseEntity.ok().build();',
                '    }',
                ''
            ])
            
        elif line.startswith('ruta put'):
            # Endpoint PUT
            path = line.replace('ruta put', '').strip().strip('"')
            result.extend([
                f'    @PutMapping("{path}/{{id}}")',
                f'    public ResponseEntity<?> put{path.replace("/", "").title()}(@PathVariable Long id, @RequestBody Object data) {{',
                '        // Lógica del endpoint PUT',
                '        return ResponseEntity.ok().build();',
                '    }',
                ''
            ])
            
        elif line.startswith('ruta delete'):
            # Endpoint DELETE
            path = line.replace('ruta delete', '').strip().strip('"')
            result.extend([
                f'    @DeleteMapping("{path}/{{id}}")',
                f'    public ResponseEntity<?> delete{path.replace("/", "").title()}(@PathVariable Long id) {{',
                '        // Lógica del endpoint DELETE',
                '        return ResponseEntity.ok().build();',
                '    }',
                ''
            ])
            
        elif line.startswith('campo'):
            # Campo de entidad
            parts = line.replace('campo', '').strip().split('"')
            if len(parts) >= 3:
                field_name = parts[1]
                field_type = parts[3]
                java_type = _convert_type_to_java(field_type)
                result.extend([
                    f'    @Column(name = "{field_name}")',
                    f'    private {java_type} {field_name};',
                    ''
                ])
                
        elif line.startswith('inyectar'):
            # Inyección de dependencias
            dependency = line.replace('inyectar', '').strip().strip('"')
            result.extend([
                f'    @Autowired',
                f'    private {dependency} {dependency.lower()};',
                ''
            ])
            
        elif line.startswith('metodo'):
            # Método de servicio
            method_name = line.replace('metodo', '').strip().strip('"')
            result.extend([
                f'    public void {method_name}() {{',
                '        // Lógica del método'
            ])
            
        elif line.startswith('fin metodo'):
            result.extend([
                '    }',
                ''
            ])
            
        elif line.startswith('repositorio'):
            # Repositorio JPA
            entity = line.replace('repositorio', '').strip().strip('"')
            result.extend([
                f'public interface {entity}Repository extends JpaRepository<{entity}, Long> {{',
                '    // Métodos de consulta personalizados',
                '}',
                ''
            ])
            
        elif line.startswith('buscar por'):
            # Query method
            field = line.replace('buscar por', '').strip().strip('"')
            field_capitalized = field.capitalize()
            result.append(f'    List<{entity_name}> findBy{field_capitalized}(String {field});')
            
        elif line.startswith('configuracion'):
            # Configuración
            result.extend([
                '@Configuration',
                'public class AppConfig {',
                ''
            ])
            
        elif line.startswith('bean'):
            # Bean de configuración
            bean_name = line.replace('bean', '').strip().strip('"')
            result.extend([
                f'    @Bean',
                f'    public {bean_name} {bean_name.lower()}() {{',
                f'        return new {bean_name}();',
                '    }',
                ''
            ])
            
        elif line.startswith('fin controlador') or line.startswith('fin servicio') or line.startswith('fin entidad') or line.startswith('fin configuracion'):
            result.append('}')
            result.append('')
            in_controller = False
            in_service = False
            in_entity = False
    
    return '\n'.join(result)

def _convert_type_to_java(vader_type):
    """Convierte tipos de Vader a tipos Java"""
    type_map = {
        'texto': 'String',
        'numero': 'Integer',
        'decimal': 'Double',
        'booleano': 'Boolean',
        'fecha': 'LocalDateTime',
        'lista': 'List<String>'
    }
    return type_map.get(vader_type, 'String')

# Palabras clave específicas de Spring Boot
SPRING_BOOT_KEYWORDS = [
    'controlador spring', 'servicio spring', 'entidad spring', 'ruta get', 'ruta post',
    'ruta put', 'ruta delete', 'inyectar', 'repositorio', 'buscar por', 'configuracion', 'bean'
]

def detect_spring_boot(code):
    """Detecta si el código contiene sintaxis específica de Spring Boot"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in SPRING_BOOT_KEYWORDS)
