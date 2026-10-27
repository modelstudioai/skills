---
name: bailian-model-recommend
description: >-
  阿里云百炼模型选型与推荐。当用户需要"选择、推荐、对比"模型，或描述一个 AI
  场景/功能需求（隐含需要帮其决策用哪个模型）时激活。核心意图是帮用户做决策，
  不是单纯查资料。触发词：推荐模型、选哪个、哪个适合、对比、做一个XX、实现XX
  功能、用什么模型好、XX场景方案。当用户同时涉及模型查询和模型选择时，优先
  使用本 skill（本 skill 内部会读取模型数据完成推荐）。
compatibility: 需要已安装 bailian-docs-llm-wiki skill（提供 models/ 数据目录）
---

# 百炼模型推荐

从阿里云百炼平台模型库中，根据用户场景推荐最合适的模型并提供调用示例代码。

## 执行流程：一次命令 + 一次撰写

**常规路径只需要两步、两次工具调用**：

```bash
# 第一步：一条命令拿全量结果（候选 + 规格 + 负面清单 + 示例代码 + 端点提示）
node scripts/recommend.mjs --scene code --exclude qwen --top 3
```

第二步：基于该输出撰写推荐理由并回答用户（见「撰写推荐理由」）。

**不要**：先 grep 模型数据、再逐个读 references、再分两次跑 recall-rank +
get-samples。场景词校验、数据自检、示例提取都已内置在 recommend.mjs 里，
所有参考表也已内联在本文档下方——happy path 不需要打开 references/。

数据缺失时脚本以退出码 1 报错并给出安装命令，照做即可（无需事先手动检查）：
`npx skills add modelstudioai/skills --skill bailian-docs-llm-wiki -y`。
**禁止在没有数据的情况下凭记忆推荐模型。**

## 适用场景

**显式选型：** "推荐一个模型"、"选哪个模型"、"帮我对比 XX 和 XX"
**隐式选型：** "我想做一个 XX"、"帮我实现 XX 功能"（描述目标，隐含需要选模型）
**不适用：** 用户已确定模型只问怎么调用 → 直接 `get-samples.mjs`；纯查参数/价格 → `bailian-docs-llm-wiki` skill。
**边界：** 同时涉及查询与选择时优先用本 skill；仅当用户已确定模型、只需查参数/价格/调用方式时交给 `bailian-docs-llm-wiki`。

## recommend.mjs 参数

| flag | 说明 |
| --- | --- |
| `--scene <预设\|场景词>[,...]` | 场景，可重复或逗号分隔。预设见下表；也可直接传目录场景词（约束由数据反推） |
| `--exclude <needle>[,...]` | 排除。**子串**匹配 model id / family / provider / familyName |
| `--only <needle>[,...]` | 限定在某家族/厂商内选（scoped） |
| `--compare <a,b>` | 对比点名模型（保持用户给定顺序，每个点名模型优先以其精确版本出现） |
| `--alternative-to <model>[,...]` | 要指定模型的替代品 |
| `--budget low\|medium\|high` | 默认 medium。"便宜点/低成本" → low（**不是** `--optimize price`） |
| `--quality flagship\|balanced\|cost-optimized` | 默认 balanced。"最好的/高精度" → flagship |
| `--context standard\|large\|extra-large` | 默认 standard。"长上下文" → large，"超长/百万级" → extra-large |
| `--optimize price\|context\|quality\|speed` | 仅当用户明确说"按 XX 优化"时才用（会改写打分权重） |
| `--top <n>` | 候选数，默认 3。"推荐一个"里的"一个"是量词，**不**等于 `--top 1` |
| `--no-samples` | 不内嵌示例代码（省 token） |
| `--intent <file\|->` | 跳过预设，直接用给定 intent JSON（pipeline / 精细控制时用） |
| `--list-scenes` | 打印预设、目录场景词后退出 |
| `--data <dir>` | 覆盖模型数据目录 |

### 场景预设

