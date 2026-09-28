# Changelog

Aips follows the upstream Compositor version and adds an Aips revision suffix:

`<upstream-version>-aips.<revision>`

Example: `1.3.7-aips.1`.

The macOS app's `CFBundleShortVersionString` remains the numeric upstream-compatible version (for example `1.3.7`). The Aips revision is tracked by Git tags, `AIPS_VERSION`, release notes, and build metadata.

## 1.3.7-aips.1 — 2026-09-28

Base: Compositor v1.3.7.

### Aips
- Simplified Chinese localization fork maintained by Ai巴拉巴拉 / aibalabala.com.
- Migrated from overlay assembly to a complete source repository.
- Fixed Aips test-host paths after renaming the app bundle from Compositor to Aips.
- Preserved the Swift module name `Compositor` while the app product remains `Aips`.
- Disabled generated String Catalog Swift symbols to avoid localization-key symbol collisions.
- Fixed localization wrapper syntax errors found by Xcode 26.6.
- Added macOS 26 / Xcode 26.6 CI verification.
- Added ARM64 Release builds.
- Added Universal 2 builds for arm64 + x86_64.
- Added SHA256 output and automated GitHub prereleases.
- Added a separate Developer ID signing / Apple notarization workflow for future formal releases.

### Upstream
Compositor v1.3.7 removes the unused Finder thumbnail image introduced in 1.3.6 while keeping Space-bar Quick Look behavior unchanged.
