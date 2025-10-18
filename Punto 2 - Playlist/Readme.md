# 🎵 Sistema de Recomendación Musical con ACO

## 📋 Descripción del Proyecto

Sistema inteligente de recomendación de playlists musicales basado en el **Algoritmo de Colonias de Hormigas (ACO - Ant Colony Optimization)**. Los usuarios actúan como hormigas virtuales que exploran un grafo musical, dejando feromonas digitales para optimizar las transiciones entre canciones según sus preferencias personales.

## 🎯 Características Principales

### 🤖 Algoritmo ACO Adaptado para Música
- **Usuarios como hormigas**: Cada usuario explora el espacio musical
- **Sistema de feromonas**: Aprende de transiciones exitosas entre canciones
- **Evaluación multi-criterio**: Combina similitud, afinidad y feromonas
- **Balance exploración-explotación**: Descubre nuevas combinaciones musicales

### 🎼 Modelo Musical Avanzado
- **Canciones como nodos**: Con múltiples atributos musicales
  - 🎸 Género (rock, pop, jazz, funk)
  - ⚡ Energía
  - 💃 Danceability 
  - 🎹 Acústica 
- **Similitud coseno**: Comparación entre características musicales
- **Afinidad personalizada**: Según preferencias individuales del usuario

### 📊 Sistema de Métricas Compuestas
```python
calidad_total = 0.5 × afinidad + 0.3 × coherencia + 0.2 × variedad
```

**Componentes:**
- **Afinidad (50%)**: Adaptación a preferencias del usuario
- **Coherencia (30%)**: Suavidad en transiciones entre canciones
- **Variedad (20%)**: Balance entre similitud y diversidad

### 📈 Dashboard Interactivo
Visualización en tiempo real con 4 paneles:

1. **Evolución del algoritmo**: Progreso de métricas por iteración
2. **Afinidad por canción**: Visualización de preferencias
3. **Métricas finales**: Resumen de rendimiento
4. **Playlist recomendada**: Lista detallada con afinidades


## 🚀 Uso del Sistema

### Ejecución Básica
```python
from spotify_aco import SistemaRecomendacionACO, UsuarioHormiga, crear_dataset_musical

# 1. Crear dataset musical
canciones = crear_dataset_musical()

# 2. Definir usuario con preferencias
usuario = UsuarioHormiga(
    preferencias={
        'rock': 0.7,
        'energia': 0.8,
        'danceability': 0.6,
        'acustica': 0.5
    },
    nombre="Rockero Energético"
)

# 3. Inicializar sistema ACO
sistema = SistemaRecomendacionACO(
    canciones=canciones,
    alpha=1.0,      # Peso de feromonas
    beta=2.0,       # Peso de heurística
    rho=0.1,        # Evaporación
    Q=100           # Factor de deposición
)

# 4. Generar playlist
playlist = sistema.generar_playlist(
    usuario=usuario,
    longitud_playlist=5,
    iteraciones=30
)
```

### Perfiles de Usuario Predefinidos

#### 🎸 Rockero Energético
```python
usuario_rock = UsuarioHormiga(
    preferencias={
        'rock': 0.9,
        'energia': 0.8,
        'danceability': 0.5,
        'acustica': 0.6
    },
    nombre="Rockero Energético"
)
```

#### 💃 Amante del Pop
```python
usuario_pop = UsuarioHormiga(
    preferencias={
        'pop': 0.8,
        'energia': 0.6,
        'danceability': 0.9,
        'acustica': 0.3
    },
    nombre="Amante del Pop"
)
```

## 📊 Métricas de Evaluación

### Métricas Principales

| Métrica | Descripción | Rango | Objetivo |
|---------|-------------|-------|----------|
| **Afinidad** | Ajuste a preferencias del usuario | [0, 1] | Maximizar |
| **Coherencia** | Suavidad de transiciones | [0, 1] | Maximizar |
| **Variedad** | Diversidad musical | [0, 1] | Balancear |
| **Calidad Total** | Métrica compuesta | [0, 1] | Maximizar |

