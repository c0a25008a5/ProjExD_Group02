"""サウンド・演出機能(担当: 
"""

from __future__ import annotations

from typing import Any

from game.core import Feature, FPSGame

SOUNDS: dict[str, str] = {
    "player_shot": "BGM/ダウンロード.mp3",
    "target_hit": "BGM/ダウンロード (3).mp3",
    "enemy_defeated": "BGM/ダウンロード (1).mp3",
    "player_healed": "BGM/ダウンロード (2).mp3",
    "item_picked": "BGM/ダウンロード (5).mp3",
    "empty_click": "BGM/ダウンロード (6).mp3",
    "victory": "BGM/ダウンロード (7).mp3",
    "game_over": "BGM/ダウンロード (4).mp3",
}




class Sound(Feature):

    PINCH = 0.3
    name = "サウンド・演出"

    def setup(self, game: FPSGame) -> None:
        self.game = game
        self._bgm_state = "normal"         
        self._pinch_blink = 0.0
        game.play_bgm("BGM/Milky_way.mp3")

        for event, path in SOUNDS.items():
            game.on(event, lambda data, p=path: game.play_sound(p, volume=0.8))

        game.on("player_damaged", self._on_damaged)
        game.on("player_healed", self._on_damaged)
        game.on("victory", self.on_victory)
        game.on("game_over", self.on_game_over)
        game.on("enemy_defeated", self._on_enemy_defeated)
        

    def _on_damaged(self, data: dict) -> None:   # ← game ではなく data
        game = self.game                          # ← self.game を使う
        is_pinch = game.player.health <= game.player.max_health * self.PINCH

        if is_pinch and self._bgm_state != "pinch":
            self._bgm_state = "pinch"
            game.play_bgm("BGM/あいつのピンチ.mp3", volume=0.5)
        elif not is_pinch and self._bgm_state != "normal":
            self._bgm_state = "normal"
            game.play_bgm("BGM/Milky_way.mp3", volume=0.5)



    def on_game_over(self, data):
        self.game.play_bgm("BGM/落とし物.mp3")

    def on_victory(self, data: dict) -> None:
        self._bgm_state = "end"
        self.game.play_bgm("BGM/貴族のお部屋.mp3")

        # 紙吹雪を3色ずらして連発
        colors = [(255, 220, 80), (120, 200, 255), (255, 120, 200)]
        for i, color in enumerate(colors):
            delay = 0.2 * (i + 1)
            self.game.after(delay, lambda c=color: self.game.spawn_particles(
                self.game.player.x, 1.5, self.game.player.z, color=c, count=20
            )) 

    def _on_enemy_defeated(self, data: dict) -> None:
        self.game.flash((255, 255, 255), 0.15)

    def update(self, game: FPSGame, dt: float) -> None:
        if self._bgm_state == "pinch":
            self._pinch_blink += dt

    def draw_hud(self, game: FPSGame, screen: Any) -> None:
        if self._bgm_state != "pinch":
            return
        # 0.5秒周期で点滅させる
        if int(self._pinch_blink / 0.5) % 2 == 0:
            game.draw_text(
                "LOW HP",
                game.width // 2, 40,
                size=36, color=(255, 60, 60), center=True, bold=True,
            )
       

            

