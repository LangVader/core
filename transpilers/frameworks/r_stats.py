# Transpilador R para Vader
# Convierte sintaxis natural a R para análisis estadístico y ciencia de datos

def transpile_r(code):
    """Transpila código Vader a R"""
    lines = code.split('\n')
    result = []
    
    # Librerías comunes de R
    result.extend([
        '# Análisis estadístico generado por Vader',
        'library(ggplot2)',
        'library(dplyr)',
        'library(readr)',
        'library(tidyr)',
        '',
    ])
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('cargar datos'):
            # Cargar dataset
            file_path = line.replace('cargar datos', '').strip().strip('"')
            var_name = 'datos'
            if ' como ' in line:
                parts = line.split(' como ')
                file_path = parts[0].replace('cargar datos', '').strip().strip('"')
                var_name = parts[1].strip().strip('"')
            
            if file_path.endswith('.csv'):
                result.append(f'{var_name} <- read_csv("{file_path}")')
            elif file_path.endswith('.xlsx'):
                result.append('library(readxl)')
                result.append(f'{var_name} <- read_excel("{file_path}")')
            else:
                result.append(f'{var_name} <- read.table("{file_path}", header = TRUE)')
            result.append('')
            
        elif line.startswith('mostrar resumen'):
            # Resumen estadístico
            dataset = line.replace('mostrar resumen', '').strip() or 'datos'
            result.extend([
                f'# Resumen estadístico de {dataset}',
                f'summary({dataset})',
                f'str({dataset})',
                f'head({dataset})',
                ''
            ])
            
        elif line.startswith('grafico barras'):
            # Gráfico de barras
            parts = line.replace('grafico barras', '').strip().split(' por ')
            if len(parts) >= 2:
                x_var = parts[0].strip()
                y_var = parts[1].strip()
                result.extend([
                    f'# Gráfico de barras: {x_var} por {y_var}',
                    f'ggplot(datos, aes(x = {x_var}, y = {y_var})) +',
                    '  geom_bar(stat = "identity", fill = "steelblue") +',
                    '  theme_minimal() +',
                    f'  labs(title = "Gráfico de barras: {x_var} vs {y_var}")',
                    ''
                ])
                
        elif line.startswith('grafico lineas'):
            # Gráfico de líneas
            parts = line.replace('grafico lineas', '').strip().split(' por ')
            if len(parts) >= 2:
                x_var = parts[0].strip()
                y_var = parts[1].strip()
                result.extend([
                    f'# Gráfico de líneas: {x_var} por {y_var}',
                    f'ggplot(datos, aes(x = {x_var}, y = {y_var})) +',
                    '  geom_line(color = "blue", size = 1) +',
                    '  geom_point(color = "red") +',
                    '  theme_minimal() +',
                    f'  labs(title = "Tendencia: {x_var} vs {y_var}")',
                    ''
                ])
                
        elif line.startswith('histograma'):
            # Histograma
            variable = line.replace('histograma', '').strip()
            result.extend([
                f'# Histograma de {variable}',
                f'ggplot(datos, aes(x = {variable})) +',
                '  geom_histogram(bins = 30, fill = "lightblue", color = "black") +',
                '  theme_minimal() +',
                f'  labs(title = "Distribución de {variable}")',
                ''
            ])
            
        elif line.startswith('boxplot'):
            # Diagrama de cajas
            variable = line.replace('boxplot', '').strip()
            result.extend([
                f'# Boxplot de {variable}',
                f'ggplot(datos, aes(y = {variable})) +',
                '  geom_boxplot(fill = "lightgreen") +',
                '  theme_minimal() +',
                f'  labs(title = "Boxplot de {variable}")',
                ''
            ])
            
        elif line.startswith('correlacion'):
            # Matriz de correlación
            variables = line.replace('correlacion', '').strip()
            if variables:
                result.extend([
                    f'# Correlación entre variables',
                    f'cor_matrix <- cor(datos[, c({variables})])',
                    'print(cor_matrix)',
                    ''
                ])
            else:
                result.extend([
                    '# Matriz de correlación completa',
                    'numeric_data <- datos[sapply(datos, is.numeric)]',
                    'cor_matrix <- cor(numeric_data, use = "complete.obs")',
                    'print(cor_matrix)',
                    ''
                ])
                
        elif line.startswith('regresion lineal'):
            # Regresión lineal
            parts = line.replace('regresion lineal', '').strip().split(' por ')
            if len(parts) >= 2:
                y_var = parts[0].strip()
                x_var = parts[1].strip()
                result.extend([
                    f'# Regresión lineal: {y_var} ~ {x_var}',
                    f'modelo <- lm({y_var} ~ {x_var}, data = datos)',
                    'summary(modelo)',
                    '',
                    '# Gráfico de regresión',
                    f'ggplot(datos, aes(x = {x_var}, y = {y_var})) +',
                    '  geom_point() +',
                    '  geom_smooth(method = "lm", se = TRUE) +',
                    '  theme_minimal() +',
                    f'  labs(title = "Regresión lineal: {y_var} vs {x_var}")',
                    ''
                ])
                
        elif line.startswith('filtrar'):
            # Filtrar datos
            condition = line.replace('filtrar', '').strip()
            result.extend([
                f'# Filtrar datos: {condition}',
                f'datos_filtrados <- datos %>% filter({condition})',
                'print(datos_filtrados)',
                ''
            ])
            
        elif line.startswith('agrupar por'):
            # Agrupar y resumir
            group_var = line.replace('agrupar por', '').strip()
            result.extend([
                f'# Agrupar por {group_var}',
                f'resumen_grupos <- datos %>%',
                f'  group_by({group_var}) %>%',
                '  summarise(',
                '    count = n(),',
                '    .groups = "drop"',
                '  )',
                'print(resumen_grupos)',
                ''
            ])
            
        elif line.startswith('test t'):
            # Test t de Student
            parts = line.replace('test t', '').strip().split(' por ')
            if len(parts) >= 2:
                variable = parts[0].strip()
                group = parts[1].strip()
                result.extend([
                    f'# Test t: {variable} por {group}',
                    f't_test_result <- t.test({variable} ~ {group}, data = datos)',
                    'print(t_test_result)',
                    ''
                ])
                
        elif line.startswith('anova'):
            # Análisis de varianza
            parts = line.replace('anova', '').strip().split(' por ')
            if len(parts) >= 2:
                variable = parts[0].strip()
                factor = parts[1].strip()
                result.extend([
                    f'# ANOVA: {variable} por {factor}',
                    f'anova_model <- aov({variable} ~ {factor}, data = datos)',
                    'summary(anova_model)',
                    ''
                ])
                
        elif line.startswith('guardar grafico'):
            # Guardar gráfico
            filename = line.replace('guardar grafico', '').strip().strip('"')
            result.extend([
                f'# Guardar gráfico como {filename}',
                f'ggsave("{filename}", width = 10, height = 6, dpi = 300)',
                ''
            ])
            
        elif line.startswith('exportar datos'):
            # Exportar datos
            filename = line.replace('exportar datos', '').strip().strip('"')
            result.extend([
                f'# Exportar datos a {filename}',
                f'write_csv(datos, "{filename}")',
                ''
            ])
            
        elif line.startswith('estadisticas descriptivas'):
            # Estadísticas descriptivas detalladas
            variable = line.replace('estadisticas descriptivas', '').strip() or 'datos'
            result.extend([
                f'# Estadísticas descriptivas de {variable}',
                'library(psych)',
                f'describe({variable})',
                ''
            ])
    
    return '\n'.join(result)

# Palabras clave específicas de R
R_KEYWORDS = [
    'cargar datos', 'mostrar resumen', 'grafico barras', 'grafico lineas', 'histograma',
    'boxplot', 'correlacion', 'regresion lineal', 'filtrar', 'agrupar por', 'test t',
    'anova', 'guardar grafico', 'exportar datos', 'estadisticas descriptivas'
]

def detect_r(code):
    """Detecta si el código contiene sintaxis específica de R"""
    code_lower = code.lower()
    return any(keyword in code_lower for keyword in R_KEYWORDS)
