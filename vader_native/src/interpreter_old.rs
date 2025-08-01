/*!
🎮 VADER INTERPRETER NATIVO - EJECUCIÓN REAL
==========================================

Intérprete nativo que ejecuta AST de Vader directamente.
Runtime completo con variables, funciones, clases y stdlib.

Autor: Adriano & Cascade AI
*/

use crate::parser::{AstNode, BinaryOp, UnaryOp};
use crate::types::VaderValue;
use std::collections::HashMap;
use std::rc::Rc;
use std::cell::RefCell;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum RuntimeError {
    #[error("Variable no definida: {0}")]
    UndefinedVariable(String),
    
    #[error("Función no definida: {0}")]
    UndefinedFunction(String),
    
    #[error("Error de tipo: {0}")]
    TypeError(String),
    
    #[error("Error de índice: {0}")]
    IndexError(String),
    
    #[error("Error de división por cero")]
    DivisionByZero,
    
    #[error("Número incorrecto de argumentos: esperados {expected}, recibidos {actual}")]
    WrongArgumentCount { expected: usize, actual: usize },
    
    #[error("Return fuera de función")]
    ReturnOutsideFunction,
    
    #[error("Break fuera de bucle")]
    BreakOutsideLoop,
    
    #[error("Continue fuera de bucle")]
    ContinueOutsideLoop,
    
    #[error("Error de runtime: {0}")]
    RuntimeError(String),
}

#[derive(Debug, Clone)]
pub struct VaderFunction {
    pub name: String,
    pub params: Vec<String>,
    pub body: AstNode,
    pub closure: Environment,
}

#[derive(Debug, Clone)]
pub struct VaderClass {
    pub name: String,
    pub methods: HashMap<String, VaderFunction>,
}

#[derive(Debug, Clone)]
pub struct Environment {
    variables: HashMap<String, VaderValue>,
    parent: Option<Rc<RefCell<Environment>>>,
}

impl Environment {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            parent: None,
        }
    }
    
    pub fn with_parent(parent: Rc<RefCell<Environment>>) -> Self {
        Self {
            variables: HashMap::new(),
            parent: Some(parent),
        }
    }
    
    pub fn define(&mut self, name: String, value: VaderValue) {
        self.variables.insert(name, value);
    }
    
    pub fn get(&self, name: &str) -> Option<VaderValue> {
        if let Some(value) = self.variables.get(name) {
            Some(value.clone())
        } else if let Some(parent) = &self.parent {
            parent.borrow().get(name)
        } else {
            None
        }
    }
    
    pub fn set(&mut self, name: &str, value: VaderValue) -> Result<(), RuntimeError> {
        if self.variables.contains_key(name) {
            self.variables.insert(name.to_string(), value);
            Ok(())
        } else if let Some(parent) = &self.parent {
            parent.borrow_mut().set(name, value)
        } else {
            Err(RuntimeError::UndefinedVariable(name.to_string()))
        }
    }
}

pub struct VaderInterpreter {
    environment: Rc<RefCell<Environment>>,
    globals: Rc<RefCell<Environment>>,
    functions: HashMap<String, VaderFunction>,
    classes: HashMap<String, VaderClass>,
    return_value: Option<VaderValue>,
    break_flag: bool,
    continue_flag: bool,
}

impl VaderInterpreter {
    pub fn new() -> Self {
        let globals = Rc::new(RefCell::new(Environment::new()));
        let environment = globals.clone();
        
        let mut interpreter = Self {
            environment,
            globals: globals.clone(),
            functions: HashMap::new(),
            classes: HashMap::new(),
            return_value: None,
            break_flag: false,
            continue_flag: false,
        };
        
        // Cargar funciones built-in
        interpreter.load_builtins();
        
        interpreter
    }
    
    fn load_builtins(&mut self) {
        // Función rango
        self.globals.borrow_mut().define(
            "rango".to_string(),
            VaderValue::Function {
                name: "rango".to_string(),
                params: vec!["start".to_string(), "end".to_string()],
                body: "builtin".to_string(),
            }
        );
        
        // Función longitud
        self.globals.borrow_mut().define(
            "longitud".to_string(),
            VaderValue::Function {
                name: "longitud".to_string(),
                params: vec!["obj".to_string()],
                body: "builtin".to_string(),
            }
        );
        
        // Función tipo
        self.globals.borrow_mut().define(
            "tipo".to_string(),
            VaderValue::Function {
                name: "tipo".to_string(),
                params: vec!["obj".to_string()],
                body: "builtin".to_string(),
            }
        );
    }
    
