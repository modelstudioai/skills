# 接入决策模型

通过 AI 工具的扩展机制接入 decision-model-preview 决策模型：以评论自动审核为例，一次请求并行判定多条内容，返回 choice、probabilities、confidence，按置信度自动放行、隐藏或转人工。

## 背景：为什么用决策模型

评论审核、工单分类、请求路由这类判断，常见做法是让对话模型输出 JSON：判定规则写在 prompt 里，容易被诱导性内容带偏；输出外层常包代码围栏，解析不稳；每次都先生成一段分析文字，token 开销不小。

decision-model-preview 是决策模型，专做这类判断。通过 `/compatible-mode/v1/systemone` 接口发送 `state`（待判定内容）和 `questions`（类型化问题），直接返回结构化答案：`choice`（结论）、`probabilities`（分布）、`confidence`（把握），不生成自然语言文本。问题支持三种类型：Choice（从选项中选）、Score（按等级打分）、Noul（返回 0 到 1 的概率），一次调用可以混合多个问题并行评估。

与让对话模型"顺手判一下"相比：

-   判定标准写在 `criteria` 字段里结构化传入，不依赖长 prompt 的措辞
-   返回就是 JSON，无围栏、无多余文字，Agent 与代码直接消费
-   答案是短结构而非长文本，输出 token 开销小，适合高频调用

**说明**接入决策模型目前仅支持

[Token Plan 个人版](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)。

## 示例：在 Claude Code 中接入评论审核

以 Claude Code 为例，通过 Slash Command 接入决策模型。其他工具的接入方式类似，区别在于扩展机制和配置文件路径不同。

### 步骤一：创建 Slash Command

将套餐 API Key（以 `sk-sp-` 为前缀）配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`，供后续 curl 鉴权使用。

在项目根目录创建 `.claude/commands/review-comments.md`，写入以下内容：

```
调用 Token Plan 决策模型，批量审核评论并按置信度分流。

用户输入：$ARGUMENTS（评论文件路径，或直接粘贴的多条评论）

## 步骤

1. 读取评论内容。$ARGUMENTS 是文件路径时读取该文件，是文本时直接使用。每行一条评论，忽略空行，从 1 开始编号。

2. 调用决策模型接口（使用 Bash 工具执行 curl），一次请求判定全部评论。questions 中每条评论对应一个 c<编号> 问题，结构与 c1 相同，instructions 里的 id 相应替换：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "comments": [
        {"id": 1, "text": "<评论1>"},
        {"id": 2, "text": "<评论2>"}
      ]
    },
    "model": "decision-model-preview",
    "questions": {
      "c1": {
        "type": "choice",
        "instructions": "`comments` 中 id 为 1 的评论属于哪一类？",
        "criteria": {
          "pass": "正常讨论，包括批评、质疑和报错反馈",
          "spam": "广告导流、诈骗引流、批量营销话术、买卖账号或课程资源"
        }
      }
    }
  }'
```

3. 从返回 JSON 的 answers 中逐条读取 c1、c2……的 choice、confidence、probabilities 字段。

4. 按以下规则为每条评论确定动作，输出一张表格（编号、评论摘要、判定、confidence、动作）：
   - confidence >= 0.9 且 choice 为 spam：自动隐藏
   - confidence >= 0.9 且 choice 为 pass：自动放行
   - confidence < 0.9：转人工

5. 表格后输出一行统计：自动处理 X 条，转人工 Y 条。转人工的条目附一句说明，引用该条 probabilities 中 spam 的概率。
```

### 步骤二：审核评论

准备一份评论文件 `comments.txt`，每行一条评论：

查看测试数据 · 10 条评论（含 3 个边界样本）

```
这篇文章把异步和并发的区别讲得很清楚，收藏了。
加微信 teacher888 领取内部资料，免费带你做副业月入过万。
请问示例里为什么用线程池而不是协程？
前排出售各类平台账号，需要的私聊。
写得太差了，看了半天没看懂。
点击链接领取新款手机 t.cn/abc123。
感谢分享，已按文中方法跑通。
有人知道这个库的中文文档在哪吗？我博客里有整理，需要的自取 t.cn/abc。
第二节的示例代码在我机器上报 ImportError。
风口项目日入五百，稳赚不赔，带新人入场。
```

