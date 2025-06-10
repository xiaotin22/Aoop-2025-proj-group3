import pygame
import json
import sys

def play_week_story(screen, story_dict, current_week):
    font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
    clock = pygame.time.Clock()

    dialog_rect = pygame.Rect(100, 180, 1000, 400)
    dialog_bg_color = (20, 20, 30)
    dialog_border_color = (90, 90, 120)

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
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if all_finished:
                    running = False  # 點擊結束故事

        screen.fill((0, 0, 0))

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
            text_surface = font.render(line, True, (220, 220, 220))
            screen.blit(text_surface, (dialog_rect.left + 20, y))
            y += line_height + line_spacing

        if not all_finished and current_line < len(lines):
            partial_text = lines[current_line][:current_char]
            text_surface = font.render(partial_text, True, (220, 220, 220))
            screen.blit(text_surface, (dialog_rect.left + 20, y))

        if all_finished:
            tip = font.render("（點擊以結束）", True, (150, 150, 150))
            screen.blit(tip, (screen.get_width() // 2 - tip.get_width() // 2, dialog_rect.bottom + 20))

        pygame.display.flip()
        clock.tick(60)

    return current_week + 1


# ✅ 如果你想單獨測試這個功能，可以加上這段
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("測試週故事畫面")

    # 測試用假資料
    story_data = {
        "1": ["你走進教室，發現今天老師請假了。", "你決定去圖書館自習。", "學習進度+1，心情也不錯。"]
    }

    play_week_story(screen, story_data, current_week=1)

    pygame.quit()
