from game.features.enemies import Enemies
from game.features.hud import Hud
from game.features.items import Items
from game.features.sound import Sound
from game.features.weapons import Weapons

FEATURES = [
    Enemies(),  # 敵担当:
    Weapons(),  # 武器担当:
    Items(),    # アイテム担当:
    Hud(),      # HUD担当:
    Sound(),    # サウンド・演出担当:
]
