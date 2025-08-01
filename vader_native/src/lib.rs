/*!
🚀 VADER NATIVE RUNTIME - LIBRERÍA PRINCIPAL
==========================================

Runtime nativo completo de Vader implementado en Rust para
máximo rendimiento y compatibilidad multiplataforma.

Autor: Adriano & Cascade AI
*/

pub mod lexer;
pub mod parser;
pub mod types;
pub mod interpreter;
pub mod compiler;
pub mod stdlib;

// Re-exportar tipos principales para facilitar el uso
pub use lexer::{VaderLexer, Token, TokenType, LexError};
pub use parser::{VaderParser, AstNode, ParseError};
pub use types::{VaderValue, TypeError};
pub use interpreter::{VaderInterpreter, RuntimeError};
pub use compiler::{VaderCompiler, CompileError};
pub use stdlib::VaderStdlib;

/// Versión del runtime nativo de Vader
pub const VERSION: &str = "1.0.0";

/// Información del runtime
pub fn runtime_info() -> String {
    format!("Vader Native Runtime v{} - Rust Edition", VERSION)
}
