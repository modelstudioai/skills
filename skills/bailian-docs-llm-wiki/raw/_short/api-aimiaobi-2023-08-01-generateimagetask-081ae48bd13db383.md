# GenerateImageTask - 生成智能配图任务

根据文字异步生成图片。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GenerateImageTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:GenerateImageTask</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AgentKey</td><td>string</td><td>是</td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td>e1be065b-adc3-435e-bd01-1c18c5ed75d3</td></tr><tr><td>ParagraphList</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>段落内容</p></div></td><td></td></tr><tr><td>ParagraphList</td><td>object</td><td>是</td><td></td><td></td></tr><tr><td>Content</td><td>string</td><td>是</td><td><div><p>段落内容</p></div></td><td>一直忧伤的猫</td></tr><tr><td>Id</td><td>long</td><td>是</td><td><div><p>段落 ID</p></div></td><td>1</td></tr><tr><td>TaskId</td><td>string</td><td>否</td><td><div><p>任务唯一标识</p><div><div><strong>说明</strong> TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</div></div></div></td><td>e1be065b-adc3-435e-bd01-1c18c5ed75d3</td></tr><tr><td>TaskStatus</td><td>string</td><td>否</td><td><div><p>当前任务状态</p><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUSPENDED：任务挂起</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></td><td>SUCCESSED</td></tr><tr><td>Style</td><td>string</td><td>是</td><td><div><p>风格</p></div><div><div>枚举值：</div><ul><li>&lt;portrait&gt;：人像写真。</li><li>&lt;auto&gt;：默认风格。</li><li>&lt;3d cartoon&gt;：3D卡通。</li><li>watercolor：水彩。</li><li>&lt;photography&gt;：摄影。</li><li>&lt;flat illustration&gt;：扁平插画。</li><li>&lt;sketch&gt;：素描。</li><li>&lt;oil painting&gt;：油画。</li><li>&lt;chinese painting&gt;：中国画。</li><li>&lt;anime&gt;：动画。</li></ul></div></td><td>'&lt;auto&gt;'</td></tr><tr><td>Size</td><td>string</td><td>是</td><td><div><p>生成图片尺寸</p></div><div><div>枚举值：</div><ul><li>1024*1024：1024*1024。</li><li>720*1280：720*1280。</li><li>1280*720：1280*720。</li></ul></div></td><td>1024*1024</td></tr><tr><td>ArticleTaskId</td><td>string</td><td>是</td><td><div><p>文章 taskId，如目前没有，可以赋值为 UUID</p></div></td><td>e1be065b-adc3-435e-bd01-1c18c5ed75d3</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PlainResult |  |
| Code | string | 状态码 | successful |
| Data | object | 业务数据 |  |
| TaskList | array<object> | 段落任务信息，根据输入的段落 ID 进行关联 |  |
| TaskList | object | 段落对象 |  |
| Content | string | 段落内容 | 一直忧伤的猫 |
| Id | long | 段落 ID | 1 |
| TaskId | string | 任务 ID 任务唯一标识 | e1be065b-adc3-435e-bd01-1c18c5ed75d3 |
| TaskStatus | string | 当前任务状态 SUCCESSED=任务执行成功 ，FAILED=任务执行失败 ，CANCELED=任务被取消 ，PENDIN=任务排队中 ，SUSPENDE=任务挂起 RUNNIN=任务处理中 | SUCCESSED |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误说明 | successful |
| RequestId | string | 请求唯一标识 | F2F366D6-E9FE-1006-BB70-2C650896AAB5 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "successful",
  "Data": {
    "TaskList": [
      {
        "Content": "一直忧伤的猫",
        "Id": 1,
        "TaskId": "e1be065b-adc3-435e-bd01-1c18c5ed75d3",
        "TaskStatus": "SUCCESSED"
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
