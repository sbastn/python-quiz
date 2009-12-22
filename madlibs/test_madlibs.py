import unittest
from madlibs import MadLibs


class TestSimplePlaceholders(unittest.TestCase):

    def setUp(self):
        story = "I had a ((an adjective)) sandwich for lunch today. It dripped all over my ((a body part)) and ((a noun))."
        self.madLibs = MadLibs(story)

    def test_extract_questions_from_story(self):
        self.assertEquals(['an adjective', 'a body part', 'a noun'], self.madLibs.questions)
        
    def test_feed_answers_to_story(self):
        answers = {'an adjective': 'smelly', 'a body part': 'toes', 'a noun': 'bathtub'}
        expected_story = "I had a smelly sandwich for lunch today. It dripped all over my toes and bathtub."
        self.assertEquals(expected_story, self.madLibs.tell_story(answers))

class TestVariablePlaceholders(unittest.TestCase):

    def setUp(self):
        story = "Our favorite animal is a ((animal:an animal)). We think a ((animal)) is better than a ((another animal))."
        self.madLibs = MadLibs(story)

    def test_extract_reusable_variables_from_story(self):
        self.assertEquals(['an animal', 'another animal'], self.madLibs.questions)
        
    def test_feed_answers_to_story_with_reusable_variables(self):
        answers = {'an animal': 'python', 'another animal': 'unicorn'}
        expected_story = "Our favorite animal is a python. We think a python is better than a unicorn."
        self.assertEquals(expected_story, self.madLibs.tell_story(answers))
