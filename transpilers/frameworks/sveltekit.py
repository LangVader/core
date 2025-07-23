"""
Framework SvelteKit para Vader
"""

class SvelteKitFramework:
    def __init__(self):
        self.name = "SvelteKit"
        self.description = "Framework full-stack de Svelte"
        self.target_language = "javascript"
        self.keywords = ['sveltekit', 'kit', 'fullstack']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return """<script>
  let message = 'Página SvelteKit desde Vader';
</script>

<svelte:head>
  <title>Vader SvelteKit</title>
</svelte:head>

<div class="vader-page">
  <h1>{message}</h1>
  <p>Generado desde código Vader</p>
</div>

<style>
  .vader-page {
    padding: 20px;
  }
</style>"""
