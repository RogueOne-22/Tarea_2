import numpy as np
import random
from math import sqrt
from typing import Dict, List, Set
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class UsuarioHormiga:
    def __init__(self, preferencias: Dict[str, float], nombre: str = "Usuario"):
        self.playlist = []
        self.preferencias = preferencias
        self.canciones_visitadas = set()
        self.nombre = nombre
    
    def evaluar_transicion(self, cancion_actual: str, siguiente_cancion: str, feromonas: Dict, canciones: Dict) -> float:
        feromona = feromonas[cancion_actual][siguiente_cancion]
        similitud = self.calcular_similitud(cancion_actual, siguiente_cancion, canciones)
        afinidad = self.calcular_afinidad(siguiente_cancion, canciones)
        
        return feromona * similitud * afinidad
    
    def calcular_similitud(self, cancion1: str, cancion2: str, canciones: Dict) -> float:
        atributos1 = canciones[cancion1]
        atributos2 = canciones[cancion2]
        
        atributos_comunes = set(atributos1.keys()) & set(atributos2.keys())
        
        if not atributos_comunes:
            return 0.0
        
        producto_punto = sum(atributos1[attr] * atributos2[attr] for attr in atributos_comunes)
        norma1 = sqrt(sum(val ** 2 for val in atributos1.values()))
        norma2 = sqrt(sum(val ** 2 for val in atributos2.values()))
        
        if norma1 == 0 or norma2 == 0:
            return 0.0
            
        return producto_punto / (norma1 * norma2)
    
    def calcular_afinidad(self, cancion: str, canciones: Dict) -> float:
        atributos_cancion = canciones[cancion]
        afinidad_total = 0.0
        atributos_comunes = 0
        
        for atributo, valor_usuario in self.preferencias.items():
            if atributo in atributos_cancion:
                valor_cancion = atributos_cancion[atributo]
                afinidad_total += 1.0 - abs(valor_usuario - valor_cancion)
                atributos_comunes += 1
        
        return afinidad_total / atributos_comunes if atributos_comunes > 0 else 0.0

