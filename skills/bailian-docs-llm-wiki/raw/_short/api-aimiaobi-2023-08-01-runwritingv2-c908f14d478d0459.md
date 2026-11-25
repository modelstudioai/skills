# RunWritingV2

智能写作。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](iframe-embedding-scheme-6f73b86f9f7bdf41.md)

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
| aimiaobi:RunWritingV2 | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/aimiaobi/runWritingV2 HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：获取<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">业务空间 ID（Workspace ID）</a></p></div></td><td><p>xxxx</p></td></tr><tr><td>TaskId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>任务唯一 ID，多轮对话可复用同一轮任务 ID</p><div><p>TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</p></div></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>SessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>单轮对话的 ID（已过期，不推荐传递）</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>WritingScene</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作场景（government:政务、media:传媒、market:营销，office：办公,custom:自定义）</p></div></td><td><p>media</p></td></tr><tr><td>WritingStyle</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作文体，具体文体列表请参考： <a href="api-aimiaobi-2023-08-01-listwritingstyles-00ef4732c20d15a3.md">ListWritingStyles</a></p></div></td><td><p>新闻评论</p></td></tr><tr><td>DistributeWriting</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否为分步骤写作，请参考 接口请求示例 的 分步骤 参数说明。</p></div></td><td><p>false</p></td></tr><tr><td>PromptMode</td><td><p>string</p></td><td><p>否</p></td><td><div><p>模板类型：Template（模板模式）, PE（高级 PE 模式）</p><ol><li><p>当 PromptMode 为空时，传 Prompt，推荐格式为：写作主题+写作篇幅+写作要求+禁止事项</p></li><li><p>当 PromptMode=Template 时，需要传 WritingParams（字典类型，key、value 都是字符串），writingParams 表单定义参考： <a href="api-aimiaobi-2023-08-01-listwritingstyles-00ef4732c20d15a3.md">ListWritingStyles</a> 接口中的 .Data.TemplateDefine[].Fields</p></li><li><p>当 PromptMode=PE，需要传 WritingParams，且固定传两个字段</p><ol><li><p>topic: 话题，必填。需要写的主题内容</p></li><li><p>prompt: 其他自定义提示词，选填。其他写作要求</p></li></ol></li></ol></div></td><td><p>Template</p></td></tr><tr><td>Step</td><td><p>string</p></td><td><p>否</p></td><td><div><p>分步骤写作步骤：</p><ul><li><p>OutlineGenerate: 大纲生成</p></li><li><p>Writing: 写作</p></li></ul><p>在分步骤写作场景中（DistributeWriting=true） 默认 先写大纲、后根据大纲写作。</p></div></td><td><p>Writing</p></td></tr><tr><td>Articles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>引用的文章（注意 传递此参数后， 联网检索将不会进行，影响：SearchSources、 SearchSources 参数）</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>文章对象</p></div></td><td></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章标题</p></div></td><td><p>文章标题</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章内容</p></div></td><td><p>文章内容</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章 URL</p></div></td><td><p><a href="https://www.example.com/aaa.docx">https://www.example.com/aaa.docx</a></p></td></tr><tr><td>Source</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章来源</p></div></td><td><p>新华社</p></td></tr><tr><td>SearchSourceName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>搜索信源</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发布时间</p></div></td><td><p>2024-11-25 14:25:59</p></td></tr><tr><td>GcNumberSizeTag</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章篇幅描述（300 字左右、600 字左右、1000 字左右、2000 字左右等）</p></div></td><td><p>2000字左右</p></td></tr><tr><td>GcNumberSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>写作的篇数（多篇按照不同的 sessionId 同时返回）</p></div></td><td><p>2</p></td></tr><tr><td>Language</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章输出语言</p><ul><li><p>en:英文</p></li><li><p>zh:中文</p></li><li><p>或者其他自定义的输出语言要求</p></li></ul></div></td><td><p>en</p></td></tr><tr><td>Keywords</td><td><p>array</p></td><td><p>否</p></td><td><div><p>关键词列表（会参与到检索与写作）</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>关键词（会参与到检索与写作）</p></div></td><td><p>关键词</p></td></tr><tr><td>Prompt</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作提示词（prompt 和 writingParams 二选一，详情请参考 PromptMode 字段说明）</p></div></td><td><p>提示词</p></td></tr><tr><td>WritingParams</td><td><p>object</p></td><td><p>否</p></td><td><div><p>模板写作参数（字典结构，key value 都是字符串）（prompt 和 writingParams 二选一，详情请参考 PromptMode 字段说明）</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>模板写作参数</p></div></td><td><p>模板写作参数</p></td></tr><tr><td>Outlines</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>大纲列表（分步骤接口使用，已过时，推荐使用新版分步骤写作的：OutlineList）</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>大纲对象</p></div></td><td></td></tr><tr><td>Outline</td><td><p>string</p></td><td><p>否</p></td><td><div><p>大纲</p></div></td><td><p>大纲</p></td></tr><tr><td>Articles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>大纲重点参考的文章列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>大纲重点参考的文章</p></div></td><td></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标题</p></div></td><td><p>标题</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>正文内容</p></div></td><td><p>正文内容</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章 URL</p></div></td><td><p>文章URL</p></td></tr><tr><td>Summarization</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>摘编对象列表（分步骤接口使用）</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>摘编对象</p></div></td><td></td></tr><tr><td>Event</td><td><p>string</p></td><td><p>否</p></td><td><div><p>事件名称</p></div></td><td><p>事件名称</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><p>否</p></td><td><div><p>事件摘编</p></div></td><td><p>事件摘编</p></td></tr><tr><td>MiniDocs</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>文章片段列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>文章片段对象</p></div></td><td></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>片段内容</p></div></td><td><p>片段内容</p></td></tr><tr><td>Star</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否重点考虑该片段</p></div></td><td><p>true</p></td></tr><tr><td>Index</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章片段在引用文章中的索引</p></div></td><td><p>索引</p></td></tr><tr><td>UseSearch</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否使用联网检索。（默认不检索，true 则会 走 系统自带的 联网检索）</p></div></td><td><p>true</p></td></tr><tr><td>SearchSources</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>使用指定的搜索源列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>搜索源对象</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><p>否</p></td><td><div><p>SystemSearch：系统内置搜索，CustomSemanticSearch：自建语义索引搜索，ThirdSearch：三方 API 搜索</p></div></td><td><p>SystemSearch</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>搜索源描述（已过时，不推荐使用， 传递后不会生效）</p></div></td><td><p>互联网搜索</p></td></tr><tr><td>DatasetName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据源唯一标识</p></div></td><td><p>QuarkCommonNews</p></td></tr><tr><td>OutlineList</td><td><p>array</p></td><td><p>否</p></td><td><div><p>大纲列表(新版分大纲写作)</p></div></td><td></td></tr><tr><td></td><td><a href="api-aimiaobi-2023-08-01-struct-writingoutline-b8942a4454fc3a65.md">WritingOutline</a></td><td><p>否</p></td><td><div><p>大纲</p></div></td><td></td></tr><tr><td>SourceTraceMethod</td><td><p>string</p></td><td><p>否</p></td><td><div><p>溯源方式（目前仅支持 modelSourceTrace） modelSourceTrace：在最后输出的正文中，让模型在 各个片段的尾部输出引用标记。以 [[n]]。索引从 1 开始。</p></div></td><td><p>modelSourceTrace</p></td></tr></tbody></table>

