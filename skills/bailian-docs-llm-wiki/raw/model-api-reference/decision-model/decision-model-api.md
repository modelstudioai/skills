# 决策模型 API

调用 POST /compatible-mode/v1/systemone 接口使用百炼决策模型（decision-model-preview），一次前向返回分类、评分、是非判断及其概率分布与置信度，不生成文本。适用于工单分流、内容审核、智能体路由与结果校验等高频结构化决策场景。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**重要****在线体验**：在编写代码前，可先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验决策模型。选择预设场景（客服对话判断、Agent 完成度核验、工单分流、内容审核、Agent 任务路由、医疗导诊辅助），输入业务内容并运行模型，查看判断结果、概率分布与 Token 用量，再修改条件观察结果变化。

## 请求说明

**协议**：TypeSafe System One（`POST /compatible-mode/v1/systemone`）

一次请求携带业务 `state` 与若干 typed 问题（`choice` / `noul` / `score`），模型一次前向返回每个问题的判定结果与概率分布，其中 `choice` 与 `score` 额外返回置信度，**不生成文本**，因此延迟与成本与输出长度无关。

**请求地址**

调用时请将 `{WorkspaceId}` 替换为业务空间 ID，详见[地域与域名](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**地域**

**Endpoint**

华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`

新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/systemone`

## 请求参数

**Content-Type** · `String` · Header · 必选

请求类型：`application/json`。

**Authorization** · `String` · Header · 必选

API-Key，格式：`Bearer $DASHSCOPE_API_KEY`。

**model** · `String` · Body · 必选

模型名，取值 `decision-model-preview`。

**state** · `String / Object / Array` · Body · 必选

待决策的业务状态：工单文本、对话或结构化对象（对象会被序列化后送模型）。

**questions** · `Object` · Body · 必选

问题表。key 为调用方自定义的问题 id；value 为问题对象，字段如下。

问题对象属性

**type** · `String` · 必选

问题类型，取值：

-   `choice`：多选一
-   `noul`：是否判断
-   `score`：有序量表

**instructions** · `String` · 可选

问题描述或评判标准。

**criteria** · `Object / Array` · 视类型

-   `choice`：选项名 → 选项描述 的映射（1–255 项，建议给全量选项并补 `other` 兜底）。
-   `noul`：可选 `{"true":…, "false":…}` 描述。
-   `score`：从低到高的等级描述数组（2–255 级，建议 3–7 级且每级可清晰区分）。

**接口限制与建议**

-   问题数上限 16（延迟随问题数近线性增长）。
-   `choice` 选项 ≤ 255。
-   `score` 等级 2–255（建议 3–7 级）。
-   上下文上限 65536 token，超长 `state` 会被拒绝。

## 请求示例

DashScope SDK 已支持决策模型（兼容 TypeSafe System One 协议）：

-   **Python**：DashScope SDK **2.0.1 及以上**（决策模型为 2.0.1 新增能力，旧版本无 `client.decision` 接口，调用会报 `AttributeError`）。安装：`pip install -U "dashscope>=2.0.1"`，参见[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)。SDK 根据业务空间与地域自动拼接 `/compatible-mode/v1/systemone` 端点。
-   **Java**：DashScope SDK **2.23.3 及以上**（决策模型为 2.23.3 新增能力，旧版本无 `com.alibaba.dashscope.decision` 包）。Maven 坐标：`com.alibaba:dashscope-sdk-java:2.23.3`（Gradle：`implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: '2.23.3'`）。API Key 默认从环境变量 `DASHSCOPE_API_KEY` 读取。
-   调用失败时，Python SDK 抛出 `DashScopeError` 异常，Java SDK 抛出 `ApiException`。

也可以使用通用 TypeSafe SDK（`typesafe-sdk`）调用，`base_url` 指向百炼网关，SDK 会自动拼接 `/v1/systemone` 并解析返回体。安装：`pip install typesafe-sdk`。

#### 工单分流示例

一次请求同时完成「派单团队 choice」「是否升级 noul」「严重度 score」三项决策。以下以华北2（北京）地域为例。

#### DashScope Python

```
import os

import dashscope

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
# 决策模型端点固定挂在业务空间网关的 compatible-mode 路径下，SDK 会根据 workspace 与 region 自动拼接。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

result = client.decision.create(
    model="decision-model-preview",
    state={"ticket_id": "T-1001", "content": "订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务。"},
    questions={
        "department": {"type": "choice", "instructions": "应该由哪个团队处理？",
                       "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"}},
        "escalate": {"type": "noul", "instructions": "是否需要立即通知值班人员？"},
        "severity": {"type": "score", "instructions": "这个问题有多严重？",
                     "criteria": ["轻微问题，不影响功能", "部分功能受影响，但存在替代方案",
                                  "核心功能不可用，没有替代方案", "造成严重业务或安全影响"]},
    },
)

print(result.answers["department"].choice)   # 选中选项
print(result.answers["escalate"].noul)       # P(yes)
print(result.answers["severity"].score)      # 概率加权等级索引
print(result.usage.input_tokens, result.latency_ms)
```

#### DashScope Java

```
import com.alibaba.dashscope.decision.DecisionModel;
import com.alibaba.dashscope.decision.DecisionModelParam;
import com.alibaba.dashscope.decision.DecisionModelResult;
import com.alibaba.dashscope.decision.DecisionQuestion;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class DecisionDemo {
  public static void main(String[] args) throws Exception {
    // API Key 默认从环境变量 DASHSCOPE_API_KEY 读取。
    // 构造参数为业务空间 ID 与地域，SDK 会拼接
    // https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone
    Map<String, Object> state = new HashMap<>();
    state.put("ticket_id", "T-1001");
    state.put("content", "订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务，要求立即处理。");

    Map<String, String> options = new LinkedHashMap<>();
    options.put("billing", "支付、退款和账单问题");
    options.put("technical", "产品故障和集成问题");

    List<String> levels = Arrays.asList(
        "轻微问题，不影响功能",
        "部分功能受影响，但存在替代方案",
        "核心功能不可用，没有替代方案",
        "造成严重业务或安全影响");

    Map<String, DecisionQuestion> questions = new LinkedHashMap<>();
    questions.put("department", DecisionQuestion.choice("应该由哪个团队处理？", options));
    questions.put("escalate", DecisionQuestion.noul("是否需要立即通知值班人员？"));
    questions.put("severity", DecisionQuestion.score("这个问题有多严重？", levels));

    DecisionModelParam param = DecisionModelParam.builder()
        .model(DecisionModelParam.Models.DECISION_MODEL_PREVIEW)
        .state(state)
        .questions(questions)
        .build();

    DecisionModel decisionModel = new DecisionModel("{WorkspaceId}", "cn-beijing");
    DecisionModelResult result = decisionModel.call(param);

    System.out.println(JsonUtils.toJson(result));
  }
}
```

#### TypeSafe Python

```
import os
from typesafe_sdk import TypeSafeClient

client = TypeSafeClient(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode",
)

result = client.system_one(
    model="decision-model-preview",
    state={"ticket_id": "T-1001", "content": "订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务。"},
    questions={
        "department": {"type": "choice", "instructions": "应该由哪个团队处理？",
                       "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"}},
        "escalate": {"type": "noul", "instructions": "是否需要立即通知值班人员？"},
        "severity": {"type": "score", "instructions": "这个问题有多严重？",
                     "criteria": ["轻微问题，不影响功能", "部分功能受影响，但存在替代方案",
                                  "核心功能不可用，没有替代方案", "造成严重业务或安全影响"]},
    },
)

print(result.answers["department"])   # choice, confidence, probabilities
print(result.answers["escalate"])     # noul P(yes)
print(result.answers["severity"])     # score, legend, probabilities
```

#### curl

```
curl -sS -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "decision-model-preview",
    "state": {"ticket_id": "T-1001", "content": "订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务，要求立即处理。"},
    "questions": {
      "department": {"type": "choice", "instructions": "应该由哪个团队处理？",
                     "criteria": {"billing": "支付、退款和账单问题", "technical": "产品故障和集成问题"}},
      "escalate":   {"type": "noul",  "instructions": "是否需要立即通知值班人员？"},
      "severity":   {"type": "score", "instructions": "这个问题有多严重？",
                     "criteria": ["轻微问题，不影响功能", "部分功能受影响，但存在替代方案",
                                  "核心功能不可用，没有替代方案", "造成严重业务或安全影响"]}
    }
  }'
```

#### 是非判断示例

对一个 `noul` 问题返回 P(yes) 概率，0=否 1=是。以下以华北2（北京）地域为例。

#### DashScope Python

```
import os

import dashscope

client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

result = client.decision.create(
    model="decision-model-preview",
    state="这段评论是否在索要退款？",
    questions={"refund": {"type": "noul", "instructions": "是否在索要退款？"}},
)

print(result.answers["refund"].noul)   # P(yes)
```

#### DashScope Java

```
import com.alibaba.dashscope.decision.DecisionModel;
import com.alibaba.dashscope.decision.DecisionModelParam;
import com.alibaba.dashscope.decision.DecisionModelResult;
import com.alibaba.dashscope.decision.DecisionQuestion;
import java.util.LinkedHashMap;
import java.util.Map;

public class DecisionDemo {
  public static void main(String[] args) throws Exception {
    Map<String, DecisionQuestion> questions = new LinkedHashMap<>();
    questions.put("refund", DecisionQuestion.noul("是否在索要退款？"));

    DecisionModelParam param = DecisionModelParam.builder()
        .model(DecisionModelParam.Models.DECISION_MODEL_PREVIEW)
        .state("这段评论是否在索要退款？")
        .questions(questions)
        .build();

    DecisionModel decisionModel = new DecisionModel("{WorkspaceId}", "cn-beijing");
    DecisionModelResult result = decisionModel.call(param);

    System.out.println(result.getAnswers().get("refund").getNoul());   // P(yes)
  }
}
```

#### TypeSafe Python

```
import os
from typesafe_sdk import TypeSafeClient

client = TypeSafeClient(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode",
)

result = client.system_one(
    model="decision-model-preview",
    state="这段评论是否在索要退款？",
    questions={"refund": {"type": "noul", "instructions": "是否在索要退款？"}},
)

print(result.answers["refund"])   # noul P(yes)
```

#### curl

```
curl -sS -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "decision-model-preview",
    "state": "这段评论是否在索要退款？",
    "questions": {
      "refund": {"type": "noul", "instructions": "是否在索要退款？"}
    }
  }'
```

## 返回参数

**model** · `String`

模型名回显。

**request\_id** · `String`

请求 ID，用于问题排查。

**answers** · `Object`

答案表，key 与请求中的问题 id 一一对应，value 为答案对象，字段如下。

答案对象属性

**type** · `String`

与问题类型一致（`choice` / `noul` / `score`）。

**choice** · `String`

`choice` 类型：选中的选项名。

**noul** · `Float`

`noul` 类型：P(yes)，0=否 1=是。

**score** · `Float`

`score` 类型：等级索引的概率加权期望，可落在两级之间（如 `1.43`）。

**probabilities** · `Object`

每个选项 / 等级的概率（和为 1）。

**confidence** · `Float`

该答案的置信度（`choice` / `score` 类型返回）。

**legend** · `Object`

`score` 类型：等级索引 → 等级描述。

**usage** · `Object`

计量信息：

-   `input_tokens`（Integer）：输入 token 数。

**latency\_ms** · `Float`

服务端耗时（毫秒）。

## 返回示例

以下为工单分流示例的返回结果（节选），概率与置信度以实际返回为准。

```
{
  "model": "decision-model-preview",
  "request_id": "7b986c65-b223-9341-b5f0-b988e27ecaac",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "billing",
      "confidence": 0.88,
      "probabilities": {"billing": 0.94, "technical": 0.06}
    },
    "escalate": {
      "type": "noul",
      "noul": 0.99
    },
    "severity": {
      "type": "score",
      "score": 2.25,
      "confidence": 0.91,
      "legend": {
        "0": "轻微问题，不影响功能",
        "1": "部分功能受影响，但存在替代方案",
        "2": "核心功能不可用，没有替代方案",
        "3": "造成严重业务或安全影响"
      },
      "probabilities": {"0": 0.0, "1": 0.01, "2": 0.73, "3": 0.26}
    }
  },
  "usage": {"input_tokens": 125},
  "latency_ms": 52.9
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