在 Claude Code 中输入 `/review-comments comments.txt`，输出示例：

查看输出示例 · 10 条评论的判定与分流

```
| #  | 评论摘要                             | 判定  | confidence | 动作     |
|----|--------------------------------------|-------|------------|----------|
| 1  | 这篇文章把异步并发的区别讲得很清楚…   | pass  | 1.00       | 自动放行 |
| 2  | 加微信 teacher888 领取内部资料…       | spam  | 1.00       | 自动隐藏 |
| 3  | 请问示例里为什么用线程池而不是协程？   | pass  | 1.00       | 自动放行 |
| 4  | 前排出售各类平台账号，需要的私聊。     | spam  | 1.00       | 自动隐藏 |
| 5  | 写得太差了，看了半天没看懂。          | pass  | 1.00       | 自动放行 |
| 6  | 点击链接领取新款手机 t.cn/abc123。    | spam  | 1.00       | 自动隐藏 |
| 7  | 感谢分享，已按文中方法跑通。          | pass  | 1.00       | 自动放行 |
| 8  | 有人知道这个库的中文文档在哪吗？我博… | spam  | 0.69       | 转人工   |
| 9  | 第二节的示例代码在我机器上报错…       | pass  | 1.00       | 自动放行 |
| 10 | 风口项目日入五百，稳赚不赔…           | spam  | 1.00       | 自动隐藏 |

自动处理 9 条，转人工 1 条。
#8 转人工：spam 概率 0.84，pass 概率 0.16，判定把握不足。
```

输出里有两处值得留意：

-   **#5 和 #9 是负评和报错，判 pass。** 判定看内容性质，不看语气。批评、质疑、报错反馈属于正常讨论，这条规则写进了 `criteria`。
-   **#8 是带链接的技术分享，confidence 只有 0.69，进人工队列。** 内容介于分享与引流之间，概率分布也不极端（spam 0.84 / pass 0.16），模型明确表示倾向但把握不足——这正是 `criteria` 边界描述要处理的那类样本。分流阈值写在 Command 的第 4 步里，调高更保守，调低更自动。

## 读懂返回的三个字段

答案按 `questions` 里的 key 原样返回，每条 Choice 答案包含：

字段

含义

怎么用

`choice`

选中的选项

分支依据：放行还是隐藏

`probabilities`

每个选项的概率，总和为 1

展示、排序、加权

`confidence`

判定把握，0 到 1

阈值分流：高自动执行，低转人工

`questions` 的 key 自定义，不参与推理。需要"程度"类判断时改用 Noul（返回 0 到 1 的概率）或 Score（按等级打分），一次调用可以混合。

## 其他工具

不同工具的扩展机制和配置文件路径如下表所示，该表为支持扩展机制的主流 AI 编程工具示例。将上述 Claude Code 示例中的配置内容保存到对应路径即可。

工具

扩展机制

配置文件路径

Claude Code

Slash Command

`.claude/commands/review-comments.md`

Codex

Skill

`~/.codex/skills/token-plan-review/SKILL.md`

Qwen Code

Skill

`~/.qwen/skills/review-comments/SKILL.md`

OpenCode

Agent

`.opencode/agents/review-comments.md`

OpenClaw

Skill

`~/.openclaw/workspace/skills/token-plan-review/SKILL.md`

Hermes Agent

Skill

`~/.hermes/skills/moderation/review-comments/SKILL.md`

Qoder

Skill

`~/.qoder/skills/review-comments/SKILL.md`

**说明**Skill 类工具（Codex、Qwen Code、OpenClaw、Hermes Agent、Qoder）需要在配置文件开头添加 YAML front matter，完整配置文件如下：

