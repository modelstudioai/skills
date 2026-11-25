# SseChat - 问答接口

SSE问答接口。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/BailianChatBot/2024-11-05/SseChat)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>bailianchatbot:SseChat</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /sse/bailian/chat HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AppId</td><td>string</td><td>是</td><td><div><p>应用 ID，通过控制台创建和查询，仅支持传单个 ID。</p></div></td><td>chatbot-cn-dDmF3jcdVf</td></tr><tr><td>Utterance</td><td>string</td><td>是</td><td><div><p>机器人访问者的输入</p></div></td><td>你有什么技能？</td></tr><tr><td>SessionId</td><td>string</td><td>否</td><td><div><p>会话 ID，⽤于标识⼀个访问者的会话和保持上下⽂信息。</p></div></td><td>15e04f27-acd7-489d-872f-1d68f7535e33</td></tr><tr><td>SenderId</td><td>string</td><td>否</td><td><div><p>访问者 ID。⽤于识别当前会话中的⽤户</p></div></td><td>uid129312098593</td></tr><tr><td>SenderNick</td><td>string</td><td>否</td><td><div><p>访问者昵称</p></div></td><td>张三</td></tr><tr><td>VendorParam</td><td>string</td><td>否</td><td><div><p>是一个 JSON 格式的用户自定义参数集（随路参数），可以传入用户自定义的参数到各对话引擎，例如：</p><ul><li><p>参数为单个值：{&quot;phone&quot;:123456789}</p></li><li><p>参数为数组：{&quot;name&quot;:[&quot;a&quot;,&quot;b&quot;,&quot;c&quot;]}</p></li><li><p>文档标签：{&quot;docLabels&quot;:&quot;标签 1,标签 2&quot;}</p></li></ul></div></td><td>{&quot;docLabels&quot;:&quot;标签1,标签2&quot;}</td></tr><tr><td>Command</td><td>string</td><td>否</td><td><div><p>请求的指令信息。</p><p>当前支持传入</p><ul><li>TIMEOUT：触发对话工厂超时话术。</li><li>GUIDEPOST：触发流程异步服务，详见异步服务使用手册。</li></ul></div></td><td>TIMEOUT</td></tr><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p>百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/use-workspace">获取 workspaceId</a></p></div></td><td>llm-g7jspxljq8k909h3</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | 请求 ID。 | 30D68C4C-4512-58A7-A328-568015B39A02 |
| Data | any | 返回的数据。 | 详见返回参数补充说明 |
| Success | boolean | 是否成功 | True |
| Message | string | 错误说明 | success |
| Code | string | 结果码 | 200 |

<a id="示例说明"></a>

<a id="responseParamsSupplement"></a>

## 示例说明

<a id="返回示例"></a>

### 返回示例

<a id="code-block-2"></a>

```json
{
    "MessageBody": {
        "DirectMessageBody": {
            "ContentType": "RICH_TEXT",
            "Ext": {},
            "HitSystemAskConfig": "GPTQA_MODEL",
            // 大模型输出的答案：把 SentenceList 列表每一个 content 为一个段落。
            "SentenceList": [
                {
                    "Content": "我作为一名人工智能助手，"
                }
            ]
        },
        "Type": "Direct"
    },
    "MessageId": "d8720210-9588-4b49-b412-09648621a073",
    "SequenceId": "f186e72492214631a6a150b2288d269f",
    "SessionId": "cidu1dmqF8iUdz2gNonzzZAhsWsocstnJqThr+wp430evc=",
    "Source": "SYSTEM_ASK_CONFIG",
    "StreamEnd": false
}
```

<a id="其他的响应示例"></a>

### 其他的响应示例

Source=TASK\_DRIVEN\_DIALOGUE

<a id="code-block-3"></a>

```json
{
    "MessageBody":{
        "Commands":{},
        "DirectMessageBody":{
            "ContentType":"PLAIN_TEXT",
            "Ext":{
                "EXTERNAL_FLAGS":{}
            },
            "SentenceList":[
                {
                    "Content":"北京市晴，气温 8 摄氏度，东风 ≤3 级"
                }
            ]
        },
        "Type":"Direct"
    },
    "MessageId":"7a2cdb51-af56-4ac9-9c6d-108905695ac9",
    "SequenceId":"4861074fe523498ba3f397e876b60105",
    "SessionId":"f3d7e960933411ee96144bea43fe4df3",
    "Source":"TASK_DRIVEN_DIALOGUE",
    "StreamEnd":true
}
```

Source=NON\_STRUCTURAL\_KNOWLEDGE

<a id="code-block-4"></a>

```json
{
    "MessageBody":{
        "DirectMessageBody":{
            "AnswerReference":{
                "ItemList":[
                    {
                        "Content":"你好",
                        "ContentType":"RICH_TEXT",
                        "DataSource":"FAQ_DIRECT",
                        "Number":1,
                        "ReferenceExt":{
                            "DocName":"FAQ 知识库"
                        },
                        "Title":"你好"
                    }
                ]
            },
            "ContentType":"RICH_TEXT",
            "SentenceList":[
                {
                    "Content":"你好",
                    "ReferNumber":1
                }
            ]
        },
        "Type":"Direct"
    },
    "MessageId":"808a9cfb-2cec-4230-aad1-66c28df6040e",
    "SequenceId":"32a052f098c14769b8b81ac202f38d01",
    "SessionId":"595fa8a0940611eeb59a155f6621f5d6",
    "Source":"NON_STRUCTURAL_KNOWLEDGE",
    "StreamEnd":true
}
```

Source=SYSTEM\_ASK\_CONFIG

<a id="code-block-5"></a>

```json
{
    "MessageBody":{
        "DirectMessageBody":{
            "ContentType":"PLAIN_TEXT",
            "HitSystemAskConfig":"NO_ANSWER",
            "SentenceList":[
                {
                    "Content":"我还没有学会这个问题，已经记录会尽快学习为您解答，请尝试询问我其他问题"
                }
            ]
        },
        "Type":"Direct"
    },
    "MessageId":"f13833e7-9ca4-4a5b-8878-f5cc8a0a327c",
    "SequenceId":"245c39ce1f11406bb3cf60b4d017dff0",
    "SessionId":"6e7c44a0940111ee91e69d173591e2de",
    "Source":"SYSTEM_ASK_CONFIG",
    "StreamEnd":true
}
```

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-6"></a>

```text
{
  "RequestId": "30D68C4C-4512-58A7-A328-568015B39A02",
  "Data": "详见返回参数补充说明",
  "Success": true,
  "Message": "success",
  "Code": 200
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/BailianChatBot/2024-11-05/errorCode)查看更多错误码。