<a id="接口请求示例"></a>

<a id="api-detail-requestParamsDescription"></a>

## 接口请求示例

<a id="1-直接写作-使用-prompt"></a>

### 1\. 直接写作（使用 Prompt）

<a id="code-block-2"></a>

```json
{
  //业务空间 ID
  "WorkspaceId": "your-workspace-id",
  //启用检索
  "UseSearch":true,
  //写作提示词
  "Prompt": "请写一篇关于人工智能发展的新闻评论，字数要求 800-1000 字，要求观点鲜明，逻辑清晰，禁止使用过于夸张的表述。"
}
```

<a id="2-模板写作-promptmode-template"></a>

### 2\. 模板写作（PromptMode=Template）

<a id="code-block-3"></a>

```json
{
  "WorkspaceId": "your-workspace-id",
  "WritingScene": "media",
  "WritingStyle": "新闻评论",
  "PromptMode": "Template",
  "WritingParams": {
    "topic": "人工智能在医疗领域的应用突破，某医院成功使用 AI 辅助诊断系统，准确率达到 95%以上",
    "corePerspective": "AI 医疗技术的快速发展体现了科技创新对传统行业的深刻变革，但同时也需要建立完善的法律法规和伦理规范，确保技术应用的安全性和公平性"
  }
}
```

**模板字段说明（传媒场景）：**

-   **topic** (必填): 选题，用简单的语言描述新闻事件或者从常见的新闻中挖掘新颖切入点，1-2000 字符
-   **corePerspective** (必填): 核心观点，明确价值判断立场、体现社会意义或行业影响，1-2000 字符

<a id="3-高级模式-promptmode-pe"></a>

### 3\. 高级模式（PromptMode=PE）

