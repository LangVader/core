"""
Framework Express.js para Vader
"""

class ExpressFramework:
    def __init__(self):
        self.name = "Express.js"
        self.description = "Framework backend completo para Node.js con APIs REST"
        self.target_language = "javascript"
        self.keywords = [
            'express', 'servidor', 'api', 'ruta', 'middleware', 'endpoint',
            'get', 'post', 'put', 'delete', 'patch', 'cors', 'auth', 'jwt',
            'session', 'cookie', 'upload', 'file', 'database', 'mongo',
            'mysql', 'postgres', 'redis', 'cache', 'validation', 'error',
            'logging', 'helmet', 'security', 'rate', 'limit', 'swagger',
            'documentation', 'test', 'socket', 'websocket', 'cluster'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Express.js con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_auth = any('auth' in line.lower() or 'jwt' in line.lower() or 'session' in line.lower() for line in lines)
        uses_database = any('database' in line.lower() or 'mongo' in line.lower() or 'mysql' in line.lower() for line in lines)
        uses_cors = any('cors' in line.lower() or 'cross' in line.lower() for line in lines)
        uses_upload = any('upload' in line.lower() or 'file' in line.lower() for line in lines)
        uses_validation = any('validation' in line.lower() or 'validate' in line.lower() for line in lines)
        uses_swagger = any('swagger' in line.lower() or 'documentation' in line.lower() for line in lines)
        uses_websocket = any('socket' in line.lower() or 'websocket' in line.lower() for line in lines)
        uses_cache = any('cache' in line.lower() or 'redis' in line.lower() for line in lines)
        uses_security = any('security' in line.lower() or 'helmet' in line.lower() or 'rate' in line.lower() for line in lines)
        
        # Detectar métodos HTTP
        has_get = any('get' in line.lower() or 'obtener' in line.lower() for line in lines)
        has_post = any('post' in line.lower() or 'crear' in line.lower() for line in lines)
        has_put = any('put' in line.lower() or 'actualizar' in line.lower() for line in lines)
        has_delete = any('delete' in line.lower() or 'eliminar' in line.lower() for line in lines)
        
        # Detectar puerto personalizado
        port = "3000"
        for line in lines:
            if 'puerto' in line.lower() or 'port' in line.lower():
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        port = part
                        break
        
        # Construir código Express
        express_code = []
        
        # Imports y dependencias
        express_code.append("// Dependencias principales")
        express_code.append("const express = require('express');")
        
        if uses_cors:
            express_code.append("const cors = require('cors');")
        
        if uses_auth:
            express_code.append("const jwt = require('jsonwebtoken');")
            express_code.append("const bcrypt = require('bcrypt');")
            express_code.append("const session = require('express-session');")
        
        if uses_database:
            express_code.append("const mongoose = require('mongoose'); // MongoDB")
            express_code.append("const mysql = require('mysql2/promise'); // MySQL")
        
        if uses_upload:
            express_code.append("const multer = require('multer');")
            express_code.append("const path = require('path');")
        
        if uses_validation:
            express_code.append("const { body, validationResult } = require('express-validator');")
        
        if uses_security:
            express_code.append("const helmet = require('helmet');")
            express_code.append("const rateLimit = require('express-rate-limit');")
        
        if uses_cache:
            express_code.append("const redis = require('redis');")
        
        if uses_websocket:
            express_code.append("const http = require('http');")
            express_code.append("const socketIo = require('socket.io');")
        
        if uses_swagger:
            express_code.append("const swaggerJsdoc = require('swagger-jsdoc');")
            express_code.append("const swaggerUi = require('swagger-ui-express');")
        
        express_code.append("")
        
        # Configuración de la app
        express_code.append("// Configuración de Express")
        express_code.append("const app = express();")
        express_code.append(f"const PORT = process.env.PORT || {port};")
        
        if uses_websocket:
            express_code.append("const server = http.createServer(app);")
            express_code.append("const io = socketIo(server);")
        
        express_code.append("")
        
        # Middlewares globales
        express_code.append("// Middlewares globales")
        express_code.append("app.use(express.json({ limit: '10mb' }));")
        express_code.append("app.use(express.urlencoded({ extended: true }));")
        
        if uses_cors:
            express_code.append("app.use(cors());")
        
        if uses_security:
            express_code.append("app.use(helmet());")
            express_code.append("const limiter = rateLimit({")
            express_code.append("  windowMs: 15 * 60 * 1000,")
            express_code.append("  max: 100")
            express_code.append("});")
            express_code.append("app.use(limiter);")
        
        if uses_auth:
            express_code.append("")
            express_code.append("// Middleware de autenticación")
            express_code.append("const authenticateToken = (req, res, next) => {")
            express_code.append("  const authHeader = req.headers['authorization'];")
            express_code.append("  const token = authHeader && authHeader.split(' ')[1];")
            express_code.append("  if (!token) return res.status(401).json({ error: 'Token requerido' });")
            express_code.append("  jwt.verify(token, process.env.JWT_SECRET || 'secret', (err, user) => {")
            express_code.append("    if (err) return res.status(403).json({ error: 'Token inválido' });")
            express_code.append("    req.user = user;")
            express_code.append("    next();")
            express_code.append("  });")
            express_code.append("};")
        
        express_code.append("")
        
        # Rutas principales
        express_code.append("// Rutas principales")
        express_code.append("app.get('/', (req, res) => {")
        express_code.append("  res.json({")
        express_code.append("    message: 'API Vader Express.js',")
        express_code.append("    version: '1.0.0',")
        express_code.append("    status: 'active'")
        express_code.append("  });")
        express_code.append("});")
        express_code.append("")
        
        # Rutas CRUD
        if has_get:
            auth_middleware = "authenticateToken, " if uses_auth else ""
            express_code.append(f"app.get('/api/data', {auth_middleware}async (req, res) => {{")
            express_code.append("  try {")
            express_code.append("    const data = [")
            express_code.append("      { id: 1, name: 'Elemento 1', description: 'Descripción 1' },")
            express_code.append("      { id: 2, name: 'Elemento 2', description: 'Descripción 2' }")
            express_code.append("    ];")
            express_code.append("    res.json({ success: true, data, total: data.length });")
            express_code.append("  } catch (error) {")
            express_code.append("    res.status(500).json({ error: 'Error al obtener datos' });")
            express_code.append("  }")
            express_code.append("});")
            express_code.append("")
        
        if has_post:
            auth_middleware = "authenticateToken, " if uses_auth else ""
            express_code.append(f"app.post('/api/data', {auth_middleware}async (req, res) => {{")
            express_code.append("  try {")
            express_code.append("    const newData = { id: Date.now(), ...req.body, createdAt: new Date() };")
            express_code.append("    res.status(201).json({ success: true, data: newData });")
            express_code.append("  } catch (error) {")
            express_code.append("    res.status(500).json({ error: 'Error al crear datos' });")
            express_code.append("  }")
            express_code.append("});")
            express_code.append("")
        
        if has_put:
            auth_middleware = "authenticateToken, " if uses_auth else ""
            express_code.append(f"app.put('/api/data/:id', {auth_middleware}async (req, res) => {{")
            express_code.append("  try {")
            express_code.append("    const { id } = req.params;")
            express_code.append("    const updatedData = { id, ...req.body, updatedAt: new Date() };")
            express_code.append("    res.json({ success: true, data: updatedData });")
            express_code.append("  } catch (error) {")
            express_code.append("    res.status(500).json({ error: 'Error al actualizar datos' });")
            express_code.append("  }")
            express_code.append("});")
            express_code.append("")
        
        if has_delete:
            auth_middleware = "authenticateToken, " if uses_auth else ""
            express_code.append(f"app.delete('/api/data/:id', {auth_middleware}async (req, res) => {{")
            express_code.append("  try {")
            express_code.append("    const { id } = req.params;")
            express_code.append("    res.json({ success: true, message: `Elemento ${id} eliminado` });")
            express_code.append("  } catch (error) {")
            express_code.append("    res.status(500).json({ error: 'Error al eliminar datos' });")
            express_code.append("  }")
            express_code.append("});")
            express_code.append("")
        
        # Rutas de autenticación
        if uses_auth:
            express_code.append("// Rutas de autenticación")
            express_code.append("app.post('/api/auth/login', async (req, res) => {")
            express_code.append("  try {")
            express_code.append("    const { email, password } = req.body;")
            express_code.append("    // Aquí validarías credenciales con la base de datos")
            express_code.append("    const token = jwt.sign({ email }, process.env.JWT_SECRET || 'secret', { expiresIn: '24h' });")
            express_code.append("    res.json({ success: true, token, user: { email } });")
            express_code.append("  } catch (error) {")
            express_code.append("    res.status(500).json({ error: 'Error en login' });")
            express_code.append("  }")
            express_code.append("});")
            express_code.append("")
        
        # Manejo de errores global
        express_code.append("// Manejo de errores global")
        express_code.append("app.use((err, req, res, next) => {")
        express_code.append("  console.error(err.stack);")
        express_code.append("  res.status(500).json({ error: 'Error interno del servidor' });")
        express_code.append("});")
        express_code.append("")
        
        # Ruta 404
        express_code.append("app.use('*', (req, res) => {")
        express_code.append("  res.status(404).json({ error: 'Ruta no encontrada' });")
        express_code.append("});")
        express_code.append("")
        
        # Iniciar servidor
        if uses_websocket:
            express_code.append("// Iniciar servidor con WebSocket")
            express_code.append("server.listen(PORT, () => {")
            express_code.append("  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);")
            express_code.append("});")
            express_code.append("")
            express_code.append("// WebSocket events")
            express_code.append("io.on('connection', (socket) => {")
            express_code.append("  console.log('Cliente conectado:', socket.id);")
            express_code.append("  socket.on('disconnect', () => {")
            express_code.append("    console.log('Cliente desconectado:', socket.id);")
            express_code.append("  });")
            express_code.append("});")
        else:
            express_code.append("// Iniciar servidor")
            express_code.append("app.listen(PORT, () => {")
            express_code.append("  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);")
            express_code.append("});")
        
        return '\n'.join(express_code)
