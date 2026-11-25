# CreateApplicationVersion

创建语音机器人应用版本。

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

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
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| bailianvoicebot:CreateApplicationVersion | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>BusinessUnitId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>百炼业务空间 ID</p></div></td><td><p>llm-c11iig67g863rih8</p></td></tr><tr><td>ApplicationId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>应用 ID</p></div></td><td><p>a395011f-a247-400f-bc69-28796749fd52</p></td></tr><tr><td>SourceVersionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>原 versionID(发布时使用)</p></div></td><td><p>20904943-f711-494f-9f1f-e7f340f37707</p></td></tr><tr><td>TranscriberConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>ASR 语音配置</p></div></td><td></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>ASR 访问方式</p></div></td><td><p>MANAGED</p></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><p>否</p></td><td><div><p>ASR 引擎类型</p></div></td><td><p>ALIYUN</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td><p>否</p></td><td><div><p>关联配置</p></div></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>三方语音配置 ID（使用豆包、科大等三方 ASR 服务时需配置）</p></div></td><td><p>c2c9baae-9351-4c49-a8cb-6f24a83a8718</p></td></tr><tr><td>VocabularyId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>热词表 ID</p></div></td><td><p>cd97223f-42f2-4cd9-95af-e734e2fe1fe3</p></td></tr><tr><td>EndSilenceTimeout</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>静音检测（说话间隔超过 x 毫秒时触发断句，即 VAD）</p></div></td><td><p>700</p></td></tr><tr><td>CustomizationId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>ASR 的定制语言模型 ID</p></div></td><td><p>cd97223f-42f2-4cd9-95af-e734e2fe1fe4</p></td></tr><tr><td>SpeechNoiseThreshold</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>噪音参数阈值，参数范围：[-100,100]。取值说明如下：</p><p>取值越趋于-100，噪音被判定为语音的概率越大。</p><p>取值越趋于+100，语音被判定为噪音的概率越大。</p></div></td><td><p>0</p></td></tr><tr><td>Model</td><td><p>string</p></td><td><p>否</p></td><td><div><p>ASR 模型</p></div><div><p><strong>枚举值：</strong></p><ul><li>fun-asr-flash-8k-realtime :<div><p>fun-asr-flash-8k-realtime</p></div></li><li>fun-asr-realtime-2026-02-28 :<div><p>fun-asr-realtime-2026-02-28</p></div></li><li>paraformer-realtime-v2 :<div><p>paraformer-realtime-v2</p></div></li><li>paraformer-realtime-8k-v2 :<div><p>paraformer-realtime-8k-v2</p></div></li></ul></div></td><td><p>fun-asr-flash-8k-realtime</p></td></tr><tr><td>CorrectionRules</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>SynthesizerConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>TTS 语音配置</p></div></td><td></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>TTS 访问方式</p></div></td><td><p>MANAGED</p></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><p>否</p></td><td><div><p>TTS 引擎类型</p></div></td><td><p>ALIYUN</p></td></tr><tr><td>Voice</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发音人</p></div></td><td><p>aiqi</p></td></tr><tr><td>SpeechRate</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>播报速度</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>-156</p></td></tr><tr><td>Volume</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>音量</p></div></td><td><p>50</p></td></tr><tr><td>PitchRate</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>语调</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>50</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>PronRules</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>ScriptProfile</td><td><p>object</p></td><td><p>否</p></td><td><div><p>模型</p></div></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td><p>否</p></td><td><div><p>LLM 模型 ID</p></div></td><td><p>qwen-plus</p></td></tr><tr><td>AgentProfile</td><td><p>object</p></td><td><p>否</p></td><td><div><p>智能体配置信息</p></div></td><td></td></tr><tr><td>ScriptProfileTemplateId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>智能体配置模版 ID</p></div></td><td><p>SFM_PROMPTS_DEFAULT</p></td></tr><tr><td>PromptsJson</td><td><p>string</p></td><td><p>否</p></td><td><div><p>提示词 json</p></div></td><td><p>{&quot;prompts&quot;:&quot;我是一个语音聊天机器人。&quot;}</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>智能体名称</p></div></td><td><p>语音机器人小云</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><p>否</p></td><td><div><p>智能体描述</p></div></td><td><p>语音机器人小云</p></td></tr><tr><td>InteractionConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>交互配置</p></div></td><td></td></tr><tr><td>SilenceDetectionConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>静默检测配置</p></div></td><td></td></tr><tr><td>Timeout</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>超时时长（毫秒）</p></div></td><td><p>5000</p></td></tr><tr><td>RagConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>RAG 配置</p></div></td><td></td></tr><tr><td>RagEngine</td><td><p>string</p></td><td><p>否</p></td><td><div><p>RAG 引擎</p></div></td><td><p>BAILIAN</p></td></tr><tr><td>Enabled</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否启用 RAG</p></div></td><td><p>false</p></td></tr><tr><td>KnowledgeBaseIds</td><td><p>array</p></td><td><p>否</p></td><td><div><p>知识库 ID 列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>知识库 ID</p></div></td><td><p>3457xghryt</p></td></tr><tr><td>TopN</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>取最大多少条数据</p></div></td><td><p>5</p></td></tr><tr><td>MaxContentLength</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>RAG 内容最大拼接长度</p></div></td><td><p>2000</p></td></tr><tr><td>ToolConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>工具配置</p></div></td><td></td></tr><tr><td>McpServers</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>MCP 信息配置列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>名称</p></div></td><td><p>phone-ai-call</p></td></tr><tr><td>BaseUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>基础 URL</p></div></td><td><p><a href="https://example.com">https://example.com</a></p></td></tr><tr><td>SseEndpoint</td><td><p>string</p></td><td><p>否</p></td><td><div><p>SSE 路径</p></div></td><td><p>/phone-ai-call/mcp/sse?key=value</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object |  |  |
| Code | string | 接口状态码 | OK |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 返回提示信息 | success |
| RequestId | string | 请求 ID | CF6D3484-19A1-5C77-863B-AC8B5754D37C |
| Data | string | 返回结果（VersionId） | 20904943-f711-494f-9f1f-e7f340f37707 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```json
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "CF6D3484-19A1-5C77-863B-AC8B5754D37C",
  "Data": "20904943-f711-494f-9f1f-e7f340f37707"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | Parameter.Enumeration | The parameter %s must be one of the value of enumeration %s. |  |
| 400 | Parameter.Blank | The parameter %s must not be null or empty. |  |
| 400 | Parameter.Empty | The parameter %s may not be null or empty. |  |
| 400 | Parameter.Null | The parameter %s may not be null. |  |
| 403 | Permission.Unauthorized | You are not authorized to perform this action. %s privileges are required. |  |
| 404 | NotExists.InstanceId | The specified instance %s does not exist. |  |

访问[错误中心](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion#workbench-doc-change-demo)。
