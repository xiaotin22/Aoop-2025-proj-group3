import pygame
import sys
from UI.components.button import Button

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("事件便條視窗疊加")

# 背景圖片
background_img = pygame.image.load("resource/image/background_intro.png").convert()

# 便條紙圖片
note_img = pygame.image.load("resource/image/event_window_bubu.PNG").convert_alpha()
orig_width, orig_height = note_img.get_size()

# 假設我們想讓寬度變成 400，並等比例縮放高度
target_width = 750
scale_factor = target_width / orig_width
target_height = int(orig_height * scale_factor)

note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
note_rect = note_img.get_rect(center=(600, 400))

font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
font_small = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
# 事件文字
event_text = "事件 1： 室友邀請你一起吃午餐，你決定..."

# 選項
options = [
    ("A. 答應它一起去吃飯 （social）", "A"),
    ("B. 婉拒，跟更熟的人有約了 (play game)", "B"),
    ("C. 婉拒，吃啥飯（OS: 趁你吃飯，我偷捲）(study)", "C"),
    ("D. 答應，『好阿，要不要一起叫外送』 (rest)", "D")
]

# 按鈕顏色設定
BUTTON_COLOR = (200, 180, 150)
BUTTON_HOVER_COLOR = (255, 220, 180)
BUTTON_TEXT_COLOR = (50, 30, 10)

button_width = 520
button_height = 40
button_margin = 10

buttons = []
for i, (text, key) in enumerate(options):
    rect = pygame.Rect(
        note_rect.left + 20,
        note_rect.top + 150 + i * (button_height + button_margin),
        button_width,
        button_height
    )
    buttons.append((rect, text, key))

def draw():
    screen.blit(background_img, (0, 0))  # 畫背景
    screen.blit(note_img, note_rect)     # 畫便條紙

    # 畫事件文字（簡單換行）
    event_surface = font.render(event_text, True, (50, 50, 50))
    screen.blit(event_surface, (note_rect.left + 30, note_rect.top + 30))

    mouse_pos = pygame.mouse.get_pos()
    for rect, text, key in buttons:
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text_surf = font_small.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        print(pygame.mouse.get_pos())
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for rect, text, key in buttons:
                    if rect.collidepoint(pos):
                        print(f"你選擇了選項 {key}: {text}")

        draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
