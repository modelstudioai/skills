# Retrieve - 检索知识库

在指定的知识库中检索信息。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   **调用方式**：本页描述 OpenAPI Retrieve 接口 `POST /{WorkspaceId}/index/retrieve`，可通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)并使用阿里云访问密钥 [AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)调用。[Spring AI Alibaba](../application-api-reference/frameworks/spring-ai-alibaba/spring-ai-alibaba-integrate-knowledge-base.md)使用阿里云百炼 [API Key](../model-api-reference/preparations/get-api-key.md)和独立的 DashScope Pipeline Retrieve 路径，不使用本页的 OpenAPI 请求语法。
    
-   权限要求：
    
    -   **RAM 用户（子账号）**：需先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（可使用`AliyunBailianDataFullAccess`策略，该策略已包含本接口所需的 sfm:Retrieve 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，才能调用本接口。
    -   **阿里云账号（主账号）**：默认拥有权限，可直接调用。
-   **响应延迟**：由于接口调用包含复杂的检索和匹配，响应时间可能较长，建议您合理设置请求的超时与重试策略。
    
-   **幂等性**：本接口具有幂等性。
    

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
| sfm:Retrieve | none | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/index/retrieve HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3shx2gu255oqxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>Query</td><td><p>string</p></td><td><p>否</p></td><td><div><p>输入文本（原始输入 prompt）。Query 的长度和字符没有限制。</p></div></td><td><p>阿里云百炼平台介绍</p></td></tr><tr><td>DenseSimilarityTopK</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>向量检索 Top K，通过生成输入文本的向量并在知识库中检索与其向量表示最相似的 K 个文本切片。K 的取值范围[0-100]。 <code>DenseSimilarityTopK</code>和<code>SparseSimilarityTopK</code>二者之和小于等于 200。</p><p>默认值为 100。</p></div></td><td><p>100</p></td></tr><tr><td>EnableReranking</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否开启重排序。更多信息，请参见<a href="../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md">知识库</a>。取值范围：</p><ul><li><p>true：开启。</p></li><li><p>false：不开启。</p></li></ul><p>默认值为 true。</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>开启</p></div></li><li>false :<div><p>不开启</p></div></li></ul></div></td><td><p>true</p></td></tr><tr><td>EnableRewrite</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否开启<a href="https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji">多轮对话改写</a>。 取值范围：</p><ul><li><p>true：开启。</p></li><li><p>false：不开启。</p></li></ul><p>默认值为 false。</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>开启</p></div></li><li>false :<div><p>不开启</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>Rerank</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>重排序配置。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>重排序配置对象。</p></div></td><td></td></tr><tr><td>ModelName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>使用指定的排序模型。此处指定值将覆盖创建知识库时所选择的排序模型。取值范围：</p><ul><li><p>qwen3-rerank-hybrid：qwen3-rerank(hybrid)排序。</p></li><li><p>qwen3-rerank：qwen3-rerank 排序。</p></li><li><p>gte-rerank-hybrid：gte-rerank(hybrid)排序。</p></li><li><p>gte-rerank：gte-rerank 排序。</p></li></ul><p>默认值为空，使用创建知识库时选择的排序模型。</p><div><p>如仅需语义排序，可使用<code>qwen3-rerank</code>；若同时需要语义排序和文本匹配特征以确保相关性，建议使用<code>qwen3-rerank-hybrid</code>。</p></div><div><p><code>gte-rerank-hybrid</code>与<code>gte-rerank</code>后续停止更新，不建议使用。</p></div></div><div><p><strong>枚举值：</strong></p><ul><li>gte-rerank-hybrid :<div><p>gte-rerank(hybrid)排序</p></div></li><li>gte-rerank :<div><p>gte-rerank 排序</p></div></li></ul></div></td><td><p>gte-rerank-hybrid</p></td></tr><tr><td>RerankMode</td><td><p>string</p></td><td><p>否</p></td><td><div><div><p>指定重排序模型的指令干预模式，以决定其评分偏好。</p><p><strong>可选值：</strong></p><ul><li><p><strong>qa</strong>:（默认值） 问答模式。模型倾向于为能直接回答查询（Query）的候选项赋予更高分。建议在问答场景使用。</p></li><li><p><strong>similar</strong>: 相似模式。模型倾向于为与查询内容一致性高的候选项赋予更高分。建议在匹配检索场景使用。</p></li><li><p><strong>custom</strong>: 自定义模式。模型的排序行为由 rerank_instruct 参数中的指令决定。</p></li></ul></div></div><div><p><strong>枚举值：</strong></p><ul><li>similar: 相似模式。 :<div><p>similar: 相似模式。</p></div></li><li>custom: 自定义模式。 :<div><p>custom: 自定义模式。</p></div></li><li>qa:（默认值） 问答模式。 :<div><p>qa:（默认值） 问答模式。</p></div></li></ul></div></td><td><p>qa</p></td></tr><tr><td>RerankInstruct</td><td><p>string</p></td><td><p>否</p></td><td><div><p>提供一个自然语言指令，用于精细化控制重排序模型的行为。</p><p>此参数仅在 rerank_mode 设置为 &quot;custom&quot; 时生效。</p></div></td><td></td></tr><tr><td>RerankMinScore</td><td><p>number</p></td><td><p>否</p></td><td><div><p>相似度阈值。该阈值表示允许召回的文本切片的最低相似度分数，用于筛选 Rank 模型返回的文本切片，即只有分数超过此数值的文本切片才会被召回。取值范围[0.01-1.00]。此参数的优先级大于知识库相似度阈值配置。</p><p>当未指定具体值时，默认采用该知识库配置的相似度阈值。</p></div></td><td><p>0.20</p></td></tr><tr><td>RerankTopN</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>重排序后的 Top N 返回数据。取值范围[1-20]，默认值为 5。</p></div></td><td><p>5</p></td></tr><tr><td>Rewrite</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>多轮对话改写配置。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>多轮对话改写配置对象。</p></div></td><td></td></tr><tr><td>ModelName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>多轮对话改写模型名称。它会基于会话上下文自动调整原始输入 prompt（用户问题）以提升检索效果。取值范围：</p><ul><li><p>conv-rewrite-qwen-1.8b：conv-rewrite-qwen-1.8b 模型（目前只支持该模型）</p></li></ul><p>默认值为空，采用 conv-rewrite-qwen-1.8b 模型。</p></div><div><p><strong>枚举值：</strong></p><ul><li>conv-rewrite-qwen-1.8b :<div><p>conv-rewrite-qwen-1.8b 模型</p></div></li></ul></div></td><td><p>conv-rewrite-qwen-1.8b</p></td></tr><tr><td>SparseSimilarityTopK</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>关键词检索 TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果。 取值范围[0-100]。 <code>DenseSimilarityTopK</code>和<code>SparseSimilarityTopK</code>二者之和小于等于 200。</p><p>默认值为：100。</p></div></td><td><p>100</p></td></tr><tr><td>IndexId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>知识库 ID，即 <strong>CreateIndex</strong> 接口返回的<code>Data.Id</code>。</p><div><ul><li><p>请确保对应知识库已成功创建且未被删除。</p></li></ul></div></div></td><td><p>5pwe0mxxxx</p></td></tr><tr><td>SaveRetrieverHistory</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否保存历史文本切片召回测试数据。取值范围：</p><ul><li><p>true：保存。</p></li><li><p>false：不保存。</p></li></ul><p>默认值为：false。</p></div></td><td><p>false</p></td></tr><tr><td>SearchFilters</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>支持通过 SearchFilters 设置个性化的检索条件（比如标签），对语义检索结果进行过滤，以排除与查询 Query 无关的信息。数组中的条件对象之间采用 AND 关系。同一对象内的多个检索字段默认采用 AND 关系；将 <code>_operator</code> 与检索字段放在同一对象中，并设为 <code>OR</code>（也支持 <code>or</code>），可匹配任一字段条件；设为 <code>AND</code> 则需同时满足所有字段条件。设置 is_displayed_chunk_content 参数为 true 生效筛选逻辑，具体内容请参见<a href="../application-api-reference/more/how-to-use-search-filters.md">知识库 SearchFilters</a>。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>检索条件对象。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Images</td><td><p>array</p></td><td><p>否</p></td><td><div><p>支持在提问时传入图片 URL 地址。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><div><p>检索图片问答类知识库时您可传入图片 URL 地址。当该知识库中存在图片索引时，系统会将输入图片转为向量并检索到相关记录；如果不存在图片索引，则输入的图片不会用于检索。</p><div><p>本字段不支持文档搜索/数据查询/音视频搜索类知识库（即使传入也不生效）</p></div><div><p>请确保链接公开可访问且指向一个有效的图片文件。格式示例：<a href="https://example.com/downloads/pic.jpg">https://example.com/downloads/pic.jpg</a></p></div></div></div></td><td><p><a href="https://example.com/downloads/pic.jpg">https://example.com/downloads/pic.jpg</a></p></td></tr><tr><td>QueryHistory</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p><a href="https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji">多轮对话改写</a>支持您传入自己管理的对话历史。仅在 EnableRewrite=<strong>true</strong> 时生效（否则即使传入也不生效）。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>role</td><td><p>string</p></td><td><p>否</p></td><td><div><p>角色。</p><p>取值范围：</p><ul><li><p>user：传入此角色，此时 content 表示您输入给阿里云百炼应用的文本。</p></li><li><p>assistant：传入此角色，此时 content 表示阿里云百炼应用的回复。</p></li></ul></div></td><td><p>user</p></td></tr><tr><td>content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>对应角色的问题或者回答内容。</p></div></td><td><p>代表一段文本。</p></td></tr><tr><td>Extra</td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>uniqueId</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr></tbody></table>

