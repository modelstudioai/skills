# DashScope API 参考

通过 DashScope API 调用千问模型，查看输入输出参数说明及调用示例。

#### 华北2（北京）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
```

#### Java代码

-   **方式一：**

```
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

```
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
```

#### 新加坡

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'
```

#### Java代码

-   **方式一：**

```
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

```
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";
```

#### 美国（弗吉尼亚）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1'
```

#### Java代码

-   **方式一：**

```
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

```
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";
```

#### 德国（法兰克福）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1'
```

#### Java代码

-   **方式一：**

```
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

```
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1";
```

#### 日本（东京）

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1'
```

#### Java代码

-   **方式一：**

```
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

```
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1";
```

#### 中国香港

HTTP 请求地址：

-   纯文本模型（如qwen-plus）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
-   多模态模型（如qwen3.7-plus或qwen3-vl-plus）：`POST https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`base_url`：

#### Python代码

```
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1'
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过DashScope SDK进行调用，需要[安装DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

**重要**阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## 请求体

**model**`string`**（必选）**

模型名称。

支持的模型：Qwen 大语言模型（商业版、开源版）、Qwen-VL、Qwen-Coder、千问Audio、数学模型、DeepSeek（阿里云直供、硅基流动直供）、Kimi（阿里云直供）、GLM（阿里云直供）、MiniMax（阿里云直供、稀宇科技直供）。

**具体模型名称和计费，请参见**[选择模型](raw/model-user-guide/get-started-with-models/models.md)。

**messages**`array`**（必选）**

传递给大模型的上下文，按对话顺序排列。

> 通过HTTP调用时，请将**messages**放入 **input** 对象中。

消息类型

System Message`object`（可选）

系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在`messages`数组的第一位。

> QwQ模型不建议设置 System Message，QVQ 模型设置 System Message不会生效。

属性

**content**`string`**（必选）**

消息内容。

**role**`string`**（必选）**

系统消息的角色，固定为 `system` 。

User Message`object`**（必选）**

用户消息，用于向模型传递问题、指令或上下文等。

属性

**content**`string 或 array`**（必选）**

消息内容。若输入只有文本，则为 string 类型；若输入包含图像等多模态数据，或启用显式缓存，则为 array 类型。

属性

**text**`string`**（必选）**

输入的文本。

**image**`string`（可选）

指定用于图片理解的图像文件，图像支持以下三种方式传入：

-   公网 URL：公网可访问的图像链接
-   图片的 Base64 编码，格式为 `data:image/<format>;base64,<data>`
-   本地文件：本地文件的绝对路径

适用模型：[Qwen-VL](raw/model-user-guide/model-experience/vision-model/vision.md)、[QVQ](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)

示例值：`{"image":"https://xxxx.jpeg"}`

**video**`array 或 string`（可选）

使用[Qwen-VL 模型](raw/model-user-guide/model-experience/vision-model/vision.md)或[QVQ模型](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)传入的视频。

-   若传入图像列表，则为`array`类型；
-   若传入视频文件，则为`string`类型\*。\*

传入本地文件请参见[本地文件（Qwen-VL）](raw/model-user-guide/model-experience/vision-model/vision.md)或[本地文件（QVQ）](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)。

示例值：

-   图像列表：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]}`
-   视频文件：`{"video":"https://xxx.mp4"}`

**fps**`float`（可选）

每秒抽帧数。取值范围为 \[0.1, 10\]，默认值为2.0。

功能说明

fps有两个功能：

-   输入视频文件时，控制抽帧频率，每 f p s 1 ​秒抽取一帧。
    
    > 适用于[Qwen-VL 模型](raw/model-user-guide/model-experience/vision-model/vision.md)与[QVQ模型](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)。
    
-   告知模型相邻帧之间的时间间隔，帮助其更好地理解视频的时间动态。同时适用于输入视频文件与图像列表时。该功能同时支持视频文件和图像列表输入，适用于事件时间定位或分段内容摘要等场景。
    
    > 支持Qwen3.7、Qwen3.6、Qwen3.5、`Qwen3-VL`、`Qwen2.5-VL`与QVQ模型。
    

较大的`fps`适合高速运动的场景（如体育赛事、动作电影等），较小的`fps`适合长视频或内容偏静态的场景。

示例值

-   图像列表传入：`{"video":["https://xx1.jpg",...,"https://xxn.jpg"]，"fps":2}`
-   视频文件传入：`{"video": "https://xx1.mp4"，"fps":2}`

**max\_frames**`integer`（可选）

视频抽取帧数的上限。当按`fps`计算的帧数超过 `max_frames`时，系统将自动调整为：在`max_frames`内均匀抽帧，确保总帧数不超过限制。

取值范围

-   qwen3.7系列、qwen3.6系列、qwen3.5系列：最大值和默认值均为 8000。
-   `qwen3-vl-plus`系列、`qwen3-vl-flash`系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：最大值和默认值均为 2000。
-   `qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：最大值和默认值均为 512。

示例值

`{"type": "video_url","video_url": {"url":"https://xxxx.mp4"},"max_frame": 2000}`

> 使用 OpenAI 兼容API调用时，不支持自定义`max_frames`参数，API 将自动使用各模型对应的默认值。

**min\_pixels**`integer`（可选）

设定输入图像或视频帧的最小像素阈值。当输入图像或视频帧的像素小于`min_pixels`时，会将其进行放大，直到总像素高于`min_pixels`。

取值范围

-   **输入图像：**
    -   `Qwen3.7、Qwen3.6、Qwen3.5`、`Qwen3-VL`：默认值和最小值均为：`65536`
    -   `qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值和最小值均为`4096`
    -   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：默认值和最小值均为`3136`
-   **输入视频文件或图像列表：**
    -   `Qwen3.7、Qwen3.6、Qwen3.5`、Qwen3-VL（包括商业版和开源版）、`qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值为`65536`，最小值为`4096`
    -   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：默认值为`50176`，最小值为`3136`

示例值

-   输入图像：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"min_pixels": 65536}`
-   输入视频文件时：`{"type": "video_url","video_url": {"url":"https://xxxx.mp4"},"min_pixels": 65536}`
-   输入图像列表时：`{"type": "video","video": ["https://xx1.jpg",...,"https://xxn.jpg"],"min_pixels": 65536}`

**max\_pixels**`integer`（可选）

用于设定输入图像或视频帧的最大像素阈值。当输入图像或视频的像素在`[min_pixels, max_pixels]`区间内时，模型会按原图进行识别。当输入图像像素大于`max_pixels`时，会将图像进行缩小，直到总像素低于`max_pixels`。

取值范围

-   **输入图像：**
    
    `max_pixels` 的取值与是否开启`vl_high_resolution_images`参数有关。
    
    -   当`vl_high_resolution_images`为`False`时：
        
        -   `Qwen3.7、Qwen3.6、Qwen3.5`、`Qwen3-VL`：默认值为`2621440`，最大值为：`16777216`
        -   `qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值为`1310720`，最大值为：`16777216`
        -   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：默认值为`1003520` ，最大值为`12845056`
    -   当`vl_high_resolution_images`为`True`时：
        
        -   `Qwen3.7、Qwen3.6、Qwen3.5`、Qwen3-VL、`qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：`max_pixels`无效，输入图像的最大像素固定为`16777216`
        -   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：`max_pixels`无效，输入图像的最大像素固定为`12845056`
-   **输入视频文件或图像列表：**
    -   `qwen3.7系列、qwen3.6系列、qwen3.5系列、qwen3-vl-plus`系列、`qwen3-vl-flash`系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：默认值为`655360`，最大值为`2048000`
    -   其他`Qwen3-VL`开源模型、`qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值`655360`，最大值为`786432`
    -   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：默认值为`501760`，最大值为`602112`

示例值

-   输入图像：`{"type": "image_url","image_url": {"url":"https://xxxx.jpg"},"max_pixels": 8388608}`
-   输入视频文件时：`{"type": "video_url","video_url": {"url":"https://xxxx.mp4"},"max_pixels": 655360}`
-   输入图像列表时：`{"type": "video","video": ["https://xx1.jpg",...,"https://xxn.jpg"],"max_pixels": 655360}`

