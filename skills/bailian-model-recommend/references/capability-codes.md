# 数据字段取值枚举

> 长尾参考：SKILL.md「内联参考表」已含能力码与场景词，happy path 不需要读本文件。
> 这里给出目录数据里**实际观测到的全部枚举取值**，供手写 intent 或新增场景预设时核对。
> 所有取值随 `bailian-docs-llm-wiki` 数据更新会漂移，改预设前先重新核对。

## 能力代码 `capabilities[]`（17 个）

| 代码 | 含义 |
| --- | --- |
| TG | 文本生成 |
| Reasoning | 推理 |
| VU | 视觉理解 |
| IG | 图像生成 |
| VG | 视频生成 |
| TTS | 语音合成 |
| ASR | 语音识别 |
| TR | 翻译 |
| ME | 多模态嵌入 |
| 3D-generation | 3D 生成 |
| World-Model | 世界模型 |
| Multimodal-Omni | 全模态 |
| Realtime-Omni | 实时全模态 |
| Realtime-Chatting | 实时对话 |
| Realtime-ASR | 实时语音识别 |
| Realtime-Text-to-Speech | 实时语音合成 |
| Realtime-Audio-Translate | 实时音频翻译 |

## 模态取值（大小写敏感）

- `inferenceMetadata.request_modality`：`Audio` / `Image` / `Text` / `Video`
- `inferenceMetadata.response_modality`：`3D-Generation` / `Audio` / `Image` / `Text` / `Video`

## 特性 `features[]`（8 个）

`batch`、`cache`、`fine-tuning`、`function-calling`、`model-experience`、`prefix-completion`、`structured-outputs`、`web-search`

> `requiredFeatures` **不参与硬过滤**（引擎硬门只有模态 + 能力）。用户提出特性诉求时，
> 需在候选的 `specs.features` 里核对，并在推荐理由中明确说明是否满足。

## 档位 `profile.familyTier`

`flagship` / `balanced` / `lightweight`（缺失时按 `balanced` 与 `unknown` 之间处理）

## 调用方式 `profile.callModes[]`

`sync`（同步）/ `streaming`（流式）/ `async`（异步任务，需轮询）/ `realtime`（实时双工）

> 写示例代码时要与 callModes 一致：只有 `async` 的模型不能给同步返回的示例；
> 只有 `realtime` 的模型要走实时接口，不是 chat/completions。

## 场景词 `profile.scenes[]`

33 个，词表见 SKILL.md「内联参考表」。核对当前真实取值：

```bash
node scripts/recommend.mjs --list-scenes     # 输出 presets + catalogScenes
```

故意写错一个场景词也能拿到全量词表（脚本会在 `warnings.scene-no-match` 里回报
`availableScenes` 与 `suggestions`），不必手动 grep `models.jsonl`。

## 偏好推断规则

见 SKILL.md「偏好推断」表（唯一来源，此处不重复）。