> **说明**
>
> （自定义提示词，系统会完全根据提示词进行写作，区分写作主题与写作要求）

<a id="code-block-4"></a>

```json
{
  "WorkspaceId": "your-workspace-id",
  "PromptMode": "PE",
  "WritingParams": {
    "topic": "人工智能发展趋势",
    "prompt": "字数要求：800-1000 字。写作风格：观点鲜明，逻辑清晰，语言生动。内容要求：需要包含背景介绍、现状分析、未来展望，重点突出创新点。禁止事项：禁止使用过于夸张的表述，避免使用过于专业的术语。其他要求：需要引用具体数据，要求结构层次分明。"
  }
}
```

**模板字段说明（PE 模式）：**

-   **topic** (必填): 话题，需要写的主题内容
    
-   **prompt** (可选): 其他自定义提示词，其他写作要求。填写时可按以下格式组织内容：
    
    -   **字数要求**：如"字数 800-1000 字"、"篇幅控制在 1500 字左右"
    -   **写作风格**：如"观点鲜明，逻辑清晰"、"语言生动，富有感染力"
    -   **内容要求**：如"需要包含背景介绍、现状分析、未来展望"、"重点突出创新点"
    -   **禁止事项**：如"禁止使用过于夸张的表述"、"避免使用专业术语"
    -   **其他特殊要求**：如"需要引用具体数据"、"要求结构层次分明"
    
    多个要求可以用句号、分号或换行分隔，建议格式：`"字数要求：XXX。写作风格：XXX。内容要求：XXX。禁止事项：XXX。其他要求：XXX。"`
    

<a id="4-分步骤写作-第一步-生成大纲"></a>

### 4\. 分步骤写作 - 第一步：生成大纲

<a id="code-block-5"></a>

```json
{
  "WorkspaceId": "your-workspace-id",
  "WritingStyle": "outlineWriting",
  "WritingScene": "others",
  "Step": "OutlineGenerate",
  "Prompt": "请生成一篇关于人工智能发展的新闻评论大纲，字数要求 800-1000 字，要求包含背景介绍、现状分析、未来展望三个部分"
}
```

**说明：**

-   第一步生成大纲，返回结果中包含 `Outlines` 字段，包含生成的大纲结构
-   `Prompt` 中应明确说明要生成的大纲主题、字数要求、结构要求等
-   返回的 `Outlines` 结构需要保存，用于第二步传递

<a id="5-分步骤写作-第二步-使用大纲写作"></a>

### 5\. 分步骤写作 - 第二步：使用大纲写作

<a id="code-block-6"></a>

```json
{
  "WorkspaceId": "your-workspace-id",
  "WritingStyle": "outlineWriting",
  "WritingScene": "others",
  "Step": "Writing",
  "OutlineList": [
    {
      "OutlineId": "outline-001",
      "Outline": "人工智能发展背景",
      "WordCount": "200-300 字",
      "Children": [
        {
          "OutlineId": "outline-001-001",
          "Outline": "人工智能技术起源",
          "WordCount": "100-150 字",
          "Children": []
        },
        {
          "OutlineId": "outline-001-002",
          "Outline": "当前发展现状",
          "WordCount": "100-150 字",
          "Children": []
        }
      ]
    },
    {
      "OutlineId": "outline-002",
      "Outline": "人工智能应用分析",
      "WordCount": "300-400 字",
      "Children": []
    },
    {
      "OutlineId": "outline-003",
      "Outline": "未来发展趋势",
      "WordCount": "300-400 字",
      "Children": []
    }
  ],
  "Prompt": "根据生成的大纲进行写作，字数要求 800-1000 字，要求观点鲜明，逻辑清晰，语言生动"
}
```

**说明：**

-   第二步使用大纲进行写作，必须传入第一步返回的 `Outlines` 结构
    
-   OutlineList 是必填参数，包含大纲的层级结构，每个大纲节点包含：
    
    -   **OutlineId** (必填): 大纲节点 ID
    -   **Outline** (必填): 大纲名称
    -   **WordCount** (可选): 该部分的字数要求
    -   **Children** (可选): 子大纲列表，结构同父级大纲
-   `Prompt` 中可以补充写作要求，如字数、风格、内容要求等
    

<a id="6-以稿写稿-快速以稿写稿-imitatewriting"></a>

### 6\. 以稿写稿（快速以稿写稿 - imitateWriting）

<a id="code-block-7"></a>

