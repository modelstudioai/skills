# 万相-通用图像编辑API参考

本文介绍万相-通用图像编辑模型的输入输出参数。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

该模型通过简单的指令即可实现多样化的图像编辑，适用于扩图、去水印、风格迁移、图像修复、图像美化等场景。 当前支持以下功能：

-   **图像风格化**：全局风格化、局部风格化。
-   **图像内容编辑**：指令编辑（无需指定区域，仅通过指令增加/修改图片内容）、局部重绘（针对指定区域增加/删除/修改图片内容）、去文字水印（中英文）。
-   **图像尺寸与分辨率优化**：扩图（按比例扩图）、图像超分（高清放大）。
-   **图像色彩处理**：图像上色（黑白或灰度图像转为彩色图像）。
-   **基于参考图像生成**：线稿生图（先提取输入图像的线稿，再参考线稿生成图像）、参考卡通形象生图。

**相关指南**：[图像编辑-万相2.1](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)

<a id="模型效果"></a>

<a id="2c8b6e330fjan"></a>

## 模型效果

| 模型功能 | 输入图像 | 输入提示词 | 输出图像 |
| --- | --- | --- | --- |
| **全局风格化** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930138.png) | 转换成法国绘本风格 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930139.png) |
| **局部风格化** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930188.png) | 把房子变成木板风格。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930413.png) |
| **指令编辑** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p942602.png) | 把她的头发修改为红色。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p942603.png) |
| **局部重绘** | 输入图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930416.png)<br><br>输入涂抹区域图像（白色为涂抹区域）<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930417.png) | 一只陶瓷兔子抱着一朵陶瓷花。 | 输出图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930415.png) |
| **去文字水印** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930146.png) | 去除图像中的文字。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930418.png) |
| **扩图** | ![20250319105917](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930580.jpg) | 一位绿色仙子。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930750.png) |
| **图像超分** | 模糊图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930151.png) | 图像超分。 | 清晰图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930152.png) |
| **图像上色** | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930149.png) | 蓝色背景，黄色的叶子。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930150.png) |
| **线稿生图** | 输入图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930155.png) | 北欧极简风格的客厅。 | 提取原图的线稿并生成图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930156.png) |
| **参考卡通形象生图** | 输入参考图（卡通形象）<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930153.png) | 卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。 | 输出图像<br><br>![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9206061571/p930154.png) |

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

万相-通用图像编辑API支持通过HTTP和DashScope SDK进行调用。

