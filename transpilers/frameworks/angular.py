"""
Framework Angular para Vader
"""

class AngularFramework:
    def __init__(self):
        self.name = "Angular"
        self.description = "Framework empresarial para aplicaciones web"
        self.target_language = "typescript"
        self.keywords = ['angular', 'componente', 'servicio', 'directiva']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return """import { Component } from '@angular/core';

@Component({
  selector: 'app-vader',
  template: `
    <div class="vader-component">
      <h1>Componente Angular desde Vader</h1>
      <p>{{ message }}</p>
    </div>
  `,
  styleUrls: ['./vader.component.css']
})
export class VaderComponent {
  message = 'Generado desde código Vader';
}"""
