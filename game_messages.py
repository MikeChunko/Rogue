import tcod
import textwrap


class Message:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Split the message if needed
        wrapped_message = textwrap.wrap(message.text, self.width)

        for line in wrapped_message:
            # Removes the oldest message if the display is filled
            if len(self.messages) == self.height:
                del self.messages[0]

            self.messages.append(Message(line, message.color))
