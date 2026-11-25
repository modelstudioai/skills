# DashScope API 参考

通过 DashScope API 调用千问模型，查看输入输出参数说明及调用示例。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-2"></a>

<a id="python代码"></a>

<a id="python代码-h4"></a>

#### Python代码

<a id="code-block"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
```

<a id="java代码"></a>

<a id="java代码-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-2"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-3"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
```

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-3"></a>

<a id="python代码-2"></a>

<a id="python代码-2-h4"></a>

#### Python代码

<a id="code-block-4"></a>

```python
import os
import dashscope

# 以下为新加坡地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="ap-southeast-1",
)
```

<a id="java代码-2"></a>

<a id="java代码-2-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-5"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-6"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";
```

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-4"></a>

<a id="python代码-3"></a>

<a id="python代码-3-h4"></a>

#### Python代码

<a id="code-block-7"></a>

```python
import os
import dashscope

# 以下为美国（弗吉尼亚）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="us-east-1",
)
```

<a id="java代码-3"></a>

<a id="java代码-3-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-8"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-9"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";
```

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-5"></a>

<a id="python代码-4"></a>

<a id="python代码-4-h4"></a>

#### Python代码

<a id="code-block-10"></a>

```python
import os
import dashscope

# 以下为德国（法兰克福）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="eu-central-1",
)
```

<a id="java代码-4"></a>

<a id="java代码-4-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-11"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-12"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";
```

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-6"></a>

<a id="python代码-5"></a>

<a id="python代码-5-h4"></a>

#### Python代码

<a id="code-block-13"></a>

```python
import os
import dashscope

# 以下为日本（东京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="ap-northeast-1",
)
```

<a id="java代码-5"></a>

<a id="java代码-5-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-14"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-15"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1";
```

<a id="中国香港"></a>

<a id="中国香港-h4"></a>

#### 中国香港

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用的地域配置：

<a id="sec-tabs-7"></a>

<a id="python代码-6"></a>

<a id="python代码-6-h4"></a>

#### Python代码

<a id="code-block-16"></a>

