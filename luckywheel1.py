import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 選項列表
options1 = [
    "帥潮學長\n超可愛學姐",
    "有點宅宅的學長\n看起來是系邊",
    "的超搞笑系核\n就表演倒立走路\n第一次見面",
    "卷哥卷姐",
    "被放生了"
]

# 每個扇形大小相同
sizes = [1] * len(options1)

# 馬卡龍色系
colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]

# 載入 JasonHandwriting3-Regular 字體
try:
    font = FontProperties(fname='resource/font/JasonHandwriting3-Regular.ttf', size=26)
except Exception:
    print("無法載入 JasonHandwriting3-Regular.ttf，使用預設字體。")
    font = FontProperties(size=14)

# 繪製更大的圓餅圖(含外框)
fig, ax = plt.subplots(figsize=(8, 8))
wedges, _ = ax.pie(sizes, colors=colors, startangle=90, radius=1.2)

# 加上外框
circle = plt.Circle((0, 0), 1.2, color='gray', fill=False, linewidth=2)
ax.add_artist(circle)
line_spacing = 12  # 行距（可調整）

for i, wedge in enumerate(wedges):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x = 0.85 * np.cos(np.deg2rad(angle))
    y = 0.85 * np.sin(np.deg2rad(angle))
    lines = options1[i].splitlines()
    for j, line in enumerate(lines):
        # 每一行往下偏移 (j - (len(lines)-1)/2) * 行距，讓多行文字垂直置中
        offset = (j - (len(lines)-1)/2) * line_spacing / 100  # 100 是座標縮放因子，可依半徑調整
        ax.text(x, y + offset, line, ha='center', va='center', fontproperties=font)
ax.axis('equal')
plt.tight_layout()
plt.show()
