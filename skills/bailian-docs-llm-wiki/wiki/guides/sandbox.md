# sandbox

sandbox 是百炼平台提供的隔离式模型运行环境，用于安全、可控地测试和调试大模型应用逻辑。它支持按需创建独立实例，隔离资源与上下文，适用于开发验证、A/B 测试及敏感数据沙箱推理等场景。所有 sandbox 实例均基于平台统一的模型服务层构建，行为与线上部署一致。

## 支持的模型与功能

- 支持全部已接入百炼平台的通用大模型（如 Qwen 系列、Qwen2-VL、Qwen3）及部分定制化微调模型（需开通白名单）  
- 支持完整对话链路：流式响应、工具调用（Function Calling）、多轮上下文管理、系统提示词（system [prompt](prompt.md)）注入  
- 支持模板化配置：可通过 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) 预置 [prompt](prompt.md) 结构、参数组合与后处理规则  
- 不支持模型训练、微调或权重导出；仅提供推理服务接口  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `sandbox_id` | string | 是 | 沙箱实例唯一标识，由 `POST /v1/sandboxes` 创建后返回 |
| `model` | string | 是 | 模型 ID（如 `qwen-max`, `qwen-plus`），必须为 sandbox 环境已启用的模型列表中的项 |
| `temperature` | float | 否 | 默认 `0.7`，取值范围 `[0.0, 2.0]`；注意该参数在 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 中明确要求不可超过 `1.5`，超出将被截断并静默修正为 `1.5` |
| `max_tokens` | int | 否 | 默认 `2048`，最大允许 `8192`；超过限制将触发 `400 Bad Request` |
| `enable_search` | bool | 否 | 默认 `false`；启用后可调用内置搜索插件（仅限部分模型支持） |

> **注意**：`temperature` 参数上限在 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 中标注为 `2.0`，但实际 SDK 行为以 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 为准——该文档明确声明服务端强制截断至 `1.5`，开发者应以此为实际约束。

## 使用方式

1. **创建沙箱实例**：调用 `POST /v1/sandboxes`，传入模型 ID 与初始配置，获取 `sandbox_id`  
2. **发起推理请求**：向 `POST /v1/sandboxes/{sandbox_id}/chat/completions` 提交消息数组（含 `system`/`user`/`assistant` 角色）  
3. **销毁实例（可选）**：调用 `DELETE /v1/sandboxes/{sandbox_id}` 释放资源；未显式销毁的实例将在空闲 30 分钟后自动回收  
详细流程见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)

## 限制和注意事项

- 单 sandbox 实例生命周期最长 24 小时，超时后自动终止且不可恢复  
- 每个账号默认最多并发 5 个活跃 sandbox 实例；如需扩容，须提交工单申请  
- 所有请求受平台全局速率限制（RPS）约束，与普通 API 共享配额，具体阈值参见 [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md) 中最新版本说明  
- 不支持跨 sandbox 实例共享 session 或 state；每个实例完全隔离  
- 日志仅保留最近 7 天，调试建议自行捕获 `request_id` 并关联业务日志

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