**total\_pixels**`integer`（可选）

用于限制从视频中抽取的所有帧的总像素（单帧图像像素 × 总帧数）。如果视频总像素超过此限制，系统将对视频帧进行缩放，但仍会确保单帧图像的像素值在`[min_pixels, max_pixels]`范围内。适用于 Qwen-VL、QVQ 模型。

对于抽帧数量较多的长视频，可适当降低此值以减少Token消耗和处理时间，但这可能会导致图像细节丢失。

取值范围

-   qwen3.7系列、qwen3.6系列、qwen3.5系列：默认值和最大值均为819200000，该值对应 `800000` 个图像 Token（每 32×32 像素对应 1 个图像 Token）。
-   `qwen3-vl-plus`系列、`qwen3-vl-flash`系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：默认值和最大值均为134217728，该值对应 `131072` 个图像 Token（每 32×32 像素对应 1 个图像 Token）。
-   其他`Qwen3-VL`开源模型、`qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`：默认值和最小值均为`67108864`，该值对应 `65536` 个图像 Token（每 32×32 像素对应 1 个图像 Token）。
-   其他`qwen-vl-plus`模型、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：默认值和最小值均为`51380224`，该值对应 `65536` 个图像 Token（每 28×28 像素对应 1 个图像 Token）。

示例值

-   输入视频文件时：`{"type": "video_url","video_url": {"url":"https://xxxx.mp4"},"total_pixels": 134217728}`
-   输入图像列表时：`{"type": "video","video": ["https://xx1.jpg",...,"https://xxn.jpg"],"total_pixels": 134217728}`

**audio**`string`

> 模型为音频理解时，是必选参数，如模型为qwen-audio-turbo等。

使用音频理解功能时，传入的音频文件。

示例值：`{"audio":"https://xxx.mp3"}`

**cache\_control**`object`**（可选）**

仅支持[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)的模型支持，用于开启显式缓存。

属性

**type** `string`**（必选）**

固定为`ephemeral`。

**role**`string`**（必选）**

用户消息的角色，固定为`user`。

Assistant Message `object`（可选）

模型对用户消息的回复。

属性

**content**`string`（可选）

消息内容。仅当助手消息中指定`tool_calls`参数时非必选。

**role**`string`**（必选）**

固定为`assistant`。

**partial**`boolean`（可选）

是否开启前缀续写。相关文档与支持的模型：[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)。

**tool\_calls** `array`（可选）

发起 Function Calling 后，返回的工具与入参信息，包含一个或多个对象。由上一轮模型响应的`tool_calls`字段获得。

属性

**id** `string`

工具响应的ID。

**type** `string`

工具类型，当前只支持设为`function`。

**function** `object`

工具与入参信息。

属性

**name** `string`

工具名称。

**arguments** `string`

入参信息，为JSON格式字符串。

**index** `integer`

当前工具信息在`tool_calls`数组中的索引。

Tool Message`object`（可选）

工具的输出信息。

属性

**content**`string`**（必选）**

工具函数的输出内容，必须为字符串格式。

**role**`string`**（必选）**

固定为`tool`。

**tool\_call\_id**`string`**（可选）**

发起 Function Calling 后返回的 id，可以通过`response.output.choices[0].message.tool_calls[$index]["id"]`获取，用于标记 Tool Message 对应的工具。

**temperature**`float`（可选）

采样温度，控制模型生成文本的多样性。

temperature越高，生成的文本更多样，反之，生成的文本更确定。

取值范围： \[0, 2)

temperature默认值

-   qwen3.8-max/qwen3.8-flash（思考模式）：视觉理解0.6，文本输入1.0，0.6以下的temperature值会默认改为0.6
-   Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、qwen开源系列、qwen-coder系列、qwen-doc-turbo、Qwen3-VL（非思考）：0.7；
-   QVQ系列 : 0.5；
-   qwen-audio-turbo系列：0.00001；
-   qwen-vl系列、qwen2.5-omni-7b：0.01；
-   qwen-math系列：0；
-   Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6；
-   qwen3-max-preview（思考模式）、qwen-long系列： 1.0；
-   qwen-plus-character：0.92
-   qwen3-omni-flash系列：0.9
-   Qwen3-VL（思考模式）：0.8
-   DeepSeek系列（阿里云直供）：deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2（非思考模式）: 1.0；deepseek-v3.2（思考模式）、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1、deepseek-r1-0528、deepseek-r1-distill-qwen 蒸馏版: 0.6；deepseek-v3: 0.7；
-   DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；
-   DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think（思考模式）: 0.6；vanchin/deepseek-v3.1-terminus: 0.7；vanchin/deepseek-v3.2-speciale、vanchin/deepseek-r1、vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；
-   Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6（思考模式）、kimi-k2.5（思考模式）、kimi-k2-thinking: 1.0；kimi-k2.6（非思考模式）、kimi-k2.5（非思考模式）、Moonshot-Kimi-K2-Instruct: 0.6；
-   Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6（思考模式）、kimi/kimi-k2.5（思考模式）: 1.0；kimi/kimi-k2.6（非思考模式）、kimi/kimi-k2.5（非思考模式）: 0.6；
-   GLM系列（阿里云直供）：glm-5.1、glm-5、glm-4.7、glm-4.6: 1.0；glm-4.5、glm-4.5-air: 0.6；
-   GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.6；
-   MiniMax系列（阿里云直供）：MiniMax-M2.5、MiniMax-M2.1: 1.0；
-   MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 1.0。
-   MiMo系列（小米直供）：mimo-v2.5-pro: 1.0，范围 \[0, 1.5\]。

> 通过HTTP调用时，请将 **temperature**放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 temperature 值。

**top\_p**`float`（可选）

核采样的概率阈值，控制模型生成文本的多样性。

top\_p越高，生成的文本更多样。反之，生成的文本更确定。

取值范围：（0,1.0\]。

top\_p默认值

Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列、Qwen3-Coder系列、qwen-max系列、qwen-plus系列（非思考模式）、qwen-flash系列（非思考模式）、qwen-turbo系列（非思考模式）、Qwen 2.5开源系列、qwen-coder系列、qwen-long、qwen-doc-turbo、Qwen3-VL（非思考）：0.8；

qwen-omni-turbo 系列：0.01；

qwen-vl-plus系列、qwen-vl-max、qwen2.5-omni-7b：0.001；

QVQ系列 : 0.5；

qwen3-max-preview（思考模式）、qwen-math系列、Qwen3-Omni-Flash系列：1.0；

Qwen3.8（思考模式）、Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：0.95

DeepSeek系列（阿里云直供）：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1、deepseek-r1-0528、deepseek-r1-distill-qwen 蒸馏版: 0.95；deepseek-v3: 0.6；

DeepSeek系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0；

DeepSeek系列（快手万擎直供）：vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus: 0.95；vanchin/deepseek-v3.2-speciale: 0.9；vanchin/deepseek-r1: 0.8；vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0；

Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5、kimi-k2-thinking: 0.95；Moonshot-Kimi-K2-Instruct: 1.0；

Kimi系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5: 0.95；

GLM系列（阿里云直供）：0.95；

GLM系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.95；

MiniMax系列（阿里云直供）：MiniMax-M2.5、MiniMax-M2.1: 0.95；

MiniMax系列（稀宇科技直供）：MiniMax/MiniMax-M3: 0.95；MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 0.9。

MiMo系列（小米直供）：xiaomi/mimo-v2.5-pro: 0.95，范围 \[0.01, 1.0\]。

> Java SDK中为**topP**\*。\*通过HTTP调用时，请将 **top\_p**放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 top\_p 值。

**top\_k**`integer`（可选）

生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top\_k大于100时，表示不启用top\_k策略，此时仅有top\_p策略生效。

取值需要大于或等于0。

top\_k默认值

QVQ系列：10；

QwQ 系列：40；

qwen-math 系列、其余qwen-vl-plus系列之前的模型、qwen-audio-turbo系列、：1；

其余模型均为20；

GLM系列（阿里云直供）：20；

DeepSeek/Kimi/MiniMax系列均不支持top\_k参数。

