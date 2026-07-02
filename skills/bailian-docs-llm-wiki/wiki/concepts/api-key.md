# API Key

API Key 是调用阿里云百炼平台所有模型与应用服务的唯一鉴权凭证，由百炼控制台创建和管理，用于在 HTTP 请求或 SDK 调用中标识调用方身份并验证权限。

## 创建与获取

在百炼控制台的密钥管理页面创建 API Key，操作要求具备主账号权限，或子账号拥有"管理员"或"API-Key"页面权限。创建时需选择归属的[业务空间](workspace.md)（建议选默认空间），并可配置 IP 白名单和模型访问范围。

自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号，前缀为 `sk-ws`。API Key 仅在创建时展示一次明文，关闭弹窗后无法再次查看，请立即复制保存。

不同地域的控制台入口不同，且各地域（北京、新加坡、弗吉尼亚、法兰克福、东京）的 API Key 不互通，使用时须确保地域匹配。

## 权限机制

API Key 的调用权限由其归属的[业务空间](workspace.md)决定：

- **默认[业务空间](workspace.md)**的 API Key 可调用所有标准模型，无法设置模型级限制。
- **子业务空间**的 API Key 仅可调用该空间已授权的模型，支持按模型调用、模型训练、模型部署三个维度做精细化授权，并支持请求数限流和 [Token](token.md) 限流。
- 同一业务空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成）分别创建。
- 单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移。

## 环境变量配置

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码造成泄露风险。SDK（DashScope SDK 和 OpenAI 兼容 SDK）会自动读取该变量。

- **Linux/macOS**：在 `~/.bashrc` 或 `~/.zshrc` 中追加 `export DASHSCOPE_API_KEY="your-key"`，然后 `source` 生效。
- **Windows**：通过系统属性设置系统变量，或使用 `setx` / `[Environment]::SetEnvironmentVariable` 命令。

设置后需重启 IDE 或终端以加载新变量。使用 `sudo` 运行脚本时需加 `-E` 参数继承用户环境变量。

## 临时 API Key

在浏览器、移动 App 等不可信环境中，应通过后端服务生成临时 API Key，避免永久 Key 泄露。

- 有效期默认 60 秒，可通过 `expire_in_seconds` 参数设置，范围 1 至 1800 秒。
- 临时 Key 继承生成它的永久 Key 的全部权限，无法进一步收窄。
- 到期后自动失效，不能提前删除。
- 生成的临时 Key 前缀为 `st-`。

请求示例：

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tokens?expire_in_seconds=1800" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## [Token](token.md) Plan 专属 API Key

[Token](token.md) Plan 团队版使用独立的 API Key（前缀 `sk-sp-`），与百炼通用 API Key（前缀 `sk-`）体系完全隔离，配合专属 Base URL 使用。两类 Key 不可混用，MCP 服务仍需使用百炼通用 API Key。

## 有效性与安全注意事项

- API Key 没有自动失效日期，手动删除后即永久失效。
- 将 RAM 账号移出业务空间会使其 API Key 失效，重新加入后可恢复。
- 在 RAM 控制台删除账号或角色会导致 API Key 永久失效、不可恢复。
- 生产环境建议按环境（dev/test/prod）划分业务空间，对 API Key 做隔离管理。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)
- [more](../api/more.md)
- [more about models](../api/more-about-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [managed agents api](../api/managed-agents-api.md)
- [security and compliance](../guides/security-and-compliance.md)
- [bailian application calling](../guides/bailian-application-calling.md)


