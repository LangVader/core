/*!
🔍 VADER PARSER NATIVO - VERSIÓN LIMPIA
=====================================

Parser nativo completamente refactorizado para usar la nueva estructura
Token/TokenType del lexer.

Autor: Adriano & Cascade AI
*/

use crate::lexer::{Token, TokenType, LexError};
use crate::types::VaderValue;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("Token inesperado: {0}")]
    UnexpectedToken(Token),
    
    #[error("Fin de archivo inesperado")]
    UnexpectedEof,
    
    #[error("Expresión inválida")]
    InvalidExpression,
    
    #[error("Error de lexer: {0}")]
    LexError(#[from] LexError),
}

#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
pub enum AstNode {
    // Literales
    Literal { value: VaderValue },
    
    // Variables
    Variable { name: String },
    
    // Operaciones binarias
    BinaryOp {
        left: Box<AstNode>,
        operator: String,
        right: Box<AstNode>,
    },
    
    // Operaciones unarias
    UnaryOp {
        operator: String,
        operand: Box<AstNode>,
    },
    
    // Asignación
    Assignment {
        name: String,
        value: Box<AstNode>,
    },
    
    // Llamadas a función
    FunctionCall {
        name: String,
        args: Vec<AstNode>,
    },
    
    // Definición de función
    FunctionDef {
        name: String,
        params: Vec<String>,
        body: Vec<AstNode>,
    },
    
    // Control de flujo
    If {
        condition: Box<AstNode>,
        then_branch: Vec<AstNode>,
        else_branch: Option<Vec<AstNode>>,
    },
    
    While {
        condition: Box<AstNode>,
        body: Vec<AstNode>,
    },
    
    For {
        variable: String,
        iterable: Box<AstNode>,
        body: Vec<AstNode>,
    },
    
    // Estructuras de datos
    List { elements: Vec<AstNode> },
    
    Dict { pairs: Vec<(AstNode, AstNode)> },
    
    // Indexación
    Index {
        object: Box<AstNode>,
        index: Box<AstNode>,
    },
    
    // Acceso a miembro
    MemberAccess {
        object: Box<AstNode>,
        member: String,
    },
    
    // Return
    Return { value: Option<Box<AstNode>> },
    
    // Bloque
    Block { statements: Vec<AstNode> },
}

pub struct VaderParser {
    tokens: Vec<Token>,
    current: usize,
}

