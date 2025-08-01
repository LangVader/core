use std::fmt;
use thiserror::Error;

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Literales
    Number(f64),
    String(String),
    Boolean(bool),
    Identifier(String),
    Keyword(String),
    
    // Operadores aritméticos
    Plus,
    Minus,
    Multiply,
    Divide,
    Modulo,
    Power,
    
    // Operadores de asignación
    Assign,
    PlusAssign,
    MinusAssign,
    
    // Operadores de comparación
    Equal,
    NotEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    
    // Operadores lógicos
    And,
    Or,
    Not,
    Bang, // Para el operador !
    
    // Delimitadores
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    LeftBrace,
    RightBrace,
    
    // Puntuación
    Comma,
    Dot,
    Colon,
    Semicolon,
    Arrow,
    
    // Control de flujo
    Newline,
    Indent,
    Dedent,
    Eof,
    
    // Comentarios
    Comment(String),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub token_type: TokenType,
    pub lexeme: String,
    pub line: usize,
    pub column: usize,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} at {}:{}", self.lexeme, self.line, self.column)
    }
}

#[derive(Error, Debug)]
pub enum LexError {
    #[error("Carácter inesperado: '{0}' en posición {1}")]
    UnexpectedChar(char, usize),
    
    #[error("String sin cerrar en posición {0}")]
    UnterminatedString(usize),
    
    #[error("Número inválido: '{0}'")]
    InvalidNumber(String),
    
    #[error("Comentario sin cerrar en posición {0}")]
    UnterminatedComment(usize),
}

pub struct VaderLexer {
    input: Vec<char>,
    position: usize,
    current_char: Option<char>,
    line: usize,
    column: usize,
    indent_stack: Vec<usize>,
}

impl VaderLexer {
    pub fn new(input: &str) -> Self {
        let chars: Vec<char> = input.chars().collect();
        let current_char = chars.get(0).copied();
        
        Self {
            input: chars,
            position: 0,
            current_char,
            line: 1,
            column: 1,
            indent_stack: vec![0],
        }
    }
    
    pub fn tokenize(&mut self) -> Result<Vec<Token>, LexError> {
        let mut tokens = Vec::new();
        
        while let Some(token) = self.next_token()? {
            if !matches!(token.token_type, TokenType::Comment(_)) {
                tokens.push(token);
            }
        }
        
        // Añadir dedents finales
        while self.indent_stack.len() > 1 {
            self.indent_stack.pop();
            tokens.push(Token {
                token_type: TokenType::Dedent,
                lexeme: "".to_string(),
                line: self.line,
                column: self.column,
            });
        }
        
        tokens.push(Token {
            token_type: TokenType::Eof,
            lexeme: "".to_string(),
            line: self.line,
            column: self.column,
        });
        
        Ok(tokens)
    }
    
