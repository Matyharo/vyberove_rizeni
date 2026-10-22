"""Recomputable cost envelope; all input costs are explicit assumptions."""
from .core import dump_json, read_json


def estimate(scenario):
    s = scenario
    if s["candidates"] <= 0 or not 0 <= s["accepted_fraction"] <= 1:
        raise ValueError("Invalid scenario population")
    hours = s["candidates"] * s["review_minutes_per_candidate"] / 60
    human = hours * s["review_usd_per_hour"]
    machine = s["candidates"] * s["machine_usd_per_candidate"]
    setup = s["setup_hours"] * s["setup_usd_per_hour"]
    subtotal = human + machine + setup + s["infrastructure_usd"]
    accepted = round(s["candidates"] * s["accepted_fraction"])
    # Check machine-readable changes for all published records. Re-review only
    # the scenario fraction that changed; do not reapply initial setup costs.
    refresh_machine = accepted * s["machine_usd_per_candidate"]
    refresh_human = accepted * s["quarterly_review_fraction"] * s["quarterly_review_minutes"] / 60 * s["review_usd_per_hour"]
    total = subtotal * (1 + s["contingency_fraction"])
    return dict(name=s["name"], candidates=s["candidates"], accepted_scenario=accepted,
                review_hours=hours, review_cost_usd=human, machine_cost_usd=machine,
                setup_cost_usd=setup, infrastructure_usd=s["infrastructure_usd"],
                contingency_usd=total-subtotal, initial_total_usd=total,
                initial_per_accepted_usd=total/accepted if accepted else None,
                quarterly_refresh_usd=(refresh_machine + refresh_human + s["quarterly_fixed_usd"]) * (1+s["contingency_fraction"]))


def build_costs(root):
    config = read_json(root / "data/cost_assumptions.json")
    output = dict(as_of=config["as_of"], status=config["status"], currency=config["currency"],
                  scenarios=[estimate(s) for s in config["scenarios"]])
    dump_json(root / "exports/cost_estimate.json", output)
    return output
