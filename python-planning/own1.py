#!/usr/bin/python3

import random
import math

import numpy as np

import matplotlib.pyplot as plt


class Pattern:
    """
    Pattern class
    """

    def __init__(self, array: tuple):
        self.array = tuple(tuple(row) for row in array)

    def __str__(self):
        string = ""
        string += "(" + str(self.array[0]) + ",\n"
        for row in self.array[1:-1]:
            string += " " + str(row) + ",\n"
        string += " " + str(self.array[-1]) + ")"
        return string

    def __repr__(self):
        string = "\n"
        string += "(" + str(self.array[0]) + ",\n"
        for row in self.array[1:-1]:
            string += " " + str(row) + ",\n"
        string += " " + str(self.array[-1]) + ")"
        return string


class Index:
    """
    Store valid patterns for each offset position for each pattern
    """

    def __init__(self, patterns: list[Pattern]):
        directions = [
            (x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)
        ]

        self.data = {}
        for pattern in patterns:
            self.data[pattern] = {}
            for direction in directions:
                self.data[pattern][direction] = []

    def add_rule(
        self, pattern: Pattern, direction: tuple[int, int], other_pattern: Pattern
    ) -> None:
        """
        Add a direction to the index
        """
        self.data[pattern][direction].append(other_pattern)

    def check_possibility(
        self, pattern: Pattern, check_pattern: Pattern, direction: tuple[int, int]
    ) -> bool:
        """
        Check the possibility of an adjacent placement of patterns
        """
        if isinstance(pattern, list):
            pattern = pattern[0]

        return check_pattern in self.data[pattern][direction]


