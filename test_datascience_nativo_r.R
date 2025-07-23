# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL DATA SCIENCE
# Archivo .vdr ejecutado nativamente para R

library(tidyverse)
library(ggplot2)
library(corrplot)

VaderDataScienceR <- function() {
  cat("📊 VADER 7.0 - R Data Science Runtime\n")
  
  list(
    cargar_datos = function(archivo, tipo = "csv") {
      if (tipo == "csv") {
        datos <- read_csv(archivo)
      } else if (tipo == "excel") {
        library(readxl)
        datos <- read_excel(archivo)
      }
      cat("✅ Datos cargados:", nrow(datos), "filas\n")
      return(datos)
    },
    
    explorar_datos = function(datos) {
      cat("📋 INFORMACIÓN DEL DATASET\n")
      print(str(datos))
      print(summary(datos))
      return(head(datos))
    },
    
    crear_visualizaciones = function(datos) {
      datos_numericos <- select_if(datos, is.numeric)
      datos_long <- gather(datos_numericos, key = "variable", value = "valor")
      
      p <- ggplot(datos_long, aes(x = valor)) +
        geom_histogram(bins = 30, alpha = 0.7) +
        facet_wrap(~variable, scales = "free") +
        theme_minimal()
      
      print(p)
      return(p)
    }
  )
}

vader_r <- VaderDataScienceR()
cat("🎯 Análisis Vader Data Science R listo\n")
