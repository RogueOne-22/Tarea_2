# 🤖 Colección de Sistemas de Inteligencia Artificial

Tres implementaciones avanzadas de algoritmos de IA aplicados a problemas reales: recomendación musical, evolución de Pokémon y control de robots de carreras.

---

## 1️⃣ 🎵 Sistema de Recomendación Musical con ACO

### 📌 Descripción
Sistema de playlists personalizadas usando **Ant Colony Optimization (ACO)** que aprende de preferencias musicales mediante feromonas virtuales.

### 🎯 Algoritmo Principal
```python
calidad = 0.5 × afinidad + 0.3 × coherencia + 0.2 × variedad

atractivo = (feromona^α) × (similitud × afinidad)^β
```

### ⚡ Características Clave
- **Sistema de feromonas** para transiciones musicales exitosas
- **Similitud coseno** entre características de canciones
- **Afinidad personalizada** según gustos del usuario
- **Dashboard interactivo** con 4 paneles de visualización

### 📊 Parámetros
```python
alpha = 1.0        # Peso de feromonas (memoria)
beta = 2.0         # Peso de heurística (similitud)
rho = 0.1          # Evaporación
iteraciones = 50   # Ciclos de optimización
```

### 🎼 Métricas
| Métrica | Peso | Objetivo |
|---------|------|----------|
| Afinidad | 50% | Preferencias del usuario |
| Coherencia | 30% | Transiciones suaves |
| Variedad | 20% | Diversidad musical |

### 🚀 Uso Rápido
```python
usuario = UsuarioHormiga(
    preferencias={'rock': 0.7, 'energia': 0.8},
    nombre="Rockero"
)
sistema = SistemaRecomendacionACO(canciones)
playlist = sistema.generar_playlist(usuario, longitud=5, iteraciones=30)
```

---

## 2️⃣ 🎮 Evolución de Pokémon con Algoritmos Genéticos

### 📌 Descripción
Simulador de evolución de Pokémon usando **Genetic Algorithm (GA)** con stats aleatorios y sistema de evoluciones progresivas.

### 🎯 Función de Fitness
```python
fitness = 0.35×Ataque + 0.15×Defensa + 0.30×Velocidad + 0.20×HP

Bonificaciones:
- Fire:     +8%
- Electric: +5%
```

### ⚡ Características Clave
- **Stats aleatorios** por tipo con distribuciones gaussianas
- **Sistema de evoluciones** (hasta 5 etapas)
- **ROUGE especial** con stats únicos cada ejecución
- **Visualización en tiempo real** con 4 gráficos

### 📊 Parámetros GA
```python
POP_SIZE = 80              # Población
N_GENS = 7                 # Generaciones
ELITISM = 3                # Élite preservada
MUTATION_RATE = 0.15       # Mutación 15%
CROSSOVER_RATE = 0.85      # Crossover 85%
```

### 🔄 Sistema de Evoluciones
- **Umbral**: Fitness ≥ 0.50
- **Boost**: +15% por etapa (progresivo)
- **Máximo**: 5 evoluciones
- **Asistida**: Activada en gen 5+ para débiles

### 📈 Operadores
| Operador | Método | Parámetros |
|----------|--------|------------|
| Selección | Ruleta | Proporcional a fitness |
| Crossover | Aritmético | α aleatorio |
| Mutación | Gaussiana | σ = 0.06 |

---

## 3️⃣ 🏎️ Robot de Carreras con IA Híbrida

### 📌 Descripción
Control autónomo de robot en carreras usando **GA + PSO + ACO**  contra 8 oponentes.

### 🎯 Algoritmos Combinados

#### 🧬 GA - Evolución de Parámetros
```python
Parámetros optimizados:
- Agresividad:    0.6-0.9
- Conservador:    0.2-0.4
- Adelantamiento: 0.7-0.95
- Umbral Riesgo:  0.4-0.6
```

#### 🐝 PSO - Decisiones de Adelantamiento
```python
decision = {
    'adelantar': True/False,
    'agresividad': 0.6-0.9,
    'momento': 'INMEDIATO' | 'ESPERAR'
}
```

#### 🐜 ACO - Optimización de Trayectorias
```python
feromonas[tramo] += 1.0 / tiempo
feromonas = clip(feromonas, 1.0, 20.0)
```

### ⚡ Características Clave
- **8 oponentes** con colores únicos
- **Feromonas visualizadas** por intensidad de color
- **Partículas PSO** durante adelantamientos
- **Evolución automática** cada 10 segundos

### 📊 Física del Sistema
```python
# Velocidades
vel_normal = 4.0 unidades/frame
vel_boost = 5.0 unidades/frame

# Detección adelantamiento
distancia < 25 && x_robot > x_oponente
```

### 🎨 Visualización
| Panel | Contenido |
|-------|-----------|
| Principal | Pista + Feromonas + Vehículos |
| Info | Parámetros + Métricas + Estado |

---

## 🔬 Comparación de Algoritmos

| Característica | ACO Musical | GA Pokémon | Robot Híbrido |
|----------------|-------------|------------|---------------|
| **Algoritmo Principal** | ACO | GA | GA+PSO+ACO |
| **Objetivo** | Playlist óptima | Fitness máximo | Adelantamientos |
| **Población** | Usuarios | 80 Pokémon | 8 oponentes |
| **Iteraciones** | 30-100 | 7 generaciones | Continuo |
| **Visualización** | 4 gráficos | 4 gráficos | 2 paneles |
| **Tiempo Ejecución** | ~5-10s | ~10-15s | Infinito |
| **Archivos Salida** | No | 3 CSV | No |

---

## 🎯 Aplicaciones Prácticas

### 🎵 Sistema Musical
- Servicios de streaming
- DJs automáticos
- Radio personalizada

### 🎮 Evolución Pokémon
- Balanceo de videojuegos
- Diseño de personajes
- Enseñanza de GAs

### 🏎️ Robot Carreras
- Vehículos autónomos
- NPCs inteligentes
- Robótica competitiva

---

## 📊 Métricas de Rendimiento

### ACO Musical
```
Afinidad típica:  0.70-0.85
Coherencia:       0.60-0.75
Calidad total:    0.75-0.82
```

### GA Pokémon
```
Fitness inicial:  0.40-0.50
Fitness final:    0.70-0.85
Evoluciones:      15-25
```

### Robot Carreras
```
Adelantamientos:  Variable
Velocidad:        4.0-5.0
Feromonas:        1.0-20.0
```
---

## 🔧 Personalización Común

### Cambiar Iteraciones
```python
# ACO Musical
iteraciones = 100

# GA Pokémon
N_GENS = 10

# Robot (frecuencia evolución)
if int(self.tiempo) % 5 == 0:  # cada 5s
```

### Ajustar Población
```python
# ACO Musical
longitud_playlist = 10

# GA Pokémon
POP_SIZE = 120

# Robot Carreras
n_oponentes = 12
```

### Modificar Parámetros
```python
# ACO
alpha=1.5, beta=3.0, rho=0.15

# GA
MUTATION_RATE=0.20, CROSSOVER_RATE=0.90

# Robot
'agresividad': 0.85, 'umbral_riesgo': 0.60
```

---

📚 **Autor Paula S**

---

🤖 **Tres implementaciones. Tres problemas. Una solución: Inteligencia Artificial.**
