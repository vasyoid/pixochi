from django.db import models
import time

from rest_framework.renderers import JSONRenderer

from api.exception import NameOccupiedError, PixochiNotFoundError, PixochiDeadError
from api.serializer import PixochiStateResponseSerializer


class NewPixochiRequest:
    def __init__(self, name, eyes, filling):
        self.name = name
        self.eyes = eyes
        self.filling = filling


class PixochiStateResponse:
    def __init__(self, state, pic):
        self.state = state
        self.pic = pic


def time_ms():
    return time.time_ns() // 1000000


class Pixochi(models.Model):
    _STATE_CHANGE_FREQUENCY = 1000 * 60 * 10

    STATES = (
        (3, 'normal'),
        (2, 'sad'),
        (1, 'hungry'),
        (0, 'dead'),
    )

    name = models.CharField(max_length=50, primary_key=True)
    eyes = models.IntegerField()
    style = models.CharField(max_length=1)
    state = models.IntegerField(choices=STATES, default=3)
    frequency = models.IntegerField(choices=STATES, default=_STATE_CHANGE_FREQUENCY)
    lastStateChange = models.IntegerField(default=time_ms)

    def update_state(self):
        interval = time_ms() - self.lastStateChange
        while self.state and interval >= self.frequency:
            interval -= self.frequency
            self.state -= 1
            self.lastStateChange += self.frequency
        self.save()

    def get_my_state(self):
        self.update_state()
        return self.get_state_display()

    def draw(self):
        char = self.style
        eyes = self.eyes
        eyes_len = (eyes * 2 - 1) * 3
        state = self.get_state_display()
        return (
          f"  {char * eyes_len}\n"
          f" {char}{' ' * eyes_len}{char}\n"
          f"{char} {eye_top(char, state)}{f'   {eye_top(char, state)}' * (eyes - 1)} {char}\n" 
          f"{char} {eye_middle(char, state)}{f'   {eye_middle(char, state)}' * (eyes - 1)} {char}\n" 
          f"{char} {eye_bottom(char, state)}{f'   {eye_bottom(char, state)}' * (eyes - 1)} {char}\n" 
          f" {char}{' ' * eyes_len}{char}\n"
          f"  {char}{' ' * ((eyes_len - 5) // 2)}{char * 3}{' ' * ((eyes_len - 5) // 2)}{char}\n"
          f"   {char}{' ' * (eyes_len - 4)}{char}\n"
          f"    {char * (eyes_len - 4)}\n"
        )

    def get_state_as_json(self):
        response = PixochiStateResponse(self.get_my_state(), self.draw())
        serializer = PixochiStateResponseSerializer(response)
        return JSONRenderer().render(serializer.data)

    def nurse(self):
        cur_state = self.get_my_state()
        if cur_state == 'dead':
            raise PixochiDeadError()
        if cur_state != 'normal':
            self.state += 1
            self.lastStateChange = time_ms()

    @staticmethod
    def create(name, eyes, style, frequency=_STATE_CHANGE_FREQUENCY, state=3):
        if Pixochi.objects.filter(pk=name).exists():
            raise NameOccupiedError()
        return Pixochi.objects.create(name=name, eyes=eyes, style=style, frequency=frequency, state=state)

    @staticmethod
    def get(name):
        found = Pixochi.objects.filter(pk=name)
        if not found.exists():
            raise PixochiNotFoundError()
        return found.get()


def eye_top(char, state):
    if state == 'normal':
        return f' {char} '
    elif state == 'sad':
        return '   '
    elif state == 'hungry':
        return char * 3
    else:
        return f'{char} {char}'


def eye_middle(char, state):
    if state == 'normal':
        return f'{char} {char}'
    elif state == 'sad':
        return char * 3
    elif state == 'hungry':
        return f'{char} {char}'
    else:
        return f' {char} '


def eye_bottom(char, state):
    if state == 'normal':
        return f' {char} '
    elif state == 'sad':
        return f' {char} '
    elif state == 'hungry':
        return char * 3
    else:
        return f'{char} {char}'
