# RunCommentGeneration - 客户之声预测

针对指定文章，预测用户之声。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCommentGeneration)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:RunCommentGeneration</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/aimiaobi/runCommentGeneration HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p>路径参数，阿里云百炼业务空间唯一标识：获取<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">业务空间 ID（Workspace ID）</a></p></div></td><td>llm-3kcs1w3lltrtbfkr</td></tr><tr><td>SessionId</td><td>string</td><td>否</td><td><div><p>对话 Id</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr><tr><td>Length</td><td>string</td><td>否</td><td><div><p>一条评论的长度</p></div></td><td>20</td></tr><tr><td>NumComments</td><td>string</td><td>是</td><td><div><p>评论的条数</p></div></td><td>10</td></tr><tr><td>Style</td><td>string</td><td>否</td><td><div><p>评论的风格</p></div></td><td>积极正面</td></tr><tr><td>SourceMaterial</td><td>string</td><td>是</td><td><div><p>要评论的文章</p></div></td><td>ps5是sony新一代的游戏机，他创新性的...</td></tr><tr><td>AllowEmoji</td><td>boolean</td><td>否</td><td><div><p>是否允许使用表情默认为 false</p></div></td><td>true</td></tr><tr><td>Type</td><td>object</td><td>是</td><td><div><p>评论类型</p><p>key 可选值</p><ul><li>emotion （情感表达型）</li><li>opinion （观点阐述型）</li><li>interaction （互动交流型）</li><li>experience （经验分享型）</li><li>humor （幽默调侃型）</li></ul></div></td><td>{&quot;emotion&quot;:&quot;50&quot;,&quot;opinion&quot;:&quot;50&quot;}</td></tr><tr><td>Sentiment</td><td>object</td><td>是</td><td><div><p>情感倾向</p><p>key 可选值</p><ul><li>positive （正向）</li><li>neutral （中立）</li><li>negative （负向）</li></ul></div></td><td>{&quot;positive&quot;:&quot;50&quot;,&quot;negative&quot;:&quot;50&quot;}</td></tr><tr><td>LengthRange</td><td>object</td><td>是</td><td><div><p>长度范围</p><p>key 可选值</p><ul><li>short （20 字以内）</li><li>medium （20-50 字）</li><li>long （50-100 字）</li></ul></div></td><td>{&quot;short&quot;:&quot;50&quot;,&quot;long&quot;:“50”}</td></tr><tr><td>ExtraInfo</td><td>string</td><td>否</td><td><div><p>补充要求</p></div></td><td>不要输出额外其他信息</td></tr><tr><td>ModelId</td><td>string</td><td>否</td><td><div><p>模型 id</p></div></td><td>quanmiao-max、quanmiao-plus</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | Id of the request | 3f7045e099474ba28ceca1b4eb6d6e21 |
| End | boolean | 是否结束 |  |
| Header | object | 返回结果的 header |  |
| Event | string | event 名称 | result-generated |
| EventInfo | string | 事件描述 | 可空 |
| RequestId | string | 请求 RequestId | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| SessionId | string | 对话 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TaskId | string | 任务 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TraceId | string | 全链路 ID | 0bd58ea2-dc38-45da-ac02-17f05cb9040b |
| Payload | object | 响应体 |  |
| Output | object | 输出 |  |
| Text | string | 输出内容 | 评论内容 |
| Usage | object | token 用量 |  |
| InputTokens | long | 输入使用的 Token 数量 | 1 |
| OutputTokens | long | 输出 Token 数量 | 2 |
| TotalTokens | long | 总 token 数量 | 3 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true,
  "Header": {
    "Event": "result-generated\n",
    "EventInfo": "可空\n",
    "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "0bd58ea2-dc38-45da-ac02-17f05cb9040b"
  },
  "Payload": {
    "Output": {
      "Text": "评论内容"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 2,
      "TotalTokens": 3
    }
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
