import pygame
import sys
import json
            
def PlayWeekStory(screen, current_week):
    
    with open('event/event.json', 'r', encoding='utf-8') as f:
            story_dict = json.load(f)
            
    font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 48)
    clock = pygame.time.Clock()
    type_sound = pygame.mixer.Sound("resource/music/sound_effect/typing.mp3")
    background = pygame.image.load(f"resource/image/backgrounds/week_{current_week}.png")
    background = pygame.transform.scale(background, screen.get_size())
    dialog_rect = pygame.Rect(100, 180, 1000, 400)
    background.set_alpha(65)

    char_interval = 100  # 字母出現間隔（毫秒）
    line_spacing = 10
    line_height = font.get_linesize()

    lines = story_dict.get(str(current_week), [])

    current_line = 0
    current_char = 0
    displayed_lines = []
    last_char_time = pygame.time.get_ticks()
    all_finished = False

    running = True
    type_sound.play()
    
    while running:
        now = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if all_finished:
                    running = False  # 點擊結束故事
        
        if background :
            screen.fill((255, 255, 255))
            screen.blit(background,(0, 0))
        else:
            screen.fill((0, 0, 0))  # 沒背景時用黑色



        if not all_finished:
            if now - last_char_time > char_interval:
                last_char_time = now
                current_char += 1
                if current_char > len(lines[current_line]):
                    displayed_lines.append(lines[current_line])
                    current_line += 1
                    current_char = 0
                    if current_line >= len(lines):
                        all_finished = True

        y = dialog_rect.top + 30
        for line in displayed_lines:
            text_surface = font.render(line, True, (50, 50, 50))
            screen.blit(text_surface, (dialog_rect.left + 20, y))
            y += line_height + line_spacing

        if not all_finished and current_line < len(lines):
            partial_text = lines[current_line][:current_char]
            text_surface = font.render(partial_text, True, (50, 50, 50))
            screen.blit(text_surface, (dialog_rect.left + 20, y))

        if all_finished:
            tip = font.render("（點擊以結束）", True, (150, 150, 150))
            screen.blit(tip, (screen.get_width() // 2 - tip.get_width() // 2, dialog_rect.bottom + 20))
            type_sound.stop()

        pygame.display.flip()
        clock.tick(60)

