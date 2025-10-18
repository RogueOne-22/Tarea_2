import numpy as np
import random
import math
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle

# ========== CLASES DEL CONTROLADOR ==========
class AlgoritmoGenetico:
    def __init__(self):
        self.mejor_controlador = None
    
    def evolucionar(self, historial_rendimiento):
        # Simulación simple de evolución
        if not historial_rendimiento:
            return {
                'agresividad': 0.7,
                'conservador': 0.3,
                'adelantamiento': 0.8,
                'umbral_riesgo': 0.5
            }
        
        # Mejorar parámetros basado en rendimiento
        nuevo_controlador = {
            'agresividad': min(0.9, random.uniform(0.6, 0.9)),
            'conservador': random.uniform(0.2, 0.4),
            'adelantamiento': min(0.95, random.uniform(0.7, 0.95)),
            'umbral_riesgo': random.uniform(0.4, 0.6)
        }
        return nuevo_controlador

class ControladorPSO:
    def decidir_adelantamiento(self, oponentes, pista):
        # Simular decisión de PSO
        oponentes_cerca = any(o['distancia'] < 50 for o in oponentes)
        
        if oponentes_cerca and pista.get('es_recta', True):
            return {
                'adelantar': True,
                'agresividad': random.uniform(0.6, 0.9),
                'velocidad': random.uniform(0.7, 1.0),
                'confianza': random.uniform(0.7, 0.9),
                'momento': 'INMEDIATO'
            }
        else:
            return {
                'adelantar': False,
                'momento': 'ESPERAR',
                'confianza': 0.3
            }

class HormigaRacing:
    def __init__(self):
        self.feromonas = np.ones(50) * 2.0
    
    def reforzar_trayectoria(self, tramo, tiempo):
        if tiempo > 0:
            self.feromonas[tramo % len(self.feromonas)] += 1.0 / tiempo
            self.feromonas = np.clip(self.feromonas, 1.0, 20.0)

# ========== CONTROLADOR PRINCIPAL ==========
class ControladorRobotCarreras:
    def __init__(self):
        self.ag = AlgoritmoGenetico()
        self.pso = ControladorPSO()
        self.hormigas = HormigaRacing()
        
        self.parametros = {
            'agresividad': 0.7,
            'conservador': 0.3,
            'adelantamiento': 0.8,
            'umbral_riesgo': 0.5
        }

