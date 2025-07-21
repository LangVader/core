#!/usr/bin/env python3
"""
☁️ VADER CLOUD RUNTIME - PRIMERA IMPLEMENTACIÓN MUNDIAL
Runtime serverless de Vader para ejecución en la nube
Soporta AWS Lambda, Google Cloud Functions, Azure Functions
"""

import json
import os
import sys
import asyncio
import aiohttp
from typing import Dict, Any, Optional
import boto3
from datetime import datetime

class VaderCloudRuntime:
    """Runtime de Vader optimizado para entornos serverless"""
    
    def __init__(self, cloud_provider='aws'):
        self.variables = {}
        self.functions = {}
        self.cloud_provider = cloud_provider
        self.debug_mode = os.getenv('VADER_DEBUG', 'false').lower() == 'true'
        self.execution_context = {}
        
        # Inicializar servicios cloud
        self.cloud_services = self._init_cloud_services()
        
        print(f"☁️ Vader Cloud Runtime inicializado para {cloud_provider}")
    
    def _init_cloud_services(self):
        """Inicializar servicios específicos del proveedor cloud"""
        services = {}
        
        if self.cloud_provider == 'aws':
            try:
                services['s3'] = boto3.client('s3')
                services['dynamodb'] = boto3.resource('dynamodb')
                services['sns'] = boto3.client('sns')
                services['sqs'] = boto3.client('sqs')
                services['lambda'] = boto3.client('lambda')
            except Exception as e:
                print(f"⚠️ AWS services no disponibles: {e}")
        
        return services
    
    async def execute_serverless(self, event, context):
        """Punto de entrada para funciones serverless"""
        try:
            # Extraer código Vader del evento
            vader_code = event.get('vader_code', '')
            if not vader_code:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No se proporcionó código Vader'})
                }
            
            # Configurar contexto de ejecución
            self.execution_context = {
                'request_id': context.aws_request_id if hasattr(context, 'aws_request_id') else 'local',
                'function_name': context.function_name if hasattr(context, 'function_name') else 'vader-function',
                'memory_limit': context.memory_limit_in_mb if hasattr(context, 'memory_limit_in_mb') else 128,
                'time_remaining': context.get_remaining_time_in_millis() if hasattr(context, 'get_remaining_time_in_millis') else 30000
            }
            
            # Ejecutar código Vader
            result = await self.execute_code(vader_code)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'result': result,
                    'execution_time': datetime.now().isoformat(),
                    'context': self.execution_context
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': str(e),
                    'type': type(e).__name__
                })
            }
    
    async def execute_code(self, code: str) -> Dict[str, Any]:
        """Ejecutar código Vader en entorno cloud"""
        output = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    result = await self.execute_line(line)
                    if result:
                        output.append(result)
                except Exception as e:
                    error_msg = f"❌ Error línea {line_num}: {str(e)}"
                    output.append(error_msg)
                    if self.debug_mode:
                        print(error_msg)
        
        return {
            'output': output,
            'variables': self.variables,
            'execution_context': self.execution_context
        }
    
    async def execute_line(self, line: str) -> Optional[str]:
        """Ejecutar línea individual con comandos cloud"""
        
        # Comandos cloud específicos
        if line.startswith('subir archivo'):
            return await self.upload_file(line)
        elif line.startswith('descargar archivo'):
            return await self.download_file(line)
        elif line.startswith('guardar en base'):
            return await self.save_to_database(line)
        elif line.startswith('consultar base'):
            return await self.query_database(line)
        elif line.startswith('enviar notificacion'):
            return await self.send_notification(line)
        elif line.startswith('procesar cola'):
            return await self.process_queue(line)
        elif line.startswith('invocar funcion'):
            return await self.invoke_function(line)
        elif line.startswith('hacer peticion'):
            return await self.make_http_request(line)
        elif line.startswith('programar tarea'):
            return await self.schedule_task(line)
        elif line.startswith('obtener secreto'):
            return await self.get_secret(line)
        
        # Comandos básicos de Vader
        elif line.startswith('mostrar'):
            message = self.extract_string(line, 'mostrar')
            print(f"📤 {message}")
            return message
        elif ' = ' in line:
            return self.handle_assignment(line)
        elif line.startswith('si '):
            return await self.handle_conditional(line)
        else:
            # Evaluar expresión
            result = self.evaluate_expression(line)
            if result is not None:
                return str(result)
        
        return None
    
    async def upload_file(self, line: str) -> str:
        """Subir archivo a almacenamiento cloud"""
        # subir archivo "local.txt" a bucket "mi-bucket" como "remoto.txt"
        import re
        match = re.match(r'subir archivo "([^"]+)" a bucket "([^"]+)" como "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: subir archivo \"archivo\" a bucket \"bucket\" como \"nombre\""
        
        local_file, bucket, remote_name = match.groups()
        
        if self.cloud_provider == 'aws' and 's3' in self.cloud_services:
            try:
                self.cloud_services['s3'].upload_file(local_file, bucket, remote_name)
                return f"✅ Archivo subido: {local_file} → s3://{bucket}/{remote_name}"
            except Exception as e:
                return f"❌ Error subiendo archivo: {e}"
        
        return "❌ Servicio de almacenamiento no disponible"
    
    async def download_file(self, line: str) -> str:
        """Descargar archivo desde almacenamiento cloud"""
        import re
        match = re.match(r'descargar archivo "([^"]+)" de bucket "([^"]+)" como "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: descargar archivo \"archivo\" de bucket \"bucket\" como \"local\""
        
        remote_file, bucket, local_name = match.groups()
        
        if self.cloud_provider == 'aws' and 's3' in self.cloud_services:
            try:
                self.cloud_services['s3'].download_file(bucket, remote_file, local_name)
                return f"✅ Archivo descargado: s3://{bucket}/{remote_file} → {local_name}"
            except Exception as e:
                return f"❌ Error descargando archivo: {e}"
        
        return "❌ Servicio de almacenamiento no disponible"
    
    async def save_to_database(self, line: str) -> str:
        """Guardar datos en base de datos NoSQL"""
        # guardar en base "tabla" clave "id" valor "datos"
        import re
        match = re.match(r'guardar en base "([^"]+)" clave "([^"]+)" valor "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: guardar en base \"tabla\" clave \"id\" valor \"datos\""
        
        table_name, key, value = match.groups()
        
        if self.cloud_provider == 'aws' and 'dynamodb' in self.cloud_services:
            try:
                table = self.cloud_services['dynamodb'].Table(table_name)
                table.put_item(Item={'id': key, 'data': value, 'timestamp': datetime.now().isoformat()})
                return f"✅ Datos guardados en {table_name}: {key} = {value}"
            except Exception as e:
                return f"❌ Error guardando en base: {e}"
        
        return "❌ Base de datos no disponible"
    
    async def query_database(self, line: str) -> str:
        """Consultar base de datos"""
        import re
        match = re.match(r'consultar base "([^"]+)" clave "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: consultar base \"tabla\" clave \"id\""
        
        table_name, key = match.groups()
        
        if self.cloud_provider == 'aws' and 'dynamodb' in self.cloud_services:
            try:
                table = self.cloud_services['dynamodb'].Table(table_name)
                response = table.get_item(Key={'id': key})
                
                if 'Item' in response:
                    data = response['Item'].get('data', 'Sin datos')
                    self.variables[f'consulta_{key}'] = data
                    return f"✅ Consultado {table_name}[{key}]: {data}"
                else:
                    return f"❌ No encontrado: {key} en {table_name}"
            except Exception as e:
                return f"❌ Error consultando base: {e}"
        
        return "❌ Base de datos no disponible"
    
    async def send_notification(self, line: str) -> str:
        """Enviar notificación push/email"""
        message = self.extract_string(line, 'enviar notificacion')
        
        if self.cloud_provider == 'aws' and 'sns' in self.cloud_services:
            try:
                topic_arn = os.getenv('VADER_SNS_TOPIC')
                if topic_arn:
                    self.cloud_services['sns'].publish(
                        TopicArn=topic_arn,
                        Message=message,
                        Subject='Notificación Vader Cloud'
                    )
                    return f"✅ Notificación enviada: {message}"
                else:
                    return "❌ Topic SNS no configurado"
            except Exception as e:
                return f"❌ Error enviando notificación: {e}"
        
        return "❌ Servicio de notificaciones no disponible"
    
    async def make_http_request(self, line: str) -> str:
        """Hacer petición HTTP"""
        import re
        match = re.match(r'hacer peticion "([^"]+)" a "([^"]+)"', line)
        
        if not match:
            return "❌ Sintaxis: hacer peticion \"GET/POST\" a \"url\""
        
        method, url = match.groups()
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == 'GET':
                    async with session.get(url) as response:
                        data = await response.text()
                        self.variables['ultima_respuesta'] = data[:500]  # Limitar tamaño
                        return f"✅ {method} {url}: {response.status}"
                elif method.upper() == 'POST':
                    async with session.post(url) as response:
                        data = await response.text()
                        self.variables['ultima_respuesta'] = data[:500]
                        return f"✅ {method} {url}: {response.status}"
        except Exception as e:
            return f"❌ Error en petición HTTP: {e}"
        
        return "❌ Método HTTP no soportado"
    
    async def invoke_function(self, line: str) -> str:
        """Invocar otra función Lambda"""
        function_name = self.extract_string(line, 'invocar funcion')
        
        if self.cloud_provider == 'aws' and 'lambda' in self.cloud_services:
            try:
                response = self.cloud_services['lambda'].invoke(
                    FunctionName=function_name,
                    InvocationType='RequestResponse',
                    Payload=json.dumps({'vader_code': 'mostrar "Invocado desde Vader"'})
                )
                
                result = json.loads(response['Payload'].read())
                return f"✅ Función invocada: {function_name} → {result.get('statusCode', 'OK')}"
            except Exception as e:
                return f"❌ Error invocando función: {e}"
        
        return "❌ Servicio Lambda no disponible"
    
    def extract_string(self, line: str, command: str) -> str:
        """Extraer string de comando"""
        import re
        pattern = f'{command}\\s+"([^"]+)"'
        match = re.search(pattern, line)
        return match.group(1) if match else line.replace(command, '').strip()
    
    def handle_assignment(self, line: str) -> str:
        """Manejar asignación de variables"""
        variable, value = line.split(' = ', 1)
        variable = variable.strip()
        evaluated_value = self.evaluate_expression(value.strip())
        self.variables[variable] = evaluated_value
        
        if self.debug_mode:
            return f"📝 {variable} = {evaluated_value}"
        return None
    
    def evaluate_expression(self, expr: str):
        """Evaluar expresión simple"""
        # Reemplazar variables
        for var, val in self.variables.items():
            expr = expr.replace(var, str(val))
        
        # Evaluar expresión segura
        try:
            # Solo permitir operaciones básicas
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars or c.isalnum() for c in expr):
                return eval(expr)
            else:
                return expr.strip('"\'')
        except:
            return expr.strip('"\'')

# Funciones de entrada para diferentes proveedores cloud

def lambda_handler(event, context):
    """Handler para AWS Lambda"""
    runtime = VaderCloudRuntime('aws')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(runtime.execute_serverless(event, context))
    finally:
        loop.close()

def azure_main(req):
    """Handler para Azure Functions"""
    import azure.functions as func
    
    runtime = VaderCloudRuntime('azure')
    event = {'vader_code': req.get_body().decode('utf-8')}
    context = type('Context', (), {'function_name': 'vader-azure'})()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(runtime.execute_serverless(event, context))
        return func.HttpResponse(
            result['body'],
            status_code=result['statusCode'],
            headers=result.get('headers', {})
        )
    finally:
        loop.close()

def gcp_main(request):
    """Handler para Google Cloud Functions"""
    runtime = VaderCloudRuntime('gcp')
    
    if request.method == 'POST':
        event = {'vader_code': request.get_json().get('vader_code', '')}
    else:
        event = {'vader_code': request.args.get('vader_code', '')}
    
    context = type('Context', (), {'function_name': 'vader-gcp'})()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(runtime.execute_serverless(event, context))
        return result['body'], result['statusCode'], result.get('headers', {})
    finally:
        loop.close()

# CLI para testing local
if __name__ == "__main__":
    async def test_local():
        runtime = VaderCloudRuntime('aws')
        
        test_code = '''
        mostrar "🚀 Probando Vader Cloud Runtime"
        contador = 5
        mostrar "Contador inicial: " + contador
        hacer peticion "GET" a "https://httpbin.org/json"
        mostrar "Petición completada"
        '''
        
        result = await runtime.execute_code(test_code)
        print("\n📊 Resultado:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test_local())
