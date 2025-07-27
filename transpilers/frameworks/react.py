"""
Framework React para Vader
Transpila código Vader a componentes React con JSX
"""

class ReactFramework:
    def __init__(self):
        self.name = "React"
        self.description = "Framework completo para crear interfaces de usuario interactivas"
        self.target_language = "javascript"
        self.keywords = [
            'componente', 'react', 'jsx', 'estado', 'hook', 'usestate', 'useeffect',
            'context', 'provider', 'router', 'ruta', 'navegacion', 'formulario',
            'evento', 'click', 'submit', 'ref', 'memo', 'callback', 'lazy',
            'suspense', 'reducer', 'props', 'children', 'key'
        ]
    
    def detect(self, code):
        """Detecta si el código usa React"""
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a React con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        react_code = []
        
        # Detectar funcionalidades avanzadas
        uses_router = any('ruta' in line.lower() or 'navegacion' in line.lower() for line in lines)
        uses_context = any('context' in line.lower() or 'provider' in line.lower() for line in lines)
        uses_forms = any('formulario' in line.lower() or 'submit' in line.lower() for line in lines)
        uses_lazy = any('lazy' in line.lower() or 'suspense' in line.lower() for line in lines)
        uses_reducer = any('reducer' in line.lower() for line in lines)
        
        # Imports avanzados de React
        imports = ["import React, { useState, useEffect, useCallback, useMemo, useRef"]
        if uses_context:
            imports.append(", useContext, createContext")
        if uses_reducer:
            imports.append(", useReducer")
        if uses_lazy:
            imports.append(", lazy, Suspense")
        imports.append(" } from 'react';")
        
        if uses_router:
            react_code.append("import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';")
        
        react_code.append(''.join(imports))
        react_code.append("")
        
        # Context si es necesario
        if uses_context:
            react_code.append("// Context para estado global")
            react_code.append("const VaderContext = createContext();")
            react_code.append("")
            react_code.append("const VaderProvider = ({ children }) => {")
            react_code.append("  const [globalState, setGlobalState] = useState({});")
            react_code.append("  return (")
            react_code.append("    <VaderContext.Provider value={{ globalState, setGlobalState }}>")
            react_code.append("      {children}")
            react_code.append("    </VaderContext.Provider>")
            react_code.append("  );")
            react_code.append("};")
            react_code.append("")
        
        # Reducer si es necesario
        if uses_reducer:
            react_code.append("// Reducer para estado complejo")
            react_code.append("const vaderReducer = (state, action) => {")
            react_code.append("  switch (action.type) {")
            react_code.append("    case 'SET_DATA':")
            react_code.append("      return { ...state, data: action.payload };")
            react_code.append("    case 'SET_LOADING':")
            react_code.append("      return { ...state, loading: action.payload };")
            react_code.append("    case 'RESET':")
            react_code.append("      return { data: '', loading: false };")
            react_code.append("    default:")
            react_code.append("      return state;")
            react_code.append("  }")
            react_code.append("};")
            react_code.append("")
        
        # Detectar componentes
        component_name = "VaderComponent"
        for line in lines:
            if 'componente' in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    component_name = parts[1].capitalize()
                break
        
        # Crear componente principal
        react_code.append(f"const {component_name} = ({{ ...props }}) => {{")
        
        # Estado avanzado
        if uses_reducer:
            react_code.append("  const [state, dispatch] = useReducer(vaderReducer, { data: '', loading: false });")
        else:
            react_code.append("  const [data, setData] = useState('');")
            react_code.append("  const [loading, setLoading] = useState(false);")
        
        react_code.append("  const [error, setError] = useState(null);")
        react_code.append("  const [formData, setFormData] = useState({});")
        
        # Refs
        react_code.append("  const inputRef = useRef(null);")
        react_code.append("  const containerRef = useRef(null);")
        
        # Context si se usa
        if uses_context:
            react_code.append("  const { globalState, setGlobalState } = useContext(VaderContext);")
        
        # Router hooks si se usa
        if uses_router:
            react_code.append("  const navigate = useNavigate();")
        
        react_code.append("")
        
        # Callbacks memoizados
        react_code.append("  // Callbacks memoizados para optimización")
        react_code.append("  const handleInputChange = useCallback((e) => {")
        if uses_reducer:
            react_code.append("    dispatch({ type: 'SET_DATA', payload: e.target.value });")
        else:
            react_code.append("    setData(e.target.value);")
        react_code.append("  }, []);")
        react_code.append("")
        
        react_code.append("  const handleSubmit = useCallback((e) => {")
        react_code.append("    e.preventDefault();")
        if uses_reducer:
            react_code.append("    dispatch({ type: 'SET_LOADING', payload: true });")
        else:
            react_code.append("    setLoading(true);")
        react_code.append("    // Lógica de envío aquí")
        react_code.append("    setTimeout(() => {")
        if uses_reducer:
            react_code.append("      dispatch({ type: 'SET_LOADING', payload: false });")
        else:
            react_code.append("      setLoading(false);")
        react_code.append("    }, 1000);")
        react_code.append("  }, []);")
        react_code.append("")
        
        # useEffect para efectos secundarios
        react_code.append("  // Efectos secundarios")
        react_code.append("  useEffect(() => {")
        react_code.append("    // Efecto de montaje")
        react_code.append("    console.log('Componente montado');")
        react_code.append("    ")
        react_code.append("    return () => {")
        react_code.append("      // Cleanup")
        react_code.append("      console.log('Componente desmontado');")
        react_code.append("    };")
        react_code.append("  }, []);")
        react_code.append("")
        
        # Valores memoizados
        react_code.append("  // Valores memoizados")
        if uses_reducer:
            react_code.append("  const computedValue = useMemo(() => {")
            react_code.append("    return state.data.length > 0 ? state.data.toUpperCase() : 'Sin datos';")
            react_code.append("  }, [state.data]);")
        else:
            react_code.append("  const computedValue = useMemo(() => {")
            react_code.append("    return data.length > 0 ? data.toUpperCase() : 'Sin datos';")
            react_code.append("  }, [data]);")
        react_code.append("")
        
        # Procesar líneas de código Vader para funcionalidades específicas
        jsx_elements = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if 'mostrar' in line.lower() or 'imprimir' in line.lower():
                content = line.split('"')[1] if '"' in line else "computedValue"
                jsx_elements.append(f"      <p className='vader-text'>{{{content}}}</p>")
            elif 'pedir' in line.lower() or 'input' in line.lower():
                jsx_elements.append("      <input")
                jsx_elements.append("        ref={inputRef}")
                jsx_elements.append("        type='text'")
                if uses_reducer:
                    jsx_elements.append("        value={state.data}")
                else:
                    jsx_elements.append("        value={data}")
                jsx_elements.append("        onChange={handleInputChange}")
                jsx_elements.append("        placeholder='Ingresa texto'")
                jsx_elements.append("        className='vader-input'")
                jsx_elements.append("      />")
            elif 'boton' in line.lower() or 'button' in line.lower():
                jsx_elements.append("      <button")
                jsx_elements.append("        onClick={handleSubmit}")
                jsx_elements.append("        disabled={loading}")
                jsx_elements.append("        className='vader-button'")
                jsx_elements.append("      >")
                jsx_elements.append("        {loading ? 'Cargando...' : 'Enviar'}")
                jsx_elements.append("      </button>")
        
        # JSX return
        react_code.append("  return (")
        react_code.append("    <div ref={containerRef} className='vader-component'>")
        react_code.append("      <h1>Componente Vader Avanzado</h1>")
        
        # Formulario si se detecta
        if uses_forms or jsx_elements:
            react_code.append("      <form onSubmit={handleSubmit} className='vader-form'>")
            
            # Agregar elementos JSX detectados
            if jsx_elements:
                react_code.extend(jsx_elements)
            else:
                react_code.append("        <input")
                react_code.append("          ref={inputRef}")
                react_code.append("          type='text'")
                if uses_reducer:
                    react_code.append("          value={state.data}")
                else:
                    react_code.append("          value={data}")
                react_code.append("          onChange={handleInputChange}")
                react_code.append("          placeholder='Ingresa texto'")
                react_code.append("          className='vader-input'")
                react_code.append("        />")
                react_code.append("        <button type='submit' disabled={loading} className='vader-button'>")
                react_code.append("          {loading ? 'Cargando...' : 'Enviar'}")
                react_code.append("        </button>")
            
            react_code.append("      </form>")
        
        # Mostrar estado
        react_code.append("      <div className='vader-status'>")
        react_code.append("        <p>Estado: {computedValue}</p>")
        if uses_reducer:
            react_code.append("        <p>Cargando: {state.loading ? 'Sí' : 'No'}</p>")
        else:
            react_code.append("        <p>Cargando: {loading ? 'Sí' : 'No'}</p>")
        react_code.append("        {error && <p className='error'>Error: {error}</p>}")
        react_code.append("      </div>")
        
        # Router si se usa
        if uses_router:
            react_code.append("      <nav className='vader-nav'>")
            react_code.append("        <Link to='/'>Inicio</Link>")
            react_code.append("        <Link to='/about'>Acerca</Link>")
            react_code.append("      </nav>")
        
        react_code.append("    </div>")
        react_code.append("  );")
        react_code.append("};")
        react_code.append("")
        
        # Componente con Suspense si usa lazy
        if uses_lazy:
            react_code.append("// Componente con lazy loading")
            react_code.append(f"const Lazy{component_name} = lazy(() => Promise.resolve({{ default: {component_name} }}));")
            react_code.append("")
            react_code.append(f"const {component_name}WithSuspense = (props) => (")
            react_code.append("  <Suspense fallback={<div>Cargando componente...</div>}>")
            react_code.append(f"    <Lazy{component_name} {{...props}} />")
            react_code.append("  </Suspense>")
            react_code.append(");")
            react_code.append("")
        
        # App principal si usa router o context
        if uses_router or uses_context:
            react_code.append("// Aplicación principal")
            react_code.append("const App = () => {")
            react_code.append("  return (")
            
            if uses_context:
                react_code.append("    <VaderProvider>")
            
            if uses_router:
                react_code.append("      <Router>")
                react_code.append("        <Routes>")
                react_code.append(f"          <Route path='/' element={{<{component_name} />}} />")
                react_code.append(f"          <Route path='/about' element={{<div>Acerca de</div>}} />")
                react_code.append("        </Routes>")
                react_code.append("      </Router>")
            else:
                if uses_lazy:
                    react_code.append(f"      <{component_name}WithSuspense />")
                else:
                    react_code.append(f"      <{component_name} />")
            
            if uses_context:
                react_code.append("    </VaderProvider>")
            
            react_code.append("  );")
            react_code.append("};")
            react_code.append("")
            react_code.append("export default App;")
        else:
            if uses_lazy:
                react_code.append(f"export default {component_name}WithSuspense;")
            else:
                react_code.append(f"export default {component_name};")
        
        # CSS básico
        react_code.append("")
        react_code.append("/* Estilos CSS para el componente */")
        react_code.append("/*")
        react_code.append(".vader-component {")
        react_code.append("  max-width: 600px;")
        react_code.append("  margin: 0 auto;")
        react_code.append("  padding: 20px;")
        react_code.append("  font-family: Arial, sans-serif;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".vader-form {")
        react_code.append("  display: flex;")
        react_code.append("  flex-direction: column;")
        react_code.append("  gap: 15px;")
        react_code.append("  margin: 20px 0;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".vader-input {")
        react_code.append("  padding: 10px;")
        react_code.append("  border: 1px solid #ddd;")
        react_code.append("  border-radius: 4px;")
        react_code.append("  font-size: 16px;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".vader-button {")
        react_code.append("  padding: 10px 20px;")
        react_code.append("  background-color: #007bff;")
        react_code.append("  color: white;")
        react_code.append("  border: none;")
        react_code.append("  border-radius: 4px;")
        react_code.append("  cursor: pointer;")
        react_code.append("  font-size: 16px;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".vader-button:disabled {")
        react_code.append("  background-color: #6c757d;")
        react_code.append("  cursor: not-allowed;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".vader-nav a {")
        react_code.append("  margin-right: 15px;")
        react_code.append("  text-decoration: none;")
        react_code.append("  color: #007bff;")
        react_code.append("}")
        react_code.append("")
        react_code.append(".error {")
        react_code.append("  color: #dc3545;")
        react_code.append("}")
        react_code.append("*/")
        
        return '\n'.join(react_code)
