import time

from django.test import TestCase

from api.exception import NameOccupiedError, PixochiNotFoundError, PixochiDeadError
from api.models import Pixochi


_TEST_STATE_UPDATE_FREQUENCY = 100
_TEST_STATE_UPDATE_FREQUENCY_SEC = 0.1


class PixochiCreateTestCase(TestCase):

    def test_create_simple(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='*')
        self.assertEqual('pix1', pixochi.name)
        self.assertEqual(2, pixochi.eyes)
        self.assertEqual('*', pixochi.style)
        self.assertEqual('normal', pixochi.get_state_display())

    def test_name_occupied(self):
        Pixochi.create(name='pix1', eyes=2, style='*')
        self.assertRaises(NameOccupiedError, Pixochi.create, name='pix1', eyes=3, style='!')

    def test_create_multiple(self):
        try:
            Pixochi.create(name='pix1', eyes=2, style='*')
            Pixochi.create(name='pix2', eyes=2, style='**')
        except:
            self.fail()


class PixochiGetTestCase(TestCase):

    def setUp(self):
        Pixochi.create(name='pix1', eyes=2, style='*')

    def test_get_simple(self):
        pixochi = Pixochi.get('pix1')
        self.assertEqual('pix1', pixochi.name)
        self.assertEqual(2, pixochi.eyes)
        self.assertEqual('*', pixochi.style)

    def test_get_not_found(self):
        self.assertRaises(PixochiNotFoundError, Pixochi.get, 'pix2')


class PixochiUpdateStateTestCase(TestCase):
    def setUp(self):
        self._pixochi = Pixochi.create(name='pix1', eyes=2, style='*', frequency=_TEST_STATE_UPDATE_FREQUENCY)
        time.sleep(_TEST_STATE_UPDATE_FREQUENCY_SEC / 2)

    def test_state_normal(self):
        self.assertEqual('normal', self._pixochi.get_my_state())

    def test_state_sad(self):
        time.sleep(_TEST_STATE_UPDATE_FREQUENCY_SEC)
        self.assertEqual('sad', self._pixochi.get_my_state())

    def test_state_hungry(self):
        time.sleep(_TEST_STATE_UPDATE_FREQUENCY_SEC * 2)
        self.assertEqual('hungry', self._pixochi.get_my_state())

    def test_state_dead(self):
        time.sleep(_TEST_STATE_UPDATE_FREQUENCY_SEC * 3)
        self.assertEqual('dead', self._pixochi.get_my_state())


class PixochiNurseStateTestCase(TestCase):

    def test_nurse_normal(self):
        self._pixochi = Pixochi.create(name='pix1', eyes=2, style='*', state=3)
        self.assertEqual('normal', self._pixochi.get_state_display())

    def test_nurse_hungry(self):
        self._pixochi = Pixochi.create(name='pix1', eyes=2, style='*', state=1)
        self._pixochi.nurse()
        self.assertEqual('sad', self._pixochi.get_state_display())

    def test_nurse_dead(self):
        self._pixochi = Pixochi.create(name='pix1', eyes=2, style='*', state=0)
        self.assertRaises(PixochiDeadError, self._pixochi.nurse)


class PixochiDrawTestCase(TestCase):

    def test_draw_normal(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='█', state=3)
        pic = (
            f"  █████████\n"
            f" █         █\n"
            f"█  █     █  █\n"
            f"█ █ █   █ █ █\n"
            f"█  █     █  █\n"
            f" █         █\n"
            f"  █  ███  █\n"
            f"   █     █\n"
            f"    █████\n"
        )
        self.assertEqual(pic, pixochi.draw())

    def test_draw_sad(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='█', state=2)
        pic = (
            f"  █████████\n"
            f" █         █\n"
            f"█           █\n"
            f"█ ███   ███ █\n"
            f"█  █     █  █\n"
            f" █         █\n"
            f"  █  ███  █\n"
            f"   █     █\n"
            f"    █████\n"
        )
        self.assertEqual(pic, pixochi.draw())

    def test_draw_hungry(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='█', state=1)
        pic = (
            f"  █████████\n"
            f" █         █\n"
            f"█ ███   ███ █\n"
            f"█ █ █   █ █ █\n"
            f"█ ███   ███ █\n"
            f" █         █\n"
            f"  █  ███  █\n"
            f"   █     █\n"
            f"    █████\n"
        )
        self.assertEqual(pic, pixochi.draw())

    def test_draw_dead(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='█', state=0)
        pic = (
            f"  █████████\n"
            f" █         █\n"
            f"█ █ █   █ █ █\n"
            f"█  █     █  █\n"
            f"█ █ █   █ █ █\n"
            f" █         █\n"
            f"  █  ███  █\n"
            f"   █     █\n"
            f"    █████\n"
        )
        self.assertEqual(pic, pixochi.draw())

    def test_draw_3_eyes(self):
        pixochi = Pixochi.create(name='pix1', eyes=3, style='█', state=3)
        pic = (
            f"  ███████████████\n"
            f" █               █\n"
            f"█  █     █     █  █\n"
            f"█ █ █   █ █   █ █ █\n"
            f"█  █     █     █  █\n"
            f" █               █\n"
            f"  █     ███     █\n"
            f"   █           █\n"
            f"    ███████████\n"
        )
        self.assertEqual(pic, pixochi.draw())

    def test_draw_style(self):
        pixochi = Pixochi.create(name='pix1', eyes=2, style='*', state=3)
        pic = (
            f"  *********\n"
            f" *         *\n"
            f"*  *     *  *\n"
            f"* * *   * * *\n"
            f"*  *     *  *\n"
            f" *         *\n"
            f"  *  ***  *\n"
            f"   *     *\n"
            f"    *****\n"
        )
        self.assertEqual(pic, pixochi.draw())

