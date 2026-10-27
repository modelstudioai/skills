# 需求提取 JSON 结构（`--intent` 路径）

> 长尾参考：常规路径用 `recommend.mjs --scene <预设>` 即可，不需要读本文件。
> 只有 pipeline（多模型协同）、需要 `scenarioHints`、或场景无法用预设表达时，
> 才手写 intent JSON 传给 `recommend.mjs --intent` / `recall-rank.mjs`。

```json
{
  "complexity": "single 或 pipeline",
  "inputModality": ["Text", "Image", "Video", "Audio"],
  "outputModality": ["Text", "Image", "Video", "Audio", "3D-Generation"],
  "requiredCapabilities": ["TG", "VU", "IG", "VG", "TTS", "ASR"],
  "requiredFeatures": ["function-calling", "web-search", "structured-outputs"],
  "matchedScenes": ["代码生成", "客服对话"],
  "scenarioHints": ["高并发", "多轮"],
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
    { "step": "...", "inputModality": ["..."], "outputModality": ["..."], "requiredCapabilities": ["..."] }
  ]
}
```

## 字段说明

字段名必须与上表完全一致。引擎会校验：`requestModality` / `response_modality` 这类无歧义别名自动归一化
（回报 `intent-key-normalized`），其余不认识的键一律忽略并回报 `unknown-intent-keys`——不会静默失效。
输出的 `intent` 字段是归一化后的版本，即引擎实际使用的约束。

| 字段 | 说明 |
| --- | --- |
| complexity | 单模型完成(single) 或 多模型协同(pipeline) |
| inputModality / outputModality | 模态取值大小写敏感，枚举见 [capability-codes.md](capability-codes.md)。填了目录里不存在的取值 → `warnings.modality-no-match` 回报真实取值 |
| requiredCapabilities | 能力代码，参与硬过滤；枚举见 [capability-codes.md](capability-codes.md)。写成全称（如 `Text-Generation`）→ `warnings.capability-no-match` 回报真实代码 |
| requiredFeatures | 特性诉求（**不参与硬过滤**，需在候选 `specs.features` 里自行核对并在理由中说明） |
| matchedScenes | 场景词，必须取自目录实际取值（词表见 SKILL.md「内联参考表」）。填错时脚本会在 `warnings.scene-no-match` 里回报真实词表与最近似词——不需要事先 grep 数据 |
| scenarioHints | 额外任务关键词，与 matchedScenes 一起参与 `notSuitableFor` 负面排除 |
| budget / contextNeed / qualityPreference | 偏好，推断规则见 SKILL.md「偏好推断」 |
| userIntent | 决定打分权重：match / optimize / evaluate / differentiate |
| optimizeDimension | **仅当**用户明确说"按 XX 优化"才填（"便宜点"是 `budget: low`，不是 `optimizeDimension: price`） |
| modelPreference.mode | comparison=对比点名模型（保持给定顺序）/ alternative=要替代品 / scoped=限定家族内选 / unconstrained=无约束 |
| modelPreference.targets | 点名对象，**子串**匹配 model id 与 family |
| modelPreference.excludes | 排除对象，**子串**匹配 model id / family / provider / familyName（所以 `qwen` 会连带排除 `qwen-domain-model`，`通义` 可匹配中文 familyName） |
| segments | pipeline 每步的模态与能力，**仅作留档与衔接校验清单，不参与排序**。相邻步骤必须模态兼容（前一步 output = 后一步 input） |

## 提取规则（与 `bl advisor recommend` 引擎一致）

| 用户信号 | 提取结果 |
| --- | --- |
| "推荐一个" | "一个"是量词，**不**意味着只返回一个结果，top 默认 3 |
| "便宜点"、"低成本" | `budget: low` |
| "按价格/成本优化" | `userIntent: optimize` + `optimizeDimension: price` |
| "按速度优化"、"越快越好" | `userIntent: optimize` + `optimizeDimension: speed` |
| "长上下文" | `contextNeed: large`（"超长/百万级" → `extra-large`） |
| "最好的"、"高精度" | `qualityPreference: flagship` |
| "A 和 B 哪个好" | `mode: comparison`, `targets: [A, B]`, `userIntent: differentiate` |
| "比 A 更便宜的" | `mode: alternative`, `targets: [A]`, `budget: low` |
| "deepseek 家族里选" | `mode: scoped`, `targets: ["deepseek"]` |
| "不要 qwen" | `excludes: ["qwen"]` |
| 无明确倾向 | `budget: medium`, `qualityPreference: balanced`, `userIntent: match` |

