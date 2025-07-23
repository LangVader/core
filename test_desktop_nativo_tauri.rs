// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL DESKTOP
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("¡Hola, {}! Desde Vader Desktop", name)
}

fn main() {
    println!("🚀 VADER 7.0 - Tauri Desktop Runtime");
    
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            window.set_title("Vader Desktop App").unwrap();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Error ejecutando la aplicación");
}