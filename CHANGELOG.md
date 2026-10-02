# Changelog

Aips follows the upstream Compositor version and adds an Aips revision suffix:

`<upstream-version>-aips.<revision>`

Example: `1.3.7-aips.1`.

The macOS app's `CFBundleShortVersionString` remains the numeric upstream-compatible version (for example `1.3.7`). The Aips revision is tracked by Git tags, `AIPS_VERSION`, release notes, and build metadata.

## 1.4.5-aips.1 — 2026-10-02

Base: Compositor v1.4.5.

### Upstream synchronization
- Synced Compositor v1.4 through v1.4.5.
- Adopted the GPU canvas rendering path and associated rendering/performance fixes.
- Adopted updated transform, tab, layer-mask, Smudge, Liquify, Blur, Dither/CRT, and Camera Raw behavior.
- Preserved Aips branding, bundle identifier, Swift module compatibility, test-host configuration, and ad-hoc nested-code re-signing.

### Simplified Chinese
- Audited all v1.3.7 → v1.4.5 upstream UI changes.
- Added Simplified Chinese coverage for new CRT Scanlines controls, mask-view interactions, transform modifier hints, Camera Raw curve guidance, Ungroup Layers, project-tab overflow labels, and related help text.
- Localization catalog audit: 0 missing/incomplete zh-Hans keys and 0 uncovered new UI candidates.

## 1.3.7-aips.2 — 2026-09-28

Base: Compositor v1.3.7.

### Fixed
- Fixed launch-time DYLD failure caused by mismatched code-signing identities between the ad-hoc-signed Aips host app and the bundled Sparkle framework.
- Universal 2 and ARM64 CI now re-sign bundled frameworks, dylibs, XPC services, and nested apps before re-signing the host Aips.app.
- DMG packaging now uses the corrected consistently signed application bundle.

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
