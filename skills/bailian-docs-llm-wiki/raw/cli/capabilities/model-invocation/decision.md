# 决策模型

阿里云百炼 CLI 调用决策模型，进行类型化判定并获取概率结果的命令速查。

`bl decision` 调用决策模型，对业务状态做类型化判定，返回 `choice`、`noul` 或 `score` 结果及概率。适合工单分类、意图判断、风险分级等需要稳定结构化结果的场景。

**说明**决策模型使用 Workspace 专用 Endpoint，需要 `--workspace-id`，也可通过 `BAILIAN_WORKSPACE_ID` 或配置中的 `workspace_id` 提供。支持 `cn-beijing`（默认）和 `ap-southeast-1` 地域；API Key 需要与目标地域匹配。

**重要**任意命令追加 `--help` 可查看完整参数说明，例如 `bl decision --help`。本文命令明细以 bl 2.5.1 为基准核实。

## 快速开始

```
bl decision --workspace-id ws_xxx \
  --state "用户要求退款，是否属于退款诉求？" \
  --questions '{"refund":{"type":"noul","instructions":"是否在要求退款？"}}' \
  --output json
```

返回结果：

```
{
  "model": "decision-model-preview",
  "request_id": "12345678-abcd-1234-abcd-123456789012",
  "answers": {
    "refund": {
      "type": "noul",
      "noul": 1
    }
  },
  "usage": {
    "input_tokens": 23
  },
  "latency_ms": 40
}
```

## 命令

### bl decision

运行决策模型。需要 API Key 鉴权。

**语法**

```
bl decision (--state <text> | --state-file <path>) (--questions <json> | --questions-file <path>) | --request-file <path>
```

参数

类型

必填

说明

`--model <model>`

string

否

决策模型 ID（默认：decision-model-preview）

`--state <text>`

string

否

要判定的业务状态，按字符串发送

`--state-file <path>`

string

否

从文件读取状态；`.json` 按对象或数组解析，其他文件按文本读取；`-` 表示标准输入

`--questions <json>`

string

否

问题表 JSON，以问题 ID 为键

`--questions-file <path>`

string

否

从 JSON 文件读取问题表，支持 `{...}` 或 `{"questions":{...}}`

`--request-file <path>`

string

否

完整请求 JSON `{state, questions}`；会自动移除 `label` 和 `target`

`--workspace-id <id>`

string

否

Endpoint 使用的 Workspace ID（也可设置 BAILIAN\_WORKSPACE\_ID）

`--region <cn-beijing|ap-southeast-1>`

string

否

Endpoint 地域：`cn-beijing`（默认）或 `ap-southeast-1`

`--api-key <key>`

string

否

API Key

`--base-url <url>`

string

否

API Base URL

**示例**：判断工单是否在要求退款

```
bl decision --workspace-id ws_xxx --state "用户要求退款，是否属于退款诉求？" --questions '{"refund":{"type":"noul","instructions":"是否在要求退款？"}}'
```

-   已配置 Base URL 时优先使用 Base URL，`--region` 只在没有可用 Base URL 时参与拼接 Endpoint。
-   `--state` 始终按字符串发送；需要传对象或数组时使用 `--state-file` 或 `--request-file`。
-   `--request-file` 会移除 `label` 和 `target`，可直接复用训练样本，不需要先手工删字段。
-   单次请求建议不超过 16 个问题；问题越多，延迟越高。

## 问题类型

### choice

从多个选项中选择一个，适合意图分类、工单类型判断。

```
{
  "intent": {
    "type": "choice",
    "instructions": "选择用户意图",
    "criteria": {
      "refund": "退款",
      "cancel": "取消订阅",
      "other": "其他"
    }
  }
}
```

返回 `choice`、`confidence` 和 `probabilities`。

### noul

判断是否成立，返回 0–1 的判定值。`criteria` 可省略，也可分别描述成立与不成立的含义。

```
{
  "refund": {
    "type": "noul",
    "instructions": "是否在要求退款？",
    "criteria": {
      "true": "已明确要求退款",
      "false": "未要求退款"
    }
  }
}
```

返回 `noul` 分值；文本输出显示为 `P(yes)`。

### score

按有序等级评分，`criteria` 必须是按从低到高排列的数组。

```
{
  "urgency": {
    "type": "score",
    "instructions": "评估紧急程度",
    "criteria": ["很低", "一般", "很高"]
  }
}
```

返回 `score`、`legend`、`probabilities` 和 `confidence`。等级数量建议 3–7 个。

## 输出

默认返回完整 JSON。使用 `--output text` 时，每个问题输出一行摘要：

```
refund   noul P(yes)=0.98
emotion  choice=angry  confidence=0.26  calm=0.03 angry=0.51 other=0.46
input_tokens=49  latency_ms=49
request_id: 12345678-abcd-1234-abcd-123456789012
```

-   `usage.input_tokens` 为本次请求的输入 Token 数。
-   `latency_ms` 为端到端耗时，单位为毫秒。
-   决策 API 不支持 `temperature`、`max_tokens` 等采样参数。
