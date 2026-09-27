"""Check validity with Z3: an argument is valid iff premises + negated conclusion is unsat.

SPDX-License-Identifier: MIT
"""

from z3 import (
    BoolSort, Bools, Const, DeclareSort, ForAll, Function, Implies, Not, Solver,
    sat, unknown, unsat,
)


def check(premises, conclusion):
    """Return ("VALID", None), ("INVALID", model) or ("UNKNOWN", reason)."""
    solver = Solver()
    solver.add(*premises)
    solver.add(Not(conclusion))
    result = solver.check()
    if result == unsat:
        return "VALID", None
    if result == sat:
        return "INVALID", solver.model()
    return "UNKNOWN", solver.reason_unknown()


def propositional():
    p, q = Bools("P Q")
    verdict, _ = check([Implies(p, q), p], q)
    assert verdict == "VALID"
    print(f"Modus ponens: {verdict}")

    verdict, model = check([Implies(p, q), q], p)
    assert verdict == "INVALID"
    assert not model.evaluate(p, model_completion=True)
    assert model.evaluate(q, model_completion=True)
    print(f"Affirming the consequent: {verdict}")
    print(f"Counterexample: P={model.evaluate(p, model_completion=True)}, "
          f"Q={model.evaluate(q, model_completion=True)}")

    verdict, _ = check([Implies(p, q), Not(q)], Not(p))
    assert verdict == "VALID"
    print(f"Modus tollens: {verdict}")

    # Unsatisfiable premises entail anything: check satisfiability separately.
    solver = Solver()
    solver.add(p, Not(p))
    assert solver.check() == unsat
    assert check([p, Not(p)], q)[0] == "VALID"
    print("Contradictory premises: VALID but unsatisfiable (not a sound argument)")


def first_order():
    Thing = DeclareSort("Thing")
    human = Function("Human", Thing, BoolSort())
    mortal = Function("Mortal", Thing, BoolSort())
    socrates = Const("socrates", Thing)
    x = Const("x", Thing)
    all_humans_mortal = ForAll([x], Implies(human(x), mortal(x)))

    verdict, _ = check([all_humans_mortal, human(socrates)], mortal(socrates))
    assert verdict == "VALID"
    print(f"Syllogism (all humans are mortal; Socrates is human): {verdict}")

    verdict, model = check([all_humans_mortal, mortal(socrates)], human(socrates))
    assert verdict == "INVALID"
    assert not model.evaluate(human(socrates), model_completion=True)
    print(f"Converse (Socrates is mortal, so human?): {verdict}")


def main():
    propositional()
    first_order()
    print("Self-checks: passed")


if __name__ == "__main__":
    main()
