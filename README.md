. Introducción
1.1 Propósito del Programa
El programa es un videojuego llamado "King Oink" desarrollado en Python utilizando la biblioteca Pygame. El objetivo del juego es avanzar a través de niveles, aumentando el puntaje y enfrentándose a desafíos en cada etapa.
1.2 Requisitos
•	Python 3.x
•	Biblioteca Pygame
2. Estructura del Código
2.1 Importación de Bibliotecas
import pygame
import src.scenes as scenes
import src.settings as settings
import sys
import pickle
Estas importaciones permiten utilizar funcionalidades de Pygame para la creación del juego, manejar la configuración del juego y gestionar el almacenamiento de datos.
2.2 Inicialización y Configuración
pygame.init()
ANCHO, ALTO = 1280, 720
COLOR_FONDO = (63, 56, 81)
GRADIENTE_INICIAL = (123, 31, 162)  # Morado
GRADIENTE_FINAL = (106, 16, 98)     # Crema
Estas líneas inicializan Pygame y definen constantes para el tamaño de la pantalla y los colores utilizados en el juego.
2.3 Configuración de la Pantalla y Recursos
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("King Oink")
Se configura la pantalla del juego y se establece el título de la ventana.
2.4 Fuentes y Sonidos
fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_pequena = pygame.font.SysFont("Arial", 36)
sonido_fondo = pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
Se cargan las fuentes y la música de fondo para el juego.
2.5 Variables de Estado del Juego
estado = 'menu'
nivel_actual = 0
puntaje = 0
Se definen las variables para el estado del juego, el nivel actual y el puntaje del jugador.
2.6 Cargar Imágenes
imagen_titulo = pygame.image.load("assets/KingOink_title.png")
imagen_titulo = pygame.transform.scale(imagen_titulo, (800, 600))
Se carga la imagen para el título del juego y se ajusta su tamaño.
3. Funciones
3.1 Funciones para Guardar y Cargar Puntajes
def cargar_puntajes():
    try:
        with open("scores.pkl", "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return []

def guardar_puntajes(puntajes):
    with open("scores.pkl", "wb") as archivo:
        pickle.dump(puntajes, archivo)
Estas funciones permiten guardar y cargar los puntajes del juego utilizando archivos pickle.
4. Clases
4.1 Clase Juego
class Game:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.estado = 'menu'
        self.nivel_actual = 0
        self.puntaje = 0
        self.fuente_grande = pygame.font.SysFont("Arial", 60)
        self.fuente_pequena = pygame.font.SysFont("Arial", 36)
        self.color_boton = (228, 134, 7)
        self.color_texto = (255, 255, 255)
        self.gradiente_inicio = (123, 31, 162)
        self.gradiente_final = (106, 16, 98)
        self.titulo_imagen = pygame.image.load("assets/KingOink_title.png")
        self.titulo_imagen = pygame.transform.scale(self.titulo_imagen, (800, 600))
La clase Game gestiona los estados del juego, las puntuaciones, y la inicialización de elementos del menú.
4.2 Clase Escenas
class Level:
    def __init__(self, pantalla, avanzar_nivel, cambiar_estado, nivel_actual, aumentar_puntaje):
        # Configuración de la escena del nivel
Las clases dentro del módulo scenes gestionan las diferentes escenas del juego, como el nivel, la pantalla de pérdida, y la pantalla de victoria.
5. Funciones Auxiliares
5.1 Crear Botones
def dibujar_boton(texto, fuente, color, x, y, ancho, alto):
    superficie_boton = pygame.Surface((ancho, alto))
    superficie_boton.fill(color)
    texto_boton = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(superficie_boton, (x, y))
    pantalla.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))
    return pygame.Rect(x, y, ancho, alto)
Esta función dibuja un botón en la pantalla con texto centrado.
5.2 Dibujar Gradiente
def dibujar_gradiente():
    for y in range(self.pantalla.get_height()):
        color = (
            self.gradiente_inicio[0] + (self.gradiente_final[0] - self.gradiente_inicio[0]) * y // self.pantalla.get_height(),
            self.gradiente_inicio[1] + (self.gradiente_final[1] - self.gradiente_inicio[1]) * y // self.pantalla.get_height(),
            self.gradiente_inicio[2] + (self.gradiente_final[2] - self.gradiente_inicio[2]) * y // self.pantalla.get_height()
        )
        pygame.draw.line(self.pantalla, color, (0, y), (self.pantalla.get_width(), y))
Dibuja un gradiente vertical en la pantalla.
6. Funciones de Dibujo de Pantallas
6.1 Pantalla de Inicio
def dibujar_menu(self):
    self.dibujar_gradiente()
    self.pantalla.blit(self.titulo_imagen, (self.pantalla.get_width() // 2 - self.titulo_imagen.get_width() // 2, self.pantalla.get_height() // 4 - self.titulo_imagen.get_height() // 2))
    boton_inicio = self.dibujar_boton("Iniciar Juego", self.fuente_pequena, self.color_boton, self.pantalla.get_width() // 2 - 100, self.pantalla.get_height() // 2, 200, 50)
    boton_salir = self.dibujar_boton("Salir", self.fuente_pequena, self.color_boton, self.pantalla.get_width() // 2 - 100, self.pantalla.get_height() // 2 + 60, 200, 50)
    self.pantalla.blit(self.fuente_pequena.render("Presiona ENTER para iniciar el juego", True, self.color_texto), (self.pantalla.get_width() // 2 - 150, self.pantalla.get_height() // 2 + 130))
Dibuja la pantalla de inicio del juego con el título y los botones.
7. Bucle Principal del Juego
El bucle principal gestiona el estado del juego, actualiza los elementos y maneja los eventos del usuario.
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if estado == 'menu' and evento.key == pygame.K_RETURN:
                estado = 'game'
            elif estado in ('lose', 'win') and evento.key == pygame.K_RETURN:
                estado = 'menu'
                reset_game()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_inicio.collidepoint(evento.pos):
                estado = 'game'
            if boton_salir.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
    
    if estado == 'menu':
        dibujar_menu()
    else:
        actualizar()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)
8. Conclusión
El código del juego "King Oink" está estructurado para manejar diferentes estados del juego, como el menú, los niveles y las pantallas de ganar o perder. La interacción del usuario se gestiona a través de eventos de teclado y ratón, proporcionando una experiencia de juego dinámica y atractiva.


