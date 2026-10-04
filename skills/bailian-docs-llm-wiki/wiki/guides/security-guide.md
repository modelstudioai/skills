# security guide

百炼平台提供多层次的安全防护能力，覆盖模型调用、Agent 资产管理、策略配置与风险审计等关键环节。开发者可通过 API、CLI 或控制台集成安全策略，实现对敏感内容、越权行为和异常调用的实时拦截与审计。所有安全能力均默认启用基础防护，高级策略需显式配置。

## 支持的模型/功能

- 所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio）均内置内容安全过滤，支持文本、图像、音频多模态输入的风险识别  
- Agent 安全能力依赖 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md) 模块，需在创建 Agent 时绑定安全策略  
- 风险审计日志与策略执行记录可通过 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面查看，支持按时间、事件类型、策略 ID 过滤  

## 关键参数

- `safety_check`: 布尔值，默认 `true`；设为 `false` 可临时关闭内容安全检查（**仅限调试，生产环境禁止**）  
- `policy_id`: 字符串，指定生效的安全策略 ID；若未提供，则使用项目级默认策略  
- `audit_level`: 枚举值（`none` / `basic` / `detailed`），控制审计日志粒度；详见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) 中 `POST /v1/chat/completions` 的 `audit` 字段说明  

## 使用方式

- **API 调用**：在请求体中添加 `safety_check` 和 `policy_id` 字段，例如：
  ```json
  { "model": "qwen-max", "messages": [...], "safety_check": true, "policy_id": "pol-abc123" }
  ```
- **CLI 工具**：使用 `bailian security enable --policy-id pol-abc123` 启用策略，具体命令参考 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)  
- **控制台配置**：在「安全中心 → 策略管理」中创建/编辑策略，并在 Agent 配置页或项目设置中关联  

> **注意**：原始文档中 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md) 提到“策略可跨项目复用”，但 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 明确说明策略作用域为单项目，且不支持跨项目引用——请以后者为准，前者为过时描述。

## 限制和注意事项

- 单次请求最多绑定 1 个 `policy_id`；如需组合策略，须预先在控制台中创建复合策略  
- `safety_check: false` 仅跳过内容过滤，不豁免审计日志生成（`audit_level` 仍生效）  
- 图像/音频类请求的安全检测延迟比文本高约 200–500ms，高并发场景下建议预留缓冲  
- 计费逻辑与安全模块强耦合：即使未显式启用策略，基础内容过滤仍计入 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) 中的“安全处理单元”用量

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


