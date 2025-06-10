import pygame

def play_week_story(screen, story_dict, current_week):
    show_story = False
    story_index = 0
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif not show_story:
                if str(current_week) in story_dict:
                    show_story = True
                    story_index = 0
                else:
                    return current_week + 1  # 沒有劇情直接下一週
            elif show_story:
                story_index += 1
                if story_index >= len(story_dict.get(str(current_week), [])):
                    return current_week + 1  # 劇情播放完畢，進入下一週

        screen.fill((255, 255, 255))
        if not show_story:
            week_text = font.render(f"第 {current_week} 週", True, (90, 90, 150))
            screen.blit(week_text, (320, 200))
        else:
            lines = story_dict[str(current_week)]
            pygame.draw.rect(screen, (230, 230, 250), (150, 200, 500, 200))
            txt = font.render(lines[story_index], True, (60, 60, 60))
            txt_rect = txt.get_rect(center=(400, 300))
            screen.blit(txt, txt_rect)
            tip = font.render("（點擊繼續）", True, (180, 180, 180))
            screen.blit(tip, (400 - tip.get_width() // 2, 350))
        pygame.display.flip()
        clock.tick(30)
    
    return current_week + 1

