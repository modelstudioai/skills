# security guide

百炼平台提供面向大模型应用的端到端安全防护能力，覆盖输入过滤、输出拦截、策略编排与风险审计等关键环节。开发者可通过控制台、CLI 或 API 集成安全策略，所有防护均默认启用基础规则，支持按需定制。安全机制深度集成于模型调用链路中，无需修改业务代码即可生效。

## 支持的模型/功能

当前安全防护能力适用于所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），并覆盖以下核心功能：  
- 输入内容安全检测（含文本、图像、音频多模态输入）  
- 输出内容安全拦截（防止越狱、有害生成、隐私泄露）  
- Agent 资产级防护（如工具调用白名单、敏感函数禁用）  
- 实时风险审计日志与合规报告导出  

> **注意**：部分旧版文档（如 [Security](../../raw/application-user-guide/security-guide.md) 中“防护总览”章节）仍将安全能力限定于文本模型，该描述已过时；实际自 v2.3.0 起已全面支持多模态输入防护，详见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)。

## 关键参数

调用模型时，以下参数用于控制安全行为：  
- `safety_check: bool`（默认 `true`）：启用/禁用实时安全检测  
- `safety_level: string`（可选 `"basic"` / `"strict"` / `"custom"`）：指定防护强度，`"custom"` 需配合 `safety_policy_id` 使用  
- `safety_policy_id: string`：引用预置或自定义策略 ID，策略定义见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)  
- `audit_enabled: bool`（默认 `false`）：开启后记录完整请求/响应及拦截原因，用于审计追溯  

## 使用方式

- **API 调用**：在 `messages` 或 `input` 字段同级传入上述安全参数，例如：  
  ```json
  { "model": "qwen-max", "input": { "text": "..." }, "safety_level": "strict", "audit_enabled": true }
  ```  
- **CLI 工具**：使用 `bailian security enable --level strict --policy <id>` 启用策略，并通过 `bailian chat --safety-check` 触发检测，详情参见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。  
- **控制台配置**：在「应用设置 → 安全策略」中为整个应用或单个 Agent 绑定策略，策略生效后自动注入所有 API 调用。

## 限制和注意事项

- 单次请求中 `safety_policy_id` 仅支持指定一个策略；若需组合多策略，须提前在 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 中创建复合策略。  
- `safety_check: false` 仅允许在测试环境临时关闭，生产环境强制校验且该参数将被忽略。  
- 图像/音频输入的安全检测延迟略高于纯文本（平均增加 150–300ms），高并发场景建议预留缓冲时间。  
- 审计日志保留周期为 90 天，超期自动清理；如需长期存档，请及时调用 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) 中的 `/v1/audit/export` 接口导出。

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


