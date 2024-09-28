import unittest

from botfirm.helper.prompts.parser.line_parse import LineParse

class TestLineParser(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = """A
B

1

2
3
4
"""
        return super().setUp()

    def test_parsing_with_empty_line(self):
        all_lines = []
        first = True
        for l in LineParse(self.test_data):
            if first:
                self.assertEqual("A", l)
                first = False
            all_lines.append(l)
        self.assertEqual(9, len(all_lines))
        self.assertEqual("1", all_lines[3])

    def test_parsing_without_empty(self):
        all_lines = [l for l in LineParse(self.test_data, skip_empty=True)]
        self.assertEqual(6, len(all_lines))
        self.assertEqual("2", all_lines[3])
