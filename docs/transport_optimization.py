# -*- coding: utf-8 -*-
"""مثالی ساده برای حل مسئله بهینه‌سازی حمل و نقل با استفاده از کتابخانه Pyomo"""

from pyomo.environ import (
    ConcreteModel,
    Var,
    NonNegativeReals,
    Objective,
    Constraint,
    SolverFactory,
    Param,
    Set,
    minimize,
    value,
)

suppliers = ["A", "B"]
supply = {"A": 20, "B": 30}
consumers = ["X", "Y", "Z"]
demand = {"X": 15, "Y": 25, "Z": 10}

costs = {
    ("A", "X"): 2,
    ("A", "Y"): 4,
    ("A", "Z"): 5,
    ("B", "X"): 3,
    ("B", "Y"): 1,
    ("B", "Z"): 7,
}

model = ConcreteModel()
model.S = Set(initialize=suppliers)
model.C = Set(initialize=consumers)
model.cost = Param(model.S, model.C, initialize=costs)
model.x = Var(model.S, model.C, within=NonNegativeReals)


def objective_rule(m):
    return sum(m.cost[s, c] * m.x[s, c] for s in m.S for c in m.C)


model.objective = Objective(rule=objective_rule, sense=minimize)


def supply_rule(m, s):
    return sum(m.x[s, c] for c in m.C) <= supply[s]


model.supply_con = Constraint(model.S, rule=supply_rule)


def demand_rule(m, c):
    return sum(m.x[s, c] for s in m.S) >= demand[c]


model.demand_con = Constraint(model.C, rule=demand_rule)

solver = SolverFactory("glpk")
solver.solve(model, tee=False)

for s in suppliers:
    for c in consumers:
        q = value(model.x[s, c])
        if q and q > 0:
            print(f"{s} -> {c}: {q} واحد")
print("هزینه نهایی:", value(model.objective))
