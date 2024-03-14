SCREEN_HEIGHT     = 720
SCREEN_WIDTH      = 1280
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60
SIMULATION_RUNTIME = 1000000 # in seconds
USE_GUI = True

PLANE_POLIKARPOV_I_16 = {
    "SPRITE" : "assets/sprite_republican_i16.png", 
    "MASS" : 1200,
    "ENGINE_FORCE" : 300,
    "AGILITY" : 100, 
    "C_DRAG" : 0.5,
    "C_LIFT" : 30,
    "AOA_CRIT_LOW" : (-15.0, -0.95),
    "AOA_CRIT_HIGH" : (19.0, 1.4),
    "CL0" : 0.32,
    "CD_MIN" : 0.5,
    "INIT_THROTTLE" : 100,
    "INIT_PITCH" : 0, 
    "INIT_V" : (100.0, 0.0),
    "INIT_POS" : (SCREEN_WIDTH / 2, 200),
    "SIZE" : (24,13)
}

BALLOON = {
    "SPRITE" : "assets/apple.gif",
    "SPRITES" : [
        "assets/finn_zoom.png",
        "assets/5g_joris.png",
        "assets/5g_nick.png",
        "assets/5g_max.png",
        "assets/hu_bas.png",
        "assets/joris_zoom.png",
        "assets/joris.png",
        "assets/cool_joost.png",
        "assets/max.png",
        "assets/igor.png",
        "assets/apple.gif"
    ],
    "SIZE" : 20,
    "BALLOON_COUNT" : 10
}

BULLET = {
    "SPRITE" : "assets/bullet.png",
    "LIFETIME" : .66,
    "SIZE" : 5,
    "SPEED": 10
}

