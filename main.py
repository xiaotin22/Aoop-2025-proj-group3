import pygame
import os
from UI.character_select import CharacterSelectScene
from UI.start_scene import StartScene
from UI.intro_scene import IntroScene
from character import Character, Bubu, Yier, Mitao, Huihui
from UI.main_scene import MainScene

def start_game(screen):
    scene = StartScene(screen)
    result = scene.run()


    if result == "START":
        print("遊戲開始！")
        return True
    elif result == "SHOW_INTRO":
        print("顯示遊戲介紹")
        intro_scene = IntroScene(screen)
        intro_scene.run()
        return start_game(screen)
        
    elif result == "RANK":
        print("顯示排行榜")
        rank_scene = RankScene(screen)
        rank_scene.run()
        return start_game(screen)
    elif result == "QUIT":
        print("遊戲結束")
        return False


def select_character(screen):
    pygame.display.set_caption(f"Choose the character you like")

    scene = CharacterSelectScene(screen)
    selected = scene.run()
    print("玩家選擇角色為：", selected)

    if selected == "布布 Bubu":
        player = Bubu()
        print("test")
        scene = MainScene(screen, player, "resource/gif/four_char2_frames")
        scene.run()
        return player
    elif selected == "一二 Yier":
        player = Yier()
        scene = MainScene(screen, player, "resource/gif/yier_exciting_frames")
        scene.run()
        return player
    elif selected == "蜜桃 Mitao":
        return Mitao()
    elif selected == "灰灰 Huihui":
        return Huihui()
    else:
        print("未選擇角色，回到主畫面")
        return start_game(screen)


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

    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1200
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Game_Start')

    while True:
        if not start_game(screen):
            break  # 玩家選擇結束遊戲

        player = select_character(screen)
        if not isinstance(player, Character):
            continue  # 沒有選擇角色，回到主選單

        player.show_status()
        game_loop(screen, player)
        end_game(screen, player)
        # 遊戲結束後自動回到主選單
    pygame.quit()

if __name__ == "__main__":
    main()
