import unittest
from hw4.server import manage_msg
from hw4.utilities import load_configs


class TestServer(unittest.TestCase):
    CONFIGS = load_configs(True)

    err_msg = {
        CONFIGS['RESPONSE']: 400,
        CONFIGS['ERROR']: 'Bad Request'
    }

    success_msg = {CONFIGS['RESPONSE']: 200}

    def test_no_action(self):
        self.assertEqual(
            manage_msg({
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }, self.CONFIGS),
            self.err_msg
        )

    def test_no_time(self):
        self.assertEqual(
            manage_msg({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }, self.CONFIGS),
            self.err_msg
        )

    def test_wrong_user(self):
        self.assertEqual(
            manage_msg({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'gest'
                }
            }, self.CONFIGS),
            self.err_msg
        )

    def test_successful_check(self):
        self.assertEqual(
            manage_msg({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: 1.1,
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }, self.CONFIGS),
            self.success_msg
        )


if __name__ == '__main__':
    unittest.main()
