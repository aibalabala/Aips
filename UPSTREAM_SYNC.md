# Upstream synchronization

Aips is a localization fork of [robbietilton/Compositor](https://github.com/robbietilton/Compositor).

## Version model

- `UPSTREAM_VERSION`: exact Compositor tag currently used as the Aips baseline.
- `AIPS_VERSION`: Aips release identifier.
- Aips release format: `<Compositor version>-aips.<revision>`.
- Example: upstream `v1.3.7` → Aips `1.3.7-aips.1`.

Aips should not silently advance its upstream baseline. Updating `UPSTREAM_VERSION` is an explicit maintenance decision after merge conflicts, localization changes, tests, and builds have been reviewed.

## Sync procedure

When a newer Compositor release appears:

1. Read the generated upstream sync report.
2. Review the upstream files changed between `UPSTREAM_VERSION` and the new tag.
3. Review the intersection between those files and files modified by Aips.
4. Treat the intersection as the highest-risk merge set.
5. Port upstream changes into the Aips full-source tree.
6. Re-apply or update Simplified Chinese localization where upstream strings changed.
7. Run Verify, ARM64 Release, and Universal 2 CI.
8. Update `UPSTREAM_VERSION`.
9. Update `AIPS_VERSION` and `CHANGELOG.md`.
10. Publish an Aips prerelease/release.

## Conflict policy

Do not replace the Aips tree wholesale with a new upstream release.

Prefer:
- upstream functional changes,
- Aips localization and branding where intentional,
- minimal code divergence from upstream,
- explicit manual review for files changed on both sides.

Files changed both upstream and in Aips are reported as **potential conflicts**. This does not necessarily mean Git would produce a textual conflict; it means the file deserves review before synchronization.

## Automation

`.github/workflows/upstream-sync.yml` runs weekly and can also be started manually.

If a newer upstream release exists, it:
- compares the current baseline to the latest upstream release,
- lists upstream-changed files,
- lists Aips-modified files relative to the current baseline,
- calculates their intersection,
- uploads a Markdown report,
- opens one GitHub issue for that upstream version unless one already exists.

The workflow only reports. It does **not** automatically merge upstream code or change `UPSTREAM_VERSION`.
