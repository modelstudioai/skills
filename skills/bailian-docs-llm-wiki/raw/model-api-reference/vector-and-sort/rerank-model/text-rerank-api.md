# 文本排序

检索系统在“召回”阶段为保证效率，返回的结果可能不够精准。排序模型能对召回的文档进行二次精准排序，确保将与用户查询最相关的结果排在最前，有效提升应用准确率。

<a id="模型概览"></a>

<a id="94a9b9899drvl"></a>

## 模型概览

> **重要**
>
> gte-rerank模型将于2026年05月30日下线，推荐使用qwen3-rerank模型替代。详情请参见[官网公告](https://www.aliyun.com/notice/118217)。

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>最大文档数</strong></p></th><th><p><strong>单条最大输入Token</strong></p></th><th><p><strong>请求最大输入Token</strong></p></th><th><p><strong>语种支持</strong></p></th><th><p><strong>应用场景</strong></p></th></tr></thead><tbody><tr><td><p>qwen3.7-text-rerank</p></td><td><p>500</p></td><td><p>30,000</p></td><td><p>120,000（建议）</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td><td><ul><li><p>文本语义检索</p></li><li><p>RAG应用</p></li></ul></td></tr><tr><td><p>qwen3-vl-rerank</p></td><td><p>文本：100</p><p>图片：40</p><p>视频：4</p></td><td><p>8,000</p></td><td rowspan="2"><p>120,000</p></td><td><p>中、英、日、韩、法、德等33种主流语言</p></td><td><ul><li><p>图像聚类</p></li><li><p>跨模态搜索</p></li><li><p>图片检索</p></li></ul></td></tr><tr><td><p>qwen3-rerank</p></td><td rowspan="2"><p>500</p></td><td rowspan="2"><p>4,000</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种</p></td><td rowspan="2"><ul><li><p>文本语义检索</p></li><li><p>RAG应用</p></li></ul></td></tr><tr><td><p>gte-rerank-v2</p></td><td><p>30,000</p></td><td><p>中、英、日、韩、泰语、西、法、葡、德、印尼语、阿拉伯语等50余语种</p></td></tr></tbody></table>

-   **单条最大输入Token**：每个Query或Document的最大Token数量。单条 Query 或 Document 的输入超过该限制时，API 会返回 HTTP 400 错误，不会截断输入内容。
-   **单次请求最大文档数**：单次请求允许的最大文档数量。对于 qwen3-vl-rerank 模型，该限制会根据文档类型（文本、图片、视频、混合模态）的不同而有所差异。
-   **请求最大输入Token**：计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，该值不得超过请求最大输入Token。

<a id="输入格式限制"></a>

<a id="f1751ee952ly4"></a>

### 输入格式限制：

| 模型 | 图片 | 视频 |
| --- | --- | --- |
| qwen3-vl-rerank | JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64） | MP4, AVI, MOV（仅支持URL） |

<a id="前提条件"></a>

<a id="o6ecl"></a>

## 前提条件

您需要已[获取 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量DASHSCOPE\_API\_KEY](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](../../preparations/install-sdk.md)。

<a id="http调用"></a>

<a id="1c5471b844yvg"></a>

## HTTP调用

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> 本节介绍 DashScope HTTP 接口。`qwen3-rerank`和`qwen3.7-text-rerank`还支持 OpenAI 兼容接口，参见[OpenAI 兼容接口](#openai-compatible-rerank)。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h3>请求</h3><a id="2319e756381fd"></a><h4>请求头（Headers）</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：qwen3.7-text-rerank、qwen3-rerank、gte-rerank-v2、qwen3-vl-rerank。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入内容。</p><blockquote><p><code>query</code> 和 <code>documents</code> 嵌套在 <code>input</code> 对象中。</p></blockquote><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>query</strong><code>string | object</code><strong>（必选）</strong></p><p>查询内容。最大长度不能超过4,000个Token。</p><p>当使用<code>qwen3-vl-rerank</code>模型时，<code>query</code>支持以下两种格式：</p><ul><li><p>字符串格式：直接传入文本字符串，例如<code>&quot;query&quot;: &quot;什么是文本排序模型&quot;</code>。</p></li><li><p>对象格式：传入字典指定模态类型和值，格式为<code>{&quot;模态类型&quot;: &quot;输入内容&quot;}</code>。支持<code>text</code>和<code>image</code>两种模态类型。</p><ul><li>文本查询：<code>&quot;query&quot;: {&quot;text&quot;: &quot;什么是文本排序模型&quot;}</code></li><li>图片查询：<code>&quot;query&quot;: {&quot;image&quot;: &quot;图片URL或Base64&quot;}</code></li></ul></li></ul><p><strong>documents</strong><code>array</code><strong>（必选）</strong></p><p>待排序的候选文档列表。每个元素是一个字符串。</p><p>当使用<code>qwen3-vl-rerank</code>模型时，每个元素是一个字典或者字符串，用于指定内容的类型和值。格式为{&quot;模态类型&quot;: &quot;输入字符串或图像、视频url&quot;}。支持<code>text</code>, <code>image</code>, <code>video</code>三种模态类型。</p><ul><li>文本：key为<code>text</code>。value为字符串形式。也可不通过dict直接传入字符串。</li><li>图片：key为<code>image</code>。value可以是公开可访问的URL，或Base64编码的Data URI。Base64格式为 <code>data:image/{format};base64,{data}</code>，其中 <code>{format}</code> 是图片格式（如 <code>jpeg</code>、<code>png</code>），<code>{data}</code> 是Base64编码字符串。</li><li>视频：key为<code>video</code>，value必须是公开可访问的URL。</li></ul></div></section><p><strong>parameters</strong><code>object</code><strong>（可选）</strong></p><p>可选参数。</p><blockquote><p><code>top_n</code> 和 <code>instruct</code> 嵌套在 <code>parameters</code> 对象中。</p></blockquote><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>top_n</strong><code>int</code><strong>（可选）</strong></p><p>返回排序后的top_n个文档。默认返回全部文档。如果指定的值大于文档总数，将返回全部文档。</p><p><strong>return_documents</strong><code>bool</code><strong>（可选）</strong></p><p>是否在排序结果中返回文档原文。默认值<code>false</code>，以减少网络传输开销。支持的模型：<code>gte-rerank-v2</code>、<code>qwen3-vl-rerank</code>、<code>qwen3-rerank</code>。</p><p><strong>instruct</strong> <code>string</code> <strong>可选</strong></p><p>添加自定义排序任务类型说明，仅在使用 <code>qwen3.7-text-rerank</code>、<code>qwen3-rerank</code> 及<code>qwen3-vl-rerank</code>模型时生效。通过该参数可以指导模型采用不同的排序策略，例如：</p><ul><li><p><strong>问答检索任务（默认）</strong>：<code>&quot;Given a web search query, retrieve relevant passages that answer the query.&quot;</code></p><ul><li>侧重点：寻找问题的答案。模型会优先评估文档是否解答了Query中的问题。</li><li>示例：对于Query“如何预防感冒？”，文档“勤洗手是预防感冒的有效方法”会获得高分；而文档“感冒是一种常见疾病”虽然主题相关，但因未提供答案，得分会显著更低。</li></ul></li><li><p><strong>语义相似度排序任务</strong>：<code>&quot;Retrieve semantically similar text.&quot;</code></p><ul><li>侧重点：判断语义的等价性。模型会评估Query和文档的核心含义是否一致，而不管具体措辞或句式。</li><li>示例：在FAQ场景中，用户Query“如何修改密码？”与候选问题“忘记密码怎么办？”在语义上高度相似，应获得高分。模型会关注两者是否指向同一个用户意图。</li></ul></li></ul><p>建议使用英文撰写。如不指定该参数，将默认按问答检索任务进行排序。更多任务指令可参考<a href="https://github.com/QwenLM/Qwen3-Embedding/blob/main/evaluation/task_prompts.json">模型仓库</a>中的示例。</p><p><strong>fps</strong> <code>float</code> <strong>可选</strong></p><p>仅 <code>qwen3-vl-rerank</code> 模型支持此参数。控制每秒从视频中抽取的帧数，值越小，抽取的帧数越少。取值范围为 (0, 5]，默认值为 1.0。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="qwen3-7-text-rerank"></a><section><a id="qwen3-7-text-rerank-h4"></a><h4>qwen3.7-text-rerank</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3.7-text-rerank&quot;,
    &quot;input&quot;: {
        &quot;query&quot;: &quot;什么是文本排序模型&quot;,
        &quot;documents&quot;: [
            &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;,
            &quot;量子计算是计算科学的一个前沿领域&quot;,
            &quot;预训练语言模型的发展给文本排序模型带来了新的进展&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;top_n&quot;: 2,
        &quot;instruct&quot;: &quot;Given a web search query, retrieve relevant passages that answer the query.&quot;
    }
}'
</code></pre></section><a id="qwen3-rerank"></a><section><a id="qwen3-rerank-h4"></a><h4>qwen3-rerank</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank \
  --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  --header &quot;Content-Type: application/json&quot; \
  --data '{
        &quot;model&quot;: &quot;qwen3-rerank&quot;,
        &quot;input&quot;: {
            &quot;documents&quot;: [
                &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;,
                &quot;量子计算是计算科学的一个前沿领域&quot;,
                &quot;预训练语言模型的发展给文本排序模型带来了新的进展&quot;
            ],
            &quot;query&quot;: &quot;什么是文本排序模型&quot;
        },
        &quot;parameters&quot;: {
            &quot;top_n&quot;: 2,
            &quot;instruct&quot;: &quot;Given a web search query, retrieve relevant passages that answer the query.&quot;
        }
}'
</code></pre></section><a id="qwen3-vl-rerank"></a><section><a id="qwen3-vl-rerank-h4"></a><h4>qwen3-vl-rerank</h4><p>文本查询</p><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3-vl-rerank&quot;,
    &quot;input&quot;:{
         &quot;query&quot;: {&quot;text&quot;: &quot;什么是文本排序模型&quot;},
         &quot;documents&quot;: [
            {&quot;text&quot;: &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;},
            {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;},
            {&quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;}
         ]
    },
    &quot;parameters&quot;: {
        &quot;return_documents&quot;: true,
        &quot;top_n&quot;: 2,
        &quot;fps&quot;: 1.0
    }
}'
</code></pre><p>图片查询</p><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3-vl-rerank&quot;,
    &quot;input&quot;:{
         &quot;query&quot;: {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;},
         &quot;documents&quot;: [
            {&quot;text&quot;: &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;},
            {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;},
            {&quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;}
         ]
    },
    &quot;parameters&quot;: {
        &quot;return_documents&quot;: true,
        &quot;top_n&quot;: 2,
        &quot;fps&quot;: 1.0
    }
}'
</code></pre></section><a id="gte-rerank-v2"></a><section><a id="gte-rerank-v2-h4"></a><h4>gte-rerank-v2</h4><a id="code-block-5"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;gte-rerank-v2&quot;,
    &quot;input&quot;:{
         &quot;query&quot;: &quot;什么是文本排序模型&quot;,
         &quot;documents&quot;: [
         &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;,
         &quot;量子计算是计算科学的一个前沿领域&quot;,
         &quot;预训练语言模型的发展给文本排序模型带来了新的进展&quot;
         ]
    },
    &quot;parameters&quot;: {
        &quot;return_documents&quot;: true,
        &quot;top_n&quot;: 2
    }
}'
</code></pre></section><a id="dashscope-cli"></a><section><a id="dashscope-cli-h4"></a><h4>dashscope CLI</h4><p>通过 dashscope 命令行调用。</p><a id="code-block-6"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope rerank create -m gte-rerank-v2 -q &quot;机器学习&quot; -d &quot;机器学习是AI分支&quot; -d &quot;今天天气真好&quot;
</code></pre><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../../preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div><p>完整地域表见 <a href="../../preparations/base-url.md">Base URL 总览</a>。</p></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b14ec019d4k6f"></a><h3>响应</h3><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>results</strong><code>array</code></p><p>排序结果列表。按 <code>relevance_score</code> 从高到低排列。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>document</strong><code>dict</code></p><p>文档原文对象。仅在请求参数 <code>return_documents</code> 为 <code>true</code> 时返回。结构为 <code>{&quot;text&quot;: &quot;文档原文&quot;}</code>。</p><p><strong>index</strong><code>int</code></p><p>表示该结果对应于输入 <code>documents</code> 列表中的原始索引位置。</p><p><strong>relevance_score</strong><code>double</code></p><p>该文档与查询的语义相关性得分，取值范围为 0.0 到 1.0。分数越高，相关性越强。</p><div><div><p><strong>说明</strong>此分数为当前请求中的相对分数，主要用于对本次请求内的文档排序，不可作为跨请求比较的绝对值。</p></div></div></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>输出信息统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>prompt_tokens</strong><code>int</code></p><p>仅 <code>qwen3.7-text-rerank</code> 返回。表示本次请求输入内容的 Token 总数。</p><p><strong>total_tokens</strong><code>int</code></p><p>本次请求消耗的 Token 总数，用于计量计费和审计。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><a id="fig-code-group"></a><div><a id="fig-code-group-qwen3-7-text-rerank-tab"></a>qwen3.7-text-rerank<div><a id="code-code-group-qwen3-7-text-rerank"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;results&quot;: [
            {
                &quot;index&quot;: 0,
                &quot;relevance_score&quot;: 0.9334521178273196
            },
            {
                &quot;index&quot;: 2,
                &quot;relevance_score&quot;: 0.34100082626411193
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;prompt_tokens&quot;: 79,
        &quot;total_tokens&quot;: 79
    },
    &quot;request_id&quot;: &quot;85ba5752-1900-47d2-8896-23f99b13f6e1&quot;
}
</code></pre></div><a id="fig-code-group-qwen3-rerank-tab"></a>qwen3-rerank<div><a id="code-code-group-qwen3-rerank"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;results&quot;: [
            {
                &quot;index&quot;: 0,
                &quot;relevance_score&quot;: 0.9334521178273196
            },
            {
                &quot;index&quot;: 2,
                &quot;relevance_score&quot;: 0.34100082626411193
            }
        ]
    },
    &quot;request_id&quot;: &quot;85ba5752-1900-47d2-8896-23f99b13f6e1&quot;,
    &quot;usage&quot;: {
        &quot;total_tokens&quot;: 79
    }
}
</code></pre></div><a id="fig-code-group-qwen3-vl-rerank-gte-rerank-v2-tab"></a>qwen3-vl-rerank / gte-rerank-v2<div><a id="code-code-group-qwen3-vl-rerank-gte-rerank-v2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;results&quot;: [
            {
                &quot;document&quot;: {
                    &quot;text&quot;: &quot;文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序&quot;
                },
                &quot;index&quot;: 0,
                &quot;relevance_score&quot;: 0.9334521178273196
            },
            {
                &quot;document&quot;: {
                    &quot;text&quot;: &quot;预训练语言模型的发展给文本排序模型带来了新的进展&quot;
                },
                &quot;index&quot;: 2,
                &quot;relevance_score&quot;: 0.34100082626411193
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;total_tokens&quot;: 79
    },
    &quot;request_id&quot;: &quot;85ba5752-1900-47d2-8896-23f99b13f6e1&quot;
}
</code></pre></div></div></section><a id="失败响应"></a><section><a id="失败响应-h4"></a><h4>失败响应</h4><p>在访问请求出错的情况下，输出的结果中会通过<code>code</code>和<code>message</code>指明出错原因。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="openai-兼容接口"></a>

