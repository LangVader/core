import hashlib
import nmap as nm
import ssl
import requests
import subprocess as sp
import socket
import re

import hashlib
import socket
import ssl
import requests
import re
# desde cryptography.fernet importar Fernet
# desde scapy.all importar sniff, IP, TCP
import nmap as nm
import subprocess as sp
class AnalizadorVulnerabilidades:
    def __init__(self):
        self.scanner_nmap = None
        self.puertos_comunes = None
        self.vulnerabilidades_encontradas = None
    def __init__(self)(self):
        self.scanner_nmap = nm.PortScanner()
        self.puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        self.vulnerabilidades_encontradas = lista

async def escanear_red(self, rango_ip):
    try:
        print(f"Iniciando escaneo de red: {rango_ip}")
        resultado = esperar self.scanner_nmap.scan(hosts=rango_ip, arguments='-sn')
        hosts_activos = lista
        for host in resultado['scan']:
            if resultado['scan'][host]['status']['state'] == 'up':
                hosts_activos.append(host)
                print(f"Host activo encontrado: {host}")
        for host in hosts_activos:
            await self.escanear_puertos(host)
        return hosts_activos
    except Exception as error:
        print(f"Error durante escaneo: {error}")
        return lista

async def escanear_puertos(self, host):
    try:
        print(f"Escaneando puertos en {host}...")
        puertos_str = ','.join([str(p) para p en self.puertos_comunes])
        resultado = esperar self.scanner_nmap.scan(
        hosts=host,
        ports=puertos_str,
        arguments='-sV -sC'
        # )
        if host en resultado['scan']:
            host_info = resultado['scan'][host]
            if 'tcp' en host_info:
                if info['state'] == 'open':
                    vulnerabilidad = {
                    # 'host': host,
                    # 'puerto': puerto,
                    # 'servicio': info.get('name', 'desconocido'),
                    # 'version': info.get('version', 'N/A'),
                    # 'riesgo': self.evaluar_riesgo(puerto, info)
                    # }
                    self.vulnerabilidades_encontradas.append(vulnerabilidad)
                    print(f"Puerto abierto: {host}:{puerto} - {info.get('name', 'desconocido')}")
except Exception as error:
    print(f"Error escaneando puertos en {host}: {error}")

    def evaluar_riesgo(self,(self):
        puertos_criticos = [21, 23, 135, 139, 445, 1433, 3389]
        if puerto en puertos_criticos:
            return "CRÍTICO"
            sino si puerto == 22 y 'ssh' en info.get('name', '').lower()
            return "MEDIO"
            # sino si puerto en [80, 443]
            return "BAJO"
        else:
            return "MEDIO"

    def generar_reporte(self)(self):
        print("\n=== REPORTE DE VULNERABILIDADES ===")
        print(f"Total de vulnerabilidades encontradas: {len(self.vulnerabilidades_encontradas)}")
        riesgos = {"CRÍTICO": 0, "MEDIO": 0, "BAJO": 0}
        for vuln in self.vulnerabilidades_encontradas:
            riesgos[vuln['riesgo']] += 1
            print(f"[{vuln['riesgo']}] {vuln['host']}:{vuln['puerto']} - {vuln['servicio']} {vuln['version']}")
        print(f"\nResumen por riesgo:")
        print(f"  {nivel}: {cantidad} vulnerabilidades")


class CifradoSeguro:
    def __init__(self):
        self.clave_fernet = None
        self.cipher_suite = None
    def __init__(self)(self):
        self.clave_fernet = Fernet.generate_key()
        self.cipher_suite = Fernet(self.clave_fernet)

    def cifrar_datos(self,(self):
        try:
            if isinstance(datos, str):
                datos = datos.encode('utf-8')
            datos_cifrados = self.cipher_suite.encrypt(datos)
            print("Datos cifrados exitosamente")
            return datos_cifrados
        except Exception as error:
            print(f"Error al cifrar: {error}")
            return None

    def descifrar_datos(self,(self):
        try:
            datos_descifrados = self.cipher_suite.decrypt(datos_cifrados)
            print("Datos descifrados exitosamente")
            return datos_descifrados.decode('utf-8')
        except Exception as error:
            print(f"Error al descifrar: {error}")
            return None

    def generar_hash_seguro(datos,(self):
        if algoritmo == 'sha256':
            hash_obj = hashlib.sha256()
            sino si algoritmo == 'md5'
            hash_obj = hashlib.md5()
            sino si algoritmo == 'sha512'
            hash_obj = hashlib.sha512()
        else:
            print(f"Algoritmo {algoritmo} no soportado")
            return None
        # hash_obj.update(datos.encode('utf-8'))
        return hash_obj.hexdigest()


@staticmethod
class DetectorIntrusiones:
    def __init__(self):
        self.patrones_maliciosos = None
        self.conexiones_sospechosas = None
    def __init__(self)(self):
        self.patrones_maliciosos = [
        r'(\bSELECT\b.*\bFROM\b.*\bWHERE\b.*\bOR\b.*=.*)',  # SQL Injection
        # r'(<script[^>]*>.*?</script>)',  # XSS
        # r'(\.\./.*\.\./)',  # Directory Traversal
        # r'(\bUNION\b.*\bSELECT\b)',  # SQL Union
        # r'(eval\s*\()',  # Code Injection
        # ]
        self.conexiones_sospechosas = lista

    def analizar_trafico(self,(self):
        try:
            if paquete.haslayer(IP) y paquete.haslayer(TCP):
                ip_src = paquete[IP].src
                ip_dst = paquete[IP].dst
                puerto_dst = paquete[TCP].dport
                if self.detectar_escaneo_puertos(ip_src, puerto_dst):
                    print(f"⚠️  Posible escaneo de puertos desde {ip_src}")
                if paquete.haslayer('Raw'):
                    payload = str(paquete['Raw'].load)
                    if self.detectar_payload_malicioso(payload):
                        print(f"🚨 Payload malicioso detectado desde {ip_src} a {ip_dst}:{puerto_dst}")
                        # 'src': ip_src,
                        # 'dst': ip_dst,
                        # 'puerto': puerto_dst,
                        # 'payload': payload[:100]  # Primeros 100 caracteres
                        # } a self.conexiones_sospechosas
        except Exception as error:
            print(f"Error analizando tráfico: {error}")

    def detectar_payload_malicioso(self,(self):
        for patron in self.patrones_maliciosos:
            if re.search(patron, payload, re.IGNORECASE):
                return True
        return False

    def detectar_escaneo_puertos(self,(self):
        return puerto en [21, 22, 23, 25, 53, 80, 135, 139, 443, 445]

    def iniciar_monitoreo(self,(self):
        print(f"Iniciando monitoreo de red en {interfaz} por {duracion} segundos...")
        try:
            # sniff(
            iface=interfaz,
            prn=self.analizar_trafico,
            timeout=duracion,
            filter="tcp"
            # )
            print(f"Monitoreo completado. Conexiones sospechosas: {len(self.conexiones_sospechosas)}")
        except Exception as error:
            print(f"Error durante monitoreo: {error}")


class AuditoriaWeb:
    def __init__(self):
        self.headers_seguridad = None
    def __init__(self)(self):
        self.headers_seguridad = [
        # 'X-Frame-Options',
        # 'X-XSS-Protection',
        # 'X-Content-Type-Options',
        # 'Strict-Transport-Security',
        # 'Content-Security-Policy',
        # 'X-Permitted-Cross-Domain-Policies'
        # ]

async def auditar_sitio_web(self, url):
    try:
        print(f"Auditando sitio web: {url}")
        ssl_valido = esperar self.verificar_ssl(url)
        headers_resultado = esperar self.verificar_headers_seguridad(url)
        vulns_web = esperar self.detectar_vulnerabilidades_web(url)
        # self.generar_reporte_web(url, ssl_valido, headers_resultado, vulns_web)
    except Exception as error:
        print(f"Error durante auditoría web: {error}")

async def verificar_ssl(self, url):
    try:
        response = esperar requests.get(url, timeout=10, verify=True)
        print("✅ Certificado SSL válido")
        return True
    except requests.exceptions.SSLError as error:
        print("❌ Problema con certificado SSL")
        return False
    except Exception as error:
        print(f"Error verificando SSL: {error}")
        return False

async def verificar_headers_seguridad(self, url):
    try:
        response = esperar requests.get(url, timeout=10)
        headers = response.headers
        resultado = diccionario
        for header in self.headers_seguridad:
            if header en headers:
                resultado[header] = "✅ Presente"
            else:
                resultado[header] = "❌ Ausente"
        return resultado
    except Exception as error:
        print(f"Error verificando headers: {error}")
        return diccionario

async def detectar_vulnerabilidades_web(self, url):
    vulnerabilidades = lista
    test_sql = f"{url}?id=1' OR '1'='1"
    try:
        response = esperar requests.get(test_sql, timeout=5)
        if "error" en response.text.lower() o "sql" en response.text.lower():
            vulnerabilidades.append("Posible SQL Injection")
    except Exception as error:
        pass
    test_xss = f"{url}?search=<script>alert('XSS')</script>"
    try:
        response = esperar requests.get(test_xss, timeout=5)
        if "<script>" en response.text:
            vulnerabilidades.append("Posible XSS")
    except Exception as error:
        pass
    return vulnerabilidades

    def generar_reporte_web(self,(self):
        print(f"\n=== REPORTE DE AUDITORÍA WEB: {url} ===")
        print(f"SSL/TLS: {'✅ Válido' si ssl_valido sino '❌ Inválido'}")
        print("\nHeaders de Seguridad:")
        print(f"  {header}: {estado}")
    print(f"\nVulnerabilidades detectadas: {len(vulnerabilidades)}")
    for vuln in vulnerabilidades:
        print(f"  🚨 {vuln}")


async def main_ciberseguridad():
    print("=== SISTEMA DE CIBERSEGURIDAD CON VADER ===")
    print("\n1. ANÁLISIS DE VULNERABILIDADES DE RED")
analizador = AnalizadorVulnerabilidades()
    hosts = esperar analizador.escanear_red("192.168.1.1-10")
    # analizador.generar_reporte()
    print("\n2. CIFRADO DE DATOS")
cifrador = CifradoSeguro()
    datos_sensibles = "Información confidencial de la empresa"
    datos_cifrados = cifrador.cifrar_datos(datos_sensibles)
    datos_recuperados = cifrador.descifrar_datos(datos_cifrados)
    print(f"Datos originales: {datos_sensibles}")
    print(f"Datos recuperados: {datos_recuperados}")
    password = "mi_password_seguro_123"
    hash_seguro = CifradoSeguro.generar_hash_seguro(password, 'sha256')
    print(f"Hash SHA256 de password: {hash_seguro}")
    print("\n3. DETECCIÓN DE INTRUSIONES")
detector = DetectorIntrusiones()
    print("Iniciando monitoreo de red (simulado)...")
    print("\n4. AUDITORÍA WEB")
auditor = AuditoriaWeb()
    await auditor.auditar_sitio_web("https://example.com")
    print("\n✅ Análisis de ciberseguridad completado")

main_ciberseguridad()