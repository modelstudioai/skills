# Multimodal-Embedding API详情

多模态向量模型将文本、图像和视频转换为同一语义空间中的向量表示，支持跨模态检索、内容分类和语义相似度计算。

<a id="核心能力"></a>

<a id="a6c4aedaf8fee"></a>

## 核心能力

-   **跨模态检索**：以文搜图、以图搜视频、以图搜图等跨模态语义搜索。
-   **语义相似度计算**：在统一向量空间中衡量不同模态内容之间的语义相似性。
-   **内容分类与聚类**：基于语义向量进行智能分组、打标和聚类分析。

> **关键特性** ：所有模态（文本、图片、视频）的向量均位于同一语义空间，可通过余弦相似度等方法直接进行跨模态匹配与比较。模型选型和使用方法详见 [文本与多模态向量化](../../../model-user-guide/model-experience/embedding-rerank-model/embedding.md) 。

<a id="向量类型说明"></a>

<a id="b8c4d9e023wuz"></a>

## 向量类型说明

多模态向量模型支持两种向量生成方式：

-   **多模态独立向量**：为 contents 中的每个输入（文本、图片、视频、多图）分别生成独立向量。例如，输入 1 段文本和 1 张图片，返回 2 个独立向量。适用于逐项对比不同内容的场景，如以图搜图、以文搜图。
    
-   **多模态融合向量**：将 contents 中的所有输入融合为 1 个向量，实现跨模态综合语义表征。适用于需要整体理解多模态内容的场景，如将商品图片和描述文本融合为统一表征进行检索。`qwen3-vl-embedding` 通过设置 `enable_fusion=true` 开启融合模式；`tongyi-embedding-vision-plus-2026-03-06` 和 `tongyi-embedding-vision-flash-2026-03-06` 通过将 text、image、video 放在同一个 content 对象中实现融合。融合向量支持以下组合：
    
    -   文本 + 图片融合
    -   文本 + 视频融合
    -   多图 + 文本融合（传入多个 image 条目）
    -   图片 + 视频 + 文本混合融合

> `qwen2.5-vl-embedding` 仅支持融合向量，不支持独立向量。 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 仅支持独立向量。 `tongyi-embedding-vision-plus-2026-03-06` 和 `tongyi-embedding-vision-flash-2026-03-06` 同时支持独立向量和融合向量，融合向量通过将 text、image、video 放在同一个 content 对象中实现。

模型介绍、选型建议和使用方法，请参考[文本与多模态向量化](../../../model-user-guide/model-experience/embedding-rerank-model/embedding.md)。

<a id="模型概览"></a>

<a id="3ef850b9cfgvv"></a>

## 模型概览

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>向量维度</strong></p></th><th><p><strong>文本长度限制</strong></p></th><th><p><strong>图片大小限制</strong></p></th><th><p><strong>视频大小限制</strong></p></th><th><p><strong>单价（每千输入Token）</strong></p></th><th><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>2560（默认）, 2048, 1536, 1024, 768, 512, 256</p></td><td rowspan="2"><p>32,000 Token</p></td><td><p>单张大小不超过<strong>10 MB</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>50 MB</strong></p></td><td rowspan="2"><p>图片/视频：0.0018元</p><p>文本：0.0007元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>2048, 1024（默认）, 768, 512</p></td><td><p>单张大小不超过<strong>5 MB</strong></p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td rowspan="4"><p>1,024 Token</p></td><td rowspan="2"><p>建议单张大小不超过<strong>5 MB</strong>，最大<strong>10 MB。</strong>支持多图，最多支持输入<strong>64张</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>50 MB</strong></p><p>且编码类型为H.264/H.265</p></td><td><p>0.0005元</p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>0.00015元</p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td rowspan="2"><p>单张大小不超过<strong>3 MB</strong>。支持多图，最多支持输入<strong>8张</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>0.0005元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>0.00015元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>1,024</p></td><td><p>512 Token</p></td><td><p>单张大小不超过<strong>3 MB</strong></p></td><td><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>图片/视频：0.0009 元</p><p>文本：0.0007 元</p></td><td><p>无免费额度</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>向量维度</strong></p></th><th><p><strong>文本长度限制</strong></p></th><th><p><strong>图片大小限制</strong></p></th><th><p><strong>视频大小限制</strong></p></th><th><p><strong>单价（每千输入Token）</strong></p></th></tr></thead><tbody><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td><p>1,024 Token</p></td><td rowspan="2"><p>最多 <strong>8 张</strong>且单张大小不超过<strong>3 MB</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>0.0005元</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>1,024 Token</p></td><td><p>0.00015元</p></td></tr></tbody></table>