<a id="openai-compatible-rerank"></a>

## OpenAI 兼容接口

`qwen3-rerank`和`qwen3.7-text-rerank`支持通过 OpenAI 兼容接口调用；`gte-rerank-v2`和`qwen3-vl-rerank`不支持，调用时会返回`model_not_supported`错误。

请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`

与 DashScope HTTP 接口的差异：

-   请求体为扁平结构，`query`、`documents`、`top_n`、`instruct`、`return_documents`与`model`同级，不嵌套在`input`和`parameters`中。
-   排序结果位于响应的`results`数组中，每项包含`index`（文档在请求中的序号）和`relevance_score`（相关性得分）；`return_documents`为`true`时额外返回`document.text`。

<a id="请求示例"></a>

<a id="openai-compatible-rerank-request"></a>

### 请求示例

<a id="code-block-8"></a>

```bash
curl --request POST \
  --url https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-rerank",
    "query": "什么是重排序模型",
    "documents": [
      "重排序模型广泛应用于搜索引擎和推荐系统",
      "量子计算是计算科学的前沿领域"
    ],
    "top_n": 2,
    "return_documents": true
}'
```

<a id="响应示例"></a>

<a id="openai-compatible-rerank-response"></a>

### 响应示例

<a id="code-block-9"></a>

```json
{
  "object": "list",
  "results": [
    {
      "document": {
        "text": "重排序模型广泛应用于搜索引擎和推荐系统"
      },
      "index": 0,
      "relevance_score": 0.8019987834170111
    },
    {
      "document": {
        "text": "量子计算是计算科学的前沿领域"
      },
      "index": 1,
      "relevance_score": 0.33869324986016763
    }
  ],
  "model": "qwen3-rerank",
  "id": "1a295f99-89ff-901f-a57f-9a38a6d963fa",
  "usage": {
    "total_tokens": 59
  }
}
```

Python 和 Node.js 调用示例请参见[重排序](../../../model-user-guide/model-experience/embedding-rerank-model/rerank.md)。

<a id="sdk调用"></a>

<a id="EKM4W"></a>

## SDK调用

<a id="调用示例"></a>

<a id="9858bdb0cf7xi"></a>

### 调用示例

以下示例展示了调用文档排序模型API的代码示例。

> SDK 的参数命名与HTTP接口基本一致，参数结构进行了一定封装。比如 HTTP 使用嵌套的 `input` 和 `parameters` 结构，但SDK 使用扁平参数。请在开发时注意区分。

<a id="code-block-10"></a>

```python
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def text_rerank():
    resp = client.rerank.create(
        model="qwen3.7-text-rerank",
        query="什么是文本排序模型",
        documents=[
            "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
            "量子计算是计算科学的一个前沿领域",
            "预训练语言模型的发展给文本排序模型带来了新的进展"
        ],
        top_n=10,
        instruct="Given a web search query, retrieve relevant passages that answer the query."
    )
    print(resp)

