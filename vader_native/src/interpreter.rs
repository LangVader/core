/*!
🚀 VADER INTERPRETER NATIVO - VERSIÓN LIMPIA
==========================================

Intérprete nativo completamente refactorizado para usar las nuevas estructuras
AstNode del parser y TokenType del lexer.

Autor: Adriano & Cascade AI
*/

use crate::parser::AstNode;
use crate::types::VaderValue;
use crate::stdlib::VaderStdlib;
use std::collections::HashMap;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum RuntimeError {
    #[error("Variable no definida: {0}")]
    UndefinedVariable(String),
    
    #[error("Función no definida: {0}")]
    UndefinedFunction(String),
    
    #[error("Error de tipo: {0}")]
    TypeError(String),
    
    #[error("Operación no soportada: {0}")]
    UnsupportedOperation(String),
    
    #[error("Expresión inválida")]
    InvalidExpression,
    
    #[error("Error en función built-in: {0}")]
    BuiltinError(String),
    
    #[error("División por cero")]
    DivisionByZero,
    
    #[error("Índice fuera de rango")]
    IndexOutOfRange,
}

#[derive(Debug, Clone, Default)]
pub struct Environment {
    variables: HashMap<String, VaderValue>,
    parent: Option<Box<Environment>>,
}

impl Environment {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            parent: None,
        }
    }
    
    pub fn with_parent(parent: Environment) -> Self {
        Self {
            variables: HashMap::new(),
            parent: Some(Box::new(parent)),
        }
    }
    
    pub fn get(&self, name: &str) -> Option<VaderValue> {
        if let Some(value) = self.variables.get(name) {
            Some(value.clone())
        } else if let Some(parent) = &self.parent {
            parent.get(name)
        } else {
            None
        }
    }
    
    pub fn set(&mut self, name: String, value: VaderValue) {
        self.variables.insert(name, value);
    }
    
    pub fn define(&mut self, name: String, value: VaderValue) {
        self.variables.insert(name, value);
    }
}

pub struct VaderInterpreter {
    environment: Environment,
    pub stdlib: VaderStdlib,
    return_value: Option<VaderValue>,
}

impl VaderInterpreter {
    pub fn new() -> Self {
        Self {
            environment: Environment::new(),
            stdlib: VaderStdlib::new(),
            return_value: None,
        }
    }
    
    pub fn interpret(&mut self, statements: Vec<AstNode>) -> Result<VaderValue, RuntimeError> {
        let mut result = VaderValue::Null;
        
        for statement in statements {
            result = self.execute_statement(&statement)?;
            
            // Si hay un return, salir inmediatamente
            if self.return_value.is_some() {
                return Ok(self.return_value.take().unwrap());
            }
        }
        
        Ok(result)
    }
    
    // Alias para compatibilidad con main.rs
    pub fn execute(&mut self, statements: Vec<AstNode>) -> Result<VaderValue, RuntimeError> {
        self.interpret(statements)
    }
    