<a id="输入格式与语种限制"></a>

<a id="f1751ee952ly4"></a>

### 输入格式与语种限制：

<table><thead><tr><th colspan="5"><strong>多模态融合向量模型</strong></th></tr><tr><th><strong>模型</strong></th><th><strong>文本</strong></th><th><strong>图片</strong></th><th><strong>视频</strong></th><th><strong>单次请求条数</strong></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>支持中、英、日、韩、法、德等33种主流语言</p><a id="accordion-所有支持语言"></a><section><p>所有支持语言</p><div><p>中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。</p></div></section></td><td rowspan="2"><p>JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64）</p></td><td rowspan="2"><p>MP4, AVI, MOV（仅支持URL）</p></td><td><p>一次请求中传入内容元素总数不超过 20。图片数量不超过10，视频数量不超过1。</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>支持中、英、日、韩、法、德等11种主流语言</p><a id="accordion-所有支持语言-2"></a><section><p>所有支持语言</p><div><p>中文、英语、日语、韩语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、印尼语</p></div></section></td><td><p>一次请求内，图片、文本、视频、融合对象每种类型最多出现 1 次。</p></td></tr><tr><td colspan="5"><strong>多模态向量模型</strong></td></tr><tr><td><strong>模型</strong></td><td><strong>文本</strong></td><td><strong>图片</strong></td><td><strong>视频</strong></td><td><strong>单次请求条数</strong></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td rowspan="2"><p>支持中、英、日、韩等超30种主流语言</p><a id="accordion-所有支持语言-3"></a><section><p>所有支持语言</p><div><p>中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。</p></div></section></td><td rowspan="2"><p>JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64）</p></td><td rowspan="2"><p>MP4, MPEG, MOV, MPG, WEBM, AVI, FLV, MKV（仅支持URL）</p></td><td rowspan="2"><p>一次请求中传入内容元素总数不超过 20，单次图片总数不超过64，视频数量不超过8。</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td rowspan="2"><p>中文与英文</p></td><td rowspan="2"><p>JPG, PNG, BMP (支持URL或Base64)</p></td><td rowspan="3"><p>MP4, MPEG, MOV, MPG, WEBM, AVI, FLV, MKV（仅支持URL）</p></td><td rowspan="2"><p>暂无传入内容元素数量限制，输入内容Token数不超过单批次处理Token数量上限即可。</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>中文与英文</p></td><td><p>JPG, PNG, BMP (支持URL或Base64)</p></td><td><p>一次请求中传入内容元素总数不超过 20；图片、视频各最多 1 条，文本最多 20 条，共享总条数上限。</p></td></tr></tbody></table>

> 所有模型均支持 text、image、video 三种输入类型及其组合。 `tongyi-embedding-vision-plus` 、 `tongyi-embedding-vision-flash` 、`tongyi-embedding-vision-plus-2026-03-06` 和 `tongyi-embedding-vision-flash-2026-03-06` 额外支持 `multi_images` 多图序列输入。

<a id="模型能力对照"></a>

<a id="mt02a3b4c5d6e"></a>

### 模型能力对照

<table><tbody><tr><td><p><strong>模型</strong></p></td><td><p><strong>默认维度</strong></p></td><td><p><strong>向量类型</strong></p></td><td><p><strong>支持的输入</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>qwen3-vl-embedding</p></td><td><p>2560</p></td><td><p>独立 / 融合</p></td><td><p>text、image、video、多个 image 条目</p></td><td><p>通过 <code>enable_fusion</code> 参数开启融合模式，可将多模态输入融合为 1 个向量</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>1024</p></td><td><p>仅融合</p></td><td><p>text、image、video</p></td><td><p>始终返回 1 个融合向量，不支持独立向量，不支持多图输入</p></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td><p>1152</p></td><td rowspan="2"><p>独立 / 融合</p></td><td rowspan="4"><p>text、image、video、multi_images</p></td><td rowspan="2"><p>基于 Qwen3 底座，支持多分辨率、30+ 语言、融合向量</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td><td><p>768</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>1152</p></td><td rowspan="3"><p>仅独立</p></td><td rowspan="2"><p>支持 multi_images 多图序列（最多 8 张）</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>768</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>1024</p></td><td><p>text、image、video</p></td><td><p>不支持 dimension 参数，固定 1024 维</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="f8fe5c677bv6q"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](../../preparations/install-sdk.md)。

