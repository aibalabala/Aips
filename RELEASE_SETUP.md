# Aips 正式签名与公证发布配置

仓库已经包含 `.github/workflows/notarized-release.yml`。

正式发布流程：

1. macOS 26 / Xcode 26.6 构建 Release 版 `Aips.app`
2. 使用 Apple **Developer ID Application** 证书签名
3. 启用 Hardened Runtime
4. 提交 Apple Notarization
5. Staple 公证票据
6. 再次验证 Gatekeeper / codesign
7. 打包 ZIP
8. 当推送 `v*` tag 时自动创建 GitHub Release

## 必须配置的 GitHub Actions Secrets

进入：

`Repository → Settings → Secrets and variables → Actions → New repository secret`

添加以下 5 项：

### APPLE_CERTIFICATE_P12_BASE64

Developer ID Application 证书的 `.p12` 文件内容，转换为 Base64 后填入。

macOS 终端示例：

```bash
base64 -i DeveloperIDApplication.p12 | pbcopy
```

把剪贴板内容完整粘贴到 Secret。

### APPLE_CERTIFICATE_PASSWORD

导出 `.p12` 时设置的密码。

### APPLE_ID

用于 Apple Developer / notarization 的 Apple ID 邮箱。

### APPLE_TEAM_ID

Apple Developer Team ID。

### APPLE_APP_PASSWORD

Apple ID 的“App 专用密码”，供 `xcrun notarytool` 使用。

不要填写 Apple ID 的登录密码。

## 发布

五个 Secrets 配置完成后创建版本 tag，例如：

```bash
git tag v1.3.7
git push origin v1.3.7
```

GitHub Actions 会自动执行：

```text
Build
→ Developer ID Sign
→ Notarize
→ Staple
→ Gatekeeper Verify
→ ZIP
→ GitHub Release
```

如果任意 Secret 缺失，正式发布工作流会在最开始停止，不会发布未签名版本。

## 当前普通构建

`.github/workflows/release-build.yml` 仍然保留，用于生成 Ad-hoc 签名的 ARM64 测试包。

它和正式发布流水线互不影响。
