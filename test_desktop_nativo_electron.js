// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL DESKTOP
const { app, BrowserWindow, Menu, dialog } = require('electron');
const path = require('path');

class VaderElectronApp {
    constructor() {
        this.mainWindow = null;
        this.initializeApp();
    }
    
    initializeApp() {
        console.log('🚀 VADER 7.0 - Electron Desktop Runtime');
        
        app.whenReady().then(() => {
            this.createMainWindow();
            this.setupMenu();
        });
        
        app.on('window-all-closed', () => {
            if (process.platform !== 'darwin') app.quit();
        });
    }
    
    createMainWindow() {
        this.mainWindow = new BrowserWindow({
            width: 1200,
            height: 800,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false
            }
        });
        
        this.mainWindow.loadFile('index.html');
    }
    
    setupMenu() {
        const template = [
            {
                label: 'Archivo',
                submenu: [
                    { label: 'Nuevo', accelerator: 'CmdOrCtrl+N' },
                    { label: 'Abrir', accelerator: 'CmdOrCtrl+O' },
                    { label: 'Guardar', accelerator: 'CmdOrCtrl+S' },
                    { type: 'separator' },
                    { label: 'Salir', role: 'quit' }
                ]
            }
        ];
        
        const menu = Menu.buildFromTemplate(template);
        Menu.setApplicationMenu(menu);
    }
}

new VaderElectronApp();