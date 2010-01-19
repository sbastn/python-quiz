import unittest

SPACE = ' '
PIPE  = '|'
DASH  = '-'
TEMPLATE = ' %s\n%s %s\n %s\n%s %s\n %s\n'

numbers = {
    0: [DASH, PIPE, PIPE, SPACE, PIPE, PIPE, DASH],
    1: [SPACE, SPACE, PIPE, SPACE, SPACE, PIPE, SPACE],
    2: [DASH, SPACE, PIPE, DASH, PIPE, SPACE, DASH],
    3: [DASH, SPACE, PIPE, DASH, SPACE, PIPE, DASH],
}

def lcd(n):
    num =  '%s\n' % display(n, section=[0])
    num += '%s\n' % display(n, section=[1, 2])
    num += '%s\n' % display(n, section=[3])
    num += '%s\n' % display(n, section=[4, 5])
    num += '%s\n' % display(n, section=[6])
    return num

def display(n, section):
    num = ''
    for s in section:
        if s in [1, 4]:
            num += '%s' % numbers[n][s]
        else:
            num += ' %s' % numbers[n][s]
    return num

class TestLCDWithSingleNumberSingleSize(unittest.TestCase):
    def test_display_zero(self):
        expected_result = TEMPLATE % (DASH, PIPE, PIPE, SPACE, PIPE, PIPE, DASH)
        self.assertEquals(expected_result, lcd(0))
    
    def test_display_one(self):
        expected_result = TEMPLATE % (SPACE, SPACE, PIPE, SPACE, SPACE, PIPE, SPACE) 
        self.assertEquals(expected_result, lcd(1))
        
    def test_display_two(self):
        expected_result = TEMPLATE % (DASH, SPACE, PIPE, DASH, PIPE, SPACE, DASH)
        self.assertEquals(expected_result, lcd(2))

    def test_display_three(self):
        expected_result = TEMPLATE % (DASH, SPACE, PIPE, DASH, SPACE, PIPE, DASH)
        self.assertEquals(expected_result, lcd(3))
        
class TestLCDWithMultipleNumbersSingleSize(unittest.TestCase):
    def test_display_zero_and_one(self):
        pass

if __name__ == '__main__':
    print lcd(2)
