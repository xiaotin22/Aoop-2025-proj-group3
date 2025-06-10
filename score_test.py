from character import Bubu, Yier, Mitao, Huihui
import random
import statistics
import matplotlib.pyplot as plt
from collections import Counter

midterm_results = []
final_results = []
actions = ["study", "rest", "play_game", "socialize"]
characters = [Bubu, Yier, Mitao, Huihui]

for _ in range(300):
    player = random.choice(characters)()
    for _ in range(16):
        action = random.choice(actions)
        getattr(player, action)()
    player.get_midterm()
    player.get_final()
    midterm_results.append(player.midterm)
    final_results.append(player.final)

# 數據
midterm_counts = Counter(midterm_results)
final_counts = Counter(final_results)

midterm_scores_sorted = sorted(midterm_counts.keys())
midterm_freqs = [midterm_counts[score] for score in midterm_scores_sorted]

final_scores_sorted = sorted(final_counts.keys())
final_freqs = [final_counts[score] for score in final_scores_sorted]

# 平滑函數
def smooth_curve(y, window_size=3):
    smoothed = []
    for i in range(len(y)):
        start = max(0, i - window_size)
        end = min(len(y), i + window_size + 1)
        smoothed.append(sum(y[start:end]) / (end - start))
    return smoothed

# 平滑
smoothed_midterm = smooth_curve(midterm_freqs)
smoothed_final = smooth_curve(final_freqs)

# 平均值
mean_midterm = round(statistics.mean(midterm_results), 2)
mean_final = round(statistics.mean(final_results), 2)

# 繪圖
plt.figure(figsize=(12, 6))
plt.plot(midterm_scores_sorted, smoothed_midterm, label=f"Midterm (Avg: {mean_midterm})", color="blue", linewidth=2)
plt.plot(final_scores_sorted, smoothed_final, label=f"Final (Avg: {mean_final})", color="red", linewidth=2)

plt.title("Score Distribution of Midterm and Final Exams")
plt.xlabel("Score")
plt.ylabel("People")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


