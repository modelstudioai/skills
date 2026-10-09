# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需自行搭建模型服务或编排工作流。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 全链路模型，专用于会议纪要生成与语音对话理解；  
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；  
- `千问联网检索Agent` 集成 Qwen-72B + 检索增强模块（RAG），实时调用搜索引擎接口完成事实性问答。  
全部应用能力详见 [应用广场](../../raw/application-user-guide/application-gallery.md) 的分类清单。

## 关键参数

调用任一应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，如 `tingwu-agent`、`ui-agent`，取值见 [应用广场](../../raw/application-user-guide/application-gallery.md) 中各子页面标题 |
| `input` | object | 是 | 输入结构体，schema 因应用而异（如 `web-search-agent` 要求 `{"query": "..."}`，`xiyan-gbi` 要求 `{"question": "...", "tables": [...]}`） |
| `timeout` | integer | 否 | 单位秒，默认 60，最大 300 |

> **注意**：`tongyi-farui` 与 `xiyan-gbi` 均宣称支持 SQL 生成，但前者仅接受法律文书文本输入并返回条款分析结果，后者明确要求结构化表元数据——二者输入 schema 不兼容，不可混用，具体以 [官方应用-析言GBI](../../raw/application-user-guide/application-gallery/xiyan-gbi.md) 文档为准。

## 使用方式

1. **获取 app_id**：从 [应用广场](../../raw/application-user-guide/application-gallery.md) 列表中确认目标应用的 ID（如 `lingque-ccai-dialogue-analysis-aio`）；  
2. **构造请求体**：参考对应子文档的 `input` 示例（如 [官方应用-伶鹊CCAI-对话分析AIO](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md) 中的 JSON Schema）；  
3. **调用 API**：向 `/v1/applications/{app_id}/invoke` 发送 POST 请求，携带 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`。

## 限制和注意事项

- 单次调用最大输入长度为 128KB（含附件 Base64 编码后），超出将返回 `413 Payload Too Large`；  
- 所有应用默认启用流式响应（`stream=true`），若需完整响应请显式设置 `stream=false`；  
- `tongyi-deepsearch` 与 `web-search-agent` 均依赖外部搜索服务，当网络策略禁止出向 HTTP(S) 请求时将失败，该行为未在 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 中明确说明，需开发者自行验证连通性。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


