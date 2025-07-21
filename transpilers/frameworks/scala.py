# Transpilador Scala para Vader
# Convierte sintaxis natural a Scala para programación funcional y big data

def transpile_scala(code):
    """Transpila código Vader a Scala"""
    lines = code.split('\n')
    result = []
    
    # Imports básicos de Scala
    result.extend([
        '// Aplicación Scala generada por Vader',
        'import scala.collection.mutable.ListBuffer',
        'import scala.util.{Try, Success, Failure}',
        'import scala.concurrent.Future',
        'import scala.concurrent.ExecutionContext.Implicits.global',
        '',
        'object VaderApp extends App {',
        ''
    ])
    
    in_class = False
    in_object = False
    class_name = "MiClase"
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('objeto scala'):
            # Objeto singleton
            if '"' in line:
                object_name = line.split('"')[1]
            else:
                object_name = "MiObjeto"
            in_object = True
            result.extend([
                f'object {object_name} {{',
                ''
            ])
            
        elif line.startswith('clase scala'):
            # Clase Scala
            if '"' in line:
                class_name = line.split('"')[1]
            in_class = True
            result.extend([
                f'class {class_name} {{',
                ''
            ])
            
        elif line.startswith('case class'):
            # Case class
            if '"' in line:
                case_class_name = line.split('"')[1]
                result.append(f'case class {case_class_name}()')
            
        elif line.startswith('funcion'):
            # Función
            func_parts = line.replace('funcion', '').strip().split('(')
            func_name = func_parts[0].strip()
            params = func_parts[1].replace(')', '').strip() if len(func_parts) > 1 else ''
            
            if params:
                scala_params = _convert_params_to_scala(params)
                result.append(f'  def {func_name}({scala_params}): Unit = {{')
            else:
                result.append(f'  def {func_name}(): Unit = {{')
                
        elif line.startswith('funcion pura'):
            # Función pura (inmutable)
            func_parts = line.replace('funcion pura', '').strip().split('(')
            func_name = func_parts[0].strip()
            params = func_parts[1].replace(')', '').strip() if len(func_parts) > 1 else ''
            
            if params:
                scala_params = _convert_params_to_scala(params)
                result.append(f'  def {func_name}({scala_params}): String = {{')
            else:
                result.append(f'  def {func_name}(): String = {{')
                
        elif line.startswith('lista inmutable'):
            # Lista inmutable
            var_name = line.replace('lista inmutable', '').strip()
            result.append(f'  val {var_name} = List.empty[String]')
            
        elif line.startswith('lista mutable'):
            # Lista mutable
            var_name = line.replace('lista mutable', '').strip()
            result.append(f'  val {var_name} = ListBuffer.empty[String]')
            
        elif line.startswith('mapa'):
            # Map/diccionario
            var_name = line.replace('mapa', '').strip()
            result.append(f'  val {var_name} = Map.empty[String, String]')
            
        elif line.startswith('filtrar'):
            # Operación filter
            parts = line.replace('filtrar', '').strip().split(' donde ')
            if len(parts) >= 2:
                collection = parts[0].strip()
                condition = parts[1].strip()
                result.append(f'  val filtrado = {collection}.filter({condition})')
                
        elif line.startswith('mapear'):
            # Operación map
            parts = line.replace('mapear', '').strip().split(' con ')
            if len(parts) >= 2:
                collection = parts[0].strip()
                transformation = parts[1].strip()
                result.append(f'  val mapeado = {collection}.map({transformation})')
                
        elif line.startswith('reducir'):
            # Operación reduce
            parts = line.replace('reducir', '').strip().split(' con ')
            if len(parts) >= 2:
                collection = parts[0].strip()
                operation = parts[1].strip()
                result.append(f'  val reducido = {collection}.reduce({operation})')
                
        elif line.startswith('fold'):
            # Operación fold
            parts = line.replace('fold', '').strip().split(' con ')
            if len(parts) >= 2:
                collection = parts[0].strip()
                operation = parts[1].strip()
                result.append(f'  val folded = {collection}.fold(0)({operation})')
                
        elif line.startswith('future'):
            # Programación asíncrona
            operation = line.replace('future', '').strip()
            result.extend([
                f'  val futureResult = Future {{',
                f'    {operation}',
                '  }',
                ''
            ])
            
        elif line.startswith('try'):
            # Manejo de errores
            operation = line.replace('try', '').strip()
            result.extend([
                f'  val resultado = Try {{',
                f'    {operation}',
                '  } match {',
                '    case Success(value) => println(s"Éxito: $value")',
                '    case Failure(exception) => println(s"Error: ${exception.getMessage}")',
                '  }',
                ''
            ])
            
        elif line.startswith('pattern matching'):
            # Pattern matching
            variable = line.replace('pattern matching', '').strip()
            result.extend([
                f'  {variable} match {{',
                '    case valor if valor > 0 => println("Positivo")',
                '    case 0 => println("Cero")',
                '    case _ => println("Negativo")',
                '  }',
                ''
            ])
            
        elif line.startswith('trait'):
            # Trait (similar a interface)
            trait_name = line.replace('trait', '').strip().strip('"')
            result.extend([
                f'trait {trait_name} {{',
                '  def metodo(): Unit',
                '}',
                ''
            ])
            
        elif line.startswith('extender'):
            # Herencia/extensión
            parts = line.replace('extender', '').strip().split(' con ')
            if len(parts) >= 2:
                class_name = parts[0].strip()
                trait_name = parts[1].strip()
                result.append(f'class {class_name} extends {trait_name} {{')
                
        elif line.startswith('implicito'):
            # Parámetro implícito
            param_def = line.replace('implicito', '').strip()
            result.append(f'  implicit val {param_def}')
            
        elif line.startswith('lazy val'):
            # Evaluación perezosa
            var_def = line.replace('lazy val', '').strip()
            result.append(f'  lazy val {var_def}')
            
        elif line.startswith('for comprehension'):
            # For comprehension
            parts = line.replace('for comprehension', '').strip().split(' en ')
            if len(parts) >= 2:
                variable = parts[0].strip()
                collection = parts[1].strip()
                result.extend([
                    f'  val resultado = for {{',
                    f'    {variable} <- {collection}',
                    f'  }} yield {variable}',
                    ''
                ])
                
        elif line.startswith('actor'):
            # Sistema de actores (Akka)
            actor_name = line.replace('actor', '').strip().strip('"')
            result.extend([
                'import akka.actor.{Actor, ActorSystem, Props}',
                '',
                f'class {actor_name} extends Actor {{',
                '  def receive = {',
                '    case msg => println(s"Recibido: $msg")',
                '  }',
                '}',
                ''
            ])
            
        elif line.startswith('spark'):
            # Apache Spark
            operation = line.replace('spark', '').strip()
            result.extend([
                'import org.apache.spark.sql.SparkSession',
                '',
                'val spark = SparkSession.builder()',
                '  .appName("VaderSparkApp")',
                '  .master("local[*]")',
                '  .getOrCreate()',
                '',
                f'// {operation}',
                ''
            ])
            
        elif line.startswith('mostrar'):
            # Imprimir
            content = line.replace('mostrar', '').strip().strip('"')
            result.append(f'    println("{content}")')
            
        elif line.startswith('fin funcion') or line.startswith('fin clase') or line.startswith('fin objeto'):
            result.extend([
                '  }',
                ''
            ])
    
    # Cerrar objeto principal
    result.append('}')
    
    return '\n'.join(result)

def _convert_params_to_scala(params):
    """Convierte parámetros de Vader a Scala"""
    if not params:
        return ''
    
    param_list = [param.strip() for param in params.split(',')]
    scala_params = []
    
    for param in param_list:
        # Asumir tipo String por defecto
        scala_params.append(f'{param}: String')
    
    return ', '.join(scala_params)

# Palabras clave específicas de Scala
SCALA_KEYWORDS = [
    'objeto scala', 'clase scala', 'case class', 'funcion pura', 'lista inmutable',
    'lista mutable', 'mapa', 'filtrar', 'mapear', 'reducir', 'fold', 'future',
    'try', 'pattern matching', 'trait', 'extender', 'implicito', 'lazy val',
    'for comprehension', 'actor', 'spark'
]

def detect_scala(code):
    """Detecta si el código contiene sintaxis específica de Scala"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in SCALA_KEYWORDS)
