import pygame
import sys
from UI.components.button import Button
from UI.components.base_scene import wrap_text
import json

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("事件便條視窗疊加")

# 背景圖片
background_img = pygame.image.load("resource/image/background_intro.png").convert()

# 便條紙圖片
note_img = pygame.image.load("resource/image/event_window_bubu.PNG").convert_alpha()
orig_width, orig_height = note_img.get_size()

# 假設我們想讓寬度變成 800，並等比例縮放高度
target_width = 800
scale_factor = target_width / orig_width
target_height = int(orig_height * scale_factor)

note_img = pygame.transform.smoothscale(note_img, (target_width, target_height))
note_rect = note_img.get_rect(center=(600, 400))

font = pygame.font.Font("resource/font/JasonHandwriting3-SemiBold.ttf", 36)
font_small = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)

# 載入所有週資料
with open("event/events.json", "r", encoding="utf-8") as f:
    all_weeks_data = json.load(f)

# 假設要顯示第1週
current_week = "week_2"
week_data = all_weeks_data[current_week]

# 事件文字（取第一個事件的描述）
event_text = week_data["events"][0]["description"]

# 選項轉成 [(text, key), ...]
options = []
for key, option in week_data["events"][0]["options"].items():
    options.append((option["text"], key))
    
# 按鈕顏色設定
BUTTON_COLOR = (200, 180, 150)
BUTTON_HOVER_COLOR = (255, 220, 180)
BUTTON_TEXT_COLOR = (50, 30, 10)

button_width = 520
button_height = 60  # 高度加大，因為雙行文字需要更多空間
button_margin = 15


# 按鈕與文字放置在便條紙下方區域，留出右下角熊圖區域(約100x100px)避免遮擋
buttons = []
start_x = note_rect.centerx - 260
start_y = note_rect.centery - 30   # 便條紙底部往上留空間放按鈕
max_text_width = button_width - 20  # 按鈕內文字左右留10px空白

for i, (text, key) in enumerate(options):
    rect = pygame.Rect(
        start_x,
        start_y + i * (button_height + button_margin),
        button_width,
        button_height
    )
    buttons.append((rect, text, key))

def update():
    global running
    print(pygame.mouse.get_pos())  # 印出滑鼠位置
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for rect, text, key in buttons:
                if rect.collidepoint(pos):
                    print(f"你選擇了選項 {key}: {text}")

def draw():
    screen.blit(background_img, (0, 0))  # 畫背景
    screen.blit(note_img, note_rect)     # 畫便條紙

    # 畫事件文字（多行換行）
    max_event_width = target_width - 250  # 事件文字左右留空間
    event_lines = wrap_text(event_text, font, max_event_width)
    for i, line in enumerate(event_lines):
        line_surf = font.render(line, True, (50, 50, 50))
        screen.blit(line_surf, (note_rect.centerx-260 , note_rect.centery - 200 + i * (font.get_height() + 5)))

    mouse_pos = pygame.mouse.get_pos()
    for rect, text, key in buttons:
         # 半透明按鈕背景帶圓角
        button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        alpha = 180  # 透明度 0-255
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        rgba_color = (*color, alpha)
        pygame.draw.rect(button_surf, rgba_color, button_surf.get_rect(), border_radius=8)
        screen.blit(button_surf, (rect.left, rect.top))
        
        # 文字換行成兩行，並垂直置中
        lines = wrap_text(" "+text, font_small, max_text_width)
        line_height = font_small.get_height()
        total_text_height = line_height * len(lines)
        start_text_y = rect.top + (rect.height - total_text_height) // 2

        for idx, line in enumerate(lines):
            text_surf = font_small.render(line, True, BUTTON_TEXT_COLOR)
            text_rect = text_surf.get_rect()
            text_rect.left = rect.left + 10  # 按鈕左側內距10px
            text_rect.top = start_text_y + idx * line_height
            screen.blit(text_surf, text_rect)

def main():
    global running
    running = True
    clock = pygame.time.Clock()

    while running:
        update()
        draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
