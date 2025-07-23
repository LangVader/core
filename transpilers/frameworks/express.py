"""
Framework Express.js para Vader
"""

class ExpressFramework:
    def __init__(self):
        self.name = "Express.js"
        self.description = "Framework web para Node.js"
        self.target_language = "javascript"
        self.keywords = ['express', 'servidor', 'api', 'ruta', 'middleware']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return """const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'API generada desde código Vader' });
});

app.listen(port, () => {
  console.log(`Servidor ejecutándose en http://localhost:${port}`);
});"""
