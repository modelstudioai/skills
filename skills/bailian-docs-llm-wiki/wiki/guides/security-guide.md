# security guide

百炼平台提供多层次的安全防护能力，覆盖模型调用、Agent 资产管理、策略配置与风险审计等关键环节。开发者可通过控制台、CLI 或 API 配置安全策略，实现细粒度访问控制与敏感操作留痕。所有安全能力均默认启用基础防护，高级功能需按需开启并遵循最小权限原则。

## 支持的模型/功能

- 所有百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio）均支持请求级内容安全检测（含涉政、暴恐、色情、违禁等维度）  
- Agent 开发场景下，支持对工具调用输入/输出、记忆存储、知识库检索结果进行实时内容过滤与脱敏  
- 安全策略可作用于模型 API、Agent SDK、工作流编排节点三类入口，具体能力详见 [Security (raw/application-user-guide/security-guide.md)](../../raw/application-user-guide/security-guide.md)  

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `security_policy_id` | string | 指定已创建的安全策略 ID，用于绑定到模型服务或 Agent 实例 | `default`（基础过滤策略） |
| `enable_audit_log` | boolean | 是否开启操作审计日志（含输入 [prompt](prompt.md)、输出响应、策略匹配结果） | `false` |
| `sensitive_word_masking` | boolean | 是否对检测出的敏感词执行掩码（如 `***`）而非拦截 | `true`（仅限非阻断型策略） |

> **注意**：`sensitive_word_masking` 在 [Security (raw/application-user-guide/security-guide.md)](../../raw/application-user-guide/security-guide.md) 的 CLI 示例中被标记为必填项，但实际 API 文档 [API 参考](https://help.aliyun.com/zh/model-studio/security/api) 明确其为可选字段，以 API 文档为准。

## 使用方式

- **控制台**：在「模型服务」或「Agent 管理」页面，编辑实例 → 「安全设置」页签 → 选择策略并启用审计  
- **CLI**：使用 `bailian security attach --model-id <id> --policy-id <pid>` 绑定策略，详情见 [使用 CLI](https://help.aliyun.com/zh/model-studio/security/cli) —— 该文档路径已在 [Security (raw/application-user-guide/security-guide.md)](../../raw/application-user-guide/security-guide.md) 中列出  
- **API**：调用 `UpdateModelService` 或 `UpdateAgent` 接口，传入 `SecurityConfig` 对象（参考 [API 参考](https://help.aliyun.com/zh/model-studio/security/api)）

## 限制和注意事项

- 单个安全策略最多关联 50 个模型服务或 Agent 实例  
- 审计日志保留周期为 90 天，不可延长；日志内容不包含原始 token 流，仅记录最终输入/输出文本  
- 启用 `enable_audit_log` 后，单次请求延迟增加约 50–200ms（取决于策略复杂度），高并发场景需评估性能影响  
- 策略中的自定义关键词库大小上限为 10MB，且仅支持 UTF-8 编码纯文本文件上传

## 来源文档

- [Security](../../raw/application-user-guide/security-guide.md)