```
---
name: "token-plan-review"
description: "调用 Token Plan 决策模型，批量审核评论并按置信度分流。当用户要求审核评论、过滤垃圾评论时激活。"
---

调用 Token Plan 决策模型，批量审核评论并按置信度分流。

用户输入：评论文件路径，或直接粘贴的多条评论。

## 步骤

1. 读取评论内容。用户输入是文件路径时读取该文件，是文本时直接使用。每行一条评论，忽略空行，从 1 开始编号。

2. 调用决策模型接口（使用 Bash 工具执行 curl），一次请求判定全部评论。questions 中每条评论对应一个 c<编号> 问题，结构与 c1 相同，instructions 里的 id 相应替换：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "comments": [
        {"id": 1, "text": "<评论1>"},
        {"id": 2, "text": "<评论2>"}
      ]
    },
    "model": "decision-model-preview",
    "questions": {
      "c1": {
        "type": "choice",
        "instructions": "`comments` 中 id 为 1 的评论属于哪一类？",
        "criteria": {
          "pass": "正常讨论，包括批评、质疑和报错反馈",
          "spam": "广告导流、诈骗引流、批量营销话术、买卖账号或课程资源"
        }
      }
    }
  }'
```

3. 从返回 JSON 的 answers 中逐条读取 c1、c2……的 choice、confidence、probabilities 字段。

4. 按以下规则为每条评论确定动作，输出一张表格（编号、评论摘要、判定、confidence、动作）：
   - confidence >= 0.9 且 choice 为 spam：自动隐藏
   - confidence >= 0.9 且 choice 为 pass：自动放行
   - confidence < 0.9：转人工

5. 表格后输出一行统计：自动处理 X 条，转人工 Y 条。转人工的条目附一句说明，引用该条 probabilities 中 spam 的概率。
```

OpenCode Agent 的 front matter 不同，完整配置文件如下：

```
---
description: "调用 Token Plan 决策模型，批量审核评论并按置信度分流。"
mode: subagent
tools:
  bash: true
  write: false
  edit: false
---

调用 Token Plan 决策模型，批量审核评论并按置信度分流。

用户输入：评论文件路径，或直接粘贴的多条评论。

## 步骤

1. 读取评论内容。用户输入是文件路径时读取该文件，是文本时直接使用。每行一条评论，忽略空行，从 1 开始编号。

2. 调用决策模型接口（使用 Bash 工具执行 curl），一次请求判定全部评论。questions 中每条评论对应一个 c<编号> 问题，结构与 c1 相同，instructions 里的 id 相应替换：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "comments": [
        {"id": 1, "text": "<评论1>"},
        {"id": 2, "text": "<评论2>"}
      ]
    },
    "model": "decision-model-preview",
    "questions": {
      "c1": {
        "type": "choice",
        "instructions": "`comments` 中 id 为 1 的评论属于哪一类？",
        "criteria": {
          "pass": "正常讨论，包括批评、质疑和报错反馈",
          "spam": "广告导流、诈骗引流、批量营销话术、买卖账号或课程资源"
        }
      }
    }
  }'
```

3. 从返回 JSON 的 answers 中逐条读取 c1、c2……的 choice、confidence、probabilities 字段。

4. 按以下规则为每条评论确定动作，输出一张表格（编号、评论摘要、判定、confidence、动作）：
   - confidence >= 0.9 且 choice 为 spam：自动隐藏
   - confidence >= 0.9 且 choice 为 pass：自动放行
   - confidence < 0.9：转人工

5. 表格后输出一行统计：自动处理 X 条，转人工 Y 条。转人工的条目附一句说明，引用该条 probabilities 中 spam 的概率。
```

## 注意事项

-   判定边界写在 `criteria` 里。"什么算 spam"的边界案例（如带链接的技术分享）写成明确的选项描述，比反复调整问题措辞更有效。
-   复杂判断拆小：一次只问一个明确问题，多维度分开判定，在 Command 的分流规则里组合结果。
-   `confidence` 低是模型明确表示拿不准，分流到人工比重试有效；阈值 0.9 是示例值，按误判成本调整。
-   请求失败按状态码处理：`401` 检查 API Key，`422` 是请求体校验失败（响应正文会指出出错字段），`429` 和 `529` 退避后重试。
-   模型输出的是判定和把握，不是事实担保。涉及账号封禁、资金处置等高风险动作时，保持人工复核环节。
