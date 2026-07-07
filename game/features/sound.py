"""サウンド・演出機能(担当: 
"""

from __future__ import annotations

from typing import Any

from game.core import Feature, FPSGame

SOUNDS: dict[str, str] = {
    "player_shot": "assets/shot.wav",
    "target_hit": "assets/hit.wav",
    "enemy_defeated": "assets/explosion.wav",
    "player_damaged": "assets/hurt.wav",
    "player_healed": "assets/heal.wav",
    "item_picked": "assets/pickup.wav",
    "empty_click": "assets/click.wav",
    "victory": "assets/win.wav",
    "game_over": "assets/lose.wav",
}


class Sound(Feature):


    name = "サウンド・演出"

    def setup(self, game: FPSGame) -> None:
        for event, path in SOUNDS.items():

            game.on(event, lambda data, p=path: game.play_sound(p, volume=0.8))

