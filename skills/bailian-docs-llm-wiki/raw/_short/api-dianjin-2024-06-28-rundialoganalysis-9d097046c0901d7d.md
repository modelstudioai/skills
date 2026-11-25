# RunDialogAnalysis - 会话分析结果生成

流式接口，获取会话分析结果。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/RunDialogAnalysis)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:RunDialogAnalysis</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/virtualHuman/dialog/stream/analysis HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 id | llm-xxxx |
| body | object | 否 | 请求体参数。 |  |
| sessionId | string | 是 | 会话 ID | 1759457905S001vejpvd6vej |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>ResultCode</p></div></td><td></td></tr><tr><td>success</td><td>boolean</td><td><div><p>是否成功</p></div></td><td>true</td></tr><tr><td>dataType</td><td>string</td><td><div><p>数据类型</p></div></td><td>null</td></tr><tr><td>time</td><td>string</td><td><div><p>时间戳</p></div></td><td>2024-04-24 11:54:34</td></tr><tr><td>errCode</td><td>string</td><td><div><p>错误码</p></div></td><td>0</td></tr><tr><td>message</td><td>string</td><td><div><p>错误信息</p></div></td><td>ok</td></tr><tr><td>data</td><td>object</td><td><div><p>响应数据</p></div></td><td></td></tr><tr><td>dialogAnalysisRespList</td><td>array&lt;object&gt;</td><td><div><p>会话分析结果列表</p></div></td><td></td></tr><tr><td>dialogAnalysisRespList</td><td>object</td><td><div><p>会话分析结果</p></div></td><td></td></tr><tr><td>sessionId</td><td>string</td><td><div><p>会话 ID</p></div></td><td>1759457905S001vejpvd6vej</td></tr><tr><td>gmtCreate</td><td>string</td><td><div><p>会话的创建时间</p></div></td><td>2024-04-24 11:54:34</td></tr><tr><td>status</td><td>string</td><td><div><p>会话分析的任务执行状态</p></div><div><div>枚举值：</div><ul><li>success：success。</li><li>pending：pending。</li><li>error：error。</li></ul></div></td><td>success</td></tr><tr><td>analysisResp</td><td>object</td><td><div><p>会话分析的结果</p></div></td><td></td></tr><tr><td>dialogLabels</td><td>array&lt;object&gt;</td><td><div><p>会话标签列表</p></div></td><td></td></tr><tr><td>dialogLabel</td><td>object</td><td><div><p>会话标签</p></div></td><td></td></tr><tr><td>name</td><td>string</td><td><div><p>标签名称</p></div></td><td>二级标签</td></tr><tr><td>value</td><td>string</td><td><div><p>标签值</p></div></td><td>协商还款</td></tr><tr><td>dialogSummary</td><td>string</td><td><div><p>会话摘要</p></div></td><td>- 是否有资金需求：否\\n- 是否有意向：否，客户认为自己已经解决，对当前状态表示不解\\n- 是否可营销：否，对话中未表现出对营销信息的兴趣或接受度\\n- 待满足需求：客户希望在三天内解决问题</td></tr><tr><td>dialogExecPlan</td><td>string</td><td><div><p>会话执行计划</p></div></td><td>1. 核实客户账户信息，确认还款情况。\\n2. 若未收到还款，联系财务部门确认是否到账延迟。\\n3. 若已还款，更新客户记录并致歉。\\n4. 跟进客户，确保问题解决。</td></tr><tr><td>dialogSop</td><td>string</td><td><div><p>会话 SOP</p></div></td><td>营销</td></tr><tr><td>dialogProcessAnalysis</td><td>object</td><td><div><p>会话过程分析</p></div></td><td></td></tr><tr><td></td><td>any</td><td><div><p>会话过程分析内容</p></div></td><td>{ &quot;dialogues&quot;: [ { &quot;result&quot;: [ { &quot;value&quot;: &quot;开场白&quot;, &quot;key&quot;: &quot;客服&quot; }, { &quot;value&quot;: &quot;拒绝&quot;, &quot;key&quot;: &quot;客户&quot; } ], &quot;round&quot;: 1.0 }, { &quot;result&quot;: [ { &quot;value&quot;: &quot;挽留&quot;, &quot;key&quot;: &quot;客服&quot; }, { &quot;value&quot;: &quot;中性&quot;, &quot;key&quot;: &quot;客户&quot; } ], &quot;round&quot;: 2.0 } ], &quot;dialogProcessAnalysisStr&quot;: &quot;第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性&quot; }</td></tr><tr><td>dialogOpenAnalysis</td><td>object</td><td><div><p>会话开放分析</p></div></td><td></td></tr><tr><td></td><td>any</td><td><div><p>会话开放分析内容</p></div></td><td>{ &quot;dialogues&quot;: [ { &quot;result&quot;: [ { &quot;value&quot;: &quot;开场白&quot;, &quot;key&quot;: &quot;客服&quot; }, { &quot;value&quot;: &quot;拒绝&quot;, &quot;key&quot;: &quot;客户&quot; } ], &quot;round&quot;: 1.0 }, { &quot;result&quot;: [ { &quot;value&quot;: &quot;挽留&quot;, &quot;key&quot;: &quot;客服&quot; }, { &quot;value&quot;: &quot;中性&quot;, &quot;key&quot;: &quot;客户&quot; } ], &quot;round&quot;: 2.0 } ], &quot;dialogProcessAnalysisStr&quot;: &quot;第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性&quot; }</td></tr><tr><td>failNode</td><td>array</td><td><div><p>失败节点列表</p></div></td><td></td></tr><tr><td>failNode</td><td>string</td><td><div><p>失败节点</p></div></td><td>DIALOG_OPEN_ANALYSIS</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id</p></div></td><td>02CD4454-3F2C-57D0-9060-68DEAA1F6993</td></tr><tr><td>cost</td><td>long</td><td><div><p>耗时</p></div></td><td>null</td></tr></tbody></table>

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
        "sessionId": "1759457905S001vejpvd6vej",
        "gmtCreate": "2024-04-24 11:54:34\n",
        "status": "success",
        "analysisResp": {
          "dialogLabels": [
            {
              "name": "二级标签",
              "value": "协商还款"
            }
          ],
          "dialogSummary": "- 是否有资金需求：否\\\\n- 是否有意向：否，客户认为自己已经解决，对当前状态表示不解\\\\n- 是否可营销：否，对话中未表现出对营销信息的兴趣或接受度\\\\n- 待满足需求：客户希望在三天内解决问题",
          "dialogExecPlan": "1. 核实客户账户信息，确认还款情况。\\\\n2. 若未收到还款，联系财务部门确认是否到账延迟。\\\\n3. 若已还款，更新客户记录并致歉。\\\\n4. 跟进客户，确保问题解决。",
          "dialogSop": "营销",
          "dialogProcessAnalysis": {
            "key": {
              "dialogues": [
                {
                  "result": [
                    {
                      "value": "开场白",
                      "key": "客服"
                    },
                    {
                      "value": "拒绝",
                      "key": "客户"
                    }
                  ],
                  "round": 1
                },
                {
                  "result": [
                    {
                      "value": "挽留",
                      "key": "客服"
                    },
                    {
                      "value": "中性",
                      "key": "客户"
                    }
                  ],
                  "round": 2
                }
              ],
              "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性"
            }
          },
          "dialogOpenAnalysis": {
            "key": {
              "dialogues": [
                {
                  "result": [
                    {
                      "value": "开场白",
                      "key": "客服"
                    },
                    {
                      "value": "拒绝",
                      "key": "客户"
                    }
                  ],
                  "round": 1
                },
                {
                  "result": [
                    {
                      "value": "挽留",
                      "key": "客服"
                    },
                    {
                      "value": "中性",
                      "key": "客户"
                    }
                  ],
                  "round": 2
                }
              ],
              "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性"
            }
          }
        },
        "failNode": [
          "DIALOG_OPEN_ANALYSIS"
        ]
      }
    ]
  },
  "requestId": "02CD4454-3F2C-57D0-9060-68DEAA1F6993",
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
