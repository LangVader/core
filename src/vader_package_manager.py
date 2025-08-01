#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VADER 7.0 - GESTOR DE PAQUETES Y LIBRERÍAS
==========================================
Sistema completo de gestión de paquetes para Vader (vader-pack CLI)

Características:
- Instalación y desinstalación de paquetes
- Repositorio central de paquetes
- Versionado semántico
- Dependencias automáticas
- Cache local de paquetes
- Publicación de paquetes
- Búsqueda y descubrimiento

Autor: Vader Team
Versión: 7.0.0 "Universal"
Fecha: 2025
"""

import os
import re
import sys
import json
import shutil
import hashlib
import requests
import tarfile
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from urllib.parse import urljoin
import tempfile
import semver
from datetime import datetime

@dataclass
class VaderPackage:
    """Representa un paquete Vader"""
    name: str
    version: str
    description: str
    author: str
    license: str = "MIT"
    keywords: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    dev_dependencies: Dict[str, str] = field(default_factory=dict)
    main_file: str = "main.vdr"
    files: List[str] = field(default_factory=list)
    repository: str = ""
    homepage: str = ""
    bugs: str = ""
    scripts: Dict[str, str] = field(default_factory=dict)
    vader_version: str = ">=7.0.0"
    created_at: str = ""
    updated_at: str = ""
    download_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el paquete a diccionario"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'license': self.license,
            'keywords': self.keywords,
            'dependencies': self.dependencies,
            'devDependencies': self.dev_dependencies,
            'main': self.main_file,
            'files': self.files,
            'repository': self.repository,
            'homepage': self.homepage,
            'bugs': self.bugs,
            'scripts': self.scripts,
            'vaderVersion': self.vader_version,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at,
            'downloadCount': self.download_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VaderPackage':
        """Crea un paquete desde diccionario"""
        return cls(
            name=data.get('name', ''),
            version=data.get('version', '1.0.0'),
            description=data.get('description', ''),
            author=data.get('author', ''),
            license=data.get('license', 'MIT'),
            keywords=data.get('keywords', []),
            dependencies=data.get('dependencies', {}),
            dev_dependencies=data.get('devDependencies', {}),
            main_file=data.get('main', 'main.vdr'),
            files=data.get('files', []),
            repository=data.get('repository', ''),
            homepage=data.get('homepage', ''),
            bugs=data.get('bugs', ''),
            scripts=data.get('scripts', {}),
            vader_version=data.get('vaderVersion', '>=7.0.0'),
            created_at=data.get('createdAt', ''),
            updated_at=data.get('updatedAt', ''),
            download_count=data.get('downloadCount', 0)
        )

class VaderPackageManager:
    """Gestor de paquetes para Vader"""
    
    def __init__(self, registry_url: str = "https://registry.vaderhub.org"):
        self.registry_url = registry_url
        self.cache_dir = Path.home() / ".vader" / "cache"
        self.packages_dir = Path.home() / ".vader" / "packages"
        self.config_file = Path.home() / ".vader" / "config.json"
        
        # Crear directorios necesarios
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar configuración
        self.config = self._load_config()
        
        # Paquetes instalados
        self.installed_packages: Dict[str, VaderPackage] = {}
        self._load_installed_packages()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración del gestor de paquetes"""
        default_config = {
            "registry": self.registry_url,
            "cache_ttl": 3600,  # 1 hora
            "auto_update": False,
            "prefer_stable": True,
            "proxy": None,
            "auth_token": None
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception:
                pass
        
        return default_config
    
    def _save_config(self):
        """Guarda la configuración"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _load_installed_packages(self):
        """Carga la lista de paquetes instalados"""
        lock_file = self.packages_dir / "vader-lock.json"
        if lock_file.exists():
            try:
                with open(lock_file, 'r', encoding='utf-8') as f:
                    lock_data = json.load(f)
                    for name, pkg_data in lock_data.get('packages', {}).items():
                        self.installed_packages[name] = VaderPackage.from_dict(pkg_data)
            except Exception:
                pass
    
    def _save_installed_packages(self):
        """Guarda la lista de paquetes instalados"""
        lock_file = self.packages_dir / "vader-lock.json"
        lock_data = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "packages": {
                name: pkg.to_dict() 
                for name, pkg in self.installed_packages.items()
            }
        }
        
        with open(lock_file, 'w', encoding='utf-8') as f:
            json.dump(lock_data, f, indent=2, ensure_ascii=False)
    
    def search_packages(self, query: str, limit: int = 20) -> List[VaderPackage]:
        """Busca paquetes en el registry"""
        try:
            response = requests.get(
                f"{self.registry_url}/search",
                params={"q": query, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            packages = []
            
            for pkg_data in results.get('packages', []):
                packages.append(VaderPackage.from_dict(pkg_data))
            
            return packages
            
        except Exception as e:
            print(f"❌ Error buscando paquetes: {e}")
            return []
    
    def get_package_info(self, package_name: str) -> Optional[VaderPackage]:
        """Obtiene información de un paquete"""
        try:
            response = requests.get(
                f"{self.registry_url}/package/{package_name}",
                timeout=10
            )
            response.raise_for_status()
            
            pkg_data = response.json()
            return VaderPackage.from_dict(pkg_data)
            
        except Exception as e:
            print(f"❌ Error obteniendo información del paquete {package_name}: {e}")
            return None
    
    def get_package_versions(self, package_name: str) -> List[str]:
        """Obtiene todas las versiones disponibles de un paquete"""
        try:
            response = requests.get(
                f"{self.registry_url}/package/{package_name}/versions",
                timeout=10
            )
            response.raise_for_status()
            
            versions_data = response.json()
            return versions_data.get('versions', [])
            
        except Exception as e:
            print(f"❌ Error obteniendo versiones del paquete {package_name}: {e}")
            return []
    
    def resolve_version(self, package_name: str, version_spec: str) -> Optional[str]:
        """Resuelve una especificación de versión a una versión concreta"""
        available_versions = self.get_package_versions(package_name)
        if not available_versions:
            return None
        
        # Ordenar versiones
        try:
            sorted_versions = sorted(available_versions, key=semver.VersionInfo.parse, reverse=True)
        except Exception:
            sorted_versions = sorted(available_versions, reverse=True)
        
        # Resolver especificación
        if version_spec == "latest" or version_spec == "*":
            return sorted_versions[0]
        
        if version_spec.startswith("^"):
            # Compatible version (^1.2.3 = >=1.2.3 <2.0.0)
            base_version = version_spec[1:]
            try:
                base_ver = semver.VersionInfo.parse(base_version)
                for version in sorted_versions:
                    ver = semver.VersionInfo.parse(version)
                    if (ver.major == base_ver.major and 
                        ver >= base_ver):
                        return version
            except Exception:
                pass
        
        if version_spec.startswith("~"):
            # Patch-level changes (~1.2.3 = >=1.2.3 <1.3.0)
            base_version = version_spec[1:]
            try:
                base_ver = semver.VersionInfo.parse(base_version)
                for version in sorted_versions:
                    ver = semver.VersionInfo.parse(version)
                    if (ver.major == base_ver.major and 
                        ver.minor == base_ver.minor and
                        ver >= base_ver):
                        return version
            except Exception:
                pass
        
        # Versión exacta
        if version_spec in available_versions:
            return version_spec
        
        return None
    
    def download_package(self, package_name: str, version: str) -> Optional[str]:
        """Descarga un paquete a la cache"""
        cache_key = f"{package_name}-{version}"
        cache_path = self.cache_dir / f"{cache_key}.tar.gz"
        
        # Verificar si ya está en cache
        if cache_path.exists():
            return str(cache_path)
        
        try:
            response = requests.get(
                f"{self.registry_url}/package/{package_name}/{version}/download",
                timeout=30,
                stream=True
            )
            response.raise_for_status()
            
            # Descargar archivo
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(cache_path)
            
        except Exception as e:
            print(f"❌ Error descargando paquete {package_name}@{version}: {e}")
            return None
    
    def install_package(self, package_spec: str, save_dev: bool = False) -> bool:
        """Instala un paquete y sus dependencias"""
        # Parsear especificación del paquete
        if '@' in package_spec:
            package_name, version_spec = package_spec.split('@', 1)
        else:
            package_name = package_spec
            version_spec = "latest"
        
        print(f"📦 Instalando {package_name}@{version_spec}...")
        
        # Resolver versión
        resolved_version = self.resolve_version(package_name, version_spec)
        if not resolved_version:
            print(f"❌ No se pudo resolver la versión {version_spec} para {package_name}")
            return False
        
        # Verificar si ya está instalado
        if package_name in self.installed_packages:
            installed_version = self.installed_packages[package_name].version
            if installed_version == resolved_version:
                print(f"✅ {package_name}@{resolved_version} ya está instalado")
                return True
        
        # Descargar paquete
        package_file = self.download_package(package_name, resolved_version)
        if not package_file:
            return False
        
        # Extraer paquete
        package_dir = self.packages_dir / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        package_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with tarfile.open(package_file, 'r:gz') as tar:
                tar.extractall(package_dir)
        except Exception as e:
            print(f"❌ Error extrayendo paquete: {e}")
            return False
        
        # Leer package.json del paquete
        package_json_path = package_dir / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                package = VaderPackage.from_dict(package_data)
        else:
            # Crear paquete básico
            package = VaderPackage(
                name=package_name,
                version=resolved_version,
                description=f"Paquete Vader: {package_name}",
                author="Desconocido"
            )
        
        # Instalar dependencias
        if package.dependencies:
            print(f"📋 Instalando dependencias de {package_name}...")
            for dep_name, dep_version in package.dependencies.items():
                if not self.install_package(f"{dep_name}@{dep_version}"):
                    print(f"⚠️ Error instalando dependencia {dep_name}@{dep_version}")
        
        # Registrar paquete instalado
        self.installed_packages[package_name] = package
        self._save_installed_packages()
        
        print(f"✅ {package_name}@{resolved_version} instalado correctamente")
        return True
    
    def uninstall_package(self, package_name: str) -> bool:
        """Desinstala un paquete"""
        if package_name not in self.installed_packages:
            print(f"❌ El paquete {package_name} no está instalado")
            return False
        
        print(f"🗑️ Desinstalando {package_name}...")
        
        # Verificar dependencias
        dependents = []
        for name, pkg in self.installed_packages.items():
            if package_name in pkg.dependencies:
                dependents.append(name)
        
        if dependents:
            print(f"⚠️ Los siguientes paquetes dependen de {package_name}:")
            for dep in dependents:
                print(f"  - {dep}")
            
            response = input("¿Continuar con la desinstalación? (s/N): ")
            if response.lower() != 's':
                print("❌ Desinstalación cancelada")
                return False
        
        # Eliminar directorio del paquete
        package_dir = self.packages_dir / package_name
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        # Eliminar del registro
        del self.installed_packages[package_name]
        self._save_installed_packages()
        
        print(f"✅ {package_name} desinstalado correctamente")
        return True
    
    def list_installed(self) -> List[VaderPackage]:
        """Lista paquetes instalados"""
        return list(self.installed_packages.values())
    
    def update_package(self, package_name: str = None) -> bool:
        """Actualiza un paquete o todos los paquetes"""
        if package_name:
            # Actualizar paquete específico
            if package_name not in self.installed_packages:
                print(f"❌ El paquete {package_name} no está instalado")
                return False
            
            current_version = self.installed_packages[package_name].version
            latest_version = self.resolve_version(package_name, "latest")
            
            if current_version == latest_version:
                print(f"✅ {package_name} ya está en la última versión ({current_version})")
                return True
            
            print(f"🔄 Actualizando {package_name} de {current_version} a {latest_version}")
            return self.install_package(f"{package_name}@{latest_version}")
        
        else:
            # Actualizar todos los paquetes
            print("🔄 Actualizando todos los paquetes...")
            success = True
            
            for pkg_name in list(self.installed_packages.keys()):
                if not self.update_package(pkg_name):
                    success = False
            
            return success
    
    def create_package(self, directory: str, output_file: str = None) -> bool:
        """Crea un paquete .tar.gz desde un directorio"""
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"❌ El directorio {directory} no existe")
            return False
        
        # Verificar package.json
        package_json = dir_path / "package.json"
        if not package_json.exists():
            print("❌ No se encontró package.json en el directorio")
            return False
        
        # Leer información del paquete
        with open(package_json, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        package_name = package_data.get('name', 'unknown')
        package_version = package_data.get('version', '1.0.0')
        
        if output_file is None:
            output_file = f"{package_name}-{package_version}.tar.gz"
        
        print(f"📦 Creando paquete {package_name}@{package_version}...")
        
        # Crear archivo tar.gz
        try:
            with tarfile.open(output_file, 'w:gz') as tar:
                tar.add(dir_path, arcname=package_name)
            
            print(f"✅ Paquete creado: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando paquete: {e}")
            return False
    
    def publish_package(self, package_file: str, auth_token: str = None) -> bool:
        """Publica un paquete en el registry"""
        if not Path(package_file).exists():
            print(f"❌ El archivo {package_file} no existe")
            return False
        
        # Usar token de configuración si no se proporciona
        if auth_token is None:
            auth_token = self.config.get('auth_token')
        
        if not auth_token:
            print("❌ Se requiere un token de autenticación para publicar")
            return False
        
        print(f"📤 Publicando {package_file}...")
        
        try:
            with open(package_file, 'rb') as f:
                files = {'package': f}
                headers = {'Authorization': f'Bearer {auth_token}'}
                
                response = requests.post(
                    f"{self.registry_url}/publish",
                    files=files,
                    headers=headers,
                    timeout=60
                )
                response.raise_for_status()
            
            result = response.json()
            print(f"✅ Paquete publicado correctamente: {result.get('message', 'OK')}")
            return True
            
        except Exception as e:
            print(f"❌ Error publicando paquete: {e}")
            return False

def main():
    """Función principal del CLI vader-pack"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vader Package Manager")
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando install
    install_parser = subparsers.add_parser('install', help='Instalar paquete')
    install_parser.add_argument('package', help='Nombre del paquete')
    install_parser.add_argument('--save-dev', action='store_true', help='Guardar como dependencia de desarrollo')
    
    # Comando uninstall
    uninstall_parser = subparsers.add_parser('uninstall', help='Desinstalar paquete')
    uninstall_parser.add_argument('package', help='Nombre del paquete')
    
    # Comando search
    search_parser = subparsers.add_parser('search', help='Buscar paquetes')
    search_parser.add_argument('query', help='Término de búsqueda')
    search_parser.add_argument('--limit', type=int, default=20, help='Límite de resultados')
    
    # Comando list
    list_parser = subparsers.add_parser('list', help='Listar paquetes instalados')
    
    # Comando update
    update_parser = subparsers.add_parser('update', help='Actualizar paquetes')
    update_parser.add_argument('package', nargs='?', help='Paquete específico a actualizar')
    
    # Comando info
    info_parser = subparsers.add_parser('info', help='Información del paquete')
    info_parser.add_argument('package', help='Nombre del paquete')
    
    # Comando create
    create_parser = subparsers.add_parser('create', help='Crear paquete')
    create_parser.add_argument('directory', help='Directorio del paquete')
    create_parser.add_argument('--output', help='Archivo de salida')
    
    # Comando publish
    publish_parser = subparsers.add_parser('publish', help='Publicar paquete')
    publish_parser.add_argument('package', help='Archivo del paquete')
    publish_parser.add_argument('--token', help='Token de autenticación')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Crear gestor de paquetes
    pm = VaderPackageManager()
    
    # Ejecutar comando
    if args.command == 'install':
        pm.install_package(args.package, args.save_dev)
    
    elif args.command == 'uninstall':
        pm.uninstall_package(args.package)
    
    elif args.command == 'search':
        packages = pm.search_packages(args.query, args.limit)
        print(f"🔍 Encontrados {len(packages)} paquetes:")
        for pkg in packages:
            print(f"  📦 {pkg.name}@{pkg.version} - {pkg.description}")
    
    elif args.command == 'list':
        packages = pm.list_installed()
        print(f"📋 Paquetes instalados ({len(packages)}):")
        for pkg in packages:
            print(f"  📦 {pkg.name}@{pkg.version}")
    
    elif args.command == 'update':
        pm.update_package(args.package)
    
    elif args.command == 'info':
        pkg = pm.get_package_info(args.package)
        if pkg:
            print(f"📦 {pkg.name}@{pkg.version}")
            print(f"📝 {pkg.description}")
            print(f"👤 Autor: {pkg.author}")
            print(f"📄 Licencia: {pkg.license}")
            if pkg.dependencies:
                print(f"📋 Dependencias: {', '.join(pkg.dependencies.keys())}")
        else:
            print(f"❌ No se encontró el paquete {args.package}")
    
    elif args.command == 'create':
        pm.create_package(args.directory, args.output)
    
    elif args.command == 'publish':
        pm.publish_package(args.package, args.token)

if __name__ == "__main__":
    main()
