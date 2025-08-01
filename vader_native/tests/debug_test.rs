use vader::{VaderLexer, VaderParser, VaderInterpreter, VaderValue};

#[cfg(test)]
mod debug_tests {
    use super::*;

    #[test]
    fn test_simple_string() {
        let code = r#""Hola mundo""#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Resultado simple string: {:?}", result);
        
        match result {
            VaderValue::String(s) => {
                println!("✅ String obtenido: '{}'", s);
                assert_eq!(s, "Hola mundo");
            },
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_string_concatenation() {
        let code = r#""Hola " + "mundo""#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Resultado concatenación: {:?}", result);
        
        match result {
            VaderValue::String(s) => {
                println!("✅ String concatenado: '{}'", s);
                assert_eq!(s, "Hola mundo");
            },
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_decir_simple() {
        let code = r#"decir("Hola mundo")"#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Resultado decir simple: {:?}", result);
        
        match result {
            VaderValue::String(s) => {
                println!("✅ Decir retornó: '{}'", s);
                assert_eq!(s, "Hola mundo");
            },
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_decir_concatenation() {
        let code = r#"decir("Hola " + "mundo")"#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Resultado decir concatenación: {:?}", result);
        
        match result {
            VaderValue::String(s) => {
                println!("✅ Decir concatenación: '{}'", s);
                assert_eq!(s, "Hola mundo");
            },
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_lexer_tokens() {
        let code = r#"decir "Hola " + "mundo""#;
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize().unwrap();
        
        println!("🔍 Tokens generados:");
        for (i, token) in tokens.iter().enumerate() {
            println!("  {}: {:?}", i, token);
        }
        
        // Verificar que tenemos los tokens esperados
        assert!(tokens.len() > 0);
    }

    // Función auxiliar para ejecutar código Vader
    fn execute_vader_code(code: &str) -> Result<VaderValue, Box<dyn std::error::Error>> {
        println!("🚀 Ejecutando código: {}", code);
        
        // Tokenizar
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize()?;
        println!("📝 Tokens: {} generados", tokens.len());
        
        // Parsear
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse()?;
        println!("🌳 AST: {} nodos generados", ast.len());
        
        // Interpretar
        let mut interpreter = VaderInterpreter::new();
        let result = interpreter.execute(ast)?;
        println!("⚡ Resultado: {:?}", result);
        
        Ok(result)
    }
}
