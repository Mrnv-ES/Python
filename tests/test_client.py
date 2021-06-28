import unittest
from hw4.client import make_presence_msg, manage_response
from hw4.utilities import load_configs


class TestClass(unittest.TestCase):
    CONFIGS = load_configs

    def test_presence(self):
        test = make_presence_msg('Guest', CONFIGS=self.CONFIGS)
        test[self.CONFIGS['TIME']] = 1.1
        self.assertEqual(
            test,
            {
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: 1.1,
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }
        )

    def test_correct_answer(self):
        self.assertEqual(
            manage_response({self.CONFIGS['RESPONSE']: 200}, self.CONFIGS),
            '200 : OK'
        )

    def test_bad_request(self):
        self.assertEqual(
            manage_response({
                self.CONFIGS['RESPONSE']: 400,
                self.CONFIGS['ERROR']: 'Bad Request'
            }, self.CONFIGS),
            '400 : Bad Request'
        )

    def test_no_response(self):
        self.assertRaises(
            ValueError,
            manage_response,
            {self.CONFIGS['ERROR']: 'Bad Request'},
            self.CONFIGS
        )


if __name__ == '__main__':
    unittest.main()
