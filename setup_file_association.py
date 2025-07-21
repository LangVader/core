#!/usr/bin/env python3
"""
Script para configurar la asociación de archivos .vdr con el logo de Vader
Hace que los archivos .vdr se vean profesionales con el icono de Vader
"""

import os
import sys
import platform
import shutil
from pathlib import Path

def get_vader_root():
    """Obtiene la ruta raíz del proyecto Vader"""
    return Path(__file__).parent.absolute()

def setup_macos_file_association():
    """Configura la asociación de archivos en macOS"""
    print("🍎 Configurando asociación de archivos para macOS...")
    
    vader_root = get_vader_root()
    logo_path = vader_root / "assets" / "logo.png"
    
    if not logo_path.exists():
        print("❌ Error: No se encontró el logo en assets/logo.png")
        return False
    
    # Crear Info.plist para la asociación de archivos
    info_plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>vdr</string>
            </array>
            <key>CFBundleTypeIconFile</key>
            <string>logo.png</string>
            <key>CFBundleTypeName</key>
            <string>Vader Source File</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
            <key>LSHandlerRank</key>
            <string>Owner</string>
        </dict>
    </array>
    <key>CFBundleIdentifier</key>
    <string>com.vader.language</string>
    <key>CFBundleName</key>
    <string>Vader</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
</dict>
</plist>"""
    
    # Crear directorio de configuración si no existe
    config_dir = vader_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Guardar Info.plist
    info_plist_path = config_dir / "Info.plist"
    with open(info_plist_path, 'w') as f:
        f.write(info_plist_content)
    
    print(f"✅ Info.plist creado en: {info_plist_path}")
    
    # Instrucciones para el usuario
    print("\n📋 Para completar la configuración en macOS:")
    print("1. Abre 'Información del Sistema' > 'Aplicaciones'")
    print("2. Busca un archivo .vdr")
    print("3. Haz clic derecho > 'Obtener información'")
    print("4. En 'Abrir con', selecciona tu editor preferido")
    print("5. Haz clic en 'Cambiar todo...'")
    
    return True

def setup_windows_file_association():
    """Configura la asociación de archivos en Windows"""
    print("🪟 Configurando asociación de archivos para Windows...")
    
    vader_root = get_vader_root()
    logo_path = vader_root / "assets" / "logo.png"
    
    if not logo_path.exists():
        print("❌ Error: No se encontró el logo en assets/logo.png")
        return False
    
    # Crear archivo .reg para Windows
    logo_path_windows = str(logo_path).replace('/', '\\\\')
    reg_content = f"""Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\\.vdr]
@="VaderFile"

[HKEY_CLASSES_ROOT\\VaderFile]
@="Archivo de Código Vader"

[HKEY_CLASSES_ROOT\\VaderFile\\DefaultIcon]
@="{logo_path_windows},0"

[HKEY_CLASSES_ROOT\\VaderFile\\shell]

[HKEY_CLASSES_ROOT\\VaderFile\\shell\\open]

[HKEY_CLASSES_ROOT\\VaderFile\\shell\\open\\command]
@="notepad.exe \\"%1\\""
"""
    
    # Crear directorio de configuración si no existe
    config_dir = vader_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Guardar archivo .reg
    reg_path = config_dir / "vader_file_association.reg"
    with open(reg_path, 'w', encoding='utf-8') as f:
        f.write(reg_content)
    
    print(f"✅ Archivo .reg creado en: {reg_path}")
    
    # Instrucciones para el usuario
    print("\n📋 Para completar la configuración en Windows:")
    print(f"1. Ejecuta como administrador: {reg_path}")
    print("2. Confirma los cambios en el registro")
    print("3. Los archivos .vdr ahora mostrarán el logo de Vader")
    
    return True

def setup_linux_file_association():
    """Configura la asociación de archivos en Linux"""
    print("🐧 Configurando asociación de archivos para Linux...")
    
    vader_root = get_vader_root()
    logo_path = vader_root / "assets" / "logo.png"
    
    if not logo_path.exists():
        print("❌ Error: No se encontró el logo en assets/logo.png")
        return False
    
    # Crear archivo .desktop
    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Vader
Comment=Lenguaje de programación en español natural
Exec=python3 {vader_root}/src/vader.py %f
Icon={logo_path}
MimeType=text/x-vader;
Categories=Development;TextEditor;
"""
    
    # Crear archivo MIME type
    mime_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="text/x-vader">
        <comment>Archivo de código Vader</comment>
        <comment xml:lang="es">Archivo de código Vader</comment>
        <glob pattern="*.vdr"/>
        <icon name="vader-logo"/>
    </mime-type>
