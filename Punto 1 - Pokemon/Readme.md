# 🎮 Sistema de Evolución Pokémon con Algoritmos Genéticos

## 📋 Descripción

 *Algoritmo Genético (GA)** que simula la evolución de Pokémon mediante selección natural, crossover y mutación. 
 
 Incluye un Pokémon especial llamado **ROUGE**  unico con stats aleatorios en cada ejecución, generando diferentes resultados en cada simulación.

 <img width="335" height="358" alt="Captura de pantalla 2025-10-17 221156" src="https://github.com/user-attachments/assets/9e746e46-bf48-4293-9f16-93d453d43e9e" />


## 🔑 Características Técnicas Clave

### ⚙️ Parámetros del Algoritmo Genético
```python
POP_SIZE = 80              # Tamaño de población
N_GENS = 7                 # Número de generaciones
ELITISM = 3                # Individuos élite preservados
MUTATION_RATE = 0.15       # Probabilidad de mutación (15%)
CROSSOVER_RATE = 0.85      # Probabilidad de crossover (85%)
MUTATION_STD = 0.06        # Desviación estándar de mutación
```

### 🧬 Función de Fitness Ponderada
```python
fitness = (0.35 × Ataque) + (0.15 × Defensa) + (0.30 × Velocidad) + (0.20 × HP)
```

**Bonificaciones de tipo:**
- 🔥 Fire: +8% fitness
- ⚡ Electric: +5% fitness

### 🔄 Sistema de Evoluciones

#### Parámetros
- **Umbral de evolución**: Fitness ≥ 0.50
- **Boost por evolución**: +15% (con incremento progresivo)
- **Máximo de evoluciones**: 5 etapas
- **Evolución asistida**: Activada en generación 5+ para Pokémon con bajo fitness

#### Boost por Tipo
```python
Fire/ROUGE:    Speed +30%, Attack +20%, HP +8%, Defense +7%
Water:         Defense +20%, HP +11%, Attack +10%, Speed +8%
Otros:         Attack +10%, Speed +9%, HP +8%, Defense +7%
```

### 🎲 Generación de Stats Aleatorios

#### Distribuciones por Tipo (Media ± Desviación)
| Tipo | HP | Attack | Defense | Speed |
|------|-------|--------|---------|-------|
| 🔥 Fire | 0.45±0.10 | 0.55±0.12 | 0.40±0.08 | 0.60±0.10 |
| 💧 Water | 0.50±0.09 | 0.48±0.10 | 0.55±0.11 | 0.45±0.09 |
| 🌿 Grass | 0.55±0.12 | 0.45±0.10 | 0.50±0.09 | 0.40±0.08 |
| ⚡ Electric | 0.40±0.08 | 0.52±0.11 | 0.42±0.07 | 0.65±0.12 |

**Nota**: Todos los valores están normalizados en rango [0, 1]

### 🔥 ROUGE - Pokémon Especial

**Generación aleatoria en cada ejecución:**
```python
HP:      65-80  → normalizado
Attack:  45-60  → normalizado
Defense: 55-70  → normalizado
Speed:   85-100 → normalizado
```

**Ventajas de ROUGE:**
- Bonificación de tipo Fire (+8%)
- Mayor boost en evoluciones (Speed +30%, Attack +20%)
- Cadena de evoluciones: ROUGE → ROUGE-II → ROUGE-III → ROUGE-IV → ROUGE-V → ROUGE-OMEGA

## 📊 Visualización en Tiempo Real

El sistema muestra 4 paneles interactivos:

<img width="1901" height="960" alt="Captura de pantalla 2025-10-17 220503" src="https://github.com/user-attachments/assets/43f23e39-b51a-4303-8f20-02976e3d1cba" />

### 1. 📈 Evolución del Fitness
- Mejor fitness por generación
- Fitness promedio
- Mejor fitness de ROUGE

### 2. ⚔️ Scatter Plot (Ataque vs Velocidad)
- Tamaño = Etapa de evolución
- Color: 🔴 ROUGE | 🔵 Kanto | 🟢 Híbridos

### 3. 🔄 Progreso de Evoluciones
- Distribución por etapa evolutiva
- Tracking de todas las etapas (0-5)

### 4. 📋 Panel de Información
- Mejor Pokémon de la generación
- Estadísticas de ROUGE
- Evoluciones recientes

## 🔬 Detalles Técnicos Avanzados

### Estrategia Evolutiva
1. **Elitismo**: Preserva los 3 mejores individuos
2. **Selección proporcional**: Basada en fitness
3. **Crossover aritmético**: Combina stats de padres
4. **Mutación adaptativa**: Gaussiana con σ = 0.06

### Control de Diversidad
- Stats aleatorios por tipo
- Mutación en cada stat independiente
- Crossover probabilístico (85%)
- Evolución asistida para individuos débiles

### Convergencia
- Típicamente 5-7 generaciones
- Mejora continua del fitness promedio
- ROUGE alcanza etapas avanzadas en gen 4-6

## 📊 Resultados Típicos

```
Generación 1:  Mejor fitness ≈ 0.45-0.52
Generación 3:  Mejor fitness ≈ 0.55-0.65
Generación 5:  Mejor fitness ≈ 0.65-0.75
Generación 7:  Mejor fitness ≈ 0.70-0.85
```

**ROUGE típicamente:**
- Fitness inicial: 0.48-0.58
- Fitness final: 0.65-0.80
- Etapa evolutiva: 3-5

## 🎮 Ejemplo de Salida

```
🎲 Semilla aleatoria: 1729845632

🔥 ROUGE INICIAL:
   ATK:0.520 DEF:0.614 SPD:0.912 HP:0.730
   Fitness inicial: 0.683

--- Generación 1 ---
✅ Gen 1: Mejor fitness = 0.5241
   Evoluciones esta gen: 0

--- Generación 5 ---
🎉 ROUGE evolucionó a ROUGE-II!
✅ Gen 5: Mejor fitness = 0.7183
   Evoluciones esta gen: 12

🏆 TOP 10 POKÉMON FINALES:
   1. ROUGE-IV       ROUGE      Tipo:Fire     Etapa:4 Fit:0.8543
   2. Child_042891   Kanto_023  Tipo:Electric Etapa:3 Fit:0.7921
   3. Kanto_045-II   Kanto_045  Tipo:Fire     Etapa:2 Fit:0.7654
```
<img width="1888" height="954" alt="Captura de pantalla 2025-10-17 220345" src="https://github.com/user-attachments/assets/4acace5f-13ad-428a-8c54-4fc744677740" />

---

🎮 ***Autor Paula S***