```json
{
  "WorkspaceId": "your-workspace-id",
  "WritingScene": "custom",
  "WritingStyle": "imitateWriting",
  "PromptMode": "Template",
  "WritingParams": {
    "topic": "新能源汽车市场快速发展，2024 年销量突破 800 万辆，同比增长 35%。政策支持、技术进步和消费者接受度提升是主要推动因素。",
    "styleStructReferenceContent": "[{\"title\":\"人工智能产业迎来爆发式增长\",\"content\":\"【引言】\\n 人工智能技术正在深刻改变着我们的生产和生活方式。从智能语音助手到自动驾驶汽车，从医疗诊断到金融风控，AI 应用场景不断拓展。\\n\\n【发展现状】\\n 据统计，2023 年全球人工智能市场规模达到 1500 亿美元，预计到 2025 年将突破 3000 亿美元。中国作为全球第二大 AI 市场，在算法、算力、数据等方面都取得了显著进展。\\n\\n【核心驱动因素】\\n 一是政策支持力度加大。国家出台多项政策支持 AI 产业发展，设立专项资金，建设创新平台。\\n 二是技术突破不断涌现。大模型、深度学习等技术日趋成熟，应用门槛逐步降低。\\n 三是市场需求持续增长。企业数字化转型加速，对 AI 解决方案的需求日益旺盛。\\n\\n【挑战与展望】\\n 尽管发展迅速，但 AI 产业仍面临数据安全、算法公平性、人才短缺等挑战。未来需要在技术创新、标准制定、人才培养等方面持续发力，推动 AI 产业健康可持续发展。\"}]"
  }
}
```

**模板字段说明（快速以稿写稿）：**

-   **topic** (必填): 主题内容，描述要写作的主题和核心信息，最大 3000 字符
-   **styleStructReferenceContent** (必填): 参考结构的文章列表，需要传入 JSON 数组序列化后的字符串，每个元素包含 `title` 和 `content` 字段，用于学习文章的结构和写作风格

**其他说明：**

