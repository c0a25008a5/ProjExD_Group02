"""敵機能(担当: 
"""

from __future__ import annotations

from game.core import Feature, FPSGame, GameObject

class Enemies(Feature):

    name = "敵"

    def setup(self, game: FPSGame) -> None:
        self.game = game  
        self.enemies: list[GameObject] = []
        for x, z in game.find_cells("E"):
            enemy = game.spawn_character(x, z, color=(180, 45, 40), style="grunt", name="enemy")
            enemy.data["hp"] = 3
            enemy.data["attack_cooldown"] = 0.0
            game.add_target(enemy, on_hit=self.on_shot) 
            self.enemies.append(enemy)

    def update(self, game: FPSGame, dt: float) -> None:
        for enemy in self.enemies:
            enemy.data["attack_cooldown"] = max(0.0, enemy.data["attack_cooldown"] - dt)

            if game.can_see(enemy, game.player) and game.distance_to_player(enemy) > 1.0:
                enemy.move_towards(game.player.x, game.player.z, speed=1.4, dt=dt)

            if game.near_player(enemy, 1.1) and enemy.data["attack_cooldown"] <= 0.0:
                game.damage_player(12)
                enemy.data["attack_cooldown"] = 0.9

    def on_shot(self, enemy: GameObject, damage: int) -> None:
        game = self.game
        enemy.data["hp"] -= damage
        if enemy.data["hp"] > 0:
            return

        game.spawn_particles(enemy.x, 1.0, enemy.z, color=(255, 120, 40), count=16, speed=4.0)
        enemy.remove()
        self.enemies.remove(enemy)
        game.score += 100
        game.emit("enemy_defeated", {"remaining": len(self.enemies)})
        if not self.enemies:
            game.win("EZLOL")
