import sys


def simplify_fraction(fraction):
    def get_divisors(n):
        return [x for x in range(1, n + 1) if n % x == 0]

    def get_common_divisors(a, b):
        nominator_divisors = get_divisors(a)
        denominator_divisors = get_divisors(b)
        return set(nominator_divisors) & set(denominator_divisors)
    fraction[0] = int(fraction[0])
    fraction[1] = int(fraction[1])
    biggest_divisor = max(get_common_divisors(fraction[0], fraction[1]))
    return fraction[0] // biggest_divisor, fraction[1] // biggest_divisor


def sort_fractions(fractions):
    def expand(fraction, multipl):
        return fraction[0] * multipl, fraction[1] * multipl

    multiplier = 1
    for f in fractions:
        multiplier *= f[1]

    sorted_expanded_fractions = list(sorted([expand(f, multiplier // f[1]) for f in fractions]))

    # Uncomment for improving performance and simplifying fraction
    # return ([simplify_fraction(f) for f in sorted_expanded_fractions])
    # ------------------------------------------------------------------

    # Major performance bottleneck
    # Can be fixed by returning just the simplified version, rather the original input

    result = []
    for simplified in sorted_expanded_fractions:
        for f in fractions:
            if simplify_fraction(f) == simplify_fraction(simplified):
                result.append(f)

    return result


if __name__ == '__main__':
    print(simplify_fraction(sys.argv[1].split('/')))