-   参考文章应选择结构清晰、层次分明的文章（如：引言-现状-分析-结论的结构）
-   系统会学习参考文章的结构框架和写作风格，然后基于新的主题内容生成新文章
-   建议只选择一篇结构鲜明的参考文章，以确保生成文章的结构一致性

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | BaseLlmResponse |  |
| Header | object | 响应头 |  |
| ErrorCode | string | 错误码 | 错误码 |
| ErrorMessage | string | 错误信息 | 错误信息 |
| Event | string | 分为两类事件，写作事件以及其他事件<br><br>写作事件：task-progress-start-generating，每次输出都是全量的文章信息<br><br>其他事件（可以不用关注，或者关注 payload.output.text 即可）： writing-instruction-analysis：指令分析 task-progress-news-search-end：联网检索 result-intent-recognition-end：意图识别 | task-progress-start-generating |
| OriginSessionId | string | 父会话 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| SessionId | string | 会话 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| StatusCode | integer | http 响应码 | 400 |
| TaskId | string | 任务 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TraceId | string | 全链路 ID | 全链路ID |
| Payload | object | 响应体 |  |
| Output | object | 输出 |  |
| Articles | array<object> | 参照文章 |  |
|  | object | 参照文章 |  |
| Author | string | 作者 | 作者 |
| Content | string | 内容 | 文章内容 |
| DocId | string | 文档-自定义的唯一 ID | 文档-自定义的唯一ID |
| DocUuid | string | 内部文档唯一标识 | 98229f6001cf4deeb1668191d4eccc75 |
| PubTime | string | 发布时间 | 2024-08-28 11:38:28 |
| Source | string | 来源 | 央视网 |
| Summary | string | 文章摘要 | 文章摘要 |
| Tag | string | 标签 | 文章标签 |
| Title | string | 标题 | 文章标题 |
| Url | string | 文章 URL | [https://www.example.com/aaa.docx](https://www.example.com/aaa.docx) |
| MiniDoc | array | 文章精排之后的片段列表 | 文章精排之后的片段 |
|  | string | 文章精排之后的片段 \* | 文章精排之后的片段 |
| SearchQuery | string | query 改写结果 | 大模型改变世界 |
| Text | string | 文本生成结果 | 文本生成结果 |
| Outlines | array | 大纲列表（分步骤大纲生成场景下 writingStyle=outlineWriting。step=outlineWriting 时返回该字段） |  |
|  | [WritingOutline](api-aimiaobi-2023-08-01-struct-writingoutline-b8942a4454fc3a65.md) | 大纲 |  |
| Title | string | 文章标题（分步骤大纲生成场景下 writingStyle=outlineWriting。step=outlineWriting 时返回该字段） | 文章标题 |
| SearchResult | [OutlineSearchResult](api-aimiaobi-2023-08-01-struct-outlinesearchresu-ecc7ccc1567368c1.md) | 检索结果（分步骤大纲生成场景下 writingStyle=outlineWriting。step=OutlineSearch 时返回该字段） |  |
| GenerateTraceability | [GenerateTraceability](api-aimiaobi-2023-08-01-struct-generatetraceabil-619a2841f2a0d3b2.md) | 溯源对象（当传入 该 modelSourceTrace 参数 后会返回该字段） |  |
| Usage | object | token 用量 |  |
| InputTokens | integer | 输入使用的 Token 数量 | 78 |
| OutputTokens | integer | 输出 Token 数量 | 34 |
| TokenMap | object | token 消耗明细 |  |
|  | integer | token 消耗明细 | 44 |
| TotalTokens | integer | 总 Token 数量 | 38 |
| RequestId | string | 请求 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| End | boolean | 响应包是否结束 | true |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-8"></a>

```json
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-progress-start-generating",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Articles": [
        {
          "Author": "作者",
          "Content": "文章内容",
          "DocId": "文档-自定义的唯一ID",
          "DocUuid": "98229f6001cf4deeb1668191d4eccc75",
          "PubTime": "2024-08-28 11:38:28",
          "Source": "央视网",
          "Summary": "文章摘要",
          "Tag": "文章标签",
          "Title": "文章标题",
          "Url": "https://www.example.com/aaa.docx"
        }
      ],
      "MiniDoc": [
        "文章精排之后的片段"
      ],
      "SearchQuery": "大模型改变世界",
      "Text": "文本生成结果",
      "Outlines": [
        {
          "WritingTips": "大纲写作要求、写作提示",
          "OutlineId": "xxx",
          "Outline": "大纲名称",
          "SearchKeyWordList": [
            "检索关键词"
          ],
          "WordCount": "写作字数要求的描述",
          "Articles": [
            {
              "Url": "http://www.example.com/xxxx.html",
              "Title": "新闻标题",
              "Content": "新闻内容",
              "SearchSource": "检索源编码",
              "SearchSourceName": "检索源名称",
              "PubTime": "2023-04-11 06:14:07",
              "PrimaryOutline": "一级大纲名称",
              "Outline": "大纲名称"
            }
          ],
          "Children": [
            {
              "WritingTips": "大纲写作要求、写作提示",
              "OutlineId": "xxx",
              "Outline": "大纲名称",
              "SearchKeyWordList": [
                "检索关键词"
              ],
              "WordCount": "写作字数要求的描述",
              "Articles": [
                {
                  "Url": "http://www.example.com/xxxx.html",
                  "Title": "新闻标题",
                  "Content": "新闻内容",
                  "SearchSource": "检索源编码",
                  "SearchSourceName": "检索源名称",
                  "PubTime": "2023-04-11 06:14:07",
                  "PrimaryOutline": "一级大纲名称",
                  "Outline": "大纲名称"
                }
              ],
              "Children": [
                {
                  "WritingTips": "大纲写作要求、写作提示",
                  "OutlineId": "xxx",
                  "Outline": "大纲名称",
                  "SearchKeyWordList": [
                    "检索关键词"
                  ],
                  "WordCount": "写作字数要求的描述",
                  "Articles": [
                    {
                      "Url": "http://www.example.com/xxxx.html",
                      "Title": "新闻标题",
                      "Content": "新闻内容",
                      "SearchSource": "检索源编码",
                      "SearchSourceName": "检索源名称",
                      "PubTime": "2023-04-11 06:14:07",
                      "PrimaryOutline": "一级大纲名称",
                      "Outline": "大纲名称"
                    }
                  ],
                  "Children": []
                }
              ]
            }
          ]
        }
      ],
      "Title": "文章标题",
      "SearchResult": {
        "Query": "高校环保义卖案例 大学生旧物循环利用率的文章",
        "Outline": "晨光中的自律：清晨6:30的校园",
        "OutlineId": "xxxxxx",
        "PrimaryOutline": "大学生正能量的一天",
        "Articles": []
      },
      "GenerateTraceability": {
        "News": [
          {
            "Url": "http://www.example.com/xxx.html\n",
            "Title": "新闻标题",
            "PubTime": "2024-01-22 10:29:00",
            "SearchSourceName": "检索源编码\n\n",
            "SearchSource": "检索源唯一标识",
            "Index": 2
          }
        ]
      }
    },
    "Usage": {
      "InputTokens": 78,
      "OutputTokens": 34,
      "TokenMap": {
        "key": 44
      },
      "TotalTokens": 38
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunWritingV2#workbench-doc-change-demo)。
