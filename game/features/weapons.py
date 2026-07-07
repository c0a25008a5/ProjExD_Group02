"""武器機能(担当:
"""

from __future__ import annotations

import math
from typing import Any

from game.core import Feature, FPSGame




class Weapons(Feature):

    name = "武器"

    def setup(self, game: FPSGame) -> None:
        self.muzzle_timer = 0.0 

    def update(self, game: FPSGame, dt: float) -> None:
        self.muzzle_timer = max(0.0, self.muzzle_timer - dt)

    def on_mouse_down(self, game: FPSGame, button: int) -> None:
        if button != 1: 
            return
        if game.player.ammo <= 0:
            game.emit("empty_click", {})  
            return
        game.player.ammo -= 1
        game.fire_bullet(damage=1)
        self.muzzle_timer = 0.07

    def draw_hud(self, game: FPSGame, screen: Any) -> None:

        draw = game.pygame.draw
        cx = game.width // 2
        sway_x = int(math.sin(game.time * 1.7) * 4)
        sway_y = int(math.cos(game.time * 3.4) * 3)
        kick = int(self.muzzle_timer * 260)
        gx = cx + sway_x
        gy = game.height - 128 + sway_y + kick


        draw.polygon(screen, (52, 46, 44), [(gx - 88, gy + 132), (gx - 30, gy + 66), (gx + 30, gy + 66), (gx + 88, gy + 132)])
        draw.rect(screen, (74, 62, 54), (gx - 34, gy + 62, 68, 70), border_radius=8)
        draw.rect(screen, (58, 48, 42), (gx - 34, gy + 62, 68, 12), border_radius=6) 
        # フレームとスライド
        draw.rect(screen, (52, 54, 60), (gx - 30, gy - 6, 60, 78), border_radius=6)
        draw.rect(screen, (108, 112, 120), (gx - 24, gy - 18, 48, 62), border_radius=4)
        draw.rect(screen, (76, 80, 88), (gx - 24, gy - 18, 48, 14), border_radius=4) 
        draw.rect(screen, (30, 32, 36), (gx + 4, gy - 8, 16, 8), border_radius=2)  
        # 銃身と銃口
        draw.rect(screen, (38, 40, 46), (gx - 10, gy - 34, 20, 22), border_radius=3)
        draw.rect(screen, (14, 14, 16), (gx - 6, gy - 31, 12, 9), border_radius=2) 
        # フロントサイトと黄色のアクセント
        draw.rect(screen, (230, 190, 70), (gx - 3, gy - 43, 6, 8))
        draw.rect(screen, (230, 190, 70), (gx - 24, gy + 32, 48, 5))

        if self.muzzle_timer > 0.0:
            flash_y = gy - 40
            draw.polygon(screen, (255, 236, 120), [(gx, flash_y - 48), (gx - 27, flash_y), (gx + 27, flash_y)])
            draw.polygon(screen, (255, 150, 40), [(gx, flash_y - 25), (gx - 14, flash_y), (gx + 14, flash_y)])
            draw.circle(screen, (255, 246, 200), (gx, flash_y - 9), 7)