    fn next_token(&mut self) -> Result<Option<Token>, LexError> {
        self.skip_whitespace();
        
        if self.current_char.is_none() {
            return Ok(None);
        }
        
        let start_line = self.line;
        let start_column = self.column;
        
        match self.current_char.unwrap() {
            // Números
            c if c.is_ascii_digit() => {
                let number = self.read_number()?;
                Ok(Some(Token {
                    token_type: TokenType::Number(number),
                    lexeme: number.to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            // Strings
            '"' => {
                let string = self.read_string()?;
                Ok(Some(Token {
                    token_type: TokenType::String(string.clone()),
                    lexeme: format!("\"{}\"", string),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            // Identificadores y keywords
            c if c.is_alphabetic() || c == '_' => {
                let word = self.read_identifier();
                let token_type = self.keyword_or_identifier(word.clone());
                Ok(Some(Token {
                    token_type,
                    lexeme: word,
                    line: start_line,
                    column: start_column,
                }))
            }
            
            // Operadores y delimitadores
            '+' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::PlusAssign,
                        lexeme: "+=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Plus,
                        lexeme: "+".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '-' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::MinusAssign,
                        lexeme: "-=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else if self.current_char == Some('>') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::Arrow,
                        lexeme: "->".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Minus,
                        lexeme: "-".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '*' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Multiply,
                    lexeme: "*".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            '/' => {
                self.advance();
                if self.current_char == Some('/') {
                    let comment = self.read_comment();
                    Ok(Some(Token {
                        token_type: TokenType::Comment(comment.clone()),
                        lexeme: format!("//{}", comment),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Divide,
                        lexeme: "/".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '=' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::Equal,
                        lexeme: "==".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Assign,
                        lexeme: "=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '<' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::LessEqual,
                        lexeme: "<=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Less,
                        lexeme: "<".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '>' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::GreaterEqual,
                        lexeme: ">=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Greater,
                        lexeme: ">".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            '!' => {
                self.advance();
                if self.current_char == Some('=') {
                    self.advance();
                    Ok(Some(Token {
                        token_type: TokenType::NotEqual,
                        lexeme: "!=".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                } else {
                    Ok(Some(Token {
                        token_type: TokenType::Bang,
                        lexeme: "!".to_string(),
                        line: start_line,
                        column: start_column,
                    }))
                }
            }
            
            ',' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Comma,
                    lexeme: ",".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            ';' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Semicolon,
                    lexeme: ";".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            ':' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Colon,
                    lexeme: ":".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            '(' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::LeftParen,
                    lexeme: "(".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            ')' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::RightParen,
                    lexeme: ")".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            '\n' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Newline,
                    lexeme: "\\n".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            c => Err(LexError::UnexpectedChar(c, self.position)),
        }
    }
    
    fn advance(&mut self) {
        if let Some('\n') = self.current_char {
            self.line += 1;
            self.column = 1;
        } else {
            self.column += 1;
        }
        
        self.position += 1;
        self.current_char = self.input.get(self.position).copied();
    }
    
    fn skip_whitespace(&mut self) {
        while let Some(ch) = self.current_char {
            if ch.is_whitespace() && ch != '\n' {
                self.advance();
            } else {
                break;
            }
        }
    }
    
    fn read_number(&mut self) -> Result<f64, LexError> {
        let mut number_str = String::new();
        
        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() || ch == '.' {
                number_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        number_str.parse::<f64>()
            .map_err(|_| LexError::InvalidNumber(number_str))
    }
    
    fn read_string(&mut self) -> Result<String, LexError> {
        self.advance(); // Skip opening quote
        
        let mut string = String::new();
        
        while let Some(ch) = self.current_char {
            if ch == '"' {
                self.advance(); // Skip closing quote
                return Ok(string);
            } else if ch == '\\' {
                self.advance();
                match self.current_char {
                    Some('n') => string.push('\n'),
                    Some('t') => string.push('\t'),
                    Some('r') => string.push('\r'),
                    Some('\\') => string.push('\\'),
                    Some('"') => string.push('"'),
                    Some(c) => string.push(c),
                    None => return Err(LexError::UnterminatedString(self.position)),
                }
                self.advance();
            } else {
                string.push(ch);
                self.advance();
            }
        }
        
        Err(LexError::UnterminatedString(self.position))
    }
    
    fn read_identifier(&mut self) -> String {
        let mut identifier = String::new();
        
        while let Some(ch) = self.current_char {
            if ch.is_alphanumeric() || ch == '_' {
                identifier.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        identifier
    }
    
    fn read_comment(&mut self) -> String {
        self.advance(); // Skip second '/'
        
        let mut comment = String::new();
        
        while let Some(ch) = self.current_char {
            if ch == '\n' {
                break;
            }
            comment.push(ch);
            self.advance();
        }
        
        comment.trim().to_string()
    }
    
    /// Detecta si una palabra es un operador lógico o una variable basándose en el contexto
    fn detect_logical_operator_context(&self, word: &str) -> TokenType {
        // Análisis contextual mejorado: mirar caracteres anteriores y siguientes
        let next_char = self.current_char;
        
        // Si el siguiente carácter es '=', definitivamente es una variable (asignación)
        if next_char == Some('=') || (next_char == Some(' ') && self.peek_next_non_space() == Some('=')) {
            return TokenType::Identifier(word.to_string());
        }
        
        // Mirar el contexto anterior más amplio
        let prev_char = if self.position > word.len() {
            self.input.get(self.position - word.len() - 1).copied()
        } else {
            None
        };
        
        // Mirar varios caracteres anteriores para mejor contexto
        let mut prev_context = String::new();
        if self.position >= word.len() + 3 {
            for i in (self.position - word.len() - 3)..(self.position - word.len()) {
                if let Some(ch) = self.input.get(i) {
                    prev_context.push(*ch);
                }
            }
        }
        
        // Mirar siguiente carácter no-espacio
        let next_non_space = self.peek_next_non_space();
        
        // Casos donde definitivamente es operador lógico:
        // 1. Después de ')' y antes de '('
        // 2. Entre expresiones (después de ')' y antes de identificador)
        // 3. Entre espacios en contexto de expresión
        match (prev_char, next_char, next_non_space) {
            // Después de ')' -> definitivamente operador lógico
            (Some(')'), Some(' '), _) => {
                match word {
                    "y" => TokenType::And,
                    "o" => TokenType::Or,
                    _ => TokenType::Identifier(word.to_string()),
                }
            }
            // Entre espacios y el contexto anterior contiene ')' -> operador lógico
            (Some(' '), Some(' '), _) if prev_context.contains(')') => {
                match word {
                    "y" => TokenType::And,
                    "o" => TokenType::Or,
                    _ => TokenType::Identifier(word.to_string()),
                }
            }
            // Antes de '(' -> operador lógico
            (Some(' '), Some(' '), Some('(')) => {
                match word {
                    "y" => TokenType::And,
                    "o" => TokenType::Or,
                    _ => TokenType::Identifier(word.to_string()),
                }
            }
            // En otros contextos, tratar como variable por defecto
            _ => TokenType::Identifier(word.to_string())
        }
    }
    
    /// Función auxiliar para mirar el siguiente carácter no-espacio
    fn peek_next_non_space(&self) -> Option<char> {
        let mut pos = self.position;
        while pos < self.input.len() {
            let ch = self.input[pos];
            if ch != ' ' && ch != '\t' {
                return Some(ch);
            }
            pos += 1;
        }
        None
    }
    
    fn keyword_or_identifier(&self, word: String) -> TokenType {
        match word.as_str() {
            "si" => TokenType::Keyword("si".to_string()),
            "sino" => TokenType::Keyword("sino".to_string()),
            "mientras" => TokenType::Keyword("mientras".to_string()),
            "para" => TokenType::Keyword("para".to_string()),
            "en" => TokenType::Keyword("en".to_string()),
            "funcion" => TokenType::Keyword("funcion".to_string()),
            "clase" => TokenType::Keyword("clase".to_string()),
            "retornar" => TokenType::Keyword("retornar".to_string()),
            "verdadero" => TokenType::Boolean(true),
            "falso" => TokenType::Boolean(false),
            // Operadores lógicos con detección contextual
            "y" => self.detect_logical_operator_context("y"),
            "o" => self.detect_logical_operator_context("o"),
            "no" => TokenType::Not,
            "decir" => TokenType::Keyword("decir".to_string()),
            
            // Keywords en inglés
            "print" => TokenType::Keyword("print".to_string()),
            "if" => TokenType::Keyword("if".to_string()),
            "else" => TokenType::Keyword("else".to_string()),
            "while" => TokenType::Keyword("while".to_string()),
            "for" => TokenType::Keyword("for".to_string()),
            "function" => TokenType::Keyword("function".to_string()),
            "class" => TokenType::Keyword("class".to_string()),
            "return" => TokenType::Keyword("return".to_string()),
            "true" => TokenType::Boolean(true),
            "false" => TokenType::Boolean(false),
            "and" => TokenType::And,
            "or" => TokenType::Or,
            "not" => TokenType::Not,
            
            // Identificador
            _ => TokenType::Identifier(word),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize_simple() {
        let mut lexer = VaderLexer::new("decir \"Hola mundo\"");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens.len(), 3); // decir, "Hola mundo", EOF
        assert!(matches!(tokens[0].token_type, TokenType::Keyword(_)));
        assert!(matches!(tokens[1].token_type, TokenType::String(_)));
        assert!(matches!(tokens[2].token_type, TokenType::Eof));
    }

    #[test]
    fn test_tokenize_numbers() {
        let mut lexer = VaderLexer::new("42 3.14");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens.len(), 3); // 42, 3.14, EOF
        assert!(matches!(tokens[0].token_type, TokenType::Number(42.0)));
        assert!(matches!(tokens[1].token_type, TokenType::Number(3.14)));
    }

    #[test]
    fn test_tokenize_operators() {
        let mut lexer = VaderLexer::new("+ - * / == +=");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens.len(), 7); // 6 operators + EOF
        assert!(matches!(tokens[0].token_type, TokenType::Plus));
        assert!(matches!(tokens[1].token_type, TokenType::Minus));
        assert!(matches!(tokens[2].token_type, TokenType::Multiply));
        assert!(matches!(tokens[3].token_type, TokenType::Divide));
        assert!(matches!(tokens[4].token_type, TokenType::Equal));
        assert!(matches!(tokens[5].token_type, TokenType::PlusAssign));
    }
}
