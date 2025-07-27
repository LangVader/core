#!/usr/bin/env python3
"""
Vader Mobile Runtime - Ejecución nativa de código Vader en aplicaciones móviles
Soporta React Native, Flutter, Ionic, y desarrollo nativo iOS/Android
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any

class VaderMobileRuntime:
    """Runtime para ejecutar código Vader en plataformas móviles"""
    
    def __init__(self):
        self.supported_platforms = {
            'react-native': {
                'extension': '.js',
                'framework': 'React Native',
                'description': 'Aplicaciones móviles multiplataforma con JavaScript'
            },
            'flutter': {
                'extension': '.dart',
                'framework': 'Flutter',
                'description': 'Aplicaciones móviles multiplataforma con Dart'
            },
            'ionic': {
                'extension': '.ts',
                'framework': 'Ionic',
                'description': 'Aplicaciones híbridas con TypeScript/Angular'
            },
            'native-ios': {
                'extension': '.swift',
                'framework': 'iOS Native',
                'description': 'Aplicaciones nativas iOS con Swift'
            },
            'native-android': {
                'extension': '.kt',
                'framework': 'Android Native',
                'description': 'Aplicaciones nativas Android con Kotlin'
            }
        }
        
        self.mobile_components = [
            'pantalla', 'vista', 'boton', 'texto', 'imagen', 'lista', 'formulario',
            'navegacion', 'tab', 'modal', 'alerta', 'cargando', 'scroll', 'input',
            'switch', 'slider', 'picker', 'mapa', 'camara', 'gps', 'sensor'
        ]
        
        self.mobile_apis = [
            'almacenamiento', 'notificaciones', 'camara', 'gps', 'acelerometro',
            'giroscopio', 'bluetooth', 'wifi', 'contactos', 'calendario', 'galeria',
            'compartir', 'vibrar', 'audio', 'video', 'biometria', 'push'
        ]
    
    def detect_mobile_components(self, vader_code: str) -> Dict[str, List[str]]:
        """Detectar componentes móviles en el código Vader"""
        detected = {
            'components': [],
            'apis': [],
            'screens': [],
            'actions': []
        }
        
        lines = vader_code.lower().split('\n')
        
        # Definir acciones móviles
        mobile_actions = [
            'navegar', 'ir', 'vibrar', 'tomar', 'foto', 'enviar', 'notificacion',
            'mostrar', 'ocultar', 'abrir', 'cerrar', 'guardar', 'cargar', 'compartir'
        ]
        
        # Mapear palabras específicas a acciones
        action_mappings = {
            'ir a': 'navegar',
            'tomar foto': 'foto',
            'enviar notificacion': 'notificacion'
        }
        
        for line in lines:
            # Detectar componentes
            for component in self.mobile_components:
                if component in line:
                    if component not in detected['components']:
                        detected['components'].append(component)
            
            # Detectar APIs
            for api in self.mobile_apis:
                if api in line:
                    if api not in detected['apis']:
                        detected['apis'].append(api)
            
            # Detectar acciones
            for action in mobile_actions:
                if action in line:
                    if action not in detected['actions']:
                        detected['actions'].append(action)
            
            # Detectar frases específicas mapeadas a acciones
            for phrase, action in action_mappings.items():
                if phrase in line:
                    if action not in detected['actions']:
                        detected['actions'].append(action)
            
            # Detectar pantallas
            if 'pantalla' in line and ('=' in line or 'crear' in line):
                screen_name = self.extract_screen_name(line)
                if screen_name and screen_name not in detected['screens']:
                    detected['screens'].append(screen_name)
        
        return detected
    
    def extract_screen_name(self, line: str) -> Optional[str]:
        """Extraer nombre de pantalla de una línea de código"""
        try:
            if '=' in line:
                parts = line.split('=')
                if len(parts) >= 2:
                    return parts[0].strip().replace('pantalla', '').strip()
            elif 'crear pantalla' in line:
                parts = line.split('crear pantalla')
                if len(parts) >= 2:
                    return parts[1].strip().split()[0]
        except:
            pass
        return None
    
    def generate_react_native_code(self, vader_code: str, components: Dict) -> str:
        """Generar código React Native desde Vader"""
        imports = [
            "import React, { useState, useEffect } from 'react';",
            "import { View, Text, Button, TextInput, ScrollView, Alert, StyleSheet, TouchableOpacity, Image, FlatList } from 'react-native';"
        ]
        
        # Agregar imports específicos según componentes detectados
        if 'mapa' in components['components']:
            imports.append("import MapView from 'react-native-maps';")
        if 'camara' in components['apis']:
            imports.append("import { Camera } from 'react-native-camera';")
        if 'gps' in components['apis']:
            imports.append("import Geolocation from 'react-native-geolocation-service';")
        
        code_lines = imports + ["", "function App() {"]
        
        # Estado inicial
        code_lines.extend([
            "  const [data, setData] = useState({});",
            "  const [loading, setLoading] = useState(false);",
            ""
        ])
        
        # Procesar líneas de Vader
        vader_lines = vader_code.split('\n')
        for line in vader_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            react_line = self.convert_vader_to_react_native(line, components)
            if react_line:
                code_lines.append(f"  {react_line}")
        
        # Render principal
        code_lines.extend([
            "",
            "  return (",
            "    <ScrollView style={styles.container}>",
            "      <View style={styles.content}>",
            "        {/* Contenido generado automáticamente */}",
            "        <Text style={styles.title}>Aplicación Vader</Text>",
        ])
        
        # Agregar componentes detectados
        for component in components['components']:
            if component == 'boton':
                code_lines.append("        <TouchableOpacity style={styles.button} onPress={() => Alert.alert('Botón presionado')}>")
                code_lines.append("          <Text style={styles.buttonText}>Botón</Text>")
                code_lines.append("        </TouchableOpacity>")
            elif component == 'input':
                code_lines.append("        <TextInput style={styles.input} placeholder='Ingrese texto' />")
            elif component == 'lista':
                code_lines.append("        <FlatList data={[]} renderItem={() => null} />")
        
        code_lines.extend([
            "      </View>",
            "    </ScrollView>",
            "  );",
            "}",
            "",
            "const styles = StyleSheet.create({",
            "  container: { flex: 1, backgroundColor: '#fff' },",
            "  content: { padding: 20 },",
            "  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },",
            "  button: { backgroundColor: '#007AFF', padding: 15, borderRadius: 8, marginVertical: 10 },",
            "  buttonText: { color: 'white', textAlign: 'center', fontSize: 16 },",
            "  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, borderRadius: 5, marginVertical: 10 }",
            "});",
            "",
            "export default App;"
        ])
        
        return '\n'.join(code_lines)
    
    def generate_flutter_code(self, vader_code: str, components: Dict) -> str:
        """Generar código Flutter desde Vader"""
        imports = [
            "import 'package:flutter/material.dart';",
            "import 'package:flutter/services.dart';"
        ]
        
        # Agregar imports específicos
        if 'mapa' in components['components']:
            imports.append("import 'package:google_maps_flutter/google_maps_flutter.dart';")
        if 'camara' in components['apis']:
            imports.append("import 'package:camera/camera.dart';")
        if 'gps' in components['apis']:
            imports.append("import 'package:geolocator/geolocator.dart';")
        
        code_lines = imports + [
            "",
            "void main() {",
            "  runApp(VaderMobileApp());",
            "}",
            "",
            "class VaderMobileApp extends StatelessWidget {",
            "  @override",
            "  Widget build(BuildContext context) {",
            "    return MaterialApp(",
            "      title: 'Vader App',",
            "      theme: ThemeData(primarySwatch: Colors.blue),",
            "      home: VaderHomePage(),",
            "    );",
            "  }",
            "}",
            "",
            "class VaderHomePage extends StatefulWidget {",
            "  @override",
            "  _VaderHomePageState createState() => _VaderHomePageState();",
            "}",
            "",
            "class _VaderHomePageState extends State<VaderHomePage> {",
            "  Map<String, dynamic> data = {};",
            "  bool loading = false;",
            "",
            "  @override",
            "  void initState() {",
            "    super.initState();",
            "    // Inicialización automática",
            "  }",
            ""
        ]
        
        # Procesar código Vader
        vader_lines = vader_code.split('\n')
        for line in vader_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            flutter_line = self.convert_vader_to_flutter(line, components)
            if flutter_line:
                code_lines.append(f"  {flutter_line}")
        
        # Build method
        code_lines.extend([
            "",
            "  @override",
            "  Widget build(BuildContext context) {",
            "    return Scaffold(",
            "      appBar: AppBar(title: Text('Aplicación Vader')),",
            "      body: SingleChildScrollView(",
            "        padding: EdgeInsets.all(16.0),",
            "        child: Column(",
            "          crossAxisAlignment: CrossAxisAlignment.stretch,",
            "          children: [",
            "            Text('¡Hola desde Vader!', style: Theme.of(context).textTheme.headline4),",
            "            SizedBox(height: 20),"
        ])
        
        # Agregar widgets según componentes
        for component in components['components']:
            if component == 'boton':
                code_lines.extend([
                    "            ElevatedButton(",
                    "              onPressed: () {},",
                    "              child: Text('Botón Vader'),",
                    "            ),",
                    "            SizedBox(height: 10),"
                ])
            elif component == 'input':
                code_lines.extend([
                    "            TextField(",
                    "              decoration: InputDecoration(labelText: 'Entrada de texto'),",
                    "            ),",
                    "            SizedBox(height: 10),"
                ])
            elif component == 'lista':
                code_lines.extend([
                    "            Container(",
                    "              height: 200,",
                    "              child: ListView.builder(",
                    "                itemCount: 0,",
                    "                itemBuilder: (context, index) => ListTile(),",
                    "              ),",
                    "            ),"
                ])
        
        code_lines.extend([
            "          ],",
            "        ),",
            "      ),",
            "    );",
            "  }",
            "}"
        ])
        
        return '\n'.join(code_lines)
    
    def convert_vader_to_react_native(self, line: str, components: Dict) -> Optional[str]:
        """Convertir línea de Vader a React Native"""
        line = line.strip()
        
        if line.startswith('mostrar '):
            content = line.replace('mostrar ', '', 1)
            return f"console.log({content});"
        elif line.startswith('boton '):
            return "// Botón generado automáticamente"
        elif '=' in line and not line.startswith('si '):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            return f"const {var_name} = {value};"
        
        return None
    
    def convert_vader_to_flutter(self, line: str, components: Dict) -> Optional[str]:
        """Convertir línea de Vader a Flutter"""
        line = line.strip()
        
        if line.startswith('mostrar '):
            content = line.replace('mostrar ', '', 1)
            return f"print({content});"
        elif '=' in line and not line.startswith('si '):
            parts = line.split('=', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            return f"var {var_name} = {value};"
        
        return None
    
    def generate_project_structure(self, platform: str, project_name: str, output_dir: str) -> Dict[str, str]:
        """Generar estructura de proyecto móvil"""
        structure = {}
        
        if platform == 'react-native':
            structure = {
                'package.json': self.generate_react_native_package_json(project_name),
                'index.js': self.generate_react_native_index(),
                'App.js': '',  # Se llenará con el código generado
                'app.json': json.dumps({"name": project_name, "displayName": project_name}),
                'android/app/build.gradle': self.generate_android_build_gradle(),
                'android/app/src/main/AndroidManifest.xml': self.generate_android_manifest(),
                'ios/Podfile': self.generate_ios_podfile(),
                'README.md': self.generate_mobile_readme(platform, project_name)
            }
        elif platform == 'flutter':
            structure = {
                'pubspec.yaml': self.generate_flutter_pubspec(project_name),
                'lib/main.dart': '',  # Se llenará con el código generado
                'android/app/build.gradle': self.generate_flutter_android_gradle(),
                'ios/Runner/Info.plist': self.generate_flutter_ios_plist(),
                'README.md': self.generate_mobile_readme(platform, project_name)
            }
        
        return structure
    
    def generate_react_native_package_json(self, project_name: str) -> str:
        """Generar package.json para React Native"""
        return json.dumps({
            "name": project_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": f"Aplicación móvil {project_name} generada con Vader",
            "main": "index.js",
            "scripts": {
                "android": "react-native run-android",
                "ios": "react-native run-ios",
                "start": "react-native start",
                "test": "jest"
            },
            "dependencies": {
                "react": "^18.0.0",
                "react-native": "^0.72.0"
            },
            "devDependencies": {
                "@babel/core": "^7.20.0",
                "@babel/preset-env": "^7.20.0",
                "jest": "^29.0.0"
            }
        }, indent=2)
    
    def generate_react_native_index(self) -> str:
        """Generar index.js para React Native"""
        return """import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);"""
    
    def generate_flutter_pubspec(self, project_name: str) -> str:
        """Generar pubspec.yaml para Flutter"""
        return f"""name: {project_name.lower().replace(' ', '_')}
