# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型；[通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 则组合检索增强与推理模型协同工作。

> **注意**：部分文档中提及的“支持 Qwen1.5 系列模型”已过时——自 v2.3.0 起，所有新上架应用默认使用 Qwen2 或 Qwen2.5 系列，旧模型仅限存量应用兼容运行，详见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的版本说明章节。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（可在控制台应用详情页获取）；
- `input`：JSON 对象，结构由具体应用定义（如 `{"query": "..."}` 或 `{"audio_url": "..."}`）；
- `parameters`（可选）：用于覆盖应用默认配置，常见字段包括 `temperature`（仅对 LLM 驱动型应用生效）、`max_output_tokens`、`enable_citation`（启用引用溯源）等；
- `stream`（布尔值）：是否启用流式响应（仅部分应用支持，如 `web-search-agent` 和 `ui-agent`）。

## 使用方式

1. **控制台调用**：进入「应用广场」页面，点击目标应用 → 「在线调试」，填写 input 并提交；
2. **OpenAPI 调用**：使用 `POST /v1/applications/{app_id}/invoke` 接口，需携带 `Authorization: Bearer <api_key>`；
3. **SDK 调用（Python）**：
   ```python
   from alibabacloud_bailian20231229 import models as bailian_models
   client = BailianClient(...)
   req = bailian_models.InvokeApplicationRequest(
       app_id="app-xxx",
       input={"query": "解释量子纠缠"},
       parameters={"enable_citation": True}
   )
   resp = client.invoke_application(req)
   ```

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含 base64 编码后的二进制内容）；
- 音频/视频类应用（如 `official-application-aipodcast.md`）要求输入 URL 可被百炼服务端直连访问，不支持私有内网地址或临时失效签名；
- 所有应用默认启用风控策略，高频调用可能触发限流（具体阈值见各应用详情页的「配额说明」）；
- 应用间**不共享上下文状态**，若需会话保持，请自行维护 `session_id` 并在 `parameters` 中透传（部分应用如 `lingque-ccai-voice-dialogue-robot` 显式支持该字段）。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


