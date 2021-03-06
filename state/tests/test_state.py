import datetime
import json
import pymongo
import unittest

from state.state import *


class TestCommunicate(unittest.TestCase):

    # static
    with open('grows.json', 'r') as g:
        g = json.load(g)
    with open('data.json', 'r') as d:
        d = json.load(d)

    def test_grows_returns_cursor(self):
        grows = connect_grows()
        self.assertIsNotNone(grows)
        self.assertIsInstance(grows, pymongo.cursor.Cursor)

    def test_data_returns_dict(self):
        d_id = device_id(self.g)
        g_name = grow_name(self.g)
        data = connect_data(d_id, g_name)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_device_id_str(self):
        g_id = device_id(self.g)
        self.assertIsNotNone(g_id)
        self.assertIsInstance(g_id, str)
        d_id = device_id(self.d)
        self.assertIsNotNone(d_id)
        self.assertIsInstance(d_id, str)

    def test_grow_name(self):
        g_name = grow_name(self.g)
        self.assertIsNotNone(g_name)
        self.assertIsInstance(g_name, str)

    def test_actuator_pin(self):
        self.assertEquals('30', actuator_pin(self.g, 'light_1'))
        with self.assertRaises(KeyError):
            actuator_pin(self.g, 'hydrobase')

    def test_controls_dates(self):
        c = {"dates" : {"start" : "01/01/2016", "end" : "12/31/2016"}}
        self.assertEquals(2, len(controls_dates(c)))
        s, e = controls_dates(c)
        self.assertTrue(s < e)
        self.assertTrue(type(s) is type(e))
        c = {"dates" : {}}
        self.assertEquals((None, None), controls_dates(c))

    def test_controls_time_list(self):
        time = controls_time(self.g)
        self.assertIsNotNone(time)
        self.assertIsInstance(time, list)

    def test_controls_condition_list(self):
        condition = controls_condition(self.g)
        self.assertIsNotNone(condition)
        self.assertIsInstance(condition, list)

    def test_current_time(self):
        h = current_time('hours')
        self.assertIsInstance(h, int)
        self.assertTrue(0 <= h <= 23)
        m = current_time('minutes')
        self.assertIsInstance(m, int)
        self.assertTrue(0 <= m <= 59)

    def test_is_odd(self):
        self.assertEquals(False, is_odd(2))
        self.assertEquals(True, is_odd(3))

    def test_time_based_on(self):
        # value depends on `current_time()`
        unit, hour, action = 'hours', 4, 'toggle'
        tbo = time_based_on(unit, hour, action)
        self.assertIsNotNone(tbo)
        self.assertIsInstance(tbo, bool)

    def test_condition_based_on(self):
        self.assertEquals(True, condition_based_on(5, '>', 3))
        self.assertEquals(False, condition_based_on(5, '<', 3))

    def test_n_values(self):
        obj = {'one' : 1, 'two' : 2}
        one, two = n_values(obj, ['one', 'two'])
        self.assertEquals(1, one)
        self.assertEquals(2, two)
        tuple_one = n_values(obj, ['one'])
        self.assertIsInstance(tuple_one, tuple)
        with self.assertRaises(KeyError):
            n_values(obj, ['three'])
        with self.assertRaises(AssertionError):
            n_values('not_a_dict', ['one'])
        with self.assertRaises(AssertionError):
            n_values(obj, 'one')

    def test_pin_and_value(self):
        c0 = controls_time(self.g)[0]
        self.assertIsInstance(pin_and_value(self.g, c0, 'time'), tuple)

    def test_payload(self):
        p_time = payload(self.g, 'time')
        self.assertIsInstance(p_time, dict)
        p_cond = payload(self.g, 'condition')
        self.assertIsInstance(p_cond, dict)
