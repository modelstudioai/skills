# RunSearchGeneration

AI妙搜-智能搜索生成：对应妙搜首页的搜索生成能力。此接口支持通用搜索和媒资搜索。支持用户问题澄清、多模态知识搜索、多agent生成等能力。 - 通用搜索：可以对数据集中知识进行语义检索，并对搜索结果进行多agent后处理，包括总结生成、摘编、时间线总结等。 - 媒资搜索：应搜尽搜，全文检索，召回更多相关知识，并可进行多agent后处理，包括聚类、新闻抽取等。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

<a id="接入说明"></a>

### 接入说明：

-   当前接口为 http-sse 协议。
-   由于 OpenAPI 门户目前对 SSE 推理协议不兼容（无法直接调试），接口 SDK 方式调用示例（支持**java、python**版本的 **sdk**）请参考[妙搜最佳实践](https://help.aliyun.com/zh/model-studio/user-guide/best-practices-for-miaosou-api/?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_1_2.42a64a34eIyBhn)文档。
-   其中获取 Java 异步 SDK 的最新版本：请点击[链接](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)获取。

<a id="搜索数据来源"></a>

### 搜索数据来源：

支持三种类型数据集：详见[妙搜最佳实践](https://help.aliyun.com/zh/model-studio/user-guide/best-practices-for-miaosou-api/?spm=a2c4g.11186623.help-menu-2400256.d_1_3_3_2_1_2.42a64a34eIyBhn)

-   内置”互联网检索“数据集：支持互联网开放域文本、图片、视频（暂未开放）的搜索；
-   语义（RAG）数据集：可以管理企业私域知识库，支持文本、图片、视频、语音（暂未开放）；
-   三方 api 数据集：可以直接集成企业自己的搜索 api。

<a id="权限说明"></a>

## 权限说明

<a id="前置条件"></a>

### 前置条件

-   登录阿里云百炼控制台，确认阿里云百炼是开通可用状态。
-   主账号调用：默认有所有 API 调用权限。
-   子账号调用：子账号默认无权限（AccessForbid）调用当前 API，需要同时在 **RAM 控制台**和**阿里云百炼控制台**中做授权。

<a id="ram-控制台授权说明"></a>

### RAM 控制台授权说明

去 [RAM 控制台](https://ram.console.aliyun.com/users)授权，具体 RAM 授权操作，参考 [RAM 文档](https://help.aliyun.com/zh/ram/user-guide/create-a-custom-policy)，步骤如下：

<a id="授予内置权限策略"></a>

#### 授予内置权限策略

授予子账号” [AliyunAiMiaoBiFullAccess](https://ram.console.aliyun.com/policies/detail?policyType=System&policyName=AliyunAiMiaoBiFullAccess) “ 权限。

<a id="阿里云百炼控制台授权说明"></a>

### 阿里云百炼控制台授权说明

使用主账号或有阿里云百炼管理员权限的子账号，登录阿里云百炼控制台，在[权限管理](https://bailian.console.aliyun.com/?tab=app#/authority)页面添加子账号“新增用户”。

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
| aimiaobi:RunSearchGeneration | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/aimiaosou/runSearchGeneration HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>WorkspaceId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>阿里云百炼业务空间 ID。获取方式请参见<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">如何使用业务空间</a>。</p></td><td><p>llm-xxx</p></td></tr><tr><td><p>TaskId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>会话任务唯一标识</p><div><div><p><strong>说明</strong>TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</p></div></div></td><td><p>7AA2AE16-D873-5C5F-9708-15396C382EB1</p></td></tr><tr><td><p>Prompt</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索词</p></td><td><p>杭州亚运会吉祥物是什么</p></td></tr><tr><td><p>OriginalSessionId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>原会话唯一标识：通常为空，非空时，表示当前对话基于此轮对话生成，会加载原始轮对话参数，搜索结果等，同时会替换生成结果，适用于，重新生成、修改数据源、新增 agent 生成场景</p></td><td><p>xxx</p></td></tr><tr><td><p>ChatConfig</p></td><td><p>object</p></td><td><p>否</p></td><td><p>会话配置信息</p></td><td><p>xxx</p></td></tr><tr><td><p>GenerateTechnology</p></td><td><p>string</p></td><td><p>否</p></td><td><p>生成技术：</p><ul><li>copilotReference：问答式搜索</li><li>copilotPrecise：纯搜索</li></ul><strong>枚举值：</strong><ul><li><p>copilotPrecise :</p><p>copilotPrecise</p></li><li><p>copilotReference :</p><p>copilotReference</p></li></ul></td><td><p>copilotReference</p></td></tr><tr><td><p>SearchParam</p></td><td><p>object</p></td><td><p>否</p></td><td><p>搜索参数</p></td><td></td></tr><tr><td><p>StartTime</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>开始时间</p></td><td><p>1725983999999</p></td></tr><tr><td><p>EndTime</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>结束时间</p></td><td><p>1725983999999</p></td></tr><tr><td><p>SearchSources</p></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><p>搜索源列表</p></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>搜索源：</p><p>Code、DatasetName 两个字段必传，来唯一标识一个搜索源。</p><p>内置互联网搜索对应：</p><ul><li>Code=SystemSearch</li><li>DatasetName=QuarkCommonNews</li></ul></td><td></td></tr><tr><td><p>Code</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索源类型：</p><ul><li>SystemSearch：系统内置搜索</li><li>CustomSemanticSearch：自建语义索引搜索</li><li>ThirdSearch：三方 API 搜索</li></ul><strong>枚举值：</strong><ul><li><p>SystemSearch :</p><p>SystemSearch</p></li><li><p>ThirdSearch :</p><p>ThirdSearch</p></li><li><p>CustomSemanticSearch :</p><p>CustomSemanticSearch</p></li></ul></td><td><p>SystemSearch</p></td></tr><tr><td><p>DatasetName</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索源唯一标识：对应页面数据集名称，比如 4cb0eda3fad841758262dbe8d61191</p></td><td><p>QuarkCommonNews</p></td></tr><tr><td><p>MultimodalSearchTypes</p></td><td><p>array</p></td><td><p>否</p></td><td><p>搜索范围列表</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索范围：</p><ul><li>text：文档</li><li>image：图片</li><li>audio：音频</li><li>video：视频</li></ul><strong>枚举值：</strong><ul><li><p>image :</p><p>image</p></li><li><p>text :</p><p>text</p></li><li><p>video :</p><p>video</p></li></ul></td><td><p>text</p></td></tr><tr><td><p>SearchTextMinScore</p></td><td><p>number</p></td><td><p>否</p></td><td><p>文本搜索阈值：仅自建数据源(0, 1)</p></td><td><p>0.66</p></td></tr><tr><td><p>SearchImageMinScore</p></td><td><p>number</p></td><td><p>否</p></td><td><p>图片搜索阈值：仅自建数据源(0, 1)</p></td><td><p>0.66</p></td></tr><tr><td><p>SearchVideoMinScore</p></td><td><p>number</p></td><td><p>否</p></td><td><p>视频搜索阈值：仅自建数据源(0, 1)</p></td><td><p>0.66</p></td></tr><tr><td><p>SearchAudioMinScore</p></td><td><p>number</p></td><td><p>否</p></td><td><p>语音搜索阈值：仅自建数据源(0, 1)</p></td><td><p>0.66</p></td></tr><tr><td><p>CategoryUuids</p></td><td><p>array</p></td><td><p>否</p></td><td><p>类目唯一标识</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>类目唯一标识</p></td><td><p>xx</p></td></tr><tr><td><p>Tags</p></td><td><p>array</p></td><td><p>否</p></td><td><p>标签</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>标签</p></td><td><p>xx</p></td></tr><tr><td><p>Extend1</p></td><td><p>string</p></td><td><p>否</p></td><td><p>扩展字段 1</p></td><td><p>xxx</p></td></tr><tr><td><p>Extend2</p></td><td><p>string</p></td><td><p>否</p></td><td><p>扩展字段 2</p></td><td><p>xxx</p></td></tr><tr><td><p>Extend3</p></td><td><p>string</p></td><td><p>否</p></td><td><p>扩展字段 3</p></td><td><p>xxx</p></td></tr><tr><td><p>CreateTimeStart</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>起始创建时间，时间戳形式。</p></td><td><p>111111111111</p></td></tr><tr><td><p>CreateTimeEnd</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>截止创建时间，时间戳形式。</p></td><td><p>111111111111</p></td></tr><tr><td><p>DocIds</p></td><td><p>array</p></td><td><p>否</p></td><td><p>文档 ID 数组</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>文档 ID</p></td><td><p>x</p></td></tr><tr><td><p>DocUuids</p></td><td><p>array</p></td><td><p>否</p></td><td><p>文档唯一标识</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>文档唯一标识</p></td><td><p>x</p></td></tr><tr><td><p>SearchModels</p></td><td><p>array</p></td><td><p>否</p></td><td><p>搜索类型列表</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索类型：</p><ul><li>TextGenerate：总结生成答案（默认）</li><li>ExcerptGenerate：用原文语句回答</li><li>TimelineGenerate：按时间线总结</li><li>PreciseSearch：纯搜索（追问）</li><li>ClusterGenerate：聚类</li><li>ExtractNewsElementGenerate：抽取新闻要素</li></ul><strong>枚举值：</strong><ul><li><p>TextGenerate :</p><p>TextGenerate</p></li><li><p>ExtractNewsElementGenerate :</p><p>ExtractNewsElementGenerate</p></li><li><p>ClusterGenerate :</p><p>ClusterGenerate</p></li><li><p>TimelineGenerate :</p><p>TimelineGenerate</p></li><li><p>ExcerptGenerate :</p><p>ExcerptGenerate</p></li></ul></td><td><p>TextGenerate</p></td></tr><tr><td><p>GenerateLevel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>回答的详细程度：</p><ul><li>concise：简洁（默认）</li><li>enhance：增强</li><li>free：自由</li><li>deepResearch：研究</li></ul><strong>枚举值：</strong><ul><li><p>concise :</p><p>concise</p></li><li><p>enhance :</p><p>enhance</p></li></ul></td><td><p>concise</p></td></tr><tr><td><p>EnableThinking</p></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否开启思考</p></td><td><p>false</p></td></tr><tr><td><p>ExcludeGenerateOptions</p></td><td><p>array</p></td><td><p>否</p></td><td><p>跳过的生成选项列表</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>跳过的生成选项</p><ul><li>think(query 改写)</li><li>multimodalSearchThink（多模态搜索思考）</li><li>queryRecommend（query 推荐）</li></ul></td><td><p>think</p></td></tr><tr><td><p>ModelCustomPromptTemplate</p></td><td><p>string</p></td><td><p>否</p></td><td><p>问答式搜索-总结生成答案-纯文本 prompt 模版，必须包含变量 query、content，比如：</p><a id="code-block-2"></a><pre class="language-text"><code># 角色
你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。

# 任务目标
请你根据检索到的相关文章，回答或表述用户问题“{query}”。

# 任务限制
- 如果用户问题中提到具体日期，请考虑知识日期做筛选。
- 生成内容结构条理。
- 生成内容尽量精简。
- 不要使用其他数据，不要杜撰。
- 如果不能回答用户问题，请输出对应语言的拒识文案:
  - 中文：&quot;根据已知信息无法回答。&quot;
  - 英文：&quot;Unable to answer based on the known information.&quot;

# 输入数据
## 检索到的相关文章
{content}
</code></pre></td><td><h1>角色</h1><p>你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。</p><h1>任务目标</h1><p>请你根据检索到的相关文章，回答或表述用户问题“{query}”。</p><h1>任务限制</h1><ul><li>如果用户问题中提到具体日期，请考虑知识日期做筛选。</li><li>生成内容结构条理。</li><li>生成内容尽量精简。</li><li>不要使用其他数据，不要杜撰。</li><li>如果不能回答用户问题，请输出对应语言的拒识文案:<ul><li>中文：&quot;根据已知信息无法回答。&quot;</li><li>英文：&quot;Unable to answer based on the known information.&quot;</li></ul></li></ul><h1>输入数据</h1><h2>检索到的相关文章</h2><p>{content}</p></td></tr><tr><td><p>ModelCustomVlPromptTemplate</p></td><td><p>string</p></td><td><p>否</p></td><td><p>问答式搜索-总结生成答案-纯文本 prompt 模版，必须包含变量 query、content，比如：</p><a id="code-block-3"></a><pre class="language-text"><code># 角色
你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。

# 任务目标
请你根据检索到的相关文章和图片，回答或表述用户问题“{query}”。

# 任务限制
- 如果用户问题中提到具体日期，请考虑知识日期做筛选。
- 生成内容结构条理。
- 生成内容尽量精简。
- 如果图片内容可以回答，可以忽略文章内容。
- 不要使用其他数据，不要杜撰。
- 如果不能回答用户问题，请输出对应语言的拒识文案:
    - 中文：&quot;根据已知信息无法回答。&quot;
    - 英文：&quot;Unable to answer based on the known information.&quot;

# 输入数据
## 检索到的相关文章
{content}
</code></pre></td><td><h1>角色</h1><p>你是一个专业的文章检索和问答专家，擅长文章检索和回答用户问题。</p><h1>任务目标</h1><p>请你根据检索到的相关文章和图片，回答或表述用户问题“{query}”。</p><h1>任务限制</h1><ul><li>如果用户问题中提到具体日期，请考虑知识日期做筛选。</li><li>生成内容结构条理。</li><li>生成内容尽量精简。</li><li>如果图片内容可以回答，可以忽略文章内容。</li><li>不要使用其他数据，不要杜撰。</li><li>如果不能回答用户问题，请输出对应语言的拒识文案:<ul><li>中文：&quot;根据已知信息无法回答。&quot;</li><li>英文：&quot;Unable to answer based on the known information.&quot;</li></ul></li></ul><h1>输入数据</h1><h2>检索到的相关文章</h2><p>{content}</p></td></tr><tr><td><p>AgentContext</p></td><td><p>object</p></td><td><p>否</p></td><td><p>上下文</p></td><td></td></tr><tr><td><p>BizContext</p></td><td><p>object</p></td><td><p>否</p></td><td><p>业务上下文</p></td><td></td></tr><tr><td><p>MultimodalMediaSelection</p></td><td><p>object</p></td><td><p>否</p></td><td><p>用户输入或选中的多模态数据</p></td><td></td></tr><tr><td><p>SelectionType</p></td><td><p>string</p></td><td><p>否</p></td><td><p>参照数据来源类型，取值范围： ‒ 全量的：all，历史会话中取全量数据，仅支持聚类场景； ‒ 选中的：selected，生成时，会取 textSearchResult 中数据；</p></td><td><p>all</p></td></tr><tr><td><p>SessionId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>生成参照会话唯一标识：搜索生成时当前对话下取数据，比如聚类，目前仅媒资搜索场景-聚类需要</p></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td><p>OriginalSessionId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>原始会话唯一标识：搜索结果取这个会话中的全量，目前仅媒资搜索场景需要</p></td><td><p>原始会话唯一标识：搜索结果取这个会话中的全量，目前仅媒资搜索场景需要</p></td></tr><tr><td><p>SearchModel</p></td><td><p>string</p></td><td><p>否</p></td><td><p>仅聚类，对聚类子类内容二次聚类时传入，ClusterGenerate</p></td><td><p>TextGenerate</p></td></tr><tr><td><p>SearchModelDataValue</p></td><td><p>string</p></td><td><p>否</p></td><td><p>searchModel=ClusterGenerate 时，取子类 topic 名称，注意如果原值有引号时也要带上</p></td><td><p>分类1</p></td></tr><tr><td><p>TextSearchResult</p></td><td><p>object</p></td><td><p>否</p></td><td><p>文本搜索结果</p></td><td></td></tr><tr><td><p>SearchResult</p></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><p>文本搜索结果列表</p></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>文本搜索结果</p></td><td></td></tr><tr><td><p>SearchSourceType</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索信源类型，同 searchSource.code</p></td><td><p>SystemSearch</p></td></tr><tr><td><p>SearchSource</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索信源唯一标识，同 searchSource.datasetName</p></td><td><p>QuarkCommonNews</p></td></tr><tr><td><p>SearchSourceName</p></td><td><p>string</p></td><td><p>否</p></td><td><p>搜索信源名称</p></td><td><p>互联网搜索</p></td></tr><tr><td><p>PubTime</p></td><td><p>string</p></td><td><p>否</p></td><td><p>发布时间</p></td><td><p>2024-11-25 14:25:59</p></td></tr><tr><td><p>Source</p></td><td><p>string</p></td><td><p>否</p></td><td><p>来源</p></td><td><p>新华社</p></td></tr><tr><td><p>Title</p></td><td><p>string</p></td><td><p>否</p></td><td><p>标题</p></td><td><p>文章标题</p></td></tr><tr><td><p>Content</p></td><td><p>string</p></td><td><p>否</p></td><td><p>内容</p></td><td><p>文章内容</p></td></tr><tr><td><p>Url</p></td><td><p>string</p></td><td><p>否</p></td><td><p>文章 URL</p></td><td><p><a href="https://www.example.com/aaa.docx">https://www.example.com/aaa.docx</a></p></td></tr><tr><td><p>Summary</p></td><td><p>string</p></td><td><p>否</p></td><td><p>文章摘要</p></td><td><p>文章摘要</p></td></tr><tr><td><p>DocUuid</p></td><td><p>string</p></td><td><p>否</p></td><td><p>内部文档唯一标识</p></td><td><p>xxx</p></td></tr><tr><td><p>Score</p></td><td><p>number</p></td><td><p>否</p></td><td><p>相关度</p></td><td><p>1</p></td></tr><tr><td><p>Chunks</p></td><td><p>array</p></td><td><p>否</p></td><td><p>相关 chunk</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>片段</p></td><td><p>xx</p></td></tr><tr><td><p>DocId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>文档-自定义的唯一 ID</p></td><td><p>文档-自定义的唯一ID</p></td></tr><tr><td><p>SkipCurrentSupplement</p></td><td><p>boolean</p></td><td><p>否</p></td><td><p>是否跳过反问</p></td><td><p>false</p></td></tr><tr><td><p>AskUser</p></td><td><p>string</p></td><td><p>否</p></td><td><p>反问</p></td><td><p>您想了解关于xx的哪些信息？</p></td></tr><tr><td><p>AskUserKeywords</p></td><td><p>array</p></td><td><p>否</p></td><td><p>反问推荐关键词列表</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>反问推荐关键词</p></td><td><p>xx</p></td></tr><tr><td><p>UserBack</p></td><td><p>string</p></td><td><p>否</p></td><td><p>反问用户反馈</p></td><td><p>地点</p></td></tr><tr><td><p>UserBackKeywords</p></td><td><p>array</p></td><td><p>否</p></td><td><p>反问用户反馈关键词列表</p></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><p>反问用户反馈关键词</p></td><td><p>xx</p></td></tr><tr><td><p>CurrentStep</p></td><td><p>string</p></td><td><p>否</p></td><td><p>当前步骤</p></td><td><p>think</p></td></tr><tr><td><p>NextStep</p></td><td><p>string</p></td><td><p>否</p></td><td><p>下一步</p></td><td><p>generate</p></td></tr><tr><td><p>SupplementDataType</p></td><td><p>string</p></td><td><p>否</p></td><td><p>思考-需要补充的数据类型：searchQuery</p></td><td><p>searchQuery</p></td></tr><tr><td><p>SupplementEnable</p></td><td><p>boolean</p></td><td><p>否</p></td><td><p>思考-是否需要补充</p></td><td><p>true</p></td></tr><tr><td><p>ModelId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>模型 id：</p><ul><li>quanmiao-max：全妙-Max</li><li>quanmiao-plus：全妙-Plus</li></ul></td><td><p>quanmiao-max</p></td></tr><tr><td><p>FileUrl</p></td><td><p>string</p></td><td><p>否</p></td><td><p>图片 url：适用于图搜、图文（prompt）混合搜索生成等场景</p></td><td><p><a href="http://xxxx">http://xxxx</a></p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Payload</td><td><p>object</p></td><td><div><p>响应体</p></div></td><td></td></tr><tr><td>Output</td><td><p>object</p></td><td><div><p>输出</p></div></td><td></td></tr><tr><td>AgentContext</td><td><p>object</p></td><td><div><p>上下文数据</p></div></td><td></td></tr><tr><td>BizContext</td><td><p>object</p></td><td><div><p>业务上下文</p></div></td><td></td></tr><tr><td>CurrentStep</td><td><p>string</p></td><td><div><p>任务当前操作步数。</p></div></td><td><p>start</p></td></tr><tr><td>NextStep</td><td><p>string</p></td><td><div><p>下一步:think、search、generat</p></div></td><td><p>search</p></td></tr><tr><td>GeneratedContent</td><td><p>object</p></td><td><div><p>生成内容</p></div></td><td></td></tr><tr><td>ClusterTopicResult</td><td><p>object</p></td><td><div><p>聚类结果</p></div></td><td></td></tr><tr><td>ClusterTopics</td><td><p>array&lt;object&gt;</p></td><td><div><p>聚类列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>聚类</p></div></td><td></td></tr><tr><td>Topic</td><td><p>string</p></td><td><div><p>主题</p></div></td><td><p>xx</p></td></tr><tr><td>ImageSearchResult</td><td><p>object</p></td><td><div><p>图片搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签。</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>数据集类型</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>数据集唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页码</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>每页记录数</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总记录数</p></div></td><td><p>1</p></td></tr><tr><td>TextSearchResult</td><td><p>object</p></td><td><div><p>文档搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>搜索信源类型，同 searchSource.code</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>搜索信源唯一标识，同 searchSource.datasetName</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间,格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2023-04-04 08:39:09</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>MultimodalMedias</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>多模态信息</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值：</p><ul><li><p>video：视频。</p></li><li><p>image：图片。</p></li></ul></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页码</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>每页记录数</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总数</p></div></td><td><p>1</p></td></tr><tr><td>VideoSearchResult</td><td><p>object</p></td><td><div><p>视频搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>x</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>数据集类型</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>数据集唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>参考置信度</p></div></td><td><p>0.9</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>开始时间</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束时间</p></div></td><td><p>1</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>对应文本，比如 asr 转写结果</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>文本类型：比如 asr</p></div></td><td><p>asr</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页码</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>每页记录数</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总记录数</p></div></td><td><p>1</p></td></tr><tr><td>AudioSearchResult</td><td><p>object</p></td><td><div><p>语音结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>object</p></td><td><div><p>语音结果</p></div></td><td></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>url</p></div></td><td><p>http://xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xxx</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>阈值</p></div></td><td><p>1</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>文本内容</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>类型</p></div></td><td><p>asr</p></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>对应文档</p></div></td><td></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>url</p></div></td><td><p>http://xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>docUuid</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>docId</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索源</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签值。</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>数据集类型</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>数据集唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>大小</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总数</p></div></td><td><p>1</p></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>文本结果</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前 agent 是否生成完成</p></div></td><td><p>true</p></td></tr><tr><td>ExcerptResult</td><td><p>object</p></td><td><div><p>原文语句回答结果</p></div></td><td></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>生成文本</p></div></td><td><p>xx</p></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>TraceabilityId</td><td><p>integer</p></td><td><div><p>溯源定位 id</p></div></td><td><p>1</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>搜索信源类型，同 searchSource.code</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>搜索信源唯一标识，同 searchSource.datasetName</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间,格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2023-04-04 08:39:09</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>正文</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>Excerpt</td><td><p>string</p></td><td><div><p>原文语句回答内容</p></div></td><td><p>xx</p></td></tr><tr><td>Select</td><td><p>boolean</p></td><td><div><p>是否参照</p></div></td><td><p>true</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.99</p></td></tr><tr><td>Chunks</td><td><p>array</p></td><td><div><p>片段列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>片段</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>TextGenerateMultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>配图列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>配图</p></div></td><td></td></tr><tr><td>Start</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>End</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值： video：视频。 image：图片。</p></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>MultimodalMedias</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>多模态信息</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值：</p><ul><li><p>video：视频。</p></li><li><p>image：图片。</p></li></ul></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 URL。</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前 agent 是否生成完成</p></div></td><td><p>true</p></td></tr><tr><td>GenerateLevel</td><td><p>string</p></td><td><div><p>回答的详细程度：</p><ul><li><p>concise：简洁（默认）</p></li><li><p>enhance：增强</p></li></ul></div></td><td><p>concise</p></td></tr><tr><td>ReasonTextGenerate</td><td><p>string</p></td><td><div><p>深度思考内容</p></div></td><td><p>xx</p></td></tr><tr><td>NewsElementResult</td><td><p>object</p></td><td><div><p>新闻抽取结果</p></div></td><td></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>文本生成内容</p></div></td><td><p>x</p></td></tr><tr><td>NewsElementArticleList</td><td><p>array&lt;object&gt;</p></td><td><div><p>新闻抽取列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>新闻抽取</p></div></td><td></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>文本生成内容</p></div></td><td><p>xx</p></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>搜索信源类型，同 searchSource.code</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>搜索信源唯一标识，同 searchSource.datasetName</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间,格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2023-04-04 08:39:09</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>正文</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>Select</td><td><p>boolean</p></td><td><div><p>是否参照</p></div></td><td><p>true</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.99</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>NewsElementList</td><td><p>array&lt;object&gt;</p></td><td><div><p>新闻列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>新闻</p></div></td><td></td></tr><tr><td>Time</td><td><p>string</p></td><td><div><p>时间</p></div></td><td><p>时间</p></td></tr><tr><td>Location</td><td><p>string</p></td><td><div><p>地点</p></div></td><td><p>xx</p></td></tr><tr><td>People</td><td><p>string</p></td><td><div><p>人物</p></div></td><td><p>xx</p></td></tr><tr><td>Event</td><td><p>object</p></td><td><div><p>事件</p></div></td><td><p>task-started</p></td></tr><tr><td>CauseList</td><td><p>array</p></td><td><div><p>原因列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>原因</p></div></td><td><p>xx</p></td></tr><tr><td>ProcessList</td><td><p>array</p></td><td><div><p>经过列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>经过</p></div></td><td><p>xx</p></td></tr><tr><td>ResultList</td><td><p>array</p></td><td><div><p>结果列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>结果</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前 agent 是否生成完成</p></div></td><td><p>true</p></td></tr><tr><td>TextGenerateResult</td><td><p>object</p></td><td><div><p>总结生成答案</p></div></td><td></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>文本生成结果</p></div></td><td><p>xx</p></td></tr><tr><td>TextGenerateMultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>配图列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>配图</p></div></td><td></td></tr><tr><td>Start</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>End</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>MultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索源名称</p></div></td><td><p>xx</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>媒资 ID。</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值： video：视频。 image：图片。</p></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>ReferenceList</td><td><p>array&lt;object&gt;</p></td><td><div><p>参考文章列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>参考文章</p></div></td><td></td></tr><tr><td>TraceabilityId</td><td><p>integer</p></td><td><div><p>溯源定位 id</p></div></td><td><p>1</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>搜索信源类型，同 searchSource.code</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>搜索信源唯一标识，同 searchSource.datasetName</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间，格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2023-04-04 08:39:09</p></td></tr><tr><td>Source</td><td><p>string</p></td><td><div><p>来源</p></div></td><td><p>新华社</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>正文</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>Select</td><td><p>boolean</p></td><td><div><p>是否参照</p></div></td><td><p>true</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.99</p></td></tr><tr><td>Chunks</td><td><p>array</p></td><td><div><p>片段列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>片段</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>MultimodalSearchResultList</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索源名称</p></div></td><td><p>xx</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>媒资 ID。</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值： video：视频。 image：图片。</p></div></td><td><p>image</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.1</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>开始时间</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束时间</p></div></td><td><p>1</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>对应文本，比如 asr 转写结果</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>类型：比如 asr</p></div></td><td><p>asr</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>TimelineDateStr</td><td><p>string</p></td><td><div><p>时间脉络-时间</p></div></td><td><p>时间脉络-时间</p></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>每页条数</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总条数</p></div></td><td><p>1</p></td></tr><tr><td>SearchType</td><td><p>string</p></td><td><div><p>搜索类型</p></div></td><td><p>realtime</p></td></tr><tr><td>SearchQuery</td><td><p>string</p></td><td><div><p>搜索 query</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateTraceability</td><td><p>object</p></td><td><div><p>溯源信息</p></div></td><td></td></tr><tr><td>Duplicate</td><td><p>number</p></td><td><div><p>综合溯源相关度</p></div></td><td><p>0.9</p></td></tr><tr><td>Coordinates</td><td><p>array&lt;object&gt;</p></td><td><div><p>溯源位置列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>溯源位置</p></div></td><td></td></tr><tr><td>GenerateCoordinate</td><td><p>object</p></td><td><div><p>生成文档块的坐标</p></div></td><td></td></tr><tr><td>X</td><td><p>integer</p></td><td><div><p>编号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>Y</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>Z</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>NewsCoordinate</td><td><p>object</p></td><td><div><p>参考文档块的坐标</p></div></td><td></td></tr><tr><td>X</td><td><p>integer</p></td><td><div><p>编号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>Y</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>Z</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>媒资类型</p></div></td><td><p>image</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前 agent 是否生成完成</p></div></td><td><p>true</p></td></tr><tr><td>GenerateLevel</td><td><p>string</p></td><td><div><p>回答的详细程度：</p><ul><li><p>concise：简洁（默认）</p></li><li><p>enhance：增强</p></li></ul></div></td><td><p>concise</p></td></tr><tr><td>ReasonTextGenerate</td><td><p>string</p></td><td><div><p>深度思考内容</p></div></td><td><p>xx</p></td></tr><tr><td>TimelineResult</td><td><p>object</p></td><td><div><p>按时间总结结果</p></div></td><td></td></tr><tr><td>TextGenerate</td><td><p>string</p></td><td><div><p>文本生成结果</p></div></td><td><p>xx</p></td></tr><tr><td>ReferenceList</td><td><p>array&lt;object&gt;</p></td><td><div><p>参考文章列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>参考文章</p></div></td><td></td></tr><tr><td>TraceabilityId</td><td><p>integer</p></td><td><div><p>溯源定位 id</p></div></td><td><p>1</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>搜索信源类型，同 searchSource.code</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>搜索信源唯一标识，同 searchSource.datasetName</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间，格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2023-04-04 08:39:09</p></td></tr><tr><td>Source</td><td><p>string</p></td><td><div><p>来源</p></div></td><td><p>新华社</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>正文</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>Select</td><td><p>boolean</p></td><td><div><p>选择情况</p></div></td><td><p>true</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.99</p></td></tr><tr><td>Chunks</td><td><p>array</p></td><td><div><p>片段列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>片段</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>MultimodalSearchResultList</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值： video：视频。 image：图片。</p></div></td><td><p>image</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>置信度，仅供参考</p></div></td><td><p>0.99</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>开始时间</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束时间</p></div></td><td><p>1</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>对应文本，比如 asr 转写结果</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>类型：比如 asr</p></div></td><td><p>asr</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 URL。</p></div></td><td><p>xx</p></td></tr><tr><td>TimelineDateStr</td><td><p>string</p></td><td><div><p>时间字符串</p></div></td><td><p>2024-09-11</p></td></tr><tr><td>GenerateTraceability</td><td><p>object</p></td><td><div><p>溯源信息</p></div></td><td></td></tr><tr><td>Duplicate</td><td><p>number</p></td><td><div><p>相关度</p></div></td><td><p>0.9</p></td></tr><tr><td>Coordinates</td><td><p>array&lt;object&gt;</p></td><td><div><p>溯源位置</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>溯源位置</p></div></td><td></td></tr><tr><td>GenerateCoordinate</td><td><p>object</p></td><td><div><p>生成文档块的坐标</p></div></td><td></td></tr><tr><td>X</td><td><p>integer</p></td><td><div><p>编号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>Y</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>Z</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>NewsCoordinate</td><td><p>object</p></td><td><div><p>参照文章的坐标</p></div></td><td></td></tr><tr><td>X</td><td><p>integer</p></td><td><div><p>编号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>Y</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>Z</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>媒资类型</p></div></td><td><p>image</p></td></tr><tr><td>TextGenerateMultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>配图列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>配图</p></div></td><td></td></tr><tr><td>Start</td><td><p>integer</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>End</td><td><p>integer</p></td><td><div><p>结束位置</p></div></td><td><p>1</p></td></tr><tr><td>MultimodalMediaList</td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>多模态数据</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xxxx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><div><p>多模态数据文件类型，取值： video：视频。 image：图片。</p></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前 agent 是否生成完成</p></div></td><td><p>true</p></td></tr><tr><td>ReasonTextGenerate</td><td><p>string</p></td><td><div><p>深度思考内容</p></div></td><td><p>xx</p></td></tr><tr><td>VideoSearchResult</td><td><p>object</p></td><td><div><p>视频搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>多模态数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配信息列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>参考置信度</p></div></td><td><p>0.8</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>片段起始时间。</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束时间</p></div></td><td><p>1</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>对应文本，比如 asr 转写结果</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>类型：比如 asr</p></div></td><td><p>asr</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>TraceabilityId</td><td><p>string</p></td><td><div><p>溯源唯一标识</p></div></td><td><p>1</p></td></tr><tr><td>ImageSearchResult</td><td><p>object</p></td><td><div><p>图片搜索结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>文章</p></div></td><td></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索信源名称</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>文章摘要</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>媒体数据唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>文件 url</p></div></td><td><p>xx</p></td></tr><tr><td>TraceabilityId</td><td><p>string</p></td><td><div><p>溯源唯一标识</p></div></td><td><p>1</p></td></tr><tr><td>TextSearchResult</td><td><p>object</p></td><td><div><p>文本文档搜索结果</p></div></td><td></td></tr><tr><td>Current</td><td><p>integer</p></td><td><div><p>当前页</p></div></td><td><p>1</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>当前页大小</p></div></td><td><p>1</p></td></tr><tr><td>Total</td><td><p>integer</p></td><td><div><p>总条数</p></div></td><td><p>1</p></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜素结构</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档业务唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>系统内部文档唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceType</td><td><p>string</p></td><td><div><p>数据源类型</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>SearchSource</td><td><p>string</p></td><td><div><p>数据源唯一标识</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>数据源描述</p></div></td><td><p>xxx</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><div><p>发布时间</p></div></td><td><p>2024-11-25 14:25:59</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>正文</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>url</p></div></td><td><p>xx</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xx</p></td></tr><tr><td>TraceabilityId</td><td><p>string</p></td><td><div><p>溯源唯一标识</p></div></td><td><p>1</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>AudioSearchResult</td><td><p>object</p></td><td><div><p>语音结果</p></div></td><td></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>语音结果</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>语音结果</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xxx</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><div><p>url</p></div></td><td><p>http://xxx</p></td></tr><tr><td>Article</td><td><p>object</p></td><td><div><p>归属文档</p></div></td><td></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>xx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>url</p></div></td><td><p>http://xxx</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>xxx</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>uuid</p></div></td><td><p>xx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xx</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><div><p>搜索源</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><div><p>标签列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>标签值。</p></div></td><td><p>x</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>ClipInfos</td><td><p>array&lt;object&gt;</p></td><td><div><p>匹配列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>匹配信息</p></div></td><td></td></tr><tr><td>Score</td><td><p>number</p></td><td><div><p>阈值</p></div></td><td><p>0.9</p></td></tr><tr><td>From</td><td><p>number</p></td><td><div><p>开始位置</p></div></td><td><p>1</p></td></tr><tr><td>To</td><td><p>number</p></td><td><div><p>结束位置</p></div></td><td><p>2</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><div><p>文本内容</p></div></td><td><p>xx</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>文本类型</p></div></td><td><p>asr</p></td></tr><tr><td>TraceabilityId</td><td><p>string</p></td><td><div><p>溯源唯一标识</p></div></td><td><p>1</p></td></tr><tr><td>SearchKeywords</td><td><p>array</p></td><td><div><p>思考-query 理解关键词列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>思考-query 理解关键词</p></div></td><td><p>xx</p></td></tr><tr><td>SearchQueryList</td><td><p>array</p></td><td><div><p>文本搜索 query 列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>文本搜索 query</p></div></td><td><p>xx</p></td></tr><tr><td>RecommendSearchQueryList</td><td><p>array</p></td><td><div><p>生成-推荐列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>生成-推荐</p></div></td><td><p>xx</p></td></tr><tr><td>SupplementDataType</td><td><p>string</p></td><td><div><p>思考-需要补充的数据类型：searchQuery</p></div></td><td><p>searchQuery</p></td></tr><tr><td>SupplementEnable</td><td><p>boolean</p></td><td><div><p>思考-是否需要补充</p></div></td><td><p>true</p></td></tr><tr><td>ModelId</td><td><p>string</p></td><td><div><p>模型 id</p></div></td><td><p>xx</p></td></tr><tr><td>TokenCalculate</td><td><p>object</p></td><td><div><p>运行统计信息</p></div></td><td></td></tr><tr><td>FirstTokenTime</td><td><p>number</p></td><td><div><p>首 TOKEN 时间</p></div></td><td><p>1</p></td></tr><tr><td>SearchTime</td><td><p>number</p></td><td><div><p>搜索耗时</p></div></td><td><p>1</p></td></tr><tr><td>OutputAvgTime</td><td><p>number</p></td><td><div><p>每秒平均输出的 token 数量</p></div></td><td><p>1</p></td></tr><tr><td>Time</td><td><p>number</p></td><td><div><p>总耗时</p></div></td><td><p>1</p></td></tr><tr><td>TotalTokens</td><td><p>integer</p></td><td><div><p>总 token 数</p></div></td><td><p>1</p></td></tr><tr><td>AskUser</td><td><p>string</p></td><td><div><p>反问</p></div></td><td><p>您想了解关于xx的哪些信息？</p></td></tr><tr><td>AskUserKeywords</td><td><p>array</p></td><td><div><p>反问推荐关键词列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>反问推荐关键词</p></div></td><td><p>时间</p></td></tr><tr><td>Messages</td><td><p>array&lt;object&gt;</p></td><td><div><p>研究模式消息列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>研究模式消息</p></div></td><td></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>节点 id</p></div></td><td><p>xx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><div><p>生成文本</p></div></td><td><p>xx</p></td></tr><tr><td>GenerateFinished</td><td><p>boolean</p></td><td><div><p>当前节点是否完成</p></div></td><td></td></tr><tr><td>Clarifications</td><td><p>boolean</p></td><td><div><p>是否需要澄清</p></div></td><td></td></tr><tr><td>SearchQueries</td><td><p>array</p></td><td><div><p>搜索 query 列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>搜索 query</p></div></td><td><p>xx</p></td></tr><tr><td>SearchResult</td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>搜索结果</p></div></td><td></td></tr><tr><td>MultimodalSearchQuery</td><td><p>string</p></td><td><div><p>多模态搜索 query</p></div></td><td><p>xx</p></td></tr><tr><td>Texts</td><td><p>array&lt;object&gt;</p></td><td><div><p>文本搜索列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>文本搜索</p></div></td><td></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xx</p></td></tr><tr><td>Images</td><td><p>array&lt;object&gt;</p></td><td><div><p>图片搜索列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>图片搜索</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xx</p></td></tr><tr><td>Audios</td><td><p>array&lt;object&gt;</p></td><td><div><p>音频结果列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>音频结果</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>xx</p></td></tr><tr><td>Videos</td><td><p>array&lt;object&gt;</p></td><td><div><p>视频结果列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>视频结果</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><div><p>id</p></div></td><td><p>1</p></td></tr><tr><td>NodeCode</td><td><p>string</p></td><td><div><p>节点 code:</p><ul><li><p>generateStartStatement</p></li><li><p>generateSearchQueries</p></li><li><p>multiSearch</p></li><li><p>readSearchResult</p></li><li><p>reflection</p></li><li><p>generate</p></li></ul></div></td><td><p>generateStartStatement</p></td></tr><tr><td>SearchQuery</td><td><p>string</p></td><td><div><p>当前节点搜索 query</p></div></td><td><p>xx</p></td></tr><tr><td>Usage</td><td><p>object</p></td><td><div><p>token 用量</p></div></td><td></td></tr><tr><td>OutputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>2</p></td></tr><tr><td>InputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>TotalTokens</td><td><p>integer</p></td><td><div><p>总 oken 数量</p></div></td><td><p>3</p></td></tr><tr><td>Header</td><td><p>object</p></td><td><div><p>响应头</p></div></td><td></td></tr><tr><td>SessionId</td><td><p>string</p></td><td><div><p>对话 ID</p></div></td><td><p>x</p></td></tr><tr><td>TraceId</td><td><p>string</p></td><td><div><p>全链路 ID</p></div></td><td><p>xx</p></td></tr><tr><td>TaskId</td><td><p>string</p></td><td><div><p>任务 ID</p></div></td><td><p>x</p></td></tr><tr><td>OriginSessionId</td><td><p>string</p></td><td><div><p>源会话 ID</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>Event</td><td><p>string</p></td><td><div><p>SSE 事件。</p></div></td><td><p>task-failed</p></td></tr><tr><td>ErrorCode</td><td><p>string</p></td><td><div><p>错误码</p></div></td><td><p>AccessForbid</p></td></tr><tr><td>ErrorMessage</td><td><p>string</p></td><td><div><p>异常错误信息</p></div></td><td><p>xx</p></td></tr><tr><td>EventInfo</td><td><p>string</p></td><td><div><p>事件描述</p></div></td><td><p>xx</p></td></tr><tr><td>ResponseTime</td><td><p>integer</p></td><td><div><p>响应时间，单位为毫秒（ms）。</p></div></td><td><p>1</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求唯一标识</p></div></td><td><p>xx</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-4"></a>

```json
{
  "Payload": {
    "Output": {
      "AgentContext": {
        "BizContext": {
          "CurrentStep": "start",
          "NextStep": "search",
          "GeneratedContent": {
            "ClusterTopicResult": {
              "ClusterTopics": [
                {
                  "Topic": "xx",
                  "ImageSearchResult": {
                    "SearchResult": [
                      {
                        "Article": {
                          "SearchSourceName": "互联网搜索",
                          "Title": "xx",
                          "Url": "xx",
                          "Summary": "xx",
                          "DocUuid": "xx",
                          "DocId": "xx",
                          "CategoryUuid": "xx",
                          "Tags": [
                            "xx"
                          ],
                          "Extend1": "xx",
                          "Extend2": "xx",
                          "Extend3": "xx",
                          "SearchSourceType": "xx",
                          "SearchSource": "xx"
                        },
                        "MediaId": "xx",
                        "FileUrl": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "TextSearchResult": {
                    "SearchResult": [
                      {
                        "SearchSourceType": "SystemSearch",
                        "SearchSource": "QuarkCommonNews",
                        "SearchSourceName": "互联网搜索",
                        "PubTime": "2023-04-04 08:39:09",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx",
                        "MultimodalMedias": [
                          {
                            "MediaId": "xx",
                            "MediaType": "image",
                            "FileUrl": "xx"
                          }
                        ],
                        "CategoryUuid": "xx",
                        "Tags": [
                          "xx"
                        ],
                        "Extend1": "xx",
                        "Extend2": "xx",
                        "Extend3": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "VideoSearchResult": {
                    "SearchResult": [
                      {
                        "Article": {
                          "SearchSourceName": "互联网搜索",
                          "Title": "xx",
                          "Url": "xx",
                          "Summary": "xx",
                          "DocUuid": "xx",
                          "DocId": "xx",
                          "CategoryUuid": "xx",
                          "Tags": [
                            "xx"
                          ],
                          "Extend1": "xx",
                          "Extend2": "xx",
                          "Extend3": "x",
                          "SearchSourceType": "xx",
                          "SearchSource": "xx"
                        },
                        "MediaId": "xx",
                        "ClipInfos": [
                          {
                            "Score": 0.9,
                            "From": 1,
                            "To": 1,
                            "Text": "xx",
                            "Type": "asr"
                          }
                        ],
                        "FileUrl": "xx"
                      }
                    ],
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  },
                  "AudioSearchResult": {
                    "SearchResult": {
                      "FileUrl": "http://xx",
                      "MediaId": "xxx",
                      "ClipInfos": [
                        {
                          "Score": 1,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "Article": {
                        "Title": "xx",
                        "Url": "http://xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx",
                        "SearchSourceName": "xx",
                        "CategoryUuid": "xx",
                        "Tags": [
                          "xx"
                        ],
                        "Extend1": "xx",
                        "Extend2": "xx",
                        "Extend3": "xx",
                        "SearchSourceType": "xx",
                        "SearchSource": "xx"
                      }
                    },
                    "Current": 1,
                    "Size": 1,
                    "Total": 1
                  }
                }
              ],
              "TextGenerate": "xx",
              "GenerateFinished": true
            },
            "ExcerptResult": {
              "TextGenerate": "xx",
              "SearchResult": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Excerpt": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "TextGenerateMultimodalMediaList": [
                    {
                      "Start": 1,
                      "End": 1,
                      "DocUuid": "xx",
                      "MultimodalMediaList": [
                        {
                          "Article": {
                            "DocId": "xx",
                            "DocUuid": "xx",
                            "SearchSourceName": "互联网搜索",
                            "Title": "xx",
                            "Url": "xx"
                          },
                          "MediaId": "xx",
                          "MediaType": "image",
                          "FileUrl": "xx"
                        }
                      ]
                    }
                  ],
                  "MultimodalMedias": [
                    {
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ],
                  "CategoryUuid": "xx",
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx",
                  "Tags": [
                    "xx"
                  ]
                }
              ],
              "GenerateFinished": true,
              "GenerateLevel": "concise",
              "ReasonTextGenerate": "xx"
            },
            "NewsElementResult": {
              "TextGenerate": "x",
              "NewsElementArticleList": [
                {
                  "TextGenerate": "xx",
                  "Article": {
                    "SearchSourceType": "SystemSearch",
                    "SearchSource": "QuarkCommonNews",
                    "SearchSourceName": "互联网搜索",
                    "PubTime": "2023-04-04 08:39:09",
                    "Title": "xx",
                    "Content": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "Select": true,
                    "DocUuid": "xx",
                    "Score": 0.99,
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "NewsElementList": [
                    {
                      "Time": "时间",
                      "Location": "xx",
                      "People": "xx",
                      "Event": {
                        "CauseList": [
                          "xx"
                        ],
                        "ProcessList": [
                          "xx"
                        ],
                        "ResultList": [
                          "xx"
                        ]
                      }
                    }
                  ]
                }
              ],
              "GenerateFinished": true
            },
            "TextGenerateResult": {
              "TextGenerate": "xx",
              "TextGenerateMultimodalMediaList": [
                {
                  "Start": 1,
                  "End": 1,
                  "MultimodalMediaList": [
                    {
                      "Article": {
                        "SearchSourceName": "xx",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ]
                }
              ],
              "ReferenceList": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Source": "新华社",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ],
              "MultimodalSearchResultList": [
                {
                  "SearchResult": [
                    {
                      "Article": {
                        "SearchSourceName": "xx",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "ClipInfos": [
                        {
                          "Score": 0.1,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "FileUrl": "xx"
                    }
                  ],
                  "TimelineDateStr": "时间脉络-时间",
                  "Current": 1,
                  "Size": 1,
                  "Total": 1,
                  "SearchType": "realtime",
                  "SearchQuery": "xx"
                }
              ],
              "GenerateTraceability": {
                "Duplicate": 0.9,
                "Coordinates": [
                  {
                    "GenerateCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1
                    },
                    "NewsCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1,
                      "MediaType": "image"
                    }
                  }
                ]
              },
              "GenerateFinished": true,
              "GenerateLevel": "concise",
              "ReasonTextGenerate": "xx"
            },
            "TimelineResult": {
              "TextGenerate": "xx",
              "ReferenceList": [
                {
                  "TraceabilityId": 1,
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "互联网搜索",
                  "PubTime": "2023-04-04 08:39:09",
                  "Source": "新华社",
                  "Title": "xx",
                  "Content": "xx",
                  "Url": "xx",
                  "Summary": "xx",
                  "Select": true,
                  "DocUuid": "xx",
                  "Score": 0.99,
                  "Chunks": [
                    "xx"
                  ],
                  "DocId": "xx",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ],
              "MultimodalSearchResultList": [
                {
                  "SearchResult": [
                    {
                      "Article": {
                        "SearchSourceName": "互联网搜索",
                        "Title": "xx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "ClipInfos": [
                        {
                          "Score": 0.99,
                          "From": 1,
                          "To": 1,
                          "Text": "xx",
                          "Type": "asr"
                        }
                      ],
                      "FileUrl": "xx"
                    }
                  ],
                  "TimelineDateStr": "2024-09-11"
                }
              ],
              "GenerateTraceability": {
                "Duplicate": 0.9,
                "Coordinates": [
                  {
                    "GenerateCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1
                    },
                    "NewsCoordinate": {
                      "X": 1,
                      "Y": 1,
                      "Z": 1,
                      "MediaType": "image"
                    }
                  }
                ]
              },
              "TextGenerateMultimodalMediaList": [
                {
                  "Start": 1,
                  "End": 1,
                  "MultimodalMediaList": [
                    {
                      "Article": {
                        "SearchSourceName": "互联网搜索",
                        "Title": "xxxx",
                        "Url": "xx",
                        "Summary": "xx",
                        "DocUuid": "xx",
                        "DocId": "xx"
                      },
                      "MediaId": "xx",
                      "MediaType": "image",
                      "FileUrl": "xx"
                    }
                  ]
                }
              ],
              "GenerateFinished": true,
              "ReasonTextGenerate": "xx"
            },
            "VideoSearchResult": {
              "SearchResult": [
                {
                  "Article": {
                    "SearchSourceName": "互联网搜索",
                    "Title": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "MediaId": "xx",
                  "ClipInfos": [
                    {
                      "Score": 0.8,
                      "From": 1,
                      "To": 1,
                      "Text": "xx",
                      "Type": "asr"
                    }
                  ],
                  "FileUrl": "xx",
                  "TraceabilityId": "1"
                }
              ]
            },
            "ImageSearchResult": {
              "SearchResult": [
                {
                  "Article": {
                    "SearchSourceName": "互联网搜索",
                    "Title": "xx",
                    "Url": "xx",
                    "Summary": "xx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "CategoryUuid": "xx",
                    "Tags": [
                      "xx"
                    ],
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx"
                  },
                  "MediaId": "xx",
                  "FileUrl": "xx",
                  "TraceabilityId": "1"
                }
              ]
            },
            "TextSearchResult": {
              "Current": 1,
              "Size": 1,
              "Total": 1,
              "SearchResult": [
                {
                  "DocId": "xx",
                  "DocUuid": "xx",
                  "SearchSourceType": "SystemSearch",
                  "SearchSource": "QuarkCommonNews",
                  "SearchSourceName": "xxx",
                  "PubTime": "2024-11-25 14:25:59",
                  "Content": "xx",
                  "Url": "xx",
                  "Title": "xx",
                  "Summary": "xx",
                  "TraceabilityId": "1",
                  "CategoryUuid": "xx",
                  "Tags": [
                    "xx"
                  ],
                  "Extend1": "xx",
                  "Extend2": "xx",
                  "Extend3": "xx"
                }
              ]
            },
            "AudioSearchResult": {
              "SearchResult": [
                {
                  "MediaId": "xxx",
                  "FileUrl": "http://xxx",
                  "Article": {
                    "Title": "xx",
                    "Url": "http://xxx",
                    "Summary": "xxx",
                    "DocUuid": "xx",
                    "DocId": "xx",
                    "SearchSourceName": "xx",
                    "Extend1": "xx",
                    "Extend2": "xx",
                    "Extend3": "xx",
                    "Tags": [
                      "x"
                    ],
                    "CategoryUuid": "xx"
                  },
                  "ClipInfos": [
                    {
                      "Score": 0.9,
                      "From": 1,
                      "To": 2,
                      "Text": "xx",
                      "Type": "asr"
                    }
                  ],
                  "TraceabilityId": "1"
                }
              ]
            }
          },
          "SearchKeywords": [
            "xx"
          ],
          "SearchQueryList": [
            "xx"
          ],
          "RecommendSearchQueryList": [
            "xx"
          ],
          "SupplementDataType": "searchQuery",
          "SupplementEnable": true,
          "ModelId": "xx",
          "TokenCalculate": {
            "FirstTokenTime": 1,
            "SearchTime": 1,
            "OutputAvgTime": 1,
            "Time": 1,
            "TotalTokens": 1
          },
          "AskUser": "您想了解关于xx的哪些信息？",
          "AskUserKeywords": [
            "时间"
          ]
        }
      },
      "Messages": [
        {
          "Id": "xx",
          "Content": "xx",
          "GenerateFinished": true,
          "Clarifications": true,
          "SearchQueries": [
            "xx"
          ],
          "SearchResult": [
            {
              "MultimodalSearchQuery": "xx",
              "Texts": [
                {
                  "DocUuid": "xx"
                }
              ],
              "Images": [
                {
                  "MediaId": "xx"
                }
              ],
              "Audios": [
                {
                  "MediaId": "xx"
                }
              ],
              "Videos": [
                {
                  "MediaId": "1"
                }
              ]
            }
          ],
          "NodeCode": "generateStartStatement",
          "SearchQuery": "xx"
        }
      ]
    },
    "Usage": {
      "OutputTokens": 2,
      "InputTokens": 1,
      "TotalTokens": 3
    }
  },
  "Header": {
    "SessionId": "x",
    "TraceId": "xx",
    "TaskId": "x",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "Event": "task-failed",
    "ErrorCode": "AccessForbid",
    "ErrorMessage": "xx",
    "EventInfo": "xx",
    "ResponseTime": 1
  },
  "RequestId": "xx"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunSearchGeneration#workbench-doc-change-demo)。
