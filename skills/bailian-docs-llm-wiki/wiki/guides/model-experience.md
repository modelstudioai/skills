# model experience

模型体验（Model Experience）是百炼平台提供的统一交互界面，用于快速试用、调试和评估各类大模型能力。开发者可通过该功能在不编写代码的前提下验证模型效果，也可结合 API 进行集成开发。所有体验功能均基于平台托管的标准化模型服务，支持[多模态](../concepts/multi-modal.md)输入与输出。

## 支持的模型与功能

当前模型体验支持以下核心能力类别（按模态与任务划分）：
- 文本生成（如 Qwen 系列大语言模型）
- 视觉理解（如 Qwen-VL、Qwen2-VL）
- 图片生成与编辑（如 Wanx 图像生成、Inpainting）
- 视频生成与编辑（如 Tongyi Video）
- 3D 模型生成（如 TripoSR）
- 语音合成（TTS）、语音识别（ASR）、语音转语音（V2V）
- 音乐生成（FunMusic）
- 全模态理解与生成（Omni-modal）
- 向量嵌入（Embedding）与重排序（Rerank）

完整能力列表详见 [模型体验](../../raw/model-user-guide/model-experience.md)。部分新上线模型（如 Qwen2.5-VL）可能尚未在该文档中体现，建议同步查阅 [视觉理解](../../raw/model-user-guide/vision-model.md) 获取最新支持情况。

## 关键参数

各模型体验页面提供可调参数，常见参数包括：
- `temperature`：控制输出随机性（0.0–1.0，默认 0.8）
- `top_p`：核采样阈值（0.1–1.0，默认 0.95）
- `max_tokens`：最大生成长度（因模型而异，文本类通常 ≤ 8192）
- `seed`：固定随机种子（启用 deterministic 输出）
- [多模态](../concepts/multi-modal.md)任务特有参数：如图像分辨率（`size`）、步数（`steps`）、引导强度（`guidance_scale`）

> **注意**：部分参数（如 `repetition_penalty`）在 [文本生成](../../raw/model-user-guide/text-generation.md) 中明确支持，但在 [模型体验](../../raw/model-user-guide/model-experience.md) 的 UI 描述中未列出——实际 API 调用仍可用，UI 可能滞后更新。

## 使用方式

1. 登录百炼控制台 → 进入「模型体验」页；
2. 选择目标模型类型（如“文本生成”或“图片生成”），再选择具体模型（如 `qwen-max` 或 `wanx-1.0`）；
3. 在输入区填写 [prompt](prompt.md) / 上传文件（图片/音频等），调整参数后点击「运行」；
4. 查看结果并复制请求体（JSON）或 cURL 命令，用于后续 API 集成。

所有体验操作均对应标准 RESTful API，请求结构与 [模型体验](../../raw/model-user-guide/model-experience.md) 中描述的 schema 一致，可直接复用于生产环境。

## 限制和注意事项

- 免费体验调用有配额限制（如每小时 50 次文本生成、每日 10 次视频生成），超出后需绑定计费项；
- 视频与 3D 生成任务耗时较长（通常 30s–5min），不支持超时中断；
- 输入内容需符合内容安全规范，违规文本/图像将被拦截并返回 400 错误；
- [多模态](../concepts/multi-modal.md)联合任务（如图文混合问答）仅在标注为「全模态」的模型中支持，普通 VL 模型不兼容跨模态 [prompt](prompt.md) 格式；
- 所有体验功能默认使用模型最新稳定版本，若需指定版本（如 `qwen-turbo-20240601`），须通过 API 显式传参，UI 不提供版本下拉选项。

## 来源文档

- [模型体验](../../raw/model-user-guide/model-experience.md)


