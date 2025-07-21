def transpile_to_django(code):
    """Transpila código Vader a Django con Python"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_app = False
    in_model = False
    in_view = False
    in_form = False
    app_name = "MiApp"
    imports = set()
    models = []
    views = []
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de Django
    add_import("from django.db import models")
    add_import("from django.shortcuts import render, get_object_or_404, redirect")
    add_import("from django.http import JsonResponse, HttpResponse")
    add_import("from django.views.decorators.csrf import csrf_exempt")
    add_import("from django.contrib.auth.decorators import login_required")
    add_import("from django.contrib import messages")
    add_import("from django.forms import ModelForm")
    add_import("from django.urls import path")
    add_import("import json")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Aplicación Django
        if line.startswith("app django"):
            parts = line.split()
            app_name = parts[2] if len(parts) > 2 else "MiApp"
            add_line(f"# Django App: {app_name}")
            add_line("")
            in_app = True
            continue

        if line == "fin app":
            in_app = False
            # Agregar URLs al final
            add_line("")
            add_line("# URLs")
            add_line("urlpatterns = [")
            for view in views:
                view_name = view.lower()
                add_line(f"    path('{view_name}/', {view}, name='{view_name}'),")
            add_line("]")
            continue

        # Modelos Django
        if line.startswith("modelo"):
            model_name = line.split()[1] if len(line.split()) > 1 else "MiModelo"
            models.append(model_name)
            add_line(f"class {model_name}(models.Model):")
            in_model = True
            indent += 1
            continue

        if line == "fin modelo":
            add_line("")
            add_line("def __str__(self):")
            add_line("    return f'{self.__class__.__name__} {self.pk}'")
            add_line("")
            add_line("class Meta:")
            add_line("    verbose_name_plural = f'{self.__class__.__name__}s'")
            add_line("")
            in_model = False
            indent -= 1
            continue

        # Campos del modelo
        if in_model and line.startswith("campo"):
            parts = line.split(":")
            if len(parts) == 2:
                field_name = parts[0].replace("campo", "").strip()
                field_type = parts[1].strip()
                
                # Mapear tipos de Vader a Django
                type_mapping = {
                    "string": "models.CharField(max_length=200)",
                    "texto": "models.TextField()",
                    "numero": "models.IntegerField()",
                    "decimal": "models.DecimalField(max_digits=10, decimal_places=2)",
                    "booleano": "models.BooleanField(default=False)",
                    "fecha": "models.DateField()",
                    "fecha_hora": "models.DateTimeField(auto_now_add=True)",
                    "email": "models.EmailField()",
                    "url": "models.URLField()",
                    "imagen": "models.ImageField(upload_to='images/')",
                    "archivo": "models.FileField(upload_to='files/')",
                    "opcional": "models.CharField(max_length=200, blank=True, null=True)"
                }
                
                django_field = type_mapping.get(field_type, f"models.CharField(max_length=200)")
                add_line(f"{field_name} = {django_field}")
            continue

        # Relaciones
        if in_model and line.startswith("relacion"):
            parts = line.split()
            if len(parts) >= 3:
                relation_type = parts[1]  # uno_a_muchos, muchos_a_muchos, etc.
                related_model = parts[2]
                field_name = parts[3] if len(parts) > 3 else related_model.lower()
                
                if relation_type == "uno_a_muchos":
                    add_line(f"{field_name} = models.ForeignKey({related_model}, on_delete=models.CASCADE)")
                elif relation_type == "muchos_a_muchos":
                    add_line(f"{field_name} = models.ManyToManyField({related_model})")
                elif relation_type == "uno_a_uno":
                    add_line(f"{field_name} = models.OneToOneField({related_model}, on_delete=models.CASCADE)")
            continue

        # Vistas Django
        if line.startswith("vista"):
            view_name = line.split()[1] if len(line.split()) > 1 else "mi_vista"
            views.append(view_name)
            add_line(f"def {view_name}(request):")
            in_view = True
            indent += 1
            continue

        if line == "fin vista":
            add_line("")
            in_view = False
            indent -= 1
            continue

        # Vista basada en clase
        if line.startswith("vista clase"):
            class_name = line.split()[2] if len(line.split()) > 2 else "MiVista"
            base_class = line.split()[3] if len(line.split()) > 3 else "View"
            
            class_mapping = {
                "lista": "ListView",
                "detalle": "DetailView",
                "crear": "CreateView",
                "actualizar": "UpdateView",
                "eliminar": "DeleteView"
            }
            
            django_base = class_mapping.get(base_class, "View")
            add_import(f"from django.views.generic import {django_base}")
            
            add_line(f"class {class_name}({django_base}):")
            in_view = True
            indent += 1
            continue

        # Respuestas
        if line.startswith("respuesta json"):
            data = line.replace("respuesta json", "").strip()
            add_line(f"return JsonResponse({data})")
            continue

        if line.startswith("respuesta plantilla"):
            template = line.replace("respuesta plantilla", "").strip()
            if "con" in template:
                parts = template.split("con")
                template_name = parts[0].strip().replace('"', '').replace("'", '')
                context = parts[1].strip()
                add_line(f"return render(request, '{template_name}', {context})")
            else:
                template_name = template.replace('"', '').replace("'", '')
                add_line(f"return render(request, '{template_name}')")
            continue

        if line.startswith("redirigir a"):
            url = line.replace("redirigir a", "").strip().replace('"', '').replace("'", '')
            add_line(f"return redirect('{url}')")
            continue

        # Formularios Django
        if line.startswith("formulario"):
            form_name = line.split()[1] if len(line.split()) > 1 else "MiFormulario"
            model_name = line.split()[2] if len(line.split()) > 2 else "MiModelo"
            add_line(f"class {form_name}(ModelForm):")
            add_line("    class Meta:")
            add_line(f"        model = {model_name}")
            add_line("        fields = '__all__'")
            add_line("")
            continue

        # Autenticación
        if line.startswith("requiere login"):
            add_line("@login_required")
            continue

        if line.startswith("sin csrf"):
            add_line("@csrf_exempt")
            continue

        # Consultas a la base de datos
        if line.startswith("obtener todos"):
            model = line.split()[-1] if len(line.split()) > 2 else "MiModelo"
            add_line(f"objects = {model}.objects.all()")
            continue

        if line.startswith("obtener por id"):
            parts = line.split()
            model = parts[-1] if len(parts) > 3 else "MiModelo"
            id_var = parts[3] if len(parts) > 3 else "id"
            add_line(f"obj = get_object_or_404({model}, pk={id_var})")
            continue

        if line.startswith("filtrar"):
            parts = line.split("por")
            model = parts[0].replace("filtrar", "").strip()
            filter_condition = parts[1].strip() if len(parts) > 1 else "pk=1"
            add_line(f"objects = {model}.objects.filter({filter_condition})")
            continue

        # Crear objeto
        if line.startswith("crear"):
            model = line.split()[1] if len(line.split()) > 1 else "MiModelo"
            add_line(f"obj = {model}.objects.create(**data)")
            continue

        # Actualizar objeto
        if line.startswith("actualizar"):
            add_line("obj.save()")
            continue

        # Eliminar objeto
        if line.startswith("eliminar"):
            add_line("obj.delete()")
            continue

        # Mensajes
        if line.startswith("mensaje exito"):
            message = line.replace("mensaje exito", "").strip().replace('"', '')
            add_line(f"messages.success(request, '{message}')")
            continue

        if line.startswith("mensaje error"):
            message = line.replace("mensaje error", "").strip().replace('"', '')
            add_line(f"messages.error(request, '{message}')")
            continue

        # Paginación
        if line.startswith("paginar"):
            per_page = line.split()[-1] if len(line.split()) > 1 else "10"
            add_import("from django.core.paginator import Paginator")
            add_line(f"paginator = Paginator(objects, {per_page})")
            add_line("page_number = request.GET.get('page')")
            add_line("page_obj = paginator.get_page(page_number)")
            continue

        # Validaciones
        if line.startswith("validar"):
            field = line.split()[1] if len(line.split()) > 1 else "field"
            add_line(f"if not request.POST.get('{field}'):")
            add_line(f"    messages.error(request, '{field} es requerido')")
            add_line(f"    return redirect(request.path)")
            continue

        # Archivos subidos
        if line.startswith("archivo subido"):
            file_name = line.split()[-1] if len(line.split()) > 2 else "file"
            add_line(f"{file_name} = request.FILES.get('{file_name}')")
            continue

        # Métodos HTTP
        if line.startswith("si metodo POST"):
            add_line("if request.method == 'POST':")
            indent += 1
            continue

        if line.startswith("si metodo GET"):
            add_line("if request.method == 'GET':")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            continue

        # Otras líneas (comentarios o código Python)
        if in_view or in_model:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"print({message})")
            elif "=" in line:
                add_line(f"{line}")
            else:
                add_line(f"# {line}")

    # Agregar imports al inicio
    import_lines = []
    if imports:
        import_lines.extend(sorted(imports))
        import_lines.append("")
    
    result_lines = import_lines + output
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_django(codigo)

# Funciones auxiliares para el transpilador de Django
def get_django_keywords():
    """Retorna las palabras clave de Vader que se mapean a Django"""
    return {
        'app django': 'Django application',
        'modelo': 'Django model',
        'campo': 'model field',
        'relacion': 'model relationship',
        'vista': 'Django view',
        'vista clase': 'class-based view',
        'formulario': 'Django form',
        'respuesta json': 'JSON response',
        'respuesta plantilla': 'template response',
        'redirigir a': 'redirect',
        'requiere login': 'login required',
        'sin csrf': 'CSRF exempt',
        'obtener todos': 'get all objects',
        'obtener por id': 'get by ID',
        'filtrar': 'filter objects',
        'crear': 'create object',
        'actualizar': 'update object',
        'eliminar': 'delete object',
        'mensaje exito': 'success message',
        'mensaje error': 'error message',
        'paginar': 'pagination',
        'validar': 'validation',
        'archivo subido': 'uploaded file',
        'si metodo POST': 'if POST method',
        'si metodo GET': 'if GET method'
    }