impl VaderParser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, current: 0 }
    }
    
    pub fn parse(&mut self) -> Result<Vec<AstNode>, ParseError> {
        let mut statements = Vec::new();
        
        while !self.is_at_end() {
            // Saltar tokens de nueva línea
            if let TokenType::Newline = self.current_token().token_type {
                self.advance();
                continue;
            }
            
            statements.push(self.parse_statement()?);
        }
        
        Ok(statements)
    }
    
    fn parse_statement(&mut self) -> Result<AstNode, ParseError> {
        match &self.current_token().token_type {
            TokenType::Keyword(keyword) => {
                match keyword.as_str() {
                    "decir" | "print" => self.parse_print(),
                    "si" | "if" => self.parse_if(),
                    "mientras" | "while" => self.parse_while(),
                    "para" | "for" => self.parse_for(),
                    "funcion" | "function" => self.parse_function_def(),
                    "retornar" | "return" => self.parse_return(),
                    _ => self.parse_expression_statement(),
                }
            }
            TokenType::Identifier(_) => {
                // Puede ser asignación o expresión
                if self.peek_token_type(1) == Some(&TokenType::Assign) {
                    self.parse_assignment()
                } else {
                    self.parse_expression_statement()
                }
            }
            _ => self.parse_expression_statement(),
        }
    }
    
    fn parse_print(&mut self) -> Result<AstNode, ParseError> {
        let function_name = match &self.current_token().token_type {
            TokenType::Keyword(keyword) => keyword.clone(),
            _ => "print".to_string(),
        };
        
        self.advance(); // consume 'decir' o 'print'
        let args = vec![self.parse_expression()?];
        Ok(AstNode::FunctionCall {
            name: function_name,
            args,
        })
    }
    
    fn parse_if(&mut self) -> Result<AstNode, ParseError> {
        self.advance(); // consume 'si' o 'if'
        let condition = self.parse_expression()?;
        
        // Consumir ':' si está presente
        if let TokenType::Colon = self.current_token().token_type {
            self.advance();
        }
        
        // Usar parse_block para manejar múltiples statements
        let then_branch = self.parse_block()?;
        
        let else_branch = if self.match_keyword("sino") || self.match_keyword("else") {
            // Consumir ':' si está presente
            if let TokenType::Colon = self.current_token().token_type {
                self.advance();
            }
            Some(self.parse_block()?)
        } else {
            None
        };
        
        Ok(AstNode::If {
            condition: Box::new(condition),
            then_branch,
            else_branch,
        })
    }
    
    fn parse_while(&mut self) -> Result<AstNode, ParseError> {
        self.advance(); // consume 'mientras' o 'while'
        let condition = self.parse_expression()?;
        
        // Consumir ':' si está presente
        if let TokenType::Colon = self.current_token().token_type {
            self.advance();
        }
        
        // Usar parse_block para manejar múltiples statements
        let body = self.parse_block()?;
        
        Ok(AstNode::While {
            condition: Box::new(condition),
            body,
        })
    }
    
    fn parse_for(&mut self) -> Result<AstNode, ParseError> {
        self.advance(); // consume 'para' o 'for'
        
        let variable = if let TokenType::Identifier(name) = &self.current_token().token_type {
            let name = name.clone();
            self.advance();
            name
        } else {
            return Err(ParseError::UnexpectedToken(self.current_token().clone()));
        };
        
        // Consume 'en' o 'in'
        if !self.match_keyword("en") && !self.match_keyword("in") {
            return Err(ParseError::UnexpectedToken(self.current_token().clone()));
        }
        
        let iterable = self.parse_expression()?;
        let body = vec![self.parse_statement()?];
        
        Ok(AstNode::For {
            variable,
            iterable: Box::new(iterable),
            body,
        })
    }
    
    fn parse_function_def(&mut self) -> Result<AstNode, ParseError> {
        self.advance(); // consume 'funcion' o 'function'
        
        let name = if let TokenType::Identifier(name) = &self.current_token().token_type {
            let name = name.clone();
            self.advance();
            name
        } else {
            return Err(ParseError::UnexpectedToken(self.current_token().clone()));
        };
        
        self.expect_token_type(&TokenType::LeftParen)?;
        
        let mut params = Vec::new();
        if !matches!(self.current_token().token_type, TokenType::RightParen) {
            loop {
                if let TokenType::Identifier(param) = &self.current_token().token_type {
                    params.push(param.clone());
                    self.advance();
                } else {
                    return Err(ParseError::UnexpectedToken(self.current_token().clone()));
                }
                
                if matches!(self.current_token().token_type, TokenType::Comma) {
                    self.advance();
                } else {
                    break;
                }
            }
        }
        
        self.expect_token_type(&TokenType::RightParen)?;
        
        // Consumir ':' si está presente
        if let TokenType::Colon = self.current_token().token_type {
            self.advance();
        }
        
        // Usar parse_block para manejar múltiples statements
        let body = self.parse_block()?;
        
        Ok(AstNode::FunctionDef { name, params, body })
    }
    
    fn parse_return(&mut self) -> Result<AstNode, ParseError> {
        self.advance(); // consume 'retornar' o 'return'
        
        let value = if self.is_at_end() || matches!(self.current_token().token_type, TokenType::Newline) {
            None
        } else {
            Some(Box::new(self.parse_expression()?))
        };
        
        Ok(AstNode::Return { value })
    }
    
    fn parse_assignment(&mut self) -> Result<AstNode, ParseError> {
        let name = if let TokenType::Identifier(name) = &self.current_token().token_type {
            let name = name.clone();
            self.advance();
            name
        } else {
            return Err(ParseError::UnexpectedToken(self.current_token().clone()));
        };
        
        self.expect_token_type(&TokenType::Assign)?;
        let value = self.parse_expression()?;
        
        Ok(AstNode::Assignment {
            name,
            value: Box::new(value),
        })
    }
    
    fn parse_expression_statement(&mut self) -> Result<AstNode, ParseError> {
        self.parse_expression()
    }
    
    fn parse_expression(&mut self) -> Result<AstNode, ParseError> {
        self.parse_logical_or()
    }
    
    fn parse_logical_or(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_logical_and()?;
        
        while self.match_token_type(&TokenType::Or) {
            let operator = "o".to_string();
            let right = self.parse_logical_and()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_logical_and(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_equality()?;
        
        while self.match_token_type(&TokenType::And) {
            let operator = "y".to_string();
            let right = self.parse_equality()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_equality(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_comparison()?;
        
        while matches!(self.current_token().token_type, TokenType::Equal | TokenType::NotEqual) {
            let operator = match &self.current_token().token_type {
                TokenType::Equal => "==",
                TokenType::NotEqual => "!=",
                _ => unreachable!(),
            }.to_string();
            self.advance();
            let right = self.parse_comparison()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_comparison(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_term()?;
        
        while matches!(self.current_token().token_type, 
                      TokenType::Greater | TokenType::GreaterEqual | 
                      TokenType::Less | TokenType::LessEqual) {
            let operator = match &self.current_token().token_type {
                TokenType::Greater => ">",
                TokenType::GreaterEqual => ">=",
                TokenType::Less => "<",
                TokenType::LessEqual => "<=",
                _ => unreachable!(),
            }.to_string();
            self.advance();
            let right = self.parse_term()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_term(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_factor()?;
        
        while matches!(self.current_token().token_type, TokenType::Plus | TokenType::Minus) {
            let operator = match &self.current_token().token_type {
                TokenType::Plus => "+",
                TokenType::Minus => "-",
                _ => unreachable!(),
            }.to_string();
            self.advance();
            let right = self.parse_factor()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_factor(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_unary()?;
        
        while matches!(self.current_token().token_type, 
                      TokenType::Multiply | TokenType::Divide | TokenType::Modulo) {
            let operator = match &self.current_token().token_type {
                TokenType::Multiply => "*",
                TokenType::Divide => "/",
                TokenType::Modulo => "%",
                _ => unreachable!(),
            }.to_string();
            self.advance();
            let right = self.parse_unary()?;
            expr = AstNode::BinaryOp {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_unary(&mut self) -> Result<AstNode, ParseError> {
        if matches!(self.current_token().token_type, TokenType::Not | TokenType::Minus) {
            let operator = match &self.current_token().token_type {
                TokenType::Not => "not",
                TokenType::Minus => "-",
                _ => unreachable!(),
            }.to_string();
            self.advance();
            let operand = self.parse_unary()?;
            return Ok(AstNode::UnaryOp {
                operator,
                operand: Box::new(operand),
            });
        }
        
        self.parse_primary()
    }
    
    fn parse_primary(&mut self) -> Result<AstNode, ParseError> {
        match &self.current_token().token_type {
            TokenType::Number(n) => {
                let value = *n;
                self.advance();
                Ok(AstNode::Literal { value: VaderValue::Number(value) })
            }
            TokenType::String(s) => {
                let value = s.clone();
                self.advance();
                Ok(AstNode::Literal { value: VaderValue::String(value) })
            }
            TokenType::Boolean(b) => {
                let value = *b;
                self.advance();
                Ok(AstNode::Literal { value: VaderValue::Boolean(value) })
            }
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                
                // Verificar si es una llamada a función
                if matches!(self.current_token().token_type, TokenType::LeftParen) {
                    self.advance(); // consume '('
                    let mut args = Vec::new();
                    
                    if !matches!(self.current_token().token_type, TokenType::RightParen) {
                        loop {
                            args.push(self.parse_expression()?);
                            if matches!(self.current_token().token_type, TokenType::Comma) {
                                self.advance();
                            } else {
                                break;
                            }
                        }
                    }
                    
                    self.expect_token_type(&TokenType::RightParen)?;
                    Ok(AstNode::FunctionCall { name, args })
                } else {
                    Ok(AstNode::Variable { name })
                }
            }
            TokenType::LeftParen => {
                self.advance(); // consume '('
                let expr = self.parse_expression()?;
                self.expect_token_type(&TokenType::RightParen)?;
                Ok(expr)
            }
            TokenType::LeftBracket => {
                self.advance(); // consume '['
                let mut elements = Vec::new();
                
                if !matches!(self.current_token().token_type, TokenType::RightBracket) {
                    loop {
                        elements.push(self.parse_expression()?);
                        if matches!(self.current_token().token_type, TokenType::Comma) {
                            self.advance();
                        } else {
                            break;
                        }
                    }
                }
                
                self.expect_token_type(&TokenType::RightBracket)?;
                Ok(AstNode::List { elements })
            }
            _ => Err(ParseError::UnexpectedToken(self.current_token().clone())),
        }
    }
    
    // Métodos auxiliares
    fn current_token(&self) -> Token {
        self.tokens.get(self.current).cloned().unwrap_or(Token {
            token_type: TokenType::Eof,
            lexeme: "".to_string(),
            line: 0,
            column: 0,
        })
    }
    
    fn peek_token_type(&self, offset: usize) -> Option<&TokenType> {
        self.tokens.get(self.current + offset).map(|t| &t.token_type)
    }
    
    fn advance(&mut self) {
        if !self.is_at_end() {
            self.current += 1;
        }
    }
    
    fn is_at_end(&self) -> bool {
        matches!(self.current_token().token_type, TokenType::Eof) || self.current >= self.tokens.len()
    }
    
    fn match_token_type(&mut self, token_type: &TokenType) -> bool {
        if std::mem::discriminant(&self.current_token().token_type) == std::mem::discriminant(token_type) {
            self.advance();
            true
        } else {
            false
        }
    }
    
    fn match_keyword(&mut self, keyword: &str) -> bool {
        if let TokenType::Keyword(k) = &self.current_token().token_type {
            if k == keyword {
                self.advance();
                return true;
            }
        }
        false
    }
    
    /// Consume todas las nuevas líneas consecutivas
    fn skip_newlines(&mut self) {
        while matches!(self.current_token().token_type, TokenType::Newline) {
            self.advance();
        }
    }
    
    /// Parsear un bloque de statements, manejando nuevas líneas
    fn parse_block(&mut self) -> Result<Vec<AstNode>, ParseError> {
        let mut statements = Vec::new();
        
        // Saltear nuevas líneas iniciales
        self.skip_newlines();
        
        // Parsear al menos un statement
        if !self.is_at_end() && !self.is_block_terminator() {
            statements.push(self.parse_statement()?);
        }
        
        // Parsear statements adicionales si hay
        while !self.is_at_end() && !self.is_block_terminator() {
            self.skip_newlines();
            if self.is_at_end() || self.is_block_terminator() {
                break;
            }
            statements.push(self.parse_statement()?);
        }
        
        Ok(statements)
    }
    
    /// Verificar si el token actual es un terminador de bloque
    fn is_block_terminator(&self) -> bool {
        match &self.current_token().token_type {
            TokenType::Keyword(keyword) => {
                matches!(keyword.as_str(), "sino" | "else" | "fin" | "end" | "funcion" | "function")
            }
            // Si encontramos un identificador después de newlines, podría ser el fin del bloque de función
            TokenType::Identifier(_) => {
                // Verificar si estamos en una nueva línea sin indentación (nivel base)
                // Por simplicidad, asumimos que cualquier identificador después de newlines
                // que no sea una keyword termina el bloque de función
                true
            }
            _ => false,
        }
    }
    
    fn expect_token_type(&mut self, expected: &TokenType) -> Result<(), ParseError> {
        if std::mem::discriminant(&self.current_token().token_type) == std::mem::discriminant(expected) {
            self.advance();
            Ok(())
        } else {
            Err(ParseError::UnexpectedToken(self.current_token().clone()))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::VaderLexer;
    
    #[test]
    fn test_parse_simple_expression() {
        let mut lexer = VaderLexer::new("2 + 3");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        
        assert_eq!(ast.len(), 1);
        // Más tests aquí...
    }
}