| `--scene` | 场景词 | 输入 → 输出 | 能力 |
| --- | --- | --- | --- |
| `code` | 代码生成 | Text → Text | TG |
| `agent` | Agent编排、意图识别 | Text → Text | TG |
| `chat` | 客服对话、知识问答 | Text → Text | TG |
| `research` | 深度研究、数学推理 | Text → Text | Reasoning、TG |
| `writing` | 创意写作、角色扮演 | Text → Text | TG |
| `translate` | 翻译 | Text → Text | TR、TG |
| `doc` | 文档理解、OCR文字识别 | Image/Text → Text | VU |
| `analytics` | 数据分析 | Text/Image → Text | TG、VU |
| `education` | 教育辅导 | Text/Image → Text | TG、VU |
| `sentiment` | 情感分析 | Text/Audio → Text | TG |
| `rag` | 向量检索、语义重排 | Text → Text | ME、TR |
| `image` | 图像生成 | Text/Image → Image | IG |
| `image-edit` | 图像编辑、图像修复 | Image/Text → Image | IG |
| `portrait` | 人脸人像、虚拟试穿 | Image/Text → Image | IG |
| `marketing` | 电商营销 | Text/Image → Text/Image/Video | TG、IG |
| `video` | 视频生成 | Text/Image → Video | VG、World-Model |
| `video-edit` | 视频编辑 | Video/Image → Video | VG |
| `3d` | 3D生成 | Text/Image → 3D-Generation/Video | 3D-generation、World-Model |
| `tts` | 语音合成、有声书、播客 | Text → Audio | TTS |
| `asr` | 语音识别 | Audio → Text | ASR、Realtime-ASR |
| `music` | 音乐生成 | Text/Audio → Audio | TTS |
| `realtime` | 实时对话、数字人 | Audio/Text → Audio/Text | Realtime-Omni 等实时能力 |
| `omni` | 实时对话、Agent编排 | 全模态 → Text/Audio | Multimodal-Omni、Realtime-Omni |

## 内联参考表

**模态取值**（大小写敏感）：输入 `Audio` / `Image` / `Text` / `Video`；输出 `3D-Generation` / `Audio` / `Image` / `Text` / `Video`。

**能力代码**：`TG` 文本生成、`Reasoning` 推理、`VU` 视觉理解、`IG` 图像生成、`VG` 视频生成、`TTS` 语音合成、`ASR` 语音识别、`TR` 翻译、`ME` 多模态嵌入、`3D-generation` 3D 生成、`World-Model` 世界模型、`Multimodal-Omni` 全模态、`Realtime-Omni` 实时全模态、`Realtime-Chatting` 实时对话、`Realtime-ASR` 实时语音识别、`Realtime-Text-to-Speech` 实时语音合成、`Realtime-Audio-Translate` 实时音频翻译。

**目录场景词**（33 个，`profile.scenes` 全集；会随数据更新漂移，脚本会在 `warnings` 里回报当时的真实词表）：
3D生成、Agent编排、OCR文字识别、人脸人像、代码生成、创意写作、向量检索、图像修复、图像生成、图像编辑、实时对话、客服对话、情感分析、意图识别、播客、教育辅导、数字人、数学推理、数据分析、文档理解、有声书、深度研究、电商营销、知识问答、翻译、虚拟试穿、视频生成、视频编辑、角色扮演、语义重排、语音合成、语音识别、音乐生成。

**偏好推断**（只在用户明确表达或场景强烈暗示时偏离默认值）：

