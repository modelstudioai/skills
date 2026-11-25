# InsertInterveneRule - 插入干预规则

插入干预规则。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InsertInterveneRule)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:InsertInterveneRule</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AgentKey</td><td>string</td><td>是</td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td>xxxxx_p_efm</td></tr><tr><td>InterveneRuleConfig</td><td>object</td><td>否</td><td><div><p>干预规则配置</p></div></td><td></td></tr><tr><td>AnswerConfig</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>答案配置</p></div></td><td></td></tr><tr><td>AnswerConfig</td><td>object</td><td>否</td><td><div><p>答案配置项</p></div></td><td></td></tr><tr><td>AnswerType</td><td>integer</td><td>否</td><td><div><p>答案类型</p></div><div><div>枚举值：</div><ul><li>1-定向回复：1-定向回复。</li><li>0-统一回复： 0-统一回复。</li></ul></div></td><td>0</td></tr><tr><td>Message</td><td>string</td><td>否</td><td><div><p>答案内容</p></div></td><td>抱歉我无法回答</td></tr><tr><td>Namespace</td><td>string</td><td>否</td><td><div><p>命名空间</p></div><div><div>枚举值：</div><ul><li>namespace_writing_query （写作输入干预）： namespace_writing_query （写作输入干预）。</li><li>namespace_qa_result （问答结果干预）： namespace_qa_result （问答结果干预）。</li><li>namespace_qa_query （问答输入干预）：namespace_qa_query （问答输入干预）。</li><li>namespace_writing_result （写作结果干预）： namespace_writing_result （写作结果干预）。</li></ul></div></td><td>namespace_qa_query</td></tr><tr><td>EffectConfig</td><td>object</td><td>否</td><td><div><p>生效配置</p></div></td><td></td></tr><tr><td>EffectType</td><td>integer</td><td>否</td><td><div><p>生效类型</p></div><div><div>枚举值：</div><ul><li>0-永久生效 ：0-永久生效 。</li><li>1-按时间生效：1-按时间生效。</li></ul></div></td><td>0</td></tr><tr><td>EndTime</td><td>string</td><td>否</td><td><div><p>结束时间</p></div></td><td>2023-03-28 06:04:29</td></tr><tr><td>StartTime</td><td>string</td><td>否</td><td><div><p>开始时间</p></div></td><td>2023-03-28 06:04:29</td></tr><tr><td>InterveneConfigList</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>干预配置列表</p></div></td><td></td></tr><tr><td>InterveneConfigList</td><td>object</td><td>否</td><td></td><td></td></tr><tr><td>Id</td><td>string</td><td>否</td><td><div><p>id</p></div></td><td>37249</td></tr><tr><td>OperationType</td><td>integer</td><td>否</td><td><div><p>操作类型</p></div><div><div>枚举值：</div><ul><li>0-新建：0-新建。</li><li>1-更新 ： 1-更新 。</li><li>2-删除：2-删除。</li></ul></div></td><td>0</td></tr><tr><td>Query</td><td>string</td><td>否</td><td><div><p>干预 query 配置</p></div></td><td>早上好</td></tr><tr><td>InterveneType</td><td>integer</td><td>否</td><td><div><p>干预类型</p></div><div><div>枚举值：</div><ul><li>0-相似问干预项目：0-相似问干预项目。</li><li>2-正则表达式干预项 ： 2-正则表达式干预项 。</li><li>3-关键词库干预项：3-关键词库干预项。</li><li>4-URL干预： 4-URL干预。</li><li>1-关键词表达式干预项：1-关键词表达式干预项。</li></ul></div></td><td>0</td></tr><tr><td>NamespaceList</td><td>array</td><td>否</td><td><div><p>命名空间列表</p></div></td><td></td></tr><tr><td>NamespaceList</td><td>string</td><td>否</td><td><div><p>干预维度</p></div><div><div>枚举值：</div><ul><li>namespace_writing_image （智能配图）：namespace_writing_image （智能配图）。</li><li>namespace_qa_query （问答输入干预）：namespace_qa_query （问答输入干预）。</li><li>namespace_qa_article （问答参考）：namespace_qa_article （问答参考）。</li><li>namespace_writing_article （写作参考）：namespace_writing_article （写作参考）。</li><li>namespace_qa_result （问答结果干预）：namespace_qa_result （问答结果干预）。</li><li>namespace_writing_result （写作结果干预）：namespace_writing_result （写作结果干预）。</li><li>namespace_writing_query （写作输入干预）：namespace_writing_query （写作输入干预）。</li></ul></div></td><td>namespace_qa_query （问答输入干预）</td></tr><tr><td>RuleId</td><td>long</td><td>否</td><td><div><p>规则 Id</p></div></td><td>2</td></tr><tr><td>RuleName</td><td>string</td><td>否</td><td><div><p>规则名字</p></div></td><td>tf-test-rule</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PlainResult |  |
| Code | string | 状态码 | success |
| Data | object | 业务数据 |  |
| RuleId | long | 规则 id | 12345 |
| Code | integer | 干预服务返回的状态码 | 200 |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误说明 | successful |
| RequestId | string | 请求唯一标识 | DD656AF9-0839-521A-A3D2-F320009F9C87 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |

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
    "RuleId": 12345,
    "Code": 200
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "DD656AF9-0839-521A-A3D2-F320009F9C87",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
