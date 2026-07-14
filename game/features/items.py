"""アイテム機能(担当:吉荒倖汰 
"""
from __future__ import annotations

import math

from typing import Any

from game.core import Feature, FPSGame, GameObject
class Items(Feature):
    """マップのHに回復パック、Aに弾薬パックを置き、触れたら拾えるようにする。"""

    name = "アイテム"

    def setup(self, game: FPSGame) -> None:
        self.game = game
        self.health_packs: list[GameObject] = [
            game.spawn_pickup(x, z, color=(74, 220, 92), name="health")
            for x, z in game.find_cells("H")
        ]
        self.ammo_packs: list[GameObject] = [
            game.spawn_pickup(x, z, color=(85, 172, 255), name="ammo")
            for x, z in game.find_cells("A")
        ]
        # ゴールドアイテムを配置する処理
        self.gold_items: list[GameObject] = [
            game.spawn_pickup(x, z, color=(255, 215, 0), name="gold")
            for x, z in game.find_cells("G")
        ]
        # レアアイテムを配置する処理
        self.rare_items: list[GameObject] = [
            game.spawn_pickup(x, z, color=(255, 0, 255), name="rare")
            for x, z in game.find_cells("R")
        ]

        # 鍵と扉の初期化
        self.keys: list[GameObject] = [
            game.spawn_pickup(x, z, color=(192, 192, 192), name="key")
            for x, z in game.find_cells("K")
        ]
        self.doors: list[GameObject] = []
        for x, z in game.find_cells("D"):
            door = game.spawn_box(x, z, size=(1.9, 2.2, 0.4), color=(150, 110, 60))
            game.add_obstacle(door)
            self.doors.append(door)
        self.has_key = False

        # 時間制限パワーアップの初期化
        self.powerups: list[GameObject] = [
            game.spawn_pickup(x, z, color=(255, 100, 100), name="powerup")
            for x, z in game.find_cells("U")
        ]
        self.score_multiplier = 1
        self.ammo_regen = False
        self.ammo_timer = 0.0

    def update(self, game: FPSGame, dt: float) -> None:
        # 全てのアイテムをふわふわ回転させる
        for pack in self.health_packs + self.ammo_packs + self.gold_items + self.rare_items + self.keys + self.powerups:
            pack.yaw += dt * 2.0
            pack.y = 0.3 + math.sin(game.time * 3.0) * 0.08 # ← ここを get_time() から time に戻す

        for pack in self.health_packs[:]:
            if game.near_player(pack, 0.7) and game.player.health < game.player.max_health:
                game.heal_player(25)
                self._take(pack, self.health_packs)

        for pack in self.ammo_packs[:]:
            if game.near_player(pack, 0.7) and game.player.ammo < game.player.max_ammo:
                game.player.ammo = min(game.player.max_ammo, game.player.ammo + 15)
                game.flash((70, 170, 255), 0.25)
                self._take(pack, self.ammo_packs)
        
        # ゴールドアイテムを取ったときの処理
        for pack in self.gold_items[:]:
            if game.near_player(pack, 0.7):
                game.score += 100 * self.score_multiplier
                self._take(pack, self.gold_items)

        # レアアイテムを取ったときの処理
        for pack in self.rare_items[:]:
            if game.near_player(pack, 0.7):
                game.score += 500 * self.score_multiplier
                self._take(pack, self.rare_items)
        
        # 鍵を取ったときの処理
        for pack in self.keys[:]:
            if game.near_player(pack, 0.7):
                self.has_key = True
                self._take(pack, self.keys)

        # パワーアップを取ったときの処理
        for pack in self.powerups[:]:
            if game.near_player(pack, 0.7):
                # 30秒間スコア2倍
                self.score_multiplier = 2
                game.after(30.0, self.reset_score_multiplier)
                # 30秒間弾薬自動回復
                self.ammo_regen = True
                game.after(30.0, self.stop_ammo_regen)
                
                self._take(pack, self.powerups)

        # パワーアップ中の弾薬自動回復処理
        if self.ammo_regen:
            self.ammo_timer += dt
            if self.ammo_timer >= 1.0:
                self.ammo_timer = 0
                game.player.ammo += 1

    def _take(self, pack: GameObject, group: list[GameObject]) -> None:
        # パーティクルの色変更と数の増加
        self.game.spawn_particles(
            pack.x,
            pack.y,
            pack.z,
            color=(255, 220, 80),
            count=20
        )
        # フラッシュ演出を重ねる
        self.game.flash((255, 240, 120), 0.15)
        
        # 音担当に知らせる
        self.game.emit("item_picked", {
            "kind": pack.name
        })
    
    
        pack.remove()
        group.remove(pack)

# Eキーで扉を開ける処理
    # Eキーで扉を開ける処理
    def on_key_down(self, game: FPSGame, key: str) -> None:
        if key == "e":
            for door in self.doors[:]:
                if self.has_key and self.game.near_player(door, 1.5):
                    door.remove()
                    self.doors.remove(door)

    # スコア倍率を戻す処理
    def reset_score_multiplier(self) -> None:
        self.score_multiplier = 1

    # 弾薬の自動回復を止める処理
    def stop_ammo_regen(self) -> None:
        self.ammo_regen = False