| 用户信号 | 结果 |
| --- | --- |
| "便宜"、"低成本"、"省钱"、高并发（如"日均百万请求"）、个人学习试玩 | `--budget low`（试玩再加 `--quality cost-optimized`） |
| "最好的"、"高精度"、"不计成本"、企业级 + 准确率优先 | `--quality flagship`（企业级再加 `--budget high`） |
| "长上下文" / "超长、百万级" | `--context large` / `--context extra-large` |
| "按价格/速度/上下文/质量优化" | `--optimize <dimension>` |
| "A 和 B 哪个好" | `--compare A,B` |
| "比 A 更便宜的" | `--alternative-to A --budget low` |
| "在 deepseek 家族里选" | `--only deepseek` |
| "不要千问/qwen 系列" | `--exclude qwen`（子串匹配，会连带排除 `qwen-domain-model` 与 id 含 qwen 的模型；`--exclude 通义` 匹配中文 familyName） |
| 无明确倾向 | 全部走默认（medium / balanced / standard / match） |

**需求模糊时**（如"推荐一个模型"无任何场景信息）：直接追问"你想用在什么场景"，拿到回答后再跑命令。不要在信息不足时猜场景。

**`requiredFeatures` 只做提示，不参与硬过滤**：引擎的硬门只有模态 + 能力。用户要求 function-calling / web-search / structured-outputs / prefix-completion 时，需要在候选的 `specs.features` 里自行核对并在理由中说明。

## 什么时候走 `--intent`（自由 intent JSON）

- pipeline：多模型协同，需要 `segments` 描述每一步的模态与能力
- 需要 `scenarioHints`（额外任务关键词，参与 notSuitableFor 负面排除）
- 场景既不在预设表也不在场景词表里，需要手工组合模态/能力

字段结构与提取规则见 [references/requirement-schema.md](references/requirement-schema.md)。用法：

```bash
node scripts/recommend.mjs --intent intent.json      # 或 --intent -  从 stdin 读
```

### pipeline：每段各跑一次，合并进一条命令

**`segments` 不参与排序**——引擎只读顶层的 `inputModality` / `outputModality` /
`requiredCapabilities` / `matchedScenes`。所以一次调用只能为**一段**选出模型，N 段链路
要跑 N 次，且必须合并进**一条** shell 命令（= 一次工具调用），不要一段一次工具调用。

每段的顶层约束就是该段的模态与能力，`matchedScenes` 填该段真正相关的场景词，
`budget` / `qualityPreference` / `userIntent` 各段一致；能用 `--scene` 表达的段就别手写。
都先带 `--no-samples`，选定模型后再单独取示例，避免 N 段示例灌满上下文。
完整示例与「预设 vs 手写」的取舍见 [references/requirement-schema.md](references/requirement-schema.md)。

拿齐结果后做**衔接校验**（脚本不做，这是 LLM 的活）：

- 前一段的输出模态必须被后一段接受——对照候选的 `pipelineRole[].from/to` 与 `capabilities`
- 后一段需要的图片/视频输入通常是**用户自备素材**，不来自前一段，必须点明
- `callModes` 含 `async` 的段要给"创建任务 + 轮询"示例，别给同步返回
- 不兼容或缺素材时明确提示，不要假装链路能跑通

## 脚本输出

```json
{
  "scene": "code",
  "intent": { "matchedScenes": ["代码生成"], "modelPreference": { "mode": "unconstrained", "excludes": ["qwen"] } },
  "gate": "structured | forced-comparison | forced-alternative",
  "poolSize": 20,
  "warnings": [],
  "endpointNote": "示例 base_url 含 [workspace-id] 占位符…",
  "candidates": [
    {
      "rank": 1,
      "slot": "primary | runner-up | exploration",
      "model": "glm-5.3",
      "name": "GLM-5.3",
      "provider": "zhipu-ai",
      "family": "glm-4.5",
      "familyName": "GLM",
      "tier": "flagship",
      "finalScore": 0.979,
      "matchedScenes": ["代码生成"],
      "oneLinePositioning": "1M上下文+128K输出的旗舰模型，专用于生产级编程任务",
      "capabilities": ["TG", "Reasoning"],
      "callModes": ["streaming", "sync"],
      "notSuitableFor": ["低延迟实时对话"],
      "pipelineRole": [{ "from": "Text", "to": "Text", "role": "长程任务规划与结构化执行" }],
      "docUrl": "https://…",
      "specs": {
        "pricing": ["输入 8 / 每百万tokens", "输出 28 / 每百万tokens"],
        "contextWindow": 1000000,
        "maxInputTokens": 1048576,
        "maxOutputTokens": 131072,
        "features": ["cache", "function-calling", "structured-outputs"]
      },
      "samples": { "source": "openai", "python": "…", "curl": "…", "docUrl": "https://…" }
    }
  ]
}
```