    fn execute_statement(&mut self, node: &AstNode) -> Result<VaderValue, RuntimeError> {
        match node {
            AstNode::Assignment { name, value } => {
                let val = self.evaluate_expression(value)?;
                self.environment.set(name.clone(), val.clone());
                Ok(val)
            }
            
            AstNode::FunctionCall { name, args } => {
                let mut arg_values = Vec::new();
                for arg in args {
                    arg_values.push(self.evaluate_expression(arg)?);
                }
                
                // Verificar funciones built-in primero
                if let Some(builtin_fn) = self.stdlib.get_function(name) {
                    return builtin_fn(&arg_values).map_err(RuntimeError::BuiltinError);
                }
                
                // Verificar funciones definidas por el usuario
                if let Some(VaderValue::Function { params, body, .. }) = self.environment.get(name) {
                    return self.call_user_function(&params, &body, &arg_values);
                }
                
                Err(RuntimeError::UndefinedFunction(name.clone()))
            }
            
            AstNode::If { condition, then_branch, else_branch } => {
                let condition_value = self.evaluate_expression(condition)?;
                
                if self.is_truthy(&condition_value) {
                    self.execute_block(then_branch)
                } else if let Some(else_stmts) = else_branch {
                    self.execute_block(else_stmts)
                } else {
                    Ok(VaderValue::Null)
                }
            }
            
            AstNode::While { condition, body } => {
                let mut result = VaderValue::Null;
                
                loop {
                    let condition_result = self.evaluate_expression(condition)?;
                    if !self.is_truthy(&condition_result) {
                        break;
                    }
                    
                    result = self.execute_block(body)?;
                    
                    // Manejar return statements
                    if self.return_value.is_some() {
                        break;
                    }
                }
                
                Ok(result)
            }
            
            AstNode::For { variable, iterable, body } => {
                let iterable_value = self.evaluate_expression(iterable)?;
                let mut result = VaderValue::Null;
                
                match iterable_value {
                    VaderValue::List(items) => {
                        for item in items {
                            self.environment.set(variable.clone(), item);
                            result = self.execute_block(body)?;
                            
                            if self.return_value.is_some() {
                                break;
                            }
                        }
                    }
                    VaderValue::Range { start, end, step } => {
                        let mut current = start;
                        while (step > 0 && current < end) || (step < 0 && current > end) {
                            self.environment.set(variable.clone(), VaderValue::Number(current as f64));
                            result = self.execute_block(body)?;
                            
                            if self.return_value.is_some() {
                                break;
                            }
                            
                            current += step;
                        }
                    }
                    _ => return Err(RuntimeError::TypeError("Objeto no iterable".to_string())),
                }
                
                Ok(result)
            }
            
            AstNode::FunctionDef { name, params, body } => {
                let function_value = VaderValue::Function {
                    name: name.clone(),
                    params: params.clone(),
                    body: body.clone(),
                };
                self.environment.set(name.clone(), function_value.clone());
                Ok(function_value)
            }
            
            AstNode::Return { value } => {
                let return_val = if let Some(val) = value {
                    self.evaluate_expression(val)?
                } else {
                    VaderValue::Null
                };
                
                self.return_value = Some(return_val.clone());
                Ok(return_val)
            }
            
            AstNode::Block { statements } => {
                self.execute_block(statements)
            }
            
            _ => self.evaluate_expression(node),
        }
    }
    
    fn execute_block(&mut self, statements: &[AstNode]) -> Result<VaderValue, RuntimeError> {
        let mut result = VaderValue::Null;
        
        for stmt in statements {
            result = self.execute_statement(stmt)?;
            
            if self.return_value.is_some() {
                break;
            }
        }
        
        Ok(result)
    }
    
