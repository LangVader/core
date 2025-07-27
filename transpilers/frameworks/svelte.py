"""
Framework Svelte para Vader
"""

class SvelteFramework:
    def __init__(self):
        self.name = "Svelte"
        self.description = "Framework reactivo compilado con compilación optimizada"
        self.target_language = "javascript"
        self.keywords = [
            'svelte', 'reactivo', 'componente', 'store', 'writable', 'readable',
            'derived', 'binding', 'evento', 'lifecycle', 'onMount', 'onDestroy',
            'beforeUpdate', 'afterUpdate', 'tick', 'dispatch', 'createEventDispatcher',
            'bind', 'two-way', 'reactive', 'statement', 'transition', 'animate',
            'motion', 'spring', 'tweened', 'crossfade', 'fly', 'fade', 'slide',
            'scale', 'draw', 'context', 'setContext', 'getContext', 'slot',
            'each', 'if', 'await', 'key', 'debug', 'html', '@html'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Svelte con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_store = any('store' in line.lower() or 'writable' in line.lower() or 'readable' in line.lower() for line in lines)
        uses_lifecycle = any('onMount' in line.lower() or 'onDestroy' in line.lower() or 'lifecycle' in line.lower() for line in lines)
        uses_events = any('evento' in line.lower() or 'dispatch' in line.lower() or 'click' in line.lower() for line in lines)
        uses_binding = any('bind' in line.lower() or 'binding' in line.lower() or 'two-way' in line.lower() for line in lines)
        uses_reactive = any('reactive' in line.lower() or '$:' in line or 'statement' in line.lower() for line in lines)
        uses_transitions = any('transition' in line.lower() or 'animate' in line.lower() or 'fly' in line.lower() for line in lines)
        uses_context = any('context' in line.lower() or 'setContext' in line.lower() or 'getContext' in line.lower() for line in lines)
        
        # Detectar elementos de interfaz
        has_form = any('formulario' in line.lower() or 'form' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() or 'each' in line.lower() for line in lines)
        has_conditional = any('if' in line.lower() or 'condicional' in line.lower() for line in lines)
        
        # Construir código Svelte
        svelte_code = []
        
        # Script section
        svelte_code.append("<script>")
        
        # Imports
        imports = []
        if uses_lifecycle:
            imports.append("import { onMount, onDestroy, beforeUpdate, afterUpdate } from 'svelte';")
        if uses_store:
            imports.append("import { writable, readable, derived } from 'svelte/store';")
        if uses_events:
            imports.append("import { createEventDispatcher } from 'svelte';")
        if uses_transitions:
            imports.append("import { fly, fade, slide, scale } from 'svelte/transition';")
        if uses_context:
            imports.append("import { setContext, getContext } from 'svelte';")
        
        if imports:
            svelte_code.extend(imports)
            svelte_code.append("")
        
        # Event dispatcher
        if uses_events:
            svelte_code.append("  const dispatch = createEventDispatcher();")
            svelte_code.append("")
        
        # Store definitions
        if uses_store:
            svelte_code.append("  // Stores")
            svelte_code.append("  const count = writable(0);")
            svelte_code.append("  const name = writable('');")
            svelte_code.append("  const items = writable([]);")
            svelte_code.append("  const doubled = derived(count, $count => $count * 2);")
            svelte_code.append("")
        
        # Component state
        svelte_code.append("  // Component state")
        svelte_code.append("  let title = 'Aplicación Svelte desde Vader';")
        svelte_code.append("  let loading = false;")
        svelte_code.append("  let error = null;")
        
        if has_form:
            svelte_code.append("  let formData = { name: '', email: '', message: '' };")
        
        if has_list:
            svelte_code.append("  let data = ['Item 1', 'Item 2', 'Item 3'];")
            svelte_code.append("  let newItem = '';")
        
        if has_conditional:
            svelte_code.append("  let showDetails = false;")
        
        svelte_code.append("")
        
        # Reactive statements
        if uses_reactive:
            svelte_code.append("  // Reactive statements")
            svelte_code.append("  $: uppercaseTitle = title.toUpperCase();")
            svelte_code.append("  $: isFormValid = formData.name && formData.email;" if has_form else "  $: isDataEmpty = data.length === 0;")
            svelte_code.append("  $: console.log('Title changed:', title);")
            svelte_code.append("")
        
        # Lifecycle hooks
        if uses_lifecycle:
            svelte_code.append("  // Lifecycle hooks")
            svelte_code.append("  onMount(() => {")
            svelte_code.append("    console.log('Component mounted');")
            svelte_code.append("    loadData();")
            svelte_code.append("  });")
            svelte_code.append("")
            svelte_code.append("  onDestroy(() => {")
            svelte_code.append("    console.log('Component destroyed');")
            svelte_code.append("  });")
            svelte_code.append("")
        
        # Functions
        svelte_code.append("  // Functions")
        
        if has_form:
            svelte_code.append("  async function handleSubmit() {")
            svelte_code.append("    loading = true;")
            svelte_code.append("    error = null;")
            svelte_code.append("    try {")
            svelte_code.append("      const response = await fetch('/api/submit', {")
            svelte_code.append("        method: 'POST',")
            svelte_code.append("        headers: { 'Content-Type': 'application/json' },")
            svelte_code.append("        body: JSON.stringify(formData)")
            svelte_code.append("      });")
            svelte_code.append("      if (!response.ok) throw new Error('Error en el envío');")
            svelte_code.append("      formData = { name: '', email: '', message: '' };")
            svelte_code.append("      dispatch('formSubmitted', { success: true });")
            svelte_code.append("    } catch (err) {")
            svelte_code.append("      error = err.message;")
            svelte_code.append("    } finally {")
            svelte_code.append("      loading = false;")
            svelte_code.append("    }")
            svelte_code.append("  }")
            svelte_code.append("")
        
        if has_list:
            svelte_code.append("  function addItem() {")
            svelte_code.append("    if (newItem.trim()) {")
            svelte_code.append("      data = [...data, newItem.trim()];")
            svelte_code.append("      newItem = '';")
            svelte_code.append("    }")
            svelte_code.append("  }")
            svelte_code.append("")
            svelte_code.append("  function removeItem(index) {")
            svelte_code.append("    data = data.filter((_, i) => i !== index);")
            svelte_code.append("  }")
            svelte_code.append("")
        
        svelte_code.append("  async function loadData() {")
        svelte_code.append("    loading = true;")
        svelte_code.append("    try {")
        svelte_code.append("      // Simulate API call")
        svelte_code.append("      await new Promise(resolve => setTimeout(resolve, 1000));")
        svelte_code.append("      console.log('Data loaded successfully');")
        svelte_code.append("    } catch (err) {")
        svelte_code.append("      error = err.message;")
        svelte_code.append("    } finally {")
        svelte_code.append("      loading = false;")
        svelte_code.append("    }")
        svelte_code.append("  }")
        
        svelte_code.append("</script>")
        svelte_code.append("")
        
        # HTML Template
        svelte_code.append("<main class='vader-app'>")
        svelte_code.append("  <header class='vader-header'>")
        
        if uses_reactive:
            svelte_code.append("    <h1>{uppercaseTitle}</h1>")
        else:
            svelte_code.append("    <h1>{title}</h1>")
        
        if uses_store:
            svelte_code.append("    <div class='store-section'>")
            svelte_code.append("      <p>Contador: {$count}</p>")
            svelte_code.append("      <p>Doble: {$doubled}</p>")
            svelte_code.append("      <button on:click={() => $count += 1}>+</button>")
            svelte_code.append("      <button on:click={() => $count -= 1}>-</button>")
            svelte_code.append("    </div>")
        
        svelte_code.append("  </header>")
        svelte_code.append("")
        
        # Loading state
        svelte_code.append("  {#if loading}")
        if uses_transitions:
            svelte_code.append("    <div class='loading' in:fade>Cargando...</div>")
        else:
            svelte_code.append("    <div class='loading'>Cargando...</div>")
        svelte_code.append("  {:else if error}")
        svelte_code.append("    <div class='error'>Error: {error}</div>")
        svelte_code.append("  {:else}")
        
        # Form section
        if has_form:
            svelte_code.append("    <section class='form-section'>")
            svelte_code.append("      <h2>Formulario</h2>")
            svelte_code.append("      <form on:submit|preventDefault={handleSubmit}>")
            
            if uses_binding:
                svelte_code.append("        <input bind:value={formData.name} placeholder='Nombre' required />")
                svelte_code.append("        <input bind:value={formData.email} type='email' placeholder='Email' required />")
                svelte_code.append("        <textarea bind:value={formData.message} placeholder='Mensaje'></textarea>")
            else:
                svelte_code.append("        <input value={formData.name} on:input={e => formData.name = e.target.value} placeholder='Nombre' required />")
                svelte_code.append("        <input value={formData.email} on:input={e => formData.email = e.target.value} type='email' placeholder='Email' required />")
            
            svelte_code.append("        <button type='submit' disabled={loading || !isFormValid}>")
            svelte_code.append("          {loading ? 'Enviando...' : 'Enviar'}")
            svelte_code.append("        </button>")
            svelte_code.append("      </form>")
            svelte_code.append("    </section>")
        
        # List section
        if has_list:
            svelte_code.append("    <section class='list-section'>")
            svelte_code.append("      <h2>Lista Dinámica</h2>")
            svelte_code.append("      <div class='add-item'>")
            
            if uses_binding:
                svelte_code.append("        <input bind:value={newItem} placeholder='Nuevo elemento' on:keydown={e => e.key === 'Enter' && addItem()} />")
            else:
                svelte_code.append("        <input value={newItem} on:input={e => newItem = e.target.value} placeholder='Nuevo elemento' />")
            
            svelte_code.append("        <button on:click={addItem}>Agregar</button>")
            svelte_code.append("      </div>")
            svelte_code.append("      {#each data as item, index (item)}")
            
            if uses_transitions:
                svelte_code.append("        <div class='list-item' in:fly={{ x: -100 }} out:fade>")
            else:
                svelte_code.append("        <div class='list-item'>")
            
            svelte_code.append("          <span>{item}</span>")
            svelte_code.append("          <button on:click={() => removeItem(index)}>&times;</button>")
            svelte_code.append("        </div>")
            svelte_code.append("      {/each}")
            svelte_code.append("    </section>")
        
        # Conditional section
        if has_conditional:
            svelte_code.append("    <section class='details-section'>")
            svelte_code.append("      <button on:click={() => showDetails = !showDetails}>")
            svelte_code.append("        {showDetails ? 'Ocultar' : 'Mostrar'} Detalles")
            svelte_code.append("      </button>")
            svelte_code.append("      {#if showDetails}")
            
            if uses_transitions:
                svelte_code.append("        <div class='details' in:slide>")
            else:
                svelte_code.append("        <div class='details'>")
            
            svelte_code.append("          <p>Estos son los detalles adicionales de la aplicación.</p>")
            svelte_code.append("          <p>Generado desde código Vader con Svelte.</p>")
            svelte_code.append("        </div>")
            svelte_code.append("      {/if}")
            svelte_code.append("    </section>")
        
        svelte_code.append("  {/if}")
        svelte_code.append("</main>")
        svelte_code.append("")
        
        # Styles
        svelte_code.append("<style>")
        svelte_code.append("  .vader-app { max-width: 1200px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }")
        svelte_code.append("  .vader-header { text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #ff3e00; }")
        svelte_code.append("  .vader-header h1 { color: #ff3e00; font-size: 2.5rem; margin: 0; }")
        svelte_code.append("  .store-section { margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }")
        svelte_code.append("  .store-section button { background: #ff3e00; color: white; border: none; padding: 8px 16px; margin: 0 5px; border-radius: 4px; cursor: pointer; }")
        svelte_code.append("  .store-section button:hover { background: #d63200; }")
        svelte_code.append("  .form-section, .list-section, .details-section { margin: 30px 0; padding: 25px; border: 1px solid #e1e5e9; border-radius: 8px; background: white; }")
        svelte_code.append("  .form-section h2, .list-section h2 { color: #333; margin-top: 0; }")
        svelte_code.append("  .form-section input, .form-section textarea { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }")
        svelte_code.append("  .form-section button { background: #ff3e00; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }")
        svelte_code.append("  .form-section button:hover { background: #d63200; }")
        svelte_code.append("  .form-section button:disabled { background: #ccc; cursor: not-allowed; }")
        svelte_code.append("  .add-item { display: flex; gap: 10px; margin-bottom: 20px; }")
        svelte_code.append("  .add-item input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }")
        svelte_code.append("  .add-item button { background: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }")
        svelte_code.append("  .list-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border: 1px solid #e9ecef; margin-bottom: 8px; border-radius: 6px; background: #f8f9fa; }")
        svelte_code.append("  .list-item button { background: #dc3545; color: white; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; }")
        svelte_code.append("  .details { margin-top: 15px; padding: 20px; background: #e7f3ff; border-radius: 6px; border-left: 4px solid #007bff; }")
        svelte_code.append("  .loading { text-align: center; padding: 40px; font-size: 18px; color: #666; }")
        svelte_code.append("  .error { color: #dc3545; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; padding: 15px; margin: 15px 0; }")
        svelte_code.append("</style>")
        
        return '\n'.join(svelte_code)