> Java SDK中为**topK**\*。\*通过HTTP调用时，请将 **top\_k**放入 **parameters** 对象中。

> 不建议修改QVQ模型的默认 top\_k 值。

**enable\_thinking** `boolean` （可选）

使用混合思考模型时，是否开启思考模式，适用于Qwen3.7、Qwen3.6、Qwen3.5、Qwen3、Qwen3-VL模型，以及 DeepSeek-V4-Pro/V4-Flash 系列（阿里云直供）、DeepSeek-V3.2/V3.2-exp/V3.1 系列（阿里云直供、硅基流动直供）、Kimi-K2.6/K2.5 系列（阿里云直供）、GLM 系列。DeepSeek-V4 系列默认开启思考，可通过 `reasoning_effort` 参数调整推理力度。

可选值：

-   `true`：开启
    
    > 开启后，思考内容将通过`reasoning_content`字段返回。
    
-   `false`：不开启
    

不同模型的默认值：[支持的模型](https://help.aliyun.com/zh/model-studio/deep-thinking#78286fdc35hlw)

> Java SDK 为enableThinking；通过HTTP调用时，请将 **enable\_thinking** 放入 **parameters** 对象中。

**preserve\_thinking** `boolean` （可选）默认值为 `false`（**qwen3.8-max/qwen3.8-flash 默认值为**`true`）

是否将对话历史中 assistant 消息的 reasoning\_content 拼接至模型输入。适用于需要模型参考历史思考过程的场景。

目前支持qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash（默认开启）、qwen3.7-max、qwen3.7-max-2026-05-20以及后续快照、qwen3.6-max-preview、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、kimi-k2.6（阿里云百炼部署）、kimi-k2.7-code（阿里云百炼部署，默认开启）、kimi/kimi-k2.7-code-highspeed（月之暗面直供，默认开启）、kimi/kimi-k2.7-code（月之暗面直供，默认开启）。

> **重要：**使用 qwen3.8-max/qwen3.8-flash 时，preserve\_thinking 默认为 true，必须将历史对话中所有的 reasoning\_content 完整回传。**不支持将 reasoning\_content 拼接到 content 字段中回传。**

-   若历史消息中不包含 reasoning\_content，开启此参数不会报错，正常兼容。
-   开启后，历史对话中的 reasoning\_content 会计入输入 Token 数量并计费。

> 通过HTTP调用时，请将 **preserve\_thinking** 放入 **parameters** 对象中。暂不支持 Java SDK。

**thinking\_budget** `integer` （可选）

思考过程的最大长度。适用于Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（阿里云直供）、Kimi（阿里云直供）系列模型，其中 kimi-k3 不支持该参数。相关文档：[限制思考长度](https://help.aliyun.com/zh/model-studio/deep-thinking#e7c0002fe4meu)。

默认值为模型最大思维链长度，请参见：[选择模型](raw/model-user-guide/get-started-with-models/models.md)

> Java SDK 为 thinkingBudget。通过HTTP调用时，请将 **thinking\_budget** 放入 **parameters** 对象中。

> 默认值为模型最大思维链长度。

**reasoning\_effort** `string` （可选）

控制模型的推理力度，不同模型支持的可选值和默认值不同。

**DeepSeek-V4、GLM 系列与 kimi/kimi-k3**（默认值为 `high`）

可选值：

-   `high`：高力度推理
-   `max`：最大力度推理

low和medium映射为high，xhigh映射为max。

适用于glm-5.2、glm-5.1、glm-5、deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-flash（阿里云直供）（deepseek-v4-flash-0731 除外）、kimi/kimi-k3（月之暗面直供，仅支持 `max`）

**glm-5.3、ZHIPU/GLM-5.3、ZHIPU/GLM-5.3-Flash、ZHIPU/GLM-5.3-FlashX 与 kimi-k3（阿里云直供）模型：默认值为**`max`

可选值：

-   `max`（默认）：深度推理
-   `high`：增强推理
-   `low`：轻度推理

该模型始终开启思考，`enable_thinking` 仅支持 `true`，传入 `false` 会导致 API 请求失败。

**deepseek-v4-flash-0731 与 deepseek-v4-pro-0813 模型：默认值为**`high`

可选值：

-   `max`：最大力度推理
-   `high`（默认）：高力度推理
-   `low`：低力度推理

出于兼容性考虑，`medium` 映射为 high，`xhigh` 映射为 high。

**qwen3.8系列模型：默认值为**`xhigh`

可选值：

-   `xhigh`（默认）：高力度推理
-   `medium`：中力度推理
-   `low`：低力度推理

`max` 映射为 xhigh，`high` 映射为 xhigh，`minimal` 映射为 low，`none` 映射为 enable\_thinking=False。

> 设置上述可选值及映射值以外的值将会报错。

**重要：**qwen3.8 系列不支持 reasoning\_effort 与 thinking\_budget 同时设置，同时设置会报错。但两者支持互转：

-   未设置 thinking\_budget 时，reasoning\_effort 档位自动映射 thinking\_budget：`low` 对应 4096，`medium` 对应 16384，`xhigh` 对应 262144。
-   未设置 reasoning\_effort 时，thinking\_budget 自动映射回 reasoning\_effort：0~4096 对应 `low`，4097~16384 对应 `medium`，16385~262144 对应 `xhigh`。
-   两者均未设置时，使用默认 thinking\_budget（131072），默认 reasoning\_effort（xhigh）。

> 通过HTTP调用时，请将 **reasoning\_effort** 放入 **parameters** 对象中。

**tool\_stream** `boolean` （可选）默认值为 `false`

仅影响复杂工具参数的流式输出行为，仅在流式调用时生效。普通工具参数（所有参数类型均为string）只要开启流式调用即可流式输出，`tool_stream`对其无影响。复杂工具是指工具定义中某些参数类型为array或object。当前仅Qwen和GLM系列支持。

**Qwen系列支持列表：**

-   qwen-max系列：qwen3.8-max系列、qwen3.7-max系列的文本模态
-   qwen-plus系列：qwen3.7-plus系列、qwen3.6-plus系列的文本模态，以及qwen3.5-plus系列的全模态
-   qwen-flash系列：qwen3.8-flash系列、qwen3.7-flash系列、qwen3.6-flash系列、qwen3.5-flash的全模态

**Qwen系列使用参考：**

-   `tool_stream=false`：复杂工具参数会一次性输出，默认行为，复杂格式会更准确。
-   `tool_stream=true`：复杂工具参数会流式输出，复杂格式没有超时风险。

> 复杂工具是指工具定义中某些参数类型为array或object。

**GLM系列支持列表：**glm-4.6、glm-4.7、glm-5、glm-5.1（阿里云直供）。

**GLM系列使用参考：**

-   `tool_stream=false`：工具参数会一次性输出，默认行为，复杂格式会更准确。
-   `tool_stream=true`：工具参数会流式输出，复杂格式没有超时风险。

> 通过HTTP调用时，请将 **tool\_stream** 放入 **parameters** 对象中。

**enable\_code\_interpreter** `boolean` （可选）默认值为 `false`

是否开启代码解释器功能。相关文档：[代码解释器](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md)

可选值：

-   `true`：开启
-   `false`：不开启

> 不支持 Java SDK。通过HTTP调用时，请将 **enable\_code\_interpreter** 放入 **parameters** 对象中。

**clear\_thinking**`boolean`（可选）默认值为false

用于控制多轮对话中是否将历史轮次的 `reasoning_content`（思考过程）作为上下文输入给模型。仅 GLM 系列glm-5.3、glm-5.2、glm-5.1、glm-5、glm-4.7模型支持。其中 glm-5.3 的默认值为 `true`，其余模型的默认值为 `false`。

-   `true`：开启。忽略历史轮次的 `reasoning_content`，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。
-   `false`（默认）：不开启。保留历史轮次的 `reasoning_content` 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 `reasoning_content`，缺失、裁剪、改写或重排会导致效果下降或无法生效。

**repetition\_penalty**`float`（可选）

模型生成时连续序列中的重复度。提高repetition\_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。

repetition\_penalty默认值

-   qwen-max、qwen-math系列、qwen-vl-max系列、qwen-audio-turbo系列、QVQ系列、QwQ系列、Qwen3-VL： 1.0；
-   qwen-coder系列：1.1；
-   qwen-vl-plus：1.2；
-   其余模型为1.05。
-   DeepSeek系列（阿里云直供）：deepseek-v3.2-exp/v3.1:1.0；
-   GLM系列（阿里云直供）：1.0；

> Java SDK中为**repetitionPenalty**\*。\*通过HTTP调用时，请将 **repetition\_penalty**放入 **parameters** 对象中。

> 使用qwen-vl-plus\_2025-01-25模型进行文字提取时，建议设置repetition\_penalty为1.0。

> 不建议修改QVQ模型的默认 repetition\_penalty 值。

**presence\_penalty**`float`（可选）

控制模型生成文本时的内容重复度。

取值范围：\[-2.0, 2.0\]。正值降低重复度，负值增加重复度。

在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。

presence\_penalty默认值

Qwen3.8（非思考模式）、Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、qwen3-max-preview（思考模式）、Qwen3（非思考模式）、Qwen3-Instruct系列/1.7b/4b（思考模式）、QVQ系列、qwen-max、qwen2.5-vl系列、qwen-vl-max系列、qwen-vl-plus、Qwen3-VL（非思考）：1.5；

qwen3-8b/14b/32b/30b-a3b/235b-a22b（思考模式）、qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo/qwen-turbo/2025-04-28（思考模式）：0.5；

其余均为0.0。

DeepSeek系列（阿里云直供）：deepseek-r1、deepseek-r1-0528、deepseek-r1-distill-qwen 蒸馏版: 1；

Kimi系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5: 0.0；

Kimi系列（月之暗面直供）：0.0；

MiniMax系列（阿里云直供）：MiniMax-M2.5、MiniMax-M2.1: 0.0；

其余DeepSeek/Kimi/GLM/MiniMax模型无默认值。

原理介绍

如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。

示例

提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”

参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。

参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。

参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。

> 使用qwen-vl-plus模型进行文字提取时，建议设置presence\_penalty为1.5。

> 不建议修改QVQ模型的默认presence\_penalty值。

> Java SDK不支持设置该参数\*。\*通过HTTP调用时，请将 **presence\_penalty**放入 **parameters** 对象中。

**vl\_high\_resolution\_images**`boolean`（可选）默认值为`false`

是否将输入图像的像素上限提升至 16384 Token 对应的像素值。相关文档：[处理高分辨率图像](raw/model-user-guide/model-experience/vision-model/vision.md)。

-   `vl_high_resolution_images：true`，使用固定分辨率策略，忽略 `max_pixels` 设置，超过此分辨率时会将图像总像素缩小至此上限内。
    
    点击查看各模型像素上限
    
    `vl_high_resolution_images`为`True`时，不同模型像素上限不同：
    
    -   Qwen3.7系列、`Qwen3.6`系列、`Qwen3.5`系列、`Qwen3-VL系列`、`qwen-vl-max`、`qwen-vl-max-0813`、`qwen-vl-plus`、`qwen-vl-plus-0815``、qwen-vl-plus-0710`模型：`16777216`（每`Token`对应`32*32`像素，即`16384*32*32`）
    -   `QVQ系列`、其他`Qwen2.5-VL系列`模型：`12845056`（每`Token`对应`28*28`像素，即 `16384*28*28`）
    
-   `vl_high_resolution_images`为`false`，像素上限由 `max_pixels` 决定，输入图像的像素超过`max_pixels`会将图像缩小至`max_pixels`内。各模型的默认像素上限即`max_pixels`的默认值。
    

> Java SDK 为 **vlHighResolutionImages**（需要的最低版本为2.20.8**）**\*。\*通过HTTP调用时，请将 **vl\_high\_resolution\_images**放入 **parameters** 对象中。

**vl\_enable\_image\_hw\_output**`boolean`（可选）默认值为 `false`

是否返回图像缩放后的尺寸。模型会对输入的图像进行缩放处理，配置为 True 时会返回图像缩放后的高度和宽度，开启流式输出时，该信息在最后一个数据块（chunk）中返回。支持[Qwen-VL模型](raw/model-user-guide/model-experience/vision-model/vision.md)。

> Java SDK中为 **vlEnableImageHwOutput**，Java SDK最低版本为2.20.8\*。\*通过HTTP调用时，请将 **vl\_enable\_image\_hw\_output**放入 **parameters** 对象中。

**max\_tokens**`integer`（可选，**即将废弃**）

> 该参数即将废弃，新接入请使用 `max_completion_tokens`。

该参数的含义随模型不同，具体如下：

-   deepseek-v4.1-flash、deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731：模型回答与思维链内容之和的最大 Token 数。模型输出超过此值时生成将提前停止，返回的 `finish_reason` 为 `length`。
-   glm-5.3：`max_tokens` 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 `finish_reason` 为 `length`。glm-5.3 会忽略 `thinking_budget` 参数。
-   glm-5.2：不传入 `thinking_budget` 参数时，`max_tokens` 为模型回答与思维链内容之和的最大 Token 数，模型输出超过此值时生成将提前停止，返回的 `finish_reason` 为 `length`；传入 `thinking_budget` 参数时，`max_tokens` 仅为模型回答的最大 Token 数，思维链部分的 Token 数由 `thinking_budget` 单独控制。
-   其他模型：模型回答的最大 Token 数（不包含思维链）。若生成内容超过此值，生成将提前停止，返回的 `finish_reason` 为 `length`。

默认值与最大值均为模型的最大输出长度。

> Java SDK中为**maxTokens**（模型为千问VL/Audio时，Java SDK中为**maxLength，**在 2.18.4 版本之后支持也设置为 maxTokens）\*。\*通过HTTP调用时，请将 **max\_tokens**放入 **parameters** 对象中。

**max\_completion\_tokens**`integer`（可选）

模型输出的最大长度，包含思维链和模型回答。模型输出超过此值时生成将提前停止，返回的 `finish_reason` 为 `length`。

默认值与最大值均为模型的最大输出长度。

与 `max_tokens` 的区别：`max_completion_tokens` 限制模型完整输出（思维链 + 回答），而 `max_tokens` 仅限制回答部分。思考类模型推荐使用 `max_completion_tokens`。

支持以下模型：

-   千问 Max：Qwen3.7-Max 及之后的模型
-   千问 Plus：Qwen3.5-Plus 及之后的模型
-   千问 Flash：Qwen3.5-Flash 及之后的模型
-   Kimi：kimi-k2.5 及其之后推出的Kimi模型
-   GLM：glm-5 及其之后推出的GLM系列模型
-   MiniMax：MiniMax-M2.5 及之后推出的MiniMax模型
-   DeepSeek：deepseek-v3、deepseek-r1、deepseek-r1-0528、deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v4-pro、deepseek-v4-flash 及之后推出的DeepSeek模型

> 以上模型均不包含三方直供模型。

> 实际输出 Token 数与设置的 `max_completion_tokens` 值之间最多可能存在 10 个 Token 的误差。

> Java SDK 暂不支持该参数。通过 HTTP 调用时，请将 **max\_completion\_tokens**放入 **parameters** 对象中。

**seed**`integer`（可选）

随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。

取值范围：`[0,2 31 −1]`。

seed默认值

qwen-vl-max、qvq-max系列：3407；

qwen-vl-max-2024-02-01、qwen-vl-plus：无默认值；

其余模型均为1234。

> 通过HTTP调用时，请将 **seed**放入 **parameters** 对象中。

**stream**`boolean`（可选）默认值为`false`

是否流式输出回复。参数值：

-   false：模型生成完所有内容后一次性返回结果。
-   true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。

> 该参数仅支持Python SDK。通过Java SDK实现流式输出请通过`streamCall`接口调用；通过HTTP实现流式输出请在Header中指定`X-DashScope-SSE`为`enable`。

> Qwen3商业版（思考模式）、Qwen3开源版、QwQ、QVQ只支持流式输出。

**incremental\_output**`boolean`（可选）默认为`false`（Qwen3-Max、Qwen3-VL、[Qwen3 开源版](raw/model-user-guide/get-started-with-models/models.md)、[QwQ](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) 、[QVQ](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)模型默认值为 `true`）

在流式输出模式下是否开启增量输出。推荐您优先设置为`true`。

参数值：

-   false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。

```
I
I like
I like apple
I like apple.
```

-   true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。

```
I
like
apple
.
```

> Java SDK中为**incrementalOutput**\*。\*通过HTTP调用时，请将 **incremental\_output**放入 **parameters** 对象中。

> QwQ 模型与思考模式下的 Qwen3 模型只支持设置为 `true`。由于 Qwen3 商业版模型默认值为`false`，您需要在思考模式下手动设置为 `true`。

> Qwen3 开源版模型不支持设置为 `false`。

**response\_format**`object` （可选） 默认值为`{"type": "text"}`

返回内容的格式。可选值：

-   `{"type": "text"}`：输出文字回复；
-   `{"type": "json_object"}`：输出标准格式的JSON字符串。
-   `{"type": "json_schema", "json_schema": {...}}`：输出严格符合指定 JSON Schema 的JSON字符串，可精确控制输出结构与字段类型。

> 相关文档：[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)。`json_object` 与 `json_schema` 支持的模型不同，参见[支持的模型](https://help.aliyun.com/zh/model-studio/qwen-structured-output#7a8e438e89xeq)。

> 若指定为`{"type": "json_object"}`，需在提示词中明确指示模型输出JSON，如：“请按照json格式输出”，否则会报错；若指定为`{"type": "json_schema", ...}`，提示词无需包含 JSON 关键词。

> Java SDK中为responseFormat\*。\*通过HTTP调用时，请将 **response\_format**放入 **parameters** 对象中。

属性

**type**`string`**（必选）**

返回内容的格式。可选值：

-   `text`：输出文字回复；
-   `json_object`：输出标准格式的JSON字符串；
-   `json_schema`：输出严格符合 `json_schema` 字段所定义结构的JSON字符串。

**json\_schema**`object`（可选）

`type` 为 `json_schema` 时必须设置，用于定义模型输出需要遵循的 JSON 结构。相关文档：[获取指定格式的输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output#a4f5d7108anxd)。

> DashScope 方式需手动构造 JSON Schema，格式与示例参见[获取指定格式的输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output#a4f5d7108anxd)。暂不支持 Java SDK。

属性

**name**`string`**（必选）**

Schema 的名称。

**schema**`object`**（必选）**

描述输出结构的 JSON Schema 对象。通过 `properties` 定义字段结构，通过 `required` 声明必填字段列表，通过 `additionalProperties` 控制是否允许输出未在 Schema 中定义的字段（推荐设置为 `false`，即只输出已定义的字段）。支持的数据类型：string、number、integer、boolean、object、array、enum。相关文档：[配置指南](https://help.aliyun.com/zh/model-studio/qwen-structured-output#001cb6ae072tc)。

**strict**`boolean`（可选）

是否严格遵循 `schema` 定义的结构。推荐设置为 `true`。

**result\_format**`string`（可选）默认为`text`（Qwen3-Max、Qwen3-VL、[QwQ](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) 模型、Qwen3 开源模型（除了qwen3-next-80b-a3b-instruct）与 Qwen-Long 模型默认值为 message）

返回数据的格式。推荐您优先设置为`message`，可以更方便地进行[多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)。

> 平台后续将统一调整默认值为`message`。

> Java SDK中为**resultFormat**\*。\*通过HTTP调用时，请将 **result\_format**放入 **parameters** 对象中。

> 模型为千问VL/QVQ/Audio时，设置`text`不生效。

> Qwen3-Max、Qwen3-VL、思考模式下的 Qwen3 模型只能设置为`message`，由于 Qwen3 商业版模型默认值为`text`，您需要将其设置为`message`。

> 如果您使用 Java SDK 调用Qwen3 开源模型，并且传入了 `text`，依然会以 `message`格式进行返回。

**logprobs** `boolean` （可选）默认值为 `false`

是否返回输出 Token 的对数概率，可选值：

-   `true`
    
    返回
    
-   `false`
    
    不返回
    

支持以下模型：

-   qwen-plus系列的快照模型（不包含稳定版模型）
-   qwen-turbo 系列的快照模型（不包含稳定版模型）
-   qwen3-vl-plus系列（包含稳定版模型）
-   qwen3-vl-flash系列（包含稳定版模型）
-   Qwen3 开源模型

> 通过HTTP调用时，请将 **logprobs**放入 **parameters** 对象中。

**top\_logprobs** `integer` （可选）默认值为0

指定在每一步生成时，返回模型最大概率的候选 Token 个数。

取值范围：\[0,5\]

仅当 `logprobs` 为 `true` 时生效。

> Java SDK中为**topLogprobs**\*。\*通过HTTP调用时，请将 **top\_logprobs**放入 **parameters** 对象中。

**n**`integer`（可选） 默认值为1

生成响应的个数，取值范围是`1-4`。对于需要生成多个响应的场景（如创意写作、广告文案等），可以设置较大的 n 值。

> 当前仅支持 [Qwen3（非思考模式）](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)、qwen-plus-character 模型，且在传入 tools 参数时固定为1。

> 设置较大的 n 值不会增加输入 Token 消耗，会增加输出 Token 的消耗。

> 通过HTTP调用时，请将 **n**放入 **parameters** 对象中。

**stop**`string 或 array`（可选）

用于指定停止词。当模型生成的文本中出现 `stop` 指定的字符串或 `token_id` 时，生成将立即终止。

可传入敏感词以控制模型的输出。

> stop为数组时，不可将`token_id`和字符串同时作为元素输入，比如不可以指定为`["你好",104307]`。

> 通过HTTP调用时，请将 **stop**放入 **parameters** 对象中。

**tools**`array`（可选）

包含一个或多个工具对象的数组，供模型在 Function Calling 中调用。相关文档：[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)

使用 `tools` 时，必须将`result_format`设为`message`。

发起 Function Calling，或提交工具执行结果时，都必须设置`tools`参数。

属性

**type**`string`**（必选）**

工具类型，当前仅支持`function`。

**function**`object`**（必选）**

属性

**name**`string`**（必选）**

工具函数的名称，必须是字母、数字，可以包含下划线和短划线，最大长度为64。

**description**`string`**（必选）**

工具函数的描述，供模型选择何时以及如何调用工具函数。

**parameters**`object`（可选）默认值为 `{}`

工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见[链接](https://json-schema.org/understanding-json-schema)。若`parameters`参数为空，表示该工具没有入参（如时间查询工具）。

> 为提高工具调用的准确性，建议传入 `parameters`。

> 通过HTTP调用时，请将 **tools**放入 **parameters** 对象中。暂时不支持qwen-vl与qwen-audio系列模型。

**tool\_choice**`string 或 object`（可选）默认值为 `auto`

工具选择策略。若需对某类问题强制指定工具调用方式（例如始终使用某工具或禁用所有工具），可设置此参数。

-   `auto`
    
    大模型自主选择工具策略；
    
-   `none`
    
    若在特定请求中希望临时禁用工具调用，可设定`tool_choice`参数为`none`；
    
-   `required`
    
    若希望强制调用至少一个工具，可设定`tool_choice`参数为`required`，模型将始终返回工具调用信息。
    
    > Qwen 系列模型暂不支持`required`：非思考模式下无法保证一定调用工具，思考模式下当前不支持`required`。
    
-   `{"type": "function", "function": {"name": "the_function_to_call"}}`
    
    若希望强制调用某个工具，可设定`tool_choice`参数为`{"type": "function", "function": {"name": "the_function_to_call"}}`，其中`the_function_to_call`是指定的工具函数名称。
    
    > 思考模式的模型不支持强制调用某个工具。
    

> Java SDK中为**toolChoice**\*。\*通过HTTP调用时，请将 **tool\_choice**放入 **parameters** 对象中。

**parallel\_tool\_calls** `boolean` （可选）默认值为 `false`

是否开启并行工具调用。

可选值：

-   `true`：开启
-   `false`：不开启。

并行工具调用详情请参见：[并行工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#cb6b5c484bt4x)。

> Java SDK中为**parallelToolCalls**\*。\*通过HTTP调用时，请将 **parallel\_tool\_calls**放入 **parameters** 对象中。

**enable\_search**`boolean`（可选）默认值为`false`

模型在生成文本时是否使用互联网搜索结果进行参考。取值如下：

-   true：启用互联网搜索，模型会将搜索结果作为文本生成过程中的参考信息，但模型会基于其内部逻辑判断是否使用互联网搜索结果。
    
    > 若开启后未联网搜索，可优化提示词，或设置`search_options`中的`forced_search`参数开启强制搜索。
    
-   false：关闭互联网搜索。
    

计费信息请参见[计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)。

> Java SDK中为**enableSearch**\*。\*通过HTTP调用时，请将 **enable\_search**放入 **parameters** 对象中。

> 启用互联网搜索功能可能会增加 Token 的消耗。

**search\_options**`object`（可选）

联网搜索的策略。仅当`enable_search`为`true`时生效。详情参见[联网搜索](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md)。

> 通过HTTP调用时，请将 **search\_options**放入 **parameters** 对象中。Java SDK中为**searchOptions**。

属性

**enable\_source**`boolean`（可选）默认值为`false`

在返回结果中是否展示搜索到的信息。参数值：

-   true：展示；
-   false：不展示。

**enable\_citation** `boolean`（可选）默认值为`false`

是否开启\[1\]或\[ref\_1\]样式的角标标注功能。在`enable_source`为`true`时生效。参数值：

-   true：开启；
-   false：不开启。

**citation\_format** `string`（可选）默认值为`"[<number>]"`

角标样式。在`enable_citation`为`true`时生效。参数值：

-   \[<number>\]：角标形式为`[1]`；
-   \[ref\_<number>\]：角标形式为`[ref_1]`。

**forced\_search** `boolean`（可选）默认值为`false`

是否强制开启搜索。参数值：

-   true：强制开启；
-   false：不强制开启。

**search\_strategy** `string`（可选）默认值为`turbo`

搜索互联网信息的策略。

可选值：

-   `turbo` （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。
    
-   `max`: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。
    
-   `agent`：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。
    
    > 该策略仅适用于qwen3.8-max、qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3-max与 qwen3-max-2026-01-23 的思考模式（仅支持流式）、qwen3-max-2026-01-23的非思考模式、qwen3-max-2025-09-23。
    
    > 启用该策略时，仅支持**返回搜索来源**（`enable_source: true`），其他联网搜索功能不可用。
    
-   `agent_max`：在`agent`策略基础上支持网页抓取，参见：[网页抓取](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-extractor.md)。
    
    > 该策略仅适用于qwen3.8-max、qwen3.7-max、qwen3.7-max-2026-05-20、qwen3-max、qwen3-max-2026-01-23的思考模式。
    
    > 启用该策略时，仅支持**返回搜索来源**（`enable_source: true`），其他联网搜索功能不可用。
    

**enable\_search\_extension** `boolean`（可选）默认值为`false`

是否开启特定领域增强。参数值：

-   `true`
    
    开启。
    
-   `false`（默认值）
    
    不开启。
    

**prepend\_search\_result** `boolean`（可选）默认值为`false`

在流式输出且`enable_source`为`true`时，可通过`prepend_search_result`配置**第一个返回的数据包**是否只包含搜索来源信息。可选值：

-   `true`
    
    只包含搜索来源信息。
    
-   `false`（默认值）
    
    包含搜索来源信息与大模型回复信息。
    

> 暂不支持 DashScope Java SDK。

**X-DashScope-DataInspection**`string` （可选）

在千问 API 的内容安全能力基础上，是否进一步识别输入输出内容的违规信息。取值如下：

-   `'{"input":"cip","output":"cip"}'`：进一步识别；
-   不设置该参数：不进一步识别。

通过 HTTP 调用时请放入请求头：`-H "X-DashScope-DataInspection: {\"input\": \"cip\", \"output\": \"cip\"}"`；

通过 Python SDK 调用时请通过`headers`配置：`headers={'X-DashScope-DataInspection': '{"input":"cip","output":"cip"}'}`。

详细使用方法请参见[输⼊输出 AI 安全护栏](raw/model-user-guide/security-and-compliance/content-security.md)。

> 不支持通过 Java SDK 设置。

> 不适用于Qwen-Audio 系列模型。

**skill**`array`（可选）

技能参数，用于启用特定生成技能（如PPT生成）。仅`qwen-doc-turbo`模型支持。详细用法请参见[生成PPT](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc#f6a7b8c9d0pp1)。

> 通过HTTP调用时，请将 **skill**放入 **parameters** 对象中。

> 使用 **skill 时，stream** 必须设置为 **true**。

属性

**type**`string`**（必选）**

技能类型。当前支持：

-   `ppt`：PPT生成。

**mode**`string` （可选）

PPT生成模式。可选值：

-   `general` （默认值）：模板模式，需配合`template_id` 使用，生成HTML格式的PPT。
-   `creative` ：创意模式，无需模板，生成图版PPT（每页为图片）。

**template\_id**`string`（可选）

PPT模板ID。与`mode`为`general`或未设置`mode`时配合使用。可选值：

-   `news_01`：新闻模板
-   `summary_01`：总结模板
-   `internet_01`：互联网模板
-   `thesis_01`：论文模板

#### 文本输入

#### Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {'role': 'system', 'content': [{'text': 'You are a helpful assistant.'}]},
    {'role': 'user', 'content': [{'text': '你是谁？'}]}
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    )
print(response)
```

#### Java

```
// 建议dashscope SDK的版本 >= 2.12.0
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static MultiModalConversationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "You are a helpful assistant.")))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "你是谁？")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen3.8-max")
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
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

#### PHP（HTTP）

```
<?php

$url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation";
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    "model" => "qwen3.8-max",
    "input" => [
        "messages" => [
            [
                "role" => "system",
                "content" => [["text" => "You are a helpful assistant."]]
            ],
            [
                "role" => "user",
                "content" => [["text" => "你是谁？"]]
            ]
        ]
    ],
    "parameters" => [
        "result_format" => "message"
    ]
];

$jsonData = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $apiKey",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    echo "Response: " . $response;
} else {
    echo "Error: " . $httpCode . " - " . $response;
}

curl_close($ch);
?>
```

#### Node.js（HTTP）

DashScope 未提供 Node.js 环境的 SDK。如需通过 OpenAI Node.js SDK调用，请参考本文的[OpenAI](raw/model-api-reference/qwen-api-reference.md)章节。

```
import fetch from 'node-fetch';

const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    model: "qwen3.8-max", // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    input: {
        messages: [
            {
                role: "system",
                content: [{ text: "You are a helpful assistant." }]
            },
            {
                role: "user",
                content: [{ text: "你是谁？" }]
            }
        ]
    },
    parameters: {
        result_format: "message"
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
.then(response => response.json())
.then(data => {
    console.log(JSON.stringify(data));
})
.catch(error => {
    console.error('Error:', error);
});
```

#### C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }

        // 设置请求 URL 和内容
        string url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation";
        // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen3.8-max"",
            ""input"": {
                ""messages"": [
                    {
                        ""role"": ""system"",
                        ""content"": [{""text"": ""You are a helpful assistant.""}]
                    },
                    {
                        ""role"": ""user"",
                        ""content"": [{""text"": ""你是谁？""}]
                    }
                ]
            },
            ""parameters"": {
                ""result_format"": ""message""
            }
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

#### Go（HTTP）

DashScope 未提供 Go 的 SDK。如需通过 OpenAI Go SDK调用，请参考本文的[OpenAI-Go](raw/model-api-reference/qwen-api-reference.md)章节。

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type ContentItem struct {
	Text string `json:"text"`
}

type Message struct {
	Role    string        `json:"role"`
	Content []ContentItem `json:"content"`
}

type Input struct {
	Messages []Message `json:"messages"`
}

type Parameters struct {
	ResultFormat string `json:"result_format"`
}

type RequestBody struct {
	Model      string     `json:"model"`
	Input      Input      `json:"input"`
	Parameters Parameters `json:"parameters"`
}

func main() {
	// 创建 HTTP 客户端
	client := &http.Client{}

	// 构建请求体
	requestBody := RequestBody{
		// 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
		Model: "qwen3.8-max",
		Input: Input{
			Messages: []Message{
				{
					Role:    "system",
					Content: []ContentItem{{Text: "You are a helpful assistant."}},
				},
				{
					Role:    "user",
					Content: []ContentItem{{Text: "你是谁？"}},
				},
			},
		},
		Parameters: Parameters{
			ResultFormat: "message",
		},
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}

	// 创建 POST 请求
	req, err := http.NewRequest("POST", "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}

	// 设置请求头
	// 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey := "sk-xxx"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

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
	fmt.Printf("%s\n", bodyText)
}
```

#### curl

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": [{"text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [{"text": "你是谁？"}]
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

#### dashscope CLI

通过 dashscope 命令行调用。

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope generation create -m qwen-plus -p "你好"
```

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

#### 流式输出

> 相关文档：[流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md)。

#### 文本生成模型

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {'role':'system','content':'you are a helpful assistant'},
    {'role': 'user','content': '你是谁？'}
]
responses = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换为其它文本生成模型
    messages=messages,
    result_format="message",
    stream=True,
    incremental_output=True
    )
for response in responses:
    print(response.output.choices[0].message.content, end="")
```

Java

```
import java.util.Arrays;
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static void handleGenerationResult(GenerationResult message) {
        System.out.println(JsonUtils.toJson(message));
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换为其它文本生成模型
                .model("qwen-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true)
                .build();
    }
    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
        } catch (ApiException | NoApiKeyException | InputRequiredException  e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--header "X-DashScope-SSE: enable" \
--data '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message",
        "incremental_output":true
    }
}'
```

#### 多模态模型

Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 若使用新加坡地域的模型，请取消下列注释
# dashscope.base_http_api_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"text": "图中描绘的是什么景象?"}
        ]
    }
]

responses = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3-vl-plus',  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    stream=True,
    incremental_output=True
    )

full_content = ""
print("流式输出内容为：")
for response in responses:
    if response.output.choices[0].message.content:
        print(response.output.choices[0].message.content[0]['text'])
        full_content += response.output.choices[0].message.content[0]['text']
print(f"完整内容为：{full_content}")
```

Java

```
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
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请取消下列注释
    //  static {Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")  // 可按需更换为其它多模态模型，并修改相应的 messages
                .messages(Arrays.asList(userMessage))
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                    // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
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
```

curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象？"}
                ]
            }
        ]
    },
    "parameters": {
        "incremental_output": true
    }
}'
```

#### 图像输入

> 关于大模型分析图像的更多用法，请参见[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)。

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"},
            {"text": "这些是什么?"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-vl-max', # 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
    )
print(response)
```

