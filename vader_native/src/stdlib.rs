/*!
📚 VADER STANDARD LIBRARY - LIBRERÍA ESTÁNDAR NATIVA
=================================================

Implementación completa de la librería estándar de Vader con funciones
nativas optimizadas para máximo rendimiento.

Autor: Adriano & Cascade AI
*/

use crate::types::VaderValue;
use std::collections::HashMap;
use std::fs;
use std::io::{self, Write};
use std::time::{SystemTime, UNIX_EPOCH};

pub struct VaderStdlib {
    functions: HashMap<String, fn(&[VaderValue]) -> Result<VaderValue, String>>,
}

impl VaderStdlib {
    pub fn new() -> Self {
        let mut stdlib = Self {
            functions: HashMap::new(),
        };
        
        stdlib.register_core_functions();
        stdlib.register_io_functions();
        stdlib.register_string_functions();
        stdlib.register_math_functions();
        stdlib.register_collection_functions();
        stdlib.register_system_functions();
        
        stdlib
    }
    
    pub fn get_function(&self, name: &str) -> Option<&fn(&[VaderValue]) -> Result<VaderValue, String>> {
        self.functions.get(name)
    }
    
    pub fn list_functions(&self) -> Vec<&String> {
        self.functions.keys().collect()
    }
    
    // ===== FUNCIONES CORE =====
    fn register_core_functions(&mut self) {
        // Función print/decir
        self.functions.insert("print".to_string(), |args| {
            let output = args.iter()
                .map(|v| v.to_string())
                .collect::<Vec<_>>()
                .join(" ");
            println!("{}", output);
            Ok(VaderValue::Null)
        });
        
        self.functions.insert("decir".to_string(), |args| {
            let output = args.iter()
                .map(|v| v.to_string())
                .collect::<Vec<_>>()
                .join(" ");
            println!("{}", output);
            // Retornar el string concatenado en lugar de Null
            Ok(VaderValue::String(output))
        });
        
        // Función type/tipo
        self.functions.insert("type".to_string(), |args| {
            if args.is_empty() {
                return Err("type() requiere al menos un argumento".to_string());
            }
            let type_name = match &args[0] {
                VaderValue::Number(_) => "numero",
                VaderValue::String(_) => "texto",
                VaderValue::Boolean(_) => "booleano",
                VaderValue::List(_) => "lista",
                VaderValue::Dict(_) => "diccionario",
                VaderValue::Object { .. } => "objeto",
                VaderValue::Function { .. } => "funcion",
                VaderValue::Range { .. } => "rango",
                VaderValue::Null => "nulo",
            };
            Ok(VaderValue::String(type_name.to_string()))
        });
        
        // Función len/longitud
        self.functions.insert("len".to_string(), |args| {
            if args.is_empty() {
                return Err("len() requiere un argumento".to_string());
            }
            let length = match &args[0] {
                VaderValue::String(s) => s.len(),
                VaderValue::List(l) => l.len(),
                VaderValue::Dict(d) => d.len(),
                VaderValue::Object { fields, .. } => fields.len(),
                _ => return Err("len() solo funciona con texto, listas, diccionarios u objetos".to_string()),
            };
            Ok(VaderValue::Number(length as f64))
        });
        
        self.functions.insert("longitud".to_string(), |args| {
            if args.is_empty() {
                return Err("longitud() requiere un argumento".to_string());
            }
            let length = match &args[0] {
                VaderValue::String(s) => s.len(),
                VaderValue::List(l) => l.len(),
                VaderValue::Dict(d) => d.len(),
                VaderValue::Object { fields, .. } => fields.len(),
                _ => return Err("longitud() solo funciona con texto, listas, diccionarios u objetos".to_string()),
            };
            Ok(VaderValue::Number(length as f64))
        });
    }
    
