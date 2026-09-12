# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均基于阿里云统一安全体系构建，满足中国《生成式人工智能服务管理暂行办法》《个人信息保护法》等法规要求。开发者需结合自身业务场景，合理配置参数并完成必要备案流程。

## 支持的模型/功能

以下安全与合规能力适用于所有百炼平台托管的模型（含 Qwen 系列、第三方精调模型及自定义部署模型）：
- **输入输出 AI 安全护栏**：实时检测并拦截违法、违规、涉政、色情、暴力等高风险内容，支持自定义敏感词库和策略等级（[输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance.md)）；
- **模型备案信息公示**：所有上线模型均已完成国家网信办备案，并在控制台及 API 响应头中返回备案编号（[模型备案信息公示](../../raw/model-user-guide/security-and-compliance.md)）；
- **应用合规备案**：调用百炼模型构建的对外服务类应用（含 Web/App/小程序），须单独完成《AI 应用备案》（[应用合规备案](../../raw/model-user-guide/security-and-compliance.md)）。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `enable_content_safety` | boolean | 启用输入输出安全护栏（仅对 `/v1/chat/completions` 和 `/v1/text-generation` 生效） | `true` |
| `safety_level` | string | 安全策略强度，取值 `low` / `medium` / `high`；`high` 模式将更严格拦截模糊边界内容 | `medium` |
| `disable_safety_cache` | boolean | 是否跳过安全策略缓存（用于调试或规避误拦截） | `false` |

> **注意**：`safety_level=high` 可能导致合法但表述敏感的请求被拦截，建议灰度验证后上线；该行为与 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance.md) 文档描述一致，但与旧版 SDK v2.3.0 的默认行为存在差异（v2.3.0 默认为 `low`），请升级至 v3.1.0+ 并显式设置。

## 使用方式

1. **API 调用时启用护栏**：在请求 Header 中添加 `X-DashScope-Safety: enabled`，或在 JSON body 中传入 `enable_content_safety=true`；
2. **私网访问配置**：通过 VPC 绑定专属资源组，并在[模型部署](../concepts/model-deployment.md)时勾选「仅限私网访问」，详见 [私网访问配置](../../raw/model-user-guide/security-and-compliance.md)；
3. **权限最小化实践**：使用 RAM 子账号 + 自定义策略（如 `AliyunBaiLianFullAccess` 需谨慎授予），推荐按 [权限管理](../../raw/model-user-guide/security-and-compliance.md) 文档配置细粒度 Action 级权限。

## 限制和注意事项

- 安全护栏不支持异步批量推理接口（`/v1/batch`）和流式响应中的逐 chunk 检测，仅对完整请求/响应体生效；
- 传输加密强制启用 TLS 1.2+，不支持降级；明文 HTTP 请求将被拒绝（参见 [传输安全](../../raw/model-user-guide/security-and-compliance.md)）；
- 模型备案编号随模型版本自动更新，但应用备案需手动同步更新，否则可能被监管平台标记为“未备案应用”；
- 所有日志默认脱敏存储，原始输入输出文本不落盘，符合 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance.md) 中关于数据处理的承诺。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)



