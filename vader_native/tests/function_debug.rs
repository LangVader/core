use vader::{VaderLexer, VaderParser, VaderInterpreter, VaderValue};

#[cfg(test)]
mod function_debug_tests {
    use super::*;

    #[test]
    fn test_function_definition_debug() {
        println!("🔍 TEST DEBUG DE DEFINICIÓN DE FUNCIONES");
        
        let code = r#"
        funcion suma(a, b):
            retornar a + b
        
        suma(5, 7)
        "#;
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
        
        // Intentar ejecutar
        println!("🚀 EJECUTANDO CÓDIGO:");
        match interpreter.execute(ast) {
            Ok(result) => {
                println!("✅ Resultado: {:?}", result);
                match result {
                    VaderValue::Number(n) => {
                        println!("🔢 Número obtenido: {}", n);
                        assert_eq!(n, 12.0);
                    }
                    _ => {
                        println!("❌ Tipo de resultado inesperado: {:?}", result);
                        panic!("Expected number result, got: {:?}", result);
                    }
                }
            }
            Err(error) => {
                println!("❌ Error: {:?}", error);
                panic!("Error ejecutando código: {:?}", error);
            }
        }
    }
}