class SistemaRecomendacionACO:
    def __init__(self, canciones: Dict, alpha: float = 1.0, beta: float = 2.0, 
                 rho: float = 0.1, Q: float = 100):
        self.canciones = canciones
        self.feromonas = self.inicializar_feromonas()
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.historial_calidad = []
        self.historial_afinidad = []
        self.historial_coherencia = []
        self.historial_variedad = []
        
    def inicializar_feromonas(self) -> Dict:
        nombres_canciones = list(self.canciones.keys())
        feromonas = {}
        
        for cancion1 in nombres_canciones:
            feromonas[cancion1] = {}
            for cancion2 in nombres_canciones:
                if cancion1 != cancion2:
                    feromonas[cancion1][cancion2] = 1.0
        
        return feromonas
    
    def generar_playlist(self, usuario: UsuarioHormiga, longitud_playlist: int = 10, 
                        iteraciones: int = 50) -> List[str]:
        mejores_playlists = []
        
        print("🎵 Iniciando algoritmo ACO...")
        for iteracion in range(iteraciones):
            usuario.canciones_visitadas = set()
            usuario.playlist = []
            
            playlist = self.construir_playlist(usuario, longitud_playlist)
            calidad, afinidad, coherencia, variedad = self.evaluar_playlist_detallado(playlist, usuario)
            
            mejores_playlists.append((playlist, calidad))
            self.historial_calidad.append(calidad)
            self.historial_afinidad.append(afinidad)
            self.historial_coherencia.append(coherencia)
            self.historial_variedad.append(variedad)
            
            # Mostrar progreso cada 10 iteraciones
            if iteracion % 10 == 0:
                print(f"   Iteración {iteracion}: Calidad = {calidad:.3f}")
            
            self.actualizar_feromonas(playlist, calidad)
        
        mejor_playlist, mejor_calidad = max(mejores_playlists, key=lambda x: x[1])
        
        # Mostrar dashboard final
        self.mostrar_dashboard_final(usuario, mejor_playlist, mejor_calidad)
        
        return mejor_playlist
    
    def construir_playlist(self, usuario: UsuarioHormiga, longitud: int) -> List[str]:
        playlist = []
        todas_canciones = set(self.canciones.keys())
        
        canciones_iniciales = list(todas_canciones)
        afinidades = [usuario.calcular_afinidad(cancion, self.canciones) for cancion in canciones_iniciales]
        cancion_actual = random.choices(canciones_iniciales, weights=afinidades)[0]
        
        playlist.append(cancion_actual)
        usuario.canciones_visitadas.add(cancion_actual)
        
        while len(playlist) < longitud and len(usuario.canciones_visitadas) < len(todas_canciones):
            siguiente_cancion = self.elegir_siguiente_cancion(usuario, cancion_actual, todas_canciones)
            if siguiente_cancion:
                playlist.append(siguiente_cancion)
                usuario.canciones_visitadas.add(siguiente_cancion)
                cancion_actual = siguiente_cancion
            else:
                no_visitadas = todas_canciones - usuario.canciones_visitadas
                if no_visitadas:
                    cancion_actual = random.choice(list(no_visitadas))
                    playlist.append(cancion_actual)
                    usuario.canciones_visitadas.add(cancion_actual)
                else:
                    break
        
        return playlist
    
    def elegir_siguiente_cancion(self, usuario: UsuarioHormiga, cancion_actual: str, 
                               todas_canciones: Set[str]) -> str:
        canciones_posibles = todas_canciones - usuario.canciones_visitadas
        
        if not canciones_posibles:
            return None
        
        probabilidades = []
        for cancion in canciones_posibles:
            atractivo = self.calcular_atractivo(usuario, cancion_actual, cancion)
            probabilidades.append(atractivo)
        
        total = sum(probabilidades)
        if total == 0:
            return random.choice(list(canciones_posibles))
        
        probabilidades = [p / total for p in probabilidades]
        return random.choices(list(canciones_posibles), weights=probabilidades)[0]
    
    def calcular_atractivo(self, usuario: UsuarioHormiga, cancion_actual: str, siguiente_cancion: str) -> float:
        feromona = self.feromonas[cancion_actual][siguiente_cancion]
        heuristica = usuario.evaluar_transicion(cancion_actual, siguiente_cancion, self.feromonas, self.canciones)
        
        return (feromona ** self.alpha) * (heuristica ** self.beta)
    
    def evaluar_playlist_detallado(self, playlist: List[str], usuario: UsuarioHormiga) -> tuple:
        if len(playlist) < 2:
            return 0.0, 0.0, 0.0, 0.0
        
        # Coherencia secuencial
        coherencia = 0.0
        for i in range(len(playlist) - 1):
            similitud = usuario.calcular_similitud(playlist[i], playlist[i + 1], self.canciones)
            coherencia += similitud
        coherencia /= (len(playlist) - 1)
        
        # Afinidad promedio
        afinidad_total = 0.0
        for cancion in playlist:
            afinidad_total += usuario.calcular_afinidad(cancion, self.canciones)
        afinidad_promedio = afinidad_total / len(playlist)
        
        # Variedad
        variedad = len(set(playlist)) / len(playlist)
        
        # Calidad combinada
        calidad = 0.5 * afinidad_promedio + 0.3 * coherencia + 0.2 * variedad
        
        return calidad, afinidad_promedio, coherencia, variedad
    
    def actualizar_feromonas(self, playlist: List[str], calidad: float):
        for cancion1 in self.feromonas:
            for cancion2 in self.feromonas[cancion1]:
                self.feromonas[cancion1][cancion2] *= (1 - self.rho)
        
        for i in range(len(playlist) - 1):
            cancion_actual = playlist[i]
            siguiente_cancion = playlist[i + 1]
            deposito = self.Q * calidad
            self.feromonas[cancion_actual][siguiente_cancion] += deposito
    
    def mostrar_dashboard_final(self, usuario: UsuarioHormiga, playlist: List[str], calidad: float):
        """Muestra un dashboard simple con matplotlib"""
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 2, figure=fig)
        
        # 1. Evolución de métricas
        ax1 = fig.add_subplot(gs[0, 0])
        iteraciones = range(len(self.historial_calidad))
        ax1.plot(iteraciones, self.historial_calidad, 'b-', label='Calidad Total', linewidth=2)
        ax1.plot(iteraciones, self.historial_afinidad, 'g-', label='Afinidad', linewidth=2)
        ax1.plot(iteraciones, self.historial_coherencia, 'r-', label='Coherencia', linewidth=2)
        ax1.set_xlabel('Iteración')
        ax1.set_ylabel('Valor')
        ax1.set_title('Evolución del Algoritmo ACO')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Playlist y afinidades
        ax2 = fig.add_subplot(gs[0, 1])
        canciones_short = [c[:15] + '...' if len(c) > 15 else c for c in playlist]
        posiciones = range(len(playlist))
        afinidades = [usuario.calcular_afinidad(c, self.canciones) for c in playlist]
        
        bars = ax2.bar(posiciones, afinidades, color='skyblue', alpha=0.7)
        ax2.set_xlabel('Posición en Playlist')
        ax2.set_ylabel('Afinidad')
        ax2.set_title('Afinidad por Canción')
        ax2.set_xticks(posiciones)
        ax2.set_xticklabels(canciones_short, rotation=45, ha='right')
        
        # Añadir valores en las barras
        for bar, afin in zip(bars, afinidades):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{afin:.2f}', ha='center', va='bottom')
        
        # 3. Métricas finales
        ax3 = fig.add_subplot(gs[1, 0])
        metricas = ['Calidad', 'Afinidad', 'Coherencia', 'Variedad']
        valores = [calidad, self.historial_afinidad[-1], self.historial_coherencia[-1], self.historial_variedad[-1]]
        bars_metricas = ax3.bar(metricas, valores, color=['blue', 'green', 'red', 'orange'])
        ax3.set_ylabel('Valor')
        ax3.set_title('Métricas Finales')
        ax3.set_ylim(0, 1)
        
        for bar, valor in zip(bars_metricas, valores):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{valor:.3f}', ha='center', va='bottom')
        
        # 4. Texto informativo
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        info_text = f"""RESULTADOS FINALES - {usuario.nombre}

🎯 Playlist Recomendada:
"""
        for i, cancion in enumerate(playlist, 1):
            afin = usuario.calcular_afinidad(cancion, self.canciones)
            info_text += f" {i:2d}. {cancion} (afinidad: {afin:.3f})\n"
        
        info_text += f"""
📊 Métricas Detalladas:
 • Calidad Total: {calidad:.3f}
 • Afinidad Promedio: {self.historial_afinidad[-1]:.3f}
 • Coherencia: {self.historial_coherencia[-1]:.3f}
 • Variedad: {self.historial_variedad[-1]:.3f}
 
🎵 Total canciones: {len(playlist)}
"""
        ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, fontfamily='monospace',
                verticalalignment='top', fontsize=10)
        
        plt.tight_layout()
        plt.show()

