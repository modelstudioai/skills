# security guide

百炼平台提供面向大模型应用的端到端安全防护能力，覆盖输入过滤、输出拦截、策略编排与风险审计等关键环节。所有安全能力通过统一策略引擎驱动，支持在 API 调用、Agent 构建及 CLI 工具链中按需启用。开发者需明确各能力的适用范围与约束条件，以确保合规、可控地集成安全机制。

## 支持的模型/功能

当前安全防护能力适用于以下模型与功能场景：
- 所有百炼托管的 **基础大模型**（如 Qwen 系列、Qwen2 系列）及 **推理模型**（含自定义 LoRA 微调模型），但不支持第三方模型接入后的实时内容过滤；
- **Agent 编排流程** 中的节点级输入/输出校验（参见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）；
- **批量异步任务** 的全链路风险扫描（需显式启用 `audit_mode=full`）；
- 不支持对 **Embedding 模型** 或 **Rerank 模型** 的请求内容进行语义级安全检测。

> **注意**：文档 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 中提及“支持所有模型类型”的描述已过时，实际限制以本节为准。

## 关键参数

安全策略通过以下核心参数控制行为：

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `security_policy_id` | string | 指定预置或自定义安全策略 ID；空值表示禁用防护 | `null` |
| `input_filter` | boolean | 是否启用输入敏感词/恶意指令过滤 | `true` |
| `output_filter` | boolean | 是否启用输出涉政、违法、色情等高危内容拦截 | `true` |
| `audit_level` | enum: `none`, `basic`, `full` | 审计粒度，影响日志保留与风险溯源能力 | `basic` |

完整参数定义请参考 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) 中 `POST /v1/chat/completions` 的 `security` 对象字段说明。

## 使用方式

### 方式一：API 调用（推荐）
在请求体中嵌入 `security` 对象：
```json
{
  "model": "qwen-max",
  "messages": [...],
  "security": {
    "security_policy_id": "sp-xxx",
    "input_filter": true,
    "output_filter": true,
    "audit_level": "full"
  }
}
```

### 方式二：CLI 工具
使用 `bailian-cli` v2.3.0+，通过 `--security-policy-id` 和 `--audit-level` 选项启用：
```bash
bailian chat --model qwen-plus \
  --security-policy-id sp-xxx \
  --audit-level full \
  --message "你好"
```
详细命令说明见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

## 限制和注意事项

- 单次请求中 `security_policy_id` 必须存在且有效，否则请求将被拒绝（HTTP 400），**不降级为默认策略**；
- 启用 `output_filter=true` 时，若检测到高危内容，响应返回 `{"error": {"code": "content_blocked", ...}}`，**不会返回原始模型输出**；
- 安全策略生效延迟 ≤ 200ms（P95），但 `audit_level=full` 会额外增加约 300–800ms 延迟；
- 所有安全事件日志默认保留 90 天，超期自动清理；如需长期归档，须调用 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 接口导出；
- 不支持在流式响应（`stream=true`）中实时拦截输出片段——仅在流结束时做最终校验。

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


