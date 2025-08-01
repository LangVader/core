use vader::{VaderLexer, VaderParser, VaderInterpreter, VaderValue};

#[cfg(test)]
mod decir_debug_tests {
    use super::*;

    #[test]
    fn test_decir_function_debug() {
        println!("🔍 TEST DEBUG DE FUNCIÓN DECIR");
        
        let code = r#"decir "Hola mundo""#;
        println!("📝 Código: {}", code);
        
        // Tokenizar
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize().unwrap();
        println!("🔤 TOKENS GENERADOS:");
        for (i, token) in tokens.iter().enumerate() {
            println!("  {}: {:?}", i, token);
        }
        
        // Parsear
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        println!("🌳 AST GENERADO: {:?}", ast);
        
        // Interpretar
        let mut interpreter = VaderInterpreter::new();
        
        // Debug: verificar si decir está en stdlib
        println!("🔧 VERIFICANDO STDLIB:");
        let stdlib = &interpreter.stdlib;
        let has_decir = stdlib.get_function("decir").is_some();
        println!("  ¿Tiene función 'decir'?: {}", has_decir);
        
        let has_print = stdlib.get_function("print").is_some();
        println!("  ¿Tiene función 'print'?: {}", has_print);
        
        // Intentar ejecutar
        println!("🚀 EJECUTANDO CÓDIGO:");
        match interpreter.execute(ast) {
            Ok(result) => {
                println!("✅ Resultado: {:?}", result);
            }
            Err(error) => {
                println!("❌ Error: {:?}", error);
                panic!("Error ejecutando código: {:?}", error);
            }
        }
    }
}
