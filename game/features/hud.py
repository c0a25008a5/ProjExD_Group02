"""HUD機能(担当:
"""

from __future__ import annotations

from typing import Any

from game.core import Feature, FPSGame


class Hud(Feature):


    name = "HUD"

    def setup(self, game: FPSGame) -> None:
        self.kills = 0
        game.on("enemy_defeated", self.on_enemy_defeated)

    def on_enemy_defeated(self, data: dict[str, Any]) -> None:
        self.kills += 1

    def draw_hud(self, game: FPSGame, screen: Any) -> None:
        game.draw_bar(20, 44, game.player.health, game.player.max_health, color=(230, 70, 60), label="HP")
        game.draw_bar(20, 96, game.player.ammo, game.player.max_ammo, color=(80, 160, 255), label="弾薬")
        game.draw_text(f"スコア {game.score}", 20, 122, size=22)
        game.draw_text(f"撃破数 {self.kills}", 20, 150, size=22)
        game.draw_text(
            "WASD移動 / Shiftダッシュ / マウス視点 / 左クリック射撃 / ESC終了",
            20,
            game.height - 36,
            size=18,
            color=(160, 168, 180),
        )