    pub fn execute(&mut self, node: AstNode) -> Result<VaderValue, RuntimeError> {
        match node {
            AstNode::Program { statements } => {
                let mut last_value = VaderValue::Null;
                for stmt in statements {
                    last_value = self.execute_statement(stmt)?;
                    
                    if self.return_value.is_some() || self.break_flag || self.continue_flag {
                        break;
                    }
                }
                Ok(last_value)
            }
            
            AstNode::ExpressionStmt { expr } => {
                self.execute(*expr)
            }
            
            AstNode::PrintStmt { expr } => {
                let value = self.execute(*expr)?;
                println!("{}", value.to_string());
                Ok(VaderValue::Null)
            }
            
            AstNode::Assignment { name, value } => {
                let val = self.execute(*value)?;
                self.environment.borrow_mut().define(name, val.clone());
                Ok(val)
            }
            
            AstNode::If { condition, then_branch, else_branch } => {
                let cond_value = self.execute(*condition)?;
                
                if cond_value.is_truthy() {
                    self.execute_block(then_branch)
                } else if let Some(else_stmts) = else_branch {
                    self.execute_block(else_stmts)
                } else {
                    Ok(VaderValue::Null)
                }
            }
            
            AstNode::While { condition, body } => {
                let mut last_value = VaderValue::Null;
                
                loop {
                    let cond_value = self.execute(*condition)?;
                    if !cond_value.is_truthy() {
                        break;
                    }
                    
                    last_value = self.execute_block(body)?;
                    
                    if self.break_flag {
                        self.break_flag = false;
                        break;
                    }
                    
                    if self.continue_flag {
                        self.continue_flag = false;
                        continue;
                    }
                    
                    if self.return_value.is_some() {
                        break;
                    }
                }
                
                Ok(last_value)
            }
            
            AstNode::For { variable, iterable, body } => {
                let iter_value = self.execute(*iterable)?;
                let items = iter_value.iter().map_err(|e| RuntimeError::RuntimeError(e))?;
                
                let mut last_value = VaderValue::Null;
                
                for item in items {
                    self.environment.borrow_mut().define(variable.clone(), item);
                    last_value = self.execute_block(body)?;
                    
                    if self.break_flag {
                        self.break_flag = false;
                        break;
                    }
                    
                    if self.continue_flag {
                        self.continue_flag = false;
                        continue;
                    }
                    
                    if self.return_value.is_some() {
                        break;
                    }
                }
                
                Ok(last_value)
            }
            
            AstNode::FunctionDecl { name, params, body } => {
                let function = VaderFunction {
                    name: name.clone(),
                    params,
                    body: *body,
                    closure: self.environment.borrow().clone(),
                };
                
                self.functions.insert(name.clone(), function.clone());
                self.environment.borrow_mut().define(
                    name.clone(),
                    VaderValue::Function {
                        name: name.clone(),
                        params: function.params.clone(),
                        body: "user_defined".to_string(),
                    }
                );
                
                Ok(VaderValue::Null)
            }
            
            AstNode::ReturnStmt { value } => {
                let return_val = if let Some(val) = value {
                    self.execute(*val)?
                } else {
                    VaderValue::Null
                };
                
                self.return_value = Some(return_val.clone());
                Ok(return_val)
            }
            
            AstNode::Block { statements } => {
                self.execute_block(statements)
                for stmt in statements {
                    last_value = self.execute(stmt)?;
                    
                    if self.return_value.is_some() || self.break_flag || self.continue_flag {
                        break;
                    }
                }
                
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
                    _ => Err(RuntimeError::UnsupportedOperation(operator.clone())),
                }
            }
            
            AstNode::UnaryOp { operator, operand } => {
                let operand_val = self.execute(*operand)?;
                
                match operator.as_str() {
                    "-" => operand_val.negate().map_err(RuntimeError::TypeError),
                    "not" => Ok(VaderValue::Boolean(!self.is_truthy(&operand_val))),
                    _ => Err(RuntimeError::UnsupportedOperation(operator.clone())),
                }
            }
            
            AstNode::FunctionCall { name, args } => {
                self.execute_statement(node) // Reutilizar la lógica de execute_statement
            }
            
            AstNode::Binary { left, operator, right } => {
                let left_val = self.execute(*left)?;
                let right_val = self.execute(*right)?;
                
                match operator {
                    BinaryOp::Add => left_val.add(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Sub => left_val.subtract(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Mul => left_val.multiply(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Div => left_val.divide(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Mod => left_val.modulo(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Pow => left_val.power(&right_val).map_err(|e| RuntimeError::TypeError(e)),
                    BinaryOp::Equal => Ok(VaderValue::Boolean(left_val.equals(&right_val))),
                    BinaryOp::NotEqual => Ok(VaderValue::Boolean(!left_val.equals(&right_val))),
                    BinaryOp::Less => {
                        match left_val.compare(&right_val) {
                            Ok(std::cmp::Ordering::Less) => Ok(VaderValue::Boolean(true)),
                            Ok(_) => Ok(VaderValue::Boolean(false)),
                            Err(e) => Err(RuntimeError::TypeError(e)),
                        }
                    }
                    BinaryOp::LessEqual => {
                        match left_val.compare(&right_val) {
                            Ok(std::cmp::Ordering::Less | std::cmp::Ordering::Equal) => Ok(VaderValue::Boolean(true)),
                            Ok(_) => Ok(VaderValue::Boolean(false)),
                            Err(e) => Err(RuntimeError::TypeError(e)),
                        }
                    }
                    BinaryOp::Greater => {
                        match left_val.compare(&right_val) {
                            Ok(std::cmp::Ordering::Greater) => Ok(VaderValue::Boolean(true)),
                            Ok(_) => Ok(VaderValue::Boolean(false)),
                            Err(e) => Err(RuntimeError::TypeError(e)),
                        }
                    }
                    BinaryOp::GreaterEqual => {
                        match left_val.compare(&right_val) {
                            Ok(std::cmp::Ordering::Greater | std::cmp::Ordering::Equal) => Ok(VaderValue::Boolean(true)),
                            Ok(_) => Ok(VaderValue::Boolean(false)),
                            Err(e) => Err(RuntimeError::TypeError(e)),
                        }
                    }
                    BinaryOp::And => {
                        if left_val.is_truthy() {
                            Ok(right_val)
                        } else {
                            Ok(left_val)
                        }
                    }
                    BinaryOp::Or => {
                        if left_val.is_truthy() {
                            Ok(left_val)
                        } else {
                            Ok(right_val)
                        }
                    }
                }
            }
            
            AstNode::Unary { operator, operand } => {
                let value = self.execute(*operand)?;
                
                match operator {
                    UnaryOp::Not => Ok(VaderValue::Boolean(!value.is_truthy())),
                    UnaryOp::Minus => {
                        match value {
                            VaderValue::Number(n) => Ok(VaderValue::Number(-n)),
                            _ => Err(RuntimeError::TypeError(format!("No se puede negar {}", value.type_name()))),
                        }
                    }
                }
            }
            
            AstNode::Call { callee, args } => {
                let function_value = self.execute(*callee)?;
                let mut arg_values = Vec::new();
                
                for arg in args {
                    arg_values.push(self.execute(arg)?);
                }
                
                self.call_function(function_value, arg_values)
            }
            
            AstNode::Variable { name } => {
                self.environment.borrow().get(&name)
                    .ok_or_else(|| RuntimeError::UndefinedVariable(name))
            }
            
            AstNode::Literal { value } => Ok(value),
            
            AstNode::List { elements } => {
                let mut list_values = Vec::new();
                for element in elements {
                    list_values.push(self.execute(element)?);
                }
                Ok(VaderValue::List(list_values))
            }
            
            AstNode::Dict { pairs } => {
                let mut dict_values = HashMap::new();
                for (key_node, value_node) in pairs {
                    let key = self.execute(key_node)?;
                    let value = self.execute(value_node)?;
                    
                    if let VaderValue::String(key_str) = key {
                        dict_values.insert(key_str, value);
                    } else {
                        return Err(RuntimeError::TypeError("Las claves del diccionario deben ser strings".to_string()));
                    }
                }
                Ok(VaderValue::Dict(dict_values))
            }
            
            AstNode::Index { object, index } => {
                let obj_value = self.execute(*object)?;
                let index_value = self.execute(*index)?;
                
                obj_value.index(&index_value).map_err(|e| RuntimeError::IndexError(e))
            }
            
            AstNode::Member { object, property } => {
                let obj_value = self.execute(*object)?;
                obj_value.get_member(&property).map_err(|e| RuntimeError::RuntimeError(e))
            }
            
            AstNode::ClassDecl { name, methods } => {
                let mut class_methods = HashMap::new();
                
                for method in methods {
                    if let AstNode::FunctionDecl { name: method_name, params, body } = method {
                        let function = VaderFunction {
                            name: method_name.clone(),
                            params,
                            body: *body,
                            closure: self.environment.borrow().clone(),
                        };
                        class_methods.insert(method_name, function);
                    }
                }
                
                let class = VaderClass {
                    name: name.clone(),
                    methods: class_methods,
                };
                
                self.classes.insert(name.clone(), class);
                Ok(VaderValue::Null)
            }
        }
    }
    
    fn call_function(&mut self, function: VaderValue, args: Vec<VaderValue>) -> Result<VaderValue, RuntimeError> {
        match function {
            VaderValue::Function { name, params, .. } => {
                // Funciones built-in
                match name.as_str() {
                    "rango" => {
                        match args.len() {
                            1 => {
                                if let VaderValue::Number(end) = args[0] {
                                    Ok(VaderValue::range(0, end as i64))
                                } else {
                                    Err(RuntimeError::TypeError("rango() requiere un número".to_string()))
                                }
                            }
                            2 => {
                                if let (VaderValue::Number(start), VaderValue::Number(end)) = (&args[0], &args[1]) {
                                    Ok(VaderValue::range(*start as i64, *end as i64))
                                } else {
                                    Err(RuntimeError::TypeError("rango() requiere números".to_string()))
                                }
                            }
                            3 => {
                                if let (VaderValue::Number(start), VaderValue::Number(end), VaderValue::Number(step)) = 
                                    (&args[0], &args[1], &args[2]) {
                                    Ok(VaderValue::range_with_step(*start as i64, *end as i64, *step as i64))
                                } else {
                                    Err(RuntimeError::TypeError("rango() requiere números".to_string()))
                                }
                            }
                            _ => Err(RuntimeError::WrongArgumentCount { expected: 1, actual: args.len() }),
                        }
                    }
                    "longitud" => {
                        if args.len() != 1 {
                            return Err(RuntimeError::WrongArgumentCount { expected: 1, actual: args.len() });
                        }
                        Ok(VaderValue::Number(args[0].len() as f64))
                    }
                    "tipo" => {
                        if args.len() != 1 {
                            return Err(RuntimeError::WrongArgumentCount { expected: 1, actual: args.len() });
                        }
                        Ok(VaderValue::String(args[0].type_name().to_string()))
                    }
                    _ => {
                        // Función definida por el usuario
                        if let Some(user_function) = self.functions.get(&name).cloned() {
                            self.call_user_function(user_function, args)
                        } else {
                            Err(RuntimeError::UndefinedFunction(name))
                        }
                    }
                }
            }
            _ => Err(RuntimeError::TypeError("Solo se pueden llamar funciones".to_string())),
        }
    }
    
    fn call_user_function(&mut self, function: VaderFunction, args: Vec<VaderValue>) -> Result<VaderValue, RuntimeError> {
        if args.len() != function.params.len() {
            return Err(RuntimeError::WrongArgumentCount {
                expected: function.params.len(),
                actual: args.len(),
            });
        }
        
        // Crear nuevo entorno para la función
        let func_env = Rc::new(RefCell::new(Environment::with_parent(self.globals.clone())));
        
        // Bind parámetros
        for (param, arg) in function.params.iter().zip(args.iter()) {
            func_env.borrow_mut().define(param.clone(), arg.clone());
        }
        
        // Guardar entorno actual
        let previous_env = self.environment.clone();
        self.environment = func_env;
        
        // Ejecutar cuerpo de la función
        let result = self.execute(function.body);
        
        // Manejar return
        let return_val = if let Some(ret_val) = self.return_value.take() {
            ret_val
        } else {
            result.unwrap_or(VaderValue::Null)
        };
        
        // Restaurar entorno
        self.environment = previous_env;
        
        Ok(return_val)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::VaderLexer;
    use crate::parser::VaderParser;
    
    fn execute_code(code: &str) -> Result<VaderValue, RuntimeError> {
        let mut lexer = VaderLexer::new(code);
        let tokens = lexer.tokenize().unwrap();
        let mut parser = VaderParser::new(tokens);
        let ast = parser.parse().unwrap();
        let mut interpreter = VaderInterpreter::new();
        interpreter.execute(ast)
    }
    
    #[test]
    fn test_arithmetic() {
        let result = execute_code("2 + 3 * 4").unwrap();
        assert_eq!(result, VaderValue::Number(14.0));
    }
    
    #[test]
    fn test_variables() {
        let result = execute_code("x = 42\nx").unwrap();
        assert_eq!(result, VaderValue::Number(42.0));
    }
    
    #[test]
    fn test_print() {
        let result = execute_code("decir \"Hola mundo\"");
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_if_statement() {
        let result = execute_code("si verdadero:\n    42\nsino:\n    0").unwrap();
        assert_eq!(result, VaderValue::Number(42.0));
    }
    
    #[test]
    fn test_function_call() {
        let result = execute_code("longitud([1, 2, 3])").unwrap();
        assert_eq!(result, VaderValue::Number(3.0));
    }
}
