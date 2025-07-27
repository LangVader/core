#!/usr/bin/env python3
"""
Tests para Vader CLI - Interfaz Unificada
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from vader_cli import VaderCLI

def test_cli_initialization():
    """Test inicialización de CLI"""
    print("=== TEST: Inicialización CLI ===")
    
    cli = VaderCLI()
    
    # Verificar componentes
    assert cli.app_generator is not None, "App generator no inicializado"
    assert cli.version == "2.0.0", "Versión incorrecta"
    assert hasattr(cli, 'config'), "Configuración no inicializada"
    
    print("✅ CLI inicializada correctamente")
    return True

def test_config_management():
    """Test gestión de configuración"""
    print("\n=== TEST: Gestión de Configuración ===")
    
    cli = VaderCLI()
    
    # Test configuración por defecto
    assert 'default_target' in cli.config, "Configuración por defecto no cargada"
    assert cli.config['default_target'] == 'python', "Target por defecto incorrecto"
    
    # Test modificar configuración
    original_target = cli.config['default_target']
    cli.config['default_target'] = 'javascript'
    assert cli.config['default_target'] == 'javascript', "Configuración no modificada"
    
    # Restaurar
    cli.config['default_target'] = original_target
    
    print("✅ Gestión de configuración funcional")
    return True

def test_parser_creation():
    """Test creación de parser"""
    print("\n=== TEST: Creación de Parser ===")
    
    cli = VaderCLI()
    parser = cli.create_parser()
    
    # Verificar que el parser se crea correctamente
    assert parser is not None, "Parser no creado"
    assert parser.prog == 'vader', "Nombre de programa incorrecto"
    
    # Test help (no debe fallar)
    try:
        help_text = parser.format_help()
        assert 'transpile' in help_text, "Subcomando transpile no encontrado"
        assert 'generate' in help_text, "Subcomando generate no encontrado"
        assert 'project' in help_text, "Subcomando project no encontrado"
        assert 'config' in help_text, "Subcomando config no encontrado"
        print("✅ Parser creado con todos los subcomandos")
    except Exception as e:
        print(f"❌ Error creando parser: {e}")
        return False
    
    return True

def test_transpile_functionality():
    """Test funcionalidad de transpilación"""
    print("\n=== TEST: Funcionalidad de Transpilación ===")
    
    # Crear archivo temporal de prueba
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vdr', delete=False, encoding='utf-8') as f:
        f.write('nombre = "Prueba"\nmostrar "Hola " + nombre')
        temp_file = f.name
    
    try:
        cli = VaderCLI()
        
        # Simular argumentos
        class MockArgs:
            input_file = temp_file
            target = 'python'
            output = None
            run = False
            check = False
            verbose = False
        
        args = MockArgs()
        
        # Test transpilación
        result = cli.handle_transpile(args)
        assert result == 0, "Transpilación falló"
        
        print("✅ Transpilación funcional")
        
    finally:
        # Limpiar archivo temporal
        os.unlink(temp_file)
    
    return True

def test_init_functionality():
    """Test funcionalidad de inicialización"""
    print("\n=== TEST: Funcionalidad de Inicialización ===")
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        cli = VaderCLI()
        
        # Simular argumentos
        class MockArgs:
            project_name = 'test_project'
            template = 'basic'
            language = 'python'
        
        args = MockArgs()
        
        # Test inicialización
        result = cli.handle_init(args)
        assert result == 0, "Inicialización falló"
        
        # Verificar archivos creados
        project_path = Path('test_project')
        assert project_path.exists(), "Directorio de proyecto no creado"
        assert (project_path / 'main.vdr').exists(), "Archivo main.vdr no creado"
        assert (project_path / 'README.md').exists(), "Archivo README.md no creado"
        
        print("✅ Inicialización funcional")
    
    return True

def test_info_functionality():
    """Test funcionalidad de información"""
    print("\n=== TEST: Funcionalidad de Información ===")
    
    cli = VaderCLI()
    
    # Test info transpilers
    class MockArgs:
        info_type = 'transpilers'
    
    args = MockArgs()
    result = cli.handle_info(args)
    assert result == 0, "Info transpilers falló"
    
    # Test info frameworks
    args.info_type = 'frameworks'
    result = cli.handle_info(args)
    assert result == 0, "Info frameworks falló"
    
    # Test info status
    args.info_type = 'status'
    result = cli.handle_info(args)
    assert result == 0, "Info status falló"
    
    print("✅ Información funcional")
    return True

def test_config_commands():
    """Test comandos de configuración"""
    print("\n=== TEST: Comandos de Configuración ===")
    
    cli = VaderCLI()
    
    # Test config list
    class MockArgs:
        config_action = 'list'
    
    args = MockArgs()
    result = cli.handle_config(args)
    assert result == 0, "Config list falló"
    
    # Test config get
    args.config_action = 'get'
    args.key = 'default_target'
    result = cli.handle_config(args)
    assert result == 0, "Config get falló"
    
    # Test config set
    args.config_action = 'set'
    args.key = 'test_key'
    args.value = 'test_value'
    result = cli.handle_config(args)
    assert result == 0, "Config set falló"
    assert cli.config['test_key'] == 'test_value', "Valor no establecido"
    
    print("✅ Comandos de configuración funcionales")
    return True

def test_template_generation():
    """Test generación de plantillas"""
    print("\n=== TEST: Generación de Plantillas ===")
    
    cli = VaderCLI()
    
    # Test todas las plantillas
    templates = ['basic', 'web', 'api', 'mobile']
    
    for template in templates:
        content = cli.get_init_template(template, 'python')
        assert content is not None, f"Plantilla {template} no generada"
        assert len(content) > 0, f"Plantilla {template} vacía"
        assert 'mostrar' in content, f"Plantilla {template} no contiene sintaxis Vader"
    
    print("✅ Generación de plantillas funcional")
    return True

def run_all_tests():
    """Ejecutar todos los tests"""
    print("🧪 INICIANDO TESTS DE VADER CLI")
    print("=" * 60)
    
    tests = [
        test_cli_initialization,
        test_config_management,
        test_parser_creation,
        test_transpile_functionality,
        test_init_functionality,
        test_info_functionality,
        test_config_commands,
        test_template_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} falló: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    print(f"✅ Pasaron: {passed}")
    print(f"❌ Fallaron: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 TODOS LOS TESTS PASARON - CLI FUNCIONAL")
        return True
    else:
        print(f"\n⚠️ {failed} TESTS FALLARON")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
