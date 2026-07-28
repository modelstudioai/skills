# 迁移指南

迁移指南是将已有应用（主要基于 OpenAI 或 Anthropic 生态构建）迁移到阿里云百炼平台模型服务的操作总览。核心目标是尽可能复用现有代码与客户端库，仅替换凭证、服务地址和模型名称即可完成接入。

## 迁移三要素

无论使用哪种兼容协议，迁移的关键是配置以下三项：

- **API Key**：替换为百炼 API Key。各地域的 API Key 不同，切换地域时需同步更换。建议通过环境变量（如 `DASHSCOPE_API_KEY`）注入，避免硬编码。
- **Base URL**：根据所选兼容协议和地域，替换为百炼对应的服务地址。
- **Model**：替换为百炼支持的模型名称（如 `qwen-plus`、`qwen3-max` 等）。

对于已有 OpenAI 应用的最简迁移路径，通常只需替换这三项即可，无需改动业务逻辑。

## 接口选择

百炼提供四类文本生成接口，迁移时应根据现有技术栈和功能需求选择：

| 现有技术栈 | 推荐接口 | 迁移成本 |
| --- | --- | --- |
| OpenAI SDK（Chat Completions） | OpenAI 兼容 Chat Completions | 最低，直接复用客户端库 |
| OpenAI SDK（需要内置工具/自动上下文） | OpenAI 兼容 Responses | 中，需适配新接口字段 |
| Anthropic SDK | Anthropic 兼容 Messages | 最低，直接复用客户端库 |
| 无特定生态绑定，需最全功能 | DashScope 原生接口 | 较高，需学习原生 SDK |

迁移时需注意：不同接口的参数集合和功能覆盖存在差异。DashScope 参数最全，OpenAI/Anthropic 兼容接口以对应生态的字段约定为准。跨接口迁移时需核对参数映射，确认目标接口是否支持原有功能（如流式输出、function call、多模态等）。

## Base URL 配置

### OpenAI 兼容协议

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为业务空间 ID，可在百炼控制台的业务空间详情页查看。

### Anthropic 兼容协议

Anthropic 兼容协议的 Base URL 在上述地址基础上将 `/compatible-mode/v1` 替换为 `/apps/anthropic`。

## 计费方案匹配

百炼提供四种计费方案：Token Plan 个人版、Token Plan 团队版、Coding Plan、按量计费。迁移时需特别注意：

- 四种方案的 API Key 互不通用，Base URL 也各不相同。
- 配置时必须确保 API Key、Base URL 和计费方案三者匹配，否则会返回 401 认证错误。
- 例如 Token Plan 个人版 OpenAI 兼容地址为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，与按量计费地址不同。

## 域名与路径迁移

### 旧域名迁移

百炼为北京、新加坡地域推出了业务空间专属域名，性能与稳定性更佳，建议从旧域名迁移：

- 北京：`https://dashscope.aliyuncs.com` → `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://dashscope-intl.aliyuncs.com` → `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

现有旧域名仍可正常使用，但建议尽快迁移。

### 旧版路径迁移

Responses 与 Conversations 接口的旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/...` 即将停止维护，请迁移至新版 `/compatible-mode/v1/...` 路径。

## 客户端工具迁移

百炼支持通过多种聊天客户端和开发工具接入模型服务（如 Claude Code、Codex、Cursor、Cline、Cherry Studio 等）。这类工具的迁移步骤通常为：

1. 选择计费方案并获取对应 API Key。
2. 根据工具支持的协议（OpenAI 兼容或 Anthropic 兼容）选择 Base URL。
3. 在工具的配置文件或设置界面中填入 API Key、Base URL 和模型名称。

各工具的具体配置文件路径和字段不同，需参照对应文档。

## 注意事项

- **地域限制**：部分模型仅支持特定地域（如 `qwen-deep-research` 仅支持华北2-北京），迁移前需确认目标模型的地域可用性。
- **协议差异**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；`qwen-deep-research` 仅支持 Python DashScope SDK，暂不支持 OpenAI 兼容接口。
- **三方模型**：三方直供模型（如 DeepSeek、Kimi、GLM 等）仅在中国站的中国内地地域可用，调用前需在控制台开通对应服务。
- **功能差异**：若原应用依赖联网搜索、代码解释器等内置工具，需使用 Responses 接口而非普通的 Chat Completions。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


