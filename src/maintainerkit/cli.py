"""CLI entrypoint for MaintainerKit."""
import sys
import argparse
from maintainerkit.health.checker import HealthChecker
from maintainerkit.triage.classifier import IssueClassifier
from maintainerkit.review.analyzer import PRAnalyzer
from maintainerkit.release.notes import ReleaseNotesGenerator, MergedPR

def main():
    parser = argparse.ArgumentParser(description="MaintainerKit - Open-source maintenance automation for GitHub.")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # health command
    health_parser = subparsers.add_parser("health", help="Audit repository health and governance standards")
    health_parser.add_argument("path", nargs="?", default=".", help="Path to repository root")

    # triage command
    triage_parser = subparsers.add_parser("triage", help="Classify and triage an issue")
    triage_parser.add_argument("--title", required=True, help="Issue title")
    triage_parser.add_argument("--body", default="", help="Issue description")
    triage_parser.add_argument("--ai", action="store_true", help="Enable optional AI reasoning")

    # review command
    review_parser = subparsers.add_parser("review", help="Prepare a structured PR review risk report")
    review_parser.add_argument("--pr", type=int, default=1, help="PR number")
    review_parser.add_argument("--title", required=True, help="PR title")
    review_parser.add_argument("--files", nargs="+", required=True, help="List of changed filepaths")
    review_parser.add_argument("--added", type=int, default=0, help="Lines added")
    review_parser.add_argument("--removed", type=int, default=0, help="Lines removed")

    # release command
    release_parser = subparsers.add_parser("release", help="Generate semantic release notes")
    release_parser.add_argument("--version", required=True, help="Release version tag (e.g. v0.1.0)")

    args = parser.parse_args()

    if args.command == "health":
        checker = HealthChecker(args.path)
        report = checker.check()
        print(report.render())
        sys.exit(0 if report.score >= 70 else 1)

    elif args.command == "triage":
        classifier = IssueClassifier(use_ai=args.ai)
        result = classifier.classify(args.title, args.body)
        print("Issue Triage Report")
        print("----------------------------------------")
        print(f"Title:            {result.title}")
        print(f"Priority:         {result.priority}")
        print(f"Area:             {result.area}")
        print(f"Suggested Labels: {', '.join(result.labels)}")
        print(f"Needs Response:   {'Yes' if result.needs_maintainer_response else 'No'}")
        print(f"Action:           {result.suggested_action}")

    elif args.command == "review":
        analyzer = PRAnalyzer()
        prep = analyzer.analyze(
            pr_number=args.pr,
            title=args.title,
            files_changed=args.files,
            lines_added=args.added,
            lines_removed=args.removed
        )
        print(f"PR Review Readiness Report - PR #{prep.pr_number}")
        print("----------------------------------------")
        print(f"Title:               {prep.title}")
        print(f"Risk Level:          {prep.risk_level}")
        print(f"Suggested Reviewers: {', '.join(prep.suggested_reviewers)}")
        print(f"Files Changed:       {len(prep.files_changed)} (+{prep.lines_added}/-{prep.lines_removed})")
        print("Checks:")
        for check, status in prep.checks_status.items():
            print(f"  [{status}] {check}")
        if prep.risk_factors:
            print("Risk Factors:")
            for rf in prep.risk_factors:
                print(f"  ! {rf}")

    elif args.command == "release":
        generator = ReleaseNotesGenerator()
        sample_prs = [
            MergedPR(1, "feat: implement issue triage classification", "qchaudary", "Features", ["feature"]),
            MergedPR(2, "fix: resolve token boundary regex in classifier", "contributor", "Bug Fixes", ["bug"]),
            MergedPR(3, "sec: harden input validation on file diffs", "sec-expert", "Security", ["security"]),
        ]
        notes = generator.generate(args.version, sample_prs)
        print(notes)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