Java

```
// Copyright (c) Alibaba, Inc. and its affiliates.

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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"),
                        Collections.singletonMap("text", "这些是什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-vl-plus")
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
```

curl

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"},
                    {"text": "这些是什么?"}
                ]
            }
        ]
    }
}'
```

#### 视频输入

> 以下为传入视频帧的示例代码，关于更多用法（如传入视频文件），请参见[视觉理解](https://help.aliyun.com/zh/model-studio/vision#80dbf6ca8fh6s)。

Python

```
from http import HTTPStatus
import os
# dashscope版本需要不低于1.20.10
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [{"role": "user",
             "content": [
                 {"video":["https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                           "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"]},
                 {"text": "描述这个视频的具体过程"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen-vl-max',  # 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
)
if response.status_code == HTTPStatus.OK:
    print(response)
else:
    print(response.code)
    print(response.message)
```

Java

```
// DashScope SDK版本需要不低于2.16.7
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    // 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    private static final String MODEL_NAME = "qwen-vl-max";
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "You are a helpful assistant.")))
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("video", Arrays.asList("https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                                "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg")),
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
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
```

curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-vl-max",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
              "https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
              "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"
            ]
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

#### 音频输入

#### 音频理解

> 关于大模型分析音频的更多用法，请参见[音频理解-Qwen-Audio](https://help.aliyun.com/zh/model-studio/audio-language-model)。

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
            {"text": "这段音频在说什么?"}
        ]
    }
]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-audio-turbo', # 此处以qwen-audio-turbo为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
    )
print(response)
```

Java

```
import java.util.Arrays;
import java.util.Collections;
import java.lang.System;
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"),
                        Collections.singletonMap("text", "这段音频在说什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-audio-turbo为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-audio-turbo")
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
```

curl

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-audio-turbo",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": [
                    {"text": "You are a helpful assistant."}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"},
                    {"text": "这段音频在说什么?"}
                ]
            }
        ]
    }
}'
```

#### 联网搜索

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {'role': 'system', 'content': [{'text': 'You are a helpful assistant.'}]},
    {'role': 'user', 'content': [{'text': '杭州明天天气是什么？'}]}
    ]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.8-max", # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    enable_search=True,
    )
print(response)
```