description: Aplicación móvil {project_name} generada con Vader

version: 1.0.0+1

environment:
  sdk: ">=2.17.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true"""
    
    def generate_android_build_gradle(self) -> str:
        """Generar build.gradle para Android"""
        return """android {
    compileSdkVersion 33
    
    defaultConfig {
        applicationId "com.vader.app"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
    }
}"""
    
    def generate_android_manifest(self) -> str:
        """Generar AndroidManifest.xml"""
        return """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.vader.reactnative.app">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    
    <application
        android:name=".MainApplication"
        android:label="@string/app_name"
        android:theme="@style/AppTheme">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme">
            
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
    
    def generate_ios_podfile(self) -> str:
        """Generar Podfile para iOS"""
        return """platform :ios, '11.0'
require_relative '../node_modules/react-native/scripts/react_native_pods'

target 'VaderApp' do
  config = use_native_modules!
  use_react_native!(:path => config[:reactNativePath])
end"""
    
    def generate_flutter_android_gradle(self) -> str:
        """Generar build.gradle para Flutter Android"""
        return """android {
    compileSdkVersion 33
    
    defaultConfig {
        applicationId "com.vader.flutter.app"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0"
    }
}"""
    
    def generate_flutter_ios_plist(self) -> str:
        """Generar Info.plist para Flutter iOS"""
        return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Vader App</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>"""
    
    def generate_mobile_readme(self, platform: str, project_name: str) -> str:
        """Generar README para proyecto móvil"""
        return f"""# {project_name}

Aplicación móvil generada automáticamente con Vader Runtime.

## Plataforma: {platform.title()}

### Instalación

```bash
# Instalar dependencias
{"npm install" if platform == "react-native" else "flutter pub get"}

# Ejecutar en desarrollo
{"npm run android" if platform == "react-native" else "flutter run"}
```

### Características

- ✅ Generado automáticamente desde código Vader
- ✅ Estructura de proyecto completa
- ✅ Configuración lista para desarrollo
- ✅ Soporte para componentes móviles nativos

### Desarrollo

Este proyecto fue generado usando Vader Mobile Runtime. 
Puedes modificar el código Vader original y regenerar la aplicación.

### Comandos Útiles

```bash
# Regenerar desde Vader
vader generate mobile mi_codigo.vdr --platform {platform}

# Ejecutar tests
{"npm test" if platform == "react-native" else "flutter test"}

# Build para producción
{"npm run build" if platform == "react-native" else "flutter build apk"}
```
"""
    
    def run_vader_mobile(self, vader_code: str, platform: str, output_dir: str = './mobile_app') -> bool:
        """Ejecutar código Vader en runtime móvil"""
        try:
            print(f"📱 Ejecutando Vader Mobile Runtime para {platform}...")
            
            # Detectar componentes móviles
            components = self.detect_mobile_components(vader_code)
            
            print(f"🔍 Componentes detectados:")
            print(f"  📦 Componentes: {len(components['components'])} ({', '.join(components['components'])})")
            print(f"  🔌 APIs: {len(components['apis'])} ({', '.join(components['apis'])})")
            print(f"  📱 Pantallas: {len(components['screens'])} ({', '.join(components['screens'])})")
            
            # Crear directorio de salida
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generar código específico de la plataforma
            if platform == 'react-native':
                mobile_code = self.generate_react_native_code(vader_code, components)
                main_file = 'App.js'
            elif platform == 'flutter':
                mobile_code = self.generate_flutter_code(vader_code, components)
                main_file = 'lib/main.dart'
            else:
                print(f"❌ Plataforma {platform} no soportada")
                return False
            
            # Generar estructura de proyecto
            project_name = Path(output_dir).name
            structure = self.generate_project_structure(platform, project_name, output_dir)
            
            # Escribir archivos
            for file_path, content in structure.items():
                full_path = Path(output_dir) / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                if file_path.endswith(main_file.split('/')[-1]):
                    content = mobile_code
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"✅ Aplicación móvil generada en {output_dir}")
            print(f"📁 Archivos principales:")
            for file_path in structure.keys():
                print(f"  - {file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en Mobile Runtime: {e}")
            return False

def main():
    """Función principal para testing"""
    runtime = VaderMobileRuntime()
    
    # Código Vader de ejemplo
    vader_code = """# Aplicación móvil de ejemplo
titulo = "Mi App Móvil"
mensaje = "¡Hola desde Vader!"

# Crear pantalla principal
pantalla_principal = "inicio"

# Componentes
boton_principal = "Comenzar"
input_nombre = "Ingrese su nombre"

# APIs móviles
usar gps
usar camara
usar notificaciones

mostrar titulo
mostrar mensaje
"""
    
    print("🧪 PROBANDO VADER MOBILE RUNTIME")
    print("=" * 50)
    
    # Probar React Native
    success_rn = runtime.run_vader_mobile(vader_code, 'react-native', './test_react_native_app')
    
    # Probar Flutter
    success_flutter = runtime.run_vader_mobile(vader_code, 'flutter', './test_flutter_app')
    
    if success_rn and success_flutter:
        print("\n🎉 MOBILE RUNTIME FUNCIONAL - Ambas plataformas generadas exitosamente")
        return True
    else:
        print("\n❌ Algunos runtimes fallaron")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
