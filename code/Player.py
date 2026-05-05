import pygame
from pathlib import Path

from code.consts.Window import HEIGHT, WIDTH

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PLAYER_IMAGE = ASSETS_DIR / "player.png"
PLAYER_STOPPED_IMAGE = ASSETS_DIR / "player_stoped.png"

class Player:
    def __init__(self):
        self.width = 64
        self.height = 64

        self.velocity_x = 0
        self.velocity_y = 0

        self.speed = 4
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False

        self.facing_right = True

        self.animations = self.load_animations()
        self.current_animation = "idle"
        self.previous_animation = None
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.rect = pygame.Rect(100, HEIGHT - 60 - self.visible_height, self.visible_width, self.visible_height)

        self.jump_sound = pygame.mixer.Sound(str(ASSETS_DIR / "jump.mp3"))
        self.jump_sound.set_volume(0.5)

    def load_animations(self):
        image = pygame.image.load(str(PLAYER_IMAGE)).convert_alpha()

        frame_height = image.get_height()
        frame_width = frame_height
        frame_count = image.get_width() // frame_width
        if frame_count <= 0:
            raise ValueError(
                f"Invalid player sprite sheet width {image.get_width()} for frame width {frame_width}"
            )

        min_x = frame_width
        max_x = 0
        min_y = frame_height
        max_y = 0
        for y in range(frame_height):
            for x in range(frame_width):
                if image.get_at((x, y)).a != 0:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

        visible_width_orig = max_x - min_x + 1
        visible_height_orig = max_y - min_y + 1
        scale_factor = self.width / frame_width
        self.visible_width = int(visible_width_orig * scale_factor)
        self.visible_height = int(visible_height_orig * scale_factor)
        self.offset_x = int(min_x * scale_factor)
        self.offset_y = int(min_y * scale_factor)

        frames = []
        for i in range(frame_count):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = image.subsurface(frame_rect)
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)

        idle_frames = self.load_stopped_animation()

        return {
            "idle": idle_frames,
            "run": frames,
            "jump": frames
        }
    
    def load_stopped_animation(self):
        image = pygame.image.load(str(PLAYER_STOPPED_IMAGE)).convert_alpha()

        frame_height = image.get_height()
        frame_width = frame_height
        frame_count = image.get_width() // frame_width
        if frame_count <= 0:
            raise ValueError(
                f"Invalid stopped sprite sheet width {image.get_width()} for frame width {frame_width}"
            )

        frames = []
        for i in range(frame_count):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = image.subsurface(frame_rect)
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)

        return frames

    def calculate_draw_offset(self, image, frame_height):
        frame = image.subsurface((0, 0, frame_height, frame_height))
        bottom = -1
        for y in range(frame_height):
            for x in range(frame_height):
                if frame.get_at((x, y)).a != 0:
                    bottom = max(bottom, y)

        if bottom < 0:
            return 0

        visible_bottom_scaled = (bottom + 1) * self.height / frame_height
        return int(round(self.height - visible_bottom_scaled))

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.velocity_x = 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            
            self.jump_sound.play()

            self.velocity_y = self.jump_power
            self.on_ground = False

    def update(self, dt, ground_rect):
        self.rect.x += self.velocity_x

        # Clamp x position to screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Clamp y position to screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        if self.rect.bottom >= ground_rect.top:
            self.rect.bottom = ground_rect.top
            self.velocity_y = 0
            self.on_ground = True

        if not self.on_ground:
            self.current_animation = "jump"
        elif self.velocity_x != 0:
            self.current_animation = "run"
        else:
            self.current_animation = "idle"

        if self.current_animation != self.previous_animation:
            self.current_frame = 0
            self.animation_timer = 0
            self.previous_animation = self.current_animation

        frames = self.animations[self.current_animation]

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(frames)

    def draw(self, screen):
        frame = self.animations[self.current_animation][self.current_frame]

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, (self.rect.x - self.offset_x, self.rect.y - self.offset_y))
