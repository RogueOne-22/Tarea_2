#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GA: Evolución de Pokémon - VERSIÓN CON STATS ALEATORIOS Y VISUALIZACIÓN COMPLETA
- Stats iniciales randomizados para variedad
- Visualización completa como en la versión anterior
- ROUGE con specs diferentes cada simulación
"""

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
from pathlib import Path

# ----------------------------
# Parámetros MEJORADOS 
# ----------------------------
POP_SIZE = 80
N_GENS = 7
ELITISM = 3
MUTATION_RATE = 0.15
MUTATION_STD = 0.06
CROSSOVER_RATE = 0.85
SEED = None  # None para aleatoriedad total

# Ponderación del fitness
W_ATTACK = 0.35
W_DEFENSE = 0.15
W_SPEED  = 0.30
W_HP     = 0.20

# Sistema de evoluciones
MAX_EVOLUTIONS = 5
EVOLUTION_THRESHOLD = 0.50
EVOLUTION_BOOST = 0.15

# Si quieres reproducibilidad, usa SEED = 42. Para máxima aleatoriedad, SEED = None
if SEED is not None:
    random.seed(SEED)
    np.random.seed(SEED)
else:
    import time
    seed_val = int(time.time() * 1000) % 2**32
    random.seed(seed_val)
    np.random.seed(seed_val)
    print(f"🎲 Semilla aleatoria: {seed_val}")

# ----------------------------
# Clase Pokémon mejorada con stats aleatorios
# ----------------------------
class Pokemon:
    def __init__(self, nombre, tipo, origin, evolution_stage=0, stats_override=None):
        self.nombre = nombre
        self.tipo = tipo
        self.origin = origin
        self.evolution_stage = evolution_stage
        self.experience = 0
        self.can_evolve = True
        
        if stats_override:
            self.hp = stats_override['hp']
            self.attack = stats_override['attack']
            self.defense = stats_override['defense']
            self.speed = stats_override['speed']
        else:
            self.hp, self.attack, self.defense, self.speed = self.generar_stats_por_tipo(tipo)
        
    def generar_stats_por_tipo(self, tipo):
        tipo = tipo.lower()
        
        if tipo in ['fire', 'fuego']:
            hp = np.clip(np.random.normal(0.45, 0.10), 0.1, 0.9)
            attack = np.clip(np.random.normal(0.55, 0.12), 0.15, 0.95)
            defense = np.clip(np.random.normal(0.40, 0.08), 0.1, 0.8)
            speed = np.clip(np.random.normal(0.60, 0.10), 0.2, 0.95)
            
        elif tipo in ['water', 'agua']:
            hp = np.clip(np.random.normal(0.50, 0.09), 0.15, 0.9)
            attack = np.clip(np.random.normal(0.48, 0.10), 0.1, 0.85)
            defense = np.clip(np.random.normal(0.55, 0.11), 0.2, 0.9)
            speed = np.clip(np.random.normal(0.45, 0.09), 0.1, 0.8)
            
        elif tipo in ['grass', 'planta']:
            hp = np.clip(np.random.normal(0.55, 0.12), 0.2, 0.95)
            attack = np.clip(np.random.normal(0.45, 0.10), 0.1, 0.8)
            defense = np.clip(np.random.normal(0.50, 0.09), 0.15, 0.85)
            speed = np.clip(np.random.normal(0.40, 0.08), 0.1, 0.75)
            
        elif tipo in ['electric', 'eléctrico']:
            hp = np.clip(np.random.normal(0.40, 0.08), 0.1, 0.8)
            attack = np.clip(np.random.normal(0.52, 0.11), 0.15, 0.9)
            defense = np.clip(np.random.normal(0.42, 0.07), 0.1, 0.75)
            speed = np.clip(np.random.normal(0.65, 0.12), 0.25, 0.95)
            
        else:
            hp = np.clip(np.random.normal(0.48, 0.10), 0.1, 0.9)
            attack = np.clip(np.random.normal(0.48, 0.10), 0.1, 0.9)
            defense = np.clip(np.random.normal(0.48, 0.10), 0.1, 0.9)
            speed = np.clip(np.random.normal(0.48, 0.10), 0.1, 0.9)
        
        return hp, attack, defense, speed
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'tipo': self.tipo,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'origin': self.origin,
            'evolution_stage': self.evolution_stage,
            'experience': self.experience,
            'fitness': self.calculate_fitness()
        }
    
    def calculate_fitness(self):
        val = (self.attack * W_ATTACK +
               self.defense * W_DEFENSE +
               self.speed * W_SPEED +
               self.hp * W_HP)
        if self.tipo.lower() in ['fire', 'fuego']:
            val *= 1.08
        elif self.tipo.lower() in ['electric', 'eléctrico']:
            val *= 1.05
        return val
    
    def add_experience(self, amount):
        self.experience += amount
        return self.check_evolution()
    
    def check_evolution(self):
        if (self.calculate_fitness() >= EVOLUTION_THRESHOLD and 
            self.can_evolve and 
            self.evolution_stage < MAX_EVOLUTIONS):
            return True
        return False
    
    def evolve(self):
        if not self.check_evolution():
            return False
        
        self.evolution_stage += 1
        evolution_boost = EVOLUTION_BOOST * (1 + 0.1 * self.evolution_stage)
        
        if self.origin == 'ROUGE' or self.tipo.lower() in ['fire', 'fuego']:
            self.speed = min(1.0, self.speed + evolution_boost * 1.3)
            self.attack = min(1.0, self.attack + evolution_boost * 1.2)
            self.hp = min(1.0, self.hp + evolution_boost * 0.8)
            self.defense = min(1.0, self.defense + evolution_boost * 0.7)
        elif self.tipo.lower() in ['water', 'agua']:
            self.defense = min(1.0, self.defense + evolution_boost * 1.2)
            self.hp = min(1.0, self.hp + evolution_boost * 1.1)
            self.attack = min(1.0, self.attack + evolution_boost)
            self.speed = min(1.0, self.speed + evolution_boost * 0.8)
        else:
            self.attack = min(1.0, self.attack + evolution_boost)
            self.speed = min(1.0, self.speed + evolution_boost * 0.9)
            self.hp = min(1.0, self.hp + evolution_boost * 0.8)
            self.defense = min(1.0, self.defense + evolution_boost * 0.7)
        
        if self.origin == 'ROUGE':
            evolution_names = ['ROUGE', 'ROUGE-II', 'ROUGE-III', 'ROUGE-IV', 'ROUGE-V', 'ROUGE-OMEGA']
            if self.evolution_stage < len(evolution_names):
                self.nombre = evolution_names[self.evolution_stage]
        else:
            evolution_suffixes = ['', '-II', '-III', '-IV', '-V', '-OMEGA']
            base_name = self.nombre.split('-')[0]
            self.nombre = f"{base_name}{evolution_suffixes[self.evolution_stage]}"
        
        print(f"🎉 {self.origin} evolucionó a {self.nombre}!")
        return True

# ----------------------------
# Generación de ROUGE aleatorio
# ----------------------------
def generar_rouge_aleatorio():
    base_hp = random.randint(65, 80)
    base_attack = random.randint(45, 60)
    base_defense = random.randint(55, 70)
    base_speed = random.randint(85, 100)
    
    max_vals = {'HP': 100, 'Attack': 100, 'Defense': 100, 'Speed': 100}
    
    return {
        'hp': base_hp / max_vals['HP'],
        'attack': base_attack / max_vals['Attack'],
        'defense': base_defense / max_vals['Defense'],
        'speed': base_speed / max_vals['Speed']
    }

# ----------------------------
# Población inicial completamente aleatoria
# ----------------------------
def crear_poblacion_aleatoria(tamanio=80):
    population = []
    tipos = ['Fire', 'Water', 'Grass', 'Electric', 'Normal', 'Rock', 'Fighting']
    
    for i in range(tamanio - 1):
        tipo = random.choice(tipos)
        pokemon = Pokemon(
            nombre=f'Kanto_{i+1:03d}',
            tipo=tipo,
            origin=f'Kanto_{i+1:03d}'
        )
        population.append(pokemon)
    
    rouge_stats = generar_rouge_aleatorio()
    rouge = Pokemon(
        nombre='ROUGE',
        tipo='Fire',
        origin='ROUGE',
        stats_override=rouge_stats
    )
    population.append(rouge)
    
    return population

# ----------------------------
# Operadores GA
# ----------------------------
def roulette_selection(population):
    fits = [p.calculate_fitness() for p in population]
    total = sum(fits)
    if total <= 0:
        return random.choice(population)
    probs = [f/total for f in fits]
    idx = np.random.choice(len(population), p=probs)
    return population[int(idx)]

def crossover(p1, p2):
    alpha = np.random.rand()
    
    hp = np.clip(alpha * p1.hp + (1-alpha) * p2.hp, 0.0, 1.0)
    attack = np.clip(alpha * p1.attack + (1-alpha) * p2.attack, 0.0, 1.0)
    defense = np.clip(alpha * p1.defense + (1-alpha) * p2.defense, 0.0, 1.0)
    speed = np.clip(alpha * p1.speed + (1-alpha) * p2.speed, 0.0, 1.0)
    
    tipo = random.choice([p1.tipo, p2.tipo])
    
    if p1.calculate_fitness() > p2.calculate_fitness():
        origin = p1.origin
    else:
        origin = p2.origin
    
    child = Pokemon(
        nombre=f"Child_{random.randint(0,99999):06d}",
        tipo=tipo,
        origin=origin
    )
    
    child.hp = hp
    child.attack = attack
    child.defense = defense
    child.speed = speed
    
    return child

def mutate(pokemon):
    if random.random() < MUTATION_RATE:
        pokemon.hp = np.clip(pokemon.hp + np.random.normal(0, MUTATION_STD), 0.0, 1.0)
    if random.random() < MUTATION_RATE:
        pokemon.attack = np.clip(pokemon.attack + np.random.normal(0, MUTATION_STD), 0.0, 1.0)
    if random.random() < MUTATION_RATE:
        pokemon.defense = np.clip(pokemon.defense + np.random.normal(0, MUTATION_STD), 0.0, 1.0)
    if random.random() < MUTATION_RATE:
        pokemon.speed = np.clip(pokemon.speed + np.random.normal(0, MUTATION_STD), 0.0, 1.0)
    return pokemon

# ----------------------------
# Sistema de experiencia mejorado
# ----------------------------
def distribuir_experiencia(population, generacion):
    for pokemon in population:
        base_exp = 0.12 + (generacion * 0.025)
        fitness_bonus = pokemon.calculate_fitness() * 0.06
        
        elite_cutoff = sorted(population, key=lambda x: x.calculate_fitness(), reverse=True)[:ELITISM]
        if pokemon in elite_cutoff:
            elite_bonus = 0.12
        else:
            elite_bonus = 0
        
        if pokemon.calculate_fitness() < 0.4:
            low_fitness_bonus = 0.15
        else:
            low_fitness_bonus = 0
        
        total_exp = base_exp + fitness_bonus + elite_bonus + low_fitness_bonus
        pokemon.add_experience(total_exp)

def aplicar_evoluciones(population, generacion):
    evoluciones_esta_generacion = []
    
    for pokemon in population:
        if (generacion >= 5 and 
            pokemon.evolution_stage == 0 and 
            pokemon.calculate_fitness() < EVOLUTION_THRESHOLD and
            random.random() < 0.3):
            
            print(f"🎯 Evolución asistida para {pokemon.nombre}")
            old_stats = pokemon.to_dict().copy()
            if pokemon.evolve():
                new_stats = pokemon.to_dict()
                evoluciones_esta_generacion.append({
                    'generacion': generacion,
                    'pokemon': pokemon.origin,
                    'nombre_anterior': old_stats['nombre'],
                    'nombre_nuevo': new_stats['nombre'],
                    'etapa': pokemon.evolution_stage,
                    'fitness_antes': old_stats['fitness'],
                    'fitness_despues': new_stats['fitness'],
                    'mejora': new_stats['fitness'] - old_stats['fitness'],
                    'tipo': 'asistida'
                })
        
        elif pokemon.check_evolution():
            old_stats = pokemon.to_dict().copy()
            if pokemon.evolve():
                new_stats = pokemon.to_dict()
                evoluciones_esta_generacion.append({
                    'generacion': generacion,
                    'pokemon': pokemon.origin,
                    'nombre_anterior': old_stats['nombre'],
                    'nombre_nuevo': new_stats['nombre'],
                    'etapa': pokemon.evolution_stage,
                    'fitness_antes': old_stats['fitness'],
                    'fitness_despues': new_stats['fitness'],
                    'mejora': new_stats['fitness'] - old_stats['fitness'],
                    'tipo': 'normal'
                })
    
    return evoluciones_esta_generacion

# ----------------------------
# VISUALIZACIÓN COMPLETA (como en la versión anterior)
# ----------------------------
print("🎲 INICIANDO SIMULACIÓN CON STATS ALEATORIOS...")

population = crear_poblacion_aleatoria(POP_SIZE)

print("\n📊 MUESTRA DE STATS INICIALES (aleatorios):")
sample_indices = random.sample(range(len(population)), 5)
for idx in sample_indices:
    p = population[idx]
    print(f"   {p.nombre:12} {p.tipo:8} "
          f"ATK:{p.attack:.3f} DEF:{p.defense:.3f} "
          f"SPD:{p.speed:.3f} HP:{p.hp:.3f}")

rouge_inicial = next((p for p in population if p.origin == 'ROUGE'), None)
if rouge_inicial:
    print(f"\n🔥 ROUGE INICIAL:")
    print(f"   ATK:{rouge_inicial.attack:.3f} DEF:{rouge_inicial.defense:.3f} "
          f"SPD:{rouge_inicial.speed:.3f} HP:{rouge_inicial.hp:.3f}")
    print(f"   Fitness inicial: {rouge_inicial.calculate_fitness():.3f}")

# CONFIGURACIÓN COMPLETA DE VISUALIZACIÓN
plt.ion()
fig = plt.figure(figsize=(16, 10))
fig.suptitle('🎮 SISTEMA DE EVOLUCIÓN POKÉMON - STATS ALEATORIOS CADA SIMULACIÓN', fontsize=16, fontweight='bold')

# Grid specification como antes
gs = plt.GridSpec(3, 3, figure=fig)

ax_curve = fig.add_subplot(gs[0, :2])
ax_scatter = fig.add_subplot(gs[1, :2])
ax_evolutions = fig.add_subplot(gs[2, :2])
ax_info = fig.add_subplot(gs[:, 2])

# Configurar ejes
ax_curve.set_title("📈 Evolución del Fitness por Generación", fontweight='bold')
ax_curve.set_xlabel("Generación")
ax_curve.set_ylabel("Fitness")
ax_curve.grid(True, alpha=0.3)

ax_scatter.set_title("⚔️ Ataque vs Velocidad (Tamaño = Etapa Evolución)", fontweight='bold')
ax_scatter.set_xlabel("Ataque (normalizado)")
ax_scatter.set_ylabel("Velocidad (normalizado)")

ax_evolutions.set_title("🔄 Progreso de Evoluciones", fontweight='bold')
ax_evolutions.set_xlabel("Generación")
ax_evolutions.set_ylabel("Etapa de Evolución")
ax_evolutions.grid(True, alpha=0.3)

ax_info.axis('off')
info_text = ax_info.text(0.02, 0.98, "", va='top', fontfamily='monospace', fontsize=9, wrap=True)

# Datos para tracking
history_best = []
history_mean = []
history_rouge_fitness = []
history_evolutions = {f'Etapa_{i}': [] for i in range(MAX_EVOLUTIONS + 1)}
gens = []
all_evolutions = []

# ----------------------------
# BUCLE EVOLUTIVO COMPLETO
# ----------------------------
print("\n🎯 INICIANDO SIMULACIÓN DE EVOLUCIONES...")
for generacion in range(1, N_GENS + 1):
    print(f"\n--- Generación {generacion} ---")
    
    # Calcular fitness
    fits = [p.calculate_fitness() for p in population]
    best_idx = int(np.argmax(fits))
    best_fit = float(fits[best_idx])
    mean_fit = float(np.mean(fits))
    
    # Distribuir experiencia
    distribuir_experiencia(population, generacion)
    
    # Aplicar evoluciones
    evoluciones_gen = aplicar_evoluciones(population, generacion)
    all_evolutions.extend(evoluciones_gen)
    
    # Tracking
    history_best.append(best_fit)
    history_mean.append(mean_fit)
    gens.append(generacion)
    
    # Tracking de ROUGE
    rouge_pokemon = [p for p in population if p.origin == 'ROUGE']
    if rouge_pokemon:
        rouge_best = max([p.calculate_fitness() for p in rouge_pokemon])
        rouge_count = len(rouge_pokemon)
        rouge_avg_stage = np.mean([p.evolution_stage for p in rouge_pokemon])
        history_rouge_fitness.append(rouge_best)
    else:
        rouge_best = 0.0
        rouge_count = 0
        rouge_avg_stage = 0
        history_rouge_fitness.append(0.0)
    
    # Tracking de evoluciones por etapa
    for etapa in range(MAX_EVOLUTIONS + 1):
        count = sum(1 for p in population if p.evolution_stage == etapa)
        history_evolutions[f'Etapa_{etapa}'].append(count)
    
    # --- ACTUALIZAR VISUALIZACIONES COMPLETAS ---
    
    # 1. Gráfico de fitness
    ax_curve.clear()
    ax_curve.plot(gens, history_best, 'b-', label='Mejor Fitness', linewidth=2, marker='o')
    ax_curve.plot(gens, history_mean, 'orange', label='Fitness Promedio', linewidth=2, marker='s')
    ax_curve.plot(gens, history_rouge_fitness, 'red', label='Mejor ROUGE', linewidth=2, marker='^')
    ax_curve.set_title(f"📈 Evolución del Fitness (Gen {generacion})", fontweight='bold')
    ax_curve.legend()
    ax_curve.grid(True, alpha=0.3)
    ax_curve.set_xlim(1, max(2, generacion))
    ax_curve.set_ylim(0, max(0.8, max(history_best) * 1.1))
    
    # 2. Scatter plot mejorado
    ax_scatter.clear()
    attacks = [p.attack for p in population]
    speeds = [p.speed for p in population]
    colors = []
    sizes = []
    
    for p in population:
        if p.origin == 'ROUGE':
            colors.append('red')
            sizes.append(100 + (p.evolution_stage * 40))
        elif 'Kanto' in p.origin:
            colors.append('blue')
            sizes.append(60 + (p.evolution_stage * 30))
        else:
            colors.append('green')
            sizes.append(50 + (p.evolution_stage * 20))
    
    scatter = ax_scatter.scatter(attacks, speeds, c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=0.5)
    ax_scatter.set_title(f"⚔️ Ataque vs Velocidad - Gen {generacion}", fontweight='bold')
    ax_scatter.set_xlim(0, 1)
    ax_scatter.set_ylim(0, 1)
    ax_scatter.grid(True, alpha=0.3)
    
    # 3. Gráfico de evoluciones
    ax_evolutions.clear()
    for etapa in range(MAX_EVOLUTIONS + 1):
        ax_evolutions.plot(gens, history_evolutions[f'Etapa_{etapa}'], 
                          label=f'Etapa {etapa}', linewidth=2, marker='.')
    ax_evolutions.set_title(f"🔄 Progreso de Evoluciones - Gen {generacion}", fontweight='bold')
    ax_evolutions.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax_evolutions.set_xlim(1, max(2, generacion))
    ax_evolutions.set_ylim(0, POP_SIZE)
    
    # 4. Panel de información
    best_pokemon = population[best_idx]
    evoluciones_text = "\n".join([f"• {e['nombre_anterior']} → {e['nombre_nuevo']}" 
                                for e in evoluciones_gen[-3:]]) if evoluciones_gen else "Ninguna"
    
    info_str = f"""🎮 GENERACIÓN {generacion}

