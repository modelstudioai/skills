# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一 Runtime 运行，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音对话分析、客服机器人、数据挖掘、深度搜索、UI 自动化等场景。例如，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成 ASR + NLU + 摘要生成流水线；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖多模态视觉理解与动作规划模型；[通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 则组合检索增强与推理模型。所有应用的功能边界和输入输出格式以对应子文档为准。

## 关键参数

各应用通过 `app_id` 唯一标识，调用时需传入标准化参数：  
- `input`: JSON 对象，结构由具体应用定义（如 `{"query": "...", "image_url": "..."}`）；  
- `parameters`: 可选运行时配置，常见字段包括 `temperature`（仅部分文本类应用支持）、`max_output_tokens`、`enable_citation`（用于深度搜索类应用）；  
- `stream`: 布尔值，控制是否启用流式响应（当前仅 [千问联网检索Agent](../../raw/application-user-guide/application-gallery/web-search-agent.md) 和 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 完全支持）。  
> **注意**：`temperature` 参数在 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md) 文档中标注为“不生效”，但 [通义点金](../../raw/application-user-guide/application-gallery/tongyi-dianjin.md) 文档仍列出其为可调项——实际调用中该参数对法睿类法律推理应用无效，请以运行时返回的 `supported_parameters` 字段为准。

## 使用方式

1. 在百炼控制台「应用广场」页浏览并复制目标应用的 `app_id`；  
2. 调用 `POST /v1/applications/{app_id}/chat` 接口（需携带 `Authorization: Bearer <api_key>`）；  
3. 请求体示例：
   ```json
   {
     "input": {"query": "解释牛顿第一定律"},
     "parameters": {"max_output_tokens": 512}
   }
   ```
4. 响应含 `output` 字段（结构化结果）及 `usage` 字段（token 消耗统计）。  
详细接口规范见 [官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md) 的「API 调用示例」章节。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含文本+图像+音频 base64）；  
- 多模态应用（如 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)）要求图像尺寸 ≤ 2048×2048，音频时长 ≤ 300 秒；  
- 所有应用默认启用平台级风控，敏感词过滤与内容安全校验不可绕过；  
- 应用 ID 全局唯一但**不跨环境复用**：测试环境 `app_id` 无法在生产环境直接调用，需重新发布；  
- 部分应用（如 [伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）依赖实时语音流，仅支持 WebSocket 接入，不支持 HTTP 同步调用。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