<a id="http调用"></a>

<a id="7f18c3fe662s1"></a>

## HTTP调用

`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`

<table><tbody><tr><td><a id="5043fa882c26r"></a><h3>请求</h3></td><td rowspan="7"><a id="sec-tabs-2"></a><section><a id="多模态独立向量"></a><section><a id="多模态独立向量-h4"></a><h4>多模态独立向量</h4><blockquote><p>以下示例使用 <code>tongyi-embedding-vision-plus</code> 模型生成独立向量（每个输入各自生成 1 个向量），也可替换为其他模型名称。其中 <code>multi_images</code> 类型仅 <code>tongyi-embedding-vision-plus</code> 和 <code>tongyi-embedding-vision-flash</code> 支持。<code>qwen3-vl-embedding</code> 额外支持融合向量模式，通过设置 <code>enable_fusion=true</code> 开启，详见&quot;多模态融合向量&quot;标签页。</p></blockquote><a id="code-block"></a><pre class="language-bash"><code>curl --silent --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;tongyi-embedding-vision-plus&quot;,
        &quot;input&quot;: {
            &quot;contents&quot;: [
                {&quot;text&quot;: &quot;多模态向量模型&quot;},
                {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;},
                {&quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;},
                {&quot;multi_images&quot;: [
                    &quot;https://img.alicdn.com/imgextra/i2/O1CN019eO00F1HDdlU4Syj5_!!6000000000724-2-tps-2476-1158.png&quot;,
                    &quot;https://img.alicdn.com/imgextra/i2/O1CN01dSYhpw1nSoamp31CD_!!6000000005089-2-tps-1765-1639.png&quot;
                    ]
                  }
            ]
        }
    }'
</code></pre></section><a id="多模态融合向量"></a><section><a id="多模态融合向量-h4"></a><h4>多模态融合向量</h4><blockquote><p><code>qwen3-vl-embedding</code>支持融合向量生成，通过设置 <code>enable_fusion=true</code> 将所有输入融合为 1 个向量。支持文本+图片、文本+视频、多图+文本、图片+视频+文本等多种融合组合。以下示例展示多图+视频+文本的混合融合。</p></blockquote><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;qwen3-vl-embedding&quot;,
        &quot;input&quot;: {
            &quot;contents&quot;: [
                {&quot;text&quot;: &quot;商品描述文本&quot;},
                {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png&quot;},
                {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;},
                {&quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;}
            ]
        },
        &quot;parameters&quot;: {
            &quot;enable_fusion&quot;: true
        }
    }'
</code></pre></section><a id="2026-03-06-快照版本示例"></a><section><a id="2026-03-06-快照版本示例-h4"></a><h4>2026-03-06 快照版本示例</h4><blockquote><p><code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 是基于 Qwen3 底座的新版模型，支持 <code>res_level</code>（多分辨率）和 <code>max_video_frames</code>（视频帧数）参数，同时支持独立向量和融合向量生成。</p></blockquote><a id="code-block-3"></a><pre class="language-bash"><code>curl --silent --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;tongyi-embedding-vision-plus-2026-03-06&quot;,
        &quot;input&quot;: {
            &quot;contents&quot;: [
                {&quot;text&quot;: &quot;这是1个视觉多模态表征模型&quot;},
                {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png&quot;},
                {&quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;},
                {&quot;multi_images&quot;: [
                    &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png&quot;,
                    &quot;https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg&quot;
                ]}
            ]
        },
        &quot;parameters&quot;: {
            &quot;dimension&quot;: 1152,
            &quot;res_level&quot;: 1,
            &quot;max_video_frames&quot;: 64
        }
    }'
</code></pre><p>以下示例展示 2026-03-06 版本的<strong>融合向量</strong>用法：将 text、image、video 放在同一个 content 对象中，模型会将所有输入融合编码为 1 个向量（type 为 <code>fused</code>）。</p><a id="code-block-4"></a><pre class="language-bash"><code>curl --silent --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    --header 'Content-Type: application/json' \
    --data '{
        &quot;model&quot;: &quot;tongyi-embedding-vision-plus-2026-03-06&quot;,
        &quot;input&quot;: {
            &quot;contents&quot;: [
                {
                    &quot;text&quot;: &quot;这是1个视觉多模态表征模型&quot;,
                    &quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png&quot;,
                    &quot;video&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4&quot;
                }
            ]
        },
        &quot;parameters&quot;: {
            &quot;dimension&quot;: 1152
        }
    }'
