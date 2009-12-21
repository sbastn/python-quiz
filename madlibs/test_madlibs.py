import unittest
import re

def extract(story):
    vars = re.findall('\(\(.*:.*?\)\)', story)
    vars = map(lambda x: x.split(':')[0][2:], vars)

    match = re.findall('\(\(.*?\)\)', story)

    match = map(lambda x: x[2:-2], match)
    for m in match:
        for v in vars:
            if m == v:
                match.remove(m)

    match = map(lambda x: x.split(':')[1] if len(x.split(':')) > 1 else x, match)

    return match

def replace(placeholders, story):
    for token in placeholders.keys():
        story = re.sub('\(\(' + token + '\)\)', placeholders[token], story)

    return story

class TestMadLibs(unittest.TestCase):
    def setUp(self):
        self.story = "I had a ((an adjective)) sandwich for lunch today. It dripped all over my ((a body part)) and ((a noun))."
        
    def test_extract_questions_from_story(self):
        self.assertEquals(['an adjective', 'a body part', 'a noun'], extract(self.story))
        
    def test_feed_answers_to_story(self):
        placeholders = {'an adjective': 'smelly', 'a body part': 'toes', 'a noun': 'bathtub'}
        expected_story = "I had a smelly sandwich for lunch today. It dripped all over my toes and bathtub."
        self.assertEquals(expected_story, replace(placeholders, self.story))

    def test_extract_reusable_variables_from_story(self):
        story = "Our favorite language is ((animal:an animal)). We think ((animal)) is better than ((an animal))."
        self.assertEquals(['an animal', 'an animal'], extract(story))
        