    // ===== FUNCIONES I/O =====
    fn register_io_functions(&mut self) {
        // Función input/leer
        self.functions.insert("input".to_string(), |args| {
            if !args.is_empty() {
                print!("{}", args[0].to_string());
                io::stdout().flush().unwrap();
            }
            let mut input = String::new();
            io::stdin().read_line(&mut input).map_err(|e| e.to_string())?;
            Ok(VaderValue::String(input.trim().to_string()))
        });
        
        self.functions.insert("leer".to_string(), |args| {
            if !args.is_empty() {
                print!("{}", args[0].to_string());
                io::stdout().flush().unwrap();
            }
            let mut input = String::new();
            io::stdin().read_line(&mut input).map_err(|e| e.to_string())?;
            Ok(VaderValue::String(input.trim().to_string()))
        });
        
        // Función read_file/leer_archivo
        self.functions.insert("read_file".to_string(), |args| {
            if args.is_empty() {
                return Err("read_file() requiere un nombre de archivo".to_string());
            }
            let filename = args[0].to_string();
            let content = fs::read_to_string(&filename)
                .map_err(|e| format!("Error leyendo archivo '{}': {}", filename, e))?;
            Ok(VaderValue::String(content))
        });
        
        self.functions.insert("leer_archivo".to_string(), |args| {
            if args.is_empty() {
                return Err("leer_archivo() requiere un nombre de archivo".to_string());
            }
            let filename = args[0].to_string();
            let content = fs::read_to_string(&filename)
                .map_err(|e| format!("Error leyendo archivo '{}': {}", filename, e))?;
            Ok(VaderValue::String(content))
        });
        
        // Función write_file/escribir_archivo
        self.functions.insert("write_file".to_string(), |args| {
            if args.len() < 2 {
                return Err("write_file() requiere nombre de archivo y contenido".to_string());
            }
            let filename = args[0].to_string();
            let content = args[1].to_string();
            fs::write(&filename, content)
                .map_err(|e| format!("Error escribiendo archivo '{}': {}", filename, e))?;
            Ok(VaderValue::Boolean(true))
        });
    }
    
    // ===== FUNCIONES DE TEXTO =====
    fn register_string_functions(&mut self) {
        // Función upper/mayusculas
        self.functions.insert("upper".to_string(), |args| {
            if args.is_empty() {
                return Err("upper() requiere un argumento de texto".to_string());
            }
            let text = args[0].to_string().to_uppercase();
            Ok(VaderValue::String(text))
        });
        
        self.functions.insert("mayusculas".to_string(), |args| {
            if args.is_empty() {
                return Err("mayusculas() requiere un argumento de texto".to_string());
            }
            let text = args[0].to_string().to_uppercase();
            Ok(VaderValue::String(text))
        });
        
        // Función lower/minusculas
        self.functions.insert("lower".to_string(), |args| {
            if args.is_empty() {
                return Err("lower() requiere un argumento de texto".to_string());
            }
            let text = args[0].to_string().to_lowercase();
            Ok(VaderValue::String(text))
        });
        
        self.functions.insert("minusculas".to_string(), |args| {
            if args.is_empty() {
                return Err("minusculas() requiere un argumento de texto".to_string());
            }
            let text = args[0].to_string().to_lowercase();
            Ok(VaderValue::String(text))
        });
        
        // Función split/dividir
        self.functions.insert("split".to_string(), |args| {
            if args.is_empty() {
                return Err("split() requiere un texto".to_string());
            }
            let text = args[0].to_string();
            let separator = if args.len() > 1 { args[1].to_string() } else { " ".to_string() };
            let parts: Vec<VaderValue> = text.split(&separator)
                .map(|s| VaderValue::String(s.to_string()))
                .collect();
            Ok(VaderValue::List(parts))
        });
    }
    
    // ===== FUNCIONES MATEMÁTICAS =====
    fn register_math_functions(&mut self) {
        // Función abs/absoluto
        self.functions.insert("abs".to_string(), |args| {
            if args.is_empty() {
                return Err("abs() requiere un número".to_string());
            }
            match &args[0] {
                VaderValue::Number(n) => Ok(VaderValue::Number(n.abs())),
                _ => Err("abs() solo funciona con números".to_string()),
            }
        });
        
        // Función sqrt/raiz
        self.functions.insert("sqrt".to_string(), |args| {
            if args.is_empty() {
                return Err("sqrt() requiere un número".to_string());
            }
            match &args[0] {
                VaderValue::Number(n) => {
                    if *n < 0.0 {
                        return Err("sqrt() no puede calcular raíz de número negativo".to_string());
                    }
                    Ok(VaderValue::Number(n.sqrt()))
                },
                _ => Err("sqrt() solo funciona con números".to_string()),
            }
        });
        
        // Función pow/potencia
        self.functions.insert("pow".to_string(), |args| {
            if args.len() < 2 {
                return Err("pow() requiere base y exponente".to_string());
            }
            match (&args[0], &args[1]) {
                (VaderValue::Number(base), VaderValue::Number(exp)) => {
                    Ok(VaderValue::Number(base.powf(*exp)))
                },
                _ => Err("pow() solo funciona con números".to_string()),
            }
        });
        
        // Función random/aleatorio
        self.functions.insert("random".to_string(), |_args| {
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            
            let mut hasher = DefaultHasher::new();
            SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos().hash(&mut hasher);
            let hash = hasher.finish();
            let random_val = (hash % 1000000) as f64 / 1000000.0;
            Ok(VaderValue::Number(random_val))
        });
    }
    