## 🎮 Casos de Uso

### 1. Música para Concentración 📚
```python
usuario_estudio = UsuarioHormiga(
    preferencias={
        'acustica': 0.9,
        'energia': 0.2,
        'jazz': 0.7,
        'danceability': 0.3
    },
    nombre="Concentración"
)
```

### 2. Fiesta/Social 🎉
```python
usuario_fiesta = UsuarioHormiga(
    preferencias={
        'danceability': 0.95,
        'energia': 0.9,
        'pop': 0.8,
        'funk': 0.7
    },
    nombre="Fiesta"
)
```

## 🎨 Dataset Musical

### Estructura de Canciones
```python
{
    'Nombre de Canción': {
        'rock': 0.0-1.0,          # Nivel de rock
        'pop': 0.0-1.0,           # Nivel de pop
        'jazz': 0.0-1.0,          # Nivel de jazz
        'funk': 0.0-1.0,          # Nivel de funk
        'energia': 0.0-1.0,       # Intensidad energética
        'danceability': 0.0-1.0,  # Capacidad de baile
        'acustica': 0.0-1.0       # Instrumentación acústica
    }
}
```

### Dataset Incluido
El sistema incluye 6 canciones de ejemplo:

| Canción | Género Principal | Energía | Danceability | Acústica |
|---------|-----------------|---------|--------------|----------|
| Bohemian Rhapsody | Rock | 0.8 | 0.4 | 0.7 |
| Blinding Lights | Pop | 0.7 | 0.9 | 0.3 |
| Take Five | Jazz | 0.3 | 0.6 | 0.8 |
| Bad Guy | Pop | 0.6 | 0.8 | 0.4 |
| Sweet Child O Mine | Rock | 0.9 | 0.5 | 0.6 |
| Uptown Funk | Funk/Pop | 0.8 | 0.9 | 0.2 |


## 💡 Ventajas del Enfoque ACO

### ✅ Beneficios Técnicos
- **Adaptabilidad**: Aprende continuamente de preferencias
- **Exploración**: Descubre combinaciones musicales innovadoras
- **Personalización**: Experiencia única por usuario
- **Escalabilidad**: Funciona con catálogos grandes
- **Transparencia**: Proceso explicable y ajustable

### 📊 Comparación con Otros Métodos

| Característica | ACO | Filtrado Colaborativo | Basado en Contenido |
|----------------|-----|----------------------|---------------------|
| **Personalización** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Descubrimiento** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Cold Start** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Coherencia** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Escalabilidad** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎵 Ejemplos

### Ejemplos de Salida
```
🎵 SISTEMA DE RECOMENDACIÓN MUSICAL CON ACO
==================================================
🎵 Iniciando algoritmo ACO...
   Iteración 0: Calidad = 0.623
   Iteración 10: Calidad = 0.741
   Iteración 20: Calidad = 0.812
   
🎯 Playlist Recomendada:
  1. Bohemian Rhapsody (afinidad: 0.825)
  2. Sweet Child O Mine (afinidad: 0.892)
  3. Uptown Funk (afinidad: 0.754)
  4. Blinding Lights (afinidad: 0.687)
  5. Bad Guy (afinidad: 0.698)

📊 Métricas Detalladas:
 • Calidad Total: 0.812
 • Afinidad Promedio: 0.771
 • Coherencia: 0.685
 • Variedad: 1.000
```

<img width="1479" height="990" alt="Captura de pantalla 2025-10-17 210049" src="https://github.com/user-attachments/assets/c4aaad14-1005-44d2-b134-f23bc853629b" />


<img width="1480" height="983" alt="Captura de pantalla 2025-10-17 210120" src="https://github.com/user-attachments/assets/3b21c805-82de-4ac7-90bb-5078dbc64b37" />

---

🎵 **Autor Paula S**