`intent` 是脚本实际使用的意图（预设解析后的结果）——回答里如需说明假设，以它为准。
`slot`：primary（最佳）/ runner-up（次优，说明与 primary 的 tradeoff）/ exploration（不同视角备选）。
`gate`：structured（常规链路）/ forced-*（点名模型路径，保持用户顺序）。

**warnings 必须处理，不能忽略**：

| code | 含义 | 处理 |
| --- | --- | --- |
| `scene-no-match` | 场景词在目录里无人认领，场景维度全按 0 分算，排序不可信 | 用 warning 里的 `availableScenes` / `suggestions` 换词重跑 |
| `capability-no-match` | 能力代码目录里不存在（如写成 `Text-Generation` 而非 `TG`），能力硬门失效并回退全池 | 用 `availableCapabilities` 里的代码重跑 |
| `modality-no-match` | 模态取值目录里不存在（大小写敏感，如 `text`），该侧模态约束不生效 | 用 `availableInputModality` / `availableOutputModality` 重跑 |
| `target-not-found` | 点名模型不存在（或已被 excludes 排除） | 如实告知用户，不要假装有该模型 |
| `empty-candidates` | 候选为空 | 先检查模态/能力是否填错（大小写敏感），修正重跑；仍为空才告知无匹配 |
| `pipeline-not-ranked` | 多段 pipeline 的约束只写在 `segments` 里、顶层为空，硬过滤完全没生效 | **最危险的一种**：输出看着正常但不属于任何一段。把每段约束提到顶层，各跑一次 |
| `intent-key-normalized` | intent 里写了 `requestModality` 之类的别名，已自动改成 `inputModality`/`outputModality` | 无需重跑；输出的 `intent` 已是归一化后的版本 |
| `unknown-intent-keys` | intent 含引擎不认识的字段，**已被忽略**（过滤/打分没生效） | 按 warning 里的 `knownKeys` 改名重跑；不重跑则排序不可信 |

前三个词表类 warning 是"填错就静默失效"的兜底——脚本会回报当时的真实词表，**不需要事先 grep 数据**。
后三个（`pipeline-not-ranked` / `intent-key-normalized` / `unknown-intent-keys`）只在手写 intent JSON
（`--intent` / `recall-rank.mjs`）时出现，`recommend.mjs --scene` 自己构造字段不会踩到。

## 撰写推荐理由

这是 LLM 在本 skill 中唯一的生成性工作。**候选列表不得增删、不得重排。**

- 理由必须关联用户的具体需求，禁止"性能强大"这类空话
- 素材全部来自脚本输出：`oneLinePositioning`、`matchedScenes`、`tier`、`specs.pricing`、`specs.contextWindow` / `maxOutputTokens`、`specs.features`、`notSuitableFor`、`callModes`——**不要回读 `models.jsonl`**
- 三条理由角度不同；有定价时结合预算做成本权衡
- tradeoff 用 `notSuitableFor` 与规格差异写，不要编造短板
- pipeline 场景：相邻步骤的模型模态必须兼容（前一步 output = 后一步 input），不兼容要明确提示

## 示例代码规则

- 直接用 `candidates[].samples`（`source` = openai / dashscope / fallback），优先给 Python，附 curl
- **base_url 必须原样取自 samples，禁止编造或改写域名**
- 输出里出现 `endpointNote` 时，必须把该提示写进回答（示例端点含 `[workspace-id]` 占位符，需替换为真实 Workspace ID，并与 API Key、地域严格匹配）
- 示例含 `enable_thinking` / `reasoning_content` 流式循环时，给用户去掉思考逻辑的最简版本
- 用户已确定模型、只要代码时：`node scripts/get-samples.mjs <model-id> [<model-id>...]`

