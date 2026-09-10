"""CLI entrypoint for MaintainerKit v0.2.0."""
import sys
import os
import json
import argparse
from maintainerkit.health.checker import HealthChecker
from maintainerkit.triage.classifier import IssueClassifier
from maintainerkit.review.analyzer import PRAnalyzer
from maintainerkit.release.notes import ReleaseNotesGenerator
from maintainerkit.github.pull_requests import PRService
from maintainerkit.github.issues import IssueService

def run_audit(path: str = ".", repo: str = "qchaudary/maintainer-kit", as_json: bool = False):
    checker = HealthChecker(path)
    health_rep = checker.check()

    audit_data = {
        "repository": repo,
        "health_score": health_rep.score,
        "governance_checks": health_rep.checks,
        "recommendations": health_rep.recommendations,
        "current_version": "0.2.0",
        "human_approval_boundary": True
    }

    if as_json:
        print(json.dumps(audit_data, indent=2))
        return

    print("MaintainerKit Repository Audit")
    print("========================================")
    print(f"Repository:        {repo}")
    print(f"Health Score:      {health_rep.score}/100")
    print(f"Current Version:   0.2.0")
    print("Governance Checks:")
    for check, passed in health_rep.checks.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {check:<24} {status}")
    print("----------------------------------------")
    print("Maintainer Automation:")
    print("  Issue Triage:          Active (Deterministic + Optional AI)")
    print("  PR Review Prep:        Active (Risk & Sensitivity Analysis)")
    print("  Release Notes:         Active (GitHub API / Git Log Engine)")
    print("  Human Approval Gate:   Enforced (No automated merges/closures)")
    print("========================================")
    print(f"MaintainerKit Score: {health_rep.score}/100")

