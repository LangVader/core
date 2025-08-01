use vader::{VaderLexer, VaderParser, VaderInterpreter, VaderValue};

#[cfg(test)]
mod runtime_tests {
    use super::*;

    #[test]
    fn test_basic_arithmetic() {
        let code = "2 + 3 * 4";
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Number(n) => assert_eq!(n, 14.0),
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_string_operations() {
        let code = r#"decir "Hola " + "mundo""#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::String(s) => assert_eq!(s, "Hola mundo"),
            _ => panic!("Expected string result"),
        }
    }

    #[test]
    fn test_variable_assignment() {
        let code = r#"
        x = 10
        y = 20
        x + y
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Number(n) => assert_eq!(n, 30.0),
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_conditional_logic() {
        let code = r#"
        x = 15
        si x > 10:
            "mayor"
        sino:
            "menor"
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::String(s) => assert_eq!(s, "mayor"),
            _ => panic!("Expected string result"),
        }
    }

    #[test]
    fn test_function_definition() {
        let code = r#"
        funcion suma(a, b):
            retornar a + b
        
        suma(5, 7)
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Number(n) => assert_eq!(n, 12.0),
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_while_loop() {
        let code = r#"
        contador = 0
        suma = 0
        mientras contador < 5:
            suma = suma + contador
            contador = contador + 1
        suma
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Number(n) => assert_eq!(n, 10.0), // 0+1+2+3+4 = 10
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_boolean_operations() {
        let code = r#"
        a = verdadero
        b = falso
        a y no b
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Boolean(b) => assert!(b),
            _ => panic!("Expected boolean result"),
        }
    }

    #[test]
    fn test_comparison_operators() {
        let code = r#"
        x = 10
        y = 5
        (x > y) y (x != y)
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Boolean(b) => assert!(b),
            _ => panic!("Expected boolean result"),
        }
    }

    #[test]
    fn test_nested_expressions() {
        let code = r#"
        x = 2
        y = 3
        z = 4
        (x + y) * z - 1
        "#;
        let result = execute_vader_code(code).unwrap();
        
        match result {
            VaderValue::Number(n) => assert_eq!(n, 19.0), // (2+3)*4-1 = 19
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_error_handling() {
        let code = "x + y"; // Variables no definidas
        let result = execute_vader_code(code);
        
        assert!(result.is_err(), "Should fail with undefined variables");
    }

    // Función auxiliar para ejecutar código Vader
    fn execute_vader_code(code: &str) -> Result<VaderValue, Box<dyn std::error::Error>> {
        // Tokenizar
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize()?;
        
        // Parsear
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse()?;
        
        // Interpretar
        let mut interpreter = VaderInterpreter::new();
        let result = interpreter.execute(ast)?;
        
        Ok(result)
    }
}

#[cfg(test)]
mod performance_tests {
    use super::*;
    use std::time::Instant;

    #[test]
    fn test_arithmetic_performance() {
        let code = "1 + 2 * 3 - 4 / 2";
        let start = Instant::now();
        
        for _ in 0..1000 {
            let _ = execute_vader_code(code).unwrap();
        }
        
        let duration = start.elapsed();
        println!("🚀 1000 operaciones aritméticas: {:?}", duration);
        
        // Debe ser menor a 100ms para 1000 operaciones
        assert!(duration.as_millis() < 100, "Performance too slow: {:?}", duration);
    }

    #[test]
    fn test_string_performance() {
        let code = r#""Hola" + " " + "mundo" + "!""#;
        let start = Instant::now();
        
        for _ in 0..1000 {
            let _ = execute_vader_code(code).unwrap();
        }
        
        let duration = start.elapsed();
        println!("🚀 1000 operaciones de string: {:?}", duration);
        
        // Debe ser menor a 200ms para 1000 operaciones
        assert!(duration.as_millis() < 200, "String performance too slow: {:?}", duration);
    }

    #[test]
    fn test_complex_expression_performance() {
        let code = r#"
        x = 10
        y = 20
        z = 30
        resultado = (x + y) * z - (x * y) + z / x
        resultado
        "#;
        let start = Instant::now();
        
        for _ in 0..500 {
            let _ = execute_vader_code(code).unwrap();
        }
        
        let duration = start.elapsed();
        println!("🚀 500 expresiones complejas: {:?}", duration);
        
        // Debe ser menor a 300ms para 500 operaciones
        assert!(duration.as_millis() < 300, "Complex expression performance too slow: {:?}", duration);
    }

    // Función auxiliar reutilizada
    fn execute_vader_code(code: &str) -> Result<VaderValue, Box<dyn std::error::Error>> {
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize()?;
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse()?;
        let mut interpreter = VaderInterpreter::new();
        let result = interpreter.execute(ast)?;
        Ok(result)
    }
}

#[cfg(test)]
mod stress_tests {
    use super::*;
    use std::time::Instant;

    #[test]
    fn test_deep_recursion_simulation() {
        // Simular recursión profunda con loops
        let code = r#"
        contador = 0
        resultado = 1
        mientras contador < 100:
            resultado = resultado + contador
            contador = contador + 1
        resultado
        "#;
        
        let start = Instant::now();
        let result = execute_vader_code(code).unwrap();
        let duration = start.elapsed();
        
        println!("🚀 Recursión profunda simulada: {:?}", duration);
        
        match result {
            VaderValue::Number(n) => {
                // Suma de 0 a 99 = 99*100/2 = 4950, más 1 inicial = 4951
                assert_eq!(n, 4951.0);
            },
            _ => panic!("Expected number result"),
        }
    }

    #[test]
    fn test_large_string_concatenation() {
        let code = r#"
        resultado = ""
        contador = 0
        mientras contador < 50:
            resultado = resultado + "test"
            contador = contador + 1
        resultado
        "#;
        
        let start = Instant::now();
        let result = execute_vader_code(code).unwrap();
        let duration = start.elapsed();
        
        println!("🚀 Concatenación masiva de strings: {:?}", duration);
        
        match result {
            VaderValue::String(s) => {
                assert_eq!(s.len(), 200); // "test" * 50 = 200 caracteres
            },
            _ => panic!("Expected string result"),
        }
        
        // No debe tomar más de 500ms
        assert!(duration.as_millis() < 500, "String concatenation too slow: {:?}", duration);
    }

    #[test]
    fn test_memory_intensive_operations() {
        // Test con muchas variables
        let code = r#"
        a1 = 1; a2 = 2; a3 = 3; a4 = 4; a5 = 5
        b1 = 10; b2 = 20; b3 = 30; b4 = 40; b5 = 50
        c1 = 100; c2 = 200; c3 = 300; c4 = 400; c5 = 500
        
        resultado = a1 + a2 + a3 + a4 + a5 + 
                   b1 + b2 + b3 + b4 + b5 + 
                   c1 + c2 + c3 + c4 + c5
        resultado
        "#;
        
        let start = Instant::now();
        let result = execute_vader_code(code).unwrap();
        let duration = start.elapsed();
        
        println!("🚀 Operaciones intensivas en memoria: {:?}", duration);
        
        match result {
            VaderValue::Number(n) => {
                // 15 + 150 + 1500 = 1665
                assert_eq!(n, 1665.0);
            },
            _ => panic!("Expected number result"),
        }
    }

    // Función auxiliar reutilizada
    fn execute_vader_code(code: &str) -> Result<VaderValue, Box<dyn std::error::Error>> {
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize()?;
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse()?;
        let mut interpreter = VaderInterpreter::new();
        let result = interpreter.execute(ast)?;
        Ok(result)
    }
}
