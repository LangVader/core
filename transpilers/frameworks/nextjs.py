"""
Framework Next.js para Vader
"""

class NextJSFramework:
    def __init__(self):
        self.name = "Next.js"
        self.description = "Framework React para producción"
        self.target_language = "javascript"
        self.keywords = ['nextjs', 'next', 'pagina', 'ruta', 'api']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return """import { useState } from 'react';

export default function VaderPage() {
  const [data, setData] = useState('');

  return (
    <div className="container">
      <h1>Página Next.js desde Vader</h1>
      <p>Generado desde código Vader</p>
    </div>
  );
}"""