    // ===== FUNCIONES DE COLECCIONES =====
    fn register_collection_functions(&mut self) {
        // Función push/agregar
        self.functions.insert("push".to_string(), |args| {
            if args.len() < 2 {
                return Err("push() requiere lista y elemento".to_string());
            }
            match &args[0] {
                VaderValue::List(list) => {
                    let mut new_list = list.clone();
                    new_list.push(args[1].clone());
                    Ok(VaderValue::List(new_list))
                },
                _ => Err("push() solo funciona con listas".to_string()),
            }
        });
        
        // Función pop/quitar
        self.functions.insert("pop".to_string(), |args| {
            if args.is_empty() {
                return Err("pop() requiere una lista".to_string());
            }
            match &args[0] {
                VaderValue::List(list) => {
                    if list.is_empty() {
                        return Err("No se puede hacer pop() de lista vacía".to_string());
                    }
                    let mut new_list = list.clone();
                    let popped = new_list.pop().unwrap();
                    Ok(popped)
                },
                _ => Err("pop() solo funciona con listas".to_string()),
            }
        });
        
        // Función reverse/invertir
        self.functions.insert("reverse".to_string(), |args| {
            if args.is_empty() {
                return Err("reverse() requiere una lista".to_string());
            }
            match &args[0] {
                VaderValue::List(list) => {
                    let mut new_list = list.clone();
                    new_list.reverse();
                    Ok(VaderValue::List(new_list))
                },
                _ => Err("reverse() solo funciona con listas".to_string()),
            }
        });
    }
    
    // ===== FUNCIONES DE SISTEMA =====
    fn register_system_functions(&mut self) {
        // Función time/tiempo
        self.functions.insert("time".to_string(), |_args| {
            let timestamp = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs() as f64;
            Ok(VaderValue::Number(timestamp))
        });
        
        // Función exit/salir
        self.functions.insert("exit".to_string(), |args| {
            let code = if args.is_empty() { 0 } else {
                match &args[0] {
                    VaderValue::Number(n) => *n as i32,
                    _ => 0,
                }
            };
            std::process::exit(code);
        });
        
        self.functions.insert("salir".to_string(), |args| {
            let code = if args.is_empty() { 0 } else {
                match &args[0] {
                    VaderValue::Number(n) => *n as i32,
                    _ => 0,
                }
            };
            std::process::exit(code);
        });
    }
}

impl Default for VaderStdlib {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_stdlib_functions() {
        let stdlib = VaderStdlib::new();
        
        // Test que las funciones básicas existen
        assert!(stdlib.get_function("print").is_some());
        assert!(stdlib.get_function("decir").is_some());
        assert!(stdlib.get_function("type").is_some());
        assert!(stdlib.get_function("len").is_some());
        
        // Test función type
        let type_fn = stdlib.get_function("type").unwrap();
        let result = type_fn(&[VaderValue::Number(42.0)]).unwrap();
        assert_eq!(result, VaderValue::String("numero".to_string()));
        
        // Test función len
        let len_fn = stdlib.get_function("len").unwrap();
        let result = len_fn(&[VaderValue::String("hola".to_string())]).unwrap();
        assert_eq!(result, VaderValue::Number(4.0));
    }
    
    #[test]
    fn test_math_functions() {
        let stdlib = VaderStdlib::new();
        
        // Test abs
        let abs_fn = stdlib.get_function("abs").unwrap();
        let result = abs_fn(&[VaderValue::Number(-5.0)]).unwrap();
        assert_eq!(result, VaderValue::Number(5.0));
        
        // Test sqrt
        let sqrt_fn = stdlib.get_function("sqrt").unwrap();
        let result = sqrt_fn(&[VaderValue::Number(16.0)]).unwrap();
        assert_eq!(result, VaderValue::Number(4.0));
    }
}
