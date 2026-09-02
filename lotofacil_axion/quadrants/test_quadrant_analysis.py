import numpy as np

from quadrant_analysis import SPACE_SIZE, bh_adjust, quadrant


def test_quadrant_labels():
    a = np.array([-1, 0, 1, 2])
    b = np.array([-1, 1, -1, 1])
    assert quadrant(a, b, 0, 0).tolist() == [1, 2, 3, 4]


def test_space_size():
    assert SPACE_SIZE == 3_268_760


def test_bh_is_bounded_and_monotone_by_rank():
    p = [0.04, 0.001, 0.20, 0.03]
    q = bh_adjust(p)
    assert all(0 <= x <= 1 for x in q)
    order = np.argsort(p)
    assert np.all(np.diff(np.asarray(q)[order]) >= -1e-12)
