# 决策模型 API

调用 POST /compatible-mode/v1/systemone 接口使用百炼决策模型（decision-model-preview），一次前向返回分类、评分、是非判断及其概率分布与置信度，不生成文本。适用于工单分流、内容审核、智能体路由与结果校验等高频结构化决策场景。

<a id="前提条件"></a>

<a id="dm-010"></a>

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **重要**
>
> **在线体验**：在编写代码前，可先通过 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线体验决策模型。选择预设场景（客服对话判断、Agent 完成度核验、工单分流、内容审核、Agent 任务路由、医疗导诊辅助），输入业务内容并运行模型，查看判断结果、概率分布与 Token 用量，再修改条件观察结果变化。

<a id="请求说明"></a>

<a id="dm-020"></a>

## 请求说明

**协议**：TypeSafe System One（`POST /compatible-mode/v1/systemone`）

一次请求携带业务 `state` 与若干 typed 问题（`choice` / `noul` / `score`），模型一次前向返回每个问题的判定结果与概率分布，其中 `choice` 与 `score` 额外返回置信度，**不生成文本**，因此延迟与成本与输出长度无关。

**请求地址**

调用时请将 `{WorkspaceId}` 替换为业务空间 ID，详见[地域与域名](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

| 地域 | Endpoint |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/systemone` |

<table><tbody><tr><td><a id="请求参数"></a><a id="dm-100"></a><h2>请求参数</h2><p><strong>Content-Type</strong> · <code>String</code> · Header · 必选</p><p>请求类型：<code>application/json</code>。</p><p><strong>Authorization</strong> · <code>String</code> · Header · 必选</p><p>API-Key，格式：<code>Bearer $DASHSCOPE_API_KEY</code>。</p><p><strong>model</strong> · <code>String</code> · Body · 必选</p><p>模型名，取值 <code>decision-model-preview</code>。</p><p><strong>state</strong> · <code>String / Object / Array</code> · Body · 必选</p><p>待决策的业务状态：工单文本、对话或结构化对象（对象会被序列化后送模型）。</p><p><strong>questions</strong> · <code>Object</code> · Body · 必选</p><p>问题表。key 为调用方自定义的问题 id；value 为问题对象，字段如下。</p><a id="accordion-问题对象属性"></a><section><p>问题对象属性</p><div><p><strong>type</strong> · <code>String</code> · 必选</p><p>问题类型，取值：</p><ul><li><code>choice</code>：多选一</li><li><code>noul</code>：是否判断</li><li><code>score</code>：有序量表</li></ul><p><strong>instructions</strong> · <code>String</code> · 可选</p><p>问题描述或评判标准。</p><p><strong>criteria</strong> · <code>Object / Array</code> · 视类型</p><ul><li><code>choice</code>：选项名 → 选项描述 的映射（1–255 项，建议给全量选项并补 <code>other</code> 兜底）。</li><li><code>noul</code>：可选 <code>{&quot;true&quot;:…, &quot;false&quot;:…}</code> 描述。</li><li><code>score</code>：从低到高的等级描述数组（2–255 级，建议 3–7 级且每级可清晰区分）。</li></ul></div></section><strong>接口限制与建议</strong><ul><li>问题数上限 16（延迟随问题数近线性增长）。</li><li><code>choice</code> 选项 ≤ 255。</li><li><code>score</code> 等级 2–255（建议 3–7 级）。</li><li>上下文上限 65536 token，超长 <code>state</code> 会被拒绝。</li></ul></td><td><a id="请求示例"></a><a id="dm-400"></a><h2>请求示例</h2><p>DashScope SDK 已支持决策模型（兼容 TypeSafe System One 协议）：</p><ul><li><strong>Python</strong>：DashScope SDK <strong>2.0.1 及以上</strong>（决策模型为 2.0.1 新增能力，旧版本无 <code>client.decision</code> 接口，调用会报 <code>AttributeError</code>）。安装：<code>pip install -U &quot;dashscope&gt;=2.0.1&quot;</code>，参见<a href="../preparations/install-sdk.md">安装 SDK</a>。SDK 根据业务空间与地域自动拼接 <code>/compatible-mode/v1/systemone</code> 端点。</li><li><strong>Java</strong>：DashScope SDK <strong>2.23.3 及以上</strong>（决策模型为 2.23.3 新增能力，旧版本无 <code>com.alibaba.dashscope.decision</code> 包）。Maven 坐标：<code>com.alibaba:dashscope-sdk-java:2.23.3</code>（Gradle：<code>implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: '2.23.3'</code>）。API Key 默认从环境变量 <code>DASHSCOPE_API_KEY</code> 读取。</li><li>调用失败时，Python SDK 抛出 <code>DashScopeError</code> 异常，Java SDK 抛出 <code>ApiException</code>。</li></ul><p>也可以使用通用 TypeSafe SDK（<code>typesafe-sdk</code>）调用，<code>base_url</code> 指向百炼网关，SDK 会自动拼接 <code>/v1/systemone</code> 并解析返回体。安装：<code>pip install typesafe-sdk</code>。</p><a id="sec-tabs"></a><section><a id="工单分流示例"></a><section><a id="工单分流示例-h4"></a><h4>工单分流示例</h4><p>一次请求同时完成“派单团队 choice”“是否升级 noul”“严重度 score”三项决策。以下以华北2（北京）地域为例。</p><a id="sec-tabs-2"></a><section><a id="dashscope-python"></a><section><a id="dashscope-python-h4"></a><h4>DashScope Python</h4><a id="code-block"></a><pre class="language-python"><code>import os

import dashscope

# 以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。
# 决策模型端点固定挂在业务空间网关的 compatible-mode 路径下，SDK 会根据 workspace 与 region 自动拼接。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

result = client.decision.create(
    model=&quot;decision-model-preview&quot;,
    state={&quot;ticket_id&quot;: &quot;T-1001&quot;, &quot;content&quot;: &quot;订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务。&quot;},
    questions={
        &quot;department&quot;: {&quot;type&quot;: &quot;choice&quot;, &quot;instructions&quot;: &quot;应该由哪个团队处理？&quot;,
                       &quot;criteria&quot;: {&quot;billing&quot;: &quot;支付、退款和账单问题&quot;, &quot;technical&quot;: &quot;产品故障和集成问题&quot;}},
        &quot;escalate&quot;: {&quot;type&quot;: &quot;noul&quot;, &quot;instructions&quot;: &quot;是否需要立即通知值班人员？&quot;},
        &quot;severity&quot;: {&quot;type&quot;: &quot;score&quot;, &quot;instructions&quot;: &quot;这个问题有多严重？&quot;,
                     &quot;criteria&quot;: [&quot;轻微问题，不影响功能&quot;, &quot;部分功能受影响，但存在替代方案&quot;,
                                  &quot;核心功能不可用，没有替代方案&quot;, &quot;造成严重业务或安全影响&quot;]},
    },
)

print(result.answers[&quot;department&quot;].choice)   # 选中选项
print(result.answers[&quot;escalate&quot;].noul)       # P(yes)
print(result.answers[&quot;severity&quot;].score)      # 概率加权等级索引
print(result.usage.input_tokens, result.latency_ms)
</code></pre></section><a id="dashscope-java"></a><section><a id="dashscope-java-h4"></a><h4>DashScope Java</h4><a id="code-block-2"></a><pre class="language-java"><code>import com.alibaba.dashscope.decision.DecisionModel;
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
    Map&lt;String, Object&gt; state = new HashMap&lt;&gt;();
    state.put(&quot;ticket_id&quot;, &quot;T-1001&quot;);
    state.put(&quot;content&quot;, &quot;订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务，要求立即处理。&quot;);

    Map&lt;String, String&gt; options = new LinkedHashMap&lt;&gt;();
    options.put(&quot;billing&quot;, &quot;支付、退款和账单问题&quot;);
    options.put(&quot;technical&quot;, &quot;产品故障和集成问题&quot;);

    List&lt;String&gt; levels = Arrays.asList(
        &quot;轻微问题，不影响功能&quot;,
        &quot;部分功能受影响，但存在替代方案&quot;,
        &quot;核心功能不可用，没有替代方案&quot;,
        &quot;造成严重业务或安全影响&quot;);

    Map&lt;String, DecisionQuestion&gt; questions = new LinkedHashMap&lt;&gt;();
    questions.put(&quot;department&quot;, DecisionQuestion.choice(&quot;应该由哪个团队处理？&quot;, options));
    questions.put(&quot;escalate&quot;, DecisionQuestion.noul(&quot;是否需要立即通知值班人员？&quot;));
    questions.put(&quot;severity&quot;, DecisionQuestion.score(&quot;这个问题有多严重？&quot;, levels));

    DecisionModelParam param = DecisionModelParam.builder()
        .model(DecisionModelParam.Models.DECISION_MODEL_PREVIEW)
        .state(state)
        .questions(questions)
        .build();

    DecisionModel decisionModel = new DecisionModel(&quot;{WorkspaceId}&quot;, &quot;cn-beijing&quot;);
    DecisionModelResult result = decisionModel.call(param);

    System.out.println(JsonUtils.toJson(result));
  }
}
</code></pre></section><a id="typesafe-python"></a><section><a id="typesafe-python-h4"></a><h4>TypeSafe Python</h4><a id="code-block-3"></a><pre class="language-python"><code>import os
from typesafe_sdk import TypeSafeClient

client = TypeSafeClient(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode&quot;,
)

result = client.system_one(
    model=&quot;decision-model-preview&quot;,
    state={&quot;ticket_id&quot;: &quot;T-1001&quot;, &quot;content&quot;: &quot;订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务。&quot;},
    questions={
        &quot;department&quot;: {&quot;type&quot;: &quot;choice&quot;, &quot;instructions&quot;: &quot;应该由哪个团队处理？&quot;,
                       &quot;criteria&quot;: {&quot;billing&quot;: &quot;支付、退款和账单问题&quot;, &quot;technical&quot;: &quot;产品故障和集成问题&quot;}},
        &quot;escalate&quot;: {&quot;type&quot;: &quot;noul&quot;, &quot;instructions&quot;: &quot;是否需要立即通知值班人员？&quot;},
        &quot;severity&quot;: {&quot;type&quot;: &quot;score&quot;, &quot;instructions&quot;: &quot;这个问题有多严重？&quot;,
                     &quot;criteria&quot;: [&quot;轻微问题，不影响功能&quot;, &quot;部分功能受影响，但存在替代方案&quot;,
                                  &quot;核心功能不可用，没有替代方案&quot;, &quot;造成严重业务或安全影响&quot;]},
    },
)

print(result.answers[&quot;department&quot;])   # choice, confidence, probabilities
print(result.answers[&quot;escalate&quot;])     # noul P(yes)
print(result.answers[&quot;severity&quot;])     # score, legend, probabilities
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><a id="code-block-4"></a><pre class="language-bash"><code>curl -sS -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H 'Content-Type: application/json' \
  -d '{
    &quot;model&quot;: &quot;decision-model-preview&quot;,
    &quot;state&quot;: {&quot;ticket_id&quot;: &quot;T-1001&quot;, &quot;content&quot;: &quot;订单支付后超过 24 小时仍未到账，用户无法继续使用核心服务，要求立即处理。&quot;},
    &quot;questions&quot;: {
      &quot;department&quot;: {&quot;type&quot;: &quot;choice&quot;, &quot;instructions&quot;: &quot;应该由哪个团队处理？&quot;,
                     &quot;criteria&quot;: {&quot;billing&quot;: &quot;支付、退款和账单问题&quot;, &quot;technical&quot;: &quot;产品故障和集成问题&quot;}},
      &quot;escalate&quot;:   {&quot;type&quot;: &quot;noul&quot;,  &quot;instructions&quot;: &quot;是否需要立即通知值班人员？&quot;},
      &quot;severity&quot;:   {&quot;type&quot;: &quot;score&quot;, &quot;instructions&quot;: &quot;这个问题有多严重？&quot;,
                     &quot;criteria&quot;: [&quot;轻微问题，不影响功能&quot;, &quot;部分功能受影响，但存在替代方案&quot;,
                                  &quot;核心功能不可用，没有替代方案&quot;, &quot;造成严重业务或安全影响&quot;]}
    }
  }'
</code></pre></section></section></section><a id="是非判断示例"></a><section><a id="是非判断示例-h4"></a><h4>是非判断示例</h4><p>对一个 <code>noul</code> 问题返回 P(yes) 概率，0=否 1=是。以下以华北2（北京）地域为例。</p><a id="sec-tabs-3"></a><section><a id="dashscope-python-2"></a><section><a id="dashscope-python-2-h4"></a><h4>DashScope Python</h4><a id="code-block-5"></a><pre class="language-python"><code>import os

import dashscope

client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

result = client.decision.create(
    model=&quot;decision-model-preview&quot;,
    state=&quot;这段评论是否在索要退款？&quot;,
    questions={&quot;refund&quot;: {&quot;type&quot;: &quot;noul&quot;, &quot;instructions&quot;: &quot;是否在索要退款？&quot;}},
)

print(result.answers[&quot;refund&quot;].noul)   # P(yes)
</code></pre></section><a id="dashscope-java-2"></a><section><a id="dashscope-java-2-h4"></a><h4>DashScope Java</h4><a id="code-block-6"></a><pre class="language-java"><code>import com.alibaba.dashscope.decision.DecisionModel;
import com.alibaba.dashscope.decision.DecisionModelParam;
import com.alibaba.dashscope.decision.DecisionModelResult;
import com.alibaba.dashscope.decision.DecisionQuestion;
import java.util.LinkedHashMap;
import java.util.Map;

public class DecisionDemo {
  public static void main(String[] args) throws Exception {
    Map&lt;String, DecisionQuestion&gt; questions = new LinkedHashMap&lt;&gt;();
    questions.put(&quot;refund&quot;, DecisionQuestion.noul(&quot;是否在索要退款？&quot;));

    DecisionModelParam param = DecisionModelParam.builder()
        .model(DecisionModelParam.Models.DECISION_MODEL_PREVIEW)
        .state(&quot;这段评论是否在索要退款？&quot;)
        .questions(questions)
        .build();

    DecisionModel decisionModel = new DecisionModel(&quot;{WorkspaceId}&quot;, &quot;cn-beijing&quot;);
    DecisionModelResult result = decisionModel.call(param);

    System.out.println(result.getAnswers().get(&quot;refund&quot;).getNoul());   // P(yes)
  }
}
</code></pre></section><a id="typesafe-python-2"></a><section><a id="typesafe-python-2-h4"></a><h4>TypeSafe Python</h4><a id="code-block-7"></a><pre class="language-python"><code>import os
from typesafe_sdk import TypeSafeClient

client = TypeSafeClient(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode&quot;,
)

result = client.system_one(
    model=&quot;decision-model-preview&quot;,
    state=&quot;这段评论是否在索要退款？&quot;,
    questions={&quot;refund&quot;: {&quot;type&quot;: &quot;noul&quot;, &quot;instructions&quot;: &quot;是否在索要退款？&quot;}},
)

print(result.answers[&quot;refund&quot;])   # noul P(yes)
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><a id="code-block-8"></a><pre class="language-bash"><code>curl -sS -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H 'Content-Type: application/json' \
  -d '{
    &quot;model&quot;: &quot;decision-model-preview&quot;,
    &quot;state&quot;: &quot;这段评论是否在索要退款？&quot;,
    &quot;questions&quot;: {
      &quot;refund&quot;: {&quot;type&quot;: &quot;noul&quot;, &quot;instructions&quot;: &quot;是否在索要退款？&quot;}
    }
  }'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="返回参数"></a><a id="dm-300"></a><h2>返回参数</h2><p><strong>model</strong> · <code>String</code></p><p>模型名回显。</p><p><strong>request_id</strong> · <code>String</code></p><p>请求 ID，用于问题排查。</p><p><strong>answers</strong> · <code>Object</code></p><p>答案表，key 与请求中的问题 id 一一对应，value 为答案对象，字段如下。</p><a id="accordion-答案对象属性"></a><section><p>答案对象属性</p><div><p><strong>type</strong> · <code>String</code></p><p>与问题类型一致（<code>choice</code> / <code>noul</code> / <code>score</code>）。</p><p><strong>choice</strong> · <code>String</code></p><p><code>choice</code> 类型：选中的选项名。</p><p><strong>noul</strong> · <code>Float</code></p><p><code>noul</code> 类型：P(yes)，0=否 1=是。</p><p><strong>score</strong> · <code>Float</code></p><p><code>score</code> 类型：等级索引的概率加权期望，可落在两级之间（如 <code>1.43</code>）。</p><p><strong>probabilities</strong> · <code>Object</code></p><p>每个选项 / 等级的概率（和为 1）。</p><p><strong>confidence</strong> · <code>Float</code></p><p>该答案的置信度（<code>choice</code> / <code>score</code> 类型返回）。</p><p><strong>legend</strong> · <code>Object</code></p><p><code>score</code> 类型：等级索引 → 等级描述。</p></div></section><p><strong>usage</strong> · <code>Object</code></p><p>计量信息：</p><ul><li><code>input_tokens</code>（Integer）：输入 token 数。</li></ul><p><strong>latency_ms</strong> · <code>Float</code></p><p>服务端耗时（毫秒）。</p></td><td><a id="返回示例"></a><a id="dm-500"></a><h2>返回示例</h2><p>以下为工单分流示例的返回结果（节选），概率与置信度以实际返回为准。</p><a id="code-block-9"></a><pre class="language-json"><code>{
  &quot;model&quot;: &quot;decision-model-preview&quot;,
  &quot;request_id&quot;: &quot;7b986c65-b223-9341-b5f0-b988e27ecaac&quot;,
  &quot;answers&quot;: {
    &quot;department&quot;: {
      &quot;type&quot;: &quot;choice&quot;,
      &quot;choice&quot;: &quot;billing&quot;,
      &quot;confidence&quot;: 0.88,
      &quot;probabilities&quot;: {&quot;billing&quot;: 0.94, &quot;technical&quot;: 0.06}
    },
    &quot;escalate&quot;: {
      &quot;type&quot;: &quot;noul&quot;,
      &quot;noul&quot;: 0.99
    },
    &quot;severity&quot;: {
      &quot;type&quot;: &quot;score&quot;,
      &quot;score&quot;: 2.25,
      &quot;confidence&quot;: 0.91,
      &quot;legend&quot;: {
        &quot;0&quot;: &quot;轻微问题，不影响功能&quot;,
        &quot;1&quot;: &quot;部分功能受影响，但存在替代方案&quot;,
        &quot;2&quot;: &quot;核心功能不可用，没有替代方案&quot;,
        &quot;3&quot;: &quot;造成严重业务或安全影响&quot;
      },
      &quot;probabilities&quot;: {&quot;0&quot;: 0.0, &quot;1&quot;: 0.01, &quot;2&quot;: 0.73, &quot;3&quot;: 0.26}
    }
  },
  &quot;usage&quot;: {&quot;input_tokens&quot;: 125},
  &quot;latency_ms&quot;: 52.9
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="dm-600"></a>

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](../preparations/error-code.md)。
