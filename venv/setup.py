from pygame import display
display.init()
window = display.set_mode((1280, 720))
display.set_caption("Jumpy Shoot!")
# This is used to create the display


def update():
    display.flip()