细则见 [references/samples-format.md](references/samples-format.md)。

## 输出格式

用自然语言直接输出推荐（如"根据你的需求，我推荐以下模型…"），每个模型包含：

1. **模型名称和 ID**
2. **推荐理由** — 关联用户具体需求，附 tradeoff 对比
3. **亮点** — 关键优势标签（来自 `specs.features`）
4. **规格信息** — 上下文窗口、最大输出、定价（来自 `specs`）
5. **调用示例代码** — 来自 `samples`（优先 Python，附 curl）

**输出约束：**

- 不暴露内部流程术语（禁止出现 "Stage"、"意图画像"、"硬过滤"、"召回" 等词汇）
- 候选列表与脚本输出保持一致
- 所有推荐基于 `bailian-docs-llm-wiki` 的实际数据，不凭记忆推荐

## 内部实现（改脚本时才需要看）

```
scripts/recommend.mjs    一键入口：场景预设 → intent → 引擎 → 内嵌 samples
scripts/recall-rank.mjs  低层入口：自带 intent JSON 时用（--with-samples 可内嵌示例）
scripts/get-samples.mjs  低层入口：只取指定模型的示例代码
scripts/lib/engine.mjs   确定性引擎（纯函数，移植自 bl advisor recommend）
scripts/lib/catalog.mjs  数据层：目录加载/快照去重/场景词表/示例提取/端点提示
```

引擎的确定性环节（无 LLM 参与）：

| 环节 | 逻辑 |
| --- | --- |
| intent 归一化 | 字段名别名归一（`requestModality`→`inputModality` 等）并回报；未识别键忽略并回报 `unknown-intent-keys` |
| pipeline | `complexity` / `segments` **只被接受、不参与排序**——引擎只读顶层模态/能力/场景。多段链路必须每段各调一次 |
| 快照去重 | 去掉日期快照版本（`-YYYY-MM-DD` / `-MMDD` 后缀），保留主版本 |
| excludes | 子串匹配 model id / family / provider / familyName |
| 词表校验 | excludes 之后、硬过滤之前，用当时的池子校验场景词/能力码/模态取值是否存在；不存在则回报真实词表（`scene-no-match` / `capability-no-match` / `modality-no-match`）。目的是消灭"填错就静默失效"——能力码写错会让硬门回退全池，排序悄悄退化成贵的优先 |
| scoped | `--only` 按 targets 收窄池子；收窄为空则回退全池并回报 warning |
| 硬过滤 | 输入/输出模态 + 能力交集门；不足 5 个时先去模态保能力，仅当无模型匹配能力才回全池（能力约束永不静默丢弃） |
| 负面排除 | 模型 `profile.notSuitableFor` 与场景/任务关键词相交则剔除 |
| 公式打分 | scene 0.4 / tier 0.2 / price 0.2 / context 0.2（按 userIntent 换权重集；optimize 时按维度切换主导权重） |
| 排序 | 档位 flagship→balanced→lightweight（要便宜则反转）；同档阿里系 provider 优先（qwen/qwen-domain-model/wan）；同档价格降序（贵的≈更强，要便宜时升序）；无价格排最后；同价取新版本号 |
| comparison | 点名集保持用户顺序；同一 target 命中多版本时按 target 轮转、组内精确命中优先，保证每个点名模型都出现 |
| fairness | 同家族最多 2 席；单一家族占满时把异家族最优换进末位 |
| 席位 | 默认每 provider 一个 flagship；要便宜时 lightweight→balanced→flagship 三档各一席 |

改预设表前请先核对目录真实取值（`--list-scenes` 或 wiki 数据），不要凭记忆新增场景词或能力码。
数据来源与字段说明见 [references/data-source.md](references/data-source.md)。