在调用前，您需要[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。目前，该SDK已支持Python和Java。

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

1.  **创建任务获取任务ID**：首先发起创建任务请求，该请求会返回任务ID（task\_id）。
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。

> **说明**
>
> 创建任务后，该任务将被加入到排队队列，等待调度执行。后续需要调用“根据任务ID查询结果接口”获取任务状态及结果。

> 通用图像编辑模型大约需要5-15秒。实际耗时取决于排队任务数量和网络状况，请您在获取结果时耐心等待。

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx2.1-imageedit。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>提示词，用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><blockquote><p>不同功能的提示词存在差异，建议根据具体功能参考相应的技巧说明。</p></blockquote><p><strong>function</strong><code>string</code><strong>（必选）</strong></p><p>图像编辑功能。目前支持的功能有：</p><ul><li>stylization_all：全局风格化，当前支持2种风格。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#d058c678a9iqt">风格和提示词技巧</a></li><li>stylization_local：局部风格化，当前支持8种风格。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#b65daaa5cb1c5">风格和提示词技巧</a></li><li>description_edit：指令编辑。通过指令即可编辑图像，简单编辑任务优先推荐这种方式。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#0c932e6efebf7">提示词技巧</a></li><li>description_edit_with_mask：局部重绘。需要指定编辑区域，适合对编辑范围有精确控制的场景。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#b0d2188736q4f">提示词技巧</a></li><li>remove_watermark：去文字水印。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#97cea0ec36xff">提示词技巧</a></li><li>expand：扩图。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#42a62bb11bx9n">提示词技巧</a></li><li>super_resolution：图像超分。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#04e73f5e9d728">提示词技巧</a></li><li>colorization：图像上色。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#dad8aa53ee8ng">提示词技巧</a></li><li>doodle：线稿生图。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#aec91c51deqld">提示词技巧</a></li><li>control_cartoon_feature：参考卡通形象生图。<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md#fade6eec1ctqa">提示词技巧</a></li></ul><p><strong>base_image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>输入图像的URL或 Base64 编码数据。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像分辨率：图像的宽度和高度范围为[512, 4096]像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>输入图像说明：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</li><li>示例值：<code>http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：<code>data:image/jpeg;base64,GDU7MtCZzEbTbmRZ......</code>。</li><li>示例中的编码字符串不完整，仅做演示，更多内容请参见<a href="wanx-image-edit-api-reference.md#c92c9077cbebb">传值方式</a>。</li></ul></li></ol><p><strong>mask_image_url</strong> <code>string</code> （可选）</p><p>仅当<code>function</code>设置为<code>description_edit_with_mask</code>（局部重绘）时必填，其余情况无需填写。</p><p>涂抹区域图像的URL或 Base64 编码数据。</p><p>支持传入公网可访问的 URL（HTTP/HTTPS）或 Base64 编码字符串，更多内容请参见<a href="wanx-image-edit-api-reference.md#c92c9077cbebb">传值方式</a>。</p><p>涂抹区域图像要求：</p><ul><li>图像分辨率 ：必须与<code>base_image_url</code>的图像分辨率保持一致。图像宽度和高度需在[512, 4096]像素之间。</li><li>图像格式 ：支持JPG、JPEG、PNG、BMP、TIFF、WEBP。</li><li>图像大小 ：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>涂抹区域颜色要求：</p><ul><li>白色区域 ：表示需要编辑的部分，必须使用纯白色（RGB值为[255,255,255]），否则可能无法正确识别。</li><li>黑色区域：表示无需改变的部分，必须使用纯黑色（RGB值为[0,0,0]），否则可能无法正确识别。</li></ul><p>关于如何获取涂抹区域图像：使用PS抠图或其他工具生成黑白涂抹图像。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><a id="sec-tabs"></a><section><a id="通用"></a><section><a id="通用-h4"></a><h4>通用</h4><p><strong>n</strong> <code>integer</code> （可选）</p><p>生成图片的数量。范围1~4，默认1。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制生成内容的随机性。取值范围<code>[0, 2147483647]</code>，未指定时自动生成；使用相同值可保持结果稳定。</p><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul></section><a id="全局风格化"></a><section><a id="全局风格化-h4"></a><h4>全局风格化</h4><p><strong>n</strong>、<strong>seed</strong>、<strong>watermark</strong></p><p>说明见通用参数。</p><p><strong>strength</strong> <code>float</code> （可选）</p><p>当<code>function</code>设置为 <code>stylization_all</code>（全局风格化）时填写。</p><p>图像修改幅度。范围[0.0, 1.0]，默认0.5。</p><p>值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。</p></section><a id="指令编辑"></a><section><a id="指令编辑-h4"></a><h4>指令编辑</h4><p><strong>n</strong>、<strong>seed</strong>、<strong>watermark</strong></p><p>说明见通用参数。</p><p><strong>strength</strong> <code>float</code> （可选）</p><p>当<code>function</code>设置为<code>description_edit</code>（指令编辑）时填写。</p><p>图像修改幅度。范围[0.0, 1.0]，默认0.5。</p><p>值越接近0，则越接近原图效果；值越接近1，对原图的修改幅度越大。</p></section><a id="扩图"></a><section><a id="扩图-h4"></a><h4>扩图</h4><p><strong>n</strong>、<strong>seed</strong>、<strong>watermark</strong></p><p>说明见通用参数。</p><p><strong>top_scale</strong> <code>float</code>（可选）</p><p>当<code>function</code>设置为<code>expand</code>（扩图）时才需填写。</p><p>向上扩展比例，默认1.0，范围[1.0, 2.0]。</p><p><strong>bottom_scale</strong> <code>float</code>（可选）</p><p>当<code>function</code>设置为<code>expand</code>（扩图）时才需填写。</p><p>向下扩展比例，默认1.0，范围[1.0, 2.0]。</p><p><strong>left_scale</strong> <code>float</code>（可选）</p><p>当<code>function</code>设置为<code>expand</code>（扩图）时才需填写。</p><p>向左扩展比例，默认1.0，范围[1.0, 2.0]。</p><p><strong>right_scale</strong> <code>float</code>（可选）</p><p>当<code>function</code>设置为<code>expand</code>（扩图）时才需填写。</p><p>向右扩展比例，默认1.0，范围[1.0, 2.0]。</p></section><a id="图像超分"></a><section><a id="图像超分-h4"></a><h4>图像超分</h4><p><strong>n</strong>、<strong>seed</strong>、<strong>watermark</strong></p><p>说明见通用参数。</p><p><strong>upscale_factor</strong> <code>integer</code>（可选）</p><p>当<code>function</code>设置为<code>super_resolution</code>（图像超分）时才需填写。</p><p>图像超分的放大倍数。在放大图像的同时增强细节，提升图像分辨率，实现高清处理。</p><p>范围1~4，默认1。当设置为1时，仅进行高清处理，不放大。</p></section><a id="线稿生图"></a><section><a id="线稿生图-h4"></a><h4>线稿生图</h4><p><strong>n</strong>、<strong>seed</strong>、<strong>watermark</strong></p><p>说明见通用参数。</p><p><strong>is_sketch</strong> <code>bool</code> （可选）</p><p>当<code>function</code>设置为<code>doodle</code>（线稿生图）时才需填写。</p><p>输入图像是否为线稿图像。</p><ul><li>false：默认值，输入图像不为线稿图像。模型会先从输入图像中提取线稿，再参考提取的线稿生成新的图像。</li><li>true：输入图像为线稿图像。模型将直接基于输入图像生成图像，适用于涂鸦作画场景。</li></ul></section></section></div></section></td><td><a id="sec-tabs-2"></a><section><a id="全局风格化-2"></a><section><a id="全局风格化-2-h4"></a><h4>全局风格化</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;stylization_all&quot;,
    &quot;prompt&quot;: &quot;转换成法国绘本风格&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="传入本地文件-base64"></a><section><a id="传入本地文件-base64-h4"></a><h4>传入本地文件（base64）</h4><p>下面以全局风格化为例，展示Base64传参示例。</p><p>由于 Base64 编码后的字符串较长，请下载<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/lzyoev/stylization_image_base64.txt">image_base64</a>，并将文本内容全部复制到<code>base_image_url</code>参数中。</p><p>数据格式详见<a href="wanx-image-edit-api-reference.md#c92c9077cbebb">传值方式</a>。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;stylization_all&quot;,
    &quot;prompt&quot;: &quot;转换成法国绘本风格&quot;,
    &quot;base_image_url&quot;: &quot;data:image/jpeg;base64,/9j/4AAQSkZJR......&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="局部风格化"></a><section><a id="局部风格化-h4"></a><h4>局部风格化</h4><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;stylization_local&quot;,
    &quot;prompt&quot;: &quot;把房子变成木板风格。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/stylization_local_1.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="指令编辑-2"></a><section><a id="指令编辑-2-h4"></a><h4>指令编辑</h4><p>无需指定区域，通过指令即可增加/修改图片内容。</p><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;description_edit&quot;,
    &quot;prompt&quot;: &quot;把她的头发修改为红色。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/description_edit_2.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="局部重绘"></a><section><a id="局部重绘-h4"></a><h4>局部重绘</h4><p>针对指定区域,可增加/删除/修改图片内容。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;description_edit_with_mask&quot;,
    &quot;prompt&quot;: &quot;陶瓷兔子拿着陶瓷小花。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg&quot;,
    &quot;mask_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="去文字水印"></a><section><a id="去文字水印-h4"></a><h4>去文字水印</h4><p>可去除中英文文字水印。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;remove_watermark&quot;,
    &quot;prompt&quot;: &quot;去除图像中的文字&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/remove_watermark_1.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="扩图-2"></a><section><a id="扩图-2-h4"></a><h4>扩图</h4><p>支持在上下左右四个方向按比例扩图。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;expand&quot;,
    &quot;prompt&quot;: &quot;一位绿色仙子&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/expand_2.jpg&quot;
  },
  &quot;parameters&quot;: {
    &quot;top_scale&quot;: 1.5,
    &quot;bottom_scale&quot;: 1.5,
    &quot;left_scale&quot;: 1.5,
    &quot;right_scale&quot;: 1.5,
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="图像超分-2"></a><section><a id="图像超分-2-h4"></a><h4>图像超分</h4><p>支持将模糊图像进行高清放大。</p><a id="code-block-8"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;super_resolution&quot;,
    &quot;prompt&quot;: &quot;图像超分。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/super_resolution_1.jpeg&quot;
  },
  &quot;parameters&quot;: {
    &quot;upscale_factor&quot;: 2,
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="图像上色"></a><section><a id="图像上色-h4"></a><h4>图像上色</h4><p>支持将黑白或灰度图像转为彩色图像。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;colorization&quot;,
    &quot;prompt&quot;: &quot;蓝色背景，黄色的叶子。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/colorization_1.jpeg&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="线稿生图-2"></a><section><a id="线稿生图-2-h4"></a><h4>线稿生图</h4><p>先提取输入图像的线稿，再参考该线稿生成图像。</p><a id="code-block-10"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;doodle&quot;,
    &quot;prompt&quot;: &quot;北欧极简风格的客厅。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/doodle_1.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section><a id="参考卡通形象生图"></a><section><a id="参考卡通形象生图-h4"></a><h4>参考卡通形象生图</h4><p>支持参考卡通形象生成图像。</p><a id="code-block-11"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx2.1-imageedit&quot;,
  &quot;input&quot;: {
    &quot;function&quot;: &quot;control_cartoon_feature&quot;,
    &quot;prompt&quot;: &quot;卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。&quot;,
    &quot;base_image_url&quot;: &quot;http://wanx.alicdn.com/material/20250318/control_cartoon_feature_1.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;n&quot;: 1
  }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-13"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><a id="code-block-14"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong> <code>array object</code></p><p>任务结果列表，包括图像URL、部分任务执行失败报错信息等。</p><a id="accordion-数据结构"></a><section><p>数据结构</p><div><a id="code-block-15"></a><pre class="language-json"><code>{
    &quot;results&quot;: [
        {
            &quot;url&quot;: &quot;&quot;
        },
        {
            &quot;code&quot;: &quot;&quot;,
            &quot;message&quot;: &quot;&quot;
        }
    ]
}
</code></pre></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-16"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;eeef0935-02e9-9742-bb55-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;a425c46f-dc0a-400f-879e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-02-21 17:56:31.786&quot;,
        &quot;scheduled_time&quot;: &quot;2025-02-21 17:56:31.821&quot;,
        &quot;end_time&quot;: &quot;2025-02-21 17:56:42.530&quot;,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/aaa.png&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 1,
            &quot;SUCCEEDED&quot;: 1,
            &quot;FAILED&quot;: 0
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-17"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;xxxxxx&quot;,
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 4,
            &quot;SUCCEEDED&quot;: 0,
            &quot;FAILED&quot;: 4
        }
    }
}
</code></pre></section><a id="任务部分失败"></a><section><a id="任务部分失败-h4"></a><h4>任务部分失败</h4><p>模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为<code>SUCCEEDED</code>，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-18"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;85eaba38-0185-99d7-8d16-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png&quot;
            },
            {
                &quot;code&quot;: &quot;InternalError.Timeout&quot;,
                &quot;message&quot;: &quot;An internal timeout error has occured during execution, please try again later or contact service support.&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 2,
            &quot;SUCCEEDED&quot;: 1,
            &quot;FAILED&quot;: 1
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="db17b3098c2iv"></a>

## DashScope SDK调用

请先确认已[安装最新版DashScope SDK](../../preparations/install-sdk.md)，否则可能导致运行报错。

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据不同语言的SDK封装而定。参数说明可参考[HTTP调用](../../../_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md#42703589880ts)。

由于视频模型处理时间较长，底层服务采用异步方式提供。SDK在上层进行了封装，支持同步、异步两种调用方式。

> 通用图像编辑模型大约需要5-15秒。实际耗时取决于排队任务数量和网络状况，请您在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="a3ad9a3b6d9if"></a>

### Python SDK调用

> **重要**
>
> **本示例要求 dashscope Python SDK ≥ 2.0.1。**请先执行 **pip install -U "dashscope>=2.0.1"** 升级 SDK 后再运行示例。

使用Python SDK处理图像文件时，支持以下三种方式输入图像。请根据您的场景选择其中一种即可。

1.  公网 URL：公网可访问的图像 URL（HTTP/HTTPS）。您可在此[获取临时公网URL](../../more-about-models/get-temporary-file-url.md)。
2.  Base64编码：传入Base64编码文件后的字符串，格式为`data:{MIME_type};base64,{base64_data}`。
3.  本地文件路径：支持传入文件的**绝对路径和相对路径**。请参考下表，传入正确的文件路径。

<table><thead><tr><th><p><strong>系统</strong></p></th><th><p><strong>传入的文件路径</strong></p></th><th><p><strong>示例（绝对路径）</strong></p></th><th><p><strong>示例（相对路径）</strong></p></th></tr></thead><tbody><tr><td><p>Linux或macOS系统</p></td><td rowspan="2"><p>file://{文件的绝对路径或相对路径}</p></td><td><p>file:///home/images/test.png</p></td><td><p>file://./images/test.png</p></td></tr><tr><td><p>Windows系统</p></td><td><p>file://D:/images/test.png</p></td><td><p>file://./images/test.png</p></td></tr></tbody></table>

<a id="示例代码"></a>

<a id="f2b1639e488og"></a>

#### 示例代码

> **说明**
>
> 在调用代码前，请确保已安装 DashScope Python SDK，推荐升级至最新版本：`pip install -U dashscope`，详见[安装SDK](../../preparations/install-sdk.md)。

<a id="sec-tabs-6"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="3cd4969b00193"></a>

##### 请求示例

<a id="code-block-19"></a>

```python
import base64
import os
import mimetypes
import dashscope
from dashscope import DashScopeError

"""
环境要求：
    dashscope python SDK >= 2.0.1
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# mask_image_url = "file://" + "/path/to/your/mask_image.png"     # Linux/macOS
# base_image_url = "file://" + "C:/path/to/your/base_image.jpeg"  # Windows
# 示例（相对路径）：
# mask_image_url = "file://" + "./mask_image.png"                 # 以实际路径为准
# base_image_url = "file://" + "./base_image.jpeg"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# mask_image_url = encode_file("./mask_image.png")               # 以实际路径为准
# base_image_url = encode_file("./base_image.jpeg")              # 以实际路径为准

def sample_sync_call_imageedit():
    print('please wait...')
    try:
        # generate 为“提交+等待”一步式调用，返回已完成的任务对象 job
        job = client.images.generate(
            model="wanx2.1-imageedit",
            function="description_edit_with_mask",
            prompt="陶瓷兔子拿着陶瓷小花",
            # base_image_url/mask_image_url 为编辑专属入参，经 extra_input 透传到请求 input 段
            extra_input={
                "mask_image_url": mask_image_url,
                "base_image_url": base_image_url,
            },
            n=1,
        )
        print('response: %s' % job)
        for url in job.image_urls:
            print("---------------------------")
            print(url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_imageedit()
```

<a id="0c0533477emwb"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-20"></a>

```json
{
    "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
    "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

本示例仅展示异步调用方式。

<a id="b994ca9918t7e"></a>

##### 请求示例

<a id="code-block-21"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

"""
环境要求：
    dashscope python SDK >= 2.0.1
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 使用公网图片 URL
mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

def sample_async_call_imageedit():
    try:
        # 异步调用（分步提交），返回一个job对象，含task_id
        job = client.images.jobs.create(
            model="wanx2.1-imageedit",
            function="description_edit_with_mask",
            prompt="陶瓷兔子拿着陶瓷小花",
            # base_image_url/mask_image_url 为编辑专属入参，经 extra_input 透传到请求 input 段
            extra_input={
                "mask_image_url": mask_image_url,
                "base_image_url": base_image_url,
            },
            n=1,
        )
        print(job)
        print("task_id: %s" % job.task_id)

        # 获取异步任务信息
        snapshot = client.images.jobs.fetch(job.task_id)
        print(snapshot.status)  # check the task status

        # 等待异步任务结束（指数退避轮询，默认总预算24小时，任务FAILED会抛出DashScopeError）
        done = client.images.jobs.wait(job.task_id)
        print(done)
        for url in done.image_urls:
            print("---------------------------")
            print(url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call_imageedit()
```

<a id="ae28dc8f72g6i"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-22"></a>

```json
{
    "request_id": "6dc3bf6c-be18-9268-9c27-xxxxxx",
    "task_id": "686391d9-7ecf-4290-a8e9-xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-23"></a>

```json
{
    "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
    "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?Expires=17xxxxxx"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

### Java SDK调用

使用Java SDK处理图像文件时，支持以下三种方式输入图像。请根据您的场景选择其中一种即可。

1.  公网 URL：公网可访问的图像 URL（HTTP/HTTPS）。您可在此[获取临时公网URL](../../more-about-models/get-temporary-file-url.md)。
2.  Base 64编码：传入Base64编码文件后的字符串，格式为`data:{MIME_type};base64,{base64_data}`。
3.  本地文件路径：仅支持传入文件的**绝对路径**。请参考下表，传入正确的文件路径。

| 系统 | 传入的文件路径 | 示例 |
| --- | --- | --- |
| Linux或macOS系统 | file://{文件的绝对路径} | file:///home/images/test.png |
| Windows系统 | file:///{文件的绝对路径} | file:///D:/images/test.png |

<a id="示例代码-2"></a>

<a id="ae42e9ea5chzu"></a>

#### 示例代码

> **说明**
>
> 在调用代码前，请确保已安装 DashScope Java SDK。推荐您升级至最新版本，详见[安装SDK](../../preparations/install-sdk.md)。

<a id="sec-tabs-7"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="36e8ee89107qx"></a>

##### 请求示例

<a id="code-block-24"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >=2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */

public class ImageEditSync {
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
    static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String maskImageUrl = "file://" + "/your/path/to/mask_image.png";    // Linux/macOS
    // static String baseImageUrl = "file:///" + "C:/your/path/to/base_image.png";  // Windows

    //【方式三】Base64编码
    // static String maskImageUrl = encodeFile("/your/path/to/mask_image.png");
    // static String baseImageUrl = encodeFile("/your/path/to/base_image.png");

    public static void syncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

<a id="75c2320e48eer"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-25"></a>

```json
{
    "request_id": "bf6c6361-f0fc-949c-9d60-xxxxxx",
    "output": {
        "task_id": "958db858-153b-4c81-b243-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

本示例仅展示异步调用方式。

<a id="49cd0bd3b7x31"></a>

##### 请求示例

<a id="code-block-26"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.1
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */

public class ImageEditAsync {
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //【方式一】公网URL
    static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
    static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

    public static void asyncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---async call, please wait a moment----");
            result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
            result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空。
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        asyncCall();
    }
}
```

<a id="13d30c3a8eq42"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-27"></a>

```json
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-xxxxxxxx",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-28"></a>

```json
{
	"request_id": "3d740fc4-a968-9c36-b0e7-xxxxxxxx",
	"output": {
		"task_id": "34dcf4b0-ed84-441e-91cb-xxxxxxxx",
		"task_status": "SUCCEEDED",
		"results": [
			{
				"url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxx.png"
			}
		],
		"submit_time": "2025-02-21 17:56:31.786",
		"scheduled_time": "2025-02-21 17:56:31.821",
		"end_time": "2025-02-21 17:56:42.530",
		"task_metrics": {
			"TOTAL": 1,
			"SUCCEEDED": 1,
			"FAILED": 0
		}
	},
	"usage": {
		"image_count": 1
	}
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

此API还有特定状态码，具体如下所示。

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidParameter | InvalidParameter | 请求参数不合法。 |
| 400 | IPInfringementSuspect | Input data is suspected of being involved in IP infringement. | 输入数据（如提示词或图像）涉嫌知识产权侵权。请检查输入，确保不包含引发侵权风险的内容。 |
| 400 | DataInspectionFailed | Input data may contain inappropriate content. | 输入数据（如提示词或图像）可能包含敏感内容。请修改输入后重试。 |
| 500 | InternalError | InternalError | 服务异常。请先尝试重试，排除偶发情况。 |

<a id="输入图像说明"></a>

<a id="b5b5df5ee6g5s"></a>

## 输入图像说明

<a id="传值方式"></a>

<a id="c92c9077cbebb"></a>

### 传值方式

输入图像支持多种字符串格式，不同调用方式的支持情况如下表所示。

<table><thead><tr><th><p><strong>调用方式</strong></p></th><th><p><strong>HTTP</strong></p></th><th><p><strong>Python SDK</strong></p></th><th><p><strong>Java SDK</strong></p></th></tr></thead><tbody><tr><td><p>支持的输入图像方式</p></td><td><ul><li><p>公网URL</p></li><li><p>Base64编码</p></li></ul></td><td><ul><li><p>公网URL</p></li><li><p>Base64编码</p></li><li><p>本地文件路径</p></li></ul></td><td><ul><li><p>公网URL</p></li><li><p>Base64编码</p></li><li><p>本地文件路径</p></li></ul></td></tr></tbody></table>

**方式一：使用公网URL**

-   提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。请在此[获取临时公网URL](../../more-about-models/get-temporary-file-url.md)。
-   示例值：`https://xxxx/img.png`。

**方式二：使用Base64编码**

将本地图片文件转换为 Base64 格式的字符串，并根据`data:{MIME_type};base64,{base64_data}`格式拼接成完整的字符串。

-   转换代码请参见[示例代码](wanx-image-edit-api-reference.md#f2b1639e488og)。
    
-   {MIME\_type}：图像的媒体类型，需与文件格式对应。
    
-   {base64\_data}：图像文件经过 Base64 编码后的字符串。
    
-   MIME 类型对应关系：
    
    | 图像格式 | MIME Type |
    | --- | --- |
    | JPEG | image/jpeg |
    | JPG | image/jpeg |
    | PNG | image/png |
    | BMP | image/bmp |
    | TIFF | image/tiff |
    | WEBP | image/webp |
    
-   示例值**：**`"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......"`**。**
    
    注意：为便于展示，上述 Base64 字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

**方式三：本地文件路径**

-   HTTP调用不支持本地文件路径，仅Python SDK和Java SDK支持。
-   关于本地文件路径的传入规则，请参见[Python SDK调用](wanx-image-edit-api-reference.md#a3ad9a3b6d9if)和[Java SDK调用](wanx-image-edit-api-reference.md#589b80853e6rn)。

<a id="常见问题"></a>

<a id="17fdffba319en"></a>

## 常见问题

图像模型的通用问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/image-faq)文档，包括以下内容：模型计费与限流规则、接口高频报错解决方法等。
