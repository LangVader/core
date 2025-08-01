/*!
🚀 VADER NATIVE - LENGUAJE DE PROGRAMACIÓN REAL
==============================================

Runtime nativo de Vader implementado en Rust para producción.
Incluye lexer, parser, intérprete y compilador LLVM.

Autor: Adriano & Cascade AI
Versión: 1.0.0 Native Runtime
*/

use clap::{Parser, Subcommand};
use colored::*;
use std::fs;
use std::path::PathBuf;

mod lexer;
mod parser;
mod interpreter;
mod compiler;
mod types;
mod stdlib;

use crate::lexer::VaderLexer;
use crate::parser::VaderParser;
use crate::interpreter::VaderInterpreter;
use crate::compiler::VaderCompiler;

#[derive(Parser)]
#[command(name = "vader")]
#[command(about = "Vader - The Ultra-Natural Programming Language")]
#[command(version = "1.0.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Run Vader code directly
    Run {
        /// Vader source file
        file: PathBuf,
        /// Enable debug output
        #[arg(short, long)]
        debug: bool,
    },
    /// Compile Vader code to native binary
    Compile {
        /// Vader source file
        file: PathBuf,
        /// Output binary name
        #[arg(short, long)]
        output: Option<String>,
        /// Optimization level (0-3)
        #[arg(short = 'O', long, default_value = "2")]
        optimization: u8,
    },
    /// Interactive REPL
    Repl {
        /// Enable debug output
        #[arg(short, long)]
        debug: bool,
    },
    /// Check syntax without execution
    Check {
        /// Vader source file
        file: PathBuf,
    },
    /// Show AST for debugging
    Ast {
        /// Vader source file
        file: PathBuf,
    },
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Run { file, debug } => {
            run_vader_file(&file, debug)?;
        }
        Commands::Compile { file, output, optimization } => {
            compile_vader_file(&file, output, optimization)?;
        }
        Commands::Repl { debug } => {
            start_repl(debug)?;
        }
        Commands::Check { file } => {
            check_vader_file(&file)?;
        }
        Commands::Ast { file } => {
            show_ast(&file)?;
        }
    }

    Ok(())
}

fn run_vader_file(file: &PathBuf, debug: bool) -> anyhow::Result<()> {
    println!("{}", "🚀 Vader Native Runtime".bright_cyan().bold());
    
    // Leer archivo
    let source = fs::read_to_string(file)?;
    
    if debug {
        println!("{} {}", "📁 Archivo:".bright_blue(), file.display());
        println!("{} {} líneas", "📊 Código:".bright_blue(), source.lines().count());
    }
    
    // Lexer
    let mut lexer = VaderLexer::new(&source);
    let tokens = lexer.tokenize()?;
    
    if debug {
        println!("{} {} tokens", "🔤 Tokens:".bright_blue(), tokens.len());
    }
    
    // Parser
    let mut parser = VaderParser::new(tokens);
    let ast = parser.parse()?;
    
    if debug {
        println!("{} AST generado", "🌳 Parser:".bright_blue());
    }
    
    // Intérprete
    let mut interpreter = VaderInterpreter::new();
    interpreter.execute(ast)?;
    
    println!("{}", "✅ Ejecución completada".bright_green());
    Ok(())
}

fn compile_vader_file(file: &PathBuf, output: Option<String>, optimization: u8) -> anyhow::Result<()> {
    println!("{}", "⚡ Vader Native Compiler".bright_yellow().bold());
    
    let source = fs::read_to_string(file)?;
    let output_name = output.unwrap_or_else(|| {
        file.file_stem()
            .unwrap_or_default()
            .to_string_lossy()
            .to_string()
    });
    
    println!("{} {}", "📁 Compilando:".bright_blue(), file.display());
    println!("{} {}", "📦 Salida:".bright_blue(), output_name);
    println!("{} O{}", "🔧 Optimización:".bright_blue(), optimization);
    
    // Lexer + Parser
    let mut lexer = VaderLexer::new(&source);
    let tokens = lexer.tokenize()?;
    let mut parser = VaderParser::new(tokens);
    let ast = parser.parse()?;
    
    // Compilador LLVM
    let mut compiler = VaderCompiler::new(optimization);
    compiler.compile(ast, &output_name)?;
    
    println!("{} {}", "✅ Compilación exitosa:".bright_green(), output_name);
    Ok(())
}

fn start_repl(debug: bool) -> anyhow::Result<()> {
    println!("{}", "🎮 Vader Interactive REPL".bright_magenta().bold());
    println!("{}", "Escribe código Vader y presiona Enter. 'salir' para terminar.".dimmed());
    
    let mut interpreter = VaderInterpreter::new();
    
    loop {
        print!("{} ", "vader>".bright_cyan());
        use std::io::{self, Write};
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        if input == "salir" || input == "exit" {
            break;
        }
        
        if input.is_empty() {
            continue;
        }
        
        match execute_line(input, &mut interpreter, debug) {
            Ok(_) => {}
            Err(e) => {
                println!("{} {}", "❌ Error:".bright_red(), e);
            }
        }
    }
    
    println!("{}", "👋 ¡Hasta luego!".bright_green());
    Ok(())
}

fn execute_line(input: &str, interpreter: &mut VaderInterpreter, debug: bool) -> anyhow::Result<()> {
    let mut lexer = VaderLexer::new(input);
    let tokens = lexer.tokenize()?;
    
    if debug {
        println!("{} {:?}", "🔤 Tokens:".dimmed(), tokens);
    }
    
    let mut parser = VaderParser::new(tokens);
    let ast = parser.parse()?;
    
    if debug {
        println!("{} {:#?}", "🌳 AST:".dimmed(), ast);
    }
    
    interpreter.execute(ast)?;
    Ok(())
}

fn check_vader_file(file: &PathBuf) -> anyhow::Result<()> {
    println!("{}", "🔍 Vader Syntax Checker".bright_blue().bold());
    
    let source = fs::read_to_string(file)?;
    
    // Solo lexer + parser para verificar sintaxis
    let mut lexer = VaderLexer::new(&source);
    let tokens = lexer.tokenize()?;
    let mut parser = VaderParser::new(tokens);
    let _ast = parser.parse()?;
    
    println!("{} Sintaxis correcta", "✅".bright_green());
    Ok(())
}

fn show_ast(file: &PathBuf) -> anyhow::Result<()> {
    println!("{}", "🌳 Vader AST Viewer".bright_purple().bold());
    
    let source = fs::read_to_string(file)?;
    let mut lexer = VaderLexer::new(&source);
    let tokens = lexer.tokenize()?;
    let mut parser = VaderParser::new(tokens);
    let ast = parser.parse()?;
    
    println!("{}", "📊 Abstract Syntax Tree:".bright_blue());
    println!("{:#?}", ast);
    
    Ok(())
}
