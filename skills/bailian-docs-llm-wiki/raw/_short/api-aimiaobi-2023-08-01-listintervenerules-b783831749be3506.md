# ListInterveneRules - 列出干预规则

获得干预规则列表。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListInterveneRules)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:ListInterveneRules</td><td>list</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| AgentKey | string | 是 | 业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey) | c160c841c8e54295bf2f441432785944\_p\_efm |
| PageIndex | integer | 否 | 页号 | 1 |
| PageSize | integer | 否 | 页面尺寸 | 10 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>PlainResult</p></div></td><td></td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>success</td></tr><tr><td>Data</td><td>object</td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>Count</td><td>long</td><td><div><p>数量</p></div></td><td>1</td></tr><tr><td>InterveneRuleList</td><td>array&lt;object&gt;</td><td><div><p>规则列表</p></div></td><td></td></tr><tr><td>InterveneRuleList</td><td>object</td><td><div><p>规则描述</p></div></td><td></td></tr><tr><td>AnswerConfig</td><td>array&lt;object&gt;</td><td><div><p>答案配置</p></div></td><td></td></tr><tr><td>AnswerConfig</td><td>object</td><td><div><p>答案配置项</p></div></td><td></td></tr><tr><td>AnswerType</td><td>integer</td><td><div><p>答案类型</p></div><div><div>枚举值：</div><ul><li>0-统一回复：0-统一回复。</li><li>1-定向回复 ：1-定向回复 。</li></ul></div></td><td>0</td></tr><tr><td>Message</td><td>string</td><td><div><p>答案内容</p></div></td><td>抱歉我无法回答</td></tr><tr><td>Namespace</td><td>string</td><td><div><p>命名空间</p></div></td><td>namespace_qa_query</td></tr><tr><td>CreateTime</td><td>string</td><td><div><p>创建时间</p></div></td><td>2023-06-05 15:17:01</td></tr><tr><td>EffectTime</td><td>string</td><td><div><p>生效时间</p></div></td><td>2023-04-03 02:42:01</td></tr><tr><td>InterveneType</td><td>integer</td><td><div><p>干预类型</p></div><div><div>枚举值：</div><ul><li>0-永久生效：0-永久生效。</li><li>1-按时间生效：1-按时间生效。</li></ul></div></td><td>0</td></tr><tr><td>NamespaceList</td><td>array</td><td><div><p>命名空间列表</p></div></td><td></td></tr><tr><td>NamespaceList</td><td>string</td><td><div><p>干预范围</p></div><div><div>枚举值：</div><ul><li>namespace_qa_query （问答输入干预）：namespace_qa_query （问答输入干预）。</li><li>namespace_qa_result （问答结果干预）：namespace_qa_result （问答结果干预）。</li><li>namespace_writing_result （写作结果干预）：namespace_writing_result （写作结果干预）。</li><li>namespace_writing_query （写作输入干预）：namespace_writing_query （写作输入干预）。</li></ul></div></td><td>namespace_qa_query</td></tr><tr><td>RuleId</td><td>long</td><td><div><p>规则 id</p></div></td><td>mr-iuo9pi9w555phfbb</td></tr><tr><td>RuleName</td><td>string</td><td><div><p>规则名字</p></div></td><td>ruletest</td></tr><tr><td>PageIndex</td><td>integer</td><td><div><p>页号</p></div></td><td>1</td></tr><tr><td>PageSize</td><td>integer</td><td><div><p>页尺寸</p></div></td><td>10</td></tr><tr><td>Code</td><td>integer</td><td><div><p>干预服务返回的状态码</p></div></td><td>200</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 状态码</p></div></td><td>200</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误说明</p></div></td><td>success</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>DA021073-17CE-5CCF-9FEB-93226C766887</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td>true</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "success",
  "Data": {
    "Count": 1,
    "InterveneRuleList": [
      {
        "AnswerConfig": [
          {
            "AnswerType": 0,
            "Message": "抱歉我无法回答",
            "Namespace": "namespace_qa_query"
          }
        ],
        "CreateTime": "2023-06-05 15:17:01",
        "EffectTime": "2023-04-03 02:42:01",
        "InterveneType": 0,
        "NamespaceList": [
          "namespace_qa_query"
        ],
        "RuleId": 0,
        "RuleName": "ruletest"
      }
    ],
    "PageIndex": 1,
    "PageSize": 10,
    "Code": 200
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "DA021073-17CE-5CCF-9FEB-93226C766887",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
