from minipy3dr.fps import FPSConfig

CONFIG = FPSConfig(
    # 画面
    screen_size=(960, 600),
    render_scale=0.6,  
    fov=78.0, 
    walk_speed=4.2,
    sprint_speed=6.0,  # Shift押下時の速度
    mouse_look=True,  # トラックパッド環境ならFalse
    max_health=100,
    start_ammo=40,
    # 見 た目のテーマ
    floor_colors=((207, 237, 240), (207, 237, 240)),
    wall_colors=((238, 213, 255), (238, 213, 255)),
    lamp_color=(238, 213, 255),
)