例如，以下 `SearchFilters` 筛选文档名称为“长上下文Qwen-Long”或切片标题为“返回结果”的切片。将字段和值替换为知识库中实际可检索的字段和值：

<a id="code-block-2"></a>

```json
[
  {
    "_operator": "OR",
    "doc_name": "长上下文Qwen-Long",
    "title": "返回结果"
  }
]
```

> **说明**
>
> 本页 OpenAPI Retrieve 接口及其 SDK 的 `SearchFilters` 使用字符串值 Map，不支持嵌套 `_conditions`。传入嵌套结构时，请求可能仍返回成功响应，但不会按嵌套条件过滤。如需对同一字段设置多个 OR 条件，请使用 RAG API JSON 请求体，或通过 Spring AI Alibaba DashScope SDK 的 `/api/v1/indices/pipeline/{pipeline_id}/retrieve` 路径调用。两种调用方式均支持 `_operator` 和嵌套 `_conditions`，具体语法和示例请参见[知识库 SearchFilters](../application-api-reference/more/how-to-use-search-filters.md)。

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>Index.InvalidParameter</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口业务数据字段。</p></div></td><td></td></tr><tr><td>Nodes</td><td><p>array&lt;object&gt;</p></td><td><div><p>命中的文本切片列表。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>文本切片对象。</p></div></td><td></td></tr><tr><td>Metadata</td><td><p>any</p></td><td><div><div><p>文本切片的元数据 Map。</p><div><p>文档搜索类知识库的元数据 Map 中<code>file_path</code>字段无意义，请勿在业务代码中使用。</p></div><div><p>检索文档搜索类识库时，若切片包含图片，将通过元数据 Map 中<code>image_url</code>字段透出，并附有过期时间。</p></div><div><p>检索音视频搜索类知识库时，若切片包含音频，将通过元数据 Map 中<code>audio_url</code>字段透出，并附有过期时间。</p></div><div><p>检索音视频搜索类知识库时，若切片包含视频，将通过元数据 Map 中<code>video_url</code>字段透出，并附有过期时间。</p></div></div></div></td><td><p>{ &quot;parent&quot;: &quot;&quot;, &quot;file_path&quot;: &quot;https://***&quot;, &quot;image_url&quot;: [ &quot;http://***&quot; ], &quot;nid&quot;: &quot;***&quot;, &quot;title&quot;: &quot;阿里云百炼文档&quot;, &quot;doc_id&quot;: &quot;doc_***&quot;, &quot;content&quot;: &quot;阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建&quot;, &quot;workspace_id&quot;: &quot;ws_***&quot;, &quot;hier_title&quot;: &quot;阿里云百炼文档&quot;, &quot;doc_name&quot;: &quot;阿里云百炼文档介绍.pdpf&quot;, &quot;pipeline_id&quot;: &quot;rhd***&quot;, &quot;_id&quot;: &quot;ws_***&quot; }</p></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>文本切片的相似度得分，可能值范围：[0-1]。</p></div></td><td><p>0.3</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>文本切片内容。</p></div></td><td><p>阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建。</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>17204B98-7734-4F9A-8464-2446A84821CA</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```json
{
  "Code": "Index.InvalidParameter",
  "Data": {
    "Nodes": [
      {
        "Metadata": "{\n  \"parent\": \"\",\n  \"file_path\": \"https://***\",\n  \"image_url\": [\n    \"http://***\"\n  ],\n  \"nid\": \"***\",\n  \"title\": \"阿里云百炼文档\",\n  \"doc_id\": \"doc_***\",\n  \"content\": \"阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建\",\n  \"workspace_id\": \"ws_***\",\n  \"hier_title\": \"阿里云百炼文档\",\n  \"doc_name\": \"阿里云百炼文档介绍.pdpf\",\n  \"pipeline_id\": \"rhd***\",\n  \"_id\": \"ws_***\"\n}",
        "Score": 0.3,
        "Text": "阿里云百炼是基于通义大模型、行业大模型以及三方大模型的一站式大模型开发平台。面向企业客户和个人开发者，提供完整的模型服务工具和全链路应用开发套件，预置丰富的能力插件，提供API及SDK等便捷的集成方式，高效完成大模型应用构建。"
      }
    ]
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-7734-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/Retrieve#workbench-doc-change-demo)。
