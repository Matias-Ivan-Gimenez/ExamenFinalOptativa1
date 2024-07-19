import pygame
import os
import src.spritesheet as spritesheet
import src.settings as settings
import src.entities as entities
import src.ui as ui

# Clase para gestionar la pantalla de victoria
class Win:
    def __init__(self, screen) -> None:
        self.screen = screen  # Pantalla de juego
        self.font = pygame.font.Font(os.path.join('assets', 'Monocraft.ttf'), 32)  # Fuente para el texto

        # Cargar y escalar la imagen del título de victoria
        self.title = pygame.image.load(os.path.join('assets', 'winner_title.png')).convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width() * 5, self.title.get_height() * 5))

        # Renderizar textos adicionales
        self.name = self.font.render('Segundo Examen Parcial', False, (255, 255, 255))
        self.using = self.font.render('Utilizando pygame', False, (255, 255, 255))

        # Configurar fondo transparente
        self.background = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81, 50))

    # Método para actualizar la pantalla
    def update(self):
        self.render()

    # Método para renderizar el contenido en la pantalla
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.name, (self.screen.get_width() / 2 - self.name.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.using, (self.screen.get_width() / 2 - self.using.get_width() / 2, self.screen.get_height() / 2 + 150))
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, self.screen.get_height() / 2 - self.title.get_height() * 2))


# Clase para gestionar la pantalla de derrota
class Lose:
    def __init__(self, screen, reset_level, set_state) -> None:
        self.screen = screen  # Pantalla de juego
        self.reset_level = reset_level  # Función para reiniciar el nivel
        self.set_game_state = set_state  # Función para cambiar el estado del juego
        self.font = pygame.font.Font(os.path.join('assets', 'Monocraft.ttf'), 32)  # Fuente para el texto

        # Cargar y escalar la imagen del título de derrota
        self.title = pygame.image.load(os.path.join('assets', 'lose_title.png')).convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width() * 5, self.title.get_height() * 5))

        # Renderizar texto de ayuda
        self.hint = self.font.render('Presione ENTER para volver a intentar', False, (255, 255, 255))

        # Configurar fondo transparente
        self.background = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81))

    # Método para manejar la entrada del usuario
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.reset_level()
            self.set_game_state('game')

    # Método para actualizar la pantalla
    def update(self):
        self.input()
        self.render()

    # Método para renderizar el contenido en la pantalla
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.hint, (self.screen.get_width() / 2 - self.hint.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, self.screen.get_height() / 2 - self.title.get_height() * 2))


# Clase para gestionar la pantalla de pausa
class Pause:
    def __init__(self, screen) -> None:
        self.screen = screen  # Pantalla de juego
        self.font = pygame.font.Font(os.path.join('assets', 'Monocraft.ttf'), 32)  # Fuente para el texto

        # Cargar y escalar la imagen del título de pausa
        self.title = pygame.image.load(os.path.join('assets', 'pause_title.png')).convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width() * 5, self.title.get_height() * 5))

        # Renderizar texto de ayuda para reanudar el juego
        self.unpause_hint = self.font.render('Presione la tecla ESC para reanudar', False, (255, 255, 255))

        # Configurar fondo transparente
        self.background = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81, 50))

    # Método para actualizar la pantalla
    def update(self):
        self.render()

    # Método para renderizar el contenido en la pantalla
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.unpause_hint, (self.screen.get_width() / 2 - self.unpause_hint.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, self.screen.get_height() / 2 - self.title.get_height() * 2))