## pipeline 示例

"做一个数字人直播"（脚本生成 → 语音合成 → 视频生成）。先用 `segments` 把链路写清楚：

```json
{
  "complexity": "pipeline",
  "segments": [
    { "step": "直播脚本生成", "inputModality": ["Text"], "outputModality": ["Text"], "requiredCapabilities": ["TG"] },
    { "step": "脚本转语音", "inputModality": ["Text"], "outputModality": ["Audio"], "requiredCapabilities": ["TTS"] },
    { "step": "语音驱动数字人视频", "inputModality": ["Audio", "Image"], "outputModality": ["Video"], "requiredCapabilities": ["VG"] }
  ],
  "matchedScenes": ["数字人", "语音合成", "视频生成"],
  "budget": "medium",
  "qualityPreference": "balanced",
  "userIntent": "match"
}
```

**但这份 intent 直接跑选不出任何一段的模型。** `segments` 不参与排序，引擎只看顶层的
`inputModality` / `outputModality` / `requiredCapabilities`——而上例这三个字段只写在
segments 里、顶层根本没有，等于硬过滤完全不生效，只剩场景词在打分。实测返回
`video-style-transform` / `wan2.2-animate-move` / `wan2.2-s2v-detect`，文案段和配音段
一个都没选出来（脚本会回报 `pipeline-not-ranked`）。

正确做法：把每段的约束**提到顶层**，各跑一次，且合并进一条 shell 命令：

```bash
S=scripts/recommend.mjs
for seg in \
  '{"inputModality":["Text"],"outputModality":["Text"],"requiredCapabilities":["TG"],"matchedScenes":["数字人"]}' \
  '{"inputModality":["Text"],"outputModality":["Audio"],"requiredCapabilities":["TTS"],"matchedScenes":["数字人","语音合成"]}' \
  '{"inputModality":["Audio","Image"],"outputModality":["Video"],"requiredCapabilities":["VG"],"matchedScenes":["数字人","视频生成"]}'; do
  echo "$seg" | node $S --intent - --no-samples
done
```

`budget` / `qualityPreference` / `userIntent` / `modelPreference` 各段沿用同一份。
输出时按步骤组织，并检查相邻步骤模态是否兼容（不兼容要明确提示用户）；后一段需要的
图片/视频输入通常来自用户自备素材，不是前一段的产出，也要点明。

### 预设 vs 手写：预设换取简单性，代价是丢掉场景特异性

以"数字人口播视频"（文案 → 配音 → 口型视频）为例，三段里只有配音那段能直接用预设：

```bash
S=scripts/recommend.mjs
# 段1 文案：手写，把「数字人」放进 matchedScenes
echo '{"inputModality":["Text"],"outputModality":["Text"],
"requiredCapabilities":["TG"],"matchedScenes":["数字人"]}' \
  | node $S --intent - --no-samples > /tmp/seg1.json
# 段2 配音：预设够用
node $S --scene tts --no-samples > /tmp/seg2.json
# 段3 口型视频：Image+Audio→Video 的组合，手写
echo '{"inputModality":["Image","Audio"],"outputModality":["Video"],
"requiredCapabilities":["VG"],"matchedScenes":["数字人","视频生成"]}' \
  | node $S --intent - --no-samples > /tmp/seg3.json
cat /tmp/seg1.json /tmp/seg2.json /tmp/seg3.json
```

段1 图省事用 `--scene writing` 会选出通用文案模型（`qwen-max` 等），而不是带「数字人」
标签的人设模型（`qwen-plus-character` / `qwen-flash-character`）；直接 `--scene 数字人`
也不行——该场景词按多数票反推出的约束是 Text→Audio + TTS，只覆盖配音那一段。
**链路里某段带特定场景标签时，就手写并把场景词放进 `matchedScenes`。**
