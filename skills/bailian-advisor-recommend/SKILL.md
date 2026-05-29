---
name: bailian-advisor-recommend
description: >-
  阿里云百炼模型推荐。用户描述 AI 场景或功能需求时激活，无需明确说"推荐模型"。
  触发词：做一个XX、实现XX功能、用什么模型、图片生成、语音合成、视频生成、
  图像理解、RAG、Agent、翻译、摘要等。依赖 bailian-docs-llm-wiki skill。
compatibility: 需要已安装 bailian-docs-llm-wiki skill（提供 models/ 数据目录）
metadata:
  author: gujieye
  version: "1.0"
---

# 百炼模型推荐

从阿里云百炼平台模型库中，根据用户场景推荐最合适的模型并提供调用示例代码。

## 前置检查

执行推荐前确认依赖的 `bailian-docs-llm-wiki` skill 已安装且数据可用。

**检测逻辑：**

1. 检查 `bailian-docs-llm-wiki` skill 是否已安装（通过查找已安装 skill 目录中是否存在 `bailian-docs-llm-wiki/models/models.jsonl`）
2. 如果未安装，执行安装：`npx skills add modelstudioai/skills --skill bailian-docs-llm-wiki -y`

安装失败则告知用户并中止。**禁止在没有数据的情况下凭记忆推荐模型。**

## 适用场景

**显式选型：**
- "推荐一个模型"、"选哪个模型"、"用什么模型好"
- "帮我对比一下XX和XX模型"

**隐式选型（用户描述想做的事，隐含需要选模型）：**
- "我想做一个XX"（客服机器人、翻译工具、代码助手...）
- "帮我实现XX功能"（图片生成、语音合成、文本摘要...）
- "怎么用 AI 来做XX"、"大模型能做XX吗"
- "XX场景有什么方案"、"我想接入XX能力"

**技术选型：**
- "XX和XX哪个更适合做YY"
- "低成本/高并发/高精度 场景怎么选"

**不适用：**
- 用户已确定模型，只问怎么调用 → 直接给调用代码
- 纯粹查询模型参数/价格 → 使用 bailian-docs-llm-wiki skill

## 推荐流程

### 第一步：理解需求（Agent 直接完成，不输出给用户）

从用户描述中快速提取结构化需求信息。JSON 结构定义见 [references/requirement-schema.md](references/requirement-schema.md)，推断规则见 [references/capability-codes.md](references/capability-codes.md)。

**要快：** 简单字段映射，不做复杂推理。如果需求不清晰，直接追问具体场景，不输出中间分析。

### 第二步：筛选候选

从 `models/models.jsonl` 中筛选匹配的模型（10~50 个）：

1. 去除历史快照版本（如 `model-2025-04-28`），只保留主版本
2. 按模态过滤（输入/输出模态必须兼容）
3. 按能力、特性、上下文窗口、质量定位评分排序
4. 同一家族最多保留少量模型，避免同质化
5. 候选不足时放宽过滤条件

数据源字段说明见 [references/data-source.md](references/data-source.md)。

### 第三步：精选推荐

从候选列表中选出 3 个推荐：

| 位置 | 策略 |
| --- | --- |
| 推荐 #1（最佳推荐） | 最符合用户预算和质量偏好的最佳模型 |
| 推荐 #2（次优选择） | 另一个档次的模型，说明与 #1 的 tradeoff |
| 推荐 #3（备选参考） | 不同视角的选择，说明场景差异 |

**排序逻辑：**

- 用户要省钱 → #1 必须是性价比最高的，不是旗舰
- 用户要最好 → #1 必须是能力最强的旗舰
- 用户无倾向 → #1 选综合匹配度最高的
- 推荐最适合场景的，不是最强的；偏好从用户表达中推断，不预设倾向

**约束：**

- 理由必须关联用户具体需求（禁止"性能强大"等空话），三条理由角度不同
- 有定价信息时结合预算权衡，帮用户做成本决策
- 避免推荐同家族多个模型，优先稳定版本
- 提供多档次选择和 tradeoff 说明，由用户自己决定

**pipeline 场景：** 相邻步骤的模型模态必须兼容，不兼容时添加提示。

### 第四步：输出推荐结果

对每个推荐模型，读取对应的 group JSON 文件（`models/groups/<slug>.json`）获取 `samples` 字段中的调用示例代码。示例代码获取方式和输出格式见 [references/samples-format.md](references/samples-format.md)。

用自然语言直接输出推荐（如"根据你的需求，我推荐以下模型..."），每个模型包含：

1. **模型名称和 ID**
2. **推荐理由** — 关联用户具体需求，附 tradeoff 对比
3. **亮点** — 关键优势标签
4. **规格信息** — 上下文窗口、最大输出、定价（如有）
5. **调用示例代码** — 从 group 文件的 samples 字段获取（优先 openai.python，同时提供 curl）

**输出约束：**

- 不暴露内部流程术语（禁止出现"Stage"、"意图画像"、"候选召回"、"精排"等词汇）
- 所有推荐基于 `bailian-docs-llm-wiki` 的实际数据，不凭记忆推荐
