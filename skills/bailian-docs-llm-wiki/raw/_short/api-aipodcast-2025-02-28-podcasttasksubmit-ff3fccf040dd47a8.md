# PodcastTaskSubmit - 播客任务提交

ai播客生成任务提交。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AIPodcast/2025-02-28/PodcastTaskSubmit)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aipodcast:PodcastTaskSubmit</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /podcast/task/submit HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>当前请求所使用的百炼业务空间 id</p></div></td><td>llm-ep8ba0dr6seiddxx</td></tr><tr><td>fileUrls</td><td>array</td><td>否</td><td><div><p>用播客任务生成的文件可访问链接</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>文件可访问链接</p></div></td><td><a href="http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202503241702148295/script.txt?OSSAccessKeyId=YOUR_ACCESS_KEY_ID****&amp;Expires=1742810622&amp;Signature=YOUR_SIGNATURE">http://xxx-ai-file.oss-cn-beijing.aliyuncs.com/202503241702148295/script.txt?OSSAccessKeyId=YOUR_ACCESS_KEY_ID****&amp;Expires=1742810622&amp;Signature=YOUR_SIGNATURE</a></td></tr><tr><td>topic</td><td>string</td><td>否</td><td><div><p>播客内容生成的主题</p></div></td><td>甲流来袭，我们该如何应对？</td></tr><tr><td>counts</td><td>integer</td><td>否</td><td><div><p>对话人数</p></div><div><div>枚举值：</div><ul><li>1：单人。</li><li>2：双人。</li></ul></div></td><td>2</td></tr><tr><td>voices</td><td>array</td><td>否</td><td><div><p>指定播客生成的人声音色，数组中的起始音色，为第一个对话人的音色</p></div><div><div>枚举值：</div><ul><li>Dylan：北京话-男声。</li><li>en_female：女声。</li><li>Cherry：女声。</li><li>Ethan：男声。</li><li>news_male：男声。</li><li>Jada：吴语-女声。</li><li>Chelsie：女声。</li><li>en_male：男声。</li><li>news_female：女声。</li><li>Serena：女声。</li><li>Sunny：四川话-女声。</li></ul></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>人声音色</p></div></td><td>news_female</td></tr><tr><td>text</td><td>string</td><td>否</td><td><div><p>文案</p></div></td><td>最近，甲型流感似乎成了大家热议的话题。但你真的了解甲流吗？它和普通感冒有什么区别？为什么症状看起来如此严重？更重要的是，我们应该如何预防和治疗？本期对话中，我们将深入探讨甲流的传播方式、易感人群以及科学的防护措施，帮助你在流感高发季节保护自己和家人的健康。</td></tr><tr><td>sourceLang</td><td>string</td><td>否</td><td><div><p>播客内容生成的结果（包含播客稿、播客音频）语种选型，目前仅支持中文及英文，默认语种为中文。</p></div></td><td>zh</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>code</td><td>string</td><td><div><p>响应状态码。</p></div></td><td>&quot;success&quot;</td></tr><tr><td>message</td><td>string</td><td><div><p>响应消息。</p></div></td><td>&quot;success&quot;</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id，用于追溯 API 调用链路。</p></div></td><td>9CE5B91A-6E6B-55FB-A1AF-037DF01C84B3</td></tr><tr><td>success</td><td>boolean</td><td><div><p>true 接口调用成功，false 接口调用失败</p></div></td><td>True</td></tr><tr><td>httpStatusCode</td><td>string</td><td><div><p>HTTP 状态码。</p></div></td><td>200</td></tr><tr><td>data</td><td>object</td><td><div><p>返回数据</p></div></td><td></td></tr><tr><td>taskId</td><td>string</td><td><div><p>任务唯一标识</p></div></td><td>63c4e0eaab3b4c0db208ecafa990e8d1</td></tr><tr><td>taskStatus</td><td>string</td><td><div><p>任务状态。</p><ul><li>PENDING：待执行</li><li>RUNNING：执行中</li><li>SUCCEEDED：成功</li><li>INVALID：失效</li><li>FAILED：失败</li><li>UNKNOWN： 未知</li></ul></div></td><td>SUCCEEDED</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "code": "success",
  "message": "success",
  "requestId": "9CE5B91A-6E6B-55FB-A1AF-037DF01C84B3",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "63c4e0eaab3b4c0db208ecafa990e8d1",
    "taskStatus": "SUCCEEDED"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AIPodcast/2025-02-28/errorCode)查看更多错误码。