</code></pre></section></section></td></tr><tr><td><a id="2319e756381fd"></a><h4>请求头（Headers）</h4></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p></td></tr><tr><td><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4></td></tr><tr><td><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。设置为<a href="multimodal-embedding-api-reference.md#3ef850b9cfgvv">模型概览</a>中的模型名称。</p></td></tr><tr><td><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入内容。</p><a id="accordion-属性"></a><section><p>属性</p><div><p>contents<code>array</code><strong>（必选）</strong></p><p>待处理的内容列表。每个元素是一个字典或者字符串，用于指定内容的类型和值。格式为{&quot;模态类型&quot;: &quot;输入字符串或图像、视频url&quot;}。支持<code>text</code>, <code>image</code>, <code>video</code>和<code>multi_images</code>四种模态类型。</p><blockquote><p><code>qwen3-vl-embedding</code> 同时支持融合向量和独立向量生成。在多模态独立向量的基础上增加 bool 类型字段 <code>enable_fusion</code>，当 <code>enable_fusion=true</code> 时返回融合向量。<code>qwen2.5-vl-embedding</code> 仅支持融合向量，不支持独立向量。<code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 同时支持独立向量和融合向量，通过将 text、image、video 放在同一个 content 对象中生成融合向量（不使用 enable_fusion 参数）。</p></blockquote><ul><li>文本：key为<code>text</code>。value为字符串形式。也可不通过dict直接传入字符串。</li><li>图片：key为<code>image</code>。value可以是公开可访问的URL，或Base64编码的Data URI。Base64格式为 <code>data:image/{format};base64,{data}</code>，其中 <code>{format}</code> 是图片格式（如 <code>jpeg</code>, <code>png</code>），<code>{data}</code> 是Base64编码字符串。</li><li>多图片：仅<code>tongyi-embedding-vision-plus</code>、<code>tongyi-embedding-vision-flash</code>、<code>tongyi-embedding-vision-plus-2026-03-06</code>与<code>tongyi-embedding-vision-flash-2026-03-06</code>模型支持此类型。key为<code>multi_images</code>，value是多图序列列表，每条为一个图片，格式要求如上方所示。</li><li>视频：key为<code>video</code>，value必须是公开可访问的URL。</li></ul></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>向量处理参数。HTTP调用需包装在parameters对象中，SDK调用可直接使用以下参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>output_type</strong> <code>string</code> （可选）</p><p>用户指定输出向量表示格式，目前仅支持dense。传入其他取值时不报错，该参数被忽略，按 dense 返回。</p><p><strong>dimension</strong> <code>integer</code> （可选）</p><p>用于用户指定输出向量维度。不同模型支持的值不同：</p><ul><li><code>qwen3-vl-embedding</code> 支持 2560、2048、1536、1024、768、512、256，默认值为 2560；</li><li><code>qwen2.5-vl-embedding</code> 支持 2048、1024、768、512，默认值为 1024；</li><li><code>tongyi-embedding-vision-plus</code> 支持 64、128、256、512、1024、1152，默认值为 1152；</li><li><code>tongyi-embedding-vision-flash</code> 支持 64、128、256、512、768，默认值为 768；</li><li><code>tongyi-embedding-vision-plus-2026-03-06</code> 支持 64、128、256、512、1024、1152，默认值为 1152；</li><li><code>tongyi-embedding-vision-flash-2026-03-06</code> 支持 64、128、256、512、768，默认值为 768；</li><li><code>multimodal-embedding-v1</code> 不支持此参数，固定返回 1024 维向量。</li></ul><p><strong>fps</strong> <code>float</code> （可选）</p><p>控制视频的帧数，比例越小，实际抽取的帧数越少，范围为 [0,1]。默认值为1.0。取值超出该范围时不报错。</p><p><strong>instruct</strong> <code>string</code> （可选）</p><p>添加自定义任务说明，可用于指导模型理解查询意图。建议使用英文撰写，通常可带来约 1%–5% 的效果提升。</p><p><strong>enable_fusion</strong> <code>bool</code> （可选）</p><p>是否生成融合向量。仅 <code>qwen3-vl-embedding</code> 模型支持该参数。设置为 <code>true</code> 时，将 contents 中的所有多模态内容融合为 1 个向量；默认为 <code>false</code>，各模态独立生成向量。融合向量支持文本+图片、文本+视频、多图+文本（传入多个 image 条目）、图片+视频+文本等组合，适用于需要综合理解多模态内容的检索场景。</p><blockquote><p><code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 不使用该参数，而是通过将 text、image、video 放在同一个 content 对象中来生成融合向量。</p></blockquote><p><strong>res_level</strong> <code>integer</code> （可选）</p><p>指定输入分辨率档位，支持设置 0/1/2/3 四档，对应的单图 token 分别是 127/402/578/1026，默认值为 1（402 token）。仅 <code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 模型支持该参数。对于 IPC/自驾/视觉文字等图像分辨率敏感的场景，高分辨率（res_level=3）可提升 5%-10% 效果。</p><p><strong>max_video_frames</strong> <code>integer</code> （可选）</p><p>控制视频的最大采样帧数上限，最大不超过 64，默认值为 8。仅 <code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 模型支持该参数。</p></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9ea3a66e2a0uv"></a><h3>响应</h3></td><td rowspan="6"><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;embeddings&quot;: [
            {
                &quot;index&quot;: 0,
                &quot;embedding&quot;: [
                    -0.026611328125,
                    -0.016571044921875,
                    -0.02227783203125,
                    ...
                ],
                &quot;type&quot;: &quot;text&quot;
            },
            {
                &quot;index&quot;: 1,
                &quot;embedding&quot;: [
                    0.051544189453125,
                    0.007717132568359375,
                    0.026611328125,
                    ...
                ],
                &quot;type&quot;: &quot;image&quot;
            },
            {
                &quot;index&quot;: 2,
                &quot;embedding&quot;: [
                    -0.0217437744140625,
                    -0.016448974609375,
                    0.040679931640625,
                    ...
                ],
                &quot;type&quot;: &quot;video&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 903,
        &quot;input_tokens_details&quot;: {
            &quot;image_tokens&quot;: 896,
            &quot;text_tokens&quot;: 7
        },
        &quot;output_tokens&quot;: 3,
        &quot;total_tokens&quot;: 906
    },
    &quot;request_id&quot;: &quot;1fff9502-a6c5-9472-9ee1-73930fdd04c5&quot;
}
</code></pre><div><div><p><strong>说明</strong>不同模型返回的 <code>usage</code> 字段存在差异，请参考以下说明：</p><ul><li><code>tongyi-embedding-vision-*</code> 系列模型：返回 <code>input_tokens</code>（含文本和图片 Token 总和）、<code>input_tokens_details</code>（含 <code>image_tokens</code> 和 <code>text_tokens</code>）、<code>output_tokens</code>、<code>total_tokens</code>。以上响应示例对应此类模型。</li><li><code>qwen3-vl-embedding</code>：仅返回 <code>input_tokens</code>（仅含文本 Token，包括系统模板 Token）、<code>image_tokens</code>、<code>total_tokens</code>（= <code>input_tokens</code> + <code>image_tokens</code>）。不返回 <code>input_tokens_details</code> 和 <code>output_tokens</code>。示例：</li></ul></div></div><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 43,
        &quot;image_tokens&quot;: 1247,
        &quot;total_tokens&quot;: 1290
    }
}
</code></pre><div><div><p><strong>说明</strong></p><ul><li><code>qwen2.5-vl-embedding</code>：仅返回 <code>input_tokens</code> 和 <code>image_tokens</code>，不返回 <code>total_tokens</code>、<code>input_tokens_details</code> 和 <code>output_tokens</code>。</li><li><code>multimodal-embedding-v1</code>：返回 <code>input_tokens</code>、<code>image_tokens</code>、<code>image_count</code> 和 <code>duration</code>，不返回 <code>total_tokens</code>、<code>input_tokens_details</code> 和 <code>output_tokens</code>。</li></ul></div></div></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1&quot;
}
</code></pre><p>本 API 常见的错误码及排查方向如下。完整错误码请参见<a href="../../preparations/error-code.md">通用错误码</a>。</p><table><thead><tr><th><p><strong>错误码</strong></p></th><th><p><strong>HTTP 状态码</strong></p></th><th><p><strong>触发条件</strong></p></th><th><p><strong>排查建议</strong></p></th></tr></thead><tbody><tr><td><p><code>InvalidApiKey</code></p></td><td><p>401</p></td><td><p>API Key 无效或已过期，返回 <code>Invalid API-key provided.</code></p></td><td><p>确认 <code>Authorization</code> 请求头为 <code>Bearer sk-xxx</code> 格式，且使用的是当前账号下有效的 API Key。</p></td></tr><tr><td><p><code>BadRequest.EmptyModel</code></p></td><td><p>400</p></td><td><p>请求中缺少 <code>model</code> 字段，返回 <code>Required parameter model missing from request.</code></p></td><td><p>在请求体中补充 <code>model</code> 字段，取值使用本文模型列表中的模型名称。</p></td></tr><tr><td><p><code>InvalidParameter</code></p></td><td><p>400</p></td><td><p><code>model</code> 取值不存在，返回 <code>Model not exist.</code></p></td><td><p>核对 <code>model</code> 拼写，并确认该模型在当前地域的模型列表中已列出。</p></td></tr><tr><td><p><code>InvalidParameter</code></p></td><td><p>400</p></td><td><p><code>input.contents</code> 缺失或为空数组，返回 <code>input can not be empty: input.contents</code> 或 <code>contents input can not be empty: input.contents</code>。tongyi-embedding-vision 系列模型（含 2026-03-06 快照版本）不校验该项，返回 200 和空向量数组</p></td><td><p>确认 <code>input.contents</code> 存在且为非空数组，数组中每个元素包含有效的 <code>text</code>、<code>image</code> 或 <code>video</code> 键。</p></td></tr><tr><td><p><code>InvalidParameter</code></p></td><td><p>400</p></td><td><p><code>dimension</code> 取值不在所选模型支持的向量维度范围内。</p></td><td><p>按本文模型列表中该模型支持的向量维度取值；<code>multimodal-embedding-v1</code> 不支持 <code>dimension</code> 参数，固定为 1024 维。</p></td></tr><tr><td><p><code>BadRequest</code></p></td><td><p>400</p></td><td><p><code>input.contents</code> 元素取值类型错误，如 <code>text</code> 传入数字。</p></td><td><p>按本文请求参数说明修正元素取值类型，例如 <code>text</code> 的取值应为字符串。</p></td></tr><tr><td><p><code>InternalError.Algo</code></p></td><td><p>500</p></td><td><p>服务端内部处理失败。</p></td><td><p>检查请求体结构，确认 <code>input</code> 及 <code>input.contents</code> 字段存在且元素格式符合本文请求参数说明；结构无误仍持续报错时，携带 <code>request_id</code> 联系技术支持。</p></td></tr></tbody></table></section></section></td></tr><tr><td><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>embeddings</strong><code>array</code></p><p>向量结果列表，每个对象对应输入列表中的一个元素。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>index</strong><code>int</code></p><p>结果在输入列表中的索引。</p><p><strong>embedding</strong><code>array</code></p><p>生成的向量数组，维度取决于模型及 <code>dimension</code> 参数设置。</p><p><strong>type</strong><code>string</code></p><p>结果对应的输入类型。<code>text</code>、<code>image</code>、<code>video</code>、<code>multi_images</code> 分别对应文本、图片、视频、多图输入。以下为特殊类型： <code>fused</code> 为 <code>tongyi-embedding-vision-plus-2026-03-06</code> 和 <code>tongyi-embedding-vision-flash-2026-03-06</code> 模型返回的融合向量类型；<code>fusion</code> 为 <code>qwen3-vl-embedding</code>或<code>qwen2.5-vl-embedding</code>模型在融合向量模式下返回的类型；<code>vl</code> 为 <code>qwen3-vl-embedding</code> 模型在独立向量模式下返回的类型。</p></div></section></div></section></td></tr><tr><td><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td></tr><tr><td><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td></tr><tr><td><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td></tr><tr><td><p><strong>usage</strong><code>object</code></p><p>输出信息统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>input_tokens</strong><code>int</code></p><p>本次请求输入内容的 Token 数目。对于 <code>qwen3-vl-embedding</code> 和 <code>qwen2.5-vl-embedding</code> 模型，该值仅包含文本 Token（含系统模板 Token），不包含图片/视频 Token；对于 <code>tongyi-embedding-vision-*</code> 系列模型，该值包含文本和图片/视频 Token 的总和。</p><p><strong>input_tokens_details</strong><code>object</code></p><p>输入 Token 的详细分类信息。仅 <code>tongyi-embedding-vision-*</code> 系列模型返回此字段，<code>qwen3-vl-embedding</code>、<code>qwen2.5-vl-embedding</code> 和 <code>multimodal-embedding-v1</code> 不返回此字段。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>image_tokens</strong><code>int</code></p><p>输入内容中图片或视频等<strong>视觉部分</strong>消耗的 Token 数量，<strong>不包含文本</strong>（文本部分见 <code>text_tokens</code>）。图片消耗的 Token 数量与输入图片的分辨率有关，分辨率越高消耗的 Token 越多；若输入为视频，系统会先对视频抽帧，再基于抽帧结果计算 Token。</p><p><strong>text_tokens</strong><code>int</code></p><p>输入内容中<strong>文本部分</strong>消耗的 Token 数量（不包含图片或视频等视觉部分）。</p></div></section><p><strong>output_tokens</strong><code>int</code></p><p>本次请求输出的 Token 数目。仅 <code>tongyi-embedding-vision-*</code> 系列模型返回此字段，其他模型不返回此字段。</p><p><strong>total_tokens</strong><code>int</code></p><p>输入与输出的 Token 总数。对于 <code>qwen3-vl-embedding</code> 模型，<code>total_tokens</code> = <code>input_tokens</code> + <code>image_tokens</code>。仅 <code>qwen3-vl-embedding</code> 和 <code>tongyi-embedding-vision-*</code> 系列模型返回此字段，<code>qwen2.5-vl-embedding</code> 和 <code>multimodal-embedding-v1</code> 不返回此字段。</p><p><strong>image_tokens</strong><code>int</code></p><p>本次请求输入的图片或视频等<strong>视觉部分</strong>消耗的 Token 数量（<strong>不包含文本</strong>）。图片消耗的 Token 数量与输入图片的分辨率有关；系统会对输入视频进行抽帧处理，帧数上限受系统配置控制，随后基于处理结果计算 Token。仅 <code>qwen3-vl-embedding</code>、<code>qwen2.5-vl-embedding</code> 和 <code>multimodal-embedding-v1</code> 返回此字段（作为顶层字段），<code>tongyi-embedding-vision-*</code> 系列模型的图片 Token 包含在 <code>input_tokens_details.image_tokens</code> 中。</p><p><strong>image_count</strong><code>int</code></p><p>本次请求输入的图片数量。仅 <code>multimodal-embedding-v1</code> 返回此字段。</p><p><strong>duration</strong><code>int</code></p><p>本次请求输入的视频时长（秒）。仅 <code>multimodal-embedding-v1</code> 返回此字段。</p></div></section></td></tr></tbody></table>