    fn evaluate_expression(&mut self, node: &AstNode) -> Result<VaderValue, RuntimeError> {
        match node {
            AstNode::Literal { value } => Ok(value.clone()),
            
            AstNode::Variable { name } => {
                self.environment.get(name)
                    .ok_or_else(|| RuntimeError::UndefinedVariable(name.clone()))
            }
            
            AstNode::BinaryOp { left, operator, right } => {
                let left_val = self.evaluate_expression(left)?;
                let right_val = self.evaluate_expression(right)?;
                
                match operator.as_str() {
                    "+" => left_val.add(&right_val).map_err(RuntimeError::TypeError),
                    "-" => left_val.subtract(&right_val).map_err(RuntimeError::TypeError),
                    "*" => left_val.multiply(&right_val).map_err(RuntimeError::TypeError),
                    "/" => left_val.divide(&right_val).map_err(RuntimeError::TypeError),
                    "%" => left_val.modulo(&right_val).map_err(RuntimeError::TypeError),
                    "==" => Ok(VaderValue::Boolean(left_val.equals(&right_val))),
                    "!=" => Ok(VaderValue::Boolean(!left_val.equals(&right_val))),
                    "<" => left_val.less_than(&right_val).map_err(RuntimeError::TypeError),
                    "<=" => left_val.less_equal(&right_val).map_err(RuntimeError::TypeError),
                    ">" => left_val.greater_than(&right_val).map_err(RuntimeError::TypeError),
                    ">=" => left_val.greater_equal(&right_val).map_err(RuntimeError::TypeError),
                    "and" => Ok(VaderValue::Boolean(self.is_truthy(&left_val) && self.is_truthy(&right_val))),
                    "or" => Ok(VaderValue::Boolean(self.is_truthy(&left_val) || self.is_truthy(&right_val))),
                    "y" => Ok(VaderValue::Boolean(self.is_truthy(&left_val) && self.is_truthy(&right_val))),
                    "o" => Ok(VaderValue::Boolean(self.is_truthy(&left_val) || self.is_truthy(&right_val))),
                    _ => Err(RuntimeError::UnsupportedOperation(operator.clone())),
                }
            }
            
            AstNode::UnaryOp { operator, operand } => {
                let operand_val = self.evaluate_expression(operand)?;
                
                match operator.as_str() {
                    "-" => operand_val.negate().map_err(RuntimeError::TypeError),
                    "not" => Ok(VaderValue::Boolean(!self.is_truthy(&operand_val))),
                    "no" => Ok(VaderValue::Boolean(!self.is_truthy(&operand_val))),
                    _ => Err(RuntimeError::UnsupportedOperation(operator.clone())),
                }
            }
            
            AstNode::FunctionCall { name, args } => {
                let mut arg_values = Vec::new();
                for arg in args {
                    arg_values.push(self.evaluate_expression(arg)?);
                }
                
                // Verificar funciones built-in primero
                if let Some(builtin_fn) = self.stdlib.get_function(name) {
                    return builtin_fn(&arg_values).map_err(RuntimeError::BuiltinError);
                }
                
                // Verificar funciones definidas por el usuario
                if let Some(VaderValue::Function { params, body, .. }) = self.environment.get(name) {
                    return self.call_user_function(&params, &body, &arg_values);
                }
                
                Err(RuntimeError::UndefinedFunction(name.clone()))
            }
            
            AstNode::List { elements } => {
                let mut values = Vec::new();
                for element in elements {
                    values.push(self.evaluate_expression(element)?);
                }
                Ok(VaderValue::List(values))
            }
            
            AstNode::Dict { pairs } => {
                let mut dict = HashMap::new();
                for (key_node, value_node) in pairs {
                    let key = match self.evaluate_expression(key_node)? {
                        VaderValue::String(s) => s,
                        other => other.to_string(),
                    };
                    let value = self.evaluate_expression(value_node)?;
                    dict.insert(key, value);
                }
                Ok(VaderValue::Dict(dict))
            }
            
            AstNode::Index { object, index } => {
                let obj_val = self.evaluate_expression(object)?;
                let idx_val = self.evaluate_expression(index)?;
                obj_val.get_index(&idx_val).map_err(RuntimeError::TypeError)
            }
            
            AstNode::MemberAccess { object, member } => {
                let obj_val = self.evaluate_expression(object)?;
                obj_val.get_member(member).map_err(RuntimeError::TypeError)
            }
            
            _ => Err(RuntimeError::InvalidExpression),
        }
    }
    
    fn call_user_function(&mut self, params: &[String], body: &[AstNode], args: &[VaderValue]) -> Result<VaderValue, RuntimeError> {
        // Crear nuevo entorno para la función
        let current_env = std::mem::take(&mut self.environment);
        self.environment = Environment::with_parent(current_env);
        
        // Asignar parámetros
        for (param, arg) in params.iter().zip(args.iter()) {
            self.environment.set(param.clone(), arg.clone());
        }
        
        // Ejecutar el cuerpo de la función
        let mut result = VaderValue::Null;
        for statement in body {
            result = self.execute_statement(statement)?;
            
            // Si hay un return, salir inmediatamente
            if let Some(return_val) = &self.return_value {
                result = return_val.clone();
                self.return_value = None; // Limpiar el return value
                break;
            }
        }
        
        // Restaurar entorno anterior
        if let Some(parent) = self.environment.parent.take() {
            self.environment = *parent;
        }
        
        Ok(result)
    }
    
    fn is_truthy(&self, value: &VaderValue) -> bool {
        match value {
            VaderValue::Boolean(b) => *b,
            VaderValue::Null => false,
            VaderValue::Number(n) => *n != 0.0,
            VaderValue::String(s) => !s.is_empty(),
            VaderValue::List(l) => !l.is_empty(),
            VaderValue::Dict(d) => !d.is_empty(),
            _ => true,
        }
    }
}

impl Default for VaderInterpreter {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::VaderLexer;
    use crate::parser::VaderParser;
    
    #[test]
    fn test_simple_arithmetic() {
        let mut lexer = VaderLexer::new("2 + 3");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        let mut interpreter = VaderInterpreter::new();
        
        let result = interpreter.interpret(ast).unwrap();
        assert_eq!(result, VaderValue::Number(5.0));
    }
    
    #[test]
    fn test_variable_assignment() {
        let mut lexer = VaderLexer::new("x = 42");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        let mut interpreter = VaderInterpreter::new();
        
        let result = interpreter.interpret(ast).unwrap();
        assert_eq!(result, VaderValue::Number(42.0));
        assert_eq!(interpreter.environment.get("x"), Some(VaderValue::Number(42.0)));
    }
}
