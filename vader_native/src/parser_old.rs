/*!
🌳 VADER PARSER NATIVO - AST REAL
===============================

Parser nativo que convierte tokens en Abstract Syntax Tree.
Implementa toda la gramática de Vader con sintaxis ultra-natural.

Autor: Adriano & Cascade AI
*/

use crate::lexer::Token;
use crate::types::VaderValue;
use std::fmt;
use thiserror::Error;

#[derive(Debug, Clone, PartialEq)]
pub enum AstNode {
    // Programa completo
    Program {
        statements: Vec<AstNode>,
    },
    
    // Declaraciones
    FunctionDecl {
        name: String,
        params: Vec<String>,
        body: Box<AstNode>,
    },
    ClassDecl {
        name: String,
        methods: Vec<AstNode>,
    },
    
    // Statements
    ExpressionStmt {
        expr: Box<AstNode>,
    },
    PrintStmt {
        expr: Box<AstNode>,
    },
    AssignStmt {
        name: String,
        value: Box<AstNode>,
    },
    IfStmt {
        condition: Box<AstNode>,
        then_branch: Box<AstNode>,
        else_branch: Option<Box<AstNode>>,
    },
    WhileStmt {
        condition: Box<AstNode>,
        body: Box<AstNode>,
    },
    ForStmt {
        var: String,
        iterable: Box<AstNode>,
        body: Box<AstNode>,
    },
    ReturnStmt {
        value: Option<Box<AstNode>>,
    },
    Block {
        statements: Vec<AstNode>,
    },
    
    // Expresiones
    Binary {
        left: Box<AstNode>,
        operator: BinaryOp,
        right: Box<AstNode>,
    },
    Unary {
        operator: UnaryOp,
        operand: Box<AstNode>,
    },
    Call {
        callee: Box<AstNode>,
        args: Vec<AstNode>,
    },
    Variable {
        name: String,
    },
    Literal {
        value: VaderValue,
    },
    List {
        elements: Vec<AstNode>,
    },
    Dict {
        pairs: Vec<(AstNode, AstNode)>,
    },
    Index {
        object: Box<AstNode>,
        index: Box<AstNode>,
    },
    Member {
        object: Box<AstNode>,
        property: String,
    },
}

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp {
    Add, Sub, Mul, Div, Mod, Pow,
    Equal, NotEqual, Less, LessEqual, Greater, GreaterEqual,
    And, Or,
}

#[derive(Debug, Clone, PartialEq)]
pub enum UnaryOp {
    Not, Minus,
}

impl fmt::Display for AstNode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AstNode::Program { statements } => {
                writeln!(f, "Program:")?;
                for stmt in statements {
                    writeln!(f, "  {}", stmt)?;
                }
                Ok(())
            }
            AstNode::PrintStmt { expr } => write!(f, "Print({})", expr),
            AstNode::Literal { value } => write!(f, "{}", value),
            AstNode::Variable { name } => write!(f, "{}", name),
            _ => write!(f, "{:?}", self),
        }
    }
}

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("Token inesperado: {0:?} en posición {1}")]
    UnexpectedToken(Token, usize),
    
    #[error("Se esperaba {expected}, se encontró {found:?}")]
    ExpectedToken { expected: String, found: Token },
    
    #[error("Fin de archivo inesperado")]
    UnexpectedEof,
    
    #[error("Expresión inválida")]
    InvalidExpression,
    
    #[error("Declaración inválida")]
    InvalidStatement,
}

pub struct VaderParser {
    tokens: Vec<Token>,
    current: usize,
}

