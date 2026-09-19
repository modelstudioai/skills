# security guide

百炼平台提供多层次安全防护能力，覆盖模型调用、Agent 资产管理、策略配置与风险审计等关键环节。开发者可通过控制台、CLI 或 API 集成安全策略，确保生产环境符合企业合规要求。所有安全功能均默认启用基础防护，高级策略需显式配置。

## 支持的模型/功能

- 所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio）均支持请求级内容安全检测（含敏感词过滤、涉政/暴恐/色情识别）  
- Agent 框架内置资产隔离机制，支持按工作空间粒度划分敏感数据访问边界  
- 安全策略模块支持自定义规则组，可联动 [防护总览](../../raw/application-user-guide/security-guide.md) 中的实时风险仪表盘进行闭环响应  

## 关键参数

- `security_level`: 可选 `basic` / `standard` / `strict`，控制内容检测强度（默认 `basic`）  
- `audit_enabled`: 布尔值，启用后记录完整请求/响应日志至审计中心（见 [风险与审计](../../raw/application-user-guide/security-guide.md)）  
- `policy_id`: 引用已创建的安全策略 ID，需通过 [安全策略](../../raw/application-user-guide/security-guide.md) 接口预配置  

## 使用方式

- **API 调用**：在请求 Header 中添加 `X-Bailian-Security-Level: strict`，或在 JSON body 中传入 `security_level` 字段  
- **CLI 工具**：使用 `bailian security enable --policy-id pol-xxx --workspace ws-yyy` 启用策略（详见 [使用 CLI](../../raw/application-user-guide/security-guide.md)）  
- **Agent 配置**：在 `agent.yaml` 中声明 `security: { policy_id: "pol-xxx" }`，策略将自动应用于该 Agent 全部[函数调用](../concepts/function-calling.md)  

## 限制和注意事项

- 单次请求最大文本长度受安全检测引擎限制：`strict` 模式下不超过 8192 字符，超长内容将被截断并返回警告  
- `audit_enabled=true` 时，日志保留周期为 90 天，不支持自定义延长（计费细节见 [计费说明](../../raw/application-user-guide/security-guide.md)）  
- > **注意**：原始文档中 [API 参考](../../raw/application-user-guide/security-guide.md) 列出的 `v1/security/scan` 接口已于 v2.3.0 版本废弃，当前统一由 `/v1/chat/completions` 的 `security_level` 参数替代，旧接口调用将返回 `410 Gone`。

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