<a id="sdk使用"></a>

<a id="0b996e6ff5j2a"></a>

## SDK使用

> SDK 的 input 参数对应HTTP请求体中的 input.contents，两者结构 **不一致** 。

<a id="代码示例"></a>

<a id="398d2f2a026yi"></a>

### 代码示例

<a id="sec-tabs-4"></a>

<a id="图片向量化示例"></a>

<a id="图片向量化示例-h4"></a>

#### 图片向量化示例

<a id="sec-tabs-5"></a>

<a id="使用图片url"></a>

<a id="使用图片url-h4"></a>

#### 使用图片URL

<a id="code-block-8"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
# 实际使用中请将url地址替换为您的图片url地址
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
input = [{'image': image}]
try:
    # 调用模型接口
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus",
        input=input
    )
    # 向量结果：resp.embeddings[i].embedding 为向量数组，resp.embeddings[i].index 为输入序号
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="使用本地图片"></a>

<a id="使用本地图片-h4"></a>

#### 使用本地图片

将本地图片转换为 Base64 格式后进行向量化：

<a id="code-block-9"></a>

```python
import os
import base64
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
# 读取图片并转换为Base64,实际使用中请将xxx.png替换为您的图片文件名或路径
image_path = "xxx.png"
with open(image_path, "rb") as image_file:
    # 读取文件并转换为Base64
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
# 设置图像格式
image_format = "png"  # 根据实际情况修改，比如jpg、bmp 等
image_data = f"data:image/{image_format};base64,{base64_image}"
# 输入数据
input = [{'image': image_data}]
try:
    # 调用模型接口
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus",
        input=input
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="视频向量化示例"></a>

<a id="视频向量化示例-h4"></a>

#### 视频向量化示例

> 多模态向量化模型目前仅支持以URL形式输入视频文件，暂不支持直接传入本地视频。

<a id="code-block-10"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
# 实际使用中请将url地址替换为您的视频url地址
video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"
input = [{'video': video}]
try:
    # 调用模型接口
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus",
        input=input
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="文本向量化示例"></a>

<a id="文本向量化示例-h4"></a>

#### 文本向量化示例

<a id="code-block-11"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
text = "通用多模态表征模型示例"
input = [{'text': text}]
try:
    # 调用模型接口
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus",
        input=input
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="融合向量化示例"></a>

<a id="融合向量化示例-h4"></a>

#### 融合向量化示例

<a id="code-block-12"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 多模态融合向量：将文本、图片、视频融合成一个融合向量
# 适用于跨模态检索、图搜等场景
text = "这是一段测试文本，用于生成多模态融合向量"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"

# 输入包含文本、图片、视频，通过 enable_fusion 参数生成融合向量
input_data = [
    {"text": text},
    {"image": image},
    {"video": video}
]

try:
    # 使用 qwen3-vl-embedding 生成融合向量
    resp = client.multimodal.embeddings.create(
        model="qwen3-vl-embedding",
        input=input_data,
        enable_fusion=True,
        # 可选参数：指定向量维度（支持 2560、2048、1536、1024、768、512、256，默认 2560）
        # dimension=1024
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="多图融合向量化示例"></a>

<a id="多图融合向量化示例-h4"></a>

#### 多图融合向量化示例

使用 `qwen3-vl-embedding` 将多张图片与文本融合为 1 个向量。传入多个 `image` 条目即可实现多图融合，适用于商品多角度图片与描述文本的综合语义检索。

<a id="code-block-13"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 多图+文本融合向量：将多张商品图片和描述文本融合为 1 个向量
# 适用于商品多角度图片+描述文本的综合语义检索
text = "白色运动鞋，轻量透气，适合跑步和日常穿着"
image1 = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
image2 = "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"

# 传入多个 image 条目实现多图融合，enable_fusion=True 将所有输入融合为 1 个向量
input_data = [
    {"text": text},
    {"image": image1},
    {"image": image2}
]

try:
    resp = client.multimodal.embeddings.create(
        model="qwen3-vl-embedding",
        input=input_data,
        enable_fusion=True
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="2026-03-06-快照版本示例-2"></a>

<a id="2026-03-06-快照版本示例-2-h4"></a>

#### 2026-03-06 快照版本示例

> 以下示例展示如何使用 `tongyi-embedding-vision-plus-2026-03-06` 模型，演示 `res_level` （多分辨率）和 `max_video_frames` （视频帧数）参数的使用。该模型基于 Qwen3 底座，支持 30+ 种语言，同时支持独立向量和融合向量生成。

<a id="code-block-14"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# tongyi-embedding-vision-plus-2026-03-06 示例
# 支持 res_level（多分辨率）和 max_video_frames（视频帧数）参数
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"
text = "这是1个视觉多模态表征模型"

input_data = [
    {"text": text},
    {"image": image},
    {"video": video}
]

try:
    # 调用 2026-03-06 快照版本模型
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus-2026-03-06",
        input=input_data,
        dimension=1152,      # 支持 1152/1024/512/256/128/64
        res_level=1,         # 分辨率档位：0/1/2/3，默认 1
        max_video_frames=64  # 视频最大采样帧数，默认 8，最大 64
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

2026-03-06 版本的**融合向量**用法：将 text、image、video 放在同一个 content 对象中，模型将所有输入融合为 1 个向量（type 为 `fused`）。

<a id="code-block-15"></a>

```python
import os
import dashscope
from dashscope import DashScopeError
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 融合向量：将 text/image/video 放在同一个 content 对象中
# 模型会将所有输入融合编码为 1 个向量，type 为 "fused"
text = "白色运动鞋，轻量透气，适合跑步和日常穿着"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"

