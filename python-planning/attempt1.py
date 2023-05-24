#!/usr/bin/python3

"""
the first attempt at writing a wave function collapse algorithm
in order to do it better later
"""

from collections import defaultdict
import random


class WaveFunctionCollapse:
    """
    Wave Function Collapse (WFC) algorithm implementation.

    Attributes:
        patterns_dict (dict): Dictionary to store the patterns and their frequencies.
        adjacency_dict (dict): Dictionary to store the adjacency between patterns.
        input_width (int): Width of the input pattern.
        input_height (int): Height of the input pattern.
        output_width (int): Width of the output pattern.
        output_height (int): Height of the output pattern.
    """

    def __init__(self, pattern, output_width, output_height):
        """
        Initialize the WaveFunctionCollapse object.

        Args:
            pattern (list): 2D array of length 1 strings representing the input pattern.
            output_width (int): Width of the output pattern.
            output_height (int): Height of the output pattern.
        """
        self.patterns_dict = defaultdict(int)
        self.adjacency_dict = defaultdict(lambda: defaultdict(int))
        self.input_width = len(pattern[0])
        self.input_height = len(pattern)
        self.output_width = output_width
        self.output_height = output_height
        self._learn_pattern(pattern)

    def _learn_pattern(self, pattern):
        """
        Learn the patterns and their adjacency from the input pattern.

        Args:
            pattern (list): 2D array of length 1 strings representing the input pattern.
        """
        for y in range(self.input_height):
            for x in range(self.input_width):
                neighbors = self._get_neighbors(pattern, x, y)
                current_pattern = pattern[y][x]
                self.patterns_dict[current_pattern] += 1

                for neighbor in neighbors:
                    self.adjacency_dict[current_pattern][neighbor] += 1

    @staticmethod
    def _get_neighbors(pattern, x, y):
        """
        Get the neighbors of a pattern at a given position.

        Args:
            pattern (list): 2D array of length 1 strings representing the input pattern.
            x (int): x-coordinate of the pattern.
            y (int): y-coordinate of the pattern.

        Returns:
            list: List of neighboring patterns.
        """
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(pattern[0]) and 0 <= ny < len(pattern):
                neighbors.append(pattern[ny][nx])
        return neighbors

    def _get_possible_patterns(self, x, y):
        """
        Get the possible patterns for a given position based on adjacency.

        Args:
            x (int): x-coordinate of the position.
            y (int): y-coordinate of the position.

        Returns:
            list: List of possible patterns.
        """
        possible_patterns = []
        for pattern in self.patterns_dict:
            if all(self.adjacency_dict[pattern][neighbor] > 0 for neighbor in self._get_neighbors(pattern, x, y)):
                possible_patterns.append(pattern)
        return possible_patterns

    def _choose_pattern(self, x, y):
        """
        Choose a pattern for a given position based on the available possibilities.

        Args:
            x (int): x-coordinate of the position.
            y (int): y-coordinate of the position.

        Returns:
            str: Chosen pattern.
        """
        possible_patterns = self._get_possible_patterns(x, y)
        pattern_weights = [self.patterns_dict[pattern] for pattern in possible_patterns]
        return random.choices(possible_patterns, weights=pattern_weights)[0]

    def generate_output(self):
        """
        Generate the output pattern using the Wave Function Collapse algorithm.

        Returns:
            list: 2D array of length 1 strings representing the output pattern.
        """
        output_pattern = [[''] * self.output_width for _ in range(self.output_height)]

        for y in range(self.output_height):
            for x in range(self.output_width):
                output_pattern[y][x] = self._choose_pattern(x, y)

        return output_pattern


# Example usage
input_pattern = [
    ['A', 'A', 'B', 'C'],
    ['A', 'B', 'B', 'C'],
    ['A', 'B', 'C', 'C']
]

output_width = 10  # Desired width of the output pattern
output_height = 10  # Desired height of the output pattern

wfc = WaveFunctionCollapse(input_pattern, output_width, output_height)
output_pattern = wfc.generate_output()

# Print the output pattern
for row in output_pattern:
    print(' '.join(row))