impl VaderParser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, current: 0 }
    }
    
    pub fn parse(&mut self) -> Result<AstNode, ParseError> {
        let mut statements = Vec::new();
        
        while !self.is_at_end() {
            if self.match_token(&Token::Newline) || self.match_token(&Token::Eof) {
                continue;
            }
            
            statements.push(self.parse_statement()?);
        }
        
        Ok(AstNode::Program { statements })
    }
    
    fn parse_statement(&mut self) -> Result<AstNode, ParseError> {
        // Función
        if self.match_token(&Token::Funcion) || self.match_token(&Token::Function) {
            return self.parse_function();
        }
        
        // Clase
        if self.match_token(&Token::Clase) || self.match_token(&Token::Class) {
            return self.parse_class();
        }
        
        // Print/Decir
        if self.match_token(&Token::Decir) || self.match_token(&Token::Print) {
            return self.parse_print();
        }
        
        // If/Si
        if self.match_token(&Token::Si) || self.match_token(&Token::If) {
            return self.parse_if();
        }
        
        // While/Mientras
        if self.match_token(&Token::Mientras) || self.match_token(&Token::While) {
            return self.parse_while();
        }
        
        // For/Para
        if self.match_token(&Token::Para) || self.match_token(&Token::For) {
            return self.parse_for();
        }
        
        // Return/Retornar
        if self.match_token(&Token::Retornar) || self.match_token(&Token::Return) {
            return self.parse_return();
        }
        
        // Bloque con indentación
        if self.match_token(&Token::Indent) {
            return self.parse_block();
        }
        
        // Asignación o expresión
        self.parse_expression_or_assignment()
    }
    
    fn parse_function(&mut self) -> Result<AstNode, ParseError> {
        let name = self.expect_identifier()?;
        
        self.expect_token(Token::LeftParen)?;
        
        let mut params = Vec::new();
        if !self.check(&Token::RightParen) {
            loop {
                params.push(self.expect_identifier()?);
                if !self.match_token(&Token::Comma) {
                    break;
                }
            }
        }
        
        self.expect_token(Token::RightParen)?;
        self.expect_token(Token::Colon)?;
        
        let body = Box::new(self.parse_statement()?);
        
        Ok(AstNode::FunctionDecl { name, params, body })
    }
    
    fn parse_class(&mut self) -> Result<AstNode, ParseError> {
        let name = self.expect_identifier()?;
        self.expect_token(Token::Colon)?;
        
        let mut methods = Vec::new();
        
        if self.match_token(&Token::Indent) {
            while !self.check(&Token::Dedent) && !self.is_at_end() {
                if self.match_token(&Token::Newline) {
                    continue;
                }
                methods.push(self.parse_statement()?);
            }
            self.expect_token(Token::Dedent)?;
        }
        
        Ok(AstNode::ClassDecl { name, methods })
    }
    
    fn parse_print(&mut self) -> Result<AstNode, ParseError> {
        let expr = Box::new(self.parse_expression()?);
        Ok(AstNode::PrintStmt { expr })
    }
    
    fn parse_if(&mut self) -> Result<AstNode, ParseError> {
        let condition = Box::new(self.parse_expression()?);
        self.expect_token(Token::Colon)?;
        
        let then_branch = Box::new(self.parse_statement()?);
        
        let else_branch = if self.match_token(&Token::Sino) || self.match_token(&Token::Else) {
            if self.match_token(&Token::Si) || self.match_token(&Token::If) {
                // else if
                Some(Box::new(self.parse_if()?))
            } else {
                self.expect_token(Token::Colon)?;
                Some(Box::new(self.parse_statement()?))
            }
        } else {
            None
        };
        
        Ok(AstNode::IfStmt {
            condition,
            then_branch,
            else_branch,
        })
    }
    
    fn parse_while(&mut self) -> Result<AstNode, ParseError> {
        let condition = Box::new(self.parse_expression()?);
        self.expect_token(Token::Colon)?;
        let body = Box::new(self.parse_statement()?);
        
        Ok(AstNode::WhileStmt { condition, body })
    }
    
    fn parse_for(&mut self) -> Result<AstNode, ParseError> {
        let var = self.expect_identifier()?;
        self.expect_token(Token::En)?; // "en" o "in"
        let iterable = Box::new(self.parse_expression()?);
        self.expect_token(Token::Colon)?;
        let body = Box::new(self.parse_statement()?);
        
        Ok(AstNode::ForStmt { var, iterable, body })
    }
    
    fn parse_return(&mut self) -> Result<AstNode, ParseError> {
        let value = if self.check(&Token::Newline) || self.is_at_end() {
            None
        } else {
            Some(Box::new(self.parse_expression()?))
        };
        
        Ok(AstNode::ReturnStmt { value })
    }
    
    fn parse_block(&mut self) -> Result<AstNode, ParseError> {
        let mut statements = Vec::new();
        
        while !self.check(&Token::Dedent) && !self.is_at_end() {
            if self.match_token(&Token::Newline) {
                continue;
            }
            statements.push(self.parse_statement()?);
        }
        
        self.expect_token(Token::Dedent)?;
        Ok(AstNode::Block { statements })
    }
    
    fn parse_expression_or_assignment(&mut self) -> Result<AstNode, ParseError> {
        let expr = self.parse_expression()?;
        
        // Verificar si es asignación
        if let AstNode::Variable { name } = &expr {
            if self.match_token(&Token::Assign) {
                let value = Box::new(self.parse_expression()?);
                return Ok(AstNode::AssignStmt {
                    name: name.clone(),
                    value,
                });
            }
        }
        
        Ok(AstNode::ExpressionStmt {
            expr: Box::new(expr),
        })
    }
    
    fn parse_expression(&mut self) -> Result<AstNode, ParseError> {
        self.parse_or()
    }
    
    fn parse_or(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_and()?;
        
        while self.match_token(&Token::O) || self.match_token(&Token::Or) {
            let right = self.parse_and()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: BinaryOp::Or,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_and(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_equality()?;
        
        while self.match_token(&Token::Y) || self.match_token(&Token::And) {
            let right = self.parse_equality()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: BinaryOp::And,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_equality(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_comparison()?;
        
        while let Some(op) = self.match_equality_op() {
            let right = self.parse_comparison()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_comparison(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_term()?;
        
        while let Some(op) = self.match_comparison_op() {
            let right = self.parse_term()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_term(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_factor()?;
        
        while let Some(op) = self.match_term_op() {
            let right = self.parse_factor()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_factor(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_power()?;
        
        while let Some(op) = self.match_factor_op() {
            let right = self.parse_power()?;
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_power(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_unary()?;
        
        if self.match_token(&Token::Power) {
            let right = self.parse_power()?; // Right associative
            expr = AstNode::Binary {
                left: Box::new(expr),
                operator: BinaryOp::Pow,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_unary(&mut self) -> Result<AstNode, ParseError> {
        if self.match_token(&Token::No) || self.match_token(&Token::Not) {
            let operand = self.parse_unary()?;
            return Ok(AstNode::Unary {
                operator: UnaryOp::Not,
                operand: Box::new(operand),
            });
        }
        
        if self.match_token(&Token::Minus) {
            let operand = self.parse_unary()?;
            return Ok(AstNode::Unary {
                operator: UnaryOp::Minus,
                operand: Box::new(operand),
            });
        }
        
        self.parse_call()
    }
    
    fn parse_call(&mut self) -> Result<AstNode, ParseError> {
        let mut expr = self.parse_primary()?;
        
        loop {
            if self.match_token(&Token::LeftParen) {
                // Llamada a función
                let mut args = Vec::new();
                if !self.check(&Token::RightParen) {
                    loop {
                        args.push(self.parse_expression()?);
                        if !self.match_token(&Token::Comma) {
                            break;
                        }
                    }
                }
                self.expect_token(Token::RightParen)?;
                
                expr = AstNode::Call {
                    callee: Box::new(expr),
                    args,
                };
            } else if self.match_token(&Token::LeftBracket) {
                // Indexación
                let index = self.parse_expression()?;
                self.expect_token(Token::RightBracket)?;
                
                expr = AstNode::Index {
                    object: Box::new(expr),
                    index: Box::new(index),
                };
            } else if self.match_token(&Token::Dot) {
                // Acceso a miembro
                let property = self.expect_identifier()?;
                expr = AstNode::Member {
                    object: Box::new(expr),
                    property,
                };
            } else {
                break;
            }
        }
        
        Ok(expr)
    }
    
    fn parse_primary(&mut self) -> Result<AstNode, ParseError> {
        // Literales
        if let Some(token) = self.advance() {
            match token {
                Token::Number(n) => {
                    return Ok(AstNode::Literal {
                        value: VaderValue::Number(*n),
                    });
                }
                Token::String(s) => {
    // Métodos auxiliares
    fn match_token(&mut self, token: &Token) -> bool {
        if self.check(token) {
            self.advance();
            true
        } else {
            false
        }
    }
    
    fn check(&self, token: &Token) -> bool {
        if self.is_at_end() {
            false
        } else {
            std::mem::discriminant(self.peek()) == std::mem::discriminant(token)
        }
    }
    
    fn advance(&mut self) -> Option<&Token> {
        if !self.is_at_end() {
            self.current += 1;
        }
        self.previous()
    }
    
    fn is_at_end(&self) -> bool {
        matches!(self.peek(), Token::Eof)
    }
    
    fn peek(&self) -> &Token {
        self.tokens.get(self.current).unwrap_or(&Token::Eof)
    }
    
    fn previous(&self) -> Option<&Token> {
        if self.current > 0 {
            self.tokens.get(self.current - 1)
        } else {
            None
        }
    }
    
    fn expect_token(&mut self, expected: Token) -> Result<(), ParseError> {
        if self.check(&expected) {
            self.advance();
            Ok(())
        } else {
            Err(ParseError::ExpectedToken {
                expected: format!("{:?}", expected),
                found: self.peek().clone(),
            })
        }
    }
    
    fn expect_identifier(&mut self) -> Result<String, ParseError> {
        if let Token::Identifier(name) = self.peek() {
            let name = name.clone();
            self.advance();
            Ok(name)
        } else {
            Err(ParseError::ExpectedToken {
                expected: "identifier".to_string(),
                found: self.peek().clone(),
            })
        }
    }
    
    fn match_equality_op(&mut self) -> Option<BinaryOp> {
        if self.match_token(&Token::Equal) {
            Some(BinaryOp::Equal)
        } else if self.match_token(&Token::NotEqual) {
            Some(BinaryOp::NotEqual)
        } else {
            None
        }
    }
    
    fn match_comparison_op(&mut self) -> Option<BinaryOp> {
        if self.match_token(&Token::Greater) {
            Some(BinaryOp::Greater)
        } else if self.match_token(&Token::GreaterEqual) {
            Some(BinaryOp::GreaterEqual)
        } else if self.match_token(&Token::Less) {
            Some(BinaryOp::Less)
        } else if self.match_token(&Token::LessEqual) {
            Some(BinaryOp::LessEqual)
        } else {
            None
        }
    }
    
    fn match_term_op(&mut self) -> Option<BinaryOp> {
        if self.match_token(&Token::Plus) {
            Some(BinaryOp::Add)
        } else if self.match_token(&Token::Minus) {
            Some(BinaryOp::Sub)
        } else {
            None
        }
    }
    
    fn match_factor_op(&mut self) -> Option<BinaryOp> {
        if self.match_token(&Token::Multiply) {
            Some(BinaryOp::Mul)
        } else if self.match_token(&Token::Divide) {
            Some(BinaryOp::Div)
        } else if self.match_token(&Token::Modulo) {
            Some(BinaryOp::Mod)
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::VaderLexer;
    
    #[test]
    fn test_parse_print() {
        let mut lexer = VaderLexer::new("decir \"Hola\"");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        
        if let AstNode::Program { statements } = ast {
            assert_eq!(statements.len(), 1);
            assert!(matches!(statements[0], AstNode::PrintStmt { .. }));
        }
    }
    
    #[test]
    fn test_parse_assignment() {
        let mut lexer = VaderLexer::new("x = 42");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        
        if let AstNode::Program { statements } = ast {
            assert_eq!(statements.len(), 1);
            assert!(matches!(statements[0], AstNode::AssignStmt { .. }));
        }
    }
}
