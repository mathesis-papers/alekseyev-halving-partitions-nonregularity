import argparse
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path


def enumerate_partitions(total):
    def follow(previous, remaining, prefix):
        if remaining == 0:
            yield prefix
            return
        if previous == 1:
            yield prefix + (1,) * remaining
            return
        for part in sorted({previous // 2, (previous + 1) // 2}):
            if 0 < part <= remaining:
                yield from follow(part, remaining - part, prefix + (part,))

    return tuple(follow(total, total, ())) if total else ((),)


def count_by_length(total, requested_total=None):
    @lru_cache(maxsize=None)
    def follow(previous, remaining):
        if remaining == 0:
            return ((0, 1),)
        if previous == 1:
            return ((remaining, 1),)
        counts = Counter()
        for part in {previous // 2, (previous + 1) // 2}:
            if 0 < part <= remaining:
                for length, count in follow(part, remaining - part):
                    counts[length + 1] += count
        return tuple(sorted(counts.items()))

    remaining = total if requested_total is None else requested_total
    return dict(follow(total, remaining))


def profile(exponent):
    qualifying = []
    candidate = 1
    while 2**candidate + candidate + 1 <= exponent:
        qualifying.append(candidate)
        candidate += 1
    lengths = {exponent: 1, exponent + 1: 1, exponent + 2: 1}
    lengths.update({exponent - shift: 1 for shift in qualifying})
    return lengths, len(qualifying)


def weighted_histogram(total):
    @lru_cache(maxsize=None)
    def follow(previous, remaining):
        if remaining == 0:
            return ((0, 0, 1),)
        if previous == 1:
            return ((remaining, 0, 1),)
        counts = Counter()
        for part in {previous // 2, (previous + 1) // 2}:
            if 0 < part <= remaining:
                for length, weight, count in follow(part, remaining - part):
                    counts[length + 1, weight + int(previous % 2 == 0)] += count
        return tuple((length, weight, count) for (length, weight), count in sorted(counts.items()))

    return {(length, weight): count for length, weight, count in follow(total, total)}


def weighted_formula(exponent):
    counts = Counter({
        (exponent, max(0, exponent - 3)): 1,
        (exponent + 1, exponent - 2): 1,
        (exponent + 2, exponent - 1): 1,
    })
    shift = 1
    while 2**shift + shift + 1 <= exponent:
        counts[exponent - shift, max(0, exponent - 2**shift - shift - 2)] += 1
        shift += 1
    return dict(counts)


@lru_cache(maxsize=None)
def stern(total):
    if total < 2:
        return total
    if total % 2 == 0:
        return stern(total // 2)
    return stern(total // 2) + stern(total // 2 + 1)


def run_checks():
    initial = [1, 1, 1, 2, 1, 3, 2, 3, 1, 3, 3, 5, 2, 5, 3, 4, 1, 4, 3, 6]
    for total, expected in enumerate(initial):
        assert sum(count_by_length(total).values()) == expected
    for total in range(257):
        partitions = enumerate_partitions(total)
        assert len(partitions) == len(set(partitions))
        assert dict(Counter(map(len, partitions))) == count_by_length(total)
        for parts in partitions:
            assert sum(parts) == total
            previous = total
            for part in parts:
                assert part > 0 and part in {previous // 2, (previous + 1) // 2}
                previous = part
        if total:
            direct_weights = Counter()
            for parts in partitions:
                predecessors = (total,) + parts[:-1]
                direct_weights[len(parts), sum(previous % 2 == 0 for previous in predecessors)] += 1
            assert dict(direct_weights) == weighted_histogram(total)
    samples = []
    for exponent in range(2, 81):
        actual = count_by_length(2**exponent + 1)
        expected, threshold_count = profile(exponent)
        assert actual == expected
        assert list(sorted(actual)) == list(range(exponent - threshold_count, exponent + 3))
        assert set(actual.values()) == {1}
        for modulus in range(1, 13):
            residue_counts = [sum(value for length, value in actual.items() if length % modulus == residue)
                              for residue in range(modulus)]
            assert max(residue_counts) - min(residue_counts) <= 1
        total_parts = sum(length * count for length, count in actual.items())
        assert total_parts == (threshold_count + 3) * exponent + 3 - threshold_count * (threshold_count + 1) // 2
        count = sum(actual.values())
        sum_squares = sum(length * length * multiplicity for length, multiplicity in actual.items())
        assert 2 * total_parts == count * (2 * exponent + 2 - threshold_count)
        assert 12 * (count * sum_squares - total_parts**2) == count**2 * (count**2 - 1)
        assert stern(2**exponent + 1) - count == exponent - 2 - threshold_count
        assert weighted_histogram(2**exponent + 1) == weighted_formula(exponent)
        if exponent <= 40:
            for offset in range(exponent + 3):
                starting = 2**exponent + 1
                shifted_count = sum(count_by_length(starting, starting + offset).values())
                thresholds = sum(2**shift + shift + 1 + offset <= exponent for shift in range(1, exponent))
                assert shifted_count == 1 + min(exponent, offset + 2) + thresholds
        for dilation in range(4):
            dilated = 2**dilation * (2**exponent + 1)
            assert count_by_length(dilated) == {length + dilation: value for length, value in actual.items()}
            assert stern(dilated) - count == exponent - 2 - threshold_count
            assert weighted_histogram(dilated) == {
                (length + dilation, weight + dilation): value
                for (length, weight), value in weighted_formula(exponent).items()
            }
        if exponent >= 4:
            logarithm = exponent.bit_length() - 1
            assert logarithm + 2 <= sum(actual.values()) <= logarithm + 3
        if exponent in [2, 3, 4, 6, 7, 11, 12, 20, 21, 37, 38, 80]:
            samples.append({'m': exponent, 'a': sum(actual.values()), 'lengths': sorted(actual)})
    for exponent in range(2, 4097):
        current = sum(profile(exponent)[0].values())
        following = sum(profile(exponent + 1)[0].values())
        jump_positions = {2**shift + shift for shift in range(1, 13)}
        assert following - current == int(exponent in jump_positions)
    for total in range(1, 513):
        assert sum(count_by_length(2 * total).values()) == sum(count_by_length(total).values())
    for exponent in range(17):
        assert sum(count_by_length(2**exponent).values()) == 1
    return {
        'status': 'pass',
        'arithmetic': 'exact integers',
        'coverage': {
            'direct_positive_list_enumeration': {'n_min': 0, 'n_max': 256},
            'dyadic_length_polynomial_and_total_parts': {'m_min': 2, 'm_max': 80},
            'dyadic_growth_bounds': {'m_min': 4, 'm_max': 80},
            'dyadic_flatness_mean_variance_deficit_and_digit_weights': {'m_min': 2, 'm_max': 80},
            'dyadic_length_residue_balance': {'m_min': 2, 'm_max': 80, 'modulus_min': 1, 'modulus_max': 12},
            'dyadic_dilation_of_length_deficit_and_weights': {'m_min': 2, 'm_max': 80, 'v_min': 0, 'v_max': 3},
            'dyadic_offset_chain_counts': {'m_min': 2, 'm_max': 40, 'offset_min': 0, 'offset_max': 'm+2'},
            'independent_weighted_positive_list_enumeration': {'n_min': 1, 'n_max': 256},
            'threshold_difference_formula': {'m_min': 2, 'm_max': 4096},
            'even_dilation': {'n_min': 1, 'n_max': 512},
            'power_of_two_counts': {'m_min': 0, 'm_max': 16}
        },
        'examples': samples,
        'scope': 'Finite exact counts test length, deficit and digit-weight formulas; nonregularity over rings and nonautomaticity in bases 2^s have written proofs.'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run_checks(), indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
