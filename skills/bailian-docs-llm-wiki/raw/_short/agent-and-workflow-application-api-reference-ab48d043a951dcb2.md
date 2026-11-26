# 工作流与旧版智能体应用 API

本文介绍 DashScope API 调用阿里云百炼应用（ 智能体 、 工作流 ）的输入与输出参数，并提供典型场景下的调用示例。

> **重要**
>
> 本文档仅适用于华北2（北京）地域。

**相关指南**

-   请参阅[调用智能体应用](call-single-agent-application-7bb88312c0915edf.md)、[调用工作流应用](../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md)。
-   如需通过 Responses API 调用，请参阅 [Responses API](../application-api-reference/flow-agent-api/application-call/openai-responses-api.md)。

<a id="前置准备"></a>

<a id="e846d6db23z61"></a>

## 前置准备

开始前，请确保您已完成以下操作：

1.  **创建应用：**前往[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)创建阿里云[百炼应用](../application-user-guide/agent-development/llm-application/llm-application-start-using/flow-agent-introduction.md)并获取应用 ID；
2.  **获取 API Key：**通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **安装SDK（可选）：**若使用 SDK 调用，请安装相应语言的[DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="调用方式"></a>

<a id="6c6a50b025gbh"></a>

## 调用方式

-   **HTTP 接口调用**
    
    请求地址：`POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion`
    
    > 其中 `APP_ID` 需替换为您的实际应用 ID
    
-   **SDK 调用**
    
    Python/Java SDK：本文已默认配置正确的 endpoint
    
    自定义 endpoint：可通过 base\_url 参数配置
    

**在线调试**：通过**应用卡片 -> 发布 -> API 调试**路径进入调试页面后，填写参数并点击运行即可。

<table><tbody><tr><td><a id="989b585548qnj"></a><h3>请求体</h3><p><strong>app_id</strong><code>string</code><strong>（必选）</strong></p><p>应用标识。</p><p>可在<a href="https://bailian.console.aliyun.com/#/app-center">应用管理</a>页面的应用卡片上获取应用 ID。</p><blockquote><p>Java SDK中为 <strong>appId。</strong>通过 HTTP 调用时，请将实际的应用 ID 放入 <strong>URL</strong>中，替换<code>APP_ID</code>。</p></blockquote><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>用户的输入指令，用于指导应用生成回复。</p><blockquote><p>通过 HTTP 调用时，请将 <strong>prompt</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>session_id</strong><code>string</code> （可选）</p><p>历史对话标识。</p><p>传入<code>session_id</code>时，请求将自动携带云端存储的对话历史。此时必须传递<code>prompt</code>。</p><p>该 ID 在连续 1 小时内无任何请求后将自动失效。</p><blockquote><p>Java SDK 中为 <strong>setSessionId</strong>。通过 HTTP 调用时，请将 <strong>session_id</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>messages</strong><code>array</code>（可选）</p><p>传递给大模型的上下文，按对话顺序排列。</p><p>当使用<code>messages</code>参数实现多轮对话时，无需传递<code>prompt</code>和 <code>session_id</code>。</p><p>若同时传入<code>session_id</code>和<code>messages</code>，则大模型优先使用<code>messages</code>中的内容，忽略<code>session_id</code>和<code>prompt</code>。</p><blockquote><p>通过HTTP调用时，请将 <strong>messages</strong> 放入 <strong>input</strong> 对象中。</p></blockquote><blockquote><p>使用该参数，Python Dashscope SDK的版本至少应为2.0.1，Java Dashscope SDK的版本至少应为2.17.0。</p></blockquote><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为<code>system</code>。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>消息内容。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>输入的文本。</p></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section><p>Assistant Message<code>object</code>（可选）</p><p>模型的回复。通常用于在多轮对话中作为上下文回传给模型。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>模型回复的文本内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>助手消息的角色，固定为<code>assistant</code>。</p></div></section></div></section><p><strong>workspace</strong> <code>string</code> （可选）</p><p>业务空间标识。相关文档：<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h">获取Workspace ID</a>。</p><p>仅调用<a href="https://help.aliyun.com/zh/model-studio/use-workspace">子业务空间</a>的应用时需传递<code>workspace ID</code>。</p><blockquote><p>通过 HTTP 调用时，请指定Header中的 <strong>X-DashScope-WorkSpace</strong>。</p></blockquote><p><strong>stream</strong> <code>boolean</code>（可选） 默认值为 <code>False</code></p><p>是否以流式输出方式回复。</p><p>推荐设置为<code>True</code>，可提升阅读体验并降低超时风险。</p><p>参数值：</p><ul><li><code>False</code>（默认）：模型生成全部内容后一次性返回；</li><li><code>True</code>（推荐）：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。</li></ul><blockquote><p>通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote><p><strong>incremental_output</strong> <code>boolean</code>（可选）默认值为 <code>False</code></p><p>在流式输出模式下是否开启增量输出。</p><p>推荐设置为<code>True</code>，可提升阅读体验。</p><p>参数值：</p><ul><li><code>False</code>（默认）：每次输出当前已经生成的整个序列，最后一次输出为生成的完整结果。</li></ul><a id="code-block"></a><pre class="language-text"><code>I
I like
I like apple
I like apple.
</code></pre><ul><li><code>True</code>（推荐）：增量输出，即后续输出内容不包含已输出的内容。需要实时地逐个读取这些片段以获得完整的结果。</li></ul><a id="code-block-2"></a><pre class="language-text"><code>I
like
apple
.
</code></pre><blockquote><p>Java SDK中为<strong>incrementalOutput</strong>*。*通过HTTP调用时，请将<strong>incremental_output</strong>放入<strong>parameters</strong>对象中。</p></blockquote><p><strong>flow_stream_mode</strong> <code>string</code>（可选）默认值为<code>full_thoughts</code></p><p><strong>工作流应用</strong>的流式输出模式。相关文档：<a href="../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md#b3be03a1ff21e">流式输出</a>。</p><p>参数值：</p><ul><li><p><code>message_format_plus</code><strong>（推荐）</strong>：消息增强模式。</p><p>在<code>workflow_message</code>字段输出所有节点的执行过程和结果，覆盖所有节点类型。与<code>message_format</code>返回相同的数据结构，但支持全部节点类型的流式推送。</p><div><div><p><strong>重要</strong>客户端处理规则：文本类节点（OUTPUT / END text 模式）的<code>message.content</code>为增量 delta，需追加拼接；JSON 类节点（LLM / Component / AgentGroup 等）的<code>message.content</code>为完整 JSON 快照，需整体替换。当<code>node_is_completed=true</code>时标记该节点执行完毕。</p></div></div><p><strong>子画布节点推流</strong>：循环节点和批处理节点的子画布内节点也会流式推送，通过响应字段<code>parent_node_id</code>标识所属父节点。</p><div><div><p><strong>重要</strong>暂不支持嵌套子画布：循环/批处理节点的子画布内不能再放置循环或批处理节点。</p></div></div><blockquote><p>Java SDK 中为<code>FlowStreamMode.MESSAGE_FORMAT_PLUS</code>。</p></blockquote></li><li><p><code>message_format</code><strong>（推荐）</strong>：消息模式。</p><p>在<code>message</code>字段输出指定节点（<strong>流程输出</strong>节点或<strong>结束</strong>节点）的结果。</p><div><div><p><strong>重要</strong>在控制台应用中开启目标节点的<strong>流式输出</strong>开关，即可流式返回结果；未开启时，一次性返回该节点的最终结果。</p></div></div><blockquote><p>Java SDK 中为<code>FlowStreamMode.MESSAGE_FORMAT</code>。</p></blockquote></li><li><p><code>full_thoughts</code>（默认）：完整思考模式。</p><div><div><p><strong>说明</strong><strong>不推荐新业务使用</strong>。建议改用<code>message_format</code>或<code>message_format_plus</code>。</p></div></div><p>在<code>thoughts</code>字段输出所有节点的结果。</p><div><div><p><strong>重要</strong>使用此模式时，必须同时将 <code>has_thoughts</code> 参数设置为 <code>True</code>。</p></div></div><blockquote><p>Java SDK 中为<code>FlowStreamMode.FULL_THOUGHTS</code>。</p></blockquote></li></ul><blockquote><p>Python SDK 版本至少为2.0.1，Java SDK 版本至少为2.22.23。通过HTTP调用时，请将<strong>flow_stream_mode</strong>放入<strong>parameters</strong>对象中。</p></blockquote><p><strong>biz_params</strong><code>object</code> （可选）</p><p>应用通过自定义变量、节点或插件传递参数时，使用该字段进行传递。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#b774db7cdc0aa">调用智能体应用-传递自定义参数</a>，<a href="../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md#6e644d5a7b3ia">调用工作流应用-传递自定义参数</a>。</p><blockquote><p>Java SDK 中为 <strong>bizParams</strong>。通过HTTP调用时，请将 <strong>biz_params</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>工作流应用</strong>开始节点的自定义变量直接传递，示例：</p><a id="code-block-3"></a><pre class="language-python"><code>biz_params = {&quot;city&quot;: &quot;杭州&quot;}
</code></pre><p><strong>智能体应用</strong>通过以下字段传递提示词变量或插件变量参数：</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>user_prompt_params</strong> <code>object</code> （可选）</p><p>表示自定义提示词变量参数信息。</p><p>一个应用内的变量名不可重复，且上限 10 个。</p><p>使用步骤：</p><ol><li>在应用内<a href="../application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md#ddecb789a81hy">配置自定义变量并在提示词中引用</a>，然后<strong>发布</strong>应用。</li><li>API调用通过此参数传递变量信息。</li></ol><p>示例：</p><a id="code-block-4"></a><pre class="language-python"><code>biz_params ={
    &quot;user_prompt_params&quot;: {
        &quot;date&quot;: &quot;2025年03月03日&quot;,
        &quot;city&quot;: &quot;杭州&quot;
    }
}
</code></pre><p><strong>user_defined_params</strong> <code>object</code> （可选）</p><p>表示自定义插件参数信息。</p><p>一个应用内添加的插件不可重复，且上限 10 个。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>tool_id</strong><code>string</code> （可选）</p><p>插件 ID，可在插件卡片上获取。</p><p><strong>${plugin_params}</strong><code>string</code>（可选）</p><p>对象最内侧包含的多个键值对。每个键值对表示用户自定义的待传递参数名及其指定值。如：</p><a id="code-block-5"></a><pre class="language-json"><code>&quot;article_index&quot;: 2
</code></pre></div></section><p>使用步骤：</p><ol><li>在应用内关联指定插件，并<strong>发布</strong>应用。</li><li>API调用通过此参数传递插件信息。</li></ol><p>可提供多个键值对，其中每个键为插件的 <code>TOOL_ID</code>，值为该插件所需的参数对象。示例：</p><a id="code-block-6"></a><pre class="language-text"><code>&quot;user_defined_params&quot;: {
        &quot;&lt;TOOL_ID&gt;&quot;: {
            &quot;article_index&quot;: 2},
        &quot;&lt;TOOL_ID&gt;&quot;: {
            &quot;article_index&quot;: 8}
        }
</code></pre><p><strong>user_defined_tokens</strong> <code>object</code>（可选）</p><p>表示自定义插件的用户级鉴权信息。</p><p>一个应用内添加的插件不可重复，且上限 10 个。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>tool_id</strong><code>string</code> （可选）</p><p>插件 ID，可在插件卡片中获取。通过<code>&lt;TOOL_ID&gt;</code>字段传递。</p><p><strong>user_token</strong> <code>string</code> （可选）</p><p>传递该插件需要的用户鉴权信息，如实际<code>DASHSCOPE_API_KEY</code>的值。</p></div></section><p>使用步骤：</p><ol><li>在应用内关联指定插件，并<strong>发布</strong>应用。</li><li>API调用通过此参数传递插件用户级鉴权信息。</li></ol><p>可提供多个键值对，其中每个键为插件的 <code>TOOL_ID</code>，值为<code>user_token</code> 对象。</p></div></section><p><strong>memory_id</strong> <code>string</code> （可选）</p><p>长期记忆体 ID，参阅<a href="api-bailian-2023-12-29-creatememory-71d9eb60188e5ed4.md">CreateMemory</a>创建。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#de63036b85aj0">长期记忆</a>。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><ol><li>在应用中打开<strong>长期记忆</strong>开关，并<strong>发布</strong>应用。</li><li>通过指定 <code>memory_id</code> 调用应用时，系统依据用户偏好信息自动构建和保存长期记忆。</li><li>后续使用同一 <code>memory_id</code> 调用时，系统会恢复这些长期记忆，并与最新的用户消息合并提供给模型处理。</li></ol><blockquote><p>Java SDK 中为 <strong>memoryId</strong>。通过 HTTP 调用时，请将 <strong>memory_id</strong> 放入<strong>input</strong>对象中。</p></blockquote><p><strong>has_thoughts</strong> <code>boolean</code> （可选）默认值为 <code>False</code></p><p>是否输出插件调用、知识检索的过程，或已开启思考模式的模型思考过程，在<code>thoughts</code>字段中查看。</p><p>参数值：</p><ul><li>True：输出。</li><li>False（默认）：不输出。</li></ul><blockquote><p>Java SDK 中为 <strong>hasThoughts</strong>。通过 HTTP 调用时，请将 <strong>has_thoughts</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><p><strong>image_list</strong> <code>array</code>（可选）</p><p>图片列表。支持图像 URL 和 Data URL（Base64 编码）。应用内需选择<a href="../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a>模型。</p><p><code>base64</code>编码格式可构建为 <a href="https://www.rfc-editor.org/rfc/rfc2397">Data URL</a>：<code>data:[MIME_type];base64,{base64_image}</code>。详细说明和代码示例见本文档右侧<a href="agent-and-workflow-application-api-reference-ab48d043a951dcb2.md">视觉理解</a>章节。</p><p>使用场景：</p><ul><li>图片检索（<strong>智能体应用</strong>）：根据上传的图片链接，检索包含图片链接的结构化知识库。</li><li>视觉理解：通过<strong>千问VL系列模型</strong>的视觉理解能力，分析图像内容实现问答。</li></ul><p>相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#30619780ddy93">上传文件（文档、图片、视频或音频）</a>。</p><blockquote><p>Java SDK 中为 <strong>images</strong>。通过 HTTP 调用时，请将 <strong>image_list</strong>放入 <strong>input</strong>对象中。</p></blockquote><p><strong>file_list</strong> <code>array</code>（可选）</p><p>包含一个或多个文件 URL 的列表。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#30619780ddy93">上传文件（文档、图片、视频或音频）</a>。</p><blockquote><p>Java SDK中为 <strong>files</strong>。通过HTTP调用时，请将 <strong>file_list</strong>放入 <strong>input</strong>对象中。</p></blockquote><blockquote><p>Python Dashscope SDK 的版本至少应为2.0.1，Java Dashscope SDK的版本至少应为2.21.13。</p></blockquote><p><strong>rag_options</strong> <code>object</code> （可选）</p><p>用于配置与检索相关的参数。包括但不限于对指定的知识库或文档进行检索。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#bb173820c5whx">检索知识库</a>。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><blockquote><p>Java SDK 中为 <strong>ragOptions</strong>。通过HTTP调用时，请将 <strong>rag_options</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>pipeline_ids</strong> <code>array</code>（<strong>必选）</strong></p><p>包含一个或多个知识库 ID 的列表。上限5个。</p><p>检索指定知识库内的所有文档。</p><p>获取方式：</p><ul><li><a href="https://bailian.console.aliyun.com/#/knowledge-base">知识库</a>页面获取知识库 ID；</li><li>或通过<a href="api-bailian-2023-12-29-createindex-8bc613c75f8af371.md">CreateIndex</a>接口（仅支持非结构化知识库）返回的<code>Data.Id</code>。</li></ul><blockquote><p>Java SDK 中为<strong>pipelineIds</strong>。</p></blockquote><p><strong>file_ids</strong><code>array</code>（可选）</p><p>包含一个或多个非结构化文档 ID 的列表。上限5个。</p><p>检索指定知识库内的非结构化文档。</p><p>传入文档 ID 时，必须同时在 <code>pipeline_ids</code> 字段中传入这些文档所属的知识库 ID。</p><p>获取方式：</p><ul><li>打开<a href="https://bailian.console.aliyun.com/cn-beijing/rag/connector/list"><strong>数据集</strong></a>，在目标文件数据集上单击<strong>详情</strong>。<br>从文档列表获取文档 ID。</li><li>或通过<a href="api-bailian-2023-12-29-addfile-8c254b3500bc50bc.md">AddFile</a>接口导入文档返回的 ID。</li></ul><blockquote><p>Java SDK 中为 <strong>fileIds</strong>。</p></blockquote><p><strong>metadata_filter</strong><code>object</code> （可选）</p><p>用于筛选非结构化文档的元数据。通过指定一个或多个键值对，检索指定知识库内具备该元数据的非结构化文档。</p><p>使用前提：</p><p>传入元数据时，必须同时在 <code>pipeline_ids</code> 字段中传入这些元数据所属的知识库 ID。</p><p>查看方式：</p><ul><li>访问<a href="https://bailian.console.aliyun.com/#/knowledge-base">知识库</a>页面，单击知识库卡片的<strong>查看详情Meta信息</strong>查看。</li><li>或通过<a href="api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md">ListChunks</a>接口获取。</li></ul><p>该对象由一个或多个键值对组成：</p><ul><li><p>键 (Key)：<code>String</code> 类型，代表元数据的名称。</p></li><li><p>值 (Value)：</p><ul><li><p>单一值匹配：值为一个 <code>String</code>，表示只检索该字段值完全等于此字符串的文档。</p><ul><li>示例: <code>&quot;author&quot;: &quot;John.Doe&quot;</code></li></ul></li><li><p>多值“或”匹配：值为一个 <code>Array</code> (数组) 或 <code>List</code> (列表)，包含多个 <code>String</code>。这表示检索该字段值匹配数组中任意一个值的文档（逻辑为 <code>OR</code>）。</p><ul><li>示例: <code>&quot;source&quot;: [&quot;internal_wiki&quot;, &quot;public_docs&quot;]</code></li></ul></li></ul></li></ul><p>组合逻辑：<br>不同键之间为“与”(AND) 逻辑。例如，<code>&quot;author&quot;: &quot;John.Doe&quot;, &quot;source&quot;: [&quot;internal_wiki&quot;, &quot;public_docs&quot;]</code> 表示筛选出作者是 &quot;John.Doe&quot; 并且来源是 &quot;internal_wiki&quot; 或 &quot;public_docs&quot; 的文档。<br></p><blockquote><p>Java SDK 中为 <strong>metadataFilter</strong>。</p></blockquote><p><strong>tags</strong> <code>array</code> （可选）</p><p>包含一个或多个非结构化文档标签的列表。</p><p>检索具备该标签的非结构化文档。</p><p>查看方式：</p><ul><li>打开<a href="https://bailian.console.aliyun.com/cn-beijing/rag/connector/list"><strong>数据集</strong></a>，在目标文件数据集上单击<strong>详情</strong>。<br>查看目标文档的标签。</li><li>或通过<a href="api-bailian-2023-12-29-describefile-020886c28a208bf2.md">DescribeFile</a>接口获取。</li></ul><p><strong>structured_filter</strong> <code>object</code> （可选）</p><p>用于对结构化数据进行元数据过滤。通过指定一个或多个键值对，可以筛选出符合条件的文档切片。</p><p>查看方式：</p><ul><li>可在<a href="https://bailian.console.aliyun.com/#/knowledge-base">知识库</a>页面，单击知识库卡片的<strong>查看详情查看索引</strong>查看。</li><li>或通过<a href="api-bailian-2023-12-29-listchunks-30a6c87b93a583c6.md">ListChunks</a>接口获取。</li></ul><p>该对象由一个或多个键值对组成：</p><blockquote><p>每个键（列名）都必须有对应的值，不支持仅通过列名筛选。</p></blockquote><ul><li><p>键 (Key)：必须是 <code>String</code> 类型，代表要筛选的元数据字段名（列名）。</p></li><li><p>值 (Value)：</p><ul><li>单一条件匹配：值为一个 <code>String</code> 或 <code>Number</code>，表示只检索该字段值完全匹配的文档。示例：<code>&quot;category&quot;: &quot;公司新闻&quot;</code>。</li><li>多值“或”匹配：值为一个 <code>Array</code> 或 <code>List</code>，包含多个 <code>String</code> 或 <code>Number</code>。这表示检索该字段值匹配数组中任意一个值的文档（逻辑为 <code>OR</code>）。示例：<code>&quot;year&quot;: 2024, &quot;department&quot;: [&quot;技术部&quot;, &quot;产品部&quot;]</code>。</li></ul></li></ul><p>组合逻辑：<br>不同键之间为“与”(AND) 逻辑。例如，<code>&quot;year&quot;: 2024, &quot;department&quot;: [&quot;技术部&quot;, &quot;产品部&quot;]</code> 表示筛选出年份是 2024 并且 部门是 &quot;技术部&quot; 或 &quot;产品部&quot; 的文档切片。<br></p><blockquote><p>Java SDK 中为 <strong>structuredFilter</strong>。</p></blockquote><p><strong>session_file_ids</strong><code>array</code>（可选）</p><p>包含一个或多个文件 ID 的列表。上限 10 个。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>在调用<strong>智能体应用</strong>时传递文件 ID，系统将提取文件中的<strong>文字内容</strong>，作为大模型问答的内容依据。</p><p>相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#30619780ddy93">上传文件（文档、图片、视频或音频）</a>。</p><div><div><p><strong>重要</strong>会话文件ID必须以“<code>file_session_</code>”开头，且文件状态为 FILE_IS_READY。否则调用失败。</p></div></div><blockquote><p>Java SDK 中为<strong>sessionFileIds</strong>。</p></blockquote><blockquote><p>Python Dashscope SDK 的版本至少应为2.0.1，Java Dashscope SDK 的版本至少应为2.17.0。</p></blockquote></div></section><p><strong>model_id</strong><code>string</code>（可选）</p><p>模型名称。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>API 调用时，可通过此参数传递本次调用使用的模型名称。</p><p>优先级：当通过 API 传递的<code>model_id</code>与控制台配置不同时，以 API 参数值为准。</p><blockquote><p>Java SDK 中为 <strong>modelId</strong>。通过HTTP调用时，请将 <strong>model_id</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK 的版本至少应为<strong>2.19.3</strong>。</p></blockquote><p><strong>enable_system_time</strong><code>boolean</code> （可选）默认值为 <code>True</code></p><p>控制模型是否自动获取当前时间（北京时间）。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>参数值：</p><ul><li>True（默认）：启用当前时间，模型可直接响应实时时间请求（如“今天日期”）。</li><li>False：禁用当前时间。需通过自定义变量手动传入时间。例如：</li></ul><a id="code-block-7"></a><pre class="language-python"><code># 通过 user_prompt_params 传递自定义时间
biz_params ={
    &quot;user_prompt_params&quot;: {
        &quot;date&quot;: &quot;2025年03月03日&quot;
    }
}
</code></pre><p>适用场景：</p><ul><li>需自定义时间来源，不依赖当前时间。</li><li>避免因当前时间变化导致模型输出结果变动。</li></ul><blockquote><p>Java SDK 中为 <strong>enableSystemTime</strong>。通过HTTP调用时，请将 <strong>enable_system_time</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK 的版本至少应为<strong>2.19.3</strong>。</p></blockquote><p><strong>enable_web_search</strong><code>boolean</code> （可选）默认值为 <code>false</code></p><p>模型在生成回复时是否使用互联网搜索结果进行参考。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>参数值：</p><ul><li><p>True：启用互联网搜索，模型会将搜索结果作为生成回复过程中的参考信息。</p><div><div><p><strong>说明</strong>模型会自行判断是否需要以及何时触发互联网搜索。</p></div></div></li><li><p>False（默认）：关闭互联网搜索。</p></li></ul><p>优先级：</p><ul><li><p>若调用时未设置此参数，以应用内联网搜索</p><p>开关状态为准。</p></li><li><p>若调用时设置了<code>enable_web_search</code>，以 API 参数为准。</p></li></ul><blockquote><p>启用互联网搜索功能可能会增加 Token 的消耗。</p></blockquote><blockquote><p>Java SDK中为<strong>enableWebSearch</strong>。通过HTTP调用时，请将 <strong>enable_web_search</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK的版本至少应为<strong>2.19.3</strong>。</p></blockquote><p><strong>dialog_round</strong><code>integer</code> （可选）</p><p>携带的上下文轮数。</p><div><div><p><strong>说明</strong>仅<strong>智能体应用</strong>支持此参数。</p></div></div><p>设置输入模型的最大历史对话轮数，轮数越多，对话相关性越强。</p><p>优先级：当通过 API 传递的<code>dialog_round</code>与控制台配置不同时，则以 API 参数值为准。</p><blockquote><p>Java SDK中为<strong>dialogRound</strong>。通过HTTP调用时，请将 <strong>dialog_round</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK的版本至少应为<strong>2.19.3</strong>。</p></blockquote><p><strong>enable_thinking</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>此参数用于在<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>中切换思考模式和非思考模式。仅适用于<strong>智能体应用</strong>。</p><div><div><p><strong>重要</strong><strong>工作流应用</strong>不支持通过此参数动态控制思考模式，需要在各大模型节点中分别设置。</p></div></div><p>参数值：</p><ul><li>False（默认）：非思考模式。直接返回最终答案（<code>text</code>字段）。</li><li>True：启用思考模式。模型先输出思考过程，再返回最终答案。</li></ul><p>优先级：</p><ul><li>若调用时未设置此参数，以应用内模型的思考模式开关状态为准。</li><li>若调用时设置了<code>enable_thinking</code>，以 API 参数为准。</li></ul><div><div><p><strong>重要</strong>要获取思考过程的内容，必须同时将<code>has_thoughts</code>设为<code>True</code>，则：</p><ol><li><strong>思考过程：智能体应用</strong>通过<code>thought</code>字段获取，<strong>工作流应用</strong>通过<code>reasoningContent</code>字段获取。</li><li><strong>最终答案：</strong><code>text</code>字段获取。</li></ol></div></div><blockquote><p>开启<code>enable_thinking</code>有极小概率不会输出思考过程。</p></blockquote><blockquote><p>Java SDK中为<strong>enableThinking</strong>。通过HTTP调用时，请将 <strong>enable_thinking</strong>放入 <strong>parameters</strong>对象中。</p></blockquote><blockquote><p>Java Dashscope SDK的版本至少应为<strong>2.20.0</strong>。</p></blockquote></td><td><a id="sec-tabs"></a><section><a id="单轮对话"></a><section><a id="单轮对话-h4"></a><h4>单轮对话</h4><a id="sec-tabs-2"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-8"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 替换为实际的应用 ID
        prompt='你是谁？')
    print(response.text)
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-9"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.12.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void appCall()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁？&quot;)
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf(&quot;text: %s\n&quot;,
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;message：&quot;+e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http"></a><section><a id="http-h4"></a><h4>HTTP</h4><a id="sec-tabs-3"></a><section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-10"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。</p></blockquote></section><a id="php"></a><section><a id="php-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-11"></a><pre class="language-php"><code>&lt;?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }}
else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js"></a><section><a id="node-js-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-12"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="code-block-13"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></section><a id="c"></a><section><a id="c-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-14"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go"></a><section><a id="go-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-15"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section><a id="dashscope-cli"></a><section><a id="dashscope-cli-h4"></a><h4>dashscope CLI</h4><strong>请求示例</strong><a id="code-block-16"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope application create -a your-app-id -p &quot;你好&quot;
</code></pre><blockquote><p>将 <code>your-app-id</code> 替换为实际的应用 ID。<code>-a</code> 指定应用 ID，<code>-p</code> 指定 prompt 内容。</p></blockquote><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../model-api-reference/preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div><p>完整地域表见 <a href="../model-api-reference/preparations/base-url.md">Base URL 总览</a>。</p></section></section></section><a id="多轮对话"></a><section><a id="多轮对话-h4"></a><h4>多轮对话</h4><p>通过<code>session_id</code>或<code>messages</code>启用多轮对话。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#6ca125d59eyc9">调用智能体应用-多轮对话</a>，<a href="../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md#6ca125d59eyc9">调用工作流应用-多轮对话</a>。</p><a id="sec-tabs-4"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-17"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