class WaveFunction:
    """
    Wave function class
    """

    def __init__(self, size: tuple[int, int], pattern_weights: dict[Pattern, int]):
        self.size = size

        self.weights = pattern_weights

        self.coefficients = [[patterns for y in range(size[1])] for x in range(size[0])]

    def is_fully_collapsed(self) -> bool:
        """
        Return whether the wave function has been fully collapsed
        """
        for row in self.coefficients:
            for entry in row:
                if len(entry) != 1:
                    return False
        return True

    def get_possible_patterns(self, position: tuple[int, int]) -> list[Pattern]:
        """
        Get a list of all possible patterns at position
        """
        x, y = position
        return self.coefficients[x][y]

    def get_shannon_entropy(self, position: tuple[int, int]) -> float:
        """
        Calculate the shannon entropy at the given position
        """
        x, y = position
        entropy = 0

        if len(self.coefficients[x][y]) == 1:
            return entropy

        for pattern in self.coefficients[x][y]:
            entropy -= probabilities[pattern] * math.log(probabilities[pattern], 2)

        entropy -= random.uniform(0, 0.1)

        return entropy

    def get_smallest_entropy_position(self) -> tuple[int, int] | None:
        """
        Get the position with lowest entropy
        """
        smallest_entropy = None
        smallest_entropy_position = None
        for x, column in enumerate(self.coefficients):
            for y, entry in enumerate(column):
                entropy = self.get_shannon_entropy((x, y))

                if entropy == 0:
                    continue

                if smallest_entropy is None or entropy < smallest_entropy:
                    smallest_entropy = entropy
                    smallest_entropy_position = (x, y)

        return smallest_entropy_position

    def observe(self) -> tuple[int, int] | None:
        """
        Observe the wave function and collapse to a single pattern for one position
        """
        smallest_entropy_position = self.get_smallest_entropy_position()

        if smallest_entropy_position is None:
            print("All tiles have 0 entropy")
            return None

        possible_patterns = self.get_possible_patterns(smallest_entropy_position)

        weights = [self.weights[pattern] for pattern in possible_patterns]

        pattern = np.random.choice(possible_patterns, 1, replace=False, p=weights)

    def valid_directions(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Get the valid directions from position that are within the image size
        """
        x, y = position

        if not (x < 1 or x > self.size[0] - 2):
            x_neighbours = (-1, 0, 1)
        else:
            if x < 1:
                x_neighbours = (0, 1)
            else:
                x_neighbours = (-1, 0)
        if not (y < 1 or y > self.size[1] - 2):
            y_neighbours = (-1, 0, 1)
        else:
            if y < 1:
                y_neighbours = (0, 1)
            else:
                y_neighbours = (-1, 0)

        return [(i, j) for j in y_neighbours for i in x_neighbours if (i, j) != (x, y)]

    def propagate(self, smallest_entropy_position) -> None:
        """
        Propagate the observations to collapse the entire wave function
        """
        stack = [smallest_entropy_position]

        while len(stack) > 0:
            position = stack.pop()

            possible_patterns = self.get_possible_patterns(position)

            for direction in self.valid_directions(position):
                adjacent_position = (
                    position[0] + direction[0],
                    position[1] + direction[1],
                )
                possible_adjacent_patterns = self.get_possible_patterns(
                    adjacent_position
                )

                if not isinstance(possible_adjacent_patterns, list):
                    possible_adjacent_patterns = [possible_adjacent_patterns]
                for possible_adjacent_pattern in possible_adjacent_patterns:
                    if len(possible_patterns) > 1:
                        is_possible = any(
                            [
                                index.check_possibility(
                                    pattern, possible_adjacent_pattern, direction
                                )
                                for pattern in possible_patterns
                            ]
                        )
                    else:
                        is_possible = index.check_possibility(
                            possible_patterns, possible_adjacent_pattern, direction
                        )

                    if not is_possible:
                        x, y = adjacent_position
                        self.coefficients[x][y] = [
                            pattern
                            for pattern in self.coefficients[x][y]
                            if pattern.array != possible_adjacent_pattern.array
                        ]

                        if adjacent_position not in stack:
                            stack.append(adjacent_position)


def get_rotations(pattern: tuple) -> list[tuple]:
    """
    Get a list of all the unique rotations of pattern
    """
    rotations = [pattern]
    temp = np.rot90(pattern)
    temp = tuple(tuple(row) for row in temp)
    if not np.array_equiv(pattern, temp):
        rotations.append(temp)
        temp = np.rot90(rotations[1])
        temp = tuple(tuple(row) for row in temp)
        if not np.array_equiv(pattern, temp):
            rotations.append(temp)
            temp = np.rot90(rotations[2])
            temp = tuple(tuple(row) for row in temp)
            rotations.append(temp)

    return rotations


def not_in(array: np.ndarray, array_list: list[np.ndarray]) -> bool:
    """
    Return whether array is not in array_list
    """
    for check_array in array_list:
        if np.array_equiv(array, check_array):
            return False
    return True


def get_pattern_weights(array: np.ndarray) -> dict[tuple, int]:
    """
    Get a list of all patterns and their rotations from an input array
    """

    weights: dict[tuple, int] = {}

    width, height = array.shape

    for x in range(width - 1):
        for y in range(height - 1):
            current_pattern = (
                tuple(array[x][y : y + 2]),
                tuple(array[x + 1][y : y + 2]),
            )
            for rotation in get_rotations(current_pattern):
                if weights.get(rotation) is None:
                    weights[rotation] = 1
                else:
                    weights[rotation] += 1

    return weights


def get_offset_tiles(pattern: Pattern, direction: tuple[int, int]):
    """
    Get the items in the pattern's array that overlap with a square offset in direction
    """
    match direction:
        case (0, 0):
            return pattern.array
        case (-1, -1):
            return tuple([pattern.array[0][0]])
        case (-1, 0):
            return tuple([pattern.array[0][0], pattern.array[1][0]])
        case (-1, 1):
            return tuple([pattern.array[1][0]])
        case (0, -1):
            return tuple([pattern.array[0]])
        case (0, 1):
            return tuple([pattern.array[1]])
        case (1, -1):
            return tuple([pattern.array[0][1]])
        case (1, 0):
            return tuple([pattern.array[0][1], pattern.array[1][1]])
        case (1, 1):
            return tuple([pattern.array[1][1]])


input_array = np.array(
    [
        [255, 255, 255, 255],
        [255, 0, 0, 0],
        [255, 0, 127, 0],
        [255, 0, 0, 0],
    ]
)

pattern_weights = get_pattern_weights(input_array)
sum_of_weights = sum(pattern_weights.values())


pattern_weights = {
    Pattern(pattern): weight for pattern, weight in pattern_weights.items()
}
patterns = list(pattern_weights)
probabilities = {
    pattern: weight / sum_of_weights for pattern, weight in pattern_weights.items()
}

index = Index(patterns)

for pattern in patterns:
    for direction in [
        (x, y) for x in range(-1, 2) for y in range(-1, 2) if (x, y) != (0, 0)
    ]:
        for check_pattern in patterns:
            overlap = get_offset_tiles(pattern, direction)
            opposite_direction = (direction[0] * -1, direction[1] * -1)
            check_overlap = get_offset_tiles(check_pattern, opposite_direction)
            if (overlap) == (check_overlap):
                index.add_rule(pattern, direction, check_pattern)


DEBUG_OUTPUT = True

if DEBUG_OUTPUT:
    plt.imshow(input_array, cmap="gray")
    plt.show()
    plt.figure(figsize=(10, 10))
    for m, (pattern, weight) in enumerate(pattern_weights.items()):
        axs = plt.subplot(4, math.ceil(len(pattern_weights) / 4), m + 1)
        axs.imshow(pattern.array, cmap="gray", vmin=0, vmax=255)
        axs.set_xticks([])
        axs.set_yticks([])
        plt.title(f"weight: {weight} prob: {probabilities[pattern]:.2f}")
    plt.show()
