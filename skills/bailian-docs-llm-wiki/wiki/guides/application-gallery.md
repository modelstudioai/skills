# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音对话理解；  
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面自动化操作；  
- `千问联网检索Agent` 集成 Qwen-Plus 与实时搜索插件，提供带引用的动态知识响应。  
完整列表见 [应用广场](../../raw/application-user-guide/application-gallery.md)，各子应用详情页（如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)、[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md)）包含具体能力说明与输入输出 Schema。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tingwu-agent`, `ui-agent`），可在控制台或 [应用广场](../../raw/application-user-guide/application-gallery.md) 文档中查得；  
- `input`：JSON 对象，结构依应用而异（例如 `tingwu-agent` 要求 `audio_url` 字段，`ui-agent` 要求 `screenshot_base64` 与 `instruction`）；  
- `timeout`：最大执行时长（单位秒），默认 120，部分长流程应用（如 `tongyi-deepsearch`）建议设为 300+。  
> **注意**：`web-search-agent` 的 `max_results` 参数在 [官方应用-千问联网检索Agent](../../raw/application-user-guide/application-gallery/web-search-agent.md) 中定义为整数，但实际 API 接收字符串类型，调用时需显式转为字符串，否则返回 400 错误。

## 使用方式

1. **控制台调用**：进入「应用广场」页面，选择目标应用 → 「在线调试」填写 input JSON → 执行；  
2. **API 调用**：使用 `POST /v1/applications/{app_id}/invoke`，Header 携带 `Authorization: Bearer <api_key>`；  
3. **SDK 集成**：Python SDK 示例见 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 文档末尾代码片段，其他应用参数结构一致，仅需替换 `app_id` 与 `input`。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含 base64 编码图像/音频）；  
- 免费试用额度覆盖前 50 次/日调用，超出后按 [应用广场](../../raw/application-user-guide/application-gallery.md) 中公示的计费规则扣费；  
- 所有应用不支持跨区域调用（如华东 region 创建的应用不可由华北 endpoint 调用），region 必须与应用部署 region 严格一致；  
- `tongyi-farui` 与 `xiyan-gbi` 应用当前仅开放白名单用户访问，未授权账号调用将返回 `403 Forbidden`。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


