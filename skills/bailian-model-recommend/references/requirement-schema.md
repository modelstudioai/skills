# 需求提取 JSON 结构

从用户描述中快速提取以下结构（纯内部使用，不展示给用户），传给
`scripts/recall-rank.mjs` 做确定性召回排序。

```json
{
  "complexity": "single 或 pipeline",
  "inputModality": ["Text", "Image", "Video", "Audio"],
  "outputModality": ["Text", "Image", "Video", "Audio"],
  "requiredCapabilities": ["TG", "VU", "IG", "VG", "TTS", "ASR", ...],
  "requiredFeatures": ["function-calling", "web-search", "structured-outputs"],
  "matchedScenes": ["代码", "客服", "长文本", ...],
  "budget": "low / medium / high",
  "contextNeed": "standard / large / extra-large",
  "qualityPreference": "flagship / balanced / cost-optimized",
  "userIntent": "match / optimize / evaluate / differentiate",
  "optimizeDimension": "price / context / quality / speed（仅 optimize 时）",
  "modelPreference": {
    "mode": "unconstrained / scoped / comparison / alternative",
    "targets": ["qwen-max", "deepseek-v3"],
    "excludes": ["qwen"]
  },
  "segments": [
    { "step": "...", "inputModality": [...], "outputModality": [...], "requiredCapabilities": [...] }
  ]
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
| matchedScenes | 用户场景（**必须从模型数据实际存在的场景词中选**：`models.jsonl` 每行 `profile.scenes` 的取值集合；先采样 grep 再填，不要编造） |
| budget | 预算倾向：low / medium / high |
| contextNeed | 上下文需求：standard / large / extra-large |
| qualityPreference | 质量偏好：flagship / balanced / cost-optimized |
| userIntent | 用户意图类型，决定打分权重：match(找合适的) / optimize(按某维度优化) / evaluate(评估好坏) / differentiate(对比差异) |
| optimizeDimension | optimize 时的优化维度：price / context / quality / speed（**仅当用户明确说"按XX优化"才填**；"便宜点"是 budget:low 不是 optimizeDimension:price） |
| modelPreference | 用户点名/排除模型：comparison(对比指定模型) / alternative(要指定模型的替代品) / scoped(限定家族内选) / unconstrained(无约束) |
| segments | pipeline 场景下每个步骤的模态和能力需求 |

## matchedScenes 场景词表（43 个，目录实际取值）

matchedScenes 只能从以下词中选（数据 `profile.scenes` 的全集）：

3D生成、Agent编排、OCR文字识别、人脸人像、代码生成、创意写作、向量检索、
图像修复、图像生成、图像编辑、实时对话、客服对话、情感分析、意图识别、
播客、有声书、教育辅导、数字人、数学推理、数据分析、文档理解、语音识别、
语音合成、翻译、视频生成、视频编辑、音乐生成、知识问答、语义重排、角色扮演、
电商营销、深度研究、虚拟试穿。

（词表随数据更新可能漂移；若用户场景不在表内，留空 matchedScenes，靠模态+
能力字段过滤，不要编造场景词。）

## 提取规则（与 `bl advisor recommend` 引擎一致）

| 用户信号 | 提取结果 |
| --- | --- |
| "推荐一个" | "一个"是量词，**不**意味着只返回一个结果，top 数量默认 3 |
| "便宜点"、"低成本" | budget:low |
| "按价格/成本优化" | userIntent:optimize + optimizeDimension:price |
| "按速度优化"、"越快越好" | userIntent:optimize + optimizeDimension:speed |
| "长上下文" | contextNeed:large（"超长/百万级" → extra-large） |
| "最好的"、"高精度" | qualityPreference:flagship |
| "A 和 B 哪个好" | modelPreference.mode:comparison, targets:[A, B], userIntent:differentiate |
| "比 A 更便宜的" | modelPreference.mode:alternative, targets:[A], budget:low |
| "deepseek 家族里选" | modelPreference.mode:scoped, targets:["deepseek"] |
| "不要 qwen" | modelPreference.excludes:["qwen"] |
| 无明确倾向 | budget:medium, qualityPreference:balanced, userIntent:match |

偏好推断的补充规则见 [capability-codes.md](capability-codes.md) 中的"偏好推断规则"。
