import pygame
import os

class Character:
    def __init__(self, name, intelligence, mood, health, social):
        self.name = name
        self.intelligence = intelligence
        self.mood = mood
        self.health = health
        self.social = social
        self.knowledge = 0
        self.week_number = 1

    def study(self):
        if self.knowledge >= 100:
            print(f"{self.name} 已經滿級啦 📚✨")
            return

        # 成長規則：主要由智力決定，心情與健康提供加成，交際會略減分心影響
        growth = (
            self.intelligence * 0.05+
            self.mood * 0.04 +
            self.health * 0.03 -
            self.social * 0.01
        )
        growth = max(0, growth)  # 不會負成長！
        self.knowledge = min(100, self.knowledge + growth)
        self.mood = max(0, self.mood - 5)  # 學習會稍微降低心情
        self.health = max(0, self.health - 2)  # 學習會稍微降低體力
        print(f"{self.name} 認真學習中 📖✨ 知識增加了 {growth} 點！現在是 {self.knowledge}/100")

    def socialize(self):
        if self.social >= 100:
            print(f"{self.name} 已經社交滿級啦 🎉✨")
            return

        # 社交成長規則：主要由心情決定，智力與健康提供加成，交際本身會略減分心影響
        growth = (
            (self.social-50) * 0.05 +
            (self.mood-50) * 0.03 +
            (self.health-30) * 0.01
        )
        self.social = min(100, self.social + growth)
        if growth > 6:
            self.knowledge = min(100, self.knowledge + growth) # 獲得考古題
        self.mood = min(100, self.mood + 5)
        self.health = max(0, self.health - 5) # 社交會稍微降低體力

    def play_game(self):
        if self.mood >= 100:
            print(f"{self.name} 已經玩到極致啦 🎮✨")
            return

        # 玩遊戲成長規則：主要由心情決定，智力與健康提供加成，交際會略減分心影響
        growth = (
            (self.mood-50) * 0.05 +
            (self.intelligence-50) * 0.02 +
            (self.health-30) * 0.01 -
            (self.social-30) * 0.01
        )
        self.mood = min(100, self.mood + growth)
        self.health = max(0, self.health - 5)
        self.knowledge = max(0, self.knowledge - growth * 0.5)

    def rest(self):
        if self.health >= 100:
            print(f"{self.name} 已經休息夠啦 😴✨")
            return

        # 休息成長規則：主要由體力決定，心情與智力提供加成，交際會略減分心影響
        growth = (
            (100 - self.mood) * 0.05 +
            (self.health - 50) * 0.02 +
            (self.intelligence - 50) * 0.01 -
            (self.social - 30) * 0.01
        )
        self.health = min(100, self.health + growth)
        self.mood = min(100, self.mood + growth * 0.5)
        self.knowledge = max(0, self.knowledge - growth * 0.2)

    def calculate_GPA(self):
        pass

    def show_status(self):
        print(f"{self.name} 在第{self.week_number}週的狀態：")
        print(f"智力：{self.intelligence} | 心情：{self.mood} | 體力：{self.health} | 社交：{self.social} | 知識：{self.knowledge}/100")
        print("=======================================================")
        


# 🧸 各角色子類別
class Bubu(Character):
    def __init__(self):
        super().__init__("Bubu", intelligence=70, mood=65, health=80, social=30)
    
class Yier(Character):
    def __init__(self):
        super().__init__("Yier", intelligence=75, mood=85, health=60, social=90)

class Mitao(Character):
    def __init__(self):
        super().__init__("Mitao", intelligence=95, mood=50, health=45, social=60)

class Huihui(Character):
    def __init__(self):
        super().__init__("Huihui", intelligence=80, mood=90, health=50, social=65)
