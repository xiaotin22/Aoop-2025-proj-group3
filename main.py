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
# from UI.diary_scene import DairyScene
from UI.sound_control_scene import SoundControlScene
from UI.end_scene import EndScene
from UI.feedback_scene import FeedbackScene

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
        return Bubu()
    elif selected == "一二 Yier":
        return Yier()
    elif selected == "蜜桃 Mitao":
        return Mitao()
    elif selected == "灰灰 Huihui":
        return Huihui()
    else:
        print("未選擇角色，回到主畫面")
        return None  # 修正

def game_loop(screen, player):
    while player.week_number < 16:
        pygame.display.set_caption(f"第 {player.week_number+1} 週｜角色：{player.name}")
        scene = MainScene(screen, player)
        player_option = scene.run()
        print(f"玩家選擇的操作為：{player_option!r}")

        if player_option == "RESTART":
            print("[game_loop] 收到 RESTART，return 中")
            return "RESTART"
        elif player_option == "Quit":
            print("遊戲結束")
            return False
        elif player_option == "Next Story":
            player.week_number += 1
            player.week_data = player.all_weeks_data[f"week_{player.week_number}"]
            story_scene = StoryScene(screen, player)
            story_scene.run()
            event_scene = EventScene(screen, player)
            event_scene.run()

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
            feedback_scene = FeedbackScene(screen, player)
            feedback_scene.run()
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
            break

        player = select_character(screen)
        if not isinstance(player, Character):
            continue

        result = game_loop(screen, player)
        if result == "RESTART":
            print("[main] 收到 RESTART，重新啟動遊戲流程")
            continue  # ✅ 重來整個流程（包括 start_game）

        elif not result:
            break

        # ⛔️ 注意：這裡也可能要跳過計算 GPA（因為 player 重設了）
        player.calculate_GPA()
        result = end_game(screen, player)

        if result == "RESTART":
            print("[main] end_game 收到 RESTART，重新啟動遊戲流程")
            continue
        elif not result:
            break

    pygame.quit()


if __name__ == "__main__":
    main()