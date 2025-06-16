import pygame
from UI.character_select import CharacterSelectScene
from UI.start_scene import StartScene
from UI.intro_scene import IntroScene
from UI.story_scene import StoryScene
from UI.event_scene import EventScene
from UI.set_scene import SetScene
from character import Character, Bubu, Yier, Mitao, Huihui
from UI.main_scene import MainScene
from UI.rank_scene import RankScene
# from UI.diary import DairyScene
from UI.sound_control_scene import SoundControlScene
from UI.end_scene import EndScene

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
        
    elif result == "SOUND_CONTROL":
        print("調整音效")
        sound_control_scene = SoundControlScene(screen)
        sound_control_scene.run()
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
        scene = MainScene(screen, player)
        scene.run()
        return player
    elif selected == "一二 Yier":
        player = Yier()
        scene = MainScene(screen, player)
        scene.run()
        return player
    elif selected == "蜜桃 Mitao":
        player = Mitao()
        scene = MainScene(screen, player)
        scene.run()
        return player
    elif selected == "灰灰 Huihui":
        player = Huihui()
        scene = MainScene(screen, player)
        scene.run()
        return player
    else:
        print("未選擇角色，回到主畫面")
        return start_game(screen)
    


def game_loop(screen, player):
    while player.week_number < 16:
        pygame.display.set_caption(f"第 {player.week_number} 週｜角色：{player.name}")
        scene = MainScene(screen, player)
        player_option = scene.run()
        print(f"玩家選擇的操作為：{player_option!r}")

        if player_option == "SETTING":
            set_scene = SetScene(screen)
            setting_result = set_scene.run()
            print(f"設定場景回傳：{setting_result}")
            if setting_result == "BACK":
                continue  # ✅ 回主畫面
            else:
                return False  # 如果不小心點 quit，就結束

        # if player_option == "Open Diary":
            # attr_scene = DairyScene(screen, player)
            # attr_scene.run()

        elif player_option == "Next Story":
            player.week_number += 1
            story_scene = StoryScene(screen, player)
            story_scene.run()
            event_scene = EventScene(screen, player)
            event_scene.run()
        
        
        elif player_option == "Quit":
            print("遊戲結束")
            return False
    return True
        
        
def end_game(screen, player):
    pygame.display.set_caption("End of Game")
    while True:
        scene = EndScene(screen, player)
        result = scene.run()
        if result == "SHOW_RANK":
            rank_scene = RankScene(screen, player)
            rank_scene.run()
            # 回到結尾場景
        elif result == "RESTART":
            print("重新開始遊戲")
            return "RESTART"
        elif result == "FEEDBACK":
            import webbrowser
            webbrowser.open("https://forms.gle/kfpH9eV348CGnTZa8")
            print("感謝您的回饋！")
            # 回到結尾場景
        elif result == "Exit":
            print("遊戲結束，謝謝遊玩！")
            return False
        else:
            # 其他情況也結束
            return False
        

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

        if not game_loop(screen, player):
            break
        
        player.calculate_GPA()
        if not end_game(screen, player):
            break


    pygame.quit()


if __name__ == "__main__":
    main()