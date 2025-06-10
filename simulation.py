# simulation.py
from character import Bubu, Yier, Mitao, Huihui
import random, statistics, math
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from pathlib import Path
from bisect import bisect_left  # ★ 用來算 percentile
import csv

class Simulation:
    """
    角色行為模擬與成績分佈分析
    ---------------------------------
    n_players : 進行模擬的人次
    n_actions : 每位學生在一次模擬中執行的動作次數
    out_dir   : 圖檔輸出資料夾
    """
    def __init__(self, n_players: int = 300, n_actions: int = 16,
                 actions=None, characters=None, out_dir: str = "./simulation_plots") -> None:
        self.n_players = n_players
        self.n_actions = n_actions
        self.actions = actions or ["study", "rest", "play_game", "socialize"]
        self.characters = characters or [Bubu, Yier, Mitao, Huihui]

        # 迴圈結束後才會填進來的屬性
        self.midterm, self.final = [], []
        self.knowledge, self.gpa = [], []
        self.total_scores = []

        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # 核心流程
    # --------------------------------------------------
    def run(self) -> None:
        """執行整體模擬，產生所有 raw data。"""
        self.midterm.clear(); self.final.clear()
        self.knowledge.clear(); self.gpa.clear()

        for _ in range(self.n_players):
            player = random.choice(self.characters)()
            for _ in range(self.n_actions):
                getattr(player, random.choice(self.actions))()

            player.get_midterm()
            player.get_final()
            player.calculate_GPA()

            self.midterm.append(player.midterm)
            self.final.append(player.final)
            self.knowledge.append(player.knowledge)
            self.gpa.append(player.GPA)

        self._calc_total_scores()

    # --------------------------------------------------
    # 資料處理
    # --------------------------------------------------
    def _smooth_curve(self, y: list[int], window: int = 3) -> list[float]:
        smoothed = []
        for i in range(len(y)):
            start, end = max(0, i - window), min(len(y), i + window + 1)
            smoothed.append(sum(y[start:end]) / (end - start))
        return smoothed

    def _calc_total_scores(self) -> None:
        weighted = [m*0.35 + f*0.35 + k*0.30
                    for m, f, k in zip(self.midterm, self.final, self.knowledge)]
        self.total_scores = [math.sqrt(s)*10 for s in weighted]   # 轉換到 0–100

    # --------------------------------------------------
    # 圖表繪製
    # --------------------------------------------------
    def plot_midterm_final(self) -> Path:
        """折線圖：期中 & 期末分佈（平滑）。"""
        mid_cnt = Counter(self.midterm)
        fin_cnt  = Counter(self.final)

        mid_x = sorted(mid_cnt); mid_y = [mid_cnt[s] for s in mid_x]
        fin_x = sorted(fin_cnt); fin_y = [fin_cnt[s] for s in fin_x]

        plt.figure(figsize=(12, 6))
        plt.plot(mid_x, self._smooth_curve(mid_y), label=f"Midterm (Avg {statistics.mean(self.midterm):.2f})", linewidth=2)
        plt.plot(fin_x, self._smooth_curve(fin_y), label=f"Final (Avg {statistics.mean(self.final):.2f})", linewidth=2)
        plt.title("Score Distribution of Midterm and Final Exams")
        plt.xlabel("Score"); plt.ylabel("People"); plt.legend(); plt.grid(True); plt.tight_layout()

        out_file = self.out_dir / "midterm_final.png"
        plt.savefig(out_file); plt.close()
        return out_file

    def plot_total(self) -> Path:
        """長條圖：總分分佈。"""
        plt.figure(figsize=(12, 6))
        plt.hist(self.total_scores, bins=10, alpha=0.7, edgecolor='black',
                 label=f"Total Avg {statistics.mean(self.total_scores):.2f}")
        plt.title("Total Score Distribution")
        plt.xlabel("Total Score"); plt.ylabel("People"); plt.legend(); plt.grid(True)

        out_file = self.out_dir / "total_score.png"
        plt.savefig(out_file); plt.close()
        return out_file

     # --------------------------------------------------
    # ❶ 重新寫：累積人數表（同分只列一次）
    # --------------------------------------------------
    def cumulative_gpa_counts(self):
        """
        回傳兩個 list：
          gpa_unique   : 由小到大、不重複的 GPA
          cum_counts   : 人數累計——'≥ 該 GPA' 的人數
        """
        counts = Counter(self.gpa)                 # 各 GPA 出現次數
        gpa_unique = sorted(counts)               # 升冪、不重複
        total = len(self.gpa)
        cum_counts = []
        running = total
        for gpa in gpa_unique:
            cum_counts.append(running)
            running -= counts[gpa]                # 下一檔少掉「這一檔」人數
        return gpa_unique, cum_counts

    # --------------------------------------------------
    # ❷ Top-x% 計算—同分共享同一名次
    # --------------------------------------------------
    def percentile_from_top(self, gpa_value: float) -> float:
        """
        回傳『前 x%』；同分者算在同一檔次（≤ 你的全都算落後）。
        """
        higher = sum(1 for g in self.gpa if g > gpa_value)   # 嚴格大於你的
        pct = higher / len(self.gpa) * 100
        return pct 

    # --------------------------------------------
    # ❹ GPA 直方圖（可標註個人成績）
    # --------------------------------------------
    def plot_gpa(self, highlight: float | None = None, bins: int = 12) -> Path:
        """
        畫 GPA 直方圖  
        - highlight: 你的 GPA (0–4.3)，圖上標一點並顯示 Top-x%
        - bins:      直方圖分箱數
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        counts, edges, _ = ax.hist(
            self.gpa, bins=bins, alpha=0.7, edgecolor="black",
            label=f"GPA Avg {statistics.mean(self.gpa):.2f}"
        )

        if highlight is not None:
            pct = self.percentile_from_top(highlight)

            # ── 找出 highlight 落在哪個 bin ───────────────────────────
            bin_idx = np.searchsorted(edges, highlight, side="right") - 1
            bin_idx = np.clip(bin_idx, 0, len(counts) - 1)  # 防呆
            y_point = counts[bin_idx]

            # ── 畫標記點與文字 ────────────────────────────────────────
            ax.plot(highlight, y_point, marker="o", markersize=8)
            ax.text(
                highlight, y_point + counts.max() * 0.02,   # 往上 2% 畫標註
                f"Your GPA {highlight:.2f}\nTop {pct:.1f}%",
                va="bottom", ha="center", fontsize=12
            )

        ax.set_title("GPA Distribution")
        ax.set_xlabel("GPA (0–4.3)")
        ax.set_ylabel("People")
        ax.legend()
        ax.grid(True)

        out_file = self.out_dir / ("gpa_highlight.png" if highlight else "gpa.png")
        fig.tight_layout()
        fig.savefig(out_file)
        plt.close(fig)
        return out_file
    # --------------------------------------------
    # ❺ 一行完成：跑模擬 + 畫全部圖
    # --------------------------------------------
    def run_and_plot_all(self, personal_gpa: float | None = None) -> None:
        self.run()
        self.plot_midterm_final()
        self.plot_total()
        self.plot_gpa(highlight=personal_gpa)
        #print(f"完成！所有圖檔位於 {self.out_dir.resolve()}")

    def export_gpa_csv(
        self,
        filename: str | Path = "gpa_rank.csv",
        include_percentile: bool = True,
    ) -> Path:
        """
        依 GPA 由高到低輸出 CSV（同分共用名次，但 Rank 會跳號）
        欄位：Rank, GPA, People[, Top%]
        - Rank：名次，＝(前面已累計人數) + 1
        - GPA   ：該分數
        - People ：該分數的人數
        - Top%  ：你若擁有此分數，位於全班前幾 %
                    = (前面已累計人數 / 總人數) × 100
        """
        path = self.out_dir / filename
        counts   = Counter(self.gpa)            # GPA → 人數
        gpa_desc = sorted(counts, reverse=True) # 由高到低
        total    = len(self.gpa)

        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["Rank", "GPA", "People"]
            if include_percentile:
                header.append("Top%")
            writer.writerow(header)

            processed = 0                       # 已經累計過多少人
            for g in gpa_desc:
                rank = processed + 1            # 下一名次＝已累計人數 + 1
                row  = [rank, f"{g:.2f}", counts[g]]

                if include_percentile:
                    top_pct = processed / total * 100
                    row.append(f"{top_pct:.1f}%")

                writer.writerow(row)
                processed += counts[g]          # 把這一批人計入累計

        return path
# -------------------------------
# 範例呼叫
# -------------------------------
if __name__ == "__main__":
    sim = Simulation()
    sim.run_and_plot_all()
    

    # 1️⃣ 取得累積人數表
    gpa_sorted, cum_counts = sim.cumulative_gpa_counts()
    

    # 2️⃣ 看自己的 GPA 在哪裡
    my_gpa = 4.22
    pct = sim.percentile_from_top(my_gpa)
    csv_file = sim.export_gpa_csv()    # 預設存成 ./plots/gpa_rank.csv
    #print(f"CSV 已產生：{csv_file.resolve()}")

    # 3️⃣ 畫圖並標註
    outfile = sim.plot_gpa(highlight=my_gpa)
    #print(f"圖檔路徑：{outfile}")
