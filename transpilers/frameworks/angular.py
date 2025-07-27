"""
Framework Angular para Vader
"""

class AngularFramework:
    def __init__(self):
        self.name = "Angular"
        self.description = "Framework empresarial completo para aplicaciones web"
        self.target_language = "typescript"
        self.keywords = [
            'angular', 'componente', 'servicio', 'directiva', 'pipe', 'modulo',
            'router', 'ruta', 'navegacion', 'formulario', 'reactive', 'template',
            'http', 'cliente', 'observable', 'rxjs', 'inyeccion', 'dependencia',
            'lifecycle', 'hook', 'oninit', 'ondestroy', 'input', 'output', 'emit'
        ]
    
    def detect(self, code):
        code_lower = code.lower()
        return any(keyword in code_lower for keyword in self.keywords)
    
    def transpile(self, vader_code):
        """Transpila código Vader a Angular con funcionalidades avanzadas"""
        lines = vader_code.strip().split('\n')
        
        # Detectar funcionalidades avanzadas
        uses_router = any('router' in line.lower() or 'ruta' in line.lower() or 'navegacion' in line.lower() for line in lines)
        uses_http = any('http' in line.lower() or 'cliente' in line.lower() for line in lines)
        uses_forms = any('formulario' in line.lower() or 'reactive' in line.lower() for line in lines)
        uses_service = any('servicio' in line.lower() or 'service' in line.lower() for line in lines)
        uses_pipe = any('pipe' in line.lower() or 'filtro' in line.lower() for line in lines)
        
        # Detectar componente
        component_name = "VaderComponent"
        for line in lines:
            if 'componente' in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    component_name = parts[1].capitalize() + "Component"
                break
        
        # Detectar elementos de interfaz
        has_input = any('pedir' in line.lower() or 'input' in line.lower() for line in lines)
        has_button = any('boton' in line.lower() or 'button' in line.lower() for line in lines)
        has_list = any('lista' in line.lower() or 'array' in line.lower() for line in lines)
        
        # Construir código Angular
        angular_code = []
        
        # Imports
        imports = ["import { Component, OnInit, OnDestroy"]
        if has_input or uses_forms:
            imports.append(", Input, Output, EventEmitter")
        imports.append(" } from '@angular/core';")
        
        if uses_forms:
            angular_code.append("import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';")
        
        if uses_http:
            angular_code.append("import { HttpClient } from '@angular/common/http';")
            angular_code.append("import { Observable } from 'rxjs';")
        
        if uses_router:
            angular_code.append("import { Router, ActivatedRoute } from '@angular/router';")
        
        if uses_service:
            angular_code.append("import { Injectable } from '@angular/core';")
        
        angular_code.append(''.join(imports))
        angular_code.append("")
        
        # Servicio si es necesario
        if uses_service:
            angular_code.append("// Servicio para lógica de negocio")
            angular_code.append("@Injectable({")
            angular_code.append("  providedIn: 'root'")
            angular_code.append("})") 
            angular_code.append("export class VaderService {")
            
            if uses_http:
                angular_code.append("  constructor(private http: HttpClient) {}")
                angular_code.append("")
                angular_code.append("  getData(): Observable<any> {")
                angular_code.append("    return this.http.get<any>('/api/data');")
                angular_code.append("  }")
                angular_code.append("")
                angular_code.append("  postData(data: any): Observable<any> {")
                angular_code.append("    return this.http.post<any>('/api/data', data);")
                angular_code.append("  }")
            else:
                angular_code.append("  processData(data: string): string {")
                angular_code.append("    return data.toUpperCase();")
                angular_code.append("  }")
                angular_code.append("")
                angular_code.append("  validateData(data: string): boolean {")
                angular_code.append("    return data.length > 0;")
                angular_code.append("  }")
            
            angular_code.append("}")
            angular_code.append("")
        
        # Pipe personalizado si es necesario
        if uses_pipe:
            angular_code.append("// Pipe personalizado")
            angular_code.append("import { Pipe, PipeTransform } from '@angular/core';")
            angular_code.append("")
            angular_code.append("@Pipe({")
            angular_code.append("  name: 'vaderTransform'")
            angular_code.append("})") 
            angular_code.append("export class VaderPipe implements PipeTransform {")
            angular_code.append("  transform(value: string, ...args: any[]): string {")
            angular_code.append("    if (!value) return '';")
            angular_code.append("    return value.toUpperCase().split('').reverse().join('');")
            angular_code.append("  }")
            angular_code.append("}")
            angular_code.append("")
        
        # Componente principal
        angular_code.append("@Component({")
        angular_code.append(f"  selector: 'app-{component_name.lower().replace('component', '')}',")
        angular_code.append("  template: `")
        
        # Template HTML
        angular_code.append("    <div class='vader-component'>")
        angular_code.append("      <h1>{{ title }}</h1>")
        
        # Formulario si se detecta
        if uses_forms or has_input or has_button:
            angular_code.append("      <form [formGroup]='vaderForm' (ngSubmit)='onSubmit()' class='vader-form'>")
            
            if has_input:
                angular_code.append("        <div class='form-group'>")
                angular_code.append("          <label for='userInput'>Entrada:</label>")
                angular_code.append("          <input")
                angular_code.append("            id='userInput'")
                angular_code.append("            type='text'")
                angular_code.append("            formControlName='input'")
                angular_code.append("            placeholder='Ingresa texto'")
                angular_code.append("            class='vader-input'")
                angular_code.append("            [class.invalid]='vaderForm.get(\"input\")?.invalid && vaderForm.get(\"input\")?.touched'")
                angular_code.append("          />")
                angular_code.append("          <div *ngIf='vaderForm.get(\"input\")?.invalid && vaderForm.get(\"input\")?.touched' class='error'>")
                angular_code.append("            <small *ngIf='vaderForm.get(\"input\")?.errors?.[\"required\"]'>Este campo es requerido</small>")
                angular_code.append("            <small *ngIf='vaderForm.get(\"input\")?.errors?.[\"minlength\"]'>Mínimo 3 caracteres</small>")
                angular_code.append("          </div>")
                angular_code.append("        </div>")
            
            if has_button:
                angular_code.append("        <button")
                angular_code.append("          type='submit'")
                angular_code.append("          [disabled]='vaderForm.invalid || loading'")
                angular_code.append("          class='vader-button'")
                angular_code.append("        >")
                angular_code.append("          {{ loading ? 'Cargando...' : 'Enviar' }}")
                angular_code.append("        </button>")
            
            angular_code.append("      </form>")
        
        # Lista si se detecta
        if has_list:
            angular_code.append("      <div class='vader-list'>")
            angular_code.append("        <h3>Lista de elementos:</h3>")
            angular_code.append("        <ul>")
            angular_code.append("          <li *ngFor='let item of items; let i = index; trackBy: trackByFn' class='list-item'>")
            if uses_pipe:
                angular_code.append("            {{ item | vaderTransform }}")
            else:
                angular_code.append("            {{ item }}")
            angular_code.append("            <button (click)='removeItem(i)' class='remove-btn'>&times;</button>")
            angular_code.append("          </li>")
            angular_code.append("        </ul>")
            angular_code.append("        <div *ngIf='items.length === 0' class='empty-state'>")
            angular_code.append("          No hay elementos en la lista")
            angular_code.append("        </div>")
            angular_code.append("      </div>")
        
        # Estado y resultados
        angular_code.append("      <div class='vader-status'>")
        angular_code.append("        <p>Estado: {{ computedStatus }}</p>")
        angular_code.append("        <p *ngIf='result'>Resultado: {{ result }}</p>")
        angular_code.append("        <p *ngIf='error' class='error'>Error: {{ error }}</p>")
        angular_code.append("      </div>")
        
        # Router navigation si se usa
        if uses_router:
            angular_code.append("      <nav class='vader-nav'>")
            angular_code.append("        <a routerLink='/' routerLinkActive='active'>Inicio</a>")
            angular_code.append("        <a routerLink='/about' routerLinkActive='active'>Acerca</a>")
            angular_code.append("        <button (click)='navigateToPage()' class='nav-button'>Navegar</button>")
            angular_code.append("      </nav>")
        
        angular_code.append("    </div>")
        angular_code.append("  `,")
        
        # Estilos
        angular_code.append("  styles: [`")
        angular_code.append("    .vader-component {")
        angular_code.append("      max-width: 600px;")
        angular_code.append("      margin: 0 auto;")
        angular_code.append("      padding: 20px;")
        angular_code.append("      font-family: Arial, sans-serif;")
        angular_code.append("    }")
        angular_code.append("    .vader-form {")
        angular_code.append("      margin: 20px 0;")
        angular_code.append("    }")
        angular_code.append("    .form-group {")
        angular_code.append("      margin-bottom: 15px;")
        angular_code.append("    }")
        angular_code.append("    .form-group label {")
        angular_code.append("      display: block;")
        angular_code.append("      margin-bottom: 5px;")
        angular_code.append("      font-weight: bold;")
        angular_code.append("    }")
        angular_code.append("    .vader-input {")
        angular_code.append("      width: 100%;")
        angular_code.append("      padding: 10px;")
        angular_code.append("      border: 1px solid #ddd;")
        angular_code.append("      border-radius: 4px;")
        angular_code.append("      font-size: 16px;")
        angular_code.append("    }")
        angular_code.append("    .vader-input.invalid {")
        angular_code.append("      border-color: #dc3545;")
        angular_code.append("    }")
        angular_code.append("    .vader-button {")
        angular_code.append("      padding: 10px 20px;")
        angular_code.append("      background-color: #dd0031;")
        angular_code.append("      color: white;")
        angular_code.append("      border: none;")
        angular_code.append("      border-radius: 4px;")
        angular_code.append("      cursor: pointer;")
        angular_code.append("      font-size: 16px;")
        angular_code.append("      transition: background-color 0.3s;")
        angular_code.append("    }")
        angular_code.append("    .vader-button:hover {")
        angular_code.append("      background-color: #c50025;")
        angular_code.append("    }")
        angular_code.append("    .vader-button:disabled {")
        angular_code.append("      background-color: #6c757d;")
        angular_code.append("      cursor: not-allowed;")
        angular_code.append("    }")
        angular_code.append("    .vader-list ul {")
        angular_code.append("      list-style: none;")
        angular_code.append("      padding: 0;")
        angular_code.append("    }")
        angular_code.append("    .list-item {")
        angular_code.append("      display: flex;")
        angular_code.append("      justify-content: space-between;")
        angular_code.append("      align-items: center;")
        angular_code.append("      padding: 8px;")
        angular_code.append("      border: 1px solid #eee;")
        angular_code.append("      margin-bottom: 5px;")
        angular_code.append("      border-radius: 4px;")
        angular_code.append("    }")
        angular_code.append("    .remove-btn {")
        angular_code.append("      background: #dc3545;")
        angular_code.append("      color: white;")
        angular_code.append("      border: none;")
        angular_code.append("      border-radius: 50%;")
        angular_code.append("      width: 25px;")
        angular_code.append("      height: 25px;")
        angular_code.append("      cursor: pointer;")
        angular_code.append("    }")
        angular_code.append("    .vader-nav a {")
        angular_code.append("      margin-right: 15px;")
        angular_code.append("      text-decoration: none;")
        angular_code.append("      color: #dd0031;")
        angular_code.append("      font-weight: bold;")
        angular_code.append("    }")
        angular_code.append("    .vader-nav a.active {")
        angular_code.append("      color: #c50025;")
        angular_code.append("    }")
        angular_code.append("    .error {")
        angular_code.append("      color: #dc3545;")
        angular_code.append("      font-weight: bold;")
        angular_code.append("    }")
        angular_code.append("    .empty-state {")
        angular_code.append("      text-align: center;")
        angular_code.append("      color: #6c757d;")
        angular_code.append("      font-style: italic;")
        angular_code.append("    }")
        angular_code.append("  `]")
        angular_code.append("})") 
        
        # Clase del componente
        angular_code.append(f"export class {component_name} implements OnInit, OnDestroy {{")
        
        # Propiedades
        angular_code.append("  title = 'Componente Angular Avanzado';")
        angular_code.append("  loading = false;")
        angular_code.append("  error: string | null = null;")
        angular_code.append("  result = '';")
        
        if uses_forms:
            angular_code.append("  vaderForm: FormGroup;")
        
        if has_list:
            angular_code.append("  items: string[] = ['Elemento 1', 'Elemento 2', 'Elemento 3'];")
        
        angular_code.append("")
        
        # Constructor
        constructor_params = []
        if uses_forms:
            constructor_params.append("private fb: FormBuilder")
        if uses_service:
            constructor_params.append("private vaderService: VaderService")
        if uses_http:
            constructor_params.append("private http: HttpClient")
        if uses_router:
            constructor_params.append("private router: Router", "private route: ActivatedRoute")
        
        if constructor_params:
            angular_code.append(f"  constructor({', '.join(constructor_params)}) {{")
        else:
            angular_code.append("  constructor() {")
        
        if uses_forms:
            angular_code.append("    this.vaderForm = this.fb.group({")
            angular_code.append("      input: ['', [Validators.required, Validators.minLength(3)]]")
            angular_code.append("    });")
        
        angular_code.append("  }")
        angular_code.append("")
        
        # Computed property
        angular_code.append("  get computedStatus(): string {")
        angular_code.append("    if (this.loading) return 'Cargando...';")
        angular_code.append("    if (this.error) return 'Error';")
        if uses_forms:
            angular_code.append("    const inputValue = this.vaderForm.get('input')?.value;")
            angular_code.append("    return inputValue ? inputValue.toUpperCase() : 'Sin datos';")
        else:
            angular_code.append("    return 'Listo';")
        angular_code.append("  }")
        angular_code.append("")
        
        # Lifecycle hooks
        angular_code.append("  ngOnInit(): void {")
        angular_code.append("    console.log('Componente inicializado');")
        
        if uses_http and uses_service:
            angular_code.append("    this.loadData();")
        
        angular_code.append("  }")
        angular_code.append("")
        
        angular_code.append("  ngOnDestroy(): void {")
        angular_code.append("    console.log('Componente destruido');")
        angular_code.append("  }")
        angular_code.append("")
        
        # Métodos
        if uses_forms or has_button:
            angular_code.append("  onSubmit(): void {")
            angular_code.append("    if (this.vaderForm?.valid) {")
            angular_code.append("      this.loading = true;")
            angular_code.append("      this.error = null;")
            angular_code.append("")
            
            if uses_service:
                if uses_http:
                    angular_code.append("      const formData = this.vaderForm.value;")
                    angular_code.append("      this.vaderService.postData(formData).subscribe({")
                    angular_code.append("        next: (response) => {")
                    angular_code.append("          this.result = `Procesado: ${JSON.stringify(response)}`;")
                    angular_code.append("          this.loading = false;")
                    angular_code.append("        },")
                    angular_code.append("        error: (err) => {")
                    angular_code.append("          this.error = err.message;")
                    angular_code.append("          this.loading = false;")
                    angular_code.append("        }")
                    angular_code.append("      });")
                else:
                    angular_code.append("      const inputValue = this.vaderForm.get('input')?.value;")
                    angular_code.append("      setTimeout(() => {")
                    angular_code.append("        this.result = this.vaderService.processData(inputValue);")
                    angular_code.append("        this.loading = false;")
                    angular_code.append("      }, 1000);")
            else:
                angular_code.append("      setTimeout(() => {")
                angular_code.append("        this.result = `Procesado: ${this.vaderForm.get('input')?.value}`;")
                angular_code.append("        this.loading = false;")
                angular_code.append("      }, 1000);")
            
            angular_code.append("    }")
            angular_code.append("  }")
            angular_code.append("")
        
        if uses_http and uses_service:
            angular_code.append("  loadData(): void {")
            angular_code.append("    this.vaderService.getData().subscribe({")
            angular_code.append("      next: (data) => {")
            angular_code.append("        console.log('Datos cargados:', data);")
            angular_code.append("      },")
            angular_code.append("      error: (err) => {")
            angular_code.append("        this.error = 'Error al cargar datos';")
            angular_code.append("      }")
            angular_code.append("    });")
            angular_code.append("  }")
            angular_code.append("")
        
        if has_list:
            angular_code.append("  removeItem(index: number): void {")
            angular_code.append("    this.items.splice(index, 1);")
            angular_code.append("  }")
            angular_code.append("")
            angular_code.append("  trackByFn(index: number, item: string): number {")
            angular_code.append("    return index;")
            angular_code.append("  }")
            angular_code.append("")
        
        if uses_router:
            angular_code.append("  navigateToPage(): void {")
            angular_code.append("    this.router.navigate(['/about']);")
            angular_code.append("  }")
            angular_code.append("")
        
        angular_code.append("}")
        
        # Módulo si es necesario
        angular_code.append("")
        angular_code.append("// Módulo del componente")
        angular_code.append("import { NgModule } from '@angular/core';")
        angular_code.append("import { CommonModule } from '@angular/common';")
        
        if uses_forms:
            angular_code.append("import { ReactiveFormsModule } from '@angular/forms';")
        
        if uses_router:
            angular_code.append("import { RouterModule } from '@angular/router';")
        
        if uses_http:
            angular_code.append("import { HttpClientModule } from '@angular/common/http';")
        
        angular_code.append("")
        angular_code.append("@NgModule({")
        
        declarations = [component_name]
        if uses_pipe:
            declarations.append("VaderPipe")
        
        angular_code.append(f"  declarations: [{', '.join(declarations)}],")
        
        imports = ["CommonModule"]
        if uses_forms:
            imports.append("ReactiveFormsModule")
        if uses_router:
            imports.append("RouterModule")
        if uses_http:
            imports.append("HttpClientModule")
        
        angular_code.append(f"  imports: [{', '.join(imports)}],")
        
        providers = []
        if uses_service:
            providers.append("VaderService")
        
        if providers:
            angular_code.append(f"  providers: [{', '.join(providers)}],")
        
        angular_code.append(f"  exports: [{component_name}]")
        angular_code.append("})") 
        angular_code.append(f"export class {component_name}Module {{ }}")
        
        return '\n'.join(angular_code)
