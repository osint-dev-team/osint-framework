import unittest

from src.scripts.convert.phone_num_generator import module
from .module import Runner


class Test(unittest.TestCase):

    def setUp(self):
        self.runner = module.Runner()

    def test_num_1(self):
        runner = Runner()
        response = runner.run(phone="+442083661177", region=None)
        self.assertIn("020-8366-1177", response.get('result'))

    def test_num_2(self):
        runner = Runner()
        response = runner.run(phone="8137777777", region="RU")
        self.assertIn("+7-813-777-77-77", response.get('result'))


if __name__ == '_main_':
    unittest.main()
