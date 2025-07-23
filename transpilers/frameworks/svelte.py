"""
Framework Svelte para Vader
"""

class SvelteFramework:
    def __init__(self):
        self.name = "Svelte"
        self.description = "Framework reactivo compilado"
        self.target_language = "javascript"
        self.keywords = ['svelte', 'reactivo', 'componente']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return """<script>
  let message = 'Componente Svelte desde Vader';
</script>

<div class="vader-component">
  <h1>{message}</h1>
  <p>Generado desde código Vader</p>
</div>

<style>
  .vader-component {
    padding: 20px;
  }
</style>"""