Java

```
// 建议dashscope SDK的版本 >= 2.12.0
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static MultiModalConversationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "You are a helpful assistant.")))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "明天杭州什么天气？")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen3.8-max")
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
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": [{"text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [{"text": "明天杭州天气如何？"}]
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "result_format": "message"
    }
}'
```

#### 工具调用

> 完整的Function Calling 流程代码请参见[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)。

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]
messages = [{"role": "user", "content": [{"text": "杭州天气怎么样"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.8-max',  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    tools=tools,
)
print(response)
```

Java

```
import java.util.ArrayList;
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public class GetWeatherTool {
        private String location;
        public GetWeatherTool(String location) {
            this.location = location;
        }
        public String call() {
            return location+"今天是晴天";
        }
    }
    public class GetTimeTool {
        public GetTimeTool() {
        }
        public String call() {
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            String currentTime = "当前时间：" + now.format(formatter) + "。";
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
        FunctionDefinition fdWeather = FunctionDefinition.builder().name("get_current_weather").description("获取指定地区的天气")
                .parameters(JsonUtils.parseString(jsonSchema_weather.toString()).getAsJsonObject()).build();
        FunctionDefinition fdTime = FunctionDefinition.builder().name("get_current_time").description("获取当前时刻的时间")
                .parameters(JsonUtils.parseString(jsonSchema_time.toString()).getAsJsonObject()).build();
        MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "You are a helpful assistant. When asked a question, use tools wherever possible.")))
                .build();
        MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue()).content(Arrays.asList(Collections.singletonMap("text", "杭州天气"))).build();
        List<MultiModalMessage> messages = new ArrayList<>();
        messages.addAll(Arrays.asList(systemMsg, userMsg));
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen3.8-max")
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
            System.out.println(String.format("Exception %s", e.getMessage()));
        }
        System.exit(0);
    }
}
```

curl

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen3.8-max",
    "input": {
        "messages": [{
            "role": "user",
            "content": [{"text": "杭州天气怎么样"}]
        }]
    },
    "parameters": {
        "result_format": "message",
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "当你想知道现在的时间时非常有用。",
                "parameters": {}
            }
        },{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                        }
                    }
                },
                "required": ["location"]
            }
        }]
    }
}'
```

