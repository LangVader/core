use vader::lexer::VaderLexer;
use vader::parser::VaderParser;
use vader::interpreter::VaderInterpreter;
use vader::types::VaderValue;

#[test]
fn test_logical_operators_detailed_debug() {
    println!("\n🔍 DIAGNÓSTICO DETALLADO DE OPERADORES LÓGICOS");
    
    // Test 1: Lexer - verificar tokens generados
    let code = "(x > y) y (x != y)";
    println!("\n📝 Código: {}", code);
    
    let mut lexer = VaderLexer::new(code);
    let tokens = lexer.tokenize().unwrap();
    
    println!("\n🔤 TOKENS GENERADOS:");
    for (i, token) in tokens.iter().enumerate() {
        println!("  {}: {:?}", i, token);
    }
    
    // Test 2: Parser - verificar AST generado
    println!("\n🌳 PARSING:");
    let mut parser = VaderParser::new(tokens);
    match parser.parse() {
        Ok(ast) => {
            println!("  ✅ AST generado exitosamente:");
            for (i, node) in ast.iter().enumerate() {
                println!("    {}: {:?}", i, node);
            }
        }
        Err(e) => {
            println!("  ❌ Error de parsing: {:?}", e);
        }
    }
}

#[test]
fn test_simple_logical_and() {
    println!("\n🔍 TEST SIMPLE: verdadero y falso");
    
    let code = "verdadero y falso";
    println!("📝 Código: {}", code);
    
    let mut lexer = VaderLexer::new(code);
    let tokens = lexer.tokenize().unwrap();
    
    println!("\n🔤 TOKENS:");
    for token in &tokens {
        println!("  {:?}", token);
    }
    
    let mut parser = VaderParser::new(tokens);
    match parser.parse() {
        Ok(ast) => {
            println!("\n✅ AST: {:?}", ast);
            
            // Intentar interpretar
            let mut interpreter = VaderInterpreter::new();
            match interpreter.interpret(ast) {
                Ok(result) => println!("✅ Resultado: {:?}", result),
                Err(e) => println!("❌ Error de interpretación: {:?}", e),
            }
        }
        Err(e) => {
            println!("❌ Error de parsing: {:?}", e);
        }
    }
}

#[test]
fn test_comparison_with_logical() {
    println!("\n🔍 TEST COMPARACIÓN CON LÓGICO");
    
    // Simplificar el test problemático
    let code = r#"
    x = 10
    y = 5
    x > y
    "#;
    println!("📝 Código: {}", code);
    
    let mut lexer = VaderLexer::new(code);
    let tokens = lexer.tokenize().unwrap();
    
    let mut parser = VaderParser::new(tokens);
    match parser.parse() {
        Ok(ast) => {
            println!("✅ AST: {:?}", ast);
            
            let mut interpreter = VaderInterpreter::new();
            match interpreter.interpret(ast) {
                Ok(result) => println!("✅ Resultado: {:?}", result),
                Err(e) => println!("❌ Error de interpretación: {:?}", e),
            }
        }
        Err(e) => {
            println!("❌ Error de parsing: {:?}", e);
        }
    }
}

#[test]
fn test_exact_failing_case() {
    println!("\n🔍 TEST CASO EXACTO QUE FALLA");
    
    // El código exacto del test que falla
    let code = r#"
        x = 10
        y = 5
        (x > y) y (x != y)
        "#;
    println!("📝 Código: {}", code);
    
    let mut lexer = VaderLexer::new(code);
    let tokens = lexer.tokenize().unwrap();
    
    println!("\n🔤 TOKENS GENERADOS:");
    for (i, token) in tokens.iter().enumerate() {
        println!("  {}: {:?}", i, token);
    }
    
    let mut parser = VaderParser::new(tokens);
    match parser.parse() {
        Ok(ast) => {
            println!("\n✅ AST: {:?}", ast);
            
            let mut interpreter = VaderInterpreter::new();
            match interpreter.interpret(ast) {
                Ok(result) => println!("✅ Resultado: {:?}", result),
                Err(e) => println!("❌ Error de interpretación: {:?}", e),
            }
        }
        Err(e) => {
            println!("❌ Error de parsing: {:?}", e);
        }
    }
}
