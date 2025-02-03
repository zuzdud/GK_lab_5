#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from cmath import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0

pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
R = 6.0

# składowe koloru materiału
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 10.0  # stopień połyskliwości materiału

light_option = 1
# kolor źródła światła
light_ambient = [0, 0, 0, 1.0]
light_diffuse = [0.5, 0.5, 0.5, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, -20.0, 0.0, 1.0]  # położenie źródła światła

# otaczające kolor cieni mniej więcej
# zwiększenie wartości to ciemniejsze stają sie jasniejsze i przyjmuja ten odcien
# nisko to scena kontrastowa, głębokie cienie
light1_ambient = [0.1, 0.1, 0.1, 1.0]

# rozproszone
# więcej to silniejszy odcień oswietlonych fragmentow
light1_diffuse = [0.96, 0.7, 0.16, 1.0]

# odbite kierunkowe
# refleksy danego koloru
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [0.0, 12.0, 0.0, 1.0]

# składowe funkcji strat natężenia
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # uaktywnienie modelu oświetlenia
    # definiowanie parametrów modelu
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    # jak jest v na końcu znaczy że wektor
    # jak wektor to 4 elementowa tablica
    # bo wektor normalizowany czy cus

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    # włączenie modelu oświetlenia
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global light_position
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


    # rysowanie sfery z bib glu
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle *0.5
        phi += delta_y * piy2angle * 0.5

    # glRotatef(theta, 0.0, 1.0, 0.0)
    # glRotatef(phi, 1.0, 0.0, 0.0)

    xs = R * cos(2*pi*theta/360) * cos(2*pi*phi/360)
    ys = R * sin(2*pi*phi/360)
    zs = R * sin(2*pi*theta/360) * cos(2*pi*phi/360)
    glTranslate(xs.real, ys.real, zs.real)
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.5, 20, 20)
    gluDeleteQuadric(quadric)

    light_position[0] = xs.real
    light_position[1] = ys.real
    light_position[2] = zs.real

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # wszytskie kolory będą wynikały z modelu obliczeniowego
    # więc wywołania glColor mamy w dupie

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global light_ambient
    global light_diffuse
    global light_option
    global light_specular
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    # wybór składowej
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        light_option = 1

    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        light_option = 2

    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        light_option = 3

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS and light_option == 1:
        if light_ambient[0] >= 0.1 and light_ambient[1] >= 0.1 and light_ambient[2] >= 0.1:
            light_ambient[0] -= 0.1
            light_ambient[1] -= 0.1
            light_ambient[2] -= 0.1
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    if key == GLFW_KEY_UP and action == GLFW_PRESS and light_option == 1:
        if light_ambient[0] <= 0.9 and light_ambient[1] <= 0.9 and light_ambient[2] <= 0.9:
            light_ambient[0] += 0.1
            light_ambient[1] += 0.1
            light_ambient[2] += 0.1
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS and light_option == 2:
        if light_diffuse[0] >= 0.1 and light_diffuse[1] >= 0.1 and light_diffuse[2] >= 0.1:
            light_diffuse[0] -= 0.1
            light_diffuse[1] -= 0.1
            light_diffuse[2] -= 0.1
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

    if key == GLFW_KEY_UP and action == GLFW_PRESS and light_option == 2:
        if light_diffuse[0] <= 0.9 and light_diffuse[1] <= 0.9 and light_diffuse[2] <= 0.9:
            light_diffuse[0] += 0.1
            light_diffuse[1] += 0.1
            light_diffuse[2] += 0.1
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS and light_option == 3:
        if light_specular[0] >= 0.1 and light_specular[1] >= 0.1 and light_specular[2] >= 0.1:
            light_specular[0] -= 0.1
            light_specular[1] -= 0.1
            light_specular[2] -= 0.1
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    if key == GLFW_KEY_UP and action == GLFW_PRESS and light_option == 3:
        if light_specular[0] <= 0.9 and light_specular[1] <= 0.9 and light_specular[2] <= 0.9:
            light_specular[0] += 0.1
            light_specular[1] += 0.1
            light_specular[2] += 0.1
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
