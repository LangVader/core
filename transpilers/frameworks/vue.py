"""
Framework Vue.js para Vader
"""

class VueFramework:
    def __init__(self):
        self.name = "Vue.js"
        self.description = "Framework progresivo para interfaces de usuario"
        self.target_language = "javascript"
        self.keywords = ['vue', 'componente', 'reactivo', 'template']
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        return f"""<template>
  <div class="vader-component">
    <h1>Componente Vue desde Vader</h1>
    <p>{{{{ message }}}}</p>
  </div>
</template>

<script>
export default {{
  name: 'VaderComponent',
  data() {{
    return {{
      message: 'Generado desde código Vader'
    }}
  }}
}}
</script>

<style scoped>
.vader-component {{
  padding: 20px;
}}
</style>"""
