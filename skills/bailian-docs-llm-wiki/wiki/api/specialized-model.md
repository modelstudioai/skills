# specialized model

专用模型（Specialized Model）是针对特定垂直场景或复杂任务链路深度优化的大语言模型集合。平台提供涵盖深度研究、光学字符识别、机器翻译及桌面界面自动化等场景的垂直能力。开发者可通过标准 API 接口直接集成，以高精度、低延迟的方式快速构建专业化 AI 应用。

## 支持的模型与核心功能
- **Qwen-Deep-Research**：面向深度信息检索与分析。支持多阶段研究规划、实时网络搜索、自动反问澄清与结构化长报告生成。详细输入输出规范参考 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)。
- **Qwen-OCR**：面向高精度图像文字提取。支持复杂版面解析、票据/证件等场景的结构化信息抽取，允许通过 Prompt 控制 JSON 输出格式。参数细节见 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)。
- **Qwen-MT**：面向企业级机器翻译。支持多语言互译，内置术语强制对齐（`terms`）、翻译记忆库匹配（`tm_list`）及领域风格提示（`domains`）等高级控制参数。接口说明见 [Qwen-MT API 参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)。
- **GUI-Plus**：面向桌面 GUI 自动化交互。通过理解屏幕截图生成标准化的键鼠操作指令（点击、拖拽、输入、滚动等），适用于智能体（Agent）自动化流。

## 关键参数说明
专用模型遵循通用大模型请求基线，但在上下文构造与扩展参数上存在差异化设计：
- `model` (string, 必选)：模型标识符。需准确传入对应版本，如 `qwen-deep-research`、`qwen-vl-ocr-latest`、`qwen-mt-plus`、`gui-plus-2026-02-26`。
- `messages` (array, 必选)：对话上下文数组。视觉类模型需在 `content` 中声明 `type: "image_url"`；多阶段任务模型需严格保持 `user`/`assistant` 角色交替。
- `translation_options` (object, Qwen-MT 特有)：包含基础翻译参数 `source_lang`、`target_lang`，支持扩展传入术语对、记忆库片段及领域描述字符串。
- `output_format` (string, Deep-Research 特有)：控制报告体量。`model_detailed_report`（默认，约 6000 Token）或 `model_summary_report`（精简版，1500-2000 Token）。
- `extra_body` (object)：[[openai-compatible]] 接口下的自定义扩展字段。如 GUI-Plus 需传入 `{"vl_high_resolution_images": true}` 以启用高分屏解析。

## 使用方式
- **协议与 SDK 差异**：Qwen-Deep-Research 当前仅支持通过 [[dashscope-sdk]] (Python) 调用，暂不开放 Java SDK 与 [[openai-compatible-api|OpenAI 兼容接口]]。其余三款模型均完整支持 OpenAI Chat Completions 格式，可使用官方 Python/Node.js SDK 或 HTTP/curl 直连。
- **地域路由配置**：OpenAI 兼容模式需根据业务地域替换 `base_url`。中国大陆版使用 `https://dashscope.aliyuncs.com/compatible-mode/v1`，新加坡/美国弗吉尼亚需切换至对应 `intl` 或 `us` 域名。
- **流式响应处理**：开启 `stream: true` 后，响应体按数据块返回。Deep-Research 会动态输出 `phase` 状态（`ResearchPlanning` → `WebResearch` → `KeepAlive` → `answer`），前端需根据状态解析进度。使用 OpenAI SDK 时，建议配置 `stream_options: {"include_usage": true}` 以获取最终 Token 计量。
- **多阶段调用范式 (Deep-Research)**：采用“请求-澄清-生成”两步法。首次请求后捕获 `step1_content`（模型反问），将用户补充意图与历史消息拼接后发起第二次调用，触发完整研究链路。

## 限制与注意事项
- **凭证与地域强绑定**：各地域的 [[api-key]] 独立签发且严格隔离。混用不同地域的 `base_url` 与密钥将直接返回鉴权失败。务必在百炼控制台对应区域获取凭证。
- **图像尺寸与缩放策略**：Qwen-OCR 与 GUI-Plus 对输入像素总量存在阈值限制（如 `min_pixels`/`max_pixels`）。超出范围的图像会自动缩放，极端情况可能影响细粒度 UI 控件或微小文字的识别精度。
- **SDK 兼容性现状**：平台专用模型目前未全面对齐 OpenAI 协议规范，部分高级特性仅支持 DashScope 原生 SDK。生产环境集成前需验证目标语言的客户端支持矩阵。

> **注意**：模型迭代频率较高，部分文档中关于响应体嵌套结构（如 `extra.deep_research.references` 字段）或默认行为可能存在版本差异。开发时建议优先依赖 SDK 的强类型校验，并实时监听 `status_code` 与 `finished_reason`。若捕获到非 200 状态，请直接解析 `code` 与 `message` 字段定位根因。

## 来源文档

- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)
- [Qwen-MT API 参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)

