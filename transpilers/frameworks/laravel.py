def transpile_to_laravel(code):
    """Transpila código Vader a Laravel con PHP"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_app = False
    in_model = False
    in_controller = False
    in_route = False
    in_migration = False
    app_name = "MiApp"
    imports = set()
    models = []
    controllers = []
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 4
        output.append(" " * current_indent + text)
    
    # Agregar encabezado PHP
    output.append("<?php")
    output.append("")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Aplicación Laravel
        if line.startswith("app laravel"):
            parts = line.split()
            app_name = parts[2] if len(parts) > 2 else "MiApp"
            add_line(f"// Laravel App: {app_name}")
            add_line("")
            in_app = True
            continue

        if line == "fin app":
            in_app = False
            continue

        # Modelos Eloquent
        if line.startswith("modelo"):
            model_name = line.split()[1] if len(line.split()) > 1 else "MiModelo"
            models.append(model_name)
            add_line("use Illuminate\\Database\\Eloquent\\Model;")
            add_line("use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;")
            add_line("")
            add_line(f"class {model_name} extends Model")
            add_line("{")
            add_line("    use HasFactory;")
            add_line("")
            add_line("    protected $fillable = [")
            in_model = True
            indent += 1
            continue

        if line == "fin modelo":
            add_line("    ];")
            add_line("")
            add_line("    protected $casts = [")
            add_line("        'created_at' => 'datetime',")
            add_line("        'updated_at' => 'datetime',")
            add_line("    ];")
            add_line("}")
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
                add_line(f"        '{attr_name}',")
            continue

        # Relaciones Eloquent
        if in_model and line.startswith("relacion"):
            parts = line.split()
            if len(parts) >= 3:
                relation_type = parts[1]
                related_model = parts[2]
                method_name = parts[3] if len(parts) > 3 else related_model.lower()
                
                if relation_type == "uno_a_muchos":
                    add_line(f"    public function {method_name}()")
                    add_line("    {")
                    add_line(f"        return $this->hasMany({related_model}::class);")
                    add_line("    }")
                elif relation_type == "pertenece_a":
                    add_line(f"    public function {method_name}()")
                    add_line("    {")
                    add_line(f"        return $this->belongsTo({related_model}::class);")
                    add_line("    }")
                elif relation_type == "muchos_a_muchos":
                    add_line(f"    public function {method_name}()")
                    add_line("    {")
                    add_line(f"        return $this->belongsToMany({related_model}::class);")
                    add_line("    }")
            continue

        # Controladores
        if line.startswith("controlador"):
            controller_name = line.split()[1] if len(line.split()) > 1 else "MiControlador"
            controllers.append(controller_name)
            add_line("use App\\Http\\Controllers\\Controller;")
            add_line("use Illuminate\\Http\\Request;")
            add_line("use Illuminate\\Http\\JsonResponse;")
            add_line("use Illuminate\\View\\View;")
            add_line("")
            add_line(f"class {controller_name} extends Controller")
            add_line("{")
            in_controller = True
            indent += 1
            continue

        if line == "fin controlador":
            add_line("}")
            add_line("")
            in_controller = False
            indent -= 1
            continue

        # Métodos del controlador
        if in_controller and line.startswith("metodo"):
            method_name = line.split()[1] if len(line.split()) > 1 else "index"
            add_line(f"    public function {method_name}(Request $request)")
            add_line("    {")
            indent += 1
            continue

        if line == "fin metodo":
            add_line("    }")
            add_line("")
            indent -= 1
            continue

        # Rutas
        if line.startswith("ruta GET"):
            path = line.split("GET")[1].strip() if "GET" in line else "/"
            add_line("use Illuminate\\Support\\Facades\\Route;")
            add_line("")
            add_line(f"Route::get('{path}', function (Request $request) {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta POST"):
            path = line.split("POST")[1].strip() if "POST" in line else "/"
            add_line(f"Route::post('{path}', function (Request $request) {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta PUT"):
            path = line.split("PUT")[1].strip() if "PUT" in line else "/"
            add_line(f"Route::put('{path}', function (Request $request) {{")
            in_route = True
            indent += 1
            continue

        if line.startswith("ruta DELETE"):
            path = line.split("DELETE")[1].strip() if "DELETE" in line else "/"
            add_line(f"Route::delete('{path}', function (Request $request) {{")
            in_route = True
            indent += 1
            continue

        if line == "fin ruta":
            add_line("});")
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
                add_line(f"    return response()->json({data}, {status_code});")
            else:
                add_line(f"    return response()->json({data});")
            continue

        if line.startswith("respuesta vista"):
            view = line.replace("respuesta vista", "").strip()
            if "con" in view:
                parts = view.split("con")
                view_name = parts[0].strip().replace('"', '').replace("'", '')
                data = parts[1].strip()
                add_line(f"    return view('{view_name}', {data});")
            else:
                view_name = view.replace('"', '').replace("'", '')
                add_line(f"    return view('{view_name}');")
            continue

        if line.startswith("redirigir a"):
            route = line.replace("redirigir a", "").strip().replace('"', '').replace("'", '')
            add_line(f"    return redirect()->route('{route}');")
            continue

        # Validaciones
        if line.startswith("validar"):
            rules = line.replace("validar", "").strip()
            add_line("    $validated = $request->validate([")
            # Parsear reglas de validación simples
            if ":" in rules:
                field_rules = rules.split(",")
                for rule in field_rules:
                    if ":" in rule:
                        field, validation = rule.split(":", 1)
                        field = field.strip()
                        validation = validation.strip()
                        add_line(f"        '{field}' => '{validation}',")
            add_line("    ]);")
            continue

        # Consultas Eloquent
        if line.startswith("obtener todos"):
            model = line.split()[-1] if len(line.split()) > 2 else "Model"
            add_line(f"    ${model.lower()}s = {model}::all();")
            continue

        if line.startswith("obtener por id"):
            parts = line.split()
            model = parts[-1] if len(parts) > 3 else "Model"
            id_var = parts[3] if len(parts) > 3 else "$id"
            add_line(f"    ${model.lower()} = {model}::findOrFail({id_var});")
            continue

        if line.startswith("crear"):
            model = line.split()[1] if len(line.split()) > 1 else "Model"
            add_line(f"    ${model.lower()} = {model}::create($validated);")
            continue

        if line.startswith("actualizar"):
            model = line.split()[1] if len(line.split()) > 1 else "model"
            add_line(f"    ${model}->update($validated);")
            continue

        if line.startswith("eliminar"):
            model = line.split()[1] if len(line.split()) > 1 else "model"
            add_line(f"    ${model}->delete();")
            continue

        # Middleware
        if line.startswith("middleware"):
            middleware_name = line.split()[1] if len(line.split()) > 1 else "auth"
            add_line(f"Route::middleware('{middleware_name}')->group(function () {{")
            indent += 1
            continue

        if line == "fin middleware":
            add_line("});")
            indent -= 1
            continue

        # Autenticación
        if line.startswith("requiere auth"):
            add_line("    $this->middleware('auth');")
            continue

        # Sesiones
        if line.startswith("guardar sesion"):
            parts = line.split("=")
            if len(parts) == 2:
                key = parts[0].replace("guardar sesion", "").strip()
                value = parts[1].strip()
                add_line(f"    session(['{key}' => {value}]);")
            continue

        if line.startswith("obtener sesion"):
            key = line.replace("obtener sesion", "").strip()
            add_line(f"    session('{key}')")
            continue

        # Base de datos
        if line.startswith("migracion"):
            table_name = line.split()[1] if len(line.split()) > 1 else "mi_tabla"
            add_line("use Illuminate\\Database\\Migrations\\Migration;")
            add_line("use Illuminate\\Database\\Schema\\Blueprint;")
            add_line("use Illuminate\\Support\\Facades\\Schema;")
            add_line("")
            add_line("class CreateTableMigration extends Migration")
            add_line("{")
            add_line("    public function up()")
            add_line("    {")
            add_line(f"        Schema::create('{table_name}', function (Blueprint $table) {{")
            add_line("            $table->id();")
            in_migration = True
            indent += 3
            continue

        if line == "fin migracion":
            add_line("            $table->timestamps();")
            add_line("        });")
            add_line("    }")
            add_line("")
            add_line("    public function down()")
            add_line("    {")
            add_line(f"        Schema::dropIfExists('{table_name}');")
            add_line("    }")
            add_line("}")
            in_migration = False
            indent -= 3
            continue

        # Campos de migración
        if in_migration and line.startswith("campo"):
            parts = line.split(":")
            if len(parts) == 2:
                field_name = parts[0].replace("campo", "").strip()
                field_type = parts[1].strip()
                
                type_mapping = {
                    "string": f"$table->string('{field_name}');",
                    "texto": f"$table->text('{field_name}');",
                    "numero": f"$table->integer('{field_name}');",
                    "decimal": f"$table->decimal('{field_name}', 8, 2);",
                    "booleano": f"$table->boolean('{field_name}')->default(false);",
                    "fecha": f"$table->date('{field_name}');",
                    "fecha_hora": f"$table->timestamp('{field_name}');",
                    "email": f"$table->string('{field_name}')->unique();",
                    "opcional": f"$table->string('{field_name}')->nullable();"
                }
                
                laravel_field = type_mapping.get(field_type, f"$table->string('{field_name}');")
                add_line(f"            {laravel_field}")
            continue

        # Otras líneas (comentarios o código PHP)
        if in_controller or in_route or in_model:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"    Log::info({message});")
            elif "=" in line and not line.startswith("//"):
                # Convertir variables de Vader a PHP
                php_line = line.replace(" = ", " = $").replace("variable ", "$")
                if not php_line.startswith("$"):
                    php_line = "    $" + php_line
                add_line(php_line)
            else:
                add_line(f"    // {line}")

    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_laravel(codigo)

# Funciones auxiliares para el transpilador de Laravel
def get_laravel_keywords():
    """Retorna las palabras clave de Vader que se mapean a Laravel"""
    return {
        'app laravel': 'Laravel application',
        'modelo': 'Eloquent model',
        'atributo': 'model attribute',
        'relacion': 'Eloquent relationship',
        'controlador': 'Laravel controller',
        'metodo': 'controller method',
        'ruta GET': 'GET route',
        'ruta POST': 'POST route',
        'ruta PUT': 'PUT route',
        'ruta DELETE': 'DELETE route',
        'respuesta json': 'JSON response',
        'respuesta vista': 'view response',
        'redirigir a': 'redirect',
        'validar': 'validation',
        'obtener todos': 'get all records',
        'obtener por id': 'get by ID',
        'crear': 'create record',
        'actualizar': 'update record',
        'eliminar': 'delete record',
        'middleware': 'middleware',
        'requiere auth': 'require authentication',
        'guardar sesion': 'save session',
        'obtener sesion': 'get session',
        'migracion': 'database migration',
        'campo': 'migration field'
    }