#### 异步调用

```
# 您的Dashscope Python SDK版本需要不低于 1.19.0。
import asyncio
import platform
import os
from dashscope.aigc.multimodal_conversation import AioMultiModalConversation

async def main():
    response = await AioMultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen3.8-max",  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "user", "content": [{"text": "你是谁"}]}],
    )
    print(response)

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
```

#### 文档理解

#### Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
        {'role': 'system', 'content': 'you are a helpful assisstant'},
        # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
        {'role':'system','content':f'fileid://{FILE_ID}'},
        {'role': 'user', 'content': '这篇文章讲了什么'}]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-long",
    messages=messages,
    result_format="message",
)
print(response)
```

#### Java

```
import java.util.Arrays;
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
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static GenerationResult callWithFile() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();

        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("you are a helpful assistant")
                .build();

        Message fileSystemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                // 请将 '{FILE_ID}'替换为您实际对话场景所使用的 file-id
                .content("fileid://{FILE_ID}")
                .build();

        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("这篇文章讲了什么")
                .build();

        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-long")
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
            System.err.println("调用 DashScope API 出错: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

#### curl

> 请将 {FILE\_ID}替换为您实际对话场景所使用的 file-id

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-long",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "system",
                "content": "fileid://{FILE_ID}"
            },
            {
                "role": "user",
                "content": "这篇文章讲了什么？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

#### PPT生成

> PPT生成功能仅`qwen-doc-turbo`模型支持。详细用法请参见[生成PPT](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc#f6a7b8c9d0pp1)。

Python

```
import os
import dashscope
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

response = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-doc-turbo',
    messages=[
        {"role": "system", "content": "you are a helpful assistant."},
        {"role": "system", "content": "您的文档内容"},
        {"role": "user", "content": "生成一个10到20页的ppt"}
    ],
    result_format="message",
    skill=[{"type": "ppt", "mode": "general", "template_id": "news_01"}]
)
try:
    if response.status_code == 200:
        print(response.output.choices[0].message.content)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
except Exception as e:
    print(f"发生错误: {e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

curl

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--header 'X-DashScope-SSE: enable' \
--data '{
    "model": "qwen-doc-turbo",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            {
                "role": "system",
                "content": "您的文档内容"
            },
            {
                "role": "user",
                "content": "生成一个10到20页的ppt"
            }
        ]
    },
    "parameters": {
        "skill": [
            {
                "type": "ppt",
                "mode": "general",
                "template_id": "news_01"
            }
        ]
    }
}'
```

## chat响应对象（流式与非流式输出格式一致）

**status\_code**`string`

本次请求的状态码。200 表示请求成功，否则表示请求失败。

> Java SDK不会返回该参数。调用失败会抛出异常，异常信息为**status\_code**和**message**的内容。

**request\_id**`string`

本次调用的唯一标识符。

> Java SDK返回参数为**requestId。**

**code**`string`

错误码，调用成功时为空值。

> 只有Python SDK返回该参数。

**output**`object`

调用结果信息。

属性

**text**`string`

模型生成的回复。当设置输入参数**result\_format**为**text**时将回复内容返回到该字段。

**finish\_reason**`string`

当设置输入参数**result\_format**为**text**时该参数不为空。

有四种情况：

-   正在生成时为null；
-   因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
-   因生成长度过长而结束为length；
-   因发生工具调用为tool\_calls。

**choices**`array`

模型的输出信息。当result\_format为message时返回choices参数。

属性

**finish\_reason**`string`

有四种情况：

-   正在生成时为null；
-   因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
-   因生成长度过长而结束为length；
-   因发生工具调用为tool\_calls。

**message**`object`

模型输出的消息对象。

属性

**role**`string`

输出消息的角色，固定为assistant。

**content**`string或array`

输出消息的内容。当使用qwen-vl或qwen-audio系列模型时为`array`，其余情况为`string`。

> 如果发起Function Calling，则该值为空。

属性

**text**`string`

当使用qwen-vl或qwen-audio系列模型时，输出消息的内容。

**image\_hw**`array`

当Qwen-VL系列模型启用 vl\_enable\_image\_hw\_output 参数时，有两种情况：

-   图像输入：返回图像的高度和高度（数值单位：像素）
-   视频输入：返回空数组

**reasoning\_content** `string`

模型的深度思考内容。

**tool\_calls**`array`

若模型需要调用工具，则会生成tool\_calls参数。

属性

**function**`object`

调用工具的名称，以及输入参数。

属性

**name**`string`

调用工具的名称

**arguments**`string`

需要输入到工具中的参数，为JSON字符串。

> 由于大模型响应有一定随机性，输出的JSON字符串并不总满足于您的函数，建议您在将参数输入函数前进行参数的有效性校验。

**index** `integer`

当前**tool\_calls**对象在tool\_calls数组中的索引。

**id** `string`

本次工具响应的ID。

**type** `string`

工具类型，固定为`function`。

**logprobs**`object`

当前 choices 对象的概率信息。

属性

**content** `array`

带有对数概率信息的 Token 数组。

属性

**token** `string`

当前 Token。

**bytes** `array`

当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。

**logprob** `float`

当前 Token 的对数概率。返回值为 null 表示概率值极低。

**top\_logprobs** `array`

当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的`top_logprobs`保持一致。

属性

**token** `string`

当前 Token。

**bytes** `array`

当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。

**logprob** `float`

当前 Token 的对数概率。返回值为 null 表示概率值极低。

**search\_info**`object`

联网搜索到的信息，在设置`search_options`参数后会返回该参数。

属性

**search\_results**`array`

联网搜索到的结果。

属性

**site\_name**`string`

搜索结果来源的网站名称。

**icon**`string`

来源网站的图标URL，如果没有图标则为空字符串。

**index**`integer`

搜索结果的序号，表示该搜索结果在`search_results`中的索引。

**title**`string`

搜索结果的标题。

**url**`string`

搜索结果的链接地址。

**extra\_tool\_info**`array`

开启`enable_search_extension`参数后返回的领域增强信息。

属性

**result**`string`

领域增强工具输出信息。

**tool**`string`

领域增强使用的工具。

**usage**`map`

本次chat请求使用的Token信息。

属性

**input\_tokens** `integer`

用户输入内容转换成Token后的长度。[补充说明](https://help.aliyun.com/zh/model-studio/text-generation#e710782c79xqy)

**output\_tokens** `integer`

模型输出内容转换成Token后的长度。

**input\_tokens\_details** `object`（可选）

输入内容转换成 Token 后的长度详情。

属性

**text\_tokens** `integer`（可选）

输入的文本转换为 Token 后的长度。

**image\_tokens** `integer`（可选）

输入的图像转换为Token后的长度。

**video\_tokens** `integer`（可选）

输入的视频文件或图像列表转换为Token后的长度。

**total\_tokens** `integer`

当输入为纯文本时返回该字段，为**input\_tokens**与**output\_tokens**之和**。**

**image\_tokens** `integer`

输入内容包含`image`时返回该字段。为用户输入图片内容转换成Token后的长度。

**video\_tokens** `integer`

输入内容包含`video`时返回该字段。为用户输入视频内容转换成Token后的长度。

**audio\_tokens** `integer`

输入内容包含`audio`时返回该字段。为用户输入音频内容转换成Token后的长度。

**output\_tokens\_details** `object`（可选）

输出内容转换成 Token 后的长度详情。部分模型返回该字段。

属性

**text\_tokens** `integer`（可选）

输出的文本转换为Token后的长度。

**reasoning\_tokens** `integer`（可选）

思考过程转换为Token后的长度。仅推理模型返回该字段。

**audio\_tokens** `integer`（可选）

输出的音频转换为 Token 后的长度。仅音频输出模型返回该字段。

**prompt\_tokens\_details** `object`

输入 Token 的细粒度分类。

属性

**cached\_tokens** `integer`

命中 Cache 的 Token 数。Context Cache 详情请参见[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

**cache\_creation** `object`

[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)创建信息。

属性

**ephemeral\_5m\_input\_tokens** `integer`

用于创建5分钟有效期显式缓存的 Token 长度。

**cache\_creation\_input\_tokens** `integer`

用于创建显式缓存的 Token 长度。

**cache\_type** `string`

使用[显式缓存](https://help.aliyun.com/zh/model-studio/context-cache#825f201c5fy6o)时，参数值为`ephemeral`，否则该参数不存在。

```
{
  "status_code": 200,
  "request_id": "902fee3b-f7f0-9a8c-96a1-6b4ea25af114",
  "code": "",
  "message": "",
  "output": {
    "text": null,
    "finish_reason": null,
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": "我是阿里云开发的一款超大规模语言模型，我叫千问。"
        }
      }
    ]
  },
  "usage": {
    "input_tokens": 22,
    "output_tokens": 17,
    "total_tokens": 39
  }
}
```

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
