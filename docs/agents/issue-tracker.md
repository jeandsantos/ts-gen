# Issue tracker: GitHub

Issues and specs live in GitHub Issues for `jeandsantos/ts-gen`. Use the `gh` CLI from this clone.

## Conventions

- Create: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- Read: `gh issue view <number> --json number,title,body,labels,comments`.
- List: `gh issue list --state open --json number,title,body,labels,comments`, with appropriate label and state filters.
- Comment: `gh issue comment <number> --body "..."`.
- Apply or remove labels: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- Close: post the explanation with `gh issue comment`, then `gh issue close <number>`. Comment separately even when the issue is already closed.

Before the first issue creation of a session, verify the target with `gh repo view --json nameWithOwner`. File only in the user's repository; confirm any unexpected target with the user.

## Parent issues and blockers

Use native GitHub sub-issues and dependencies where available:

- Parent: `gh issue create --parent <parent> ...`, or `gh issue edit <parent> --add-sub-issue <child>` (`gh` 2.94+).
- Blockers: `gh issue create --blocked-by <n>,<n> ...`, or `gh issue edit <child> --add-blocked-by <blocker>` (`gh` 2.94+).
- Older CLI: retrieve an issue's database ID with `gh api repos/jeandsantos/ts-gen/issues/<n> --jq .id`. Add a sub-issue with `gh api --method POST repos/jeandsantos/ts-gen/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`; add a blocker with `gh api --method POST repos/jeandsantos/ts-gen/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`.
- Where native links are unavailable, put `Part of #<parent>` or `Blocked by: #<n>, #<n>` at the top of the child body, and list children in the parent's task list.
- Count open blockers: `gh api repos/jeandsantos/ts-gen/issues/<n> --jq .issue_dependencies_summary.blocked_by`. A ticket is startable when every blocker is closed.

## Pull requests as a triage surface

**PRs as a request surface: no.** Set to `yes` to treat external PRs as feature requests; `/triage` reads this flag.

## Skill operations

When a skill says "publish to the issue tracker", create a GitHub issue. When it says "fetch the relevant ticket", read the issue using the command above.

## Wayfinding operations

For `/wayfinder`, the map is one issue labelled `wayfinder:map`, containing Notes / Decisions-so-far / Fog. Link child tickets as sub-issues, or use the parent/task-list fallback above. Label children `wayfinder:<type>` (`research`, `prototype`, `grilling`, or `task`).

The frontier is the map's open children, in map order, excluding assigned issues and those with open blockers. Claim the first eligible child with `gh issue edit <n> --add-assignee @me` as the session's first write. Resolve by commenting with the answer, closing the child, then adding a gist and link to the map's Decisions-so-far.