</mime-info>"""
    
    # Crear directorio de configuración si no existe
    config_dir = vader_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Guardar archivos de configuración
    desktop_path = config_dir / "vader.desktop"
    mime_path = config_dir / "vader-mime.xml"
    
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    with open(mime_path, 'w') as f:
        f.write(mime_content)
    
    print(f"✅ Archivo .desktop creado en: {desktop_path}")
    print(f"✅ Archivo MIME creado en: {mime_path}")
    
    # Instrucciones para el usuario
    print("\n📋 Para completar la configuración en Linux:")
    print(f"1. Copia {desktop_path} a ~/.local/share/applications/")
    print(f"2. Ejecuta: xdg-mime install {mime_path}")
    print(f"3. Ejecuta: xdg-mime default vader.desktop text/x-vader")
    print("4. Actualiza la base de datos MIME: update-mime-database ~/.local/share/mime")
    
    return True

def create_icon_variants():
    """Crea variantes del icono para diferentes tamaños"""
    print("🎨 Creando variantes del icono...")
    
    vader_root = get_vader_root()
    logo_path = vader_root / "assets" / "logo.png"
    icons_dir = vader_root / "assets" / "icons"
    
    if not logo_path.exists():
        print("❌ Error: No se encontró el logo en assets/logo.png")
        return False
    
    # Crear directorio de iconos
    icons_dir.mkdir(exist_ok=True)
    
    # Copiar logo original
    shutil.copy2(logo_path, icons_dir / "vader-logo.png")
    
    print(f"✅ Icono copiado a: {icons_dir / 'vader-logo.png'}")
    
    # Crear archivo de información de iconos
    icon_info = f"""# Iconos de Vader

## Archivos disponibles:
- `vader-logo.png` - Logo principal de Vader

## Uso:
- **macOS**: Configurado en Info.plist
- **Windows**: Configurado en archivo .reg
- **Linux**: Configurado en archivos .desktop y MIME

## Tamaños recomendados:
- 16x16, 32x32, 48x48, 64x64, 128x128, 256x256

## Formatos soportados:
- PNG (recomendado)
- ICO (Windows)
- ICNS (macOS)
"""
    
    with open(icons_dir / "README.md", 'w') as f:
        f.write(icon_info)
    
    return True

def main():
    """Función principal"""
    print("🎨 Configurador de Asociación de Archivos Vader")
    print("=" * 50)
    
    # Detectar sistema operativo
    system = platform.system().lower()
    
    print(f"🖥️ Sistema detectado: {system}")
    print(f"📁 Directorio Vader: {get_vader_root()}")
    
    # Crear variantes de iconos
    create_icon_variants()
    
    # Configurar según el sistema operativo
    success = False
    
    if system == "darwin":  # macOS
        success = setup_macos_file_association()
    elif system == "windows":  # Windows
        success = setup_windows_file_association()
    elif system == "linux":  # Linux
        success = setup_linux_file_association()
    else:
        print(f"❌ Sistema operativo no soportado: {system}")
        return False
    
    if success:
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("🎨 Los archivos .vdr ahora mostrarán el logo de Vader")
        print("📝 Sigue las instrucciones específicas para tu sistema operativo")
    else:
        print("\n❌ Error en la configuración")
        return False
    
    return True

if __name__ == "__main__":
    main()