def crear_dataset_musical() -> Dict:
    return {
        'Bohemian Rhapsody': {'rock': 0.9, 'energia': 0.8, 'danceability': 0.4, 'acustica': 0.7},
        'Blinding Lights': {'pop': 0.8, 'energia': 0.7, 'danceability': 0.9, 'acustica': 0.3},
        'Take Five': {'jazz': 0.9, 'energia': 0.3, 'danceability': 0.6, 'acustica': 0.8},
        'Bad Guy': {'pop': 0.7, 'energia': 0.6, 'danceability': 0.8, 'acustica': 0.4},
        'Sweet Child O Mine': {'rock': 0.8, 'energia': 0.9, 'danceability': 0.5, 'acustica': 0.6},
        'Uptown Funk': {'funk': 0.8, 'pop': 0.7, 'energia': 0.8, 'danceability': 0.9, 'acustica': 0.2},
    }

def main():
    print("🎵 SISTEMA DE RECOMENDACIÓN MUSICAL CON ACO")
    print("=" * 50)
    
    canciones = crear_dataset_musical()
    
    usuario = UsuarioHormiga(
        preferencias={'rock': 0.7, 'energia': 0.8, 'danceability': 0.6, 'acustica': 0.5},
        nombre="Rockero Energético"
    )
    
    sistema = SistemaRecomendacionACO(canciones=canciones)
    
    playlist_final = sistema.generar_playlist(
        usuario=usuario,
        longitud_playlist=5,
        iteraciones=30
    )

if __name__ == "__main__":
    main()