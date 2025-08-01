/*!
🎯 VADER TYPES - SISTEMA DE TIPOS NATIVO
======================================

Sistema de tipos dinámico de Vader con valores nativos.
Soporta todos los tipos primitivos y complejos.

Autor: Adriano & Cascade AI
*/

use std::collections::HashMap;
use std::fmt;
use thiserror::Error;
use crate::parser::AstNode;

#[derive(Error, Debug)]
pub enum TypeError {
    #[error("Tipo incompatible: esperado {expected}, encontrado {found}")]
    IncompatibleType { expected: String, found: String },
    
    #[error("Operación no soportada: {operation} en tipo {type_name}")]
    UnsupportedOperation { operation: String, type_name: String },
    
    #[error("Índice fuera de rango: {index}")]
    IndexOutOfRange { index: String },
    
    #[error("Miembro no encontrado: {member} en {type_name}")]
    MemberNotFound { member: String, type_name: String },
}
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum VaderValue {
    // Tipos primitivos
    Number(f64),
    String(String),
    Boolean(bool),
    Null,
    
    // Tipos complejos
    List(Vec<VaderValue>),
    Dict(HashMap<String, VaderValue>),
    
    // Funciones
    Function {
        name: String,
        params: Vec<String>,
        body: Vec<AstNode>,
    },
    
    // Objetos/Clases
    Object {
        class_name: String,
        fields: HashMap<String, VaderValue>,
    },
    
    // Tipos especiales
    Range {
        start: i64,
        end: i64,
        step: i64,
    },
}

