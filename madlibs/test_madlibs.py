import unittest
import re

def extract(story):
    """ extract placeholders from a story"""
    variables = find_reusable_variables(story)
    placeholders = find_placeholders(story)
    return remove_variables_from_placeholders(placeholders, variables)

def find_reusable_variables(story):
    """ returns a collection of reusable variables in a story
    from ((animal: an animal)) it returns ['animal']
    """
    vars = re.findall('\(\(.*:.*?\)\)', story)
    return map(lambda x: x.split(':')[0][2:], vars)

def find_placeholders(story):
    """ returns a collections of placeholders.
    from 'Hello ((an animal)), you are ((a color))'
    it returns ['((an animal))', '((a color))']
    """
    return re.findall('\(\(.*?\)\)', story)

def remove_variables_from_placeholders(match, variables):
    """ filters out the reusable variables from the placeholders 
    from ['((animal: an animal))', '((animal))', '((a color))']
    it returns ['an animal', 'a color']
    """
    match = map(lambda x: x[2:-2], match)
    for m in match:
        for v in variables:
            if m == v:
                match.remove(m)

    return  map(lambda x: x.split(':')[1] if len(x.split(':')) > 1 else x, match)

def replace(answers, story):
    variables = find_reusable_variables(story)
    placeholders = find_placeholders(story)

    # simple case with no vars
    for answer in answers.keys():
        found = False
        for token in placeholders:
            if token[2:-2] == answer:
                found = True
                story = re.sub('\(\(' + answer + '\)\)', answers[answer], story)

        # search and replace placeholders with vars
        if not found:
            token_with_vars = filter(lambda x: x if len(x.split(':')) > 1 else None, placeholders)
            for var_token in token_with_vars:
                var = re.split(':', var_token)[0][2:]
                story = re.sub('\(\(' + var + '\)\)', answers[answer], story)
                story = re.sub('\(\(' + var_token + '\)\)', answers[answer], story)
                
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
        story = "Our favorite animal is ((animal:an animal)). We think ((animal)) is better than ((another animal))."
        self.assertEquals(['an animal', 'another animal'], extract(story))
        
    def test_feed_answers_to_story_with_reusable_variables(self):
        story = "Our favorite animal is a ((animal:an animal)). We think a ((animal)) is better than a ((another animal))."
        placeholders = {'an animal': 'python', 'another animal': 'unicorn'}
        expected_story = "Our favorite animal is a python. We think a python is better than a unicorn."
        self.assertEquals(expected_story, replace(placeholders, story))
