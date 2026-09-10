"""A minimal truth-table checker for classical propositional entailment.

SPDX-License-Identifier: MIT
"""

from itertools import product
from typing import Callable, Dict, Optional, Sequence, Tuple

Assignment = Dict[str, bool]
Formula = Callable[[Assignment], bool]


def implies(p: bool, q: bool) -> bool:
    return not p or q


def check_entailment(
    variables: Sequence[str], premises: Sequence[Formula], conclusion: Formula
) -> Tuple[bool, Optional[Assignment], int]:
    """Return validity, first counterexample, and count of satisfying assignments.

    A zero count means the premises are unsatisfiable. Such premises entail
    every conclusion in classical logic, but cannot form a sound argument.
    """
    if len(set(variables)) != len(variables):
        raise ValueError("Variable names must be unique")
    counterexample = None
    satisfying = 0
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(premise(assignment) for premise in premises):
            satisfying += 1
            if not conclusion(assignment) and counterexample is None:
                counterexample = assignment.copy()
    return counterexample is None, counterexample, satisfying


def main() -> None:
    p = lambda a: a["P"]
    q = lambda a: a["Q"]
    conditional = lambda a: implies(a["P"], a["Q"])
    variables = ("P", "Q")

    assert [implies(pv, qv) for pv, qv in product((False, True), repeat=2)] == [
        True, True, False, True
    ]
    valid, counterexample, count = check_entailment(variables, [conditional, p], q)
    assert valid and counterexample is None and count == 1
    print(f"Modus ponens: VALID ({count} satisfying assignment)")

    valid, counterexample, count = check_entailment(variables, [conditional, q], p)
    assert not valid and counterexample == {"P": False, "Q": True} and count == 2
    print("Affirming the consequent: INVALID")
    print(f"Counterexample: P={counterexample['P']}, Q={counterexample['Q']}")

    assert check_entailment(variables, [p, lambda a: not p(a)], q) == (True, None, 0)
    assert check_entailment(variables, [], lambda a: p(a) or not p(a)) == (True, None, 4)
    print("Self-checks: passed")


if __name__ == "__main__":
    main()