# Clase para gestionar el nivel del juego
class Level:
    def __init__(self, screen, swap_level, set_state, curr_level, increase_score_callback) -> None:
        self.layout = settings.Level_data()  # Datos del diseño del nivel
        self.deco_layout = settings.Level_decor()  # Datos de la decoración del nivel
        self.entity_data = entities.Entity_data()  # Datos de las entidades del nivel
        self.increase_score_callback = increase_score_callback  # Callback para aumentar el puntaje

        self.screen = screen  # Pantalla de juego
        self.level_cleared = False  # Indicador de nivel completado
        self.swap_level = swap_level  # Función para cambiar de nivel
        self.curr_level = curr_level  # Nivel actual

        self.entities = []  # Lista de entidades en el nivel
        self.player = entities.Player(screen, set_state)  # Crear el jugador
        self.entities.append(self.player)  # Añadir el jugador a la lista de entidades
        self.scroll_speed = 0  # Velocidad de desplazamiento del mapa
        self.player_vel = self.player.velocity  # Velocidad del jugador

        self.terrain_tiles = spritesheet.TerrainTiles()  # Tiles de terreno
        self.decoratione_tiles = spritesheet.DecorationTiles()  # Tiles de decoración
        self.map = []  # Mapa del nivel
        self.collidables = []  # Tiles con los que se puede colisionar

        self.enter_door = None  # Puerta de entrada
        self.exit_door = None  # Puerta de salida

        self.ui = ui.Healthbar(self.screen)  # Barra de salud del jugador

        self.load()  # Cargar el nivel
        self.setup_level()  # Configurar el nivel
        if self.curr_level == 0:
            self.setup_tutorial()  # Configurar tutorial si es el primer nivel

        self.enter_door.close_sound.play()  # Reproducir sonido de puerta cerrada

    # Método para aumentar el puntaje
    def increase_score(self, points):
        self.increase_score_callback(points)

    # Método para actualizar el nivel
    def update(self):
        self.render()  # Renderizar el nivel
        self.scroll_map()  # Desplazar el mapa
        self.horizontal_collision()  # Comprobar colisiones horizontales
        self.vertical_collision()  # Comprobar colisiones verticales
        self.input()  # Procesar entrada del usuario
        self.ui.update()  # Actualizar la UI

        self.enter_door.update()  # Actualizar la puerta de entrada
        self.exit_door.update()  # Actualizar la puerta de salida

    # Método para renderizar el nivel
    def render(self):
        for tile in self.map:
            if isinstance(tile, entities.Enemy):
                continue
            elif isinstance(tile, entities.Box):
                tile.render()
            tile.surface.set_colorkey((0, 0, 0))
            self.screen.blit(tile.surface, tile.rect)

        if self.curr_level == 0:
            self.show_tutorial()

        self.enter_door.render()
        self.exit_door.render()

        for e in self.entities:
            e.render()

        self.ui.render()

        for e in self.entities:
            e.update()
            if isinstance(e, entities.Enemy):
                if e.rect.colliderect(self.player.hurtbox) and self.player.can_deal_dmg:
                    e.take_damage()
                if e.rect.colliderect(self.player.rect) and self.player.can_take_damage and e.animation_manager.state != 'dead':
                    self.player.take_damage()
                    self.ui.took_damage()
                if e.is_dead():
                    self.entities.remove(e)
                    self.map.remove(e)
                    self.increase_score(10)

    # Método para cargar el nivel desde los datos
    def load(self):
        for row_id, row in enumerate(self.layout.levels[self.curr_level]):
            for tile_id, tile in enumerate(row):
                if tile in self.terrain_tiles.background.keys():
                    position = (tile_id * settings.tile_size, row_id * settings.tile_size)
                    t = spritesheet.Tile(self.terrain_tiles.background[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                elif tile in self.terrain_tiles.walls.keys():
                    position = (tile_id * settings.tile_size, row_id * settings.tile_size)
                    t = spritesheet.Tile(self.terrain_tiles.walls[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                    self.collidables.append(t)

        for row_id, row in enumerate(self.deco_layout.levels[self.curr_level]):
            for tile_id, tile in enumerate(row):
                if tile in self.decoratione_tiles.decorations.keys():
                    position = (tile_id * settings.tile_size, row_id * settings.tile_size)
                    t = spritesheet.Tile(self.decoratione_tiles.decorations[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                if tile in self.decoratione_tiles.platforms.keys():
                    position = (tile_id * settings.tile_size, row_id * settings.tile_size)
                    t = spritesheet.Tile(self.decoratione_tiles.platforms[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                    self.collidables.append(t)

    # Método para configurar el tutorial
    def setup_tutorial(self):
        self.title = pygame.image.load(os.path.join('assets', 'KingOink_title.png')).convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width() * 4, self.title.get_height() * 4))

        self.a_key = spritesheet.Tile(self.decoratione_tiles.hints['L'], (600, 400), self.decoratione_tiles.hints['L'].get_size())
        self.d_key = spritesheet.Tile(self.decoratione_tiles.hints['R'], (680, 400), self.decoratione_tiles.hints['R'].get_size())
        self.w_key = spritesheet.Tile(self.decoratione_tiles.hints['J'], (640, 350), self.decoratione_tiles.hints['J'].get_size())
        self.space_key = spritesheet.Tile(self.decoratione_tiles.hints['A'], (1500, 400), self.decoratione_tiles.hints['A'].get_size())
        self.enter_key = spritesheet.Tile(self.decoratione_tiles.hints['E'], (2000, 400), self.decoratione_tiles.hints['E'].get_size())

        self.map.append(self.a_key)
        self.map.append(self.d_key)
        self.map.append(self.w_key)
        self.map.append(self.space_key)
        self.map.append(self.enter_key)

    # Método para configurar el nivel
    def setup_level(self):
        for item in self.entity_data.levels[self.curr_level]:
            item.screen = self.screen
            self.map.append(item)

            if isinstance(item, entities.Enemy):
                self.entities.append(item)
            elif isinstance(item, entities.Box):
                self.collidables.append(item)
            elif isinstance(item, entities.Door):
                if item.state == 'exit':
                    self.exit_door = item
                    item.change_scene = self.swap_level
                else:
                    self.enter_door = item

    # Método para manejar la entrada del usuario
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.player.direction.x = -1
            self.player.flip_sprite = True
            self.player.animation_manager.set_state('run')
        elif keys[pygame.K_d]:
            self.player.direction.x = 1
            self.player.flip_sprite = False
            self.player.animation_manager.set_state('run')
        else:
            self.player.direction.x = 0
            self.player.animation_manager.set_state('idle')

        if keys[pygame.K_w]:
            if not self.player.is_in_air:
                self.player.jump()

        if keys[pygame.K_SPACE]:
            self.player.attack()

        if keys[pygame.K_RETURN] and self.player.rect.colliderect(self.exit_door.rect):
            if not self.level_cleared:
                self.exit_door.open_sound.play()
                self.player.animation_manager.set_state('enter_door')
                self.exit_door.animation_manager.set_state('open')
                self.level_cleared = not self.level_cleared

    # Método para manejar colisiones verticales
    def vertical_collision(self):
        for entity in self.entities:
            entity.gravity()
            for tile in self.collidables:
                if tile.rect.colliderect(entity.rect):
                    if entity.direction.y > 0:
                        entity.rect.bottom = tile.rect.top
                        entity.is_in_air = False
                    elif entity.direction.y < 0:
                        entity.rect.top = tile.rect.bottom
                    entity.direction.y = 0

    # Método para manejar colisiones horizontales
    def horizontal_collision(self):
        for entity in self.entities:
            for tile in self.collidables:
                if tile.rect.colliderect(entity.rect):
                    if entity.direction.x > 0:
                        entity.rect.right = tile.rect.left
                    elif entity.direction.x < 0:
                        entity.rect.left = tile.rect.right
                    entity.direction.x = 0

    # Método para mover el mapa
    def move_map(self):
        for tile in self.map:
            tile.rect.x += self.scroll_speed
            if isinstance(tile, entities.Enemy):
                tile.walk_area[0] += self.scroll_speed
                tile.walk_area[1] += self.scroll_speed

    # Método para desplazar el mapa
    def scroll_map(self):
        if self.player.rect.x > self.screen.get_width()/2 + 100 and self.player.direction.x > 0:
            self.scroll_speed = -self.player_vel
            self.player.velocity = 0
            self.move_map()
        elif self.player.rect.x < self.screen.get_width()/2 - 200 and self.player.direction.x < 0:
            self.player.velocity = 0
            self.scroll_speed = self.player_vel
            self.move_map()
        else:
            self.scroll_speed = 0
            self.player.velocity = self.player_vel

    # Método para mostrar el tutorial
    def show_tutorial(self):
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width()/2, 200))
    def update(self):
        self.render()
        self.scroll_map()
        self.horizontal_collision()
        self.vertical_collision()
        self.input()
        self.ui.update()

        self.enter_door.update()
        self.exit_door.update()

        # worse hitreg I've written lol
        for e in self.entities:
            e.update()
            if isinstance(e, entities.Enemy):
                if e.rect.colliderect(self.player.hurtbox) and self.player.can_deal_dmg:
                    e.take_damage()
                if e.rect.colliderect(self.player.rect) and self.player.can_take_damage and e.animation_manager.state != 'dead':
                    self.player.take_damage()
                    self.ui.took_damage()
                if e.is_dead():
                    self.entities.remove(e)
                    self.map.remove(e)
                    
              
                    self.increase_score(10)
        
            
    def render(self):
        # render tiles
        for tile in self.map:
            if isinstance(tile, entities.Enemy):
                continue
            elif isinstance(tile, entities.Box):
                tile.render()
            tile.surface.set_colorkey((0, 0, 0))
            self.screen.blit(tile.surface, tile.rect)

        if self.curr_level == 0:
            self.show_tutorial()

        self.enter_door.render()
        self.exit_door.render()

        for e in self.entities:
            e.render()

        self.ui.render()
