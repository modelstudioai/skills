# GetDialogAnalysisResult - 获取会话分析结果

获取会话分析结果。可批量获取，根据会话ID列表或时间范围。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDialogAnalysisResult)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetDialogAnalysisResult</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/virtualHuman/dialog/analysis HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 id | llm-xxxx |
| body | object | 否 | 请求体参数。 |  |
| sessionIds | array | 否 | 会话 id 列表。useUrl 为 true 时，返回 ossUrl；支持 1000 个会话，超过 1000 个，返回前 1000 个会话的分析结果。useUrl 为 false 时，返回会话分析结果；仅支持 10 个会话，超过 10 个，返回前 10 个会话的分析结果。非必填。sessionIds 为空时根据起始时间和结束时间查询会话分析结果。不为空时，根据 sessionIds 查询会话分析结果。二者不可同时为空。 |  |
| sessionId | string | 否 | 会话 ID。 | 183764873624 |
| useUrl | boolean | 否 | 返回结果是否为 ossUrl。为 true 时，返回结果 ossUrl，链接有效期为 1 小时。默认为 true；支持 1000 个会话，超过 1000 个，返回前 1000 个会话的分析结果。为 false 时，返回会话分析结果；仅支持 10 个会话，超过 10 个，返回前 10 个会话的分析结果。 | true |
| startTime | string | 否 | 起始时间, 格式为 yyyy-MM-dd HH:mm:ss。sessionIds 不为空时，根据 sessionIds 查询会话分析结果。 | 2024-09-14 09:11:00 |
| endTime | string | 否 | 结束时间, 格式为 yyyy-MM-dd HH:mm:ss。sessionIds 不为空时，根据 sessionIds 查询会话分析结果。 | 2024-09-23 09:20:02 |
| asc | boolean | 否 | 是否升序, 默认为 true，按会话创建时间升序排序。为 false 时，按会话创建时间降序排序。 | true |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>响应体参数。</p></div></td><td></td></tr><tr><td>success</td><td>boolean</td><td><div><p>是否成功</p></div></td><td>true</td></tr><tr><td>dataType</td><td>string</td><td><div><p>数据类型</p></div></td><td>null</td></tr><tr><td>time</td><td>string</td><td><div><p>时间戳</p></div></td><td>2024-04-24 11:54:34</td></tr><tr><td>errCode</td><td>string</td><td><div><p>错误码</p></div></td><td>0</td></tr><tr><td>message</td><td>string</td><td><div><p>错误信息</p></div></td><td>ok</td></tr><tr><td>data</td><td>object</td><td><div><p>响应数据</p></div></td><td></td></tr><tr><td>dialogAnalysisRespList</td><td>array&lt;object&gt;</td><td><div><p>会话分析结果列表</p></div></td><td></td></tr><tr><td>dialogAnalysisRespList</td><td>object</td><td><div><p>会话分析结果</p></div></td><td></td></tr><tr><td>sessionId</td><td>string</td><td><div><p>会话 ID</p></div></td><td>183764873624</td></tr><tr><td>gmtCreate</td><td>string</td><td><div><p>会话的创建时间</p></div></td><td>2024-04-24 11:54:34</td></tr><tr><td>status</td><td>string</td><td><div><p>会话分析的任务执行状态。</p><ul><li>init 表示未开始</li><li>pending 表示会话分析任务正在排队中</li><li>running 表示会话分析任务正在进行中</li><li>error 表示会话分析任务执行失败</li><li>success 表示会话分析任务执行成功</li></ul></div></td><td>running</td></tr><tr><td>ossUrl</td><td>string</td><td><div><p>会话分析的结果,ossUrl 形式，过期时间为一小时。</p></div></td><td><a href="https://xxx.oss-cn-beijing.aliyuncs.com/dialog-analysis/2024-12-30/2/1826661605606129665">https://xxx.oss-cn-beijing.aliyuncs.com/dialog-analysis/2024-12-30/2/1826661605606129665</a></td></tr><tr><td>analysisResp</td><td>object</td><td><div><p>会话分析的结果</p></div></td><td></td></tr><tr><td>dialogLabels</td><td>array&lt;object&gt;</td><td><div><p>会话标签列表</p></div></td><td></td></tr><tr><td>dialogLabel</td><td>object</td><td><div><p>会话标签</p></div></td><td></td></tr><tr><td>name</td><td>string</td><td><div><p>标签名称</p></div></td><td>额度不足</td></tr><tr><td>value</td><td>string</td><td><div><p>标签值</p></div></td><td>0</td></tr><tr><td>dialogSummary</td><td>string</td><td><div><p>会话摘要</p></div></td><td>- 是否有资金需求：不确定，客户未明确表示有无资金需求。\n- 是否有意向：不确定，客户未明确表达意向。\n- 是否可营销：不可营销，客户对客服的多次询问未表现出兴趣，且对话中提到因不适希望减少联系。\n- 待满足需求：客户希望了解具体的预审额度信息。</td></tr><tr><td>dialogExecPlan</td><td>string</td><td><div><p>会话执行计划</p></div></td><td>1. 客服应再次确认客户的疑问是否已解决，特别是关于额度的具体数额。\n2. 如果客户仍有疑问，提供客服热线电话，建议客户直接拨打以获取更详细的帮助。\n3. 提醒客户检查短信中的链接，以便快速查看和操作。\n4. 记录此次通话中客户表现出的任何不适或不便，确保后续跟进时更加体贴。\n5. 发送一条包含操作指南的短信，确保客户能够轻松找到并使用服务。\n6. 结束通话前，再次感谢客户的支持，并表达希望客户早日康复的愿望。</td></tr><tr><td>dialogSop</td><td>string</td><td><div><p>会话 SOP</p></div></td><td>产品介绍</td></tr><tr><td>dialogProcessAnalysis</td><td>object</td><td><div><p>会话过程分析</p></div></td><td>{ &quot;dialogues&quot;: [ { &quot;round&quot;: 1, &quot;result&quot;: [ { &quot;key&quot;: &quot;客服&quot;, &quot;value&quot;: &quot;客服回应标签&quot; }, { &quot;key&quot;: &quot;客户&quot;, &quot;value&quot;: &quot;客户回应态度标签&quot; } ] }, { &quot;round&quot;: 2, &quot;result&quot;: [ { &quot;key&quot;: &quot;客服&quot;, &quot;value&quot;: &quot;客服回应标签&quot; }, { &quot;key&quot;: &quot;客户&quot;, &quot;value&quot;: &quot;客户回应态度标签&quot; } ] } ], &quot;dialogProcessAnalysisStr&quot;:&quot;第一轮对话：客服-客服回应标签，客户-客户回应态度标签 第二轮对话：客服-客服回应标签，客户-客户回应态度标签&quot; }</td></tr><tr><td>dialogOpenAnalysis</td><td>object</td><td><div><p>会话开放分析</p></div></td><td>{ &quot;dialogues&quot;: [ { &quot;round&quot;: 1, &quot;result&quot;: [ { &quot;key&quot;: &quot;对话主题&quot;, &quot;value&quot;: &quot;XX&quot; }, { &quot;key&quot;: &quot;客户反应&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;客户反应分析&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;客服话术&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;本轮客服话术修改建议&quot;, &quot;value&quot;: &quot;XXX&quot; } ] }, { &quot;round&quot;: 2, &quot;result&quot;: [ { &quot;key&quot;: &quot;对话主题&quot;, &quot;value&quot;: &quot;XX&quot; }, { &quot;key&quot;: &quot;客户反应&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;客户反应分析&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;客服话术&quot;, &quot;value&quot;: &quot;XXX&quot; }, { &quot;key&quot;: &quot;本轮客服话术修改建议&quot;, &quot;value&quot;: &quot;XXX&quot; } ] } ], &quot;dialogOpenAnalysisStr&quot;:&quot;第一轮对话：对话主题-xx##客户反应-xx##客户反应分析-xx##客服话术-xx##本轮客服话术修改建议-xx 第二轮对话：对话主题-xx##客户反应-xx##客户反应分析-xx##客服话术-xx##本轮客服话术修改建议-xx&quot; }</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id</p></div></td><td>88A006F0-B565-53BA-B38A-DBDF9D0B2935</td></tr><tr><td>cost</td><td>long</td><td><div><p>耗时</p></div></td><td>null</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": {
    "dialogAnalysisRespList": [
      {
        "sessionId": 183764873624,
        "gmtCreate": "2024-04-24 11:54:34\n",
        "status": "running",
        "ossUrl": "https://xxx.oss-cn-beijing.aliyuncs.com/dialog-analysis/2024-12-30/2/1826661605606129665",
        "analysisResp": {
          "dialogLabels": [
            {
              "name": "额度不足",
              "value": 0
            }
          ],
          "dialogSummary": "- 是否有资金需求：不确定，客户未明确表示有无资金需求。\\n- 是否有意向：不确定，客户未明确表达意向。\\n- 是否可营销：不可营销，客户对客服的多次询问未表现出兴趣，且对话中提到因不适希望减少联系。\\n- 待满足需求：客户希望了解具体的预审额度信息。",
          "dialogExecPlan": "1. 客服应再次确认客户的疑问是否已解决，特别是关于额度的具体数额。\\n2. 如果客户仍有疑问，提供客服热线电话，建议客户直接拨打以获取更详细的帮助。\\n3. 提醒客户检查短信中的链接，以便快速查看和操作。\\n4. 记录此次通话中客户表现出的任何不适或不便，确保后续跟进时更加体贴。\\n5. 发送一条包含操作指南的短信，确保客户能够轻松找到并使用服务。\\n6. 结束通话前，再次感谢客户的支持，并表达希望客户早日康复的愿望。",
          "dialogSop": "产品介绍",
          "dialogProcessAnalysis": {
            "test": "test",
            "test2": 1
          },
          "dialogOpenAnalysis": {
            "test": "test",
            "test2": 1
          }
        }
      }
    ]
  },
  "requestId": "88A006F0-B565-53BA-B38A-DBDF9D0B2935",
  "cost": 0
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
