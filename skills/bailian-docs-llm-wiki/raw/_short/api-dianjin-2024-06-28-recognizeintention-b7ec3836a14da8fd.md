# RecognizeIntention - 意图识别

意图识别，支持意图识别（全局+分层）、态度识别、企业识别。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/RecognizeIntention)

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:RecognizeIntention</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/recog/intent HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>业务空间 id</p></div></td><td>llm-xxxx</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求体。</p></div></td><td></td></tr><tr><td>analysis</td><td>boolean</td><td>否</td><td><div><p>是否分析</p></div></td><td>false</td></tr><tr><td>bizType</td><td>string</td><td>是</td><td><div><p>业务类型。</p></div><div><div>枚举值：</div><ul><li>common：意图识别。</li><li>business：企业识别。</li><li>attitude：态度识别。</li></ul></div></td><td>common</td></tr><tr><td>conversation</td><td>string</td><td>是</td><td><div><p>对话内容。</p></div></td><td>##客服##：您好，请问是朱杰先生吗？这里是诚信财务的周莉。我们发现您有一项款项昨天是账单日，但您还没还款，这很可能是一个小小的疏忽。来电是提醒您尽快完成还款，避免影响您的信用记录。\n ##客户##：今天天气怎么样呢？</td></tr><tr><td>globalIntentionList</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>全局意图列表，当操作类型 opType 为分层 hierarchical 时，必填。</p></div></td><td></td></tr><tr><td>globalIntentionList</td><td>object</td><td>否</td><td><div><p>全局意图</p></div></td><td></td></tr><tr><td>description</td><td>string</td><td>否</td><td><div><p>意图描述</p></div></td><td>正常付款3</td></tr><tr><td>intention</td><td>string</td><td>否</td><td><div><p>意图名称</p></div></td><td>正常付款3</td></tr><tr><td>intentionCode</td><td>string</td><td>否</td><td><div><p>意图 code</p></div></td><td>1810566978021232640</td></tr><tr><td>intentionScript</td><td>string</td><td>否</td><td><div><p>意图话术</p></div></td><td>好的，那先不打扰您了，祝您生活愉快！再见！</td></tr><tr><td>hierarchicalIntentionList</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>分层意图列表，当操作类型 opType 为分层 hierarchical 时，必填。</p></div></td><td></td></tr><tr><td>hierarchicalIntentionList</td><td>object</td><td>否</td><td><div><p>分层意图</p></div></td><td></td></tr><tr><td>description</td><td>string</td><td>否</td><td><div><p>意图描述</p></div></td><td>询问股票价格</td></tr><tr><td>intention</td><td>string</td><td>否</td><td><div><p>意图名称</p></div></td><td>询问股票价格</td></tr><tr><td>intentionCode</td><td>string</td><td>否</td><td><div><p>意图 code</p></div></td><td>1810929291010150400</td></tr><tr><td>intentionScript</td><td>string</td><td>否</td><td><div><p>意图话术</p></div></td><td>好的，那先不打扰您了，祝您生活愉快！再见！</td></tr><tr><td>intentionList</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>意图列表，当业务类型<strong>不为</strong>态度识别时，必填。</p></div></td><td></td></tr><tr><td>intentionList</td><td>object</td><td>否</td><td><div><p>意图</p></div></td><td></td></tr><tr><td>description</td><td>string</td><td>否</td><td><div><p>意图描述</p></div></td><td>客户表示忘记还款</td></tr><tr><td>intention</td><td>string</td><td>否</td><td><div><p>意图名称</p></div></td><td>客户表示忘记还款</td></tr><tr><td>intentionCode</td><td>string</td><td>否</td><td><div><p>意图 code</p></div></td><td>1808766224000262144</td></tr><tr><td>intentionScript</td><td>string</td><td>否</td><td><div><p>意图话术</p></div></td><td>好的，那先不打扰您了，祝您生活愉快！再见！</td></tr><tr><td>opType</td><td>string</td><td>否</td><td><div><p>操作类型。</p></div><div><div>枚举值：</div><ul><li>common：通用。</li><li>hierarchical：分层。</li></ul></div></td><td>common</td></tr><tr><td>recommend</td><td>boolean</td><td>否</td><td><div><p>推荐意图</p></div></td><td>false</td></tr><tr><td>intentionDomainCode</td><td>string</td><td>否</td><td><div><p>意图库: 本地意图库 code</p></div></td><td>collection</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | ResultCode |  |
| cost | long | 耗时 | null |
| data | object | 响应数据 |  |
| analysisProcess | string | 分析过程 | 客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。 |
| intentionCode | string | 意图 code | \-1 |
| intentionName | string | 意图名称 | 其它 |
| recommendIntention | string | 推荐意图 | 客户试图回避谈论逾期还款的话题 |
| recommendScript | string | 推荐话术 | 朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。 |
| intentionScript | string | 意图话术 | 朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。 |
| dataType | string | 数据类型 | null |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| requestId | string | 请求 id | 003D019A-1BB3-53EC-A0D2-CE76DA5D73B1 |
| success | boolean | 是否成功 | true |
| time | string | 时间戳 | 2024-04-24 11:54:34 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": {
    "analysisProcess": "客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。",
    "intentionCode": -1,
    "intentionName": "其它",
    "recommendIntention": "客户试图回避谈论逾期还款的话题",
    "recommendScript": "朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。",
    "intentionScript": "朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。"
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "003D019A-1BB3-53EC-A0D2-CE76DA5D73B1",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |

暂无变更历史
