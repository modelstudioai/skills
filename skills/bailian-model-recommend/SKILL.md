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

## 设计原则：确定性的流程交给脚本，LLM 只做两件事

本 skill 的召回、打分、排序、席位分配全部由确定性脚本完成（移植自 bailian-cli
推荐引擎，`bailian-cli >= 2.6.0` 的 `bl advisor recommend` 同源逻辑）。**LLM 不
参与排序和筛选决策**，只负责：

1. **意图提取** — 把用户的自然语言需求转成一份 intent JSON（第二步）
2. **推荐理由撰写** — 为脚本选出的模型写关联用户需求的理由（第四步）

禁止 LLM 凭判断增删或重排脚本输出的候选列表。

## 适用场景

**显式选型：**
- "推荐一个模型"、"选哪个模型"、"用什么模型好"
- "帮我对比一下XX和XX模型"

**隐式选型（用户描述想做的事，隐含需要选模型）：**
- "我想做一个XX"（客服机器人、翻译工具、代码助手...）
- "帮我实现XX功能"（图片生成、语音合成、文本摘要...）

**不适用：**
- 用户已确定模型，只问怎么调用 → 直接给调用代码
- 纯粹查询模型参数/价格 → 使用 bailian-docs-llm-wiki skill

**与 bailian-docs-llm-wiki 的边界：** 当用户同时涉及模型查询和模型选择时，优先使用本 skill。仅当用户已确定模型、只需查参数/价格/调用方式时，由 bailian-docs-llm-wiki 处理。

## 前置检查

1. 检查 `bailian-docs-llm-wiki` skill 是否已安装（查找 `~/.bailian/skills/bailian-docs-llm-wiki/models/models.jsonl`；优先用环境变量 `BAILIAN_CONFIG_DIR` 定位配置根）
2. 如果未安装，执行安装：`npx skills add modelstudioai/skills --skill bailian-docs-llm-wiki -y`

安装失败则告知用户并中止。**禁止在没有数据的情况下凭记忆推荐模型。**

## 推荐流程

### 第一步：理解需求 → 意图 JSON（LLM 完成）

从用户描述中提取结构化意图，一次完成，不输出中间分析。JSON 结构定义见
[references/requirement-schema.md](references/requirement-schema.md)，能力代码与
偏好推断规则见 [references/capability-codes.md](references/capability-codes.md)。

**意图提取的关键规则**（与引擎一致，违反会导致排序失真）：

- "推荐一个"中的"一个"是量词，**不是**只返回一个结果
- "便宜点"、"低成本" → `budget: "low"`，而不是 `optimizeDimension: "price"`；
  `optimizeDimension` 仅在用户明确说"按价格/速度/上下文/质量优化"时设置
- `matchedScenes` 必须从模型数据实际存在的场景词中选（先 grep 一次
  `models.jsonl` 里 `profile.scenes` 的取值集合再填），不要编造场景词
- 用户点名了模型 → 填 `modelPreference`（comparison=对比两个指定模型 /
  alternative=要指定模型的替代品 / scoped=在该家族内选 / unconstrained=无约束）
- 排除某家族 → `modelPreference.excludes`

**需求模糊时（如"推荐一个模型"无任何场景信息）：** 直接向用户追问"你想用在
什么场景"，拿到回答后把用户原话和回答一起重新提取意图。不要在信息不足时
猜测场景。

### 第二步：脚本召回+排序（确定性，无 LLM）

把 intent JSON 写入临时文件（或 stdin 传入），运行：

```bash
node scripts/recall-rank.mjs intent.json            # 默认 top 3
node scripts/recall-rank.mjs intent.json --top 5    # 指定数量
```

脚本内置（与 `bl advisor recommend` 引擎同源）：

