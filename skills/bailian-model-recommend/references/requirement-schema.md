# 需求提取 JSON 结构

从用户描述中快速提取以下结构（纯内部使用，不展示给用户）：

```json
{
  "complexity": "single 或 pipeline",
  "inputModality": ["Text", "Image", "Video", "Audio"],
  "outputModality": ["Text", "Image", "Video", "Audio"],
  "requiredCapabilities": ["TG", "VU", "IG", "VG", "TTS", "ASR", ...],
  "requiredFeatures": ["function-calling", "web-search", "structured-outputs"],
  "budget": "low / medium / high",
  "contextNeed": "standard / large / extra-large",
  "qualityPreference": "flagship / balanced / cost-optimized",
  "segments": [{"step": "...", "inputModality": [...], "outputModality": [...], "requiredCapabilities": [...]}]
}
```

## 字段说明

| 字段 | 说明 |
| --- | --- |
| complexity | 单模型完成(single) 或 多模型协同(pipeline) |
| inputModality | 输入模态：Text / Image / Video / Audio |
| outputModality | 输出模态 |
| requiredCapabilities | 所需能力代码（见 [capability-codes.md](capability-codes.md)） |
| requiredFeatures | 所需特性（function-calling / web-search / structured-outputs 等） |
| budget | 预算倾向：low / medium / high |
| contextNeed | 上下文需求：standard / large / extra-large |
| qualityPreference | 质量偏好：flagship / balanced / cost-optimized |
| segments | pipeline 场景下每个步骤的模态和能力需求 |

## 推断规则

偏好推断见 [capability-codes.md](capability-codes.md) 中的"偏好推断规则"。