def call_with_session():
    client = dashscope.Client(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
    try:
        response = client.apps.completions.create(
            app_id='APP_ID',  # 替换为实际的应用 ID
            prompt='你是谁？')

        responseNext = client.apps.completions.create(
                    app_id='APP_ID',  # 替换为实际的应用 ID
                    prompt='你有什么技能?',
                    session_id=response.session_id)  # 上一轮response的session_id

        print('%s\n session_id=%s\n' % (responseNext.text, responseNext.session_id))
        # print('%s\n' % (response.usage))
    except DashScopeError as e:
        print(f'request_id={e.request_id}')
        print(f'code={e.code}')
        print(f'message={e.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')

if __name__ == '__main__':
    call_with_session()
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-18"></a><pre class="language-java"><code>import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;
import java.util.List;
public class Main {
    public static void callWithSession()
            throws ApiException, NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 替换为实际的应用 ID
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁？&quot;)
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        param.setSessionId(result.getOutput().getSessionId());
        param.setPrompt(&quot;你有什么技能?&quot;);
        result = application.call(param);

        System.out.printf(&quot;%s\n session_id: %s\n&quot;,
                result.getOutput().getText(), result.getOutput().getSessionId());
    }

    public static void main(String[] args) {
        try {
            callWithSession();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-2"></a><section><a id="http-2-h4"></a><h4>HTTP</h4><a id="sec-tabs-5"></a><section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-19"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-20"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你有什么技能？&quot;,
        &quot;session_id&quot;:&quot;4f8ef7233dc641aba496cb201fa59f8c&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre></section><a id="php-2"></a><section><a id="php-2-h4"></a><h4>PHP</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-21"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    };
    if (isset($response_data['output']['session_id'])) {
        echo &quot;session_id={$response_data['output']['session_id']}\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-22"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你有什么技能？',
        // 替换为实际上一轮对话返回的session_id
        'session_id' =&gt; '2e658bcb514f4d30ab7500b4766a8d43'
    ]
];

// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    };
    if (isset($response_data['output']['session_id'])) {
        echo &quot;session_id={$response_data['output']['session_id']}\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-2"></a><section><a id="node-js-2-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-23"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例（上一轮对话）</strong><a id="code-block-24"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-25"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;
    // session_id替换为实际上一轮对话的session_id
    const data = {
        input: {
            prompt: &quot;你有什么技能？&quot;,
            session_id: 'fe4ce8b093bf46159ea9927a7b22f0d3',
        },
        parameters: {},
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
            console.log(`session_id=${response.data.output.session_id}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
</code></pre></section><a id="c-2"></a><section><a id="c-2-h4"></a><h4>C#</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-26"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-27"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你有什么技能？&quot;&quot;,
                    &quot;&quot;session_id&quot;&quot;: &quot;&quot;7b830e4cc8fe44faad0e648f9b71435f&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-2"></a><section><a id="go-2-h4"></a><h4>Go</h4><strong>请求示例（上一轮对话）</strong><a id="code-block-28"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre><strong>请求示例（下一轮对话）</strong><a id="code-block-29"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;:     &quot;你有什么技能？&quot;,
			&quot;session_id&quot;: &quot;f7eea37f0c734c20998a021b688d6de2&quot;, // 替换为实际上一轮对话的session_id
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section><blockquote><p>APP_ID替换为实际的应用 ID。下一轮对话的输入参数<code>session_id</code>字段值替换为实际上一轮对话返回的session_id值。</p></blockquote></section></section></section><a id="传递-参数"></a><section><a id="传递-参数-h4"></a><h4>传递 参数</h4><p>通过<code>biz_params</code>传递自定义参数。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#b774db7cdc0aa">调用智能体应用-传递自定义参数</a>，<a href="../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md#6e644d5a7b3ia">调用工作流应用-传递自定义参数</a>。</p><a id="sec-tabs-6"></a><section><a id="python-3"></a><section><a id="python-3-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-30"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
biz_params = {
    # 智能体应用的自定义插件输入参数传递，自定义的插件ID替换&lt;TOOL_ID&gt;
    &quot;user_defined_params&quot;: {
        &quot;&lt;TOOL_ID&gt;&quot;: {
            &quot;article_index&quot;: 2}}}
try:
    response = client.apps.completions.create(
        app_id='APP_ID',
        prompt='寝室公约内容',
        biz_params=biz_params)
    print('%s\n' % (response.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-3"></a><section><a id="java-3-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-31"></a><pre class="language-java"><code>import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        String bizParams =
                // 智能体应用的自定义插件输入参数传递，自定义的插件ID替换&lt;TOOL_ID&gt;
                &quot;{\&quot;user_defined_params\&quot;:{\&quot;&lt;TOOL_ID&gt;\&quot;:{\&quot;article_index\&quot;:2}}}&quot;;
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;寝室公约内容&quot;)
                .bizParams(JsonUtils.parse(bizParams))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-3"></a><section><a id="http-3-h4"></a><h4>HTTP</h4><a id="sec-tabs-7"></a><section><a id="curl-3"></a><section><a id="curl-3-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-32"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;寝室公约内容&quot;,
        &quot;biz_params&quot;:
        {
            &quot;user_defined_params&quot;:
            {
                &quot;&lt;TOOL_ID&gt;&quot;:
                    {
                    &quot;article_index&quot;: 2
                    }
            }
        }
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;:{}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。&lt;TOOL_ID&gt;替换为插件ID。</p></blockquote></section><a id="php-3"></a><section><a id="php-3-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-33"></a><pre class="language-php"><code>&lt;?php

# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID
$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;
//&lt;TOOL_ID&gt;替换为实际的插件ID
// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '寝室公约内容',
        'biz_params' =&gt; [
        'user_defined_params' =&gt; [
            '&lt;TOOL_ID&gt;' =&gt; [
                'article_index' =&gt; 2
                ]
            ]
        ]
    ],
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-3"></a><section><a id="node-js-3-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-34"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="code-block-35"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID
    const pluginCode = 'TOOL_ID';// 替换为实际的插件ID
    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;寝室公约内容&quot;,
            biz_params: {
                user_defined_params: {
                    [pluginCode]: {
                        // article_index为自定义插件的变量，替换为实际的插件变量
                        'article_index': 3
                    }
                }
            }
        },
        parameters: {},
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            if (response.data.output &amp;&amp; response.data.output.text) {
                console.log(`${response.data.output.text}`);
            }
        } else {
            console.log(&quot;Request failed:&quot;);
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}
callDashScope();
</code></pre></section><a id="c-3"></a><section><a id="c-3-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-36"></a><pre class="language-csharp"><code>using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string pluginCode = &quot;TOOL_ID&quot;; // TOOL_ID替换为实际的插件 ID
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;寝室公约内容&quot;&quot;,
                    &quot;&quot;biz_params&quot;&quot;: {{
                        &quot;&quot;user_defined_params&quot;&quot;: {{
                            &quot;&quot;{pluginCode}&quot;&quot;: {{
                                &quot;&quot;article_index&quot;&quot;: 2
                            }}
                        }}
                    }}
                }},
                &quot;&quot;parameters&quot;&quot;: {{}},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-3"></a><section><a id="go-3-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-37"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot;           // 替换为实际的应用 ID
	pluginCode := &quot;TOOL_ID&quot; // 替换为实际的插件 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]interface{}{
			&quot;prompt&quot;: &quot;寝室公约内容&quot;,
			&quot;biz_params&quot;: map[string]interface{}{
				&quot;user_defined_params&quot;: map[string]interface{}{
					pluginCode: map[string]interface{}{
						&quot;article_index&quot;: 2,
					},
				},
			},
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section></section></section><a id="发布新版本对-api-调用的影响"></a><section><a id="发布新版本对-api-调用的影响-h4"></a><h4>发布新版本对 API 调用的影响</h4><p>应用发布新版本后，APP_ID 始终指向最新已发布版本。发布时正在进行的请求不会被中断，会按发布前的配置正常完成；发布完成后，通过同一 APP_ID 发起的新请求将使用新版本的配置（包括<strong>提示词</strong>、模型、工具等）。</p><p>API 不支持通过参数指定调用历史版本。请求体仅包含<code>input</code>和<code>parameters</code>字段，不提供版本号或历史版本参数。</p><p>多轮对话的<code>session_id</code>在新版本发布后继续使用时，可能出现上下文理解偏差或工具调用异常，因为该会话的历史上下文基于发布前的配置产生。建议在发布重大变更前结束活跃的多轮对话，或在发布后使用新的<code>session_id</code>重新开始会话。</p><p>如需恢复发布前的配置，请在<strong>百炼控制台</strong>的<strong>应用详情页</strong>执行版本回滚：</p><ol><li>单击<strong>版本管理</strong>。</li><li>选中需要恢复的历史版本。</li><li>单击<strong>覆盖当前草稿</strong>。</li><li>单击<strong>发布</strong>，使回滚生效。</li></ol><p>为降低对线上调用的影响，建议在业务低峰期发布重大变更；如需同时对外提供多个版本的能力，可通过创建多个应用（使用不同的 APP_ID）实现版本管理。</p></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><p>通过<code>stream</code>实现流式输出。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#b3be03a1ff21e">调用智能体应用-流式输出</a>，<a href="../application-user-guide/agent-development/llm-application/bailian-application-calling/invoke-workflow-application.md#b3be03a1ff21e">调用工作流应用-流式输出</a>。</p><a id="sec-tabs-8"></a><section><a id="python-4"></a><section><a id="python-4-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-38"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    stream = client.apps.completions.create(
                app_id='APP_ID',
                prompt='你是谁？',
                stream=True,  # 流式输出
                incremental_output=True)  # 增量输出

    for partial in stream:
        print(f'{partial.text}\n')  # 处理只输出文本text
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-4"></a><section><a id="java-4-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-39"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.15.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;// 流式输出
// 智能体应用调用实现流式输出结果

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 替换为实际的应用 ID
                .appId(&quot;APP_ID&quot;)
                .prompt(&quot;你是谁?&quot;)
                // 增量输出
                .incrementalOutput(true)
                .build();
        Application application = new Application();
        // .streamCall（）：流式输出内容
        Flowable&lt;ApplicationResult&gt; result = application.streamCall(param);
        result.blockingForEach(data -&gt; {
            System.out.printf(&quot;%s\n&quot;,
                    data.getOutput().getText());
        });
    }
    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-4"></a><section><a id="http-4-h4"></a><h4>HTTP</h4><a id="sec-tabs-9"></a><section><a id="curl-4"></a><section><a id="curl-4-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-40"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--header 'X-DashScope-SSE: enable' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;你是谁？&quot;

    },
    &quot;parameters&quot;:  {
        &quot;incremental_output&quot;:true
    },
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。</p></blockquote></section><a id="php-4"></a><section><a id="php-4-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-41"></a><pre class="language-php"><code>&lt;?php

// 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '你是谁？'],
    &quot;parameters&quot; =&gt; [
        'incremental_output' =&gt; true]];// 增量输出
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, false); // 不返回传输的数据
curl_setopt($ch, CURLOPT_WRITEFUNCTION, function ($ch, $string) {
    echo $string; // 处理流式数据
    return strlen($string);
});
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key,
    'X-DashScope-SSE: enable' // 流式输出
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);

if ($status_code != 200) {
    echo &quot;HTTP Status Code: $status_code\n&quot;;
    echo &quot;Request Failed.\n&quot;;
}
?&gt;
</code></pre></section><a id="node-js-4"></a><section><a id="node-js-4-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-42"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="accordion-1-输出完整响应"></a><section><p>1.输出完整响应</p><div><a id="code-block-43"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;你是谁？&quot;
        },
        parameters: {
            'incremental_output' : true // 增量输出
        },
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // 处理流式响应
            response.data.on('data', (chunk) =&gt; {
                console.log(`Received chunk: ${chunk.toString()}`);
            });
        } else {
            console.log(&quot;Request failed:&quot;);
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></div></section><p>可展开折叠面板查看具体内容：</p><a id="accordion-2-只输出text字段内容"></a><section><p>2.只输出text字段内容</p><div><a id="code-block-44"></a><pre class="language-javascript"><code>const axios = require('axios');
const { Transform } = require('stream');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID'; // 替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: { prompt: &quot;你是谁？&quot; },
        parameters: { incremental_output: true }, // 增量输出
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'enable' // 流式输出
            },
            responseType: 'stream' // 用于处理流式响应
        });

        if (response.status === 200) {
            // // 处理流式响应 SSE协议解析转换流
            const sseTransformer = new Transform({
                transform(chunk, encoding, callback) {
                    this.buffer += chunk.toString();

                    // 按SSE事件分割（两个换行符）
                    const events = this.buffer.split(/\n\n/);
                    this.buffer = events.pop() || ''; // 保留未完成部分

                    events.forEach(eventData =&gt; {
                        const lines = eventData.split('\n');
                        let textContent = '';

                        // 解析事件内容
                        lines.forEach(line =&gt; {
                            if (line.startsWith('data:')) {
                                try {
                                    const jsonData = JSON.parse(line.slice(5).trim());
                                    if (jsonData.output?.text) {
                                        textContent = jsonData.output.text;
                                    }
                                } catch(e) {
                                    console.error('JSON解析错误:', e.message);
                                }
                            }
                        });

                        if (textContent) {
                            // 添加换行符并推送
                            this.push(textContent + '\n');
                        }
                    });

                    callback();
                },
                flush(callback) {
                    if (this.buffer) {
                        this.push(this.buffer + '\n');
                    }
                    callback();
                }
            });
            sseTransformer.buffer = '';

            // 管道处理
            response.data
                .pipe(sseTransformer)
                .on('data', (textWithNewline) =&gt; {
                    process.stdout.write(textWithNewline); // 自动换行输出
                })
                .on('end', () =&gt; console.log(&quot;&quot;))
                .on('error', err =&gt; console.error(&quot;管道错误:&quot;, err));

        } else {
            console.log(&quot;请求失败，状态码:&quot;, response.status);
            response.data.on('data', chunk =&gt; console.log(chunk.toString()));
        }
    } catch (error) {
        console.error(`API调用失败: ${error.message}`);
        if (error.response) {
            console.error(`状态码: ${error.response.status}`);
            error.response.data.on('data', chunk =&gt; console.log(chunk.toString()));
        }
    }
}

callDashScope();
</code></pre></div></section></section><a id="c-4"></a><section><a id="c-4-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-45"></a><pre class="language-csharp"><code>using System.Net;
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;) ?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;; // 替换为实际的应用ID
        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            client.DefaultRequestHeaders.Add(&quot;X-DashScope-SSE&quot;, &quot;enable&quot;);

            string jsonContent = @&quot;{
                &quot;&quot;input&quot;&quot;: {
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;你是谁&quot;&quot;
                },
                &quot;&quot;parameters&quot;&quot;: {&quot;&quot;incremental_output&quot;&quot;: true},
                &quot;&quot;debug&quot;&quot;: {}
            }&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, url);
                request.Content = content;

                HttpResponseMessage response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine(&quot;Request successful:&quot;);
                    Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
                    using (var stream = await response.Content.ReadAsStreamAsync())
                    using (var reader = new StreamReader(stream))
                    {
                        string? line; // 声明为可空字符串
                        while ((line = await reader.ReadLineAsync()) != null)
                        {
                            if (line.StartsWith(&quot;data:&quot;))
                            {
                                string data = line.Substring(5).Trim();
                                Console.WriteLine(data);
                                Console.WriteLine(DateTime.Now.ToString(&quot;yyyy-MM-dd HH:mm:ss:fff&quot;));
                            }
                        }
                    }
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-4"></a><section><a id="go-4-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-46"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
	&quot;strings&quot;
	&quot;time&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体，其中incremental_output为是否开启流式响应
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;你是谁？&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{
			&quot;incremental_output&quot;: true,
		},
		&quot;debug&quot;: map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头,其中X-DashScope-SSE设置为enable，表示开启流式响应
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)
	req.Header.Set(&quot;X-DashScope-SSE&quot;, &quot;enable&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		body, _ := io.ReadAll(resp.Body)
		fmt.Println(string(body))
		return
	}

	// 处理流式响应
	reader := io.Reader(resp.Body)
	buf := make([]byte, 1024)
	for {
		n, err := reader.Read(buf)
		if n &gt; 0 {
			data := string(buf[:n])
			lines := strings.Split(data, &quot;\n&quot;)
			for _, line := range lines {
				line = strings.TrimSpace(line)
				if len(line) &gt;= 5 &amp;&amp; line[:5] == &quot;data:&quot; {
					timestamp := time.Now().Format(&quot;2006-01-02 15:04:05.000&quot;)
					fmt.Printf(&quot;%s: %s\n&quot;, timestamp, line[5:])
				} else if len(line) &gt; 0 {
					fmt.Println(line)
				}
			}
		}
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf(&quot;Error reading response: %v\n&quot;, err)
			break
		}
	}
}
</code></pre></section></section></section></section></section><a id="检索知识库"></a><section><a id="检索知识库-h4"></a><h4>检索知识库</h4><p>调用<strong>智能体应用</strong>时，通过<code>rag_options</code>实现知识库检索。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#bb173820c5whx">检索知识库</a>。</p><a id="sec-tabs-10"></a><section><a id="python-5"></a><section><a id="python-5-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-47"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='请帮我推荐一款3000元以下的手机',
        rag_options={
            &quot;pipeline_ids&quot;: [&quot;PIPELINE_ID1&quot;,&quot;PIPELINE_ID2&quot;],  # 替换为实际的知识库ID,逗号隔开多个
        }
    )
    print('%s\n' % (response.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-5"></a><section><a id="java-5-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-48"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.16.8；
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;

public class Main {
    public static void streamCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;请帮我推荐一款3000元左右的手机&quot;)
                .ragOptions(RagOptions.builder()
                        // 替换为实际指定的知识库ID，逗号隔开多个
                        .pipelineIds(Arrays.asList(&quot;PIPELINES_ID1&quot;, &quot;PIPELINES_ID2&quot;))
                        .build())
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());// 处理只输出文本text
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-5"></a><section><a id="http-5-h4"></a><h4>HTTP</h4><a id="sec-tabs-11"></a><section><a id="curl-5"></a><section><a id="curl-5-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-49"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;请帮我推荐一款3000元以下的手机&quot;
    },
    &quot;parameters&quot;:  {
                    &quot;rag_options&quot; : {
                    &quot;pipeline_ids&quot;:[&quot;PIPELINE_ID1&quot;]}
    },
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID，PIPELINE_ID1替换为指定的知识库ID。</p></blockquote></section><a id="php-5"></a><section><a id="php-5-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-50"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '请帮我推荐一款3000元以下的手机'
    ],
    &quot;parameters&quot; =&gt; [
        'rag_options' =&gt; [
            'pipeline_ids' =&gt; ['PIPELINE_ID1','PIPELINE_ID2']//替换为指定的知识库ID,逗号隔开多个
        ]
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-5"></a><section><a id="node-js-5-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-51"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="code-block-52"></a><pre class="language-javascript"><code>const axios = require('axios');
async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';//替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;请帮我推荐一款3000元以下的手机&quot;
        },
        parameters: {
            rag_options:{
                pipeline_ids:['PIPELINE_ID1','PIPELINE_ID2']  // 替换为指定的知识库ID，多个请用逗号隔开
            }
        },
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></section><a id="c-5"></a><section><a id="c-5-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-53"></a><pre class="language-csharp"><code>using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID
        // PIPELINE_ID1替换为指定的知识库ID
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;请帮我推荐一款3000元以下的手机&quot;&quot;
                }},
                &quot;&quot;parameters&quot;&quot;: {{
                    &quot;&quot;rag_options&quot;&quot; : {{
                        &quot;&quot;pipeline_ids&quot;&quot;:[&quot;&quot;PIPELINE_ID1&quot;&quot;]
                    }}
                }},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-5"></a><section><a id="go-5-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-54"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;请帮我推荐一款3000元以下的手机&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{
			&quot;rag_options&quot;: map[string]interface{}{
				&quot;pipeline_ids&quot;: []string{&quot;PIPELINE_ID1&quot;}, // 替换为指定的知识库ID
			},
		},
		&quot;debug&quot;: map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section></section><p><strong>查看检索过程信息：</strong>调用时在代码中添加<code>has_thoughts</code>并设置为True，则检索的过程信息会在响应的<code>thoughts</code>字段中返回。</p></section><a id="长期记忆"></a><section><a id="长期记忆-h4"></a><h4>长期记忆</h4><p>调用<strong>智能体应用</strong>时，指定 <code>memory_id</code> 启用长期记忆。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#de63036b85aj0">长期记忆</a>。</p><a id="sec-tabs-12"></a><section><a id="python-6"></a><section><a id="python-6-h4"></a><h4>Python</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-55"></a><pre class="language-python"><code># 需要 dashscope 2.0.1 及以上版本
import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
           # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
                app_id='APP_ID',  # 请输入实际的应用 ID
                prompt='用户饮食偏好：面食',
                memory_id='MEMORY_ID')  # 请输入实际的记忆体 ID

    print('%s\n' % (response.text))  # 处理只输出text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-56"></a><pre class="language-python"><code># 需要 dashscope 2.0.1 及以上版本
import os
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(
           # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
                app_id='APP_ID',  # 请输入实际的应用 ID
                prompt='美食推荐',
                memory_id='MEMORY_ID')  # 请输入实际的记忆体 ID

    print('%s\n' % (response.text))  # 处理只输出text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-6"></a><section><a id="java-6-h4"></a><h4>Java</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-57"></a><pre class="language-java"><code>// DashScope SDK版本不低于2.17.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void callWithMemory() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用 ID
                .prompt(&quot;用户饮食偏好：面食&quot;)
                .memoryId(&quot;MEMORY_ID&quot;) // 替换为实际的记忆体 ID
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText()); // 处理只输出文本text
    }
    public static void main(String[] args) {
        try {
            callWithMemory();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-58"></a><pre class="language-java"><code>// DashScope SDK版本不低于2.17.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public class Main {
    public static void callWithMemory() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用 ID
                .prompt(&quot;美食推荐&quot;)
                .memoryId(&quot;MEMORY_ID&quot;) // 替换为实际的记忆体 ID
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);

        System.out.printf(&quot;text: %s\n&quot;,
                result.getOutput().getText()); // 处理只输出文本text
    }
    public static void main(String[] args) {
        try {
            callWithMemory();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-6"></a><section><a id="http-6-h4"></a><h4>HTTP</h4><a id="sec-tabs-13"></a><section><a id="curl-6"></a><section><a id="curl-6-h4"></a><h4>curl</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-59"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;用户饮食偏好：面食&quot;,
        &quot;memory_id&quot;: &quot;MEMORY_ID&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-60"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;美食推荐&quot;,
        &quot;memory_id&quot;: &quot;MEMORY_ID&quot;
    },
    &quot;parameters&quot;:  {},
    &quot;debug&quot;: {}
}'
</code></pre><blockquote><p>APP_ID替换为实际的应用 ID。</p></blockquote></section><a id="php-6"></a><section><a id="php-6-h4"></a><h4>PHP</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-61"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID
$memory_id = 'MEMORY_ID'; // 替换为实际的记忆体 ID
$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/{$application_id}/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '用户饮食偏好：面食',
        'memory_id' =&gt; $memory_id
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-62"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID
$memory_id = 'MEMORY_ID'; // 替换为实际的记忆体 ID
$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/{$application_id}/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '美食推荐',
        'memory_id' =&gt; $memory_id
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-6"></a><section><a id="node-js-6-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-63"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例（生成记忆体内容）</strong><a id="code-block-64"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID
    const memoryId = 'MEMORY_ID';// 替换为实际的memory_id

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;用户饮食偏好：面食&quot;,
            memory_id: memoryId
        },
        parameters: {},
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            if (response.data.output &amp;&amp; response.data.output.text) {
                console.log(`${response.data.output.text}`);
            }
        } else {
            console.log(&quot;Request failed:&quot;);
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-65"></a><pre class="language-javascript"><code>const axios = require('axios');

async function callDashScope() {
    //若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';// 替换为实际的应用 ID
    const memoryId = 'MEMORY_ID';// 替换为实际的memory_id

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;美食推荐&quot;,
            memory_id: memoryId
        },
        parameters: {},
        debug: {}
    };

    try {
        console.log(&quot;Sending request to DashScope API...&quot;);

        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            if (response.data.output &amp;&amp; response.data.output.text) {
                console.log(`${response.data.output.text}`);
            }
        } else {
            console.log(&quot;Request failed:&quot;);
            if (response.data.request_id) {
                console.log(`request_id=${response.data.request_id}`);
            }
            console.log(`code=${response.status}`);
            if (response.data.message) {
                console.log(`message=${response.data.message}`);
            } else {
                console.log('message=Unknown error');
            }
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></section><a id="c-6"></a><section><a id="c-6-h4"></a><h4>C#</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-66"></a><pre class="language-csharp"><code>using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID
        string memoryId = &quot;MEMORY_ID&quot;;//替换为实际的memory_id
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;用户饮食偏好：面食&quot;&quot;,
                    &quot;&quot;memory_id&quot;&quot;:&quot;&quot;{memoryId}&quot;&quot;
                }},
                &quot;&quot;parameters&quot;&quot;: {{}},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-67"></a><pre class="language-csharp"><code>using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID
        string memoryId = &quot;MEMORY_ID&quot;;//替换为实际的memory_id
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;美食推荐&quot;&quot;,
                    &quot;&quot;memory_id&quot;&quot;:&quot;&quot;{memoryId}&quot;&quot;
                }},
                &quot;&quot;parameters&quot;&quot;: {{}},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-6"></a><section><a id="go-6-h4"></a><h4>Go</h4><strong>请求示例（生成记忆体内容）</strong><a id="code-block-68"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;:    &quot;用户饮食偏好：面食&quot;,
			&quot;memory_id&quot;: &quot;MEMORY_ID&quot;, // 替换为实际的记忆体 ID
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre><strong>请求示例（再次调用）</strong><a id="code-block-69"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;:    &quot;美食推荐&quot;,
			&quot;memory_id&quot;: &quot;MEMORY_ID&quot;, // 替换为实际的记忆体 ID
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section></section></section><a id="上传文件"></a><section><a id="上传文件-h4"></a><h4>上传文件</h4><p>调用<strong>智能体应用</strong>时，指定 <code>session_file_ids</code> /<code>file_list</code>启用上传文件功能。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#30619780ddy93">文件问答</a>。</p><a id="sec-tabs-14"></a><section><a id="python-7"></a><section><a id="python-7-h4"></a><h4>Python</h4><strong>请求示例</strong><a id="code-block-70"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='请根据以下文件帮我推荐一款3000元以下的手机',
        rag_options={
            &quot;session_file_ids&quot;: [&quot;Session_File_ID1&quot;],  # Session_File_ID1 替换为实际的临时文件ID,逗号隔开多个
        }
    )
    print('%s\n' % (response.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-7"></a><section><a id="java-7-h4"></a><h4>Java</h4><strong>请求示例</strong><a id="code-block-71"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.17.0；
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

import java.util.Arrays;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;请根据以下文件帮我推荐一款3000元左右的手机&quot;)
                .ragOptions(RagOptions.builder()
                        .sessionFileIds(Arrays.asList(&quot;Session_File_ID1&quot;, &quot;Session_File_ID2&quot;))  // 替换为实际指定的临时文件 ID，逗号隔开多个
                        .build())
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());// 处理只输出文本text
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-7"></a><section><a id="http-7-h4"></a><h4>HTTP</h4><a id="sec-tabs-15"></a><section><a id="curl-7"></a><section><a id="curl-7-h4"></a><h4>curl</h4><strong>请求示例</strong><a id="code-block-72"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;请根据以下文件帮我推荐一款3000元以下的手机&quot;
    },
    &quot;parameters&quot;:  {
                    &quot;rag_options&quot; : {
                    &quot;session_file_ids&quot;:[&quot;Session_File_ID1&quot;]}
    },
    &quot;debug&quot;: {}
}'
</code></pre></section><a id="php-7"></a><section><a id="php-7-h4"></a><h4>PHP</h4><strong>请求示例</strong><a id="code-block-73"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        'prompt' =&gt; '请根据以下文件帮我推荐一款3000元以下的手机'
    ],
    &quot;parameters&quot; =&gt; [
        'rag_options' =&gt; [
            'session_file_ids' =&gt; ['Session_File_ID1']//替换为指定的临时文件ID,逗号隔开多个
        ]
    ]
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre></section><a id="node-js-7"></a><section><a id="node-js-7-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-74"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>请求示例</strong><a id="code-block-75"></a><pre class="language-javascript"><code>const axios = require('axios');
async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';//替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;请根据以下文件帮我推荐一款3000元以下的手机&quot;
        },
        parameters: {
            rag_options:{
                session_file_ids:['Session_File_ID1']  // 替换为指定的临时文件 ID，多个请用逗号隔开
            }
        },
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre></section><a id="c-7"></a><section><a id="c-7-h4"></a><h4>C#</h4><strong>请求示例</strong><a id="code-block-76"></a><pre class="language-csharp"><code>using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID
        // Session_File_ID1替换为指定的临时文件ID
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;请根据以下文件帮我推荐一款3000元以下的手机&quot;&quot;
                }},
                &quot;&quot;parameters&quot;&quot;: {{
                    &quot;&quot;rag_options&quot;&quot; : {{
                        &quot;&quot;session_file_ids&quot;&quot;:[&quot;&quot;Session_File_ID1&quot;&quot;]
                    }}
                }},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre></section><a id="go-7"></a><section><a id="go-7-h4"></a><h4>Go</h4><strong>请求示例</strong><a id="code-block-77"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]string{
			&quot;prompt&quot;: &quot;请根据以下文件帮我推荐一款3000元以下的手机&quot;,
		},
		&quot;parameters&quot;: map[string]interface{}{
			&quot;rag_options&quot;: map[string]interface{}{
				&quot;session_file_ids&quot;: []string{&quot;Session_File_ID1&quot;}, // 替换为实际的临时文件
			},
		},
		&quot;debug&quot;: map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre></section></section></section></section></section><a id="视觉理解"></a><section><a id="视觉理解-h4"></a><h4>视觉理解</h4><p>通过 <code>image_list</code> 参数传入图像 URL 或 Data URL（Base64 编码）启用视觉理解功能。</p><p><strong>应用配置：</strong>应用内需使用<a href="../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a>模型。相关文档：<a href="call-single-agent-application-7bb88312c0915edf.md#30619780ddy93">文件问答</a>。</p><div><div><p><strong>说明</strong>支持使用 Base64 编码本地图像。将图像编码为 Base64 字符串后，按<code>data:[MIME_type];base64,{base64_image}</code>格式构建 Data URL 传入。<code>MIME_type</code>必须与图像格式匹配。常见格式：PNG 使用 <code>image/png</code>，JPEG 使用 <code>image/jpeg</code>，WebP 使用 <code>image/webp</code>。</p></div></div><a id="sec-tabs-16"></a><section><a id="python-8"></a><section><a id="python-8-h4"></a><h4>Python</h4><strong>URL请求示例</strong><a id="code-block-78"></a><pre class="language-python"><code>import os
import dashscope
# 需要 dashscope 2.0.1 及以上版本
from dashscope import DashScopeError

client = dashscope.Client(
    # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='这是什么',
        image_list=['https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg'],
    )
    print('%s\n' % (response.text))  # 处理只输出文本text
    # print('%s\n' % (response.usage))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre><strong>Base64 编码示例</strong><a id="code-block-79"></a><pre class="language-python"><code>import os
import base64
import dashscope
from dashscope import DashScopeError

client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

# 将本地图像编码为 Base64 字符串
def encode_image(image_path):
    with open(image_path, &quot;rb&quot;) as image_file:
        return base64.b64encode(image_file.read()).decode(&quot;utf-8&quot;)

# 编码本地图像
base64_image = encode_image(&quot;/path/to/your/image.jpeg&quot;)  # 替换为实际图像路径

# 构建 Data URL（注意：MIME type 需与图像格式匹配）
data_url = f&quot;data:image/jpeg;base64,{base64_image}&quot;

# 调用应用 API
try:
    response = client.apps.completions.create(
        app_id='APP_ID',  # 应用ID替换APP_ID
        prompt='这张图片里有什么？',
        image_list=[data_url],  # 使用 Data URL
    )
    print('%s\n' % (response.text))
except DashScopeError as e:
    print(f'request_id={e.request_id}')
    print(f'code={e.code}')
    print(f'message={e.message}')
    print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
</code></pre></section><a id="java-8"></a><section><a id="java-8-h4"></a><h4>Java</h4><strong>URL请求示例</strong><a id="code-block-80"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.19.0；
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Arrays;

public class Main {
    public static void appCall() throws NoApiKeyException, InputRequiredException {
        ApplicationParam param = ApplicationParam.builder()
                // 若没有配置环境变量，可用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;这是什么？&quot;)
                .images(Arrays.asList(&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;))
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;,
                result.getOutput().getText());// 处理只输出文本text
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-81"></a><pre class="language-java"><code>// 建议dashscope SDK 的版本 &gt;= 2.19.0
import com.alibaba.dashscope.app.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Base64;

public class Main {
    // 将本地图像编码为 Base64 字符串
    public static String encodeImage(String imagePath) throws IOException {
        byte[] imageBytes = Files.readAllBytes(Paths.get(imagePath));
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void appCall() throws NoApiKeyException, InputRequiredException, IOException {
        // 编码本地图像
        String base64Image = encodeImage(&quot;/path/to/your/image.jpeg&quot;); // 替换为实际图像路径

        // 构建 Data URL（注意：MIME type 需与图像格式匹配）
        String dataUrl = &quot;data:image/jpeg;base64,&quot; + base64Image;

        ApplicationParam param = ApplicationParam.builder()
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .appId(&quot;APP_ID&quot;) // 替换为实际的应用ID
                .prompt(&quot;这张图片里有什么？&quot;)
                .images(Arrays.asList(dataUrl)) // 使用 Data URL
                .build();

        Application application = new Application();
        ApplicationResult result = application.call(param);
        System.out.printf(&quot;%s\n&quot;, result.getOutput().getText());
    }

    public static void main(String[] args) {
        try {
            appCall();
        } catch (ApiException | NoApiKeyException | InputRequiredException | IOException e) {
            System.out.printf(&quot;Exception: %s&quot;, e.getMessage());
            System.out.println(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;);
        }
        System.exit(0);
    }
}
</code></pre></section><a id="http-8"></a><section><a id="http-8-h4"></a><h4>HTTP</h4><a id="sec-tabs-17"></a><section><a id="curl-8"></a><section><a id="curl-8-h4"></a><h4>curl</h4><strong>URL请求示例</strong><a id="code-block-82"></a><pre class="language-bash"><code>curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;这是什么&quot;,
        &quot;image_list&quot;:[&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;]
    },
    &quot;debug&quot;: {}
}'
</code></pre><strong>Base64 编码示例</strong><a id="code-block-83"></a><pre class="language-bash"><code># 将本地图像编码为 Base64 字符串
base64_image=$(base64 -i /path/to/your/image.jpeg)  # macOS/Linux

# 构建 Data URL（注意：MIME type 需与图像格式匹配）
data_url=&quot;data:image/jpeg;base64,${base64_image}&quot;

# 调用应用 API
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data &quot;{
    \&quot;input\&quot;: {
        \&quot;prompt\&quot;: \&quot;这张图片里有什么？\&quot;,
        \&quot;image_list\&quot;: [\&quot;${data_url}\&quot;]
    },
    \&quot;debug\&quot;: {}
}&quot;
</code></pre></section><a id="php-8"></a><section><a id="php-8-h4"></a><h4>PHP</h4><strong>URL请求示例</strong><a id="code-block-84"></a><pre class="language-php"><code>&lt;?php
# 若没有配置环境变量，可用百炼API Key将下行替换为：$api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID'; // 替换为实际的应用 ID

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;

// 构造请求数据
$data = [
    &quot;input&quot; =&gt; [
        &quot;prompt&quot; =&gt; &quot;这是什么&quot;,
        &quot;image_list&quot; =&gt; [&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;],
    ],
    &quot;debug&quot; =&gt; [],
];
// 将数据编码为 JSON
$dataString = json_encode($data);

// 检查 json_encode 是否成功
if (json_last_error() !== JSON_ERROR_NONE) {
    die(&quot;JSON encoding failed with error: &quot; . json_last_error_msg());
}

// 初始化 cURL 对话
$ch = curl_init($url);

// 设置 cURL 选项
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, $dataString);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $api_key
]);

// 执行请求
$response = curl_exec($ch);

// 检查 cURL 执行是否成功
if ($response === false) {
    die(&quot;cURL Error: &quot; . curl_error($ch));
}

// 获取 HTTP 状态码
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
// 关闭 cURL 对话
curl_close($ch);
// 解码响应数据
$response_data = json_decode($response, true);
// 处理响应
if ($status_code == 200) {
    if (isset($response_data['output']['text'])) {
        echo &quot;{$response_data['output']['text']}\n&quot;;
    } else {
        echo &quot;No text in response.\n&quot;;
    }
}else {
    if (isset($response_data['request_id'])) {
        echo &quot;request_id={$response_data['request_id']}\n&quot;;}
    echo &quot;code={$status_code}\n&quot;;
    if (isset($response_data['message'])) {
        echo &quot;message={$response_data['message']}\n&quot;;}
    else {
        echo &quot;message=Unknown error\n&quot;;}
}
?&gt;
</code></pre><strong>Base64 编码示例</strong><a id="code-block-85"></a><pre class="language-php"><code>&lt;?php
$api_key = getenv(&quot;DASHSCOPE_API_KEY&quot;);
$application_id = 'APP_ID';

function encodeImage($imagePath) {
    if (!file_exists($imagePath)) die(&quot;Error: Image file not found&quot;);
    return base64_encode(file_get_contents($imagePath));
}

$base64Image = encodeImage(&quot;/path/to/your/image.jpeg&quot;);
$dataUrl = &quot;data:image/jpeg;base64,&quot; . $base64Image;

$url = &quot;https://dashscope.aliyuncs.com/api/v1/apps/$application_id/completion&quot;;
$data = [&quot;input&quot; =&gt; [&quot;prompt&quot; =&gt; &quot;这张图片里有什么？&quot;, &quot;image_list&quot; =&gt; [$dataUrl]], &quot;debug&quot; =&gt; []];

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, &quot;POST&quot;);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json', 'Authorization: Bearer ' . $api_key]);

$response = curl_exec($ch);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($status_code == 200) {
    $response_data = json_decode($response, true);
    echo $response_data['output']['text'];
}
?&gt;
</code></pre></section><a id="node-js-8"></a><section><a id="node-js-8-h4"></a><h4>Node.js</h4><strong>需安装相关依赖：</strong><a id="code-block-86"></a><pre class="language-bash"><code>npm install axios
</code></pre><strong>URL请求示例</strong><a id="code-block-87"></a><pre class="language-javascript"><code>import axios from 'axios';
async function callDashScope() {
    // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey='sk-xxx'。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';//替换为实际的应用 ID

    const url = `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`;

    const data = {
        input: {
            prompt: &quot;这是什么&quot;,
            image_list: [&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;],
        },
        debug: {}
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            console.log(`${response.data.output.text}`);
        } else {
            console.log(`request_id=${response.headers['request_id']}`);
            console.log(`code=${response.status}`);
            console.log(`message=${response.data.message}`);
        }
    } catch (error) {
        console.error(`Error calling DashScope: ${error.message}`);
        if (error.response) {
            console.error(`Response status: ${error.response.status}`);
            console.error(`Response data: ${JSON.stringify(error.response.data, null, 2)}`);
        }
    }
}

callDashScope();
</code></pre><strong>Base64 编码示例</strong><a id="code-block-88"></a><pre class="language-javascript"><code>import axios from 'axios';
import fs from 'fs';

async function callWithBase64() {
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const appId = 'APP_ID';

    const imageBuffer = fs.readFileSync('/path/to/your/image.jpeg');
    const base64Image = imageBuffer.toString('base64');
    const dataUrl = `data:image/jpeg;base64,${base64Image}`;

    const response = await axios.post(
        `https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`,
        { input: { prompt: &quot;这张图片里有什么？&quot;, image_list: [dataUrl] } },
        { headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' } }
    );

    console.log(response.data.output.text);
}

callWithBase64();
</code></pre></section><a id="c-8"></a><section><a id="c-8-h4"></a><h4>C#</h4><strong>URL请求示例</strong><a id="code-block-89"></a><pre class="language-csharp"><code>using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        string apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;)?? throw new InvalidOperationException(&quot;DASHSCOPE_API_KEY environment variable is not set.&quot;);
        string appId = &quot;APP_ID&quot;;// 替换为实际的应用ID

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;请确保设置了 DASHSCOPE_API_KEY。&quot;);
            return;
        }

        string url = $&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;;

        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);
            string jsonContent = $@&quot;{{
                &quot;&quot;input&quot;&quot;: {{
                    &quot;&quot;prompt&quot;&quot;: &quot;&quot;这是什么&quot;&quot;,
                    &quot;&quot;image_list&quot;&quot;: [&quot;&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;&quot;]
                }},
                &quot;&quot;parameters&quot;&quot;: {{
                }},
                &quot;&quot;debug&quot;&quot;: {{}}
            }}&quot;;

            HttpContent content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;);

            try
            {
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
                else
                {
                    Console.WriteLine($&quot;Request failed with status code: {response.StatusCode}&quot;);
                    string responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine(responseBody);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($&quot;Error calling DashScope: {ex.Message}&quot;);
            }
        }
    }
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-90"></a><pre class="language-csharp"><code>using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        var apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;);
        var appId = &quot;APP_ID&quot;;

        byte[] imageBytes = File.ReadAllBytes(&quot;/path/to/your/image.jpeg&quot;);
        var base64Image = Convert.ToBase64String(imageBytes);
        var dataUrl = $&quot;data:image/jpeg;base64,{base64Image}&quot;;

        using var client = new HttpClient();
        client.DefaultRequestHeaders.Add(&quot;Authorization&quot;, $&quot;Bearer {apiKey}&quot;);

        var json = $@&quot;{{&quot;&quot;input&quot;&quot;: {{&quot;&quot;prompt&quot;&quot;: &quot;&quot;这张图片里有什么？&quot;&quot;, &quot;&quot;image_list&quot;&quot;: [&quot;&quot;{dataUrl}&quot;&quot;]}}, &quot;&quot;debug&quot;&quot;: {{}}}}&quot;;
        var content = new StringContent(json, Encoding.UTF8, &quot;application/json&quot;);
        var response = await client.PostAsync($&quot;https://dashscope.aliyuncs.com/api/v1/apps/{appId}/completion&quot;, content);

        Console.WriteLine(await response.Content.ReadAsStringAsync());
    }
}
</code></pre></section><a id="go-8"></a><section><a id="go-8-h4"></a><h4>Go</h4><strong>URL请求示例</strong><a id="code-block-91"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	// 若没有配置环境变量，可用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot; // 替换为实际的应用 ID

	if apiKey == &quot;&quot; {
		fmt.Println(&quot;请确保设置了DASHSCOPE_API_KEY。&quot;)
		return
	}

	url := fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId)

	// 创建请求体
	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]interface{}{
			&quot;prompt&quot;:     &quot;这是什么&quot;,
			&quot;image_list&quot;: []string{&quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;},
		},
		&quot;parameters&quot;: map[string]interface{}{},
		&quot;debug&quot;:      map[string]interface{}{},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf(&quot;Failed to marshal JSON: %v\n&quot;, err)
		return
	}

	// 创建 HTTP POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf(&quot;Failed to create request: %v\n&quot;, err)
		return
	}

	// 设置请求头
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	client := &amp;http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf(&quot;Failed to send request: %v\n&quot;, err)
		return
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf(&quot;Failed to read response: %v\n&quot;, err)
		return
	}

	// 处理响应
	if resp.StatusCode == http.StatusOK {
		fmt.Println(&quot;Request successful:&quot;)
		fmt.Println(string(body))
	} else {
		fmt.Printf(&quot;Request failed with status code: %d\n&quot;, resp.StatusCode)
		fmt.Println(string(body))
	}
}
</code></pre><strong>Base64 编码示例</strong><a id="code-block-92"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/base64&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

func main() {
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	appId := &quot;APP_ID&quot;

	imageData, _ := os.ReadFile(&quot;/path/to/your/image.jpeg&quot;)
	base64Image := base64.StdEncoding.EncodeToString(imageData)
	dataUrl := fmt.Sprintf(&quot;data:image/jpeg;base64,%s&quot;, base64Image)

	requestBody := map[string]interface{}{
		&quot;input&quot;: map[string]interface{}{&quot;prompt&quot;: &quot;这张图片里有什么？&quot;, &quot;image_list&quot;: []string{dataUrl}},
	}

	jsonData, _ := json.Marshal(requestBody)
	req, _ := http.NewRequest(&quot;POST&quot;, fmt.Sprintf(&quot;https://dashscope.aliyuncs.com/api/v1/apps/%s/completion&quot;, appId), bytes.NewBuffer(jsonData))
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	client := &amp;http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Println(string(body))
}
</code></pre></section></section></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f304e81314ngo"></a><h3>响应对象</h3><p><strong>status_code</strong> <code>string</code></p><p>返回的HTTP状态码（仅HTTP调用时出现在响应中）。</p><p>200表示请求成功，否则表示请求失败。</p><blockquote><p>Python SDK 与 Java SDK 调用失败时均会抛出异常，可从异常属性 <code>e.status_code</code>/<code>e.code</code>/<code>e.message</code> 获取状态码、错误码与错误详细信息。</p></blockquote><p><strong>request_id</strong> <code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<code>requestId</code>。</p></blockquote><p><strong>code</strong> <code>string</code></p><p>表示错误码，调用成功时为空值（仅HTTP响应体中返回）。</p><blockquote><p>SDK 调用失败时，错误码通过 <code>DashScopeError</code> 异常（Java 为 <code>ApiException</code>）的 <code>code</code> 属性返回。</p></blockquote><p><strong>message</strong> <code>string</code></p><p>表示错误详细信息，请求成功则忽略（仅HTTP响应体中返回）。</p><blockquote><p>SDK 调用失败时，错误信息通过 <code>DashScopeError</code> 异常（Java 为 <code>ApiException</code>）的 <code>message</code> 属性返回。</p></blockquote><p><strong>output</strong> <code>object</code></p><p>调用结果信息。</p><a id="accordion-output属性"></a><section><p>output属性</p><div><p><strong>text</strong> <code>string</code></p><p>模型生成的回复内容。</p><p><strong>finish_reason</strong> <code>string</code></p><p>完成原因。</p><p><code>stop</code>为自然结束（遇预设标记），<code>null</code>为强制中断（如达到最大长度限制或手动停止）。</p><p><strong>session_id</strong><code>string</code></p><p>当前对话的唯一标识。</p><p>在后续请求中传入，可携带历史对话记录。</p><p><strong>thoughts</strong><code>array</code></p><p>调用时将<code>has_thoughts</code>参数设置为True，即可在<code>thoughts</code>中查看插件调用、知识检索的过程，或<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>的思考过程。</p><a id="accordion-thoughts属性"></a><section><p>thoughts属性</p><div><p><strong>thought</strong> <code>string</code></p><p>模型的思考过程。</p><p>当在控制台<strong>智能体应用</strong>中选择了<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>，并成功发布应用后，若在 API 调用时将 <code>has_thoughts</code> 参数设为 <code>True</code>，则模型的思考过程将在此字段中返回。</p><p><strong>reasoningContent</strong><code>string</code></p><p>模型的思考过程。</p><p>当在控制台<strong>工作流应用</strong>中选择了<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>，并成功发布应用后，若在 API 调用时将 <code>has_thoughts</code> 参数设为 <code>True</code>，则模型的思考过程将在此字段中返回。</p><p><strong>action_type</strong> <code>string</code></p><p>大模型返回的执行步骤类型。如API表示执行API插件、agentRag表示执行知识检索、reasoning表示执行<a href="../model-user-guide/model-experience/text-generation-model/deep-thinking.md">深度思考模型</a>的思考过程。</p><p><strong>action_name</strong> <code>string</code></p><p>执行的action名称，如知识检索、API插件、思考过程。</p><p><strong>action</strong> <code>string</code></p><p>执行的步骤。</p><p><strong>action_input_stream</strong> <code>string</code></p><p>入参的流式结果。</p><p><strong>action_input</strong> <code>string</code></p><p>插件的输入参数。</p><p><strong>observation</strong> <code>string</code></p><p>检索或插件的过程。</p></div></section><p><strong>doc_references</strong> <code>array</code></p><p>检索的召回文档中被模型引用的文档信息。</p><p>在百炼控制台的<strong>智能体应用</strong>内，打开<strong>展示回答来源</strong>开关并<strong>发布</strong>应用，<code>doc_references</code>才可能包含有效信息。</p><a id="accordion-doc-references属性"></a><section><p>doc_references属性</p><div><p><strong>index_id</strong> <code>string</code></p><p>模型引用的召回文档索引，如[1]。</p><p><strong>title</strong> <code>string</code></p><p>模型引用的文本切片标题。</p><p><strong>doc_id</strong> <code>string</code></p><p>模型引用的文档ID。</p><p><strong>doc_name</strong> <code>string</code></p><p>模型引用的文档名。</p><p><strong>doc_url</strong> <code>string</code></p><p>模型引用的文档链接，若文档保存于阿里云百炼平台的安全存储空间中时为<code>null</code>。</p><p><strong>text</strong> <code>string</code></p><p>模型引用的具体文本内容。</p><p><strong>biz_id</strong> <code>string</code></p><p>模型引用的业务关联标识。</p><p><strong>images</strong> <code>array</code></p><p>模型引用的图片URL列表。</p><p><strong>page_number</strong><code>array</code></p><p>模型引用的文本切片的页码。</p><blockquote><p>此参数仅支持在2024年10月25日后创建的知识库。</p></blockquote><blockquote><p>如需使用该参数，Python Dashscope SDK的版本至少应为2.0.1；Java Dashscope SDK的版本至少应为2.16.10。</p></blockquote></div></section><p><strong>workflow_message</strong><code>object</code></p><p>包含工作流节点状态和消息的对象。</p><div><div><p><strong>说明</strong><strong>工作流应用特有输出字段</strong>：</p><ul><li>此字段<strong>仅在调用工作流应用</strong>时返回，智能体应用不会返回此字段。</li><li>在流式输出模式下，当<code>flow_stream_mode</code>设置为<code>message_format</code>或<code>message_format_plus</code>时，此字段会实时返回工作流各节点的执行状态和消息。</li><li>在非流式输出模式下，此字段返回最终节点（<strong>结束</strong>节点或<strong>流程输出</strong>节点）的状态和消息。</li></ul><p><strong>与智能体应用的输出区别</strong>：</p><ul><li><strong>智能体应用</strong>：主要通过<code>output.text</code>字段返回最终回复，<code>thoughts</code>字段（需<code>has_thoughts=true</code>）返回插件调用和知识检索过程。</li><li><strong>工作流应用</strong>：除了<code>output.text</code>外，还通过<code>workflow_message</code>字段返回工作流节点的详细执行信息，包括节点名称、类型、状态和每个节点的输出内容。</li></ul></div></div><a id="accordion-workflow-message属性"></a><section><p>workflow_message属性</p><div><p><strong>node_status</strong><code>string</code></p><p>当前节点的执行状态，例如 executing（执行中）。</p><p><strong>node_type</strong><code>string</code></p><p>当前节点的类型，例如End（结束节点）。</p><p><strong>node_msg_seq_id</strong><code>integer</code></p><p>节点内消息的序列号。</p><p><strong>node_name</strong><code>string</code></p><p>当前节点的名称，例如结束。</p><p><strong>message</strong><code>object</code></p><p>包含具体消息内容的对象。</p><a id="accordion-message属性"></a><section><p>message属性</p><div><p><strong>content</strong><code>string</code></p><p>消息的具体文本内容。</p><p><strong>role</strong><code>string</code></p><p>消息发送者的角色，例如Assistant。</p></div></section><p><strong>node_is_completed</strong><code>boolean</code></p><p>指示当前节点是否已完成执行。true表示完成，false 表示未完成。</p><p><strong>node_id</strong><code>string</code></p><p>当前节点的唯一标识ID。</p><p><strong>parent_node_id</strong><code>string</code></p><p>当前节点所属父节点（循环节点 / 批处理节点）的 ID。</p><ul><li>主画布节点：返回 null。</li><li>子画布节点：返回所属循环节点或批处理节点的<code>node_id</code>。</li></ul><p>仅<code>message_format_plus</code>模式下子画布节点会返回非空值。</p></div></section><p><strong>子画布节点 content 结构</strong>（<code>message_format_plus</code>）</p><p>当<code>flow_stream_mode=message_format_plus</code>且节点位于子画布内（<code>parent_node_id</code>非空）时，<code>message.content</code>为该次迭代/分支的完整 NodeResult JSON。</p><a id="accordion-子画布节点-content-字段"></a><section><p>子画布节点 content 字段</p><div><p><strong>nodeId</strong><code>string</code></p><p>子画布内节点 ID。</p><p><strong>nodeName</strong><code>string</code></p><p>节点名称。</p><p><strong>nodeType</strong><code>string</code></p><p>节点类型，如 LLM、Plugin、Output 等。</p><p><strong>nodeStatus</strong><code>string</code></p><p>节点执行状态：<code>success</code>（成功）/ <code>fail</code>（失败）/ <code>skip</code>（跳过，未执行）/ <code>executing</code>（执行中）。</p><p><strong>input</strong><code>string</code></p><p>节点输入内容。</p><p><strong>output</strong><code>string</code></p><p>节点输出内容。</p><p><strong>index</strong><code>integer</code></p><p>子画布迭代/分支序号，从 0 起递增。</p><p><strong>parentNodeId</strong><code>string</code></p><p>父节点（循环节点 / 批处理节点）ID。</p><p><strong>nodeExecTime</strong><code>string</code></p><p>节点执行耗时，如<code>100ms</code>。</p><p><strong>errorCode</strong><code>string</code></p><p>节点执行失败时返回。</p><p><strong>errorInfo</strong><code>string</code></p><p>节点执行失败时返回。</p></div></section><div><div><p><strong>说明</strong>文本类节点（Output / End text 模式）和 LLM 等 JSON 类节点的处理规则与主画布一致：文本类是 delta 需拼接，JSON 类是快照需整体替换；<code>node_is_completed=true</code>标记节点结束。</p></div></div></div></section><p><strong>usage</strong> <code>object</code></p><p>表示本次请求使用的数据信息。</p><a id="accordion-usage属性"></a><section><p>usage属性</p><div><p><strong>models</strong><code>array</code></p><p>本次调用的模型信息。</p><a id="accordion-models属性"></a><section><p>models属性</p><div><p><strong>model_id</strong> <code>string</code></p><p>本次应用调用到的模型 ID。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>用户输入文本转换成Token后的长度。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型生成回复转换为Token后的长度。</p></div></section></div></section></td><td><strong>单轮对话响应示例</strong><p>以下为 HTTP 接口返回的原始响应（Python SDK 返回扁平化后的响应对象，可经 <code>response.text</code>/<code>response.finish_reason</code>/<code>response.session_id</code> 直接读取）。</p><a id="code-block-93"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;session_id&quot;: &quot;6105c965c31b40958a43dc93c28c7a59&quot;,
        &quot;text&quot;: &quot;我是千问，由阿里云开发的AI助手。我被设计用来回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？&quot;
    },
    &quot;usage&quot;: {
        &quot;models&quot;: [
            {
                &quot;output_tokens&quot;: 36,
                &quot;model_id&quot;: &quot;qwen-plus&quot;,
                &quot;input_tokens&quot;: 74
            }
        ]
    },
    &quot;request_id&quot;: &quot;f97ee37d-0f9c-9b93-b6bf-bd263a232bf9&quot;
}
</code></pre><strong>指定知识库响应示例</strong><p>调用应用知识库功能时，想要输出召回文档中被模型引用的文档信息，可在百炼控制台的<strong>智能体应用</strong>内，单击<strong>检索配置</strong>，打开<strong>展示回答来源</strong>开关，<strong>发布</strong>应用。</p><p>以下为 Python SDK 2.0 响应对象形态。</p><a id="code-block-94"></a><pre class="language-json"><code>{
    &quot;text&quot;: &quot;根据您的预算，我推荐您考虑百炼 Zephyr Z9。这款手机轻巧便携，拥有6.4英寸1080 x 2340像素的屏幕，搭配128GB存储与6GB RAM，非常适合日常使用&lt;ref&gt;[1]&lt;/ref&gt;。此外，它还配备了4000mAh电池以及30倍数字变焦镜头，能够捕捉远处细节，价格区间在2499-2799元之间，完全符合您的预算需求&lt;ref&gt;[1]&lt;/ref&gt;。&quot;,
    &quot;finish_reason&quot;: &quot;stop&quot;,
    &quot;session_id&quot;: &quot;6c1d47fa5eca46b2ad0668c04ccfbf13&quot;,
    &quot;thoughts&quot;: null,
    &quot;doc_references&quot;: [
        {
            &quot;index_id&quot;: &quot;1&quot;,
            &quot;title&quot;: &quot;百炼手机产品介绍&quot;,
            &quot;doc_id&quot;: &quot;file_7c0e9abee4f142f386e488c9baa9cf38_10317360&quot;,
            &quot;doc_name&quot;: &quot;百炼系列手机产品介绍&quot;,
            &quot;doc_url&quot;: null,
            &quot;text&quot;: &quot;【文档名】:百炼系列手机产品介绍\n【标题】:百炼手机产品介绍\n【正文】:参考售价：5999- 6499。百炼 Ace Ultra ——游戏玩家之选：配备 6.67英寸 1080 x 2400像素屏幕，内置 10GB RAM与 256GB存储，确保游戏运行丝滑无阻。百炼 Ace Ultra ——游戏玩家之选：配备 6.67英寸 1080 x 2400像素屏幕，内置 10GB RAM与 256GB存储，确保游戏运行丝滑无阻。5500mAh电池搭配液冷散热系统，长时间游戏也能保持冷静。高动态双扬声器，沉浸式音效升级游戏体验。参考售价：3999- 4299。百炼 Zephyr Z9 ——轻薄便携的艺术：轻巧的 6.4英寸 1080 x 2340像素设计，搭配 128GB存储与 6GB RAM，日常使用游刃有余。4000mAh电池确保一天无忧，30倍数字变焦镜头捕捉远处细节，轻薄而不失强大。参考售价：2499- 2799。百炼 Flex Fold+ ——折叠屏新纪元：集创新与奢华于一身，主屏 7.6英寸 1800 x 2400像素与外屏 4.7英寸 1080 x 2400像素，多角度自由悬停设计，满足不同场景需求。512GB存储、12GB RAM，加之 4700mAh电池与 UTG超薄柔性玻璃，开启折叠屏时代新篇章。此外，这款手机还支持双卡双待、卫星通话，帮助您在世界各地都能畅联通话。参考零售价：9999- 10999。\n&quot;,
            &quot;biz_id&quot;: null,
            &quot;images&quot;: [

            ],
            &quot;page_number&quot;: [
                0]
        }]
}
</code></pre><strong>异常响应示例</strong><p>在访问请求出错的情况下，Python SDK 会抛出异常，异常的 <code>code</code> 和 <code>message</code> 属性会指明错误原因。</p><p>此处展示未传入正确<code>API-KEY</code>的异常响应示例。</p><a id="code-block-95"></a><pre class="language-json"><code>request_id=1d14958f-0498-91a3-9e15-be477971967b,
code=401,
message=Invalid API-key provided.
</code></pre></td></tr></tbody></table>

<a id="qpm限制"></a>

<a id="qpm_limit_h2_workflow"></a>

## QPM限制

应用调用按应用与账号两个维度限流，两个维度独立生效，任一触发都会返回限流错误：

-   **单应用并发**：按应用 ID（`app_id`）统计的每秒请求数，默认上限 **100 QPS**。工作流异步任务的提交请求与同步调用共享该配额。
-   **账号总流量**：同一阿里云主账号维度统计的每分钟请求数，默认上限 **15000 QPM**。

超出阈值的请求会被拒绝并返回 HTTP 429，错误码为 `Throttling.RateQuota`，通常在一分钟内自动恢复。预计业务并发或调用量将大幅上涨时，建议提前联系阿里云对接商务经理评估并申请扩容。

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果调用失败（Python SDK 会抛出 `DashScopeError` 异常，HTTP 调用返回报错信息），请参阅[错误码](../model-api-reference/preparations/error-code.md)进行解决。
