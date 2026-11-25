# GetApplication

获取语音机器人应用。

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
| bailianvoicebot:GetApplication | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| BusinessUnitId | string | 是 | 百炼业务空间 ID | llm-c11iig67g863rih8 |
| ApplicationId | string | 是 | 应用 ID。 | a395011f-a247-400f-bc69-28796749fd52 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>code 码</p></div></td><td><p>OK</p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>响应信息</p></div></td><td><p>success</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID</p></div></td><td><p>D771A1B6-3D5F-174A-BEE1-98CE1000D337</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>返回数据</p></div></td><td></td></tr><tr><td>ApplicationId</td><td><p>string</p></td><td><div><p>应用 ID</p></div></td><td><p>a395011f-a247-400f-bc69-28796749fd52</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>应用名称</p></div></td><td><p>测试001</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>应用描述</p></div></td><td><p>描述一下这个应用</p></td></tr><tr><td>Concurrency</td><td><p>integer</p></td><td><div><p>呼叫并发量，即同时在外呼的通话数量。</p></div></td><td><p>10</p></td></tr><tr><td>CreatedTime</td><td><p>integer</p></td><td><div><p>应用创建时间。</p></div></td><td><p>1730081561000</p></td></tr><tr><td>UpdatedTime</td><td><p>integer</p></td><td><div><p>应用修改的时间。</p></div></td><td><p>1730081561000</p></td></tr><tr><td>NluEngine</td><td><p>string</p></td><td><div><p>Nlu 引擎</p></div></td><td><p>PROMPTS</p></td></tr><tr><td>NluAccessType</td><td><p>string</p></td><td><div><p>Nlu 访问方式</p></div></td><td><p>MANAGED</p></td></tr><tr><td>DraftVersion</td><td><p>object</p></td><td><div><p>编辑版配置内容</p></div></td><td></td></tr><tr><td>VersionId</td><td><p>string</p></td><td><div><p>版本 ID</p></div></td><td><p>743219815472857088</p></td></tr><tr><td>TranscriberConfig</td><td><p>object</p></td><td><div><p>ASR 配置</p></div></td><td></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><div><p>ASR 引擎</p></div><div><p><strong>枚举值：</strong></p><ul><li>ALIYUN :<div><p>ALIYUN</p></div></li></ul></div></td><td><p>ALIYUN</p></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><div><p>ASR 调用方式</p></div><div><p><strong>枚举值：</strong></p><ul><li>MANAGED :<div><p>MANAGED</p></div></li></ul></div></td><td><p>MANAGED</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>VocabularyId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>EndSilenceTimeout</td><td><p>integer</p></td><td></td><td></td></tr><tr><td>CustomizationId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>SpeechNoiseThreshold</td><td><p>integer</p></td><td></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td></td><td></td></tr><tr><td>CorrectionRules</td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td></td><td></td></tr><tr><td>SynthesizerConfig</td><td><p>object</p></td><td><div><p>TTS 配置</p></div></td><td></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><div><p>TTS 引擎</p></div><div><p><strong>枚举值：</strong></p><ul><li>ALIYUN :<div><p>ALIYUN</p></div></li></ul></div></td><td><p>ALIYUN</p></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><div><p>TTS 调用方式</p></div><div><p><strong>枚举值：</strong></p><ul><li>MANAGED :<div><p>MANAGED</p></div></li></ul></div></td><td><p>MANAGED</p></td></tr><tr><td>Voice</td><td><p>string</p></td><td><div><p>发音人</p></div></td><td><p>aixia</p></td></tr><tr><td>SpeechRate</td><td><p>integer</p></td><td><div><p>播报速度</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>1</p></td></tr><tr><td>Volume</td><td><p>integer</p></td><td><div><p>音量</p></div></td><td><p>50</p></td></tr><tr><td>PitchRate</td><td><p>integer</p></td><td><div><p>音调</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>5</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td></td><td></td></tr><tr><td>PronRules</td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td></td><td></td></tr><tr><td>ScriptProfile</td><td><p>object</p></td><td><div><p>应用模型配置</p></div></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td><div><p>模型</p></div></td><td><p>qwen-plus</p></td></tr><tr><td>Temperature</td><td><p>string</p></td><td><div><p>生成过程中的核采样方法概率阈值</p><div><ul><li><p>例如，取值为 0.8 时，仅保留概率加起来大于等于 0.8 的最可能 token 的最小集合作为候选集。 * 取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高</p></li></ul></div></div></td><td><p>0.8</p></td></tr><tr><td>TopP</td><td><p>string</p></td><td><div><p>用于控制模型回复的随机性和多样性</p><div><ul><li><p>具体来说，temperature 值控制了生成文本时对每个候选词的概率分布进行平滑的程度。 较高的 temperature 值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的 temperature 值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。</p></li><li><p>取值范围： [0, 2)，不建议取值为 0，无意义。</p></li></ul></div></div></td><td><p>0.1</p></td></tr><tr><td>AgentProfile</td><td><p>object</p></td><td><div><p>智能体配置信息</p></div></td><td></td></tr><tr><td>ScriptProfileTemplateId</td><td><p>string</p></td><td><div><p>应用模版 ID</p></div></td><td><p>SFM_PROMPTS_DEFAULT</p></td></tr><tr><td>AgentProfileId</td><td><p>string</p></td><td><div><p>智能体配置 ID。</p></div></td><td><p>6a50b67072d44788951de29758432d94</p></td></tr><tr><td>PromptsJson</td><td><p>string</p></td><td><div><p>提示词 json</p></div></td><td><p>{&quot;prompts&quot;:&quot;我是一个聊天机器人。&quot;}</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>智能体描述</p></div></td><td><p>聊天机器人</p></td></tr><tr><td>InteractionConfig</td><td><p>object</p></td><td><div><p>交互配置</p></div></td><td></td></tr><tr><td>SilenceDetectionConfig</td><td><p>object</p></td><td><div><p>静默检测配置</p></div></td><td></td></tr><tr><td>Timeout</td><td><p>integer</p></td><td><div><p>任务执行超时时间，单位秒。</p></div></td><td><p>3</p></td></tr><tr><td>RagConfig</td><td><p>object</p></td><td><div><p>RAG 配置</p></div></td><td></td></tr><tr><td>RagEngine</td><td><p>string</p></td><td><div><p>RAG 引擎</p></div></td><td><p>BAILIAN</p></td></tr><tr><td>Enabled</td><td><p>boolean</p></td><td><div><p>是否启用 RAG</p></div></td><td><p>false</p></td></tr><tr><td>KnowledgeBaseIds</td><td><p>array</p></td><td><div><p>知识库 ID 列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>知识库 ID</p></div></td><td><p>8345xghryt</p></td></tr><tr><td>TopN</td><td><p>integer</p></td><td><div><p>取最大多少条数据</p></div></td><td><p>5</p></td></tr><tr><td>MaxContentLength</td><td><p>integer</p></td><td><div><p>RAG 内容最大拼接长度</p></div></td><td><p>2000</p></td></tr><tr><td>ToolConfig</td><td><p>object</p></td><td><div><p>工具配置</p></div></td><td></td></tr><tr><td>McpServers</td><td><p>array&lt;object&gt;</p></td><td><div><p>MCP 信息配置列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>名称</p></div></td><td><p>phone-ai-call</p></td></tr><tr><td>BaseUrl</td><td><p>string</p></td><td><div><p>基础 URL</p></div></td><td><p><a href="https://example.com">https://example.com</a></p></td></tr><tr><td>SseEndpoint</td><td><p>string</p></td><td><div><p>SSE 路径</p></div></td><td><p>/phone-ai-call/mcp/sse?key=value</p></td></tr><tr><td>PublishedVersion</td><td><p>object</p></td><td><div><p>已发布应用版本</p></div></td><td></td></tr><tr><td>VersionId</td><td><p>string</p></td><td><div><p>版本 ID</p></div></td><td><p>47889c1f-dd3f-4ace-9587-a13a3563e678</p></td></tr><tr><td>TranscriberConfig</td><td><p>object</p></td><td><div><p>ASR 配置</p></div></td><td></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><div><p>ASR 引擎</p></div><div><p><strong>枚举值：</strong></p><ul><li>ALIYUN :<div><p>ALIYUN</p></div></li></ul></div></td><td><p>ALIYUN</p></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><div><p>ASR 调用方式</p></div><div><p><strong>枚举值：</strong></p><ul><li>MANAGED :<div><p>MANAGED</p></div></li></ul></div></td><td><p>MANAGED</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>VocabularyId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>EndSilenceTimeout</td><td><p>integer</p></td><td></td><td></td></tr><tr><td>CustomizationId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>SpeechNoiseThreshold</td><td><p>integer</p></td><td></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td></td><td></td></tr><tr><td>CorrectionRules</td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td></td><td></td></tr><tr><td>SynthesizerConfig</td><td><p>object</p></td><td><div><p>TTS 配置</p></div></td><td></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><div><p>TTS 引擎</p></div><div><p><strong>枚举值：</strong></p><ul><li>ALIYUN :<div><p>ALIYUN</p></div></li></ul></div></td><td><p>ALIYUN</p></td></tr><tr><td>NlsAccessType</td><td><p>string</p></td><td><div><p>TTS 调用方式</p></div><div><p><strong>枚举值：</strong></p><ul><li>MANAGED :<div><p>MANAGED</p></div></li></ul></div></td><td><p>MANAGED</p></td></tr><tr><td>Voice</td><td><p>string</p></td><td><div><p>发音人</p></div></td><td><p>aixia</p></td></tr><tr><td>SpeechRate</td><td><p>integer</p></td><td><div><p>播报速度</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>-20</p></td></tr><tr><td>Volume</td><td><p>integer</p></td><td><div><p>音量</p></div></td><td><p>50</p></td></tr><tr><td>PitchRate</td><td><p>integer</p></td><td><div><p>音调</p><div><p>取值范围：-500~500。</p></div></div></td><td><p>3</p></td></tr><tr><td>NlsAccessProfile</td><td><p>object</p></td><td></td><td></td></tr><tr><td>AccessProfileId</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td></td><td></td></tr><tr><td>PronRules</td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Pattern</td><td><p>string</p></td><td></td><td></td></tr><tr><td>Replacement</td><td><p>string</p></td><td></td><td></td></tr><tr><td>ScriptProfile</td><td><p>object</p></td><td><div><p>应用模型配置</p></div></td><td></td></tr><tr><td>Model</td><td><p>string</p></td><td><div><p>模型</p></div></td><td><p>qwen-plus</p></td></tr><tr><td>Temperature</td><td><p>string</p></td><td><div><p>生成过程中的核采样方法概率阈值</p><div><ul><li><p>例如，取值为 0.8 时，仅保留概率加起来大于等于 0.8 的最可能 token 的最小集合作为候选集。 * 取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高</p></li></ul></div></div></td><td><p>0.8</p></td></tr><tr><td>TopP</td><td><p>string</p></td><td><div><p>用于控制模型回复的随机性和多样性</p><div><ul><li><p>具体来说，temperature 值控制了生成文本时对每个候选词的概率分布进行平滑的程度。 较高的 temperature 值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的 temperature 值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。</p></li><li><p>取值范围： [0, 2)，不建议取值为 0，无意义。</p></li></ul></div></div></td><td><p>0.1</p></td></tr><tr><td>AgentProfile</td><td><p>object</p></td><td><div><p>智能体配置信息</p></div></td><td></td></tr><tr><td>ScriptProfileTemplateId</td><td><p>string</p></td><td><div><p>智能体配置模版 ID</p></div></td><td><p>SFM_PROMPTS_DEFAULT</p></td></tr><tr><td>AgentProfileId</td><td><p>string</p></td><td><div><p>智能体配置 ID</p></div></td><td><p>b97b6822dd624c32b6c2a54d717db718</p></td></tr><tr><td>PromptsJson</td><td><p>string</p></td><td><div><p>提示词 json</p></div></td><td><p>{&quot;prompts&quot;:&quot;我是一个聊天机器人。&quot;}</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>智能体描述</p></div></td><td><p>我是一个聊天机器人</p></td></tr><tr><td>InteractionConfig</td><td><p>object</p></td><td><div><p>交互配置</p></div></td><td></td></tr><tr><td>SilenceDetectionConfig</td><td><p>object</p></td><td><div><p>静默检测配置</p></div></td><td></td></tr><tr><td>Timeout</td><td><p>integer</p></td><td><div><p>超时时长。</p></div></td><td><p>30</p></td></tr><tr><td>RagConfig</td><td><p>object</p></td><td><div><p>RAG 配置</p></div></td><td></td></tr><tr><td>RagEngine</td><td><p>string</p></td><td><div><p>RAG 引擎</p></div></td><td><p>BAILIAN</p></td></tr><tr><td>Enabled</td><td><p>boolean</p></td><td><div><p>是否启用 RAG</p></div></td><td><p>false</p></td></tr><tr><td>KnowledgeBaseIds</td><td><p>array</p></td><td><div><p>知识库 ID 列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>知识库 ID</p></div></td><td><p>3472xghryt</p></td></tr><tr><td>TopN</td><td><p>integer</p></td><td><div><p>取最大多少条数据</p></div></td><td><p>5</p></td></tr><tr><td>MaxContentLength</td><td><p>integer</p></td><td><div><p>RAG 内容最大拼接长度</p></div></td><td><p>2000</p></td></tr><tr><td>ToolConfig</td><td><p>object</p></td><td><div><p>工具配置</p></div></td><td></td></tr><tr><td>McpServers</td><td><p>array&lt;object&gt;</p></td><td><div><p>MCP 信息配置列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>名称。</p></div></td><td><p>phone-ai-call</p></td></tr><tr><td>BaseUrl</td><td><p>string</p></td><td><div><p>基础 URL</p></div></td><td><p><a href="https://example.com">https://example.com</a></p></td></tr><tr><td>SseEndpoint</td><td><p>string</p></td><td><div><p>SSE 路径</p></div></td><td><p>/phone-ai-call/mcp/sse?key=value</p></td></tr></tbody></table>

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
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "ApplicationId": "a395011f-a247-400f-bc69-28796749fd52\n",
    "Name": "测试001\n",
    "Description": "描述一下这个应用\n",
    "Concurrency": 10,
    "CreatedTime": 1730081561000,
    "UpdatedTime": 1730081561000,
    "NluEngine": "PROMPTS",
    "NluAccessType": "MANAGED",
    "DraftVersion": {
      "VersionId": "743219815472857088",
      "TranscriberConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "VocabularyId": "",
        "EndSilenceTimeout": 0,
        "CustomizationId": "",
        "SpeechNoiseThreshold": 0,
        "Model": "",
        "CorrectionRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "SynthesizerConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "Voice": "aixia",
        "SpeechRate": 1,
        "Volume": 50,
        "PitchRate": 5,
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "Model": "",
        "PronRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "ScriptProfile": {
        "Model": "qwen-plus",
        "Temperature": "0.8",
        "TopP": "0.1",
        "AgentProfile": {
          "ScriptProfileTemplateId": "SFM_PROMPTS_DEFAULT",
          "AgentProfileId": "6a50b67072d44788951de29758432d94",
          "PromptsJson": "{\"prompts\":\"我是一个聊天机器人。\"}",
          "Description": "聊天机器人"
        }
      },
      "InteractionConfig": {
        "SilenceDetectionConfig": {
          "Timeout": 3
        }
      },
      "RagConfig": {
        "RagEngine": "BAILIAN",
        "Enabled": false,
        "KnowledgeBaseIds": [
          "8345xghryt"
        ],
        "TopN": 5,
        "MaxContentLength": 2000
      },
      "ToolConfig": {
        "McpServers": [
          {
            "Name": "phone-ai-call",
            "BaseUrl": "https://example.com",
            "SseEndpoint": "/phone-ai-call/mcp/sse?key=value"
          }
        ]
      }
    },
    "PublishedVersion": {
      "VersionId": "47889c1f-dd3f-4ace-9587-a13a3563e678",
      "TranscriberConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "VocabularyId": "",
        "EndSilenceTimeout": 0,
        "CustomizationId": "",
        "SpeechNoiseThreshold": 0,
        "Model": "",
        "CorrectionRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "SynthesizerConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "Voice": "aixia",
        "SpeechRate": -20,
        "Volume": 50,
        "PitchRate": 3,
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "Model": "",
        "PronRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "ScriptProfile": {
        "Model": "qwen-plus\n",
        "Temperature": "0.8",
        "TopP": "0.1",
        "AgentProfile": {
          "ScriptProfileTemplateId": "SFM_PROMPTS_DEFAULT",
          "AgentProfileId": "b97b6822dd624c32b6c2a54d717db718",
          "PromptsJson": "{\"prompts\":\"我是一个聊天机器人。\"}\n",
          "Description": "我是一个聊天机器人"
        }
      },
      "InteractionConfig": {
        "SilenceDetectionConfig": {
          "Timeout": 30
        }
      },
      "RagConfig": {
        "RagEngine": "BAILIAN",
        "Enabled": false,
        "KnowledgeBaseIds": [
          "3472xghryt"
        ],
        "TopN": 5,
        "MaxContentLength": 2000
      },
      "ToolConfig": {
        "McpServers": [
          {
            "Name": "phone-ai-call",
            "BaseUrl": "https://example.com",
            "SseEndpoint": "/phone-ai-call/mcp/sse?key=value"
          }
        ]
      }
    }
  }
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

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication#workbench-doc-change-demo)。