| 环节 | 确定性逻辑 |
| --- | --- |
| 快照去重 | 去掉日期快照版本（`-YYYY-MM-DD` / `-MMDD` 后缀），保留主版本 |
| 硬过滤 | 输入/输出模态 + 能力交集门；不足 5 个时先去模态保能力，仅当无模型匹配能力才回全池（能力约束永不静默丢弃） |
| 负面排除 | 模型 `profile.notSuitableFor` 与用户场景/任务关键词相交则剔除 |
| 公式打分 | scene 0.4 / tier 0.2 / price 0.2 / context 0.2（按 userIntent 换权重集；optimize 时 price 0.6 主导） |
| 排序 | 档位 flagship→balanced→lightweight（用户要便宜则反转）；同档阿里系 provider 优先（qwen/qwen-domain-model/wan）；同档价格降序（贵的≈更强，要便宜时升序）；无价格排最后；同价取新版本号 |
| fairness | 同家族最多 2 席；单一家族占满时把异家族最优换进末位 |
| 席位 | 默认每 provider 一个 flagship；用户要便宜时 lightweight→balanced→flagship 三档各一席；标注 primary / runner-up / exploration |

输出 JSON（结构见下方"脚本输出"）。

### 第三步：读取脚本结果

脚本输出即最终候选列表——**不得增删、不得重排**。检查两件事：

1. **点名模型缺失**：用户点名的模型（comparison/alternative targets）没出现 →
   说明目录里无此模型，如实告知用户
2. **zero 候选**：`candidates` 为空 → 检查 intent 的模态/能力字段是否填错，
   修正后重跑脚本；仍为空才告知用户无匹配

### 第四步：取调用示例 + 撰写推荐理由（LLM 完成）

**调用示例**（确定性提取，用脚本）：

```bash
node scripts/get-samples.mjs qwen-max deepseek-v3
```

优先 `samples.openai`，其次 `samples.dashscope`，都没有时构造最简 OpenAI 兼容
示例。示例代码规则见 [references/samples-format.md](references/samples-format.md)。

**推荐理由**（LLM 撰写，这是 LLM 在本 skill 中唯一的生成性工作）：

- 理由必须关联用户具体需求（禁止"性能强大"等空话）
- 结合脚本输出的 `matchedScenes`、`tier`、`specs.pricing`、`specs.contextWindow` 撰写
- 三条理由角度不同；有定价时结合预算权衡，帮用户做成本决策
- pipeline 场景：相邻步骤模型模态必须兼容，不兼容时明确提示

### 第五步：输出推荐结果

用自然语言直接输出推荐（如"根据你的需求，我推荐以下模型..."），每个模型包含：

1. **模型名称和 ID**
2. **推荐理由** — 关联用户具体需求，附 tradeoff 对比
3. **亮点** — 关键优势标签（来自 `specs.features`）
4. **规格信息** — 上下文窗口、最大输出、定价（来自 `specs`）
5. **调用示例代码** — 来自 get-samples.mjs 输出（优先 Python，附 curl）

**输出约束：**

- 不暴露内部流程术语（禁止出现"Stage"、"意图画像"、"硬过滤"、"召回"等词汇）
- 候选列表与脚本输出保持一致，LLM 不得增删重排
- 所有推荐基于 `bailian-docs-llm-wiki` 的实际数据，不凭记忆推荐

## 脚本输出

`recall-rank.mjs` 输出 JSON：

```json
{
  "gate": "structured | forced-comparison | forced-alternative",
  "poolSize": 21,
  "candidates": [
    {
      "rank": 1,
      "slot": "primary | runner-up | exploration",
      "model": "qwen3.8-max",
      "name": "Qwen3.8 Max",
      "provider": "qwen",
      "family": "qwen3.8-max",
      "tier": "flagship",
      "finalScore": 0.996,
      "matchedScenes": ["代码"],
      "specs": {
        "pricing": ["输入 12 / 每百万tokens"],
        "contextWindow": 262144,
        "maxInputTokens": 262144,
        "maxOutputTokens": 32768,
        "features": ["function-calling", "structured-outputs"]
      }
    }
  ]
}
```

字段含义：`slot` = primary（最佳推荐）/ runner-up（次优、说明与 primary 的
tradeoff）/ exploration（不同视角备选）。`gate` = structured（常规硬过滤链）/
forced-*（用户点名模型路径，点名集保持用户顺序）。
