# use chat client or development tool

Token Plan 提供标准化的 API 接口，支持与主流 AI 编程工具和智能体开发平台集成。开发者可通过 OpenAI 兼容或 Anthropic 兼容协议快速接入，无需修改业务逻辑。所有配置均围绕 Token Plan 专属凭证与隔离式 Base URL 展开，确保计费与权限精准匹配。详细背景请参见 [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md)。

## 支持的模型/功能

- **协议兼容性**：支持 OpenAI 兼容（`/v1/chat/completions` 等标准路径）与 Anthropic 兼容（`/messages`）两种模式，对应不同 Base URL。
- **工具覆盖**：已验证兼容 Qoder、Claude Code、Codex、Qwen Code、OpenClaw、Hermes Agent、OpenCode、Trae、DeepSeek Harness、WorkBuddy 等十余种开发工具（完整列表见 [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md)）。
- **模型能力**：底层调用 Token Plan 所购模型实例（如 Qwen2.5-72B、Qwen3、DeepSeek-V3 等），具体可用模型取决于账户开通的服务包，不支持跨计划模型混用。

## 关键参数

| 参数 | 值 | 说明 |
|------|----|------|
| `Base URL`（OpenAI 兼容） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 仅限 `sk-sp-` 开头的 Token Plan API Key 使用 |
| `Base URL`（Anthropic 兼容） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 同上，需配合 Anthropic 协议客户端（如 Claude Code） |
| `API Key` | `sk-sp-xxxx` | Token Plan 专属密钥，生成后仅显示一次；**不可复用 Coding Plan 或百炼 `sk-` 密钥** |
| `Authorization Header` | `Bearer sk-sp-xxxx` | 与标准 OpenAI/Anthropic 格式一致，无需额外前缀 |

> **注意**：原始文档中“更多工具”链接指向 [更多工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide.md)，但该文件当前为空白页（HTTP 200 + 空内容），实际可用工具应以主文档所列 11 项为准，避免依赖此链接。

## 使用方式

1. 在目标工具（如 Qoder 或 Trae）的设置页中，选择「自定义 API」或「Local LLM」模式；
2. 填写对应协议的 Base URL（见上表），并粘贴 `sk-sp-` 开头的 API Key；
3. 保存配置后发起测试请求（例如发送 `"Hello"`）；
4. 验证响应状态码为 `200` 且含有效 `choices[0].message.content` 字段。

推荐首次调试时使用 `curl` 快速验证：
```bash
curl -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer sk-sp-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## 限制和注意事项

- **严格绑定关系**：Token Plan API Key（`sk-sp-`）**必须且只能**搭配文档中指定的两个 Base URL 使用；混用 Coding Plan 或百炼 Base URL 将导致 401/403 错误或意外按量扣费（详见 [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md)）。
- **地域限制**：当前 Base URL 仅支持 `cn-beijing` 地域，不支持跨地域调用（如从上海节点发起请求会失败）。
- **无代理转发支持**：Token Plan 不提供反向代理或网关层路由能力，客户端必须直连上述域名。
- **Key 安全**：API Key 无控制台续期或重置功能，丢失后需重新生成并更新所有客户端配置。

## 来源文档

- [接入AI工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool.md)


