import pygame
import src.scenes as scenes
import src.settings as settings
import sys
import pickle

class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.state = 'menu'  # Estado inicial del juego
        self.current_level = 0  # Nivel actual del juego
        self.score = 0  # Inicializar el puntaje del jugador

        # Inicializar atributos para el menú
        self.font_large = pygame.font.SysFont("Arial", 60)
        self.font_small = pygame.font.SysFont("Arial", 36)
        self.button_color = (228, 134, 7)
        self.text_color = (255, 255, 255)
        self.gradient_start = (123, 31, 162)  # Morado
        self.gradient_mid = (255, 87, 34)  # Naranja
        self.gradient_end = (106, 16, 98 )  # Crema

        # Crear las escenas
        self.level = scenes.Level(
            screen, self.next_level, self.set_state, self.current_level, self.increase_score)
        self.lose_scene = scenes.Lose(screen, self.reset_level, self.set_state)
        self.pause_scene = scenes.Pause(screen)
        self.win_scene = scenes.Win(screen)

        # Inicializar botones del menú
        self.start_button = None
        self.exit_button = None

        # Cargar puntuaciones
        self.scores = self.load_scores()
      
        # Cargar la imagen del título y redimensionarla
        self.title_image = pygame.image.load("assets/KingOink_title.png")
        self.title_image = pygame.transform.scale(self.title_image, (self.title_image.get_width() * 5, self.title_image.get_height() * 5))

    def set_state(self, state):
        """Establece el estado actual del juego."""
        self.state = state

    def draw_gradient(self):
        """Dibuja un gradiente de fondo."""
        for y in range(self.screen.get_height()):
            color = (
                self.gradient_start[0] + (self.gradient_end[0] - self.gradient_start[0]) * y // self.screen.get_height(),
                self.gradient_start[1] + (self.gradient_end[1] - self.gradient_start[1]) * y // self.screen.get_height(),
                self.gradient_start[2] + (self.gradient_end[2] - self.gradient_start[2]) * y // self.screen.get_height()
            )
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))

    def draw_button(self, text, font, color, x, y, width, height):
        """Dibuja un botón."""
        button_surface = pygame.Surface((width, height))
        button_surface.fill(color)
        text_surface = font.render(text, True, self.text_color)
        self.screen.blit(button_surface, (x, y))
        self.screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
        return pygame.Rect(x, y, width, height)

    def draw_menu(self):
        """Dibuja la pantalla del menú inicial."""
        self.draw_gradient()
        
        # Dibuja la imagen del título redimensionada
        title_image_rect = self.title_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(self.title_image, title_image_rect)
        
        self.start_button = self.draw_button("Iniciar Juego", self.font_small, self.button_color, self.screen.get_width() // 2 - 100, self.screen.get_height() // 2, 200, 50)
        self.exit_button = self.draw_button("Salir", self.font_small, self.button_color, self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 60, 200, 50)
        
        self.screen.blit(self.font_small.render("Presiona ENTER para iniciar el juego", True, self.text_color), (self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 + 130))
        self.draw_scores()

    def draw_scores(self):
        """Dibuja las puntuaciones en la pantalla del menú."""
        score_text = self.font_small.render("", True, self.text_color)
        self.screen.blit(score_text, (10, 10))
        for i, score in enumerate(self.scores):
            score_text = self.font_small.render(f"{i+1}. {score}", True, self.text_color)
            self.screen.blit(score_text, (10, 40 + i * 30))

    def load_scores(self):
        """Carga las puntuaciones desde un archivo."""
        try:
            with open("scores.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def save_scores(self):
        """Guarda las puntuaciones en un archivo."""
        with open("scores.pkl", "wb") as file:
            pickle.dump(self.scores, file)

    def handle_events(self):
        """Maneja los eventos del juego."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.state == 'win':
                        pygame.quit()
                        sys.exit()
                    else:
                        self.toggle_pause()

                if e.key == pygame.K_RETURN:
                    if self.state == 'menu':
                        self.start_game()
                    elif self.state in ('lose', 'win'):
                        self.state = 'menu'
                        self.reset_game()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    if self.start_button and self.start_button.collidepoint(e.pos):
                        self.start_game()
                    if self.exit_button and self.exit_button.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()

    def start_game(self):
        """Inicia el juego y cambia el estado."""
        self.state = 'game'

    def reset_game(self):
        """Reinicia el juego."""
        self.current_level = 0
        self.score = 0
        self.scores = self.load_scores()
        self.reset_level()

    def reset_level(self):
        """Reinicia el nivel actual del juego."""
        self.level = scenes.Level(
            self.screen, self.next_level, self.set_state, self.current_level, self.increase_score)

    def next_level(self):
        """Avanza al siguiente nivel del juego."""
        if self.current_level + 1 < 5:  # Si hay más niveles por jugar
            self.current_level += 1  # Incrementar el nivel actual
            self.reset_level()  # Reiniciar el nivel
        else:
            self.set_state('win')  # Si no hay más niveles, cambiar el estado a 'ganar'

    def increase_score(self, points):
        """Aumenta el puntaje del jugador."""
        self.score += points  # Sumar los puntos al puntaje actual

    def toggle_pause(self):
        """Pausa o reanuda el juego dependiendo del estado actual."""
        if self.state == 'game':
            self.state = 'pause'
        else:
            self.state = 'game'

    def update(self):
        """Actualiza el estado del juego."""
        if self.state == 'game':
            self.render()
            self.level.update()  # Actualizar la lógica del nivel
        elif self.state == 'pause':
            self.pause_scene.update()  # Actualizar la pantalla de pausa si es necesario
        elif self.state == 'lose':
            self.lose_scene.update()  # Actualizar la pantalla de perder si es necesario
        elif self.state == 'win':
            self.win_scene.update()  # Actualizar la pantalla de ganar si es necesario
        elif self.state == 'menu':
            self.draw_menu()  # Dibujar la pantalla del menú

    def render(self):
        """Renderiza la pantalla del juego."""
        self.screen.fill((63, 56, 81))
        self.draw_score()

    def draw_score(self):
        """Dibuja el puntaje del jugador en la pantalla."""
        font = pygame.font.SysFont(None, 36)
        score_surface = font.render(f'Puntaje: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption('King Oink')

    screen_height, screen_width = (1280, 720)
    screen = pygame.display.set_mode((screen_height, screen_width))

    clock = pygame.time.Clock()
    game = Game(screen)

    pygame.mixer.music.load("./assets/sounds/music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    while True:
        clock.tick(60)
        game.handle_events()

        if game.state == 'menu':
            game.draw_menu()
        else:
            game.update()
        
        pygame.display.update()

if __name__ == '__main__':
    main()
