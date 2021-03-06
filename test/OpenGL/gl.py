from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
print('imported')

def showScreen():
    # Remove everything from screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

# Initialize a glut instance
glutInit()

#Set display mode to be colored
glutInitDisplayMode(GLUT_RGBA)

# Set width and height of window
glutInitWindowSize(500, 500)

# Set position at which the window should appear
glutInitWindowPosition(0, 0)

# Assign title
wind = glutCreateWindow("OpenGL First")

# Call showScreen method continuously
glutDisplayFunc(showScreen)

# Draw any graphics or shapes in the showScreen func at all times
glutIdleFunc(showScreen)

# Keeps the window created above displaying/running in a loop
glutMainLoop()