# 同一对象中的多模态内容会被融合为 1 个向量
input_data = [
    {"text": text, "image": image}
]

try:
    resp = client.multimodal.embeddings.create(
        model="tongyi-embedding-vision-plus-2026-03-06",
        input=input_data,
        dimension=1152
    )
    print(resp.model_dump_json(indent=4))
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="dashscope-cli"></a>

<a id="dashscope-cli-h4"></a>

#### dashscope CLI

<a id="code-block-16"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID；该模型仅在北京和新加坡地域提供，使用新加坡时将 cn-beijing 替换为 ap-southeast-1
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope multimodal-embedding create -m tongyi-embedding-vision-plus --text "你好世界"
```

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../../preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../../preparations/base-url.md)。

<a id="输出示例"></a>

<a id="81b889218b9g2"></a>

### 输出示例

<a id="code-block-17"></a>

```json
{
    "request_id": "40532987-ba72-42aa-a178-bb58b52fb7f3",
    "embeddings": [
        {
            "index": 0,
            "embedding": [
                -0.009490966796875,
                -0.024871826171875,
                -0.031280517578125,
                ...
            ],
            "type": "text"
        }
    ],
    "usage": {
        "input_tokens": 10,
        "input_tokens_details": {
            "image_tokens": 0,
            "text_tokens": 10
        },
        "output_tokens": 1,
        "total_tokens": 11
    }
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
