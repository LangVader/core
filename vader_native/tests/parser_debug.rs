use vader::{VaderLexer, VaderParser, VaderInterpreter, VaderValue};

#[cfg(test)]
mod parser_debug_tests {
    use super::*;

    #[test]
    fn test_function_with_parens() {
        let code = r#"decir("Hola mundo")"#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Con paréntesis: {:?}", result);
        
        match result {
            VaderValue::String(s) => assert_eq!(s, "Hola mundo"),
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_function_without_parens() {
        let code = r#"decir "Hola mundo""#;
        let result = execute_vader_code(code).unwrap();
        println!("🔍 Sin paréntesis: {:?}", result);
        
        match result {
            VaderValue::String(s) => assert_eq!(s, "Hola mundo"),
            _ => panic!("Expected string result, got: {:?}", result),
        }
    }

    #[test]
    fn test_parse_tokens_with_parens() {
        let code = r#"decir("Hola mundo")"#;
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize().unwrap();
        
        println!("🔍 Tokens con paréntesis:");
        for (i, token) in tokens.iter().enumerate() {
            println!("  {}: {:?}", i, token);
        }
        
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        
        println!("🔍 AST con paréntesis:");
        for (i, node) in ast.iter().enumerate() {
            println!("  {}: {:?}", i, node);
        }
    }

    #[test]
    fn test_parse_tokens_without_parens() {
        let code = r#"decir "Hola mundo""#;
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize().unwrap();
        
        println!("🔍 Tokens sin paréntesis:");
        for (i, token) in tokens.iter().enumerate() {
            println!("  {}: {:?}", i, token);
        }
        
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        
        println!("🔍 AST sin paréntesis:");
        for (i, node) in ast.iter().enumerate() {
            println!("  {}: {:?}", i, node);
        }
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
