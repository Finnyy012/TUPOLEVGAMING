SCREEN_HEIGHT     = 720
SCREEN_WIDTH      = 1280
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60
SIMULATION_RUNTIME = 10000 # in seconds
USE_GUI = True

PLANE_POLIKARPOV_I_16 = {
    "SPRITE" : "assets/sprite_republican_i16.png", 
    "MASS" : 1200,
    "ENGINE_FORCE" : 300,
    "AGILITY" : 100, 
    "C_DRAG" : 0.5,
    "C_LIFT" : 15,
    "AOA_CRIT_LOW" : (-15.0, -0.95),
    "AOA_CRIT_HIGH" : (19.0, 1.4),
    "CL0" : 0.32,
    "CD_MIN" : 0.5,
    "INIT_THROTTLE" : 100,
    "INIT_PITCH" : 0, 
    "INIT_V" : (100.0, 0.0),
    "INIT_POS" : (SCREEN_WIDTH / 2, 200)
}
