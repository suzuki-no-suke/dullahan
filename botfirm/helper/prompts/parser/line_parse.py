

class LineParse:
    def __init__(self, lines, skip_empty=False):
        self.lines = lines
        self.index = 0
        self.split_lines = [line.strip() for line in lines.split('\n')]

        if skip_empty:
            self.split_lines = list(filter(lambda x: x, self.split_lines))

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.split_lines):
            result = self.split_lines[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