def main():
    parser = argparse.ArgumentParser(description="MaintainerKit - Open-source maintenance automation for GitHub.")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # audit command (Flagship command)
    audit_parser = subparsers.add_parser("audit", help="Run comprehensive repository and maintainer audit")
    audit_parser.add_argument("path", nargs="?", default=".", help="Path to repository root")
    audit_parser.add_argument("--repo", default="qchaudary/maintainer-kit", help="GitHub repository (owner/name)")
    audit_parser.add_argument("--json", action="store_true", help="Output results as JSON")

    # health command
    health_parser = subparsers.add_parser("health", help="Audit repository health and governance standards")
    health_parser.add_argument("path", nargs="?", default=".", help="Path to repository root")
    health_parser.add_argument("--json", action="store_true", help="Output report as JSON")

    # triage command
    triage_parser = subparsers.add_parser("triage", help="Classify and triage an issue")
    triage_parser.add_argument("--title", required=False, help="Issue title")
    triage_parser.add_argument("--body", default="", help="Issue description")
    triage_parser.add_argument("--issue", type=int, help="Fetch issue directly from GitHub repo")
    triage_parser.add_argument("--repo", default="qchaudary/maintainer-kit", help="GitHub repository (owner/name)")
    triage_parser.add_argument("--comment", action="store_true", help="Post triage assessment as an issue comment")
    triage_parser.add_argument("--ai", action="store_true", help="Explicitly enable optional AI reasoning")
    triage_parser.add_argument("--json", action="store_true", help="Output triage as JSON")

    # review command
    review_parser = subparsers.add_parser("review", help="Prepare a structured PR review risk report")
    review_parser.add_argument("--pr", type=int, default=1, help="PR number")
    review_parser.add_argument("--title", required=False, help="PR title")
    review_parser.add_argument("--files", nargs="+", help="List of changed filepaths")
    review_parser.add_argument("--repo", default="qchaudary/maintainer-kit", help="GitHub repository (owner/name)")
    review_parser.add_argument("--added", type=int, default=0, help="Lines added")
    review_parser.add_argument("--removed", type=int, default=0, help="Lines removed")
    review_parser.add_argument("--comment", action="store_true", help="Post review readiness report as a PR comment")
    review_parser.add_argument("--json", action="store_true", help="Output report as JSON")

    # release command
    release_parser = subparsers.add_parser("release", help="Generate semantic release notes")
    release_parser.add_argument("--version", required=True, help="Release version tag (e.g. v0.2.0)")
    release_parser.add_argument("--repo", default="qchaudary/maintainer-kit", help="GitHub repository (owner/name)")
    release_parser.add_argument("--local", action="store_true", help="Use local git commit log instead of GitHub API")
    release_parser.add_argument("--json", action="store_true", help="Output notes as JSON")

    args = parser.parse_args()

    if args.command == "audit":
        run_audit(args.path, args.repo, as_json=args.json)
        sys.exit(0)

    elif args.command == "health":
        checker = HealthChecker(args.path)
        report = checker.check()
        if args.json:
            print(report.to_json())
        else:
            print(report.render())
        sys.exit(0 if report.score >= 70 else 1)

    elif args.command == "triage":
        title = args.title or ""
        body = args.body or ""
        if args.issue:
            svc = IssueService()
            data = svc.get_issue(args.repo, args.issue)
            if data:
                title = data.get("title", title)
                body = data.get("body", body) or ""

        if not title:
            print("Error: --title or valid --issue number required.")
            sys.exit(1)

        classifier = IssueClassifier(use_ai=args.ai)
        result = classifier.classify(title, body)

        if args.json:
            print(json.dumps({
                "title": result.title,
                "priority": result.priority,
                "area": result.area,
                "labels": result.labels,
                "needs_response": result.needs_maintainer_response,
                "summary": result.summary,
                "action": result.suggested_action
            }, indent=2))
        else:
            print("Issue Triage Report")
            print("----------------------------------------")
            print(f"Title:            {result.title}")
            print(f"Priority:         {result.priority}")
            print(f"Area:             {result.area}")
            print(f"Suggested Labels: {', '.join(result.labels)}")
            print(f"Needs Response:   {'Yes' if result.needs_maintainer_response else 'No'}")
            print(f"Action:           {result.suggested_action}")

        if args.comment and args.issue:
            svc = IssueService()
            report_text = (
                "### MaintainerKit Triage Report\n"
                f"- **Priority**: {result.priority}\n"
                f"- **Area**: {result.area}\n"
                f"- **Suggested Labels**: `{', '.join(result.labels)}`\n"
                f"- **Needs Maintainer Response**: {'Yes' if result.needs_maintainer_response else 'No'}\n"
                f"- **Summary**: {result.summary}\n"
                f"- **Action**: {result.suggested_action}"
            )
            svc.post_issue_comment(args.repo, args.issue, report_text)
            print("Successfully posted triage comment to GitHub!")

    elif args.command == "review":
        title = args.title or f"PR #{args.pr}"
        files = args.files or []
        added = args.added
        removed = args.removed

        if not files and args.pr:
            pr_svc = PRService()
            pr_data = pr_svc.get_pr(args.repo, args.pr)
            if pr_data:
                title = pr_data.get("title", title)
                added = pr_data.get("additions", added)
                removed = pr_data.get("deletions", removed)
            pr_files = pr_svc.get_pr_files(args.repo, args.pr)
            files = [f.get("filename", "") for f in pr_files if f.get("filename")]

        analyzer = PRAnalyzer()
        prep = analyzer.analyze(
            pr_number=args.pr,
            title=title,
            files_changed=files,
            lines_added=added,
            lines_removed=removed
        )

        if args.json:
            print(json.dumps({
                "pr_number": prep.pr_number,
                "title": prep.title,
                "risk_level": prep.risk_level,
                "suggested_reviewers": prep.suggested_reviewers,
                "files_count": len(prep.files_changed),
                "checks": prep.checks_status,
                "risk_factors": prep.risk_factors
            }, indent=2))
        else:
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

        if args.comment and args.pr:
            pr_svc = PRService()
            review_md = (
                f"### MaintainerKit PR Review Readiness - PR #{prep.pr_number}\n"
                f"- **Risk Level**: {prep.risk_level}\n"
                f"- **Suggested Reviewers**: {', '.join(prep.suggested_reviewers)}\n"
                f"- **Changes**: {len(prep.files_changed)} files changed (+{prep.lines_added}/-{prep.lines_removed})\n\n"
                "**Review Checklist:**\n"
            )
            for rf in prep.risk_factors:
                review_md += f"- [ ] Verify: {rf}\n"
            if not prep.risk_factors:
                review_md += "- [x] Low risk change. Standard review applies.\n"
            pr_svc.post_pr_comment(args.repo, args.pr, review_md)
            print("Successfully posted PR review preparation comment to GitHub!")

    elif args.command == "release":
        generator = ReleaseNotesGenerator()
        prs = []
        if not args.local:
            prs = generator.fetch_live_prs(args.repo)
        if not prs:
            prs = generator.fetch_local_git_commits()

        notes = generator.generate(args.version, prs, repo=args.repo)
        if args.json:
            print(json.dumps({"version": args.version, "repository": args.repo, "notes": notes}, indent=2))
        else:
            print(notes)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