```python
import os
import dashscope

# 以下为中国香港地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-hongkong",
)
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过DashScope SDK进行调用，需要[安装DashScope SDK](../preparations/install-sdk.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<table><tbody><tr><td><a id="2a1c410015otp"></a><h2>请求体</h2><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p>支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、千问Audio、数学模型、DeepSeek（阿里云直供、硅基流动直供）、Kimi（阿里云直供）、GLM（阿里云直供）、MiniMax（阿里云直供、稀宇科技直供）。</p><p><strong>具体模型名称和计费，请参见</strong><a href="../../model-user-guide/get-started-with-models/models.md">选择模型</a>。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><blockquote><p>通过HTTP调用时，请将<strong>messages</strong>放入 <strong>input</strong> 对象中。</p></blockquote><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><blockquote><p>QwQ模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。</p></blockquote><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>消息内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为 <code>system</code> 。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>string 或 array</code><strong>（必选）</strong></p><p>消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>输入的文本。</p><p><strong>image</strong><code>string</code>（可选）</p><p>指定用于图片理解的图像文件，图像支持以下三种方式传入：</p><ul><li>公网 URL：公网可访问的图像链接</li><li>图片的 Base64 编码，格式为 <code>data:image/&lt;format&gt;;base64,&lt;data&gt;</code></li><li>本地文件：本地文件的绝对路径</li></ul><p>适用模型：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">Qwen-VL、QVQ</a></p><p>示例值：<code>{&quot;image&quot;:&quot;https://xxxx.jpeg&quot;}</code></p><p><strong>detail</strong> <code>string</code> （可选）</p><p>图片处理精度。自 Qwen4 起，Max、Plus 和 Flash 模型支持此参数。默认值为 <code>high</code>。</p><p>未传入 <code>max_pixels</code> 时：</p><ul><li><code>high</code>：按原图分辨率处理，上限为 <code>16777216</code> 像素。</li><li><code>low</code>：像素上限为 <code>2621440</code>。</li><li><code>auto</code>：与 <code>low</code> 相同。</li></ul><p>显式传入 <code>max_pixels</code> 时，以该值作为像素上限，优先于 <code>detail</code>。最大值为 <code>16777216</code>。Chat Completions 的 <code>max_pixels</code> 与 <code>image_url</code> 同级；DashScope 与 <code>image</code> 同级。</p><p>高分辨率图片使用 <code>high</code> 时，输入 Token 用量通常高于 <code>low</code>。</p><p>Chat Completions 可在 <code>image_url</code> 内或与 <code>image_url</code> 同级传入 <code>detail</code>；DashScope 与 <code>image</code> 同级传入。</p><a id="code-block-17"></a><pre class="language-json"><code>{&quot;image&quot;:&quot;https://example.com/image.jpg&quot;,&quot;detail&quot;:&quot;high&quot;}
</code></pre><p><strong>video</strong><code>array 或 string</code>（可选）</p><p>Qwen4-Max、Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5 系列以公网 URL 图像列表传入视频时，支持 4–8000 张图片；以 Base64 图像列表传入时，最多 250 张图片。</p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">Qwen-VL 或 QVQ 模型</a>传入的视频。</p><ul><li>若传入图像列表，则为<code>array</code>类型；</li><li>若传入视频文件，则为<code>string</code>类型*。*</li></ul><p>传入本地文件请参见<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#d987f8de5395x">本地文件</a>。</p><p>示例值：</p><ul><li>图像列表：<code>{&quot;video&quot;:[&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;]}</code></li><li>视频文件：<code>{&quot;video&quot;:&quot;https://xxx.mp4&quot;}</code></li></ul><p><strong>fps</strong><code>float</code>（可选）</p><p>每秒抽帧数。取值范围为 [0.1, 10]，默认值为2.0。</p><a id="accordion-功能说明"></a><section><p>功能说明</p><div><p>fps有两个功能：</p><ul><li><p>输入视频文件时，控制抽帧频率，每 f p s 1 ​秒抽取一帧。</p><blockquote><p>适用于<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">Qwen-VL 与 QVQ 模型</a>。</p></blockquote></li><li><p>告知模型相邻帧之间的时间间隔，帮助其更好地理解视频的时间动态。同时适用于输入视频文件与图像列表时。该功能同时支持视频文件和图像列表输入，适用于事件时间定位或分段内容摘要等场景。</p><blockquote><p>支持Qwen3.7、Qwen3.6、Qwen3.5、<code>Qwen3-VL</code>、<code>Qwen2.5-VL</code>与QVQ模型。</p></blockquote></li></ul><p>较大的<code>fps</code>适合高速运动的场景（如体育赛事、动作电影等），较小的<code>fps</code>适合长视频或内容偏静态的场景。</p></div></section><a id="accordion-示例值"></a><section><p>示例值</p><div><ul><li>图像列表传入：<code>{&quot;video&quot;:[&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;]，&quot;fps&quot;:2}</code></li><li>视频文件传入：<code>{&quot;video&quot;: &quot;https://xx1.mp4&quot;，&quot;fps&quot;:2}</code></li></ul></div></section><p><strong>max_frames</strong><code>integer</code>（可选）</p><p>视频抽取帧数的上限。当按<code>fps</code>计算的帧数超过 <code>max_frames</code>时，系统将自动调整为：在<code>max_frames</code>内均匀抽帧，确保总帧数不超过限制。</p><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li>qwen3.7系列、qwen3.6系列、qwen3.5系列：最大值和默认值均为 8000。</li><li><code>qwen3-vl-plus</code>系列：最大值和默认值均为 2000。</li></ul></div></section><a id="accordion-示例值-2"></a><section><p>示例值</p><div><p><code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;max_frame&quot;: 2000}</code></p></div></section><blockquote><p>使用 OpenAI 兼容API调用时，不支持自定义<code>max_frames</code>参数，API 将自动使用各模型对应的默认值。</p></blockquote><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>设定输入图像或视频帧的最小像素阈值。当输入图像或视频帧的像素小于<code>min_pixels</code>时，会将其进行放大，直到总像素高于<code>min_pixels</code>。</p><a id="accordion-取值范围-2"></a><section><p>取值范围</p><div><ul><li><strong>输入图像：</strong><ul><li><code>qwen4-max</code>、<code>Qwen3.7、Qwen3.6、Qwen3.5</code>、<code>Qwen3-VL</code>：默认值和最小值均为：<code>65536</code></li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值和最小值均为<code>3136</code></li></ul></li><li><strong>输入视频文件或图像列表：</strong><ul><li><code>qwen4-max</code>、<code>qwen3-omni-flash</code>、<code>qwen3-vl-plus</code>、<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.5-omni-flash</code>、<code>qwen3.5-omni-flash-2026-03-15</code>、<code>qwen3.5-omni-plus</code>、<code>qwen3.5-omni-plus-2026-03-15</code>、<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.6-27b</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-omni-flash</code>：默认值为 <code>65536</code>，最小值为 <code>4096</code>。</li><li><code>kimi-k2.5</code>、<code>kimi-k2.6</code>、<code>kimi-k2.7-code</code>：最小值为 <code>3136</code>。</li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值为<code>50176</code>，最小值为<code>3136</code></li></ul></li></ul></div></section><a id="accordion-示例值-3"></a><section><p>示例值</p><div><ul><li>输入图像：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;min_pixels&quot;: 65536}</code></li><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;min_pixels&quot;: 65536}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;min_pixels&quot;: 65536}</code></li></ul></div></section><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。</p><a id="accordion-取值范围-3"></a><section><p>取值范围</p><div><ul><li><strong>输入图像：</strong><ul><li><code>qwen4-max</code>：最大值为 <code>16777216</code>。未传入时按 <code>detail</code> 处理图像；显式传入的 <code>max_pixels</code> 不受 <code>vl_high_resolution_images</code> 影响。</li></ul><p>其他模型：<code>max_pixels</code> 的取值与是否开启<code>vl_high_resolution_images</code>参数有关。</p><ul><li><p>当<code>vl_high_resolution_images</code>为<code>False</code>时：</p><ul><li><code>Qwen3.7、Qwen3.6、Qwen3.5</code>、<code>Qwen3-VL</code>：默认值为<code>2621440</code>，最大值为：<code>16777216</code></li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值为<code>1003520</code> ，最大值为<code>12845056</code></li></ul></li><li><p>当<code>vl_high_resolution_images</code>为<code>True</code>时：</p><ul><li><code>Qwen3.7、Qwen3.6、Qwen3.5</code>、Qwen3-VL：<code>max_pixels</code>无效，输入图像的最大像素固定为<code>16777216</code></li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：<code>max_pixels</code>无效，输入图像的最大像素固定为<code>12845056</code></li></ul></li></ul></li><li><strong>输入视频文件或图像列表：</strong><p>同时设置 <code>min_pixels</code> 和 <code>max_pixels</code> 时，<code>max_pixels</code> 不得小于 <code>min_pixels</code>。</p><ul><li><code>qwen4-max</code>、<code>qwen3-vl-plus</code>、<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.5-omni-flash</code>、<code>qwen3.5-omni-flash-2026-03-15</code>、<code>qwen3.5-omni-plus</code>、<code>qwen3.5-omni-plus-2026-03-15</code>、<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.6-27b</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-flash</code>、<code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>、<code>qwen3.8-omni-flash</code>：默认值为 <code>655360</code>，最大值为 <code>2048000</code>。</li><li><code>qwen3-omni-flash</code>：默认值为 <code>655360</code>，最大值为 <code>786432</code>。</li><li><code>kimi-k2.5</code>、<code>kimi-k2.6</code>、<code>kimi-k2.7-code</code>：最大值为 <code>1568000</code>。</li><li>其他<code>Qwen3-VL</code>开源模型：默认值<code>655360</code>，最大值为<code>786432</code></li><li><code>Qwen2.5-VL</code>开源系列及<code>QVQ</code>系列模型：默认值为<code>501760</code>，最大值为<code>602112</code></li></ul></li></ul></div></section><a id="accordion-示例值-4"></a><section><p>示例值</p><div><ul><li>输入图像：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;max_pixels&quot;: 8388608}</code></li><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;max_pixels&quot;: 655360}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;max_pixels&quot;: 655360}</code></li></ul></div></section><p><strong>total_pixels</strong><code>integer</code>（可选）</p><p>视频抽帧后的总像素预算。</p><a id="accordion-最大值"></a><section><p>最大值</p><div><ul><li><strong><code>268435456</code></strong>： <code>qwen4-max</code>, <code>qwen3.8-max</code>、<code>qwen3.8-max-0902</code>。</li><li><strong><code>234881024</code></strong>：<code>qwen3.5-plus</code>、<code>qwen3.5-plus-2026-02-15</code>、<code>qwen3.5-plus-2026-04-20</code>、<code>qwen3.6-plus</code>、<code>qwen3.6-plus-2026-04-02</code>、<code>qwen3.7-max-2026-06-08</code>、<code>qwen3.7-plus</code>、<code>qwen3.7-plus-2026-05-26</code>。</li><li><strong><code>819200000</code></strong>：<code>qwen3.5-122b-a10b</code>、<code>qwen3.5-27b</code>、<code>qwen3.5-35b-a3b</code>、<code>qwen3.5-397b-a17b</code>、<code>qwen3.5-flash</code>、<code>qwen3.5-flash-2026-02-23</code>、<code>qwen3.6-27b</code>、<code>qwen3.6-35b-a3b</code>、<code>qwen3.6-flash</code>、<code>qwen3.6-flash-2026-04-16</code>、<code>qwen3.7-flash</code>、<code>qwen3.7-flash-2026-07-15</code>、<code>qwen3.8-27b</code>、<code>qwen3.8-flash</code>。</li><li><strong><code>184549376</code></strong>：<code>qwen3.5-omni-flash</code>、<code>qwen3.5-omni-flash-2026-03-15</code>、<code>qwen3.5-omni-plus</code>、<code>qwen3.5-omni-plus-2026-03-15</code>、<code>qwen3.8-omni-flash</code>。</li><li><strong><code>16777216</code></strong>：<code>qwen3-omni-flash</code>。</li><li><strong><code>102760448</code></strong>：<code>kimi-k2.5</code>、<code>kimi-k2.6</code>、<code>kimi-k2.7-code</code>。</li><li><strong><code>134217728</code></strong>：<code>qwen3-vl-plus</code>。</li></ul></div></section><a id="accordion-示例值-5"></a><section><p>示例值</p><div><ul><li>输入视频文件时：<code>{&quot;type&quot;: &quot;video_url&quot;,&quot;video_url&quot;: {&quot;url&quot;:&quot;https://xxxx.mp4&quot;},&quot;total_pixels&quot;: 134217728}</code></li><li>输入图像列表时：<code>{&quot;type&quot;: &quot;video&quot;,&quot;video&quot;: [&quot;https://xx1.jpg&quot;,...,&quot;https://xxn.jpg&quot;],&quot;total_pixels&quot;: 134217728}</code></li></ul></div></section><p><strong>audio</strong><code>string</code></p><blockquote><p>模型为音频理解时，是必选参数，如模型为qwen-audio-turbo等。</p></blockquote><p>使用音频理解功能时，传入的音频文件。</p><p>示例值：<code>{&quot;audio&quot;:&quot;https://xxx.mp3&quot;}</code></p><p><strong>cache_control</strong><code>object</code><strong>（可选）</strong></p><p>仅支持<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>的模型支持，用于开启显式缓存。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code><strong>（必选）</strong></p><p>固定为<code>ephemeral</code>。</p></div></section></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section><p>Assistant Message <code>object</code>（可选）</p><p>模型对用户消息的回复。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code>（可选）</p><p>消息内容。仅当助手消息中指定<code>tool_calls</code>参数时非必选。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>assistant</code>。</p><p><strong>partial</strong><code>boolean</code>（可选）</p><p>是否开启前缀续写。相关文档与支持的模型：<a href="../../model-user-guide/model-experience/text-generation-model/partial-mode.md">前缀续写</a>。</p><p><strong>tool_calls</strong> <code>array</code>（可选）</p><p>发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的<code>tool_calls</code>字段获得。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>工具响应的ID。</p><p><strong>type</strong> <code>string</code></p><p>工具类型，当前只支持设为<code>function</code>。</p><p><strong>function</strong> <code>object</code></p><p>工具与入参信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>name</strong> <code>string</code></p><p>工具名称。</p><p><strong>arguments</strong> <code>string</code></p><p>入参信息，为JSON格式字符串。</p></div></section><p><strong>index</strong> <code>integer</code></p><p>当前工具信息在<code>tool_calls</code>数组中的索引。</p></div></section></div></section><p>Tool Message<code>object</code>（可选）</p><p>工具的输出信息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>工具函数的输出内容，必须为字符串格式。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>tool</code>。</p><p><strong>tool_call_id</strong><code>string</code><strong>（可选）</strong></p><p>发起 Function Calling 后返回的 id，可以通过<code>response.output.choices[0].message.tool_calls[$index][&quot;id&quot;]</code>获取，用于标记 Tool Message 对应的工具。</p></div></section></div></section><p><strong>temperature</strong><code>float</code>（可选）</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><a id="accordion-temperature默认值"></a><section><p>temperature默认值</p><div><ul><li><p><code>qwen4-max</code>：思考模式为 <code>1.0</code>，非思考模式为 <code>0.7</code>。</p></li><li><p>qwen3.8-max/qwen3.8-flash（思考模式）：视觉理解0.6，文本输入1.0，0.6以下的temperature值会默认改为0.6</p></li><li><p>（非思考模式）、Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen开源系列、qwen-coder系列、qwen-doc-turbo、Qwen3-VL（非思考）：0.7；</p></li><li><p>QVQ系列 : 0.5；</p></li><li><p>qwen-audio-turbo系列：0.00001；</p></li><li><p>qwen-vl系列：0.01；</p></li><li><p>qwen-math系列：0；</p></li><li><p>Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-Thinking、QwQ 系列：0.6；</p></li><li><p>qwen-long系列： 1.0；</p></li><li><p>qwen-plus-character：0.92</p></li><li><p>Qwen3-VL（思考模式）：0.8</p></li><li><p>DeepSeek系列（阿里云直供）：deepseek-v4.1-flash、deepseek-v4-pro: 1.0；deepseek-r1-distill-qwen 蒸馏版: 0.6；</p></li><li><p>DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；</p></li><li><p>DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think（思考模式）: 0.6；vanchin/deepseek-v3.1-terminus: 0.7；vanchin/deepseek-v3.2-speciale、vanchin/deepseek-r1、vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；</p></li><li><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6（思考模式）、kimi-k2.5（思考模式）: 1.0；kimi-k2.6（非思考模式）、kimi-k2.5（非思考模式）: 0.6；</p></li><li><p>Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6（思考模式）、kimi/kimi-k2.5（思考模式）: 1.0；kimi/kimi-k2.6（非思考模式）、kimi/kimi-k2.5（非思考模式）: 0.6；</p></li><li><p>GLM系列（阿里云直供）：glm-5.1、glm-5: 1.0；</p></li><li><p>GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.6；</p></li><li><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 1.0；</p></li><li><p>MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 1.0。</p></li><li><p>MiMo系列（小米直供）：mimo-v2.5-pro: 1.0，范围 [0, 1.5]；xiaomi/mimo-v2.6-pro-ultraspeed: 1.0，不支持自定义，传入其他值时仍按 1.0 生效。</p></li></ul></div></section><blockquote><p>通过HTTP调用时，请将 <strong>temperature</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 temperature 值。</p></blockquote><p><strong>top_p</strong><code>float</code>（可选）</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]。</p><a id="accordion-top-p默认值"></a><section><p>top_p默认值</p><div><ul><li><code>qwen4-max</code>：思考模式为 <code>0.95</code>，非思考模式为 <code>0.8</code>。</li></ul><p>（非思考模式）、Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、Qwen 2.5开源系列、qwen-coder系列、qwen-long、qwen-doc-turbo、Qwen3-VL（非思考）：0.8；</p><p>QVQ系列 : 0.5；</p><p>qwen-math系列：1.0；</p><p>（思考模式）、Qwen3.8（思考模式）、Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、qwen-plus-character：0.95</p><p>DeepSeek系列（阿里云直供）：deepseek-v4-pro、deepseek-r1-distill-qwen 蒸馏版: 0.95；</p><p>DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；</p><p>DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus: 0.95；vanchin/deepseek-v3.2-speciale: 0.9；vanchin/deepseek-r1: 0.8；vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；</p><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5: 0.95；</p><p>Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5: 0.95；</p><p>GLM系列（阿里云直供）：0.95；</p><p>GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.95；</p><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 0.95；</p><p>MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3: 0.95；MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 0.9。</p><p>MiMo系列（小米直供）：xiaomi/mimo-v2.5-pro: 0.95，范围 [0.01, 1.0]；xiaomi/mimo-v2.6-pro-ultraspeed: 0.95，不支持自定义，传入其他值时仍按 0.95 生效。</p></div></section><blockquote><p>Java SDK中为<strong>topP</strong>*。*通过HTTP调用时，请将 <strong>top_p</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 top_p 值。</p></blockquote><p><strong>top_k</strong><code>integer</code>（可选）</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><a id="accordion-top-k默认值"></a><section><p>top_k默认值</p><div><p>QVQ系列：10；</p><p>QwQ 系列：40；</p><p>qwen-math 系列、qwen-audio-turbo系列：1；</p><p>其余模型均为20；</p><p>GLM系列（阿里云直供）：20；</p><p>DeepSeek/Kimi/MiniMax系列均不支持top_k参数。</p></div></section><blockquote><p>Java SDK中为<strong>topK</strong>*。*通过HTTP调用时，请将 <strong>top_k</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 top_k 值。</p></blockquote><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>使用混合思考模型时，是否开启思考模式，适用于Qwen4、Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3、Qwen3-VL模型，以及 DeepSeek-V4-Pro/V4-Flash 系列（阿里云直供）、DeepSeek-V3.2/V3.2-exp/V3.1 系列（阿里云直供、硅基流动直供）、Kimi-K2.6/K2.5 系列（阿里云直供）、GLM 系列。DeepSeek-V4 系列默认开启思考，可通过 <code>reasoning_effort</code> 参数调整推理力度。</p><p>可选值：</p><ul><li><p><code>true</code>：开启</p><blockquote><p>开启后，思考内容将通过<code>reasoning_content</code>字段返回。</p></blockquote></li><li><p><code>false</code>：不开启</p></li></ul><p>不同模型的默认值：<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#78286fdc35hlw">支持的模型</a></p><blockquote><p>Java SDK 为enableThinking；通过HTTP调用时，请将 <strong>enable_thinking</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>thinking_display</strong> <code>string</code> （可选）</p><p><code>qwen4-max</code>: <code>&quot;summarized&quot;</code>. <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#enable">思维链摘要与加密</a>.</p><p>默认返回完整思维链。开启本功能后，原始思维链不再以明文返回，改为返回摘要与完整密文。摘要用于展示，密文用于恢复历史思考。</p><p><strong>preserve_thinking</strong> <code>boolean</code> （可选）默认值为 <code>false</code>（<strong>qwen4-max、qwen3.8-max/qwen3.8-flash 默认值为</strong><code>true</code>）</p><p>是否将对话历史中 assistant 消息的 reasoning_content 拼接至模型输入。适用于需要模型参考历史思考过程的场景。</p><p>kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 支持此参数，默认关闭。</p><p>目前支持qwen4-max、qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash（默认开启）、qwen3.7-max、qwen3.7-max-2026-05-20以及后续快照、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、kimi-k2.6（阿里云百炼部署）、kimi-k2.7-code（阿里云百炼部署，默认开启）、kimi/kimi-k2.7-code-highspeed（月之暗面直供，默认开启）、kimi/kimi-k2.7-code（月之暗面直供，默认开启）。</p><blockquote><p><strong>重要：</strong>使用 qwen4-max、qwen3.8-max/qwen3.8-flash 时，preserve_thinking 默认为 true，必须将历史对话中所有的 reasoning_content 完整回传。<strong>不支持将 reasoning_content 拼接到 content 字段中回传。</strong></p></blockquote><ul><li>若历史消息中不包含 reasoning_content，开启此参数不会报错，正常兼容。</li><li>开启后，历史对话中的 reasoning_content 会计入输入 Token 数量并计费。</li></ul><blockquote><p>通过HTTP调用时，请将 <strong>preserve_thinking</strong> 放入 <strong>parameters</strong> 对象中。暂不支持 Java SDK。</p></blockquote><p><strong>thinking_budget</strong> <code>integer</code> （可选）</p><p>思考过程的最大长度。适用于Qwen4、Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（阿里云直供）、Kimi（阿里云直供）系列模型，其中 kimi-k3 和 kimi-k3.1-pro 不支持该参数。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#e7c0002fe4meu">限制思考长度</a>。 <code>qwen4-max</code> 的默认值为 <code>131072</code>。</p><p>其他模型: 默认值为模型最大思维链长度，请参见：<a href="../../model-user-guide/get-started-with-models/models.md">选择模型</a></p><blockquote><p>Java SDK 为 thinkingBudget。通过HTTP调用时，请将 <strong>thinking_budget</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>其他模型: 默认值为模型最大思维链长度。</p></blockquote><p><strong>reasoning_effort</strong> <code>string</code> （可选）</p><p><strong><code>qwen4-max</code></strong></p><p>默认值: <code>reasoning_effort=high</code>.</p><table><thead><tr><th><code>reasoning_effort</code></th><th>实际档位</th></tr></thead><tbody><tr><td><code>minimal</code>, <code>low</code></td><td><code>low</code></td></tr><tr><td><code>medium</code>, <code>high</code></td><td><code>high</code></td></tr><tr><td><code>xhigh</code>, <code>max</code></td><td><code>xhigh</code></td></tr><tr><td><code>none</code></td><td>关闭思考</td></tr></tbody></table><p><code>qwen4-max</code> 不支持同时设置 <code>reasoning_effort</code> 和 <code>thinking_budget</code>。<code>thinking_budget</code> 必须为正整数，不能设为 <code>0</code>。</p><p>仅设置 <code>thinking_budget</code> 时，按下表确定思考档位，保留传入的预算值。</p><table><thead><tr><th><code>thinking_budget</code></th><th>实际档位</th></tr></thead><tbody><tr><td><code>1–4096</code></td><td><code>low</code></td></tr><tr><td><code>4097–131072</code></td><td><code>high</code></td></tr><tr><td><code>131073–262144</code></td><td><code>xhigh</code></td></tr></tbody></table><p>两者均未设置时，使用 <code>high</code> 和 <code>131072</code>。</p><p>控制模型的推理力度，不同模型支持的可选值和默认值不同。</p><p><strong>kimi-k3.1-pro（阿里云百炼部署）</strong>：默认值为 <code>max</code>。</p><ul><li><code>max</code>（默认）：深度推理</li><li><code>high</code>：增强推理</li><li><code>medium</code>：中度推理</li><li><code>low</code>：轻度推理</li></ul><p><code>enable_thinking</code> 默认为 <code>true</code>。支持设为 <code>false</code> 关闭思考，但建议保持开启，关闭会显著影响模型输出效果。</p><p><strong>DeepSeek-V4、GLM 系列</strong>（默认值为 <code>high</code>）</p><p>可选值：</p><ul><li><code>high</code>：高力度推理</li><li><code>max</code>：最大力度推理</li></ul><p>low和medium映射为high，xhigh映射为max。</p><p>适用于glm-5.2、glm-5.1、glm-5、deepseek-v4.1-flash、deepseek-v4-pro（deepseek-v4-flash-0731 除外）</p><p><strong>kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed（月之暗面直供）</strong>（默认值为 <code>max</code>，仅支持 <code>max</code>）</p><p>可选值：</p><ul><li><code>max</code>：最大力度推理</li></ul><p><strong>glm-5.3、ZHIPU/GLM-5.3、ZHIPU/GLM-5.3-Flash、ZHIPU/GLM-5.3-FlashX 与 kimi-k3（阿里云直供）模型：默认值为</strong><code>max</code></p><p>可选值：</p><ul><li><code>max</code>（默认）：深度推理</li><li><code>high</code>：增强推理</li><li><code>low</code>：轻度推理</li></ul><p>该模型始终开启思考，<code>enable_thinking</code> 仅支持 <code>true</code>，传入 <code>false</code> 会导致 API 请求失败。</p><p><strong>deepseek-v4-flash-0731 与 deepseek-v4-pro-0813 模型：默认值为</strong><code>high</code></p><p>可选值：</p><ul><li><code>max</code>：最大力度推理</li><li><code>high</code>（默认）：高力度推理</li><li><code>low</code>：低力度推理</li></ul><p>出于兼容性考虑，<code>medium</code> 映射为 high，<code>xhigh</code> 映射为 high。</p><p><strong>qwen3.8系列模型：默认值为</strong><code>xhigh</code></p><p>可选值：</p><ul><li><code>xhigh</code>（默认）：高力度推理</li><li><code>medium</code>：中力度推理</li><li><code>low</code>：低力度推理</li></ul><p><code>max</code> 映射为 xhigh，<code>high</code> 映射为 xhigh，<code>minimal</code> 映射为 low，<code>none</code> 映射为 enable_thinking=False。</p><blockquote><p>设置上述可选值及映射值以外的值将会报错。</p></blockquote><p><strong>重要：</strong>qwen3.8 系列不支持 reasoning_effort 与 thinking_budget 同时设置，同时设置会报错。但两者支持互转：</p><ul><li>未设置 thinking_budget 时，reasoning_effort 档位自动映射 thinking_budget：<code>low</code> 对应 4096，<code>medium</code> 对应 16384，<code>xhigh</code> 对应 262144。</li><li>未设置 reasoning_effort 时，thinking_budget 自动映射回 reasoning_effort：0~4096 对应 <code>low</code>，4097~16384 对应 <code>medium</code>，16385~262144 对应 <code>xhigh</code>。</li><li>两者均未设置时，使用默认 thinking_budget（131072），默认 reasoning_effort（xhigh）。</li></ul><blockquote><p>通过HTTP调用时，请将 <strong>reasoning_effort</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>tool_stream</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>仅影响复杂工具参数的流式输出行为，仅在流式调用时生效。普通工具参数（所有参数类型均为string）只要开启流式调用即可流式输出，<code>tool_stream</code>对其无影响。复杂工具是指工具定义中某些参数类型为array或object。当前仅Qwen和GLM系列支持。</p><strong>Qwen系列支持列表：</strong><ul><li>qwen-max系列：qwen4-max、qwen3.8-max系列、qwen3.7-max系列的文本模态</li><li>qwen-plus系列：qwen3.7-plus系列、qwen3.6-plus系列的文本模态，以及qwen3.5-plus系列的全模态</li><li>qwen-flash系列：qwen3.8-flash系列、qwen3.7-flash系列、qwen3.6-flash系列、qwen3.5-flash的全模态</li></ul><strong>Qwen系列使用参考：</strong><ul><li><code>tool_stream=false</code>：复杂工具参数会一次性输出，默认行为，复杂格式会更准确。</li><li><code>tool_stream=true</code>：复杂工具参数会流式输出，复杂格式没有超时风险。</li></ul><blockquote><p>复杂工具是指工具定义中某些参数类型为array或object。</p></blockquote><p><strong>GLM系列支持列表：</strong>glm-5、glm-5.1（阿里云直供）。</p><strong>GLM系列使用参考：</strong><ul><li><code>tool_stream=false</code>：工具参数会一次性输出，默认行为，复杂格式会更准确。</li><li><code>tool_stream=true</code>：工具参数会流式输出，复杂格式没有超时风险。</li></ul><blockquote><p>通过HTTP调用时，请将 <strong>tool_stream</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>enable_code_interpreter</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否开启代码解释器功能。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md">代码解释器</a></p><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启</li></ul><blockquote><p>不支持 Java SDK。通过HTTP调用时，请将 <strong>enable_code_interpreter</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>clear_thinking</strong><code>boolean</code>（可选）默认值为false</p><p>用于控制多轮对话中是否将历史轮次的 <code>reasoning_content</code>（思考过程）作为上下文输入给模型。仅 GLM 系列glm-5.3、glm-5.2、glm-5.1、glm-5模型支持。其中 glm-5.3 的默认值为 <code>true</code>，其余模型的默认值为 <code>false</code>。</p><ul><li><code>true</code>：开启。忽略历史轮次的 <code>reasoning_content</code>，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。</li><li><code>false</code>（默认）：不开启。保留历史轮次的 <code>reasoning_content</code> 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 <code>reasoning_content</code>，缺失、裁剪、改写或重排会导致效果下降或无法生效。</li></ul><p><strong>repetition_penalty</strong><code>float</code>（可选）</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。</p><a id="accordion-repetition-penalty默认值"></a><section><p>repetition_penalty默认值</p><div><ul><li>qwen4-max、qwen-max、qwen-math系列、qwen-audio-turbo系列、QVQ系列、QwQ系列、Qwen3-VL： 1.0；</li><li>qwen-coder系列：1.1；</li><li>其余模型为1.05。</li><li>GLM系列（阿里云直供）：1.0；</li></ul></div></section><blockquote><p>Java SDK中为<strong>repetitionPenalty</strong>*。*通过HTTP调用时，请将 <strong>repetition_penalty</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>不建议修改QVQ模型的默认 repetition_penalty 值。</p></blockquote><p><strong>frequency_penalty</strong> <code>float</code> （可选）</p><p>支持 <code>qwen4-max</code>。按 Token 已出现的次数施加惩罚，以调整重复内容的生成。</p><p><strong>presence_penalty</strong><code>float</code>（可选）</p><p>控制模型生成文本时的内容重复度。</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-presence-penalty默认值"></a><section><p>presence_penalty默认值</p><div><p><code>qwen4-max</code>（非思考模式）、Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen2.5-vl系列、Qwen3-VL（非思考）：1.5；</p><p>qwen-plus/qwen-plus-latest/2025-04-28（思考模式）：0.5；</p><p>其余均为0.0。</p><p>DeepSeek系列（阿里云直供）：deepseek-r1-distill-qwen 蒸馏版: 1；</p><p>Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5: 0.0；</p><p>Kimi系列（月之暗面直供）：0.0；</p><p>MiniMax系列（阿里云直供）：MiniMax-M2.5: 0.0；</p><p>其余DeepSeek/Kimi/GLM/MiniMax模型无默认值。</p></div></section><a id="accordion-原理介绍"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><a id="accordion-示例"></a><section><p>示例</p><div><p>提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”</p><p>参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。</p><p>参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。</p><p>参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。</p></div></section><blockquote><p>不建议修改QVQ模型的默认presence_penalty值。</p></blockquote><blockquote><p>Java SDK不支持设置该参数*。*通过HTTP调用时，请将 <strong>presence_penalty</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>vl_high_resolution_images</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>对 <code>qwen4-max</code>，即使 <code>vl_high_resolution_images=true</code>，显式传入的 <code>max_pixels</code> 仍生效。</p><p>是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">处理高分辨率图像</a>。</p><ul><li><p><code>vl_high_resolution_images：true</code>，使用固定分辨率策略，忽略 <code>max_pixels</code> 设置，超过此分辨率时会将图像总像素缩小至此上限内。</p><a id="accordion-点击查看各模型像素上限"></a><section><p>点击查看各模型像素上限</p><div><p><code>vl_high_resolution_images</code>为<code>True</code>时，不同模型像素上限不同：</p><ul><li>Qwen3.7系列、<code>Qwen3.6</code>系列、<code>Qwen3.5</code>系列、<code>Qwen3-VL系列</code>模型：<code>16777216</code>（每<code>Token</code>对应<code>32*32</code>像素，即<code>16384*32*32</code>）</li><li><code>QVQ系列</code>、其他<code>Qwen2.5-VL系列</code>模型：<code>12845056</code>（每<code>Token</code>对应<code>28*28</code>像素，即 <code>16384*28*28</code>）</li></ul></div></section></li><li><p><code>vl_high_resolution_images</code>为<code>false</code>，像素上限由 <code>max_pixels</code> 决定，输入图像的像素超过<code>max_pixels</code>会将图像缩小至<code>max_pixels</code>内。各模型的默认像素上限即<code>max_pixels</code>的默认值。</p></li></ul><blockquote><p>Java SDK 为 <strong>vlHighResolutionImages</strong>（需要的最低版本为2.20.8<strong>）</strong>*。*通过HTTP调用时，请将 <strong>vl_high_resolution_images</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>vl_enable_image_hw_output</strong><code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否返回图像缩放后的尺寸。模型会对输入的图像进行缩放处理，配置为 True 时会返回图像缩放后的高度和宽度，开启流式输出时，该信息在最后一个数据块（chunk）中返回。支持<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">Qwen-VL模型</a>。</p><blockquote><p>Java SDK中为 <strong>vlEnableImageHwOutput</strong>，Java SDK最低版本为2.20.8*。*通过HTTP调用时，请将 <strong>vl_enable_image_hw_output</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>max_tokens</strong><code>integer</code>（可选，<strong>即将废弃</strong>）</p><blockquote><p>该参数即将废弃，新接入请使用 <code>max_completion_tokens</code>。</p></blockquote><p>该参数的含义随模型不同，具体如下：</p><ul><li>deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash-0731：模型回答与思维链内容之和的最大 Token 数。模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</li><li><code>qwen4-max</code>: 最大 Token 数（思考与最终回答之和）。<code>max_tokens</code> 与 <code>max_completion_tokens</code> 等价；超过此上限时，生成提前停止，<code>finish_reason</code> 为 <code>length</code>。</li><li>glm-5.3：<code>max_tokens</code> 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。glm-5.3 会忽略 <code>thinking_budget</code> 参数。</li><li>glm-5.2：不传入 <code>thinking_budget</code> 参数时，<code>max_tokens</code> 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>；传入 <code>thinking_budget</code> 参数时，<code>max_tokens</code> 仅为模型回答的最大 Token 数，思维链部分的 Token 数由 <code>thinking_budget</code> 单独控制。</li><li>其他模型：模型回答的最大 Token 数（不包含思维链）。若生成内容超过此值，生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</li></ul><p>GLM 模型的默认值与最大值如下表所示，其他模型的默认值与最大值均为模型的最大输出长度。</p><table><thead><tr><th>供应方式</th><th>模型</th><th>默认值</th><th>最大值</th></tr></thead><tbody><tr><td>阿里云直供</td><td>glm-5.3、glm-5.2、glm-5.2-fast-preview、glm-5.1、glm-5</td><td>65536</td><td>131072</td></tr><tr><td>智谱直供</td><td>ZHIPU/GLM-5.3、ZHIPU/GLM-5.3-Flash、ZHIPU/GLM-5.3-FlashX、ZHIPU/GLM-5.2、ZHIPU/GLM-5.1、ZHIPU/GLM-5</td><td>65536</td><td>131072</td></tr></tbody></table><blockquote><p>Java SDK中为<strong>maxTokens</strong>（模型为千问VL/Audio时，Java SDK中为<strong>maxLength，</strong>在 2.18.4 版本之后支持也设置为 maxTokens）*。*通过HTTP调用时，请将 <strong>max_tokens</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>max_completion_tokens</strong><code>integer</code>（可选）</p><p>模型输出的最大长度，包含思维链和模型回答。模型输出超过此值时生成将提前停止，返回的 <code>finish_reason</code> 为 <code>length</code>。</p><p>GLM 模型的默认值与最大值见 <code>max_tokens</code> 参数中的表格，其他模型的默认值与最大值均为模型的最大输出长度。</p><p>与 <code>max_tokens</code> 的区别：<code>max_completion_tokens</code> 始终限制模型完整输出（思维链 + 回答）；<code>max_tokens</code> 的具体限制范围随模型及 <code>thinking_budget</code> 设置而异，见上文说明。思考类模型推荐使用 <code>max_completion_tokens</code>。</p><p>支持以下模型：</p><ul><li>千问 Max：Qwen3.7-Max 及之后的模型</li><li>千问 Plus：Qwen3.5-Plus 及之后的模型</li><li>千问 Flash：Qwen3.5-Flash 及之后的模型</li><li>Kimi：kimi-k2.5 及其之后推出的Kimi模型</li><li>GLM：上表所列的阿里云直供和智谱直供模型</li><li>MiniMax：MiniMax-M2.5 及之后推出的MiniMax模型</li><li>DeepSeek：deepseek-v4-pro 及之后推出的DeepSeek模型</li></ul><blockquote><p>除上表所列的智谱直供 GLM 模型外，以上模型均不包含其他三方直供模型。</p></blockquote><blockquote><p>实际输出 Token 数与设置的 <code>max_completion_tokens</code> 值之间最多可能存在 10 个 Token 的误差。</p></blockquote><blockquote><p>Java SDK 暂不支持该参数。通过 HTTP 调用时，请将 <strong>max_completion_tokens</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><a id="accordion-seed默认值"></a><section><p>seed默认值</p><div><p>其余模型均为1234。</p></div></section><blockquote><p>通过HTTP调用时，请将 <strong>seed</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>stream</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否流式输出回复。参数值：</p><ul><li>false：模型生成完所有内容后一次性返回结果。</li><li>true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。</li></ul><blockquote><p>该参数仅支持Python SDK。通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote><blockquote><p>Qwen3商业版（思考模式）、Qwen3开源版、QwQ、QVQ只支持流式输出。</p></blockquote><p><strong>incremental_output</strong><code>boolean</code>（可选）默认为<code>false</code>（Qwen3-Max、Qwen3-VL、<a href="../../model-user-guide/get-started-with-models/models.md">Qwen3 开源版</a>、<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md">QwQ</a> 、<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">QVQ</a>模型默认值为 <code>true</code>）</p><p>在流式输出模式下是否开启增量输出。推荐您优先设置为<code>true</code>。</p><blockquote><p>Python SDK 2.0 流式输出默认增量返回（incremental_output 默认 true），无需设置该参数。</p></blockquote><p>参数值：</p><ul><li>false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。</li></ul><a id="code-block-18"></a><pre class="language-text"><code>I
I like
I like apple
I like apple.
</code></pre><ul><li>true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。</li></ul><a id="code-block-19"></a><pre class="language-text"><code>I
like
apple
.
</code></pre><blockquote><p>Java SDK中为<strong>incrementalOutput</strong>*。*通过HTTP调用时，请将 <strong>incremental_output</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>QwQ 模型与思考模式下的 Qwen3 模型只支持设置为 <code>true</code>。由于 Qwen3 商业版模型默认值为<code>false</code>，您需要在思考模式下手动设置为 <code>true</code>。</p></blockquote><blockquote><p>Qwen3 开源版模型不支持设置为 <code>false</code>。</p></blockquote><p><strong>response_format</strong><code>object</code> （可选） 默认值为<code>{&quot;type&quot;: &quot;text&quot;}</code></p><p>返回内容的格式。可选值：</p><ul><li><code>{&quot;type&quot;: &quot;text&quot;}</code>：输出文字回复；</li><li><code>{&quot;type&quot;: &quot;json_object&quot;}</code>：输出标准格式的JSON字符串。</li><li><code>{&quot;type&quot;: &quot;json_schema&quot;, &quot;json_schema&quot;: {...}}</code>：输出严格符合指定 JSON Schema 的JSON字符串，可精确控制输出结构与字段类型。</li></ul><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md">结构化输出</a>。<code>json_object</code> 与 <code>json_schema</code> 支持的模型不同，参见<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#7a8e438e89xeq">支持的模型</a>。</p></blockquote><blockquote><p>若指定为<code>{&quot;type&quot;: &quot;json_object&quot;}</code>，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错；若指定为<code>{&quot;type&quot;: &quot;json_schema&quot;, ...}</code>，提示词无需包含 JSON 关键词。</p></blockquote><blockquote><p>Java SDK中为responseFormat*。*通过HTTP调用时，请将 <strong>response_format</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>返回内容的格式。可选值：</p><ul><li><code>text</code>：输出文字回复；</li><li><code>json_object</code>：输出标准格式的JSON字符串；</li><li><code>json_schema</code>：输出严格符合 <code>json_schema</code> 字段所定义结构的JSON字符串。</li></ul><p><strong>json_schema</strong><code>object</code>（可选）</p><p><code>type</code> 为 <code>json_schema</code> 时必须设置，用于定义模型输出需要遵循的 JSON 结构。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#a4f5d7108anxd">获取指定格式的输出</a>。</p><blockquote><p>DashScope 方式需手动构造 JSON Schema，格式与示例参见<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#a4f5d7108anxd">获取指定格式的输出</a>。暂不支持 Java SDK。</p></blockquote><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>name</strong><code>string</code><strong>（必选）</strong></p><p>Schema 的名称。</p><p><strong>schema</strong><code>object</code><strong>（必选）</strong></p><p>描述输出结构的 JSON Schema 对象。通过 <code>properties</code> 定义字段结构，通过 <code>required</code> 声明必填字段列表，通过 <code>additionalProperties</code> 控制是否允许输出未在 Schema 中定义的字段（推荐设置为 <code>false</code>，即只输出已定义的字段）。支持的数据类型：string、number、integer、boolean、object、array、enum。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/qwen-structured-output.md#001cb6ae072tc">配置指南</a>。</p><p><strong>strict</strong><code>boolean</code>（可选）</p><p>是否严格遵循 <code>schema</code> 定义的结构。推荐设置为 <code>true</code>。</p></div></section></div></section><p><strong>result_format</strong><code>string</code>（可选）默认为<code>text</code>（Qwen3-Max、Qwen3-VL、<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md">QwQ</a> 模型、Qwen3 开源模型与 Qwen-Long 模型默认值为 message）</p><p>返回数据的格式。推荐您优先设置为<code>message</code>，可以更方便地进行<a href="../../model-user-guide/model-experience/text-generation-model/multi-round-conversation.md">多轮对话</a>。</p><blockquote><p>Python SDK 2.0 固定返回 message 形态，无需设置该参数；该参数仅 HTTP 接口调用需关注。</p></blockquote><blockquote><p>平台后续将统一调整默认值为<code>message</code>。</p></blockquote><blockquote><p>Java SDK中为<strong>resultFormat</strong>*。*通过HTTP调用时，请将 <strong>result_format</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>模型为千问VL/QVQ/Audio时，设置<code>text</code>不生效。</p></blockquote><blockquote><p>Qwen3-Max、Qwen3-VL、思考模式下的 Qwen3 模型只能设置为<code>message</code>，由于 Qwen3 商业版模型默认值为<code>text</code>，您需要将其设置为<code>message</code>。</p></blockquote><blockquote><p>如果您使用 Java SDK 调用Qwen3 开源模型，并且传入了 <code>text</code>，依然会以 <code>message</code>格式进行返回。</p></blockquote><p><strong>logprobs</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否返回输出 Token 的对数概率，可选值：</p><ul><li><p><code>true</code></p><p>返回</p></li><li><p><code>false</code></p><p>不返回</p></li></ul><p>支持以下模型：</p><ul><li><code>qwen4-max</code></li><li>qwen-plus系列的快照模型（不包含稳定版模型）</li><li>qwen3-vl-plus系列（包含稳定版模型）</li><li>Qwen3 开源模型</li></ul><blockquote><p>通过HTTP调用时，请将 <strong>logprobs</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>top_logprobs</strong> <code>integer</code> （可选）默认值为0</p><p>指定在每一步生成时，返回模型最大概率的候选 Token 个数。</p><p>取值范围：[0,5]</p><p>仅当 <code>logprobs</code> 为 <code>true</code> 时生效。</p><blockquote><p>Java SDK中为<strong>topLogprobs</strong>*。*通过HTTP调用时，请将 <strong>top_logprobs</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>n</strong><code>integer</code>（可选） 默认值为1</p><p>生成响应的个数，取值范围是<code>1-4</code>。对于需要生成多个响应的场景（如创意写作、广告文案等），可以设置较大的 n 值。</p><blockquote><p>kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 不支持此参数。</p></blockquote><blockquote><p>当前仅支持 <code>qwen4-max</code>、<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md">Qwen3（非思考模式）</a>、qwen-plus-character 模型，且在传入 tools 参数时固定为1。</p></blockquote><blockquote><p>设置较大的 n 值不会增加输入 Token 消耗，会增加输出 Token 的消耗。</p></blockquote><blockquote><p>通过HTTP调用时，请将 <strong>n</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现 <code>stop</code> 指定的字符串或 <code>token_id</code> 时，生成将立即终止。</p><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote><blockquote><p>通过HTTP调用时，请将 <strong>stop</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>tools</strong><code>array</code>（可选）</p><p>包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></p><p>使用 <code>tools</code> 时，必须将<code>result_format</code>设为<code>message</code>。</p><p>发起 Function Calling，或提交工具执行结果时，都必须设置<code>tools</code>参数。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>工具类型，当前仅支持<code>function</code>。</p><p><strong>function</strong><code>object</code><strong>（必选）</strong></p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>name</strong><code>string</code><strong>（必选）</strong></p><p>工具函数的名称，必须是字母、数字，可以包含下划线和短划线，最大长度为64。</p><p><strong>description</strong><code>string</code><strong>（必选）</strong></p><p>工具函数的描述，供模型选择何时以及如何调用工具函数。</p><p><strong>parameters</strong><code>object</code>（可选）默认值为 <code>{}</code></p><p>工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见<a href="https://json-schema.org/understanding-json-schema">链接</a>。若<code>parameters</code>参数为空，表示该工具没有入参（如时间查询工具）。</p><blockquote><p>为提高工具调用的准确性，建议传入 <code>parameters</code>。</p></blockquote></div></section></div></section><blockquote><p>通过HTTP调用时，请将 <strong>tools</strong>放入 <strong>parameters</strong> 对象中。暂时不支持qwen-vl与qwen-audio系列模型。</p></blockquote><p><strong>tool_choice</strong><code>string 或 object</code>（可选）默认值为 <code>auto</code></p><p>工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。</p><ul><li><p><code>auto</code></p><p>大模型自主选择工具策略；</p></li><li><p><code>none</code></p><p>若在特定请求中希望临时禁用工具调用，可设定<code>tool_choice</code>参数为<code>none</code>；</p></li><li><p><code>required</code></p><p>若希望强制调用至少一个工具，可设定<code>tool_choice</code>参数为<code>required</code>，模型将始终返回工具调用信息。</p><blockquote><p>Qwen 系列模型暂不支持<code>required</code>：非思考模式下无法保证一定调用工具，思考模式下当前不支持<code>required</code>。</p></blockquote></li><li><p><code>{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;the_function_to_call&quot;}}</code></p><p>若希望强制调用某个工具，可设定<code>tool_choice</code>参数为<code>{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;the_function_to_call&quot;}}</code>，其中<code>the_function_to_call</code>是指定的工具函数名称。</p><blockquote><p>思考模式的模型不支持强制调用某个工具。</p></blockquote></li></ul><blockquote><p>Java SDK中为<strong>toolChoice</strong>*。*通过HTTP调用时，请将 <strong>tool_choice</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>parallel_tool_calls</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否开启并行工具调用。</p><blockquote><p>kimi/kimi-k3.1-pro 和 kimi/kimi-k3.1-pro-highspeed 不支持此参数。</p></blockquote><p>可选值：</p><ul><li><code>true</code>：开启</li><li><code>false</code>：不开启。</li></ul><p>并行工具调用详情请参见：<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md#cb6b5c484bt4x">并行工具调用</a>。</p><blockquote><p>Java SDK中为<strong>parallelToolCalls</strong>*。*通过HTTP调用时，请将 <strong>parallel_tool_calls</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>enable_search</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>模型在生成文本时是否使用互联网搜索结果进行参考。取值如下：</p><ul><li><p>true：启用互联网搜索，模型会将搜索结果作为文本生成过程中的参考信息，但模型会基于其内部逻辑判断是否使用互联网搜索结果。</p><blockquote><p>若开启后未联网搜索，可优化提示词，或设置<code>search_options</code>中的<code>forced_search</code>参数开启强制搜索。</p></blockquote></li><li><p>false：关闭互联网搜索。</p></li></ul><p>计费信息请参见<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md#92ce83df3a599">计费说明</a>。</p><blockquote><p>Java SDK中为<strong>enableSearch</strong>*。*通过HTTP调用时，请将 <strong>enable_search</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>启用互联网搜索功能可能会增加 Token 的消耗。</p></blockquote><p><strong>search_options</strong><code>object</code>（可选）</p><p>联网搜索的策略。仅当<code>enable_search</code>为<code>true</code>时生效。详情参见<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a>。</p><blockquote><p>通过HTTP调用时，请将 <strong>search_options</strong>放入 <strong>parameters</strong> 对象中。Java SDK中为<strong>searchOptions</strong>。</p></blockquote><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>enable_source</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>在返回结果中是否展示搜索到的信息。参数值：</p><ul><li>true：展示；</li><li>false：不展示。</li></ul><p><strong>enable_citation</strong> <code>boolean</code>（可选）默认值为<code>false</code></p><p>是否开启[1]或[ref_1]样式的角标标注功能。在<code>enable_source</code>为<code>true</code>时生效。参数值：</p><ul><li>true：开启；</li><li>false：不开启。</li></ul><p><strong>citation_format</strong> <code>string</code>（可选）默认值为<code>&quot;[&lt;number&gt;]&quot;</code></p><p>角标样式。在<code>enable_citation</code>为<code>true</code>时生效。参数值：</p><ul><li>[&lt;number&gt;]：角标形式为<code>[1]</code>；</li><li>[ref_&lt;number&gt;]：角标形式为<code>[ref_1]</code>。</li></ul><p><strong>forced_search</strong> <code>boolean</code>（可选）默认值为<code>false</code></p><p>是否强制开启搜索。参数值：</p><ul><li>true：强制开启；</li><li>false：不强制开启。</li></ul><p><strong>search_strategy</strong> <code>string</code>（可选）默认值为<code>turbo</code></p><p>搜索互联网信息的策略。</p><p>可选值：</p><ul><li><p><code>turbo</code> （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。</p></li><li><p><code>max</code>: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。</p></li><li><p><code>agent</code>：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。</p><blockquote><p>该策略仅适用于qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash与qwen3.5-flash-2026-02-23的思考模式（仅支持流式）的非思考模式。</p></blockquote><blockquote><p>启用该策略时，仅支持<strong>返回搜索来源</strong>（<code>enable_source: true</code>），其他联网搜索功能不可用。 <strong>enable_search_extension</strong> <code>boolean</code>（可选）默认值为<code>false</code></p></blockquote></li></ul><p>是否开启特定领域增强。参数值：</p><ul><li><p><code>true</code></p><p>开启。</p></li><li><p><code>false</code>（默认值）</p><p>不开启。</p></li></ul><p><strong>prepend_search_result</strong> <code>boolean</code>（可选）默认值为<code>false</code></p><p>在流式输出且<code>enable_source</code>为<code>true</code>时，可通过<code>prepend_search_result</code>配置<strong>第一个返回的数据包</strong>是否只包含搜索来源信息。可选值：</p><ul><li><p><code>true</code></p><p>只包含搜索来源信息。</p></li><li><p><code>false</code>（默认值）</p><p>包含搜索来源信息与大模型回复信息。</p></li></ul><blockquote><p>暂不支持 DashScope Java SDK。</p></blockquote></div></section><p><strong>X-DashScope-DataInspection</strong><code>string</code> （可选）</p><p>在千问 API 的内容安全能力基础上，可通过 AI 安全护栏进一步识别输入输出内容的违规信息。参数值为 JSON 字符串，<code>input</code> 和 <code>output</code> 分别对应输入和输出，取值为 <code>cip</code> 时使用 AI 安全护栏进一步识别该方向的违规信息，可分别设置：</p><ul><li><code>'{&quot;input&quot;:&quot;cip&quot;,&quot;output&quot;:&quot;cip&quot;}'</code>：输入和输出均使用 AI 安全护栏进一步识别；</li><li><code>'{&quot;input&quot;:&quot;cip&quot;}'</code>：仅对输入使用 AI 安全护栏进一步识别；</li><li><code>'{&quot;output&quot;:&quot;cip&quot;}'</code>：仅对输出使用 AI 安全护栏进一步识别；</li><li>不设置该参数：不启用 AI 安全护栏。</li></ul><p>通过 HTTP 调用时请放入请求头：<code>-H &quot;X-DashScope-DataInspection: {\&quot;input\&quot;: \&quot;cip\&quot;, \&quot;output\&quot;: \&quot;cip\&quot;}&quot;</code>；</p><p>通过 Python SDK 调用时请通过<code>headers</code>配置：<code>headers={'X-DashScope-DataInspection': '{&quot;input&quot;:&quot;cip&quot;,&quot;output&quot;:&quot;cip&quot;}'}</code>。</p><p>详细使用方法请参见<a href="../../model-user-guide/security-and-compliance/content-security.md">输入输出 AI 安全护栏</a>；若不想修改调用代码，可通过<a href="../../model-user-guide/security-and-compliance/content-security.md#h2-workspace-switch">业务空间维度开关</a>启用护栏。</p><blockquote><p>不支持通过 Java SDK 设置。</p></blockquote><blockquote><p>不适用于Qwen-Audio 系列模型。</p></blockquote><p><strong>skill</strong><code>array</code>（可选）</p><p>技能参数，用于启用特定生成技能（如PPT生成）。仅<code>qwen-doc-turbo</code>模型支持。详细用法请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md#f6a7b8c9d0pp1">生成PPT</a>。</p><blockquote><p>通过HTTP调用时，请将 <strong>skill</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><blockquote><p>使用 <strong>skill 时，stream</strong> 必须设置为 <strong>true</strong>。</p></blockquote><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>技能类型。当前支持：</p><ul><li><code>ppt</code>：PPT生成。</li></ul><p><strong>mode</strong><code>string</code> （可选）</p><p>PPT生成模式。可选值：</p><ul><li><code>general</code> （默认值）：模板模式，需配合<code>template_id</code> 使用，生成HTML格式的PPT。</li><li><code>creative</code> ：创意模式，无需模板，生成图版PPT（每页为图片）。</li></ul><p><strong>template_id</strong><code>string</code>（可选）</p><p>PPT模板ID。与<code>mode</code>为<code>general</code>或未设置<code>mode</code>时配合使用。可选值：</p><ul><li><code>news_01</code>：新闻模板</li><li><code>summary_01</code>：总结模板</li><li><code>internet_01</code>：互联网模板</li><li><code>thesis_01</code>：论文模板</li></ul></div></section></td><td><div><a id="sec-tabs-8"></a><section><a id="文本输入"></a><section><a id="文本输入-h4"></a><h4>文本输入</h4><a id="sec-tabs-9"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><a id="code-block-20"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {'role': 'system', 'content': [{'text': 'You are a helpful assistant.'}]},
    {'role': 'user', 'content': [{'text': '你是谁？'}]}
]
response = client.multimodal.chat.create(
    # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model=&quot;qwen4-max&quot;,
    messages=messages,
    )
print(response)
</code></pre></section><a id="java"></a><section><a id="java-h4"></a><h4>Java</h4><a id="code-block-21"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.12.0
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    public static MultiModalConversationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;You are a helpful assistant.&quot;)))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;你是谁？&quot;)))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model(&quot;qwen4-max&quot;)
                .messages(Arrays.asList(systemMsg, userMsg))
                .build();
        return conv.call(param);
    }
    public static void main(String[] args) {
        try {
            MultiModalConversationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println(&quot;An error occurred while calling the generation service: &quot; + e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></section><a id="php-http"></a><section><a id="php-http-h4"></a><h4>PHP（HTTP）</h4><a id="code-block-22"></a><pre class="language-php"><code>&lt;?php

$url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot;;
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    &quot;model&quot; =&gt; &quot;qwen4-max&quot;,
    &quot;input&quot; =&gt; [
        &quot;messages&quot; =&gt; [
            [
                &quot;role&quot; =&gt; &quot;system&quot;,
                &quot;content&quot; =&gt; [[&quot;text&quot; =&gt; &quot;You are a helpful assistant.&quot;]]
            ],
            [
                &quot;role&quot; =&gt; &quot;user&quot;,
                &quot;content&quot; =&gt; [[&quot;text&quot; =&gt; &quot;你是谁？&quot;]]
            ]
        ]
    ],
    &quot;parameters&quot; =&gt; [
        &quot;result_format&quot; =&gt; &quot;message&quot;
    ]
];

$jsonData = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    &quot;Authorization: Bearer $apiKey&quot;,
    &quot;Content-Type: application/json&quot;
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    echo &quot;Response: &quot; . $response;
} else {
    echo &quot;Error: &quot; . $httpCode . &quot; - &quot; . $response;
}

curl_close($ch);
?&gt;
</code></pre></section><a id="node-js-http"></a><section><a id="node-js-http-h4"></a><h4>Node.js（HTTP）</h4><p>DashScope 未提供 Node.js 环境的 SDK。如需通过 OpenAI Node.js SDK调用，请参考本文的<a href="../qwen-api-reference.md">OpenAI</a>章节。</p><a id="code-block-23"></a><pre class="language-javascript"><code>import fetch from 'node-fetch';

const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    model: &quot;qwen4-max&quot;, // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    input: {
        messages: [
            {
                role: &quot;system&quot;,
                content: [{ text: &quot;You are a helpful assistant.&quot; }]
            },
            {
                role: &quot;user&quot;,
                content: [{ text: &quot;你是谁？&quot; }]
            }
        ]
    },
    parameters: {
        result_format: &quot;message&quot;
    }
};

fetch('https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response =&gt; response.json())
.then(data =&gt; {
    console.log(JSON.stringify(data));
})
.catch(error =&gt; {
    console.error('Error:', error);
});
</code></pre></section><a id="c-http"></a><section><a id="c-http-h4"></a><h4>C#（HTTP）</h4><a id="code-block-24"></a><pre class="language-csharp"><code>using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = &quot;sk-xxx&quot;;
        string? apiKey = Environment.GetEnvironmentVariable(&quot;DASHSCOPE_API_KEY&quot;);

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine(&quot;API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。&quot;);
            return;
        }

        // 设置请求 URL 和内容
        string url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot;;
        // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @&quot;{
            &quot;&quot;model&quot;&quot;: &quot;&quot;qwen4-max&quot;&quot;,
            &quot;&quot;input&quot;&quot;: {
                &quot;&quot;messages&quot;&quot;: [
                    {
                        &quot;&quot;role&quot;&quot;: &quot;&quot;system&quot;&quot;,
                        &quot;&quot;content&quot;&quot;: [{&quot;&quot;text&quot;&quot;: &quot;&quot;You are a helpful assistant.&quot;&quot;}]
                    },
                    {
                        &quot;&quot;role&quot;&quot;: &quot;&quot;user&quot;&quot;,
                        &quot;&quot;content&quot;&quot;: [{&quot;&quot;text&quot;&quot;: &quot;&quot;你是谁？&quot;&quot;}]
                    }
                ]
            },
            &quot;&quot;parameters&quot;&quot;: {
                &quot;&quot;result_format&quot;&quot;: &quot;&quot;message&quot;&quot;
            }
        }&quot;;

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task&lt;string&gt; SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, &quot;application/json&quot;))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(&quot;Bearer&quot;, apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue(&quot;application/json&quot;));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $&quot;请求失败: {response.StatusCode}&quot;;
            }
        }
    }
}
</code></pre></section><a id="go-http"></a><section><a id="go-http-h4"></a><h4>Go（HTTP）</h4><p>DashScope 未提供 Go 的 SDK。如需通过 OpenAI Go SDK调用，请参考本文的<a href="../qwen-api-reference.md">OpenAI-Go</a>章节。</p><a id="code-block-25"></a><pre class="language-go"><code>package main

import (
	&quot;bytes&quot;
	&quot;encoding/json&quot;
	&quot;fmt&quot;
	&quot;io&quot;
	&quot;log&quot;
	&quot;net/http&quot;
	&quot;os&quot;
)

type ContentItem struct {
	Text string `json:&quot;text&quot;`
}

type Message struct {
	Role    string        `json:&quot;role&quot;`
	Content []ContentItem `json:&quot;content&quot;`
}

type Input struct {
	Messages []Message `json:&quot;messages&quot;`
}

type Parameters struct {
	ResultFormat string `json:&quot;result_format&quot;`
}

type RequestBody struct {
	Model      string     `json:&quot;model&quot;`
	Input      Input      `json:&quot;input&quot;`
	Parameters Parameters `json:&quot;parameters&quot;`
}

func main() {
	// 创建 HTTP 客户端
	client := &amp;http.Client{}

	// 构建请求体
	requestBody := RequestBody{
		// 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
		Model: &quot;qwen4-max&quot;,
		Input: Input{
			Messages: []Message{
				{
					Role:    &quot;system&quot;,
					Content: []ContentItem{{Text: &quot;You are a helpful assistant.&quot;}},
				},
				{
					Role:    &quot;user&quot;,
					Content: []ContentItem{{Text: &quot;你是谁？&quot;}},
				},
			},
		},
		Parameters: Parameters{
			ResultFormat: &quot;message&quot;,
		},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}

	// 创建 POST 请求
	req, err := http.NewRequest(&quot;POST&quot;, &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot;, bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}

	// 设置请求头
	// 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey := &quot;sk-xxx&quot;
	apiKey := os.Getenv(&quot;DASHSCOPE_API_KEY&quot;)
	req.Header.Set(&quot;Authorization&quot;, &quot;Bearer &quot;+apiKey)
	req.Header.Set(&quot;Content-Type&quot;, &quot;application/json&quot;)

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// 读取响应体
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	// 打印响应内容
	fmt.Printf(&quot;%s\n&quot;, bodyText)
}
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><a id="code-block-26"></a><pre class="language-bash"><code>curl --location &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: [{&quot;text&quot;: &quot;You are a helpful assistant.&quot;}]
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [{&quot;text&quot;: &quot;你是谁？&quot;}]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;result_format&quot;: &quot;message&quot;
    }
}'
</code></pre></section><a id="dashscope-cli"></a><section><a id="dashscope-cli-h4"></a><h4>dashscope CLI</h4><p>通过 dashscope 命令行调用。</p><a id="code-block-27"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope generation create -m qwen-plus -p &quot;你好&quot;
</code></pre><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div><p>完整地域表见 <a href="../preparations/base-url.md">Base URL 总览</a>。</p></section></section></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><blockquote><p>相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/stream.md">流式输出</a>。</p></blockquote><a id="sec-tabs-10"></a><section><a id="文本生成模型"></a><section><a id="文本生成模型-h4"></a><h4>文本生成模型</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {'role':'system','content':'you are a helpful assistant'},
    {'role': 'user','content': '你是谁？'}
]
responses = client.chat.completions.create(
    # 此处以qwen-plus为例，可按需更换为其它文本生成模型
    model=&quot;qwen-plus&quot;,
    messages=messages,
    stream=True,
    # 流式输出默认为增量模式：每个数据块仅包含新生成的内容。
    )
for response in responses:
    print(response.choices[0].delta.content, end=&quot;&quot;)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static void handleGenerationResult(GenerationResult message) {
        System.out.println(JsonUtils.toJson(message));
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable&lt;GenerationResult&gt; result = gen.streamCall(param);
        result.blockingForEach(message -&gt; handleGenerationResult(message));
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 此处以qwen-plus为例，可按需更换为其它文本生成模型
                .model(&quot;qwen-plus&quot;)
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true)
                .build();
    }
    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content(&quot;你是谁？&quot;).build();
            streamCallWithMessage(gen, userMsg);
        } catch (ApiException | NoApiKeyException | InputRequiredException  e) {
            logger.error(&quot;An exception occurred: {}&quot;, e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --location &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--header &quot;X-DashScope-SSE: enable&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-plus&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: &quot;You are a helpful assistant.&quot;
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: &quot;你是谁？&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;result_format&quot;: &quot;message&quot;,
        &quot;incremental_output&quot;:true
    }
}'
</code></pre></div></div></section><a id="多模态模型"></a><section><a id="多模态模型-h4"></a><h4>多模态模型</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若使用新加坡地域的模型，请将下行region替换为：region=&quot;ap-southeast-1&quot;
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg&quot;},
            {&quot;text&quot;: &quot;图中描绘的是什么景象?&quot;}
        ]
    }
]

responses = client.multimodal.chat.create(
    # 可按需更换为其它多模态模型，并修改相应的 messages
    model='qwen3-vl-plus',
    messages=messages,
    stream=True,
    # 流式输出默认为增量模式：每个数据块仅包含新生成的内容。
    )

full_content = &quot;&quot;
print(&quot;流式输出内容为：&quot;)
for response in responses:
    if response.choices[0].delta.content:
        print(response.choices[0].delta.content)
        full_content += response.choices[0].delta.content
print(f&quot;完整内容为：{full_content}&quot;)
</code></pre></div><a id="fig-code-group-2-java-tab"></a>Java<div><a id="code-code-group-2-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请取消下列注释
    //  static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1&quot;;}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;image&quot;, &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg&quot;),
                        Collections.singletonMap(&quot;text&quot;, &quot;图中描绘的是什么景象？&quot;))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3-vl-plus&quot;)  // 可按需更换为其它多模态模型，并修改相应的 messages
                .messages(Arrays.asList(userMessage))
                .incrementalOutput(true)
                .build();
        Flowable&lt;MultiModalConversationResult&gt; result = conv.streamCall(param);
        result.blockingForEach(item -&gt; {
            try {
                var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                    // 判断content是否存在且不为空
                if (content != null &amp;&amp;  !content.isEmpty()) {
                    System.out.println(content.get(0).get(&quot;text&quot;));
                    }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg&quot;},
                    {&quot;text&quot;: &quot;图中描绘的是什么景象？&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;incremental_output&quot;: true
    }
}'
</code></pre></div></div></section></section></section><a id="图像输入"></a><section><a id="图像输入-h4"></a><h4>图像输入</h4><blockquote><p>关于大模型分析图像的更多用法，请参见<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">图像与视频理解</a>。</p></blockquote><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;},
            {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png&quot;},
            {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png&quot;},
            {&quot;text&quot;: &quot;这些是什么?&quot;}
        ]
    }
]
response = client.multimodal.chat.create(
    # 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model='qwen3-vl-plus',
    messages=messages
    )
print(response)
</code></pre></div><a id="fig-code-group-3-java-tab"></a>Java<div><a id="code-code-group-3-java"></a><pre class="language-java"><code>// Copyright (c) Alibaba, Inc. and its affiliates.

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;
public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;image&quot;, &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;),
                        Collections.singletonMap(&quot;image&quot;, &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png&quot;),
                        Collections.singletonMap(&quot;image&quot;, &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png&quot;),
                        Collections.singletonMap(&quot;text&quot;, &quot;这些是什么?&quot;))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model(&quot;qwen3-vl-plus&quot;)
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-3-curl-tab"></a>curl<div><a id="code-code-group-3-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;},
                    {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png&quot;},
                    {&quot;image&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png&quot;},
                    {&quot;text&quot;: &quot;这些是什么?&quot;}
                ]
            }
        ]
    }
}'
</code></pre></div></div></section><a id="视频输入"></a><section><a id="视频输入-h4"></a><h4>视频输入</h4><blockquote><p>以下为传入视频帧的示例代码，关于更多用法（如传入视频文件），请参见<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#80dbf6ca8fh6s">视觉理解</a>。</p></blockquote><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import os
# 需要 dashscope 2.0.1 及以上版本
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{&quot;role&quot;: &quot;user&quot;,
             &quot;content&quot;: [
                 {&quot;video&quot;:[&quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
                           &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
                           &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
                           &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;]},
                 {&quot;text&quot;: &quot;描述这个视频的具体过程&quot;}]}]
try:
    response = client.multimodal.chat.create(
        # 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model='qwen3-vl-plus',
        messages=messages
    )
    print(response)
except DashScopeError as e:
    print(f&quot;HTTP返回码：{e.status_code}&quot;)
    print(f&quot;错误码：{e.code}&quot;)
    print(f&quot;错误信息：{e.message}&quot;)
    print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)
</code></pre></div><a id="fig-code-group-4-java-tab"></a>Java<div><a id="code-code-group-4-java"></a><pre class="language-java"><code>// DashScope SDK版本需要不低于2.16.7
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;
public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    // 此处以qwen3-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    private static final String MODEL_NAME = &quot;qwen3-vl-plus&quot;;
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;You are a helpful assistant.&quot;)))
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;video&quot;, Arrays.asList(&quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
                                &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
                                &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
                                &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;)),
                        Collections.singletonMap(&quot;text&quot;, &quot;描述这个视频的具体过程&quot;)))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL_NAME).message(systemMessage)
                .message(userMessage).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>curl<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-d '{
  &quot;model&quot;: &quot;qwen3-vl-plus&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;video&quot;: [
              &quot;https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg&quot;,
              &quot;https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg&quot;,
              &quot;https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg&quot;,
              &quot;https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg&quot;
            ]
          },
          {
            &quot;text&quot;: &quot;描述这个视频的具体过程&quot;
          }
        ]
      }
    ]
  }
}'
</code></pre></div></div></section><a id="联网搜索"></a><section><a id="联网搜索-h4"></a><h4>联网搜索</h4><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
    {'role': 'system', 'content': [{'text': 'You are a helpful assistant.'}]},
    {'role': 'user', 'content': [{'text': '杭州明天天气是什么？'}]}
    ]
response = client.multimodal.chat.create(
    # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model=&quot;qwen4-max&quot;,
    messages=messages,
    enable_search=True,
    )
print(response)
</code></pre></div><a id="fig-code-group-5-java-tab"></a>Java<div><a id="code-code-group-5-java"></a><pre class="language-java"><code>// 建议dashscope SDK的版本 &gt;= 2.12.0
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    public static MultiModalConversationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;You are a helpful assistant.&quot;)))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;明天杭州什么天气？&quot;)))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model(&quot;qwen4-max&quot;)
                .messages(Arrays.asList(systemMsg, userMsg))
                .enableSearch(true)
                .build();
        return conv.call(param);
    }
    public static void main(String[] args) {
        try {
            MultiModalConversationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println(&quot;An error occurred while calling the generation service: &quot; + e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>curl<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: [{&quot;text&quot;: &quot;You are a helpful assistant.&quot;}]
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [{&quot;text&quot;: &quot;明天杭州天气如何？&quot;}]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;enable_search&quot;: true,
        &quot;result_format&quot;: &quot;message&quot;
    }
}'
</code></pre></div></div></section><a id="工具调用"></a><section><a id="工具调用-h4"></a><h4>工具调用</h4><blockquote><p>完整的Function Calling 流程代码请参见<a href="../../model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a>。</p></blockquote><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

tools = [
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_time&quot;,
            &quot;description&quot;: &quot;当你想知道现在的时间时非常有用。&quot;,
            &quot;parameters&quot;: {}
        }
    },
    {
        &quot;type&quot;: &quot;function&quot;,
        &quot;function&quot;: {
            &quot;name&quot;: &quot;get_current_weather&quot;,
            &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
            &quot;parameters&quot;: {
                &quot;type&quot;: &quot;object&quot;,
                &quot;properties&quot;: {
                    &quot;location&quot;: {
                        &quot;type&quot;: &quot;string&quot;,
                        &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                    }
                }
            },
            &quot;required&quot;: [
                &quot;location&quot;
            ]
        }
    }
]
messages = [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;text&quot;: &quot;杭州天气怎么样&quot;}]}]
response = client.multimodal.chat.create(
    # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model='qwen4-max',
    messages=messages,
    tools=tools,
)
print(response)
</code></pre></div><a id="fig-code-group-6-java-tab"></a>Java<div><a id="code-code-group-6-java"></a><pre class="language-java"><code>import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import com.alibaba.dashscope.aigc.conversation.ConversationParam.ResultFormat;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.tools.FunctionDefinition;
import com.alibaba.dashscope.tools.ToolFunction;
import com.alibaba.dashscope.utils.JsonUtils;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.github.victools.jsonschema.generator.Option;
import com.github.victools.jsonschema.generator.OptionPreset;
import com.github.victools.jsonschema.generator.SchemaGenerator;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfig;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfigBuilder;
import com.github.victools.jsonschema.generator.SchemaVersion;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}
    public class GetWeatherTool {
        private String location;
        public GetWeatherTool(String location) {
            this.location = location;
        }
        public String call() {
            return location+&quot;今天是晴天&quot;;
        }
    }
    public class GetTimeTool {
        public GetTimeTool() {
        }
        public String call() {
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern(&quot;yyyy-MM-dd HH:mm:ss&quot;);
            String currentTime = &quot;当前时间：&quot; + now.format(formatter) + &quot;。&quot;;
            return currentTime;
        }
    }
    public static void SelectTool()
            throws NoApiKeyException, ApiException, InputRequiredException {
        SchemaGeneratorConfigBuilder configBuilder =
                new SchemaGeneratorConfigBuilder(SchemaVersion.DRAFT_2020_12, OptionPreset.PLAIN_JSON);
        SchemaGeneratorConfig config = configBuilder.with(Option.EXTRA_OPEN_API_FORMAT_VALUES)
                .without(Option.FLATTENED_ENUMS_FROM_TOSTRING).build();
        SchemaGenerator generator = new SchemaGenerator(config);
        ObjectNode jsonSchema_weather = generator.generateSchema(GetWeatherTool.class);
        ObjectNode jsonSchema_time = generator.generateSchema(GetTimeTool.class);
        FunctionDefinition fdWeather = FunctionDefinition.builder().name(&quot;get_current_weather&quot;).description(&quot;获取指定地区的天气&quot;)
                .parameters(JsonUtils.parseString(jsonSchema_weather.toString()).getAsJsonObject()).build();
        FunctionDefinition fdTime = FunctionDefinition.builder().name(&quot;get_current_time&quot;).description(&quot;获取当前时刻的时间&quot;)
                .parameters(JsonUtils.parseString(jsonSchema_time.toString()).getAsJsonObject()).build();
        MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;You are a helpful assistant. When asked a question, use tools wherever possible.&quot;)))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue()).content(Arrays.asList(Collections.singletonMap(&quot;text&quot;, &quot;杭州天气&quot;))).build();
        List&lt;MultiModalMessage&gt; messages = new ArrayList&lt;&gt;();
        messages.addAll(Arrays.asList(systemMsg, userMsg));
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                // 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model(&quot;qwen4-max&quot;)
                .messages(messages)
                .tools(Arrays.asList(
                        ToolFunction.builder().function(fdWeather).build(),
                        ToolFunction.builder().function(fdTime).build()))
                .build();
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            SelectTool();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(String.format(&quot;Exception %s&quot;, e.getMessage()));
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-6-curl-tab"></a>curl<div><a id="code-code-group-6-curl"></a><pre class="language-bash"><code>curl --location &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen4-max&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{&quot;text&quot;: &quot;杭州天气怎么样&quot;}]
        }]
    },
    &quot;parameters&quot;: {
        &quot;result_format&quot;: &quot;message&quot;,
        &quot;tools&quot;: [{
            &quot;type&quot;: &quot;function&quot;,
            &quot;function&quot;: {
                &quot;name&quot;: &quot;get_current_time&quot;,
                &quot;description&quot;: &quot;当你想知道现在的时间时非常有用。&quot;,
                &quot;parameters&quot;: {}
            }
        },{
            &quot;type&quot;: &quot;function&quot;,
            &quot;function&quot;: {
                &quot;name&quot;: &quot;get_current_weather&quot;,
                &quot;description&quot;: &quot;当你想查询指定城市的天气时非常有用。&quot;,
                &quot;parameters&quot;: {
                    &quot;type&quot;: &quot;object&quot;,
                    &quot;properties&quot;: {
                        &quot;location&quot;: {
                            &quot;type&quot;: &quot;string&quot;,
                            &quot;description&quot;: &quot;城市或县区，比如北京市、杭州市、余杭区等。&quot;
                        }
                    }
                },
                &quot;required&quot;: [&quot;location&quot;]
            }
        }]
    }
}'
</code></pre></div></div></section><a id="异步调用"></a><section><a id="异步调用-h4"></a><h4>异步调用</h4><a id="code-block-28"></a><pre class="language-python"><code># 需要 dashscope 2.0.1 及以上版本
import asyncio
import platform
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
aclient = dashscope.AsyncClient(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

async def main():
    response = await aclient.multimodal.chat.create(
        # 此处以qwen4-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model=&quot;qwen4-max&quot;,
        messages=[{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: [{&quot;text&quot;: &quot;你是谁&quot;}]}],
    )
    print(response)

if platform.system() == &quot;Windows&quot;:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
</code></pre></section><a id="文档理解"></a><section><a id="文档理解-h4"></a><h4>文档理解</h4><a id="sec-tabs-11"></a><section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><a id="code-block-29"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [
        {'role': 'system', 'content': 'you are a helpful assisstant'},
        # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
        {'role':'system','content':'fileid://{FILE_ID}'},
        {'role': 'user', 'content': '这篇文章讲了什么'}]
response = client.chat.completions.create(
    model=&quot;qwen-long&quot;,
    messages=messages,
)
print(response)
</code></pre></section><a id="java-2"></a><section><a id="java-2-h4"></a><h4>Java</h4><a id="code-block-30"></a><pre class="language-java"><code>import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static GenerationResult callWithFile() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();

        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content(&quot;you are a helpful assistant&quot;)
                .build();

        Message fileSystemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                // 请将 '{FILE_ID}'替换为您实际对话场景所使用的 file-id
                .content(&quot;fileid://{FILE_ID}&quot;)
                .build();

        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(&quot;这篇文章讲了什么&quot;)
                .build();

        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen-long&quot;)
                .messages(Arrays.asList(systemMsg, fileSystemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();

        return gen.call(param);
    }

    public static void main(String[] args) {
        try {
            GenerationResult result = callWithFile();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println(&quot;调用 DashScope API 出错: &quot; + e.getMessage());
            e.printStackTrace();
        }
    }
}
</code></pre></section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><blockquote><p>请将 {FILE_ID}替换为您实际对话场景所使用的 file-id</p></blockquote><a id="code-block-31"></a><pre class="language-bash"><code>curl --location &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation&quot; \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;Content-Type: application/json&quot; \
--data '{
    &quot;model&quot;: &quot;qwen-long&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: &quot;You are a helpful assistant.&quot;
            },
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: &quot;fileid://{FILE_ID}&quot;
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: &quot;这篇文章讲了什么？&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;result_format&quot;: &quot;message&quot;
    }
}'
</code></pre></section></section></section><a id="ppt生成"></a><section><a id="ppt生成-h4"></a><h4>PPT生成</h4><blockquote><p>PPT生成功能仅<code>qwen-doc-turbo</code>模型支持。详细用法请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md#f6a7b8c9d0pp1">生成PPT</a>。</p></blockquote><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

try:
    response = client.chat.completions.create(
        model='qwen-doc-turbo',
        messages=[
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;you are a helpful assistant.&quot;},
            {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;您的文档内容&quot;},
            {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;生成一个10到20页的ppt&quot;}
        ],
        parameters={&quot;skill&quot;: [{&quot;type&quot;: &quot;ppt&quot;, &quot;mode&quot;: &quot;general&quot;, &quot;template_id&quot;: &quot;news_01&quot;}]}
    )
    print(response.choices[0].message.content)
except DashScopeError as e:
    print(f&quot;HTTP返回码：{e.status_code}&quot;)
    print(f&quot;错误码：{e.code}&quot;)
    print(f&quot;错误信息：{e.message}&quot;)
    print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)
</code></pre></div><a id="fig-code-group-7-curl-tab"></a>curl<div><a id="code-code-group-7-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--header 'X-DashScope-SSE: enable' \
--data '{
    &quot;model&quot;: &quot;qwen-doc-turbo&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: &quot;you are a helpful assistant.&quot;
            },
            {
                &quot;role&quot;: &quot;system&quot;,
                &quot;content&quot;: &quot;您的文档内容&quot;
            },
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: &quot;生成一个10到20页的ppt&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;skill&quot;: [
            {
                &quot;type&quot;: &quot;ppt&quot;,
                &quot;mode&quot;: &quot;general&quot;,
                &quot;template_id&quot;: &quot;news_01&quot;
            }
        ]
    }
}'
</code></pre></div></div></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h2>chat响应对象（流式与非流式输出格式一致）</h2><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<strong>requestId。</strong></p></blockquote><p><strong>code</strong><code>string</code></p><p>错误码，调用失败时返回。</p><blockquote><p>Python SDK 2.0 调用失败时不返回信封字段，而是抛出 DashScopeError（e.code/e.status_code/e.message/e.request_id）。</p></blockquote><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>模型生成的回复。当设置输入参数<strong>result_format</strong>为<strong>text</strong>时将回复内容返回到该字段。</p><p><strong>finish_reason</strong><code>string</code></p><p>当设置输入参数<strong>result_format</strong>为<strong>text</strong>时该参数不为空。</p><p>有四种情况：</p><ul><li>正在生成时为null；</li><li>因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；</li><li>因生成长度过长而结束为length；</li><li>因发生工具调用为tool_calls。</li></ul><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。当result_format为message时返回choices参数。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有四种情况：</p><ul><li>正在生成时为null；</li><li>因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；</li><li>因生成长度过长而结束为length；</li><li>因发生工具调用为tool_calls。</li></ul><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为assistant。</p><p><strong>content</strong><code>string或array</code></p><p>输出消息的内容。当使用qwen-vl或qwen-audio系列模型时为<code>array</code>，其余情况为<code>string</code>。</p><blockquote><p>如果发起Function Calling，则该值为空。</p></blockquote><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>当使用qwen-vl或qwen-audio系列模型时，输出消息的内容。</p><p><strong>image_hw</strong><code>array</code></p><p>当Qwen-VL系列模型启用 vl_enable_image_hw_output 参数时，有两种情况：</p><ul><li>图像输入：返回图像的高度和高度（数值单位：像素）</li><li>视频输入：返回空数组</li></ul></div></section><p><strong>encrypted_content</strong> <code>string</code></p><p><code>qwen4-max</code>, <code>thinking_display=&quot;summarized&quot;</code>: 每轮都需传开启参数。客户端只能原样回传密文，不能读取、截断、重新编码、修改或拼接多轮密文。摘要不能替代历史思维链。 <a href="../../model-user-guide/model-experience/text-generation-model/cot-summary.md#multi-turn">思维链摘要与加密</a>.</p><p><strong>reasoning_content</strong> <code>string</code></p><p>模型的深度思考内容。</p><p><strong>tool_calls</strong><code>array</code></p><p>若模型需要调用工具，则会生成tool_calls参数。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>function</strong><code>object</code></p><p>调用工具的名称，以及输入参数。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>name</strong><code>string</code></p><p>调用工具的名称</p><p><strong>arguments</strong><code>string</code></p><p>需要输入到工具中的参数，为JSON字符串。</p><blockquote><p>由于大模型响应有一定随机性，输出的JSON字符串并不总满足于您的函数，建议您在将参数输入函数前进行参数的有效性校验。</p></blockquote></div></section><p><strong>index</strong> <code>integer</code></p><p>当前<strong>tool_calls</strong>对象在tool_calls数组中的索引。</p><p><strong>id</strong> <code>string</code></p><p>本次工具响应的ID。</p><p><strong>type</strong> <code>string</code></p><p>工具类型，固定为<code>function</code>。</p></div></section></div></section><p><strong>logprobs</strong><code>object</code></p><p>当前 choices 对象的概率信息。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>content</strong> <code>array</code></p><p>带有对数概率信息的 Token 数组。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p><p><strong>top_logprobs</strong> <code>array</code></p><p>当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的<code>top_logprobs</code>保持一致。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p></div></section></div></section></div></section></div></section><p><strong>search_info</strong><code>object</code></p><p>联网搜索到的信息，在设置<code>search_options</code>参数后会返回该参数。</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>search_results</strong><code>array</code></p><p>联网搜索到的结果。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>site_name</strong><code>string</code></p><p>搜索结果来源的网站名称。</p><p><strong>icon</strong><code>string</code></p><p>来源网站的图标URL，如果没有图标则为空字符串。</p><p><strong>index</strong><code>integer</code></p><p>搜索结果的序号，表示该搜索结果在<code>search_results</code>中的索引。</p><p><strong>title</strong><code>string</code></p><p>搜索结果的标题。</p><p><strong>url</strong><code>string</code></p><p>搜索结果的链接地址。</p></div></section><p><strong>extra_tool_info</strong><code>array</code></p><p>开启<code>enable_search_extension</code>参数后返回的领域增强信息。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>result</strong><code>string</code></p><p>领域增强工具输出信息。</p><p><strong>tool</strong><code>string</code></p><p>领域增强使用的工具。</p></div></section></div></section></div></section><p><strong>usage</strong><code>map</code></p><p>本次chat请求使用的Token信息。</p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>用户输入内容转换成Token后的长度。<a href="../../model-user-guide/model-experience/text-generation-model/text-generation.md#e710782c79xqy">补充说明</a></p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型输出内容转换成Token后的长度。</p><p><strong>input_tokens_details</strong> <code>object</code>（可选）</p><p>输入内容转换成 Token 后的长度详情。</p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code>（可选）</p><p>输入的文本转换为 Token 后的长度。</p><p><strong>image_tokens</strong> <code>integer</code>（可选）</p><p>输入的图像转换为Token后的长度。</p><p><strong>video_tokens</strong> <code>integer</code>（可选）</p><p>输入的视频文件或图像列表转换为Token后的长度。</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>当输入为纯文本时返回该字段，为<strong>input_tokens</strong>与<strong>output_tokens</strong>之和<strong>。</strong></p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入内容包含<code>image</code>时返回该字段。为用户输入图片内容转换成Token后的长度。</p><p><strong>video_tokens</strong> <code>integer</code></p><p>输入内容包含<code>video</code>时返回该字段。为用户输入视频内容转换成Token后的长度。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>输入内容包含<code>audio</code>时返回该字段。为用户输入音频内容转换成Token后的长度。</p><p><strong>output_tokens_details</strong> <code>object</code>（可选）</p><p>输出内容转换成 Token 后的长度详情。部分模型返回该字段。</p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code>（可选）</p><p>输出的文本转换为Token后的长度。</p><p><strong>reasoning_tokens</strong> <code>integer</code>（可选）</p><p>思考过程转换为Token后的长度。仅推理模型返回该字段。</p><p><strong>audio_tokens</strong> <code>integer</code>（可选）</p><p>输出的音频转换为 Token 后的长度。仅音频输出模型返回该字段。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-30"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中 Cache 的 Token 数。Context Cache 详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md">上下文缓存</a>。</p><p><strong>cache_creation</strong> <code>object</code></p><p><a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>创建信息。</p><a id="accordion-属性-31"></a><section><p>属性</p><div><p><strong>ephemeral_5m_input_tokens</strong> <code>integer</code></p><p>用于创建5分钟有效期显式缓存的 Token 长度。</p></div></section><p><strong>cache_creation_input_tokens</strong> <code>integer</code></p><p>用于创建显式缓存的 Token 长度。</p><p><strong>cache_type</strong> <code>string</code></p><p>使用<a href="../../model-user-guide/model-experience/text-generation-model/context-cache.md#825f201c5fy6o">显式缓存</a>时，参数值为<code>ephemeral</code>，否则该参数不存在。</p></div></section></div></section></td><td><div><a id="code-block-32"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;902fee3b-f7f0-9a8c-96a1-6b4ea25af114&quot;,
  &quot;output&quot;: {
    &quot;text&quot;: null,
    &quot;finish_reason&quot;: null,
    &quot;choices&quot;: [
      {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;message&quot;: {
          &quot;role&quot;: &quot;assistant&quot;,
          &quot;content&quot;: &quot;我是阿里云开发的一款超大规模语言模型，我叫千问。&quot;
        }
      }
    ]
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 22,
    &quot;output_tokens&quot;: 17,
    &quot;total_tokens&quot;: 39
  }
}
</code></pre></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