# ========== SIMULADOR FUNCIONAL ==========
class SimuladorCarrerasFuncional:
    def __init__(self):
        self.fig, (self.ax_main, self.ax_info) = plt.subplots(1, 2, figsize=(15, 8))
        self.controlador = ControladorRobotCarreras()
        self.setup_simulacion()
        
    def setup_simulacion(self):
        # Robot principal
        self.robot = {
            'x': 200, 'y': 350, 'velocidad': 4.0, 'angulo': 0,
            'trayectoria': [], 'adelantamientos': 0
        }
        
        # 8 oponentes
        self.oponentes = []
        colores = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        for i in range(8):
            self.oponentes.append({
                'x': 100 + i * 30,
                'y': 200 + (i % 4) * 100,
                'velocidad': 3.0 + random.uniform(-0.5, 0.5),
                'color': colores[i],
                'nombre': f'OP{i+1}'
            })
        
        # Pista
        self.pista = {
            'ancho': 1000,
            'alto': 500,
            'x_inicio': 100,
            'y_inicio': 150
        }
        
        self.particulas = []
        self.tiempo = 0
        self.estado_actual = "INICIANDO"

    def dibujar_pista(self):
        # Fondo
        self.ax_main.add_patch(Rectangle((0, 0), 1200, 700, facecolor='darkgreen', alpha=0.3))
        
        # Pista
        self.ax_main.add_patch(Rectangle(
            (self.pista['x_inicio'], self.pista['y_inicio']),
            self.pista['ancho'], self.pista['alto'],
            facecolor='gray', alpha=0.8, edgecolor='white', linewidth=3
        ))
        
        # Líneas de carril
        for i in range(1, 4):
            y = self.pista['y_inicio'] + i * self.pista['alto'] / 4
            self.ax_main.axhline(y, color='white', linestyle='--', alpha=0.7)

    def dibujar_feromonas(self):
        for i, fuerza in enumerate(self.controlador.hormigas.feromonas):
            if fuerza > 2.5:
                x = self.pista['x_inicio'] + (i / len(self.controlador.hormigas.feromonas)) * self.pista['ancho']
                for carril in range(3):
                    y = self.pista['y_inicio'] + 60 + carril * 120
                    tamaño = min(8, fuerza / 3)
                    alpha = min(0.8, fuerza / 10)
                    
                    if fuerza > 10:
                        color = 'red'
                    elif fuerza > 5:
                        color = 'orange'
                    else:
                        color = 'yellow'
                    
                    self.ax_main.add_patch(Circle((x, y), tamaño, color=color, alpha=alpha))

    def dibujar_particulas(self):
        for particula in self.particulas:
            x, y = particula['posicion']
            tamaño = 3 + particula.get('agresividad', 0.5) * 5
            alpha = 0.6
            
            self.ax_main.add_patch(Circle((x, y), tamaño, color='cyan', alpha=alpha))

    def dibujar_vehiculos(self):
        # Oponentes
        for oponente in self.oponentes:
            self.ax_main.add_patch(Circle(
                (oponente['x'], oponente['y']), 12,
                color=oponente['color'], alpha=0.8, edgecolor='white'
            ))
            
            # Dirección
            dx = oponente['velocidad'] * 10
            self.ax_main.arrow(oponente['x'], oponente['y'], dx, 0, 
                             head_width=8, head_length=5, fc='white', ec='white')

        # Robot principal
        self.ax_main.add_patch(Circle(
            (self.robot['x'], self.robot['y']), 15,
            color='gold', alpha=1.0, edgecolor='red', linewidth=3
        ))
        
        # Dirección del robot
        dx = math.cos(self.robot['angulo']) * 20
        dy = math.sin(self.robot['angulo']) * 20
        self.ax_main.arrow(self.robot['x'], self.robot['y'], dx, dy,
                         head_width=10, head_length=8, fc='red', ec='red')

        # Trayectoria
        if len(self.robot['trayectoria']) > 1:
            x_vals = [p[0] for p in self.robot['trayectoria']]
            y_vals = [p[1] for p in self.robot['trayectoria']]
            self.ax_main.plot(x_vals, y_vals, 'cyan', alpha=0.6, linewidth=2)

    def dibujar_info(self):
        self.ax_info.clear()
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        self.ax_info.axis('off')
        
        params = self.controlador.parametros
        
        info_text = (
            "🚀 ROBOT DE CARRERAS IA\n\n"
            f"⏱️ Tiempo: {self.tiempo:.1f}s\n"
            f"🏆 Adelantamientos: {self.robot['adelantamientos']}\n"
            f"🎯 Estado: {self.estado_actual}\n\n"
            "🔧 PARÁMETROS:\n"
            f"⚡ Agresividad: {params['agresividad']:.2f}\n"
            f"🛡️ Conservador: {params['conservador']:.2f}\n"
            f"💨 Adelantamiento: {params['adelantamiento']:.2f}\n"
            f"⚠️ Riesgo: {params['umbral_riesgo']:.2f}\n\n"
            "🧠 ALGORITMOS:\n"
            "• Genético (Parámetros)\n"
            "• PSO (Adelantamientos)\n"
            "• Hormigas (Trayectoria)"
        )
        
        self.ax_info.text(0.05, 0.95, info_text, fontsize=12, fontfamily='monospace',
                         verticalalignment='top', linespacing=1.5,
                         bbox=dict(boxstyle="round,pad=1", facecolor="black", alpha=0.8))

    def actualizar_simulacion(self):
        self.tiempo += 0.1
        
        # Mover oponentes
        for oponente in self.oponentes:
            oponente['x'] += oponente['velocidad']
            if oponente['x'] > self.pista['x_inicio'] + self.pista['ancho']:
                oponente['x'] = self.pista['x_inicio'] - 50
            oponente['y'] += random.uniform(-2, 2)
            oponente['y'] = max(self.pista['y_inicio'] + 20, 
                              min(self.pista['y_inicio'] + self.pista['alto'] - 20, 
                                  oponente['y']))

        # Preparar datos para controlador
        oponentes_data = []
        for oponente in self.oponentes:
            distancia = math.sqrt((self.robot['x'] - oponente['x'])**2 + 
                                (self.robot['y'] - oponente['y'])**2)
            oponentes_data.append({'distancia': distancia})

        # Tomar decisión
        decision = self.controlador.pso.decidir_adelantamiento(
            oponentes_data, 
            {'es_recta': True}
        )
        
        # Aplicar decisión
        if decision['adelantar']:
            self.robot['velocidad'] = 5.0
            self.robot['angulo'] = random.uniform(-0.3, 0.3)
            self.estado_actual = "ADELANTANDO ⚡"
            
            # Generar partículas
            self.particulas = []
            for _ in range(15):
                self.particulas.append({
                    'posicion': (
                        self.robot['x'] + random.uniform(-40, 40),
                        self.robot['y'] + random.uniform(-40, 40)
                    ),
                    'agresividad': decision['agresividad']
                })
        else:
            self.robot['velocidad'] = 4.0
            self.robot['angulo'] = 0
            self.estado_actual = "MANTENIENDO 🛡️"
            self.particulas = []

        # Mover robot
        self.robot['x'] += self.robot['velocidad'] * math.cos(self.robot['angulo'])
        self.robot['y'] += self.robot['velocidad'] * math.sin(self.robot['angulo'])
        
        # Mantener en pista
        self.robot['x'] = max(self.pista['x_inicio'] + 10, 
                            min(self.pista['x_inicio'] + self.pista['ancho'] - 10, 
                                self.robot['x']))
        self.robot['y'] = max(self.pista['y_inicio'] + 20, 
                            min(self.pista['y_inicio'] + self.pista['alto'] - 20, 
                                self.robot['y']))

        # Registrar trayectoria
        self.robot['trayectoria'].append((self.robot['x'], self.robot['y']))
        if len(self.robot['trayectoria']) > 50:
            self.robot['trayectoria'].pop(0)

        # Detectar adelantamientos
        for oponente in self.oponentes:
            if (abs(self.robot['x'] - oponente['x']) < 25 and 
                self.robot['x'] > oponente['x'] and
                abs(self.robot['y'] - oponente['y']) < 20):
                self.robot['adelantamientos'] += 1
                oponente['x'] -= 100

        # Actualizar feromonas
        tramo = int((self.robot['x'] - self.pista['x_inicio']) / self.pista['ancho'] * 50)
        self.controlador.hormigas.reforzar_trayectoria(tramo, 0.1)

        # Evolucionar cada 10 segundos
        if int(self.tiempo) % 10 == 0 and random.random() < 0.1:
            nuevos_params = self.controlador.ag.evolucionar([{}])
            self.controlador.parametros.update(nuevos_params)

    def animar(self, frame):
        self.ax_main.clear()
        self.ax_main.set_xlim(0, 1200)
        self.ax_main.set_ylim(0, 700)
        self.ax_main.set_aspect('equal')
        self.ax_main.set_facecolor('black')
        self.ax_main.set_title(f'CARRERA DE ROBOTS IA - Tiempo: {self.tiempo:.1f}s', 
                             color='white', fontsize=14, pad=20)
        
        # Actualizar simulación
        self.actualizar_simulacion()
        
        # Dibujar elementos
        self.dibujar_pista()
        self.dibujar_feromonas()
        self.dibujar_particulas()
        self.dibujar_vehiculos()
        self.dibujar_info()

    def iniciar(self):
        print("🏁 Iniciando Simulador de Carreras de Robots...")
        print("🧠 Algoritmos activos: Genético, PSO, Hormigas")
        print("🎮 Visualizando: 8 competidores, feromonas, partículas PSO")
        print("⏹️ Cierra la ventana para terminar")
        
        anim = animation.FuncAnimation(self.fig, self.animar, interval=50, cache_frame_data=False)
        plt.tight_layout()
        plt.show()

# ========== EJECUCIÓN ==========
if __name__ == "__main__":
    # Verificar dependencias
    try:
        simulador = SimuladorCarrerasFuncional()
        simulador.iniciar()
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de tener instaladas las dependencias:")
        print("pip install matplotlib numpy")