impl VaderValue {
    pub fn type_name(&self) -> &'static str {
        match self {
            VaderValue::Number(_) => "numero",
            VaderValue::String(_) => "texto",
            VaderValue::Boolean(_) => "booleano",
            VaderValue::Null => "nulo",
            VaderValue::List(_) => "lista",
            VaderValue::Dict(_) => "diccionario",
            VaderValue::Function { .. } => "funcion",
            VaderValue::Object { .. } => "objeto",
            VaderValue::Range { .. } => "rango",
        }
    }
    
    pub fn is_truthy(&self) -> bool {
        match self {
            VaderValue::Boolean(b) => *b,
            VaderValue::Null => false,
            VaderValue::Number(n) => *n != 0.0,
            VaderValue::String(s) => !s.is_empty(),
            VaderValue::List(l) => !l.is_empty(),
            VaderValue::Dict(d) => !d.is_empty(),
            _ => true,
        }
    }
    
    pub fn to_string(&self) -> String {
        match self {
            VaderValue::Number(n) => {
                if n.fract() == 0.0 {
                    format!("{}", *n as i64)
                } else {
                    format!("{}", n)
                }
            }
            VaderValue::String(s) => s.clone(),
            VaderValue::Boolean(b) => if *b { "verdadero".to_string() } else { "falso".to_string() },
            VaderValue::Null => "nulo".to_string(),
            VaderValue::List(items) => {
                let items_str: Vec<String> = items.iter().map(|v| v.to_string()).collect();
                format!("[{}]", items_str.join(", "))
            }
            VaderValue::Dict(map) => {
                let pairs: Vec<String> = map.iter()
                    .map(|(k, v)| format!("{}: {}", k, v.to_string()))
                    .collect();
                format!("{{{}}}", pairs.join(", "))
            }
            VaderValue::Function { name, params, .. } => {
                format!("funcion {}({})", name, params.join(", "))
            }
            VaderValue::Object { class_name, .. } => {
                format!("objeto de {}", class_name)
            }
            VaderValue::Range { start, end, step } => {
                format!("rango({}, {}, {})", start, end, step)
            }
        }
    }
    
    pub fn add(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => Ok(VaderValue::Number(a + b)),
            (VaderValue::String(a), VaderValue::String(b)) => Ok(VaderValue::String(format!("{}{}", a, b))),
            (VaderValue::String(a), other) => Ok(VaderValue::String(format!("{}{}", a, other.to_string()))),
            (VaderValue::List(a), VaderValue::List(b)) => {
                let mut result = a.clone();
                result.extend(b.clone());
                Ok(VaderValue::List(result))
            }
            _ => Err(format!("No se puede sumar {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn subtract(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => Ok(VaderValue::Number(a - b)),
            _ => Err(format!("No se puede restar {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn multiply(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => Ok(VaderValue::Number(a * b)),
            (VaderValue::String(s), VaderValue::Number(n)) => {
                if *n >= 0.0 && n.fract() == 0.0 {
                    Ok(VaderValue::String(s.repeat(*n as usize)))
                } else {
                    Err("Solo se puede multiplicar string por entero positivo".to_string())
                }
            }
            _ => Err(format!("No se puede multiplicar {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn divide(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => {
                if *b == 0.0 {
                    Err("División por cero".to_string())
                } else {
                    Ok(VaderValue::Number(a / b))
                }
            }
            _ => Err(format!("No se puede dividir {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn modulo(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => {
                if *b == 0.0 {
                    Err("Módulo por cero".to_string())
                } else {
                    Ok(VaderValue::Number(a % b))
                }
            }
            _ => Err(format!("No se puede calcular módulo de {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn power(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => Ok(VaderValue::Number(a.powf(*b))),
            _ => Err(format!("No se puede elevar {} a la potencia {}", self.type_name(), other.type_name())),
        }
    }
    
    pub fn equals(&self, other: &VaderValue) -> bool {
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => (a - b).abs() < f64::EPSILON,
            (VaderValue::String(a), VaderValue::String(b)) => a == b,
            (VaderValue::Boolean(a), VaderValue::Boolean(b)) => a == b,
            (VaderValue::Null, VaderValue::Null) => true,
            _ => false,
        }
    }
    
    pub fn compare(&self, other: &VaderValue) -> Result<std::cmp::Ordering, String> {
        use std::cmp::Ordering;
        
        match (self, other) {
            (VaderValue::Number(a), VaderValue::Number(b)) => Ok(a.partial_cmp(b).unwrap_or(Ordering::Equal)),
            (VaderValue::String(a), VaderValue::String(b)) => Ok(a.cmp(b)),
            _ => Err(format!("No se puede comparar {} y {}", self.type_name(), other.type_name())),
        }
    }
    
    // Métodos de comparación específicos
    pub fn less_than(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match self.compare(other)? {
            std::cmp::Ordering::Less => Ok(VaderValue::Boolean(true)),
            _ => Ok(VaderValue::Boolean(false)),
        }
    }
    
    pub fn less_equal(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match self.compare(other)? {
            std::cmp::Ordering::Less | std::cmp::Ordering::Equal => Ok(VaderValue::Boolean(true)),
            _ => Ok(VaderValue::Boolean(false)),
        }
    }
    
    pub fn greater_than(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match self.compare(other)? {
            std::cmp::Ordering::Greater => Ok(VaderValue::Boolean(true)),
            _ => Ok(VaderValue::Boolean(false)),
        }
    }
    
    pub fn greater_equal(&self, other: &VaderValue) -> Result<VaderValue, String> {
        match self.compare(other)? {
            std::cmp::Ordering::Greater | std::cmp::Ordering::Equal => Ok(VaderValue::Boolean(true)),
            _ => Ok(VaderValue::Boolean(false)),
        }
    }
    
    // Método de negación
    pub fn negate(&self) -> Result<VaderValue, String> {
        match self {
            VaderValue::Number(n) => Ok(VaderValue::Number(-n)),
            VaderValue::Boolean(b) => Ok(VaderValue::Boolean(!b)),
            _ => Err(format!("No se puede negar {}", self.type_name())),
        }
    }
    
    // Alias para el método index (compatibilidad)
    pub fn get_index(&self, index: &VaderValue) -> Result<VaderValue, String> {
        self.index(index)
    }
    
    pub fn index(&self, index: &VaderValue) -> Result<VaderValue, String> {
        match (self, index) {
            (VaderValue::List(list), VaderValue::Number(n)) => {
                let idx = *n as usize;
                if idx < list.len() {
                    Ok(list[idx].clone())
                } else {
                    Err(format!("Índice {} fuera de rango para lista de {} elementos", idx, list.len()))
                }
            }
            (VaderValue::Dict(dict), VaderValue::String(key)) => {
                dict.get(key).cloned().ok_or_else(|| format!("Clave '{}' no encontrada", key))
            }
            (VaderValue::String(s), VaderValue::Number(n)) => {
                let idx = *n as usize;
                let chars: Vec<char> = s.chars().collect();
                if idx < chars.len() {
                    Ok(VaderValue::String(chars[idx].to_string()))
                } else {
                    Err(format!("Índice {} fuera de rango para string de {} caracteres", idx, chars.len()))
                }
            }
            _ => Err(format!("No se puede indexar {} con {}", self.type_name(), index.type_name())),
        }
    }
    
    pub fn set_index(&mut self, index: &VaderValue, value: VaderValue) -> Result<(), String> {
        let self_type = self.type_name();
        let index_type = index.type_name();
        
        match (self, index) {
            (VaderValue::List(list), VaderValue::Number(n)) => {
                let idx = *n as usize;
                if idx < list.len() {
                    list[idx] = value;
                    Ok(())
                } else {
                    Err(format!("Índice {} fuera de rango para lista de {} elementos", idx, list.len()))
                }
            }
            (VaderValue::Dict(dict), VaderValue::String(key)) => {
                dict.insert(key.clone(), value);
                Ok(())
            }
            _ => Err(format!("No se puede asignar índice {} en {}", index_type, self_type)),
        }
    }
    
    pub fn get_member(&self, name: &str) -> Result<VaderValue, String> {
        match self {
            VaderValue::Object { fields, .. } => {
                fields.get(name).cloned().ok_or_else(|| format!("Propiedad '{}' no encontrada", name))
            }
            VaderValue::List(_) => {
                match name {
                    "longitud" | "length" => Ok(VaderValue::Number(self.len() as f64)),
                    _ => Err(format!("Lista no tiene propiedad '{}'", name)),
                }
            }
            VaderValue::String(_) => {
                match name {
                    "longitud" | "length" => Ok(VaderValue::Number(self.len() as f64)),
                    _ => Err(format!("String no tiene propiedad '{}'", name)),
                }
            }
            _ => Err(format!("{} no tiene propiedades", self.type_name())),
        }
    }
    
    pub fn set_member(&mut self, name: &str, value: VaderValue) -> Result<(), String> {
        match self {
            VaderValue::Object { fields, .. } => {
                fields.insert(name.to_string(), value);
                Ok(())
            }
            _ => Err(format!("No se puede asignar propiedad '{}' a {}", name, self.type_name())),
        }
    }
    
    pub fn len(&self) -> usize {
        match self {
            VaderValue::String(s) => s.chars().count(),
            VaderValue::List(l) => l.len(),
            VaderValue::Dict(d) => d.len(),
            _ => 0,
        }
    }
    
    pub fn is_iterable(&self) -> bool {
        matches!(self, VaderValue::List(_) | VaderValue::Dict(_) | VaderValue::String(_) | VaderValue::Range { .. })
    }
    
    pub fn iter(&self) -> Result<Vec<VaderValue>, String> {
        match self {
            VaderValue::List(list) => Ok(list.clone()),
            VaderValue::String(s) => {
                Ok(s.chars().map(|c| VaderValue::String(c.to_string())).collect())
            }
            VaderValue::Dict(dict) => {
                Ok(dict.keys().map(|k| VaderValue::String(k.clone())).collect())
            }
            VaderValue::Range { start, end, step } => {
                let mut result = Vec::new();
                let mut current = *start;
                
                if *step > 0 {
                    while current < *end {
                        result.push(VaderValue::Number(current as f64));
                        current += step;
                    }
                } else if *step < 0 {
                    while current > *end {
                        result.push(VaderValue::Number(current as f64));
                        current += step;
                    }
                }
                
                Ok(result)
            }
            _ => Err(format!("{} no es iterable", self.type_name())),
        }
    }
}

impl fmt::Display for VaderValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

// Funciones de utilidad para crear valores
impl VaderValue {
    pub fn range(start: i64, end: i64) -> Self {
        VaderValue::Range { start, end, step: 1 }
    }
    
    pub fn range_with_step(start: i64, end: i64, step: i64) -> Self {
        VaderValue::Range { start, end, step }
    }
    
    pub fn empty_list() -> Self {
        VaderValue::List(Vec::new())
    }
    
    pub fn empty_dict() -> Self {
        VaderValue::Dict(HashMap::new())
    }
    
    pub fn from_bool(b: bool) -> Self {
        VaderValue::Boolean(b)
    }
    
    pub fn from_str(s: &str) -> Self {
        VaderValue::String(s.to_string())
    }
    
    pub fn from_number(n: f64) -> Self {
        VaderValue::Number(n)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_arithmetic() {
        let a = VaderValue::Number(10.0);
        let b = VaderValue::Number(5.0);
        
        assert_eq!(a.add(&b).unwrap(), VaderValue::Number(15.0));
        assert_eq!(a.subtract(&b).unwrap(), VaderValue::Number(5.0));
        assert_eq!(a.multiply(&b).unwrap(), VaderValue::Number(50.0));
        assert_eq!(a.divide(&b).unwrap(), VaderValue::Number(2.0));
    }
    
    #[test]
    fn test_string_operations() {
        let hello = VaderValue::String("Hola".to_string());
        let world = VaderValue::String(" mundo".to_string());
        
        let result = hello.add(&world).unwrap();
        assert_eq!(result, VaderValue::String("Hola mundo".to_string()));
    }
    
    #[test]
    fn test_truthiness() {
        assert!(VaderValue::Boolean(true).is_truthy());
        assert!(!VaderValue::Boolean(false).is_truthy());
        assert!(!VaderValue::Null.is_truthy());
        assert!(VaderValue::Number(1.0).is_truthy());
        assert!(!VaderValue::Number(0.0).is_truthy());
    }
    
    #[test]
    fn test_list_indexing() {
        let list = VaderValue::List(vec![
            VaderValue::Number(1.0),
            VaderValue::Number(2.0),
            VaderValue::Number(3.0),
        ]);
        
        let index = VaderValue::Number(1.0);
        let result = list.index(&index).unwrap();
        assert_eq!(result, VaderValue::Number(2.0));
    }
}
