import argparse
import json
import sys
from pathlib import Path

from .core import build, read_json, validate
from .costs import build_costs


def main():
    parser = argparse.ArgumentParser(description="Validate and export evidence-led investor pilot")
    parser.add_argument("command", choices=["validate", "build", "check-release"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        root = args.root
        if args.command == "validate":
            validate(read_json(root/"data/pilot.json"), read_json(root/"data/candidates.json"), read_json(root/"data/predictions.json"))
            print("Structural validation passed; factual human verification is a separate step.")
            return 0
        result = build(root)
        if (root/"data/cost_assumptions.json").exists():
            build_costs(root)
        print(json.dumps({"classification": result["classification"], "coverage": result["coverage"]}, ensure_ascii=False, indent=2))
        if args.command == "check-release":
            blockers = []
            if result["classification"]["human_reviewed"] < result["classification"]["candidates"]:
                blockers.append("Missing human candidate reviews")
            if result["classification"]["precision"]["value"] is None or result["classification"]["initial_positive_not_resolved"]:
                blockers.append("Initial positive predictions still lack resolved human evaluation")
            if not list((root / "ai-log").glob("conversation-export.*")):
                blockers.append("Missing authentic conversation export: ai-log/conversation-export.*")
            metadata = read_json(root/"release.json") if (root/"release.json").exists() else {}
            repository_url = metadata.get("public_repository_url")
            if not isinstance(repository_url, str) or not repository_url.startswith("https://github.com/"):
                blockers.append("Missing public GitHub repository URL in release.json")
            if blockers:
                print("NOT READY TO SUBMIT: " + "; ".join(blockers), file=sys.stderr)
                return 2
            print("Submission checklist complete; manually confirm repository is public and export is authentic.")
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
