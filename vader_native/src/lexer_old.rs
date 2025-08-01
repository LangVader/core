/*!
🔤 VADER LEXER NATIVO - TOKENIZACIÓN REAL
=======================================

Lexer nativo que convierte código Vader en tokens.
Soporta toda la sintaxis ultra-natural de Vader.

Autor: Adriano & Cascade AI
*/

use std::fmt;
use thiserror::Error;

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Literales
    Number(f64),
    String(String),
    Boolean(bool),
    
    // Identificadores y palabras clave
    Identifier(String),
    Keyword(String),
    
    // Operadores
    Plus,
    Minus,
    Multiply,
    Divide,
    Modulo,
    Power,
    
    // Comparación
    Equal,
    NotEqual,
    Less,
    Greater,
    LessEqual,
    GreaterEqual,
    
    // Lógicos
    And,
    Or,
    Not,
    
    // Asignación
    Assign,
    PlusAssign,
    MinusAssign,
    
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
    
    // Especiales
    Newline,
    Indent,
    Dedent,
    Comment(String),
    
    // Control
    Eof,
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
    
    #[error("Número inválido: '{0}' en posición {1}")]
    InvalidNumber(String, usize),
    
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
                        lexeme: format!("//{}" , comment),
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
            
            '%' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Modulo,
                    lexeme: "%".to_string(),
                    line: start_line,
                    column: start_column,
                }))
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
                    Err(LexError::UnexpectedChar('!', self.position))
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
            
            '[' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::LeftBracket,
                    lexeme: "[".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            ']' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::RightBracket,
                    lexeme: "]".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            '{' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::LeftBrace,
                    lexeme: "{".to_string(),
                    line: start_line,
                    column: start_column,
                }))
            }
            
            '}' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::RightBrace,
                    lexeme: "}".to_string(),
                    line: start_line,
                    column: start_column,
                }))
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
            
            '.' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Dot,
                    lexeme: ".".to_string(),
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
            
            ';' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Semicolon,
                    lexeme: ";".to_string(),
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
    
    fn peek(&self) -> Option<char> {
        self.input.get(self.position + 1).copied()
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
        let quote_char = self.current_char.unwrap();
        self.advance(); // Skip opening quote
        
        let mut string = String::new();
        
        while let Some(ch) = self.current_char {
            if ch == quote_char {
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
                    Some('\'') => string.push('\''),
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
        self.advance(); // Skip first '/'
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
    
    fn keyword_or_identifier(&self, word: String) -> TokenType {
        match word.as_str() {
            // Keywords en español
            "decir" => TokenType::Keyword("decir".to_string()),
            "si" => TokenType::Keyword("si".to_string()),
            "sino" => TokenType::Keyword("sino".to_string()),
            "mientras" => TokenType::Keyword("mientras".to_string()),
            "para" => TokenType::Keyword("para".to_string()),
            "en" => TokenType::Keyword("en".to_string()),
            "funcion" => TokenType::Keyword("funcion".to_string()),
            "clase" => TokenType::Keyword("clase".to_string()),
            "retornar" => TokenType::Keyword("retornar".to_string()),
            "importar" => TokenType::Keyword("importar".to_string()),
            "desde" => TokenType::Keyword("desde".to_string()),
            "como" => TokenType::Keyword("como".to_string()),
            "verdadero" => TokenType::Boolean(true),
            "falso" => TokenType::Boolean(false),
            "nulo" => TokenType::Keyword("nulo".to_string()),
            "y" => TokenType::And,
            "o" => TokenType::Or,
            "no" => TokenType::Not,
            "es" => TokenType::Keyword("es".to_string()),
            
            // Keywords en inglés
            "print" => TokenType::Keyword("print".to_string()),
            "if" => TokenType::Keyword("if".to_string()),
            "else" => TokenType::Keyword("else".to_string()),
            "while" => TokenType::Keyword("while".to_string()),
            "for" => TokenType::Keyword("for".to_string()),
            "in" => TokenType::Keyword("in".to_string()),
            "function" => TokenType::Keyword("function".to_string()),
            "class" => TokenType::Keyword("class".to_string()),
            "return" => TokenType::Keyword("return".to_string()),
            "import" => TokenType::Keyword("import".to_string()),
            "from" => TokenType::Keyword("from".to_string()),
            "as" => TokenType::Keyword("as".to_string()),
            "true" => TokenType::Boolean(true),
            "false" => TokenType::Boolean(false),
            "and" => TokenType::And,
            "or" => TokenType::Or,
            "not" => TokenType::Not,
            "is" => TokenType::Keyword("is".to_string()),
            
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
        let mut lexer = VaderLexer::new("+ - * / == != <= >=");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens.len(), 9); // 8 operators + EOF
        assert!(matches!(tokens[0].token_type, TokenType::Plus));
        assert!(matches!(tokens[1].token_type, TokenType::Minus));
        assert!(matches!(tokens[2].token_type, TokenType::Multiply));
        assert!(matches!(tokens[3].token_type, TokenType::Divide));
        assert!(matches!(tokens[4].token_type, TokenType::Equal));
        assert!(matches!(tokens[5].token_type, TokenType::NotEqual));
        assert!(matches!(tokens[6].token_type, TokenType::LessEqual));
        assert!(matches!(tokens[7].token_type, TokenType::GreaterEqual));
    }
}
                    Some('\\') => string.push('\\'),
                    Some('"') => string.push('"'),
                    Some('\'') => string.push('\''),
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
    
    fn read_number(&mut self) -> Result<f64, LexError> {
        let mut number = String::new();
        
        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() || ch == '.' {
                number.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        number.parse::<f64>()
            .map_err(|_| LexError::InvalidNumber(number, self.position))
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
        let mut comment = String::new();
        self.advance(); // Skip #
        
        while let Some(ch) = self.current_char {
            if ch == '\n' {
                break;
            }
            comment.push(ch);
            self.advance();
        }
        
        comment.trim().to_string()
    }
    
    fn read_line_comment(&mut self) -> String {
        let mut comment = String::new();
        self.advance(); // Skip first /
        self.advance(); // Skip second /
        
        while let Some(ch) = self.current_char {
            if ch == '\n' {
                break;
            }
            comment.push(ch);
            self.advance();
        }
        
        comment.trim().to_string()
    }
    
    fn keyword_or_identifier(&self, word: String) -> TokenType {
        match word.as_str() {
            // Keywords en español
            "decir" => TokenType::Keyword("decir".to_string()),
            "si" => TokenType::Keyword("si".to_string()),
            "sino" => TokenType::Keyword("sino".to_string()),
            "mientras" => TokenType::Keyword("mientras".to_string()),
            "para" => TokenType::Keyword("para".to_string()),
            "en" => TokenType::Keyword("en".to_string()),
            "funcion" => TokenType::Keyword("funcion".to_string()),
            "clase" => TokenType::Keyword("clase".to_string()),
            "retornar" => TokenType::Keyword("retornar".to_string()),
            "importar" => TokenType::Keyword("importar".to_string()),
            "desde" => TokenType::Keyword("desde".to_string()),
            "como" => TokenType::Keyword("como".to_string()),
            "verdadero" => TokenType::Boolean(true),
            "falso" => TokenType::Boolean(false),
            "nulo" => TokenType::Keyword("nulo".to_string()),
            "y" => TokenType::And,
            "o" => TokenType::Or,
            "no" => TokenType::Not,
            "es" => TokenType::Keyword("es".to_string()),
            
            // Keywords en inglés
            "print" => TokenType::Keyword("print".to_string()),
            "if" => TokenType::Keyword("if".to_string()),
            "else" => TokenType::Keyword("else".to_string()),
            "while" => TokenType::Keyword("while".to_string()),
            "for" => TokenType::Keyword("for".to_string()),
            "in" => TokenType::Keyword("in".to_string()),
            "function" => TokenType::Keyword("function".to_string()),
            "class" => TokenType::Keyword("class".to_string()),
            "return" => TokenType::Keyword("return".to_string()),
            "import" => TokenType::Keyword("import".to_string()),
            "from" => TokenType::Keyword("from".to_string()),
            "as" => TokenType::Keyword("as".to_string()),
            "true" => TokenType::Boolean(true),
            "false" => TokenType::Boolean(false),
            "and" => TokenType::And,
            "or" => TokenType::Or,
            "not" => TokenType::Not,
            "is" => TokenType::Keyword("is".to_string()),
            
            // Identificador
            _ => TokenType::Identifier(word),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_basic_tokens() {
        let mut lexer = VaderLexer::new("decir \"Hola mundo\"");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens[0], Token::Decir);
        assert_eq!(tokens[1], Token::String("Hola mundo".to_string()));
    }
    
    #[test]
    fn test_numbers() {
        let mut lexer = VaderLexer::new("42 3.14");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens[0], Token::Number(42.0));
        assert_eq!(tokens[1], Token::Number(3.14));
    }
    
    #[test]
    fn test_operators() {
        let mut lexer = VaderLexer::new("+ - * / == != <= >=");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens[0], Token::Plus);
        assert_eq!(tokens[1], Token::Minus);
        assert_eq!(tokens[2], Token::Multiply);
        assert_eq!(tokens[3], Token::Divide);
        assert_eq!(tokens[4], Token::Equal);
        assert_eq!(tokens[5], Token::NotEqual);
        assert_eq!(tokens[6], Token::LessEqual);
        assert_eq!(tokens[7], Token::GreaterEqual);
    }
}
