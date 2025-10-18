# 🏎️ Robot de Carreras con IA Multi-Algoritmo

## 📋 Descripción

**control inteligente para carreras autónomas** que combina tres algoritmos de inteligencia artificial: **Algoritmos Genéticos (GA)**, **Optimización por Enjambre de Partículas (PSO)** y **Colonias de Hormigas (ACO)** para controlar un robot en competencia contra 8 oponentes.

## 🎯 Características Principales

### 🧠 Arquitectura Híbrida Multi-Algoritmo

#### 1. 🧬 Algoritmo Genético (GA)
**Función:** Evolución y optimización de parámetros del controlador
```python
Parámetros optimizados:
- Agresividad:    0.6 - 0.9  (comportamiento ofensivo)
- Conservador:    0.2 - 0.4  (comportamiento defensivo)
- Adelantamiento: 0.7 - 0.95 (decisión de overtake)
- Umbral Riesgo:  0.4 - 0.6  (tolerancia al riesgo)
```

**Evolución:** Cada 10 segundos ajusta los parámetros basándose en el rendimiento

#### 2. 🐝 PSO - Particle Swarm Optimization
**Función:** Toma de decisiones para adelantamientos en tiempo real
```python
Criterios de decisión:
- Detección de oponentes (distancia < 50 unidades)
- Análisis de tramo de pista (recta/curva)
- Evaluación de agresividad y confianza
- Momento óptimo: INMEDIATO o ESPERAR
```

#### 3. 🐜 ACO - Ant Colony Optimization
**Función:** Optimización de trayectorias mediante feromonas virtuales
```python
Sistema de feromonas:
- 50 tramos de pista con niveles de feromona
- Rango: 1.0 - 20.0
- Refuerzo: Δτ = 1.0 / tiempo_tramo
- Visualización por intensidad de color
```

**Código de colores:**
- 🟡 Amarillo: Feromonas bajas (2.5-5.0)
- 🟠 Naranja: Feromonas medias (5.0-10.0)
- 🔴 Rojo: Feromonas altas (>10.0)

### 🏁 Sistema de Simulación

#### Robot Principal
- 🟡 **Color:** Dorado con borde rojo
- 🎯 **Objetivo:** Adelantar máximo número de oponentes
- 📊 **Tracking:** Trayectoria visible en tiempo real (cyan)
- ⚡ **Estados:** INICIANDO | ADELANTANDO | MANTENIENDO

#### 8 Oponentes
| Color | Código | Velocidad |
|-------|--------|-----------|
| 🔵 Azul | OP1 | 3.0 ± 0.5 |
| 🟢 Verde | OP2 | 3.0 ± 0.5 |
| 🔴 Rojo | OP3 | 3.0 ± 0.5 |
| 🟠 Naranja | OP4 | 3.0 ± 0.5 |
| 🟣 Púrpura | OP5 | 3.0 ± 0.5 |
| 🔵 Cyan | OP6 | 3.0 ± 0.5 |
| 🟣 Magenta | OP7 | 3.0 ± 0.5 |
| 🟡 Amarillo | OP8 | 3.0 ± 0.5 |

## 🚀 Uso

<img width="1131" height="661" alt="Captura de pantalla 2025-10-17 231318" src="https://github.com/user-attachments/assets/f03f5483-7111-4980-baab-9413d7e00cd0" />


https://github.com/user-attachments/assets/9cbf0a2c-5b6d-451e-912c-69278174d369



### Salida Esperada
```
🏁 Iniciando Simulador de Carreras de Robots...
🧠 Algoritmos activos: Genético, PSO, Hormigas
🎮 Visualizando: 8 competidores, feromonas, partículas PSO
⏹️ Cierra la ventana para terminar
```

## 📊 Visualización en Tiempo Real

### Panel Principal (Izquierdo)
- **Pista**: Fondo gris con líneas de carril
- **Feromonas**: Círculos de colores según intensidad
- **Partículas PSO**: Puntos cyan durante adelantamientos
- **Vehículos**: Círculos coloreados con flechas direccionales
- **Trayectoria**: Línea cyan siguiendo al robot principal

### Panel de Información (Derecho)
```
🚀 ROBOT DE CARRERAS IA

⏱️ Tiempo: XX.Xs
🏆 Adelantamientos: X
🎯 Estado: ESTADO_ACTUAL

🔧 PARÁMETROS:
⚡ Agresividad: 0.XX
🛡️ Conservador: 0.XX
💨 Adelantamiento: 0.XX
⚠️ Riesgo: 0.XX

🧠 ALGORITMOS:
• Genético (Parámetros)
• PSO (Adelantamientos)
• Hormigas (Trayectoria)
```

### Sistema de Feromonas

#### Actualización
```python
tramo = int((x - x_inicio) / ancho_pista × 50)
feromonas[tramo] += 1.0 / tiempo
feromonas = clip(feromonas, 1.0, 20.0)
```

#### Visualización
```python
for cada tramo con feromona > 2.5:
    tamaño = min(8, feromona / 3)
    alpha = min(0.8, feromona / 10)
    
    if feromona > 10:  color = 'red'
    elif feromona > 5: color = 'orange'
    else:              color = 'yellow'
```

### Generación de Partículas PSO
```python
# Durante adelantamiento
n_particulas = 15
for cada partícula:
    posición = robot_pos + random(-40, 40)
    agresividad = decision['agresividad']
    tamaño = 3 + agresividad × 5
    color = 'cyan', alpha = 0.6
```

## 📈 Métricas de Rendimiento

### Indicadores Principales
```python
adelantamientos_total    # Objetivo: maximizar
tiempo_promedio_vuelta   # Objetivo: minimizar
colisiones              # Objetivo: 0
estabilidad_trayectoria # Objetivo: alta
```

### Análisis de Parámetros Óptimos

| Escenario | Agresividad | Conservador | Adelantamiento | Riesgo |
|-----------|-------------|-------------|----------------|--------|
| **Agresivo** | 0.85-0.90 | 0.20-0.25 | 0.90-0.95 | 0.55-0.60 |
| **Balanceado** | 0.70-0.75 | 0.30-0.35 | 0.80-0.85 | 0.48-0.52 |
| **Conservador** | 0.60-0.65 | 0.35-0.40 | 0.70-0.75 | 0.40-0.45 |

## 🔧 Personalización

### Modificar Número de Oponentes
```python
# En setup_simulacion()
n_oponentes = 12  # Cambiar de 8 a 12
for i in range(n_oponentes):
    # ... código de creación
```

### Ajustar Velocidades
```python
# Robot
self.robot['velocidad'] = 5.0  # Más rápido

# Oponentes
'velocidad': 4.0 + random.uniform(-0.8, 0.8)  # Mayor variación
```

### Cambiar Tamaño de Pista
```python
self.pista = {
    'ancho': 1500,  # Más ancha
    'alto': 700,    # Más alta
    'x_inicio': 100,
    'y_inicio': 150
}
```

### Modificar Frecuencia de Evolución
```python
# Evolucionar cada 5 segundos en lugar de 10
if int(self.tiempo) % 5 == 0 and random.random() < 0.1:
    nuevos_params = self.controlador.ag.evolucionar([{}])
```
---


## 🎮 **Autor Paula S**
