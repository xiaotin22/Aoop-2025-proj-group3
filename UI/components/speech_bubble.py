import pygame
import random

class SpeechBubble:
    def __init__(self, player, pos, font, duration=1500):
        self.player = player
        self.text = self.get_text()
        self.pos = pos  # (x, y) 中心點
        self.font = font
        self.start_time = pygame.time.get_ticks()
        self.duration = duration  # 毫秒


    def draw(self, screen):
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        padding = 20
        bubble_w = text_surf.get_width() + padding
        bubble_h = text_surf.get_height() + padding
        bubble_rect = pygame.Rect(0, 0, bubble_w, bubble_h)
        bubble_rect.center = self.pos
        pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 2, border_radius=15)
        screen.blit(text_surf, text_surf.get_rect(center=bubble_rect.center))

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration
    
    def get_text(self):
        if self.player.mood <= self.player.low_mood_limit:

            if self.player.knowledge <= self.player.low_knowledge_limit:
                num = random.randint(0, len(low_knowledge) - 1)
                self.text = low_knowledge[num]
                
            elif self.player.social <= self.player.low_social_limit :
                num = random.randint(0, len(low_social) - 1)
                self.text = low_social[num]
                
            else :
                num = random.randint(0, len(low_energy) - 1)
                self.text = low_energy[num]
                
        elif self.player.mood >= self.player.high_mood_limit:
            
            if self.player.knowledge >= self.player.high_knowledge_limit:
                num = random.randint(0, len(high_knowledge) - 1)
                self.text = high_knowledge[num]
                
            elif self.player.social >= self.player.low_social_limit :
                num = random.randint(0, len(high_social) - 1)
                self.text = high_social[num]
                
            else :
                num = random.randint(0, len(high_energy) - 1)
                self.text = high_energy[num]
                
        else:
            num = random.randint(0, len(commom) - 1)
            self.text = commom[num]
            
        low_knowledge = [ "「我不是不想唸書，我只是醒著的時間都在焦慮。」",
                        "「成績單不是紙，是我精神狀況的體檢報告。」",
                        "「我不是不努力，是未來看起來真的不值得我努力。」",
                        "「系統通知：你的人生正在緩慢當機中，請稍候...」",
                        "「GPA 就像月亮，不會發光但總能反射我人生的黑暗。」",
                        "「別人都在期末衝刺，我在懷疑人生。」"
                        ]
        low_social = ["「明明社交距離解除了，我的孤單卻沒解除。」",
                        "「我發的限動沒人會看，但我還是發了。」",
                        "「社交能量是限量的，講一句話就想逃回宿舍。」",
                        "「怕尷尬所以沉默，沉默了又更尷尬。」",
                        "「社交場合對我來說是高難度副本，我是新手村NPC。」",
                        " 你說我安靜，我只是還沒 download 好社交模組。」"
                        ]         
        low_energy = ["「我的未來不是夢，是爛尾樓。」",
                        "「我不是翹課，我是在追尋人生的更多可能性。」",
                        "「今天只想做三件事：吃飯、睡覺、當廢物。」",
                        "「我不是在拖延，我是在回魂。」",
                        "「醒來是本日第一個錯誤。」",
                        "「想逃避但連逃的力氣都沒有。」",
                        "「一天的活力就只夠刷個手機和嘆口氣。」",
                        "「我不是不在狀況內，我是卡在狀況外進不去也出不來。」",
                        "「我不是不想上課，我只是想多睡一會。」",
                        ]
        high_knowledge = [ "「甜課選得好，週週像在放寒假。」",
                        "「不是我愛炫耀，是我的成績自己會發光。」",
                        "「別問我怎麼念的，我只是剛好比教授還懂那一章。」",
                        "「好想把成績單放大貼在宿舍牆上（但怕室友心臟受不了）」",
                        "「我不是作弊，只是我和考古題有精神連結。」",
                        "「我不是在讀書，我是在和知識談戀愛。」",
                        "「成績爆表，我的精神狀態也順便升級了 」"
                        ]
        high_social = ["「早八也能社交，晚上還能開趴，電力永遠滿格 」",
                        "「認識我不是意外，是你的幸運！」",
                        "「陌生人是還沒認識的朋友 ~」",
                        "「我不是在刷存在感，我是在建立人脈網絡。」",
                        "「我不是故意太熱情，我是天生開啟社交 buff 模式 」"
                        ]
        high_energy = ["「今天不一定順利，但我一定努力。」",
                        "「夢想不會自己實現，但我可以逼自己起床！」",
                        "「小事完成也是成就感，大事失敗也有經驗值 ~ 」",
                        "「要焦慮，就邊跑邊焦慮，至少風會吹走一點煩惱。」",  
                        "「失敗乃成功之母——那我應該快變祖母了吧。」",
                        "「加油啊自己，你可是我最喜歡的那個廢物了。」",
                        "「就算只前進0.1，也比昨天原地打轉好多了。」"
                        ]
        commom = ["「原本想讀書的，結果桌子太遠。」",
                    "「今天也是努力躺平的一天。」",
                    "「想喝手搖，但又想存錢買麥當勞。」",
                    "「已經吃膩學餐了，但走出校門又太熱。」",
                    "「點開 foodpanda，關掉，再點開，還是不知道要吃什麼。」",
                    "「報告要不要開始寫？... 再滑一下就好...」",
                    "「今天的我絕對會寫報告（和昨天的我一樣堅定）。」",
                    "「要不要回訊息…先裝死一下好了。」",
                    "「限動要發哪張？這張太假掰，那張太真實…」",
                    "「剛剛教授在說什麼？我怎麼只記得他今天穿藍色。」",
                    "「這學期怎麼已經快過完了，我什麼都還沒做。」",
                ]
    
        
        return self.text
    
    