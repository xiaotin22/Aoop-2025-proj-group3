import pygame
import os
from UI.start_select import CharacterSelectScene
from character import Character, Bubu, Yier, Mitao, Huihui

def start_game(screen):
    scene = StartScene(screen)
    result = scene.run()

    if result == "START":
        print("遊戲開始！")
    elif result == "show intro":
        print("顯示遊戲介紹")
        intro_scene = IntroScene(screen)
        intro_scene.run()
        return start_game(screen)  # 重新跑開始畫面

    return True


def select_character(screen):
    pygame.display.set_caption(f"Choose the character you like")

    scene = CharacterSelectScene(screen)
    selected = scene.run()
    print("玩家選擇角色為：", selected)

    if selected == "布布 Bubu":
        return Bubu()
    elif selected == "一二 Yier":
        return Yier()
    elif selected == "蜜桃 Mitao":
        return Mitao()
    elif selected == "灰灰 Huihui":
        return Huihui()
    else:
        print("未選擇角色，回到主畫面")
        return select_character(screen)


def game_loop(screen, player):
    pygame.display.set_caption(f"第 {player.week_number} 週｜角色：{player.name}")
    while player.week_number <= 16:
        scene = MainMenuScene(screen, player)
        player_option = scene.run()

        if player_option == "Open Character Info":
            attr_scene = AttributeScene(screen, player)
            attr_scene.run()

        elif player_option == "Next Week":
            event_scene = EventScene(screen, player)
            event_scene.run()


def end_game(screen, player):
    pygame.display.set_caption("End of Game")
    scene = EndScene(screen, player)
    player.show_status()
    player.calculate_GPA()

    if scene.run() == "Exit":
        print("遊戲結束，謝謝遊玩！")


# 🕹️ 主程序入口點
def main():
    

    pygame.init()
    pygame.mixer.init()

    # Define screen dimensions
    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1200
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption('Game_Start')

    if start_game(screen):
        player = select_character(screen)
        player.show_status()
        game_loop(screen, player)
        end_game(screen, player)

    pygame.quit()


if __name__ == "__main__":
    main()