🏆 MEJOR POKÉMON:
Nombre: {best_pokemon.nombre}
Origen: {best_pokemon.origin}
Tipo: {best_pokemon.tipo}
Etapa: {best_pokemon.evolution_stage}
Fitness: {best_fit:.4f}

📊 ESTADÍSTICAS:
Ataque: {best_pokemon.attack:.3f}
Defensa: {best_pokemon.defense:.3f}
Velocidad: {best_pokemon.speed:.3f}
HP: {best_pokemon.hp:.3f}

🔥 INFO ROUGE:
Mejor Fitness: {rouge_best:.4f}
Cantidad: {rouge_count}
Etapa Promedio: {rouge_avg_stage:.1f}

🔄 EVOLUCIONES RECIENTES:
{evoluciones_text}

📈 POBLACIÓN:
Total: {len(population)}
Evoluciones: {len(evoluciones_gen)} esta gen.
"""
    info_text.set_text(info_str)
    
    plt.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    # --- CREAR NUEVA GENERACIÓN ---
    sorted_pop = sorted(population, key=lambda x: x.calculate_fitness(), reverse=True)
    new_population = sorted_pop[:ELITISM].copy()
    
    while len(new_population) < POP_SIZE:
        parent1 = roulette_selection(population)
        parent2 = roulette_selection(population)
        
        if random.random() < CROSSOVER_RATE:
            child = crossover(parent1, parent2)
        else:
            child = parent1
        
        child = mutate(child)
        new_population.append(child)
    
    population = new_population[:POP_SIZE]
    
    # Reporte de progreso
    print(f"✅ Gen {generacion}: Mejor fitness = {best_fit:.4f}")
    print(f"   Evoluciones esta gen: {len(evoluciones_gen)}")
    print(f"   Mejor ROUGE: {rouge_best:.4f} (Etapa avg: {rouge_avg_stage:.1f})")

# ----------------------------
# FIN DE LA SIMULACIÓN
# ----------------------------
plt.ioff()

# Guardar resultados
OUT_CSV_POP_FINAL = Path("kanto_pop_final_aleatorio.csv")
OUT_CSV_HISTORY = Path("historial_aleatorio.csv")
OUT_CSV_EVOLUTIONS = Path("evoluciones_aleatorio.csv")

df_final = pd.DataFrame([p.to_dict() for p in population])
df_final = df_final.sort_values('fitness', ascending=False).reset_index(drop=True)
df_final.to_csv(OUT_CSV_POP_FINAL, index=False)

df_hist = pd.DataFrame({
    'generacion': gens,
    'best_fitness': history_best,
    'mean_fitness': history_mean,
    'rouge_fitness': history_rouge_fitness
})
df_hist.to_csv(OUT_CSV_HISTORY, index=False)

if all_evolutions:
    df_evol = pd.DataFrame(all_evolutions)
    df_evol.to_csv(OUT_CSV_EVOLUTIONS, index=False)

print(f"\n🎉 SIMULACIÓN COMPLETADA!")
print(f"📁 Resultados guardados:")
print(f"   - Población final: {OUT_CSV_POP_FINAL}")
print(f"   - Historial fitness: {OUT_CSV_HISTORY}")
print(f"   - Registro evoluciones: {OUT_CSV_EVOLUTIONS}")

# Mostrar resumen final
print(f"\n📊 RESUMEN FINAL:")
print(f"   Generaciones simuladas: {N_GENS}")
print(f"   Total de evoluciones: {len(all_evolutions)}")
print(f"   Mejor fitness alcanzado: {max(history_best):.4f}")

# Top 10 Pokémon
print(f"\n🏆 TOP 10 POKÉMON FINALES:")
top_10 = df_final.head(10)
for i, (_, row) in enumerate(top_10.iterrows(), 1):
    print(f"   {i:2d}. {row['nombre']:15} {row['origin']:10} "
          f"Tipo:{row['tipo']:8} Etapa:{row['evolution_stage']} Fit:{row['fitness']:.4f}")

# Evoluciones de ROUGE
rouge_final = [p for p in population if p.origin == 'ROUGE']
if rouge_final:
    print(f"\n🔥 EVOLUCIONES ROUGE FINALES:")
    for rouge in sorted(rouge_final, key=lambda x: x.calculate_fitness(), reverse=True):
        print(f"   • {rouge.nombre}: Etapa {rouge.evolution_stage}, "
              f"Fitness: {rouge.calculate_fitness():.4f}, "
              f"Tipo: {rouge.tipo}")

print(f"   ¡Ejecuta de nuevo para ver resultados diferentes!")

plt.show()