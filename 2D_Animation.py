import glfw
from OpenGL.GL import *
import numpy as np
import time
import sys

# Global variables
wind = 0.0
wind_speed = 0.003
day_night = 0.7
rain_speed = 0.015
rain_drops = []
POINT_SIZE = 3.0

# Initialize rain particles

def init_rain_drops(num_drops=200):
    global rain_drops
    rain_drops = [(np.random.uniform(-1, 1),
                   np.random.uniform(-1, 1)) for _ in range(num_drops)]

# Draw a house
def draw_house():
    # Roof
    glColor3f(0.6, 0.25, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.3, -0.3)
    glVertex2f(0.3, -0.3)
    glVertex2f(0.0, 0.2)
    glEnd()

    # Walls
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_LINES)
    glVertex2f(-0.25, -0.3); glVertex2f(-0.25, -0.7)
    glVertex2f(0.25, -0.3); glVertex2f(0.25, -0.7)
    glVertex2f(-0.25, -0.7); glVertex2f(0.25, -0.7)
    glEnd()

    # Door
    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-0.08, -0.7); glVertex2f(-0.08, -0.5)
    glVertex2f(-0.08, -0.5); glVertex2f(0.08, -0.5)
    glVertex2f(0.08, -0.5); glVertex2f(0.08, -0.7)
    glEnd()

    # Window
    glColor3f(0.2, 0.6, 1.0)
    glBegin(GL_LINES)
    glVertex2f(0.12, -0.4); glVertex2f(0.12, -0.5)
    glVertex2f(0.05, -0.4); glVertex2f(0.05, -0.5)
    glVertex2f(0.05, -0.45); glVertex2f(0.12, -0.45)
    glEnd()

# Draw RED rain
def draw_rain():
    global rain_drops, wind, rain_speed

    glColor3f(1.0, 0.0, 0.0)  # RED
    glPointSize(POINT_SIZE)
    glBegin(GL_POINTS)

    for i, (x, y) in enumerate(rain_drops):
        new_x = x + wind
        glVertex2f(new_x, y)

        # update
        x += wind
        y -= rain_speed

        if y < -1:
            x = np.random.uniform(-1, 1)
            y = 1

        rain_drops[i] = (x, y)

    glEnd()

# Keyboard controls
def key_callback(window, key, scancode, action, mods):
    global wind, wind_speed, day_night, rain_speed

    if action == glfw.PRESS or action == glfw.REPEAT:

        # Wind movement
        if key == glfw.KEY_LEFT:
            wind -= wind_speed
        elif key == glfw.KEY_RIGHT:
            wind += wind_speed
        elif key == glfw.KEY_R:
            wind = 0

        # Wind speed control
        elif key == glfw.KEY_W:
            wind_speed = min(wind_speed + 0.001, 0.02)
        elif key == glfw.KEY_S:
            wind_speed = max(wind_speed - 0.001, 0.001)

        # Day–Night cycle
        elif key == glfw.KEY_UP:
            day_night = min(1.0, day_night + 0.05)
        elif key == glfw.KEY_DOWN:
            day_night = max(0.0, day_night - 0.05)

        # Rain speed control
        elif key == glfw.KEY_EQUAL or key == glfw.KEY_KP_ADD:
            rain_speed = min(rain_speed + 0.005, 0.05)
        elif key == glfw.KEY_MINUS or key == glfw.KEY_KP_SUBTRACT:
            rain_speed = max(rain_speed - 0.005, 0.002)

# Start window + animation
def start(width=720, height=600, title="Red Rain Animation"):
    if not glfw.init():
        print("GLFW initialization failed.")
        return

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        print("Window creation failed.")
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    init_rain_drops()
    glEnable(GL_POINT_SMOOTH)
    glPointSize(POINT_SIZE)

    print("Animation started. Close window to exit.")

    while not glfw.window_should_close(window):

        sky_r = day_night * 0.4
        sky_g = day_night * 0.6
        sky_b = day_night * 1.0

        glClearColor(sky_r, sky_g, sky_b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        draw_house()
        draw_rain()

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.01)

    glfw.terminate()
start()


