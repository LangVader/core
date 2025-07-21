def transpile_to_flutter_web(code):
    """Transpila código Vader a Flutter Web con Dart"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_app = False
    in_widget = False
    in_state = False
    widget_name = "MiWidget"
    imports = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de Flutter
    add_import("import 'package:flutter/material.dart'")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Aplicación Flutter Web
        if line.startswith("app flutter"):
            app_name = line.split()[2] if len(line.split()) > 2 else "MiApp"
            add_line("")
            add_line("void main() {")
            add_line(f"  runApp({app_name}());")
            add_line("}")
            add_line("")
            add_line(f"class {app_name} extends StatelessWidget {{")
            add_line("  @override")
            add_line("  Widget build(BuildContext context) {")
            add_line("    return MaterialApp(")
            add_line(f"      title: '{app_name}',")
            add_line("      theme: ThemeData(")
            add_line("        primarySwatch: Colors.blue,")
            add_line("      ),")
            add_line("      home: HomePage(),")
            add_line("    );")
            add_line("  }")
            add_line("}")
            add_line("")
            in_app = True
            continue

        if line == "fin app":
            in_app = False
            continue

        # Widget sin estado
        if line.startswith("widget"):
            widget_name = line.split()[1] if len(line.split()) > 1 else "MiWidget"
            add_line(f"class {widget_name} extends StatelessWidget {{")
            add_line("  @override")
            add_line("  Widget build(BuildContext context) {")
            in_widget = True
            indent += 2
            continue

        # Widget con estado
        if line.startswith("widget estado"):
            widget_name = line.split()[2] if len(line.split()) > 2 else "MiWidget"
            add_line(f"class {widget_name} extends StatefulWidget {{")
            add_line("  @override")
            add_line(f"  _{widget_name}State createState() => _{widget_name}State();")
            add_line("}")
            add_line("")
            add_line(f"class _{widget_name}State extends State<{widget_name}> {{")
            in_state = True
            indent += 1
            continue

        if line == "fin widget":
            if in_state:
                add_line("}")
                in_state = False
            else:
                add_line("  }")
                add_line("}")
            in_widget = False
            indent = 0
            add_line("")
            continue

        # Variables de estado
        if line.startswith("estado"):
            parts = line.split("=")
            if len(parts) == 2:
                var_name = parts[0].replace("estado", "").strip()
                initial_value = parts[1].strip()
                
                # Determinar tipo basado en el valor
                dart_type = "String"
                if initial_value.isdigit():
                    dart_type = "int"
                elif initial_value.replace(".", "").isdigit():
                    dart_type = "double"
                elif initial_value.lower() in ["true", "false"]:
                    dart_type = "bool"
                elif initial_value.startswith("["):
                    dart_type = "List<dynamic>"
                
                add_line(f"{dart_type} {var_name} = {initial_value};")
            continue

        # Establecer estado
        if line.startswith("establecer"):
            parts = line.split("=")
            if len(parts) == 2:
                var_name = parts[0].replace("establecer", "").strip()
                value = parts[1].strip()
                add_line("setState(() {")
                add_line(f"  {var_name} = {value};")
                add_line("});")
            continue

        # Funciones
        if line.startswith("funcion"):
            func_name = line.split()[1] if len(line.split()) > 1 else "miFuncion"
            params = ""
            if "(" in line and ")" in line:
                params = line[line.find("("):line.find(")")+1]
            add_line(f"void {func_name}{params} {{")
            indent += 1
            continue

        if line == "fin funcion":
            add_line("}")
            indent -= 1
            continue

        # Construir widget
        if line.startswith("construir") or line.startswith("build"):
            if not in_widget:
                add_line("@override")
                add_line("Widget build(BuildContext context) {")
                indent += 1
            add_line("return ")
            continue

        # Widgets de Flutter
        if line.startswith("scaffold"):
            add_line("Scaffold(")
            indent += 1
            continue

        if line == "fin scaffold":
            indent -= 1
            add_line("),")
            continue

        if line.startswith("app bar"):
            title = line.replace("app bar", "").strip().replace('"', '')
            add_line("appBar: AppBar(")
            add_line(f"  title: Text('{title}'),")
            add_line("),")
            continue

        if line.startswith("cuerpo"):
            add_line("body: ")
            continue

        if line.startswith("columna"):
            add_line("Column(")
            add_line("  children: [")
            indent += 2
            continue

        if line == "fin columna":
            indent -= 2
            add_line("  ],")
            add_line("),")
            continue

        if line.startswith("fila"):
            add_line("Row(")
            add_line("  children: [")
            indent += 2
            continue

        if line == "fin fila":
            indent -= 2
            add_line("  ],")
            add_line("),")
            continue

        if line.startswith("contenedor"):
            add_line("Container(")
            indent += 1
            continue

        if line == "fin contenedor":
            indent -= 1
            add_line("),")
            continue

        if line.startswith("texto"):
            content = line.replace("texto", "").strip().replace('"', '')
            if "{" in content:
                # Variable interpolation
                content = content.replace("{", "${")
                add_line(f"Text('{content}'),")
            else:
                add_line(f"Text('{content}'),")
            continue

        if line.startswith("boton elevado"):
            text = line.replace("boton elevado", "").strip().replace('"', '')
            add_line("ElevatedButton(")
            add_line(f"  child: Text('{text}'),")
            add_line("  onPressed: () {")
            indent += 2
            continue

        if line == "fin boton":
            indent -= 2
            add_line("  },")
            add_line("),")
            continue

        if line.startswith("boton texto"):
            text = line.replace("boton texto", "").strip().replace('"', '')
            add_line("TextButton(")
            add_line(f"  child: Text('{text}'),")
            add_line("  onPressed: () {")
            indent += 2
            continue

        if line.startswith("campo texto"):
            placeholder = ""
            if "placeholder=" in line:
                placeholder_text = line.split("placeholder=")[1].strip().replace('"', '')
                placeholder = f"  decoration: InputDecoration(hintText: '{placeholder_text}'),"
            
            add_line("TextField(")
            if placeholder:
                add_line(placeholder)
            add_line("),")
            continue

        if line.startswith("imagen"):
            src = line.replace("imagen", "").strip().replace('"', '')
            if src.startswith("http"):
                add_line(f"Image.network('{src}'),")
            else:
                add_line(f"Image.asset('{src}'),")
            continue

        if line.startswith("icono"):
            icon_name = line.replace("icono", "").strip()
            add_line(f"Icon(Icons.{icon_name}),")
            continue

        # Navegación
        if line.startswith("navegar a"):
            page_name = line.replace("navegar a", "").strip()
            add_line("Navigator.push(")
            add_line("  context,")
            add_line("  MaterialPageRoute(")
            add_line(f"    builder: (context) => {page_name}(),")
            add_line("  ),")
            add_line(");")
            continue

        if line.startswith("volver"):
            add_line("Navigator.pop(context);")
            continue

        # Padding y margen
        if line.startswith("padding"):
            value = line.split("=")[1].strip() if "=" in line else "16.0"
            add_line(f"padding: EdgeInsets.all({value}),")
            continue

        if line.startswith("margen"):
            value = line.split("=")[1].strip() if "=" in line else "16.0"
            add_line(f"margin: EdgeInsets.all({value}),")
            continue

        # Colores
        if line.startswith("color"):
            color = line.split("=")[1].strip() if "=" in line else "Colors.blue"
            add_line(f"color: {color},")
            continue

        # Alineación
        if line.startswith("centrar"):
            add_line("Center(")
            add_line("  child: ")
            indent += 1
            continue

        if line == "fin centrar":
            indent -= 1
            add_line("),")
            continue

        # Listas
        if line.startswith("lista"):
            add_line("ListView(")
            add_line("  children: [")
            indent += 2
            continue

        if line == "fin lista":
            indent -= 2
            add_line("  ],")
            add_line("),")
            continue

        if line.startswith("lista builder"):
            add_line("ListView.builder(")
            add_line("  itemBuilder: (context, index) {")
            add_line("    return ")
            indent += 2
            continue

        if line == "fin lista builder":
            indent -= 2
            add_line("  },")
            add_line("),")
            continue

        # Condicionales
        if line.startswith("si"):
            condition = line.replace("si", "").strip()
            add_line(f"if ({condition})")
            continue

        # Otras líneas (comentarios o código Dart)
        if in_widget or in_state:
            if "=" in line and not line.startswith("//"):
                add_line(f"{line};")
            else:
                add_line(f"// {line}")

    # Agregar imports al inicio
    import_lines = []
    if imports:
        import_lines.extend(sorted(imports))
        import_lines.append("")
    
    result_lines = import_lines + output
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_flutter_web(codigo)

# Funciones auxiliares para el transpilador de Flutter Web
def get_flutter_web_keywords():
    """Retorna las palabras clave de Vader que se mapean a Flutter Web"""
    return {
        'app flutter': 'Flutter web application',
        'widget': 'StatelessWidget',
        'widget estado': 'StatefulWidget',
        'estado': 'state variable',
        'establecer': 'setState',
        'funcion': 'function',
        'construir': 'build method',
        'scaffold': 'Scaffold widget',
        'app bar': 'AppBar widget',
        'cuerpo': 'body property',
        'columna': 'Column widget',
        'fila': 'Row widget',
        'contenedor': 'Container widget',
        'texto': 'Text widget',
        'boton elevado': 'ElevatedButton',
        'boton texto': 'TextButton',
        'campo texto': 'TextField',
        'imagen': 'Image widget',
        'icono': 'Icon widget',
        'navegar a': 'Navigator.push',
        'volver': 'Navigator.pop',
        'padding': 'padding property',
        'margen': 'margin property',
        'color': 'color property',
        'centrar': 'Center widget',
        'lista': 'ListView',
        'lista builder': 'ListView.builder'
    }
