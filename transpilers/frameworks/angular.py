def transpile_to_angular(code):
    """Transpila código Vader a Angular con TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_service = False
    in_module = False
    component_name = "MiComponente"
    imports = set()
    decorators_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def detect_angular_features(line):
        """Detecta características de Angular en el código"""
        if "componente" in line:
            decorators_used.add("Component")
        if "servicio" in line:
            decorators_used.add("Injectable")
        if "modulo" in line:
            decorators_used.add("NgModule")
        if "input" in line or "entrada" in line:
            decorators_used.add("Input")
        if "output" in line or "salida" in line:
            decorators_used.add("Output")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_angular_features(line)

        # Componente Angular
        if line.startswith("componente angular"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            
            # Selector y template
            selector = component_name.lower().replace("componente", "")
            template_file = f"./{selector}.component.html"
            style_file = f"./{selector}.component.css"
            
            add_line("@Component({")
            add_line(f"  selector: 'app-{selector}',")
            add_line(f"  templateUrl: '{template_file}',")
            add_line(f"  styleUrls: ['{style_file}']")
            add_line("})")
            add_line(f"export class {component_name} {{")
            in_component = True
            indent += 1
            continue

        if line == "fin componente":
            indent -= 1
            add_line("}")
            in_component = False
            continue

        # Servicio Angular
        if line.startswith("servicio"):
            parts = line.split()
            service_name = parts[1] if len(parts) > 1 else "MiServicio"
            
            add_line("@Injectable({")
            add_line("  providedIn: 'root'")
            add_line("})")
            add_line(f"export class {service_name} {{")
            in_service = True
            indent += 1
            continue

        if line == "fin servicio":
            indent -= 1
            add_line("}")
            in_service = False
            continue

        # Módulo Angular
        if line.startswith("modulo"):
            parts = line.split()
            module_name = parts[1] if len(parts) > 1 else "MiModulo"
            
            add_line("@NgModule({")
            add_line("  declarations: [],")
            add_line("  imports: [],")
            add_line("  providers: [],")
            add_line("  bootstrap: []")
            add_line("})")
            add_line(f"export class {module_name} {{")
            in_module = True
            indent += 1
            continue

        if line == "fin modulo":
            indent -= 1
            add_line("}")
            in_module = False
            continue

        # Propiedades de entrada (@Input)
        if line.startswith("entrada") or line.startswith("@Input"):
            prop_name = line.split()[1] if len(line.split()) > 1 else "data"
            prop_type = "any"
            
            if ":" in line:
                type_part = line.split(":")[1].strip()
                if "=" in type_part:
                    prop_type = type_part.split("=")[0].strip()
                else:
                    prop_type = type_part
            
            add_line(f"@Input() {prop_name}: {prop_type};")
            continue

        # Propiedades de salida (@Output)
        if line.startswith("salida") or line.startswith("@Output"):
            event_name = line.split()[1] if len(line.split()) > 1 else "evento"
            add_import("import { EventEmitter } from '@angular/core';")
            add_line(f"@Output() {event_name} = new EventEmitter<any>();")
            continue

        # Emitir eventos
        if line.startswith("emitir"):
            event_name = line.split()[1] if len(line.split()) > 1 else "evento"
            data = line.split()[2:] if len(line.split()) > 2 else ""
            data_str = " ".join(data) if data else "null"
            add_line(f"this.{event_name}.emit({data_str});")
            continue

        # Ciclo de vida de componentes
        if line.startswith("al inicializar") or line.startswith("ngOnInit"):
            add_import("import { OnInit } from '@angular/core';")
            add_line("ngOnInit(): void {")
            indent += 1
            continue

        if line.startswith("al destruir") or line.startswith("ngOnDestroy"):
            add_import("import { OnDestroy } from '@angular/core';")
            add_line("ngOnDestroy(): void {")
            indent += 1
            continue

        if line.startswith("al cambiar") or line.startswith("ngOnChanges"):
            add_import("import { OnChanges, SimpleChanges } from '@angular/core';")
            add_line("ngOnChanges(changes: SimpleChanges): void {")
            indent += 1
            continue

        if line == "fin ciclo":
            indent -= 1
            add_line("}")
            continue

        # Inyección de dependencias
        if line.startswith("inyectar"):
            service_name = line.split()[1] if len(line.split()) > 1 else "MiServicio"
            service_type = line.split()[2] if len(line.split()) > 2 else service_name
            add_line(f"constructor(private {service_name}: {service_type}) {{}}")
            continue

        # HTTP Client
        if line.startswith("http get"):
            url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
            add_import("import { HttpClient } from '@angular/common/http';")
            add_line(f"return this.http.get({url});")
            continue

        if line.startswith("http post"):
            url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
            data = line.split()[3] if len(line.split()) > 3 else "data"
            add_import("import { HttpClient } from '@angular/common/http';")
            add_line(f"return this.http.post({url}, {data});")
            continue

        if line.startswith("http put"):
            url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
            data = line.split()[3] if len(line.split()) > 3 else "data"
            add_import("import { HttpClient } from '@angular/common/http';")
            add_line(f"return this.http.put({url}, {data});")
            continue

        if line.startswith("http delete"):
            url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
            add_import("import { HttpClient } from '@angular/common/http';")
            add_line(f"return this.http.delete({url});")
            continue

        # Observables y RxJS
        if line.startswith("observable"):
            obs_name = line.split()[1] if len(line.split()) > 1 else "miObservable"
            add_import("import { Observable } from 'rxjs';")
            add_line(f"{obs_name}: Observable<any>;")
            continue

        if line.startswith("suscribir"):
            observable = line.split()[1] if len(line.split()) > 1 else "observable"
            add_line(f"{observable}.subscribe({{")
            add_line("  next: (data) => {")
            indent += 2
            continue

        if line == "fin suscripcion":
            indent -= 2
            add_line("  },")
            add_line("  error: (error) => console.error(error)")
            add_line("});")
            continue

        # Formularios reactivos
        if line.startswith("formulario reactivo"):
            form_name = line.split()[2] if len(line.split()) > 2 else "miFormulario"
            add_import("import { FormBuilder, FormGroup, Validators } from '@angular/forms';")
            add_line(f"{form_name}: FormGroup;")
            continue

        if line.startswith("crear formulario"):
            form_name = line.split()[2] if len(line.split()) > 2 else "miFormulario"
            add_line(f"this.{form_name} = this.fb.group({{")
            indent += 1
            continue

        if line == "fin formulario":
            indent -= 1
            add_line("});")
            continue

        if line.startswith("campo"):
            field_name = line.split()[1] if len(line.split()) > 1 else "campo"
            validators = "[]"
            initial_value = "''"
            
            if "requerido" in line:
                validators = "[Validators.required]"
            if "email" in line:
                validators = "[Validators.required, Validators.email]"
            if "=" in line:
                initial_value = line.split("=")[1].strip()
            
            add_line(f"{field_name}: [{initial_value}, {validators}],")
            continue

        # Validación
        if line.startswith("validar"):
            field_name = line.split()[1] if len(line.split()) > 1 else "campo"
            add_line(f"get {field_name}() {{ return this.miFormulario.get('{field_name}'); }}")
            continue

        # Routing
        if line.startswith("navegar a"):
            route = line.split()[2] if len(line.split()) > 2 else "'/'"
            add_import("import { Router } from '@angular/router';")
            add_line(f"this.router.navigate([{route}]);")
            continue

        if line.startswith("ruta"):
            path = line.split()[1] if len(line.split()) > 1 else "''"
            component = line.split()[2] if len(line.split()) > 2 else "MiComponente"
            add_line(f"{{ path: {path}, component: {component} }},")
            continue

        # Pipes
        if line.startswith("pipe"):
            pipe_name = line.split()[1] if len(line.split()) > 1 else "MiPipe"
            add_line("@Pipe({")
            add_line(f"  name: '{pipe_name.lower()}'")
            add_line("})")
            add_line(f"export class {pipe_name} implements PipeTransform {{")
            add_line("  transform(value: any, ...args: any[]): any {")
            indent += 2
            continue

        if line == "fin pipe":
            add_line("return value;")
            indent -= 2
            add_line("  }")
            add_line("}")
            continue

        # Directivas
        if line.startswith("directiva"):
            directive_name = line.split()[1] if len(line.split()) > 1 else "MiDirectiva"
            selector = directive_name.lower().replace("directiva", "")
            
            add_line("@Directive({")
            add_line(f"  selector: '[{selector}]'")
            add_line("})")
            add_line(f"export class {directive_name} {{")
            indent += 1
            continue

        if line == "fin directiva":
            indent -= 1
            add_line("}")
            continue

        # Guards
        if line.startswith("guard"):
            guard_name = line.split()[1] if len(line.split()) > 1 else "MiGuard"
            add_import("import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';")
            add_line("@Injectable({")
            add_line("  providedIn: 'root'")
            add_line("})")
            add_line(f"export class {guard_name} implements CanActivate {{")
            add_line("  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {")
            indent += 2
            continue

        if line == "fin guard":
            add_line("return true;")
            indent -= 2
            add_line("  }")
            add_line("}")
            continue

        # Interceptors
        if line.startswith("interceptor"):
            interceptor_name = line.split()[1] if len(line.split()) > 1 else "MiInterceptor"
            add_import("import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';")
            add_line("@Injectable()")
            add_line(f"export class {interceptor_name} implements HttpInterceptor {{")
            add_line("  intercept(req: HttpRequest<any>, next: HttpHandler) {")
            indent += 2
            continue

        if line == "fin interceptor":
            add_line("return next.handle(req);")
            indent -= 2
            add_line("  }")
            add_line("}")
            continue

        # Métodos/funciones
        if line.startswith("metodo") or line.startswith("funcion"):
            parts = line.split()
            if len(parts) >= 2:
                method_name = parts[1]
                return_type = "void"
                
                if ":" in line:
                    return_type = line.split(":")[1].split("(")[0].strip()
                
                if "(" in line and ")" in line:
                    params_part = line.split("(")[1].split(")")[0].strip()
                    add_line(f"{method_name}({params_part}): {return_type} {{")
                else:
                    add_line(f"{method_name}(): {return_type} {{")
                indent += 1
            continue

        if line == "fin metodo" or line == "fin funcion":
            indent -= 1
            add_line("}")
            continue

        # Propiedades de clase
        if line.startswith("propiedad"):
            parts = line.split()
            if len(parts) >= 2:
                prop_name = parts[1]
                prop_type = "any"
                initial_value = ""
                
                if ":" in line:
                    type_part = line.split(":")[1].strip()
                    if "=" in type_part:
                        prop_type = type_part.split("=")[0].strip()
                        initial_value = " = " + type_part.split("=")[1].strip()
                    else:
                        prop_type = type_part
                elif "=" in line:
                    initial_value = " = " + line.split("=")[1].strip()
                
                add_line(f"{prop_name}: {prop_type}{initial_value};")
            continue

        # Asignaciones y expresiones TypeScript normales
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
    
    # Imports básicos de Angular
    if decorators_used:
        core_imports = []
        if "Component" in decorators_used:
            core_imports.append("Component")
        if "Injectable" in decorators_used:
            core_imports.append("Injectable")
        if "NgModule" in decorators_used:
            core_imports.append("NgModule")
        if "Input" in decorators_used:
            core_imports.append("Input")
        if "Output" in decorators_used:
            core_imports.append("Output")
        
        if core_imports:
            import_lines.append(f"import {{ {', '.join(core_imports)} }} from '@angular/core';")
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(sorted(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    else:
        result_lines = output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_angular(codigo)

# Funciones auxiliares para el transpilador de Angular
def get_angular_keywords():
    """Retorna las palabras clave de Vader que se mapean a Angular"""
    return {
        'componente angular': 'Angular component',
        'servicio': 'Angular service',
        'modulo': 'Angular module',
        'entrada': '@Input decorator',
        'salida': '@Output decorator',
        'emitir': 'EventEmitter.emit',
        'al inicializar': 'ngOnInit',
        'al destruir': 'ngOnDestroy',
        'al cambiar': 'ngOnChanges',
        'inyectar': 'dependency injection',
        'http get': 'HttpClient.get',
        'http post': 'HttpClient.post',
        'http put': 'HttpClient.put',
        'http delete': 'HttpClient.delete',
        'observable': 'Observable',
        'suscribir': 'subscribe',
        'formulario reactivo': 'reactive form',
        'crear formulario': 'FormBuilder.group',
        'campo': 'form field',
        'validar': 'form validation',
        'navegar a': 'router.navigate',
        'ruta': 'route definition',
        'pipe': 'Angular pipe',
        'directiva': 'Angular directive',
        'guard': 'route guard',
        'interceptor': 'HTTP interceptor',
        'metodo': 'class method',
        'propiedad': 'class property'
    }
