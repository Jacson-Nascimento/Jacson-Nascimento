import math

import numpy as np

from statistical_physics_analysis import SPACE_SIZE, overlap_support, physical_features


def _mask(numbers):
    return sum(1 << (number - 1) for number in numbers)


def test_overlap_support_covers_exact_space():
    _, counts, mean, _ = overlap_support()
    assert int(counts.sum()) == SPACE_SIZE
    assert math.isclose(mean, 9.0)


def test_physical_features_are_rotation_invariant():
    game = [1, 2, 3, 7, 8, 9, 11, 13, 15, 17, 18, 19, 23, 24, 25]
    rotated = [25 - n + 1 for n in game]
    features = physical_features(np.asarray([_mask(game), _mask(rotated)], dtype=np.uint32))
    assert features[0].tolist() == features[1].tolist()


def test_boundary_energy_for_top_three_rows():
    game = list(range(1, 16))
    features = physical_features(np.asarray([_mask(game)], dtype=np.uint32))[0]
    assert int(features[4]) == 5
