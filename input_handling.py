import tcod


def handle_keys(key):
    # Movement keys
    if key.vk == tcod.KEY_RIGHT:
        return {"move": (1, 0)}
    elif key.vk == tcod.KEY_LEFT:
        return {"move": (-1, 0)}
    elif key.vk == tcod.KEY_UP:
        return {"move": (0, -1)}
    elif key.vk == tcod.KEY_DOWN:
        return {"move": (0, 1)}

    # Other keys
    if key.vk == tcod.KEY_ENTER and tcod.KEY_ALT:
        # Alt+Enter: toggle fullscreen
        return {"fullscreen": True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit
        return {"exit": True}

    # No key pressed
    return {}
