import pygame
from UI.lucky_wheel_scene import LuckyWheelScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("幸運轉盤測試")

    # 測試選項
    options = ["超可愛學姐\n帥潮學長", "看起來是系邊\n有點宅宅的學長", "超搞笑的系核\n第一次見面\n就表演倒立走路", "卷哥卷姐", "被放生了"]

    wheel = LuckyWheelScene(screen, options)
    result = wheel.run()
    print(f"轉盤結果: {result}")

if __name__ == "__main__":
    main()

     