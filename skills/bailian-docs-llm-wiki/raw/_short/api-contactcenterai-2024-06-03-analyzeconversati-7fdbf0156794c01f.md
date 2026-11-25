# AnalyzeConversation

获取对话摘要、标题生成、关键词、字段信息抽取、问题及解决方案、服务质检、代办事项、满意度、情绪检测、QA抽取、用户画像、标签分类等对话分析结果，应用调用支持 HTTP 调用来完成客户的响应。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：获取[APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.41df281fWNMfrx)。

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
POST /{workspaceId}/ccai/app/{appId}/analyze_conversation HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 工作空间 ID | llm-368\*\*\*\*\*\*3ifum |
| appId | string | 是 | 应用 id。 | a070a49c681f4a95a0f0\*\*\*\*\*\*\*\*\*35c |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>body</td><td><p>object</p></td><td><p>否</p></td><td><div><p>请求体。</p></div></td><td></td></tr><tr><td>categoryTags</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>标签分类列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>tagDesc</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签描述</p></div></td><td><p>客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为</p></td></tr><tr><td>tagName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签名称</p></div></td><td><p>客服过度承诺</p></td></tr><tr><td>dialogue</td><td><p>object</p></td><td><p>否</p></td><td><div><p>对话内容列表</p></div></td><td></td></tr><tr><td>sentences</td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>对话内容</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>是</p></td><td></td><td></td></tr><tr><td>role</td><td><p>string</p></td><td><p>是</p></td><td><div><p>通话角色：</p><ul><li><p>user-客户</p></li><li><p>agent-客服</p></li><li><p>system-系统消息</p></li></ul></div></td><td><p>user</p></td></tr><tr><td>text</td><td><p>string</p></td><td><p>是</p></td><td><div><p>对话文本</p></div></td><td><p>请问怎么申请新卡</p></td></tr><tr><td>sessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>客服会话 sessionId</p></div></td><td><p>session-01</p></td></tr><tr><td>examples</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>指令示例列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>指令示例</p></div></td><td></td></tr><tr><td>output</td><td><p>string</p></td><td><p>是</p></td><td><div><p>输出示例</p></div></td><td><p>问题描述：询问2.2更新时间，处理方案：已告知</p></td></tr><tr><td>sentences</td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>对话内容示例列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>是</p></td><td><div><p>对话内容示例</p></div></td><td></td></tr><tr><td>chatId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>每一轮对话 id</p></div></td><td><p>chat-01</p></td></tr><tr><td>role</td><td><p>string</p></td><td><p>是</p></td><td><div><p>通话角色：</p><ul><li><p>user-客户</p></li><li><p>agent-客服</p></li><li><p>system-系统消息</p></li></ul></div></td><td><p>user</p></td></tr><tr><td>text</td><td><p>string</p></td><td><p>是</p></td><td><div><p>对话文本</p></div></td><td><p>什么时候更新</p></td></tr><tr><td>fields</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>信息抽取时，需要抽取的字段列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>字段结构信息</p></div></td><td></td></tr><tr><td>code</td><td><p>string</p></td><td><p>否</p></td><td><div><p>字段编码</p></div></td><td><p>phoneNumber</p></td></tr><tr><td>desc</td><td><p>string</p></td><td><p>是</p></td><td><div><p>字段描述</p></div></td><td><p>用户来电咨询的原因分类，主要有投诉、咨询、政策建议等。</p></td></tr><tr><td>enumValues</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>枚举值列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>是</p></td><td></td><td></td></tr><tr><td>desc</td><td><p>string</p></td><td><p>是</p></td><td><div><p>枚举描述</p></div></td><td><p>客户有新的需求/新的场景，客服跟进沟通需求细节</p></td></tr><tr><td>enumValue</td><td><p>string</p></td><td><p>是</p></td><td><div><p>枚举值</p></div></td><td><p>新业务拓展</p></td></tr><tr><td>name</td><td><p>string</p></td><td><p>是</p></td><td><div><p>字段名称</p></div></td><td><p>来电原因类型</p></td></tr><tr><td>modelCode</td><td><p>string</p></td><td><p>否</p></td><td><div><p>模型 code</p></div></td><td><p>tyxmTurbo</p></td></tr><tr><td>resultTypes</td><td><p>array</p></td><td><p>是</p></td><td><div><p>指令任务类型</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>是</p></td><td><div><p>summary-对话摘要，title-标题生成、fields-字段信息抽取、keywords -关键字抽取，service_inspection-服务质检、question_solution-问题和解决方案、actions-代办事项、satisfaction-满意度、emotion_detection-情绪检测、questions_and_answer-QA 抽取、user_profile-用户画像、category_tag-标签分类、custom_prompt-自定义指令</p></div></td><td><p>summary</p></td></tr><tr><td>sceneName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>场景名称</p></div></td><td><p>阿里云工单质检场景</p></td></tr><tr><td>serviceInspection</td><td><p>object</p></td><td><p>否</p></td><td><div><p>服务质检结构信息</p></div></td><td></td></tr><tr><td>inspectionContents</td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>服务质检维度结构列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>是</p></td><td><div><p>服务质检维度结构</p></div></td><td></td></tr><tr><td>content</td><td><p>string</p></td><td><p>是</p></td><td><div><p>服务质检维度描述</p></div></td><td><p>客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。</p></td></tr><tr><td>title</td><td><p>string</p></td><td><p>是</p></td><td><div><p>服务质检维度名称</p></div></td><td><p>客服是否过度承诺</p></td></tr><tr><td>inspectionIntroduction</td><td><p>string</p></td><td><p>是</p></td><td><div><p>服务质检场景详细介绍及描述</p></div></td><td><p>请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等</p></td></tr><tr><td>sceneIntroduction</td><td><p>string</p></td><td><p>是</p></td><td><div><p>服务质检场景</p></div></td><td><p>保险销售场景</p></td></tr><tr><td>stream</td><td><p>boolean</p></td><td><p>是</p></td><td><div><p>必填。是否流式：true，流式返回答案；false，全量返回答案。</p></div></td><td><p>false</p></td></tr><tr><td>userProfiles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>用户画像列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>名称</p></div></td><td><p>sex</p></td></tr><tr><td>value</td><td><p>string</p></td><td><p>否</p></td><td><div><p>描述</p></div></td><td><p>表示客户的性别，从列表[“男”, “女”]中选择一个值</p></td></tr><tr><td>timeConstraintList</td><td><p>array</p></td><td><p>否</p></td><td><div><p>时间约束，用于告诉大模型在做分析时，需要关注或限定在哪些时间范围内</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>时间信息</p></div></td><td><p>2026年1月</p></td></tr><tr><td>sourceCallerUid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>不用填</p></div></td><td><p>null</p></td></tr><tr><td>customPrompt</td><td><p>string</p></td><td><p>否</p></td><td><div><p>自定义指令，指令中必须包含${dialogue}</p></div></td><td><p>对通话内容进行总结${dialogue}</p></td></tr><tr><td>responseFormatType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>输出结果格式化类型，jsonObject-json 结构，text-原始字符串</p></div></td><td><p>jsonObject</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| errorCode | string | 错误码 | success |
| errorInfo | string | 错误信息 | success |
| finishReason | string | 如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。 | stop |
| requestId | string | 系统生成的标志本次请求的唯一性 ID | 968A8634-FA2C-5381-9B3E-C552DED7E8BF |
| success | boolean | 请求是否成功 | True |
| text | string | 应用返回的结果。 | 这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。 |
| inputTokens | string | 输入 Token 数量 | 238 |
| outputTokens | string | 输出 Token 数量 | 458 |
| totalTokens | string | Tokens 总量 | 696 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "errorCode": "success",
  "errorInfo": "success",
  "finishReason": "stop",
  "requestId": "968A8634-FA2C-5381-9B3E-C552DED7E8BF",
  "success": true,
  "text": "这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。",
  "inputTokens": "238",
  "outputTokens": "458",
  "totalTokens": "696"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | CCAI.Throttling.Qps | Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475). | 触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 400 | CCAI.Throttling.Qpm | Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475). | 触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。 |
| 400 | CCAI.InvalidParam.NotExist | The specified parameter %s is not valid. | 请求API的参数不存在 |
| 400 | CCAI.ParamInvalid.IllegalParamValue | The parameter value of the request API is illegal %s. | 请求API的参数不合法 |
| 500 | CCAI.InternalError | The request processing has failed due to some unknown error, exception or failure. | 系统内部错误，请稍后重试 |
| 403 | CCAI.TenantPermission.NoAuth | The current account does not have the permission to specify the business space. Please authorize the business space permission. | 当前账号没有指定业务空间的权限，请进行业务空间权限授权。 |
| 403 | CCAI.ParamNotfound.MissParam | Parameter verification failed, The specified parameter %s is missing. | 参数校验失败，指定参数缺失。 |
| 403 | CCAI.IllegalPermission.NoAuth | User not authorized to operate on the specified resource %s . | 该用户未被授权可操作指定资源 |

访问[错误中心](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/AnalyzeConversation#workbench-doc-change-demo)。
