# RunCompletion

支持调用通义晓蜜CCAI-对话分析AIO应用获取对话摘要、关键信息抽取、质检结果、对话分析结果，应用调用支持 HTTP 调用来完成客户的响应，目前提供普通 HTTP 和 HTTP SSE 两种协议，您可根据自己的需求自行选择。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

当前API暂无授权信息透出。

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/ccai/app/{appId}/completion HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 子业务空间标识 | llm-ik\*\*\*\*\*\*RVYCKzt |
| appId | string | 是 | 应用 ID | 097d65c9c7004f8dad2b454850ac232b |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>body</td><td><p>object</p></td><td><p>否</p></td><td><div><p>request body 结构信息</p></div></td><td></td></tr><tr><td>Dialogue</td><td><p>object</p></td><td><p>是</p></td><td><div><p>对话结构信息</p></div></td><td></td></tr><tr><td>Sentences</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>对话内容列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>每一轮对话内容的结构信息</p></div></td><td></td></tr><tr><td>ChatId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>每一轮对话内容的唯一性 ID</p></div></td><td><p>ae2483e01a8446aa859925947fcf4d8e</p></td></tr><tr><td>Role</td><td><p>string</p></td><td><p>是</p></td><td><div><p>（通话角色） user-客户 agent-客服 system-系统消息</p></div></td><td><p>user</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><p>是</p></td><td><div><p>对话内容信息</p></div></td><td><p>查询北京天气</p></td></tr><tr><td>SessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>对话唯一性 ID</p></div></td><td><p>d25zc9c7004f8dad2b454d</p></td></tr><tr><td>Fields</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>信息抽取时，需要抽取的字段列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>字段结构信息</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><p>否</p></td><td><div><p>字段编码</p></div></td><td><p>phoneNumber</p></td></tr><tr><td>Desc</td><td><p>string</p></td><td><p>否</p></td><td><div><p>字段描述</p></div></td><td><p>用户来电咨询的原因分类，主要有投诉、咨询、政策建议等。</p></td></tr><tr><td>EnumValues</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>枚举值列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>枚举值结构信息</p></div></td><td></td></tr><tr><td>Desc</td><td><p>string</p></td><td><p>否</p></td><td><div><p>枚举值描述</p></div></td><td><p>客户有新的需求/新的场景，客服跟进沟通需求细节</p></td></tr><tr><td>EnumValue</td><td><p>string</p></td><td><p>是</p></td><td><div><p>枚举值</p></div></td><td><p>新业务拓展</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>是</p></td><td><div><p>字段名称</p></div></td><td><p>来电原因类型</p></td></tr><tr><td>ModelCode</td><td><p>string</p></td><td><p>否</p></td><td><div><p>模型规格</p></div><div><p><strong>枚举值：</strong></p><ul><li>tyxmPlus :<div><p>tyxmPlus</p></div></li><li>tyxmTurbo :<div><p>tyxmTurbo</p></div></li></ul></div></td><td><p>tyxmTurbo</p></td></tr><tr><td>ServiceInspection</td><td><p>object</p></td><td><p>否</p></td><td><div><p>服务质检结构信息</p></div></td><td></td></tr><tr><td>InspectionContents</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>服务质检维度结构列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>服务质检维度结构</p></div></td><td></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>服务质检维度描述</p></div></td><td><p>客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>是</p></td><td><div><p>服务质检维度名称</p></div></td><td><p>客服是否过度承诺</p></td></tr><tr><td>InspectionIntroduction</td><td><p>string</p></td><td><p>否</p></td><td><div><p>服务质检场景详细介绍及描述</p></div></td><td><p>请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等</p></td></tr><tr><td>SceneIntroduction</td><td><p>string</p></td><td><p>否</p></td><td><div><p>服务质检场景</p></div></td><td><p>保险销售场景</p></td></tr><tr><td>Stream</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>true 则会开启 SSE 响应，默认 false</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>true</p></div></li><li>false :<div><p>false</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>TemplateIds</td><td><p>array</p></td><td><p>是</p></td><td><div><p>CCAI 应用下的模版 ID 列表</p></div></td><td></td></tr><tr><td></td><td><p>integer</p></td><td><p>否</p></td><td><div><p>CCAI 应用下的模版 ID</p></div></td><td><p>10375</p></td></tr><tr><td>variables</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>变量列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>变量列表</p></div></td><td></td></tr><tr><td>variableCode</td><td><p>string</p></td><td><p>否</p></td><td><div><p>变量 code</p></div></td><td><p>name</p></td></tr><tr><td>variableValue</td><td><p>string</p></td><td><p>否</p></td><td><div><p>变量值</p></div></td><td><p>张三</p></td></tr><tr><td>responseFormatType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>输出结果格式化类型，jsonObject-json 结构，text-原始字符串</p></div></td><td><p>jsonObject</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Response 结构信息 |  |
| FinishReason | string | 如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。 | stop |
| RequestId | string | 系统生成的标志本次请求的唯一性 ID | 17204B98-xxxx-4F9A-8464-2446A84821CA |
| Text | string | 应用返回的结果。 | 这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。 |
| inputTokens | string | 输入 Token 数量 | 4672 |
| outputTokens | string | 输出 Token 数量 | 621 |
| totalTokens | string | Tokens 总量 | 5609 |
| usage | object | 使用量 |  |
| rag | object | rag 使用详情 |  |
| dialogSummary | object | 会话摘要 |  |
| inputTokens | integer | 输入 Token 数量 | 4672 |
| outputTokens | integer | 输出 Token 数量 | 621 |
| invokeCount | integer | 调用次数 | 3 |
| adaptive | object | rag 智能调用 |  |
| inputTokens | integer | 输入 Token 数量 | 4672 |
| outputTokens | integer | 输出 Token 数量 | 621 |
| invokeCount | integer | 调用次数 | 3 |
| ragStatus | string | rag 执行状态 | SUCCESS |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "FinishReason": "stop",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA\n",
  "Text": "这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。\n",
  "inputTokens": "4672",
  "outputTokens": "621",
  "totalTokens": "5609",
  "usage": {
    "rag": {
      "dialogSummary": {
        "inputTokens": 4672,
        "outputTokens": 621,
        "invokeCount": 3
      },
      "adaptive": {
        "inputTokens": 4672,
        "outputTokens": 621,
        "invokeCount": 3
      }
    }
  },
  "ragStatus": "SUCCESS"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | CCAI.InvalidParam.NotExist | The specified parameter %s is not valid. | 请求API的参数不存在 |
| 400 | CCAI.Throttling.Qpm | Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475). | 触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 400 | CCAI.Throttling.Qps | Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475). | 触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 400 | CCAI.ParamInvalid.IllegalParamValue | The parameter value of the request API is illegal %s. | 请求API的参数不合法 |
| 500 | CCAI.InternalError | The request processing has failed due to some unknown error, exception or failure. | 系统内部错误，请稍后重试 |
| 403 | CCAI.IllegalPermission.NoAuth | User not authorized to operate on the specified resource. | 该用户未被授权可操作指定资源 |
| 403 | CCAI.ParamNotfound.MissParam | Parameter verification failed, The specified parameter %s is missing. | 参数校验失败，指定参数缺失。 |
| 403 | CCAI.TenantPermission.NoAuth | The current account does not have the permission to specify the business space. Please authorize the business space permission. | 当前账号没有指定业务空间的权限，请进行业务空间权限授权。 |

访问[错误中心](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/RunCompletion#workbench-doc-change-demo)。
