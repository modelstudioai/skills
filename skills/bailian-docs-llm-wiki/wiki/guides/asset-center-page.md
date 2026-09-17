# asset center page

资产中心是百炼平台中统一管理、查看和调用各类模型资产（如大模型、微调模型、[插件](../concepts/plugin.md)、知识库等）的核心页面。开发者可通过该页面快速定位已部署或已授权的模型资源，配置运行参数并发起推理请求。所有资产均按权限隔离，确保多租户环境下的安全性与可控性。

## 支持的模型/功能

- 支持调用平台托管的**基础大模型**（如 Qwen 系列、Qwen2-VL）、**微调后模型**（Fine-tuned Model）、**自定义[插件](../concepts/plugin.md)（Plugin）** 及 **RAG 知识库绑定模型**  
- 提供模型元信息展示（版本、创建时间、[Token](../concepts/token.md) 用量统计）、在线调试（Chat Playground）、批量测试（Batch Inference）及 API 调用凭证生成  
- 支持通过 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 页面直接跳转至对应模型的详细配置页，包括 [prompt](prompt.md) 模板、系统指令、输出格式控制等  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 资产中心分配的唯一模型标识符，可在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的模型卡片右上角复制 |
| `temperature` | float | 否 | 默认 `0.8`，取值范围 `[0.0, 2.0]`；注意：部分微调模型不支持该参数，强制设置将被忽略（见 [原文标题](../../raw/model-user-guide/asset-center-page.md) 中“参数兼容性”章节） |
| `max_tokens` | integer | 否 | 默认 `1024`，最大值受模型上下文长度限制；超过时请求将被截断并返回 `400` 错误 |

> **注意**：原始文档中关于 `top_p` 的默认值描述存在矛盾——[原文标题](../../raw/model-user-guide/asset-center-page.md) 写为 `0.95`，但 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 实际接口返回默认值为 `1.0`。以接口实际行为为准，建议显式传参避免歧义。

## 使用方式

1. 登录百炼控制台 → 进入「模型服务」→ 点击「资产中心」  
2. 在列表中筛选目标模型，点击「调用」按钮进入 Playground 或「API 接入」页获取 SDK 示例与 cURL 命令  
3. 若需程序化调用，使用 `POST /v1/models/{model_id}/chat/completions` 接口，`Authorization` 头需携带平台颁发的 `Bearer <api_key>`（密钥在 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的「凭证管理」中生成）

## 限制和注意事项

- 单次请求输入文本长度上限为 128KB（含 system + user + history），超出将触发 `413 Payload Too Large`  
- 免费试用模型仅限开发测试，QPS 限流为 1，生产环境请升级至付费配额  
- 所有通过资产中心发起的请求均计入项目级 [Token](../concepts/token.md) 消耗统计，不可跨项目共享配额  
- 模型若处于「下线」或「禁用」状态，则无法在资产中心页面显示或调用（详见 [原文标题](../../raw/model-user-guide/asset-center-page.md) 的生命周期说明）

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