if __name__ == '__main__':
    text_rerank()
```

以下示例展示了使用`qwen3-vl-rerank`模型进行多模态排序（以图片作为查询）的代码示例。

<a id="code-block-11"></a>

```python
import os
import dashscope
import json
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def vl_rerank():
    resp = client.rerank.create(
        model="qwen3-vl-rerank",
        query={"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
        documents=[
            {"text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"},
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
        ],
        top_n=2,
        return_documents=True
    )
    print(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))

if __name__ == '__main__':
    vl_rerank()
```

<a id="输出示例"></a>

<a id="abfe95f4ab4tt"></a>

### 输出示例

> **说明**
>
> SDK 2.0 返回结构化响应对象，排序结果通过 `resp.results` 访问（`resp.results[i].index` / `.relevance_score` / `.document`）；请求失败时抛出 `DashScopeError` 异常。

<a id="code-block-12"></a>

```json
{
    "request_id": "4b0805c0-6b36-490d-8bc1-4365f4c89905",
    "output": {
        "results": [
            {
                "index": 0,
                "relevance_score": 0.9334521178273196
            },
            {
                "index": 2,
                "relevance_score": 0.34100082626411193
            }
        ]
    },
    "usage": {
        "prompt_tokens": 79,
        "total_tokens": 79
    }
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="限流"></a>

<a id="8229db579efdw"></a>

## 限流

模型限流触发条件请参考[限流](../../../model-user-guide/get-started-with-models/rate-limit.md)。
