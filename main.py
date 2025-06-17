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

        if player_option == "SETTING":
            set_scene = SetScene(screen)
            setting_result = set_scene.run()
            print(f"設定場景回傳：{setting_result}")
            if setting_result == "BACK":
                continue  # 回主畫面
            elif setting_result == "RESTART":
                return "RESTART"  # 重啟遊戲流程
            else:
                return False  # 點到 Quit 就結束


        # if player_option == "Open Diary":
            # attr_scene = DairyScene(screen, player)
            # attr_scene.run()


        elif player_option == "Next Story":
            player.week_number += 1
            player.week_data = player.all_weeks_data[f"week_{player.week_number}"]
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
        # 每輪都重新從頭開始（包含選角色）
        if not start_game(screen):
            break

        player = select_character(screen)
        if not isinstance(player, Character):
            continue  # 沒有選角色就回主選單

        result = game_loop(screen, player)

        if result == "RESTART":
            continue  # 回到最外層 while 重新開始
        elif not result:
            break  # 玩家選擇結束

        player.calculate_GPA()
        if not end_game(screen, player):
            break

    pygame.quit()