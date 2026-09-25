# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义听悟Agent` 基于 Qwen-Audio 模型，支持语音转写、会议摘要与发言分析；
- `通义 UI Agent` 依赖 Qwen-VL + Qwen2.5-72B，实现网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen2.5-72B 与实时搜索插件，支持动态知识增强推理。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。部分应用（如 `析言GBI` 和 `通义法睿`）还提供领域微调模型版本，需在创建实例时显式指定模型 ID。

> **注意**：`伶鹊CCAI-语音对话机器人` 文档中声明支持流式语音输入，但 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md) 当前未公开流式 API 接口定义，实际调用需使用非流式 `POST /v1/applications/{app_id}/chat`；该不一致已在内部工单 #BL-2024-883 中标记待同步。

## 关键参数

调用任一应用时，必须传入以下核心参数：
- `app_id`：应用唯一标识（可在控制台「应用广场」页获取）；
- `input`：结构化输入对象，格式因应用而异（如 `tongyi-dianjin` 要求 `{"stock_code": "600519", "period": "Q3"}`，而 `ui-agent` 要求 `{"screenshot_base64": "...", "instruction": "点击登录按钮"}`）；
- `stream`（可选）：布尔值，仅部分应用（如 `web-search-agent`、`tongyi-deepsearch`）支持 true 值启用 SSE 流式响应。

完整参数规范请参考各应用专属文档，例如 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 明确要求 `query` 字段为必填字符串，且长度 ≤ 512 字符。

## 使用方式

1. **控制台接入**：进入百炼控制台 → 应用管理 → 应用广场 → 选择目标应用 → 点击「立即使用」生成实例；
2. **API 调用**：使用 `POST https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/chat`，携带 `Authorization: Bearer <api_key>` 及 JSON body；
3. **SDK 调用**（Python 示例）：
   ```python
   from dashscope import Application
   resp = Application.call(app_id='app-xxx', input={'query': '2024年Q2营收'}, api_key='sk-xxx')
   ```

所有应用均遵循统一鉴权与限流策略，详细调用流程见 [应用广场](../../raw/application-user-guide/application-gallery.md) 的「快速开始」章节。

## 限制和注意事项

- 单应用实例默认 QPS 限制为 5，可通过提交工单申请提升；
- `通义音频播客生成` 和 `通义多模态翻译` 不支持自定义模型替换，仅允许调整 [prompt](prompt.md) 模板；
- 输入内容含敏感信息（如身份证号、银行卡号）将触发平台自动脱敏，可能导致输出异常——建议前置清洗；
- 所有应用均不支持跨区域调用（如华东1区创建的应用不可通过华北2区 endpoint 访问），该约束在 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md) 中有明确说明。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


