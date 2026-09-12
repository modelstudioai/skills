# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态解决方案。所有应用均基于通义系列大模型构建，支持一键部署、参数微调与 API 集成。应用列表持续更新，具体能力以 [原文标题](../../raw/application-user-guide/application-gallery.md) 中所列为准。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与功能定位，例如：
- **通义法睿**：面向法律场景的推理与文书生成，底层调用 `qwen-law-7b` 或 `qwen-law-72b`（视实例规格而定）；
- **通义听悟Agent**：集成语音识别（ASR）、语义理解与对话生成，依赖 `qwen-audio-7b` 及配套 Whisper 模型；
- **通义 UI Agent**：支持截图理解与自动化操作，需 `qwen-vl-plus` 多模态模型支撑；
- **千问联网检索Agent**：结合 RAG 与实时网络搜索，底层调用 `qwen-max` 或 `qwen-plus`（取决于配置）。

全部官方应用及其对应模型能力详见 [原文标题](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

各应用在部署时可配置以下通用参数（部分应用支持扩展参数）：
- `temperature`: 控制输出随机性，范围 `[0.0, 2.0]`，默认 `0.7`；
- `max_tokens`: 生成长度上限，最大值因应用而异（如通义点金为 `4096`，通义深度搜索为 `8192`）；
- `top_p`: 核采样阈值，默认 `0.95`；
- `enable_search`: 仅适用于联网类应用（如千问联网检索Agent），布尔值，默认 `false`；
- `input_schema`: 多模态应用（如通义 UI Agent）需显式声明输入结构（如 `{"screenshot": "base64", "instruction": "string"}`）。

参数兼容性与取值范围请严格参照 [原文标题](../../raw/application-user-guide/application-gallery.md) 所示应用详情页说明。

## 使用方式

1. **控制台部署**：登录百炼控制台 → 进入「应用广场」→ 点击目标应用卡片 → 「立即部署」→ 选择环境与规格 → 完成发布；
2. **API 调用**：部署后获取 `app_id`，通过 `/v1/apps/{app_id}/chat` 接口发送 JSON 请求体（含 `messages` 和可选 `parameters`）；
3. **SDK 集成**：使用 `dashscope` Python SDK 时，调用 `Application.call(app_id=..., input={...}, parameters={...})`；
4. **自定义微调**：部分应用（如析言GBI、伶鹊CCAI 系列）支持上传私有知识库并启用 `retrieval_enabled: true`。

> **注意**：原始文档未说明是否所有应用均支持 SDK 的 `Application.call` 方式；实际开发中请以 [原文标题](../../raw/application-user-guide/application-gallery.md) 中各应用详情页的「接入方式」章节为准，避免假设通用接口行为。

## 限制和注意事项

- 免费试用额度仅覆盖前 3 个部署应用，超出后需绑定计费项；
- 多模态应用（如通义拍照解题辅导、通义 UI Agent）对输入图像尺寸/格式有硬性约束（如 PNG/JPEG，≤10MB，分辨率 ≤4096×4096）；
- 通义音频播客生成暂不支持自定义音色切换，仅限平台预置 TTS 声音；
- 所有应用的 `system_prompt` 不可覆盖，若需定制角色设定，须通过 `messages[0].content` 显式传入；
- 应用间存在模型复用但能力隔离，例如通义听悟Agent 与通义音频播客生成虽共用 `qwen-audio-7b`，但前者禁用语音合成，后者禁用语音识别。

请始终以 [原文标题](../../raw/application-user-guide/application-gallery.md) 列出的最新链接跳转至帮助中心，确认各应用当前支持的模型版本与功能边界。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


