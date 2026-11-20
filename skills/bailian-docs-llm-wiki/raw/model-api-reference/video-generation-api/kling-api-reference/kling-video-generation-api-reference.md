# 可灵-视频生成API文档

可灵-视频生成模型支持 文生视频、图生视频-基于首帧、图生视频-基于首尾帧、参考生视频以及视频编辑 。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 服务开通

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“kling”，找到**可灵AI**模型卡片，单击**立即开通**，在弹窗内确认开通及授权。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](raw/model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)。

## 模型概览

模型名称

能力支持

输入模态

输出视频规格

kling/kling-v3-turbo-video-generation

文生视频；图生视频-基于首帧

文本、图像

分辨率模式：std（720P）、pro（1080P）；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4

kling/kling-v3-video-generation

文生视频；图生视频-基于首帧；图生视频-基于首尾帧

文本、图像

分辨率模式：std（720P）、pro（1080P）、4k；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4

kling/kling-v3-omni-video-generation

文生视频；图生视频-基于首帧；图生视频-基于首尾帧；参考生视频；视频编辑

文本、图像、视频

分辨率模式：std（720P）、pro（1080P）、4k；宽高比：16:9、9:16、1:1；视频时长：3-15秒；视频格式：MP4

以下两个 Kling 4.0 模型均仅在华北2（北京）地域提供，采用相同的百炼异步调用流程，但支持的素材不同：

模型名称

能力支持

输入模态

输出视频规格

kling/kling-v4-video-generation

文生视频、关键帧生视频（首帧、中间帧、尾帧可任意组合）

文本、帧图

`std`（720P）、`pro`（1080P）；21:9、16:9、9:16、1:1；3～30秒；MP4（H.264）

kling/kling-v4-omni-reference-video-generation

文生视频、关键帧生视频、参考生视频、视频编辑

文本、帧图、参考图、视频、主体

`std`（720P）、`pro`（1080P）；21:9、16:9、9:16、1:1；3～30秒；MP4（H.264）

4.0 固定生成有声视频，不支持 `4k` 模式。模型和素材的详细限制见下文请求参数。

## HTTP调用

由于视频生成任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

#### 请求参数

##### 请求头（Headers）

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async**`string`**（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`enable`。

**重要**缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `string` **（必选）**

模型名称。

可选值：

-   `kling/kling-v3-turbo-video-generation`
-   `kling/kling-v3-video-generation`
-   `kling/kling-v3-omni-video-generation`
-   `kling/kling-v4-video-generation`
-   `kling/kling-v4-omni-reference-video-generation`

**input** `object` **（必选）**

输入的基本信息，如提示词、媒体素材等。

属性

**prompt** `string` （条件必填）

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

3.0 模型支持中英文，每个汉字/字母占一个字符，不超过2500个字符，超过将返回错误。填写逻辑：

-   当 `shot_type=intelligence` 时，此参数**必填**。
-   当 `shot_type=customize` 时，此参数**不生效**，请以 `multi_prompt` 为准。

4.0 模型可在 `prompt` 中同时描述期望和不期望出现的内容，并直接描述分镜需求：

-   `kling/kling-v4-video-generation`：文生视频时必填；传入帧图时可不填。
-   `kling/kling-v4-omni-reference-video-generation`：必填。
-   纯英文最多26000个字符，纯非英文最多11000个字符；中英文混合时，英文字符数 ÷ 26000 + 非英文字符数 ÷ 11000 ≤ 1。

Omni 模型可在 `prompt` 中引用主体、图片、视频等内容：

-   支持模型：`kling/kling-v3-omni-video-generation`、`kling/kling-v4-omni-reference-video-generation`；3.0 的此用法适用于参考生视频。
-   引用格式：使用 `<<<element_1>>>`、`<<<image_1>>>`、`<<<video_1>>>` 等标记；4.0 还可使用 `<<<voice_1>>>` 引用 `voice_list` 中的音色。
-   引用顺序：4.0 的图片、视频分别按 `media` 中同类素材的出现顺序编号，主体和音色分别按 `element_list`、`voice_list` 的顺序编号；3.0 按 `media` 数组顺序定义图片和视频的引用顺序。
-   用法示例：`一只<<<element_1>>>在月光下奔跑`。

**negative\_prompt** `string` （可选）

3.0 模型的负向提示词，用于描述不希望在结果中出现的内容，不超过2500个字符。

-   `kling/kling-v3-turbo-video-generation` 无独立负向提示词能力，该字段不生效（负向描述可写入`prompt`）。
-   支持模型：`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`。
-   4.0 模型的此字段不生效，请将负向描述写入 `prompt`。

**media** `array` （可选）

文生视频任务无需填写此参数。

媒体素材列表，用于指定图像或视频素材。

不同模型支持的媒体素材搭配不一样：

素材组合规则

kling/kling-v3-turbo-video-generation

仅支持以下媒体素材组合，非法组合将报错。

-   **图生视频-基于首帧**：`first_frame`。
    
    -   数量限制：首帧恰好1张。不支持`last_frame`。

kling/kling-v3-video-generation

仅支持以下媒体素材组合，非法组合将报错。

-   **图生视频-基于首帧**：`first_frame`。
    
    -   数量限制：首帧1张。
-   **图生视频-基于首尾帧**：`first_frame+last_frame`。
    
    -   数量限制：首帧1张，尾帧1张。

kling/kling-v3-omni-video-generation

仅支持以下媒体素材组合，非法组合将报错。

-   **图生视频-基于首帧**：`first_frame`。
    
    -   图像数量：首帧1张。
-   **图生视频-基于首尾帧**：`first_frame+last_frame`。
    
    -   图像数量：首帧1张，尾帧1张。
-   **参考生视频**：支持以下 `media` 组合。
    
    -   仅传入 `feature` 时：必须传入1个视频。
    -   仅传入 `refer` 时：参考图片与多图主体数量（`element_list` 的数组长度）之和不得超过7。
    -   传入 `feature+refer` 时：必须传入1个视频，且参考图片与多图主体数量（`element_list` 的数组长度）之和不得超过4。
    -   传入 `feature+first_frame` 时：必须传入1个视频和1张首帧。
-   **视频编辑**：支持以下 `media` 组合。
    
    -   仅传入 `base` 时：必须传入1个视频。
    -   传入 `base+refer` 时：必须传入1个视频，且参考图片与多图主体数量（`element_list` 的数组长度）之和不得超过4。

kling/kling-v4-video-generation

支持 `first_frame`、`middle_frame`、`last_frame` 任意组合，也可不传 `media` 进行文生视频；可仅传尾帧或中间帧。首帧和尾帧各最多1张，帧图总数不超过10张。不支持 `refer`、`feature`、`base` 或 `element_list`。

kling/kling-v4-omni-reference-video-generation

支持帧图、参考图（`refer`）、特征参考视频（`feature`）、待编辑视频（`base`）及主体；3.0 的素材互斥限制不适用于此模型，尾帧无需与首帧同时传入，`base` 可与帧图和 `feature` 组合。

-   图片（首帧、中间帧、尾帧和参考图）合计不超过10张，首帧和尾帧各最多1张。
-   视频（`feature` 和 `base`）合计不超过5个，`base` 最多1个；视频角色主体与参考视频合计不超过5个。
-   主体最多7个，其中视频角色主体最多3个；音色最多3个，已绑定音色的主体不占音色数量。
-   图片、视频、主体、音色合计不超过15个。素材规格见下文 `url` 参数。

属性

**type** `string` **（必选）**

媒体素材类型。可选值与所选模型有关：

kling/kling-v3-turbo-video-generation

可选值：

-   `first_frame`：首帧图片。

不支持`last_frame`。不同媒体素材之间的搭配限制，请参见 `media` 参数下的”素材组合规则”。

kling/kling-v3-video-generation

可选值：

-   `first_frame`：首帧图片。
-   `last_frame`：尾帧图片。

不同媒体素材之间的搭配限制，请参见 `media` 参数下的”素材组合规则”。

kling/kling-v3-omni-video-generation

可选值：

-   `first_frame`：首帧图片。
-   `last_frame`：尾帧图片。
-   `refer`：参考图片。
-   `base`：待编辑视频。
-   `feature`：特征参考视频。

不同媒体素材之间的搭配限制，请参见 `media` 参数下的“素材组合规则”。

kling/kling-v4-video-generation

-   `first_frame`：首帧图片。
-   `middle_frame`：中间帧图片，可传多张。
-   `last_frame`：尾帧图片。

kling/kling-v4-omni-reference-video-generation

-   `first_frame`、`middle_frame`、`last_frame`：首帧、中间帧和尾帧图片。
-   `refer`：参考图片。
-   `feature`：特征参考视频。
-   `base`：待编辑视频。

**url** `string` **（必选）**

媒体素材URL。素材包括图像、视频。

传入图像（type=first\_frame、middle\_frame、last\_frame或refer）

图像URL。

-   支持 HTTP 或 HTTPS 协议。
-   示例值：`https://example.com/image.png`。

3.0 模型的图像限制：

-   格式：JPEG、JPG、PNG（不支持透明通道）。
-   分辨率：宽和高的范围为\[300, 8000\]像素。
-   宽高比：1:2.5 ~ 2.5:1。
-   文件大小：不超过10MB。

4.0 模型的图像限制：

-   格式：JPG、JPEG、PNG。
-   分辨率：宽和高均不小于300像素。
-   宽高比：2:5～5:2。
-   文件大小：不超过30MB。

传入视频（type=base或feature）

视频文件的 URL。

-   支持 HTTP 和 HTTPS 协议。
-   示例值：`https://example.com/video.mp4`。

3.0 Omni 模型的视频限制：

-   格式：mp4、mov。
-   文件大小：不超过200MB。
-   时长：3～15.5s。
-   分辨率：宽和高的范围为\[700, 4553\]像素，像素总面积不超过8294400。
-   宽高比：0.4～2。
-   帧率：24～60fps。

4.0 Omni 模型的视频限制（`feature`、`base`）：

-   格式：MP4、MOV；单个文件不超过300MB。
-   单个视频及输入视频总时长均为3～30秒；输入视频总时长还包含视频角色主体的时长。
-   宽和高均在700～4553像素之间，像素总面积不超过8294400；宽高比2:5～5:2，帧率24～60fps。

**keep\_original\_sound** `string` （可选）

支持模型：kling/kling-v3-omni-video-generation 。

生效条件：当且仅当传入视频（type=base或feature）时生效。

是否保留原视频声音。

-   `no`：默认值，不保留原声。
-   `yes`：保留原声。

4.0 Omni 模型不保留输入视频原声：传 `yes` 会导致参数错误，传 `no` 或不传不受影响。

**multi\_shot** `boolean` （可选）

3.0 模型是否开启多镜头生成。

-   `false`：默认值，不开启多镜头。
-   `true`：开启多镜头生成。

注意：

-   3.0 的视频特征参考（feature）场景支持开启多镜头（`shot_type`仅支持`intelligence`）。
-   3.0 的视频编辑（base）场景不支持多镜头。
-   4.0 默认智能分镜，无需设置此字段；传入任何 `multi_shot` 值均不生效。分镜需求直接写在 `prompt` 中。

**shot\_type** `string` （条件必填）

3.0 模型在 `multi_shot=true` 时必填。多镜头模式类型。

-   `intelligence`：智能分镜，由模型自动规划镜头。
-   `customize`：自定义模式，支持自定义每个片段的提示词和时长。

4.0 模型不使用此字段；传入 `shot_type=customize` 会导致参数错误，分镜需求请直接写在 `prompt` 中。

**multi\_prompt** `array` （条件必填）

3.0 模型在 `shot_type=customize` 时必填。多镜头自定义模式下的片段列表。4.0 模型传入此字段会导致参数错误。

属性

**index** `integer` **（必选）**

分镜片段索引，分镜数量为1～6个，索引从1开始。

**prompt** `string` **（必选）**

对应片段的提示词，支持中英文，不超过512个字符，超过自动截断。

**duration** `integer` **（必选）**

对应片段的时长，单位为秒。

取值为\[1, `parameters.duration`\]之间的整数。

**element\_list** `array` （可选）

主体列表，用于指定视频中需要引入的主体元素。

注意：`kling/kling-v3-turbo-video-generation` 和 `kling/kling-v4-video-generation` 不支持主体，该字段不可传。

属性

**element\_id** `integer` （条件必填）

传`element_list`时必填，表示主体ID。请在[可灵-官方主体库](https://help.aliyun.com/zh/model-studio/kling-object-ids#entity-library)获取主体ID。

3.0 模型的主体个数限制（`element_list` 数组长度限制）：

-   图生视频-基于首帧：最多支持3个主体。
-   图生视频-基于首尾帧：最多支持3个主体。
-   参考生视频（`type=refer`）：参考图片与多图主体数量之和不得超过7。
-   参考生视频（`type=feature+refer`）：参考图片与多图主体数量之和不得超过4。
-   视频输入场景（omni模型）：支持视频类型主体，最多1个。引用视频类型主体后，不可再传参考图/图片类型主体。

4.0 Omni 模型最多传7个主体，其中视频角色主体最多3个；视频角色主体与输入视频合计不超过5个，视频角色主体的时长计入视频总时长。图片、视频、主体、音色合计不超过15个。主体 ID 仅可来自官方主体库，不支持主体创建接口。

**voice\_list** `array` （可选，适用于4.0模型）

音色列表，最多3个；已绑定音色的主体不占此数量。每项的 `voice_id` 为必填音色 ID，仅可来自[官方音色库](https://help.aliyun.com/zh/model-studio/kling-object-ids#voice-library)，不支持音色定制接口。可在 `prompt` 中通过 `<<<voice_1>>>`、`<<<voice_2>>>` 等标记，按 `voice_list` 顺序引用音色。

**parameters** `object` （可选）

视频生成参数。如设置生成模式、画面比例、视频时长、是否生成音频等。

属性

**mode** `string` （可选）

视频生成模式。

-   `pro`：默认值，专业模式，输出视频分辨率为1080P。
-   `std`：标准模式，输出视频分辨率为720P。
-   `4k`：4K模式，输出视频分辨率为4K（仅适用于支持该模式的3.0模型）。

`kling/kling-v3-turbo-video-generation` 和两个 4.0 模型仅支持 `std`（720P）和 `pro`（1080P），不支持 `4k`；4.0 默认 `pro`。

**aspect\_ratio** `string` （3.0条件必填；4.0可选）

生成视频的宽高比例。

3.0 模型的可选值：

-   `16:9`：默认值。
-   `9:16`
-   `1:1`

3.0 模型的以下场景必须填写：

-   文生视频：必须设置。
-   参考生视频（`type=feature`、`type=feature+refer`、`type=refer`）：必须设置。

3.0 模型其他场景无需设置

-   图生视频-基于首帧：以首帧的宽高比为基准，无需填写。
-   图生视频-基于首尾帧：以首帧的宽高比为基准，无需填写。
-   参考生视频（`type=feature+first_frame`）：以首帧的宽高比为基准，无需填写。
-   视频编辑：以输入视频的宽高比为基准，无需填写。

4.0 模型可选 `21:9`、`16:9`、`9:16`、`1:1`：

-   `kling/kling-v4-video-generation`：文生视频时生效；不传则先按提示词中的比例描述生成，未指明时使用 `16:9`。传入帧图时此参数不生效，比例依次跟随首帧、中间帧首张、尾帧。
-   `kling/kling-v4-omni-reference-video-generation`：可显式指定；不传则先按提示词中的比例描述，未指明时依次跟随待编辑视频、首帧、中间帧首张、尾帧，均无时使用 `16:9`。

**duration** `integer` （可选）

**重要**3.0 模型按生成视频时长计费。4.0 模型按计费时长（秒）计费：无视频输入时等于生成视频时长；有视频输入时等于 max（输入视频总时长，生成视频时长）+ 生成视频时长。具体单价见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#9cb8313752li4)。

生成视频的时长，单位为秒。

-   kling/kling-v3-turbo-video-generation：取值为\[3, 15\]之间的整数，默认值为5。
    
-   kling/kling-v3-video-generation：取值为\[3, 15\]之间的整数，默认值为5。
    
-   kling/kling-v3-omni-video-generation：取值为\[3, 15\]之间的整数，默认值为5。
    
    -   注意：当传入视频时，该参数的行为因`type`不同而异：
        
        -   `type=feature`：取值为\[3, 10\]之间的整数，默认值为5。
        -   `type=base`：输出视频时长与传入视频时长相同，此时当前参数无效。按输入视频时长四舍五入取整计量计费。
-   两个 4.0 模型：取值为3～30之间的整数。不传时先按提示词中的时长描述生成；若未指明，Omni 模型有待编辑视频时跟随该视频时长，否则默认10秒。
    

示例值：5。

**audio** `boolean` （可选）

**重要**3.0 模型的有声选项会影响费用，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看对应型号的价格；4.0 固定生成有声视频。

3.0 模型是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。

-   `false`：默认值，输出无声视频。
-   `true`：输出有声视频。

注意：

-   3.0 Omni 模型传入视频（`type=base或feature`）时，`audio`只能设置为`false`。
-   `kling/kling-v3-turbo-video-generation` 固定生成音画同出视频，该字段不生效（恒为生成）。
-   两个 4.0 模型固定生成有声视频，传入任何 `audio` 值均不生效，不能关闭声音。

**watermark** `boolean` （可选）

是否同时生成含水印的视频。3.0 模型的水印位于视频右下角，文案固定为”可灵AI”。3.0 和 4.0 模型设置为 `true` 时，响应中均额外返回 `watermark_video_url` 字段。

-   `false`：默认值，不生成含水印的视频。
-   `true`：同时生成含水印的视频。

以下原有示例使用3.0模型及其专属参数，不可仅替换模型名称用于4.0。4.0 请参考末尾两个示例，并按上述参数规则选择素材与设置。

#### 文生视频

支持模型：`kling/kling-v3-turbo-video-generation`、`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v3-turbo-video-generation",
    "input": {
        "prompt": "一只小猫在月光下奔跑"
    },
    "parameters": {
        "mode": "std",
        "aspect_ratio": "16:9",
        "duration": 5,
        "audio": false,
        "watermark": true
    }
}'
```

#### Python SDK

```
import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

def sample_async_call():
    # 异步提交视频生成任务
    # mode/aspect_ratio/audio 为 parameters 段字段，不在具名签名内，经 parameters 透传
    try:
        job = client.videos.jobs.create(model='kling/kling-v3-turbo-video-generation',
                                        prompt='一只小猫在月光下奔跑',
                                        duration=5,
                                        watermark=True,
                                        parameters={'mode': 'std',
                                                    'aspect_ratio': '16:9',
                                                    'audio': False})
        print(job)
        print("task_id: %s" % job.task_id)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return

    # 查询任务状态
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # 等待任务完成
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call()
```

#### 文生视频（智能分镜）

支持模型：`kling/kling-v3-turbo-video-generation`、`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v3-video-generation",
    "input": {
        "prompt": "",
        "multi_shot": true,
        "shot_type": "customize",
        "multi_prompt": [
            {
                "index": 1,
                "prompt": "雾岭镇比地图上更小，山雾像棉絮一样堵在街口。邮局背后果然有三棵槐树，第三棵树根旁的泥土被人动过。",
                "duration": 5
            },
            {
                "index": 2,
                "prompt": "林澈蹲下挖出一个铁盒，里面除了一把生锈的钥匙，还有一盘老旧的录音带。录音机是邮局借的，按下播放键时，父亲的声音从沙沙杂音里爬出来：“如果你听到这段话，说明你已经走到我走过的路上了。",
                "duration": 5
            }
        ],
        "media": [],
        "element_list": []
    },
    "parameters": {
        "mode": "pro",
        "duration": 10,
        "audio": true,
        "aspect_ratio": "9:16",
        "watermark": true
    }
}'
```

#### 图生视频（首帧生视频）

支持模型：`kling/kling-v3-turbo-video-generation`、`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v3-omni-video-generation",
    "input": {
        "prompt": "让图片中的人物动起来，头发被微风吹动",
        "media": [
            {
                "type": "first_frame",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
            }
        ]
    },
    "parameters": {
        "mode": "std",
        "duration": 5,
        "audio": false,
        "watermark": true
    }
}'
```

#### 图生视频（首尾帧生视频）

支持模型：`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v3-omni-video-generation",
    "input": {
        "prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
        "media": [
            {
                "type": "first_frame",
                "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"
            },
          {
                "type": "last_frame",
                "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"
            }
        ]
    },
    "parameters": {
        "mode": "std",
        "duration": 5,
        "audio": false,
        "watermark": true
    }
}'
```

#### 参考生视频（视频+图像）

支持模型：`kling/kling-v3-omni-video-generation`。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v3-omni-video-generation",
    "input": {
        "prompt": "<<<element_1>>>背景，<<<image_2>>>和<<<image_1>>>握手交谈，<<<video_1>>>人物穿着黑色风衣的侦探站在公寓楼顶，手持望远镜观察街道",
        "multi_shot": false,
        "shot_type": "intelligence",
        "multi_prompt": [],
        "media": [
            {
                "url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/lip_sync_5s.mp4",
                "type": "base",
                "keep_original_sound": "yes"
            },
            {
                "type": "refer",
                "url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/zem_test/yangmi01.jpg"
            },
            {
                "type": "refer",
                "url": "https://p2-kling.klingai.com/kcdn/cdn-kcdn112452/kling-qa-test/human_2.JPG"
            }
        ],
        "element_list": [
            {
                "element_id": 171
            }
        ]
    },
    "parameters": {
        "mode": "pro",
        "duration": 10,
        "audio": false,
        "aspect_ratio": "1:1",
        "watermark": true
    }
}'
```

#### Kling 4.0 关键帧生视频

支持模型：`kling/kling-v4-video-generation`。以下示例使用首尾帧；也可以仅传中间帧或尾帧。将示例图片 URL 替换为可访问且符合规格的图片地址。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v4-video-generation",
    "input": {
        "prompt": "镜头从近景缓慢拉远，人物站在海边看向远处，头发被海风吹动，海浪声渐强",
        "media": [
            {"type": "first_frame", "url": "https://example.com/first.jpeg"},
            {"type": "last_frame", "url": "https://example.com/last.jpeg"}
        ]
    },
    "parameters": {
        "mode": "pro",
        "duration": 10,
        "watermark": false
    }
}'
```

#### Kling 4.0 全能参考生视频

支持模型：`kling/kling-v4-omni-reference-video-generation`。将视频 URL 和 `element_id` 替换为符合规格、可使用的素材与[主体 ID](raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)。

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "kling/kling-v4-omni-reference-video-generation",
    "input": {
        "prompt": "让<<<element_1>>>模仿<<<video_1>>>中的动作，从画面左侧走向镜头，整体保持电影感夜景氛围",
        "media": [
            {"type": "feature", "url": "https://example.com/reference.mp4"}
        ],
        "element_list": [
            {"element_id": 148}
        ]
    },
    "parameters": {
        "mode": "pro",
        "duration": 10,
        "aspect_ratio": "16:9",
        "watermark": false
    }
}'
```

#### 响应参数

**output** `object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

#### 成功响应

请保存 task\_id，用于查询任务状态与结果。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

#### 异常响应

创建任务失败，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 请求参数

##### 请求头（Headers）

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### URL路径参数（Path parameters）

**task\_id** `string`**（必选）**

任务ID。

#### 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应参数

**output**`object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url**`string`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接有效期30天，但不建议将其作为长期存储依赖，请及时下载。

**watermark\_video\_url**`string`

带水印的视频URL，仅在 task\_status 为 SUCCEEDED 且启用水印时返回。

视频格式为MP4（H.264 编码）。视频链接有效期30天，但不建议将其作为长期存储依赖，请及时下载。

**orig\_prompt** `string`

原始输入的prompt，对应请求参数`prompt`。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计，只对成功的结果计数。

属性

**duration** `number`

计费时长（秒）。无视频输入时等于生成视频时长；3.0 Omni 的 `base` 视频编辑按输入视频时长四舍五入取整计量；4.0 模型有视频输入时等于 max（输入视频总时长，生成视频时长）+ 生成视频时长。

**input\_video\_duration** `number`

4.0 模型的输入视频总时长（秒），保留两位小数，包含特征参考视频、待编辑视频与视频角色主体；无视频输入时为0.00。

**output\_video\_duration** `number`

4.0 模型生成的视频时长（秒），保留两位小数。

**reference\_type** `string`

4.0 模型存在视频输入（特征参考视频、待编辑视频、视频角色主体任一）时返回 `video`；无视频输入时不返回该字段。

**size** `string`

生成视频的分辨率。示例值：1280\*720。

**fps** `integer`

生成视频的帧率。示例值：24。

**SR** `string`

生成视频的分辨率档位。示例值：720。`mode=4k`时返回`4k`；`kling/kling-v3-turbo-video-generation`仅返回`720`或`1080`。

**audio** `boolean`

生成视频是否为有声视频。示例值：false。`kling/kling-v3-turbo-video-generation`和两个 4.0 模型恒为`true`（固定音画同出）。

**video\_count** `integer`

生成视频的数量。固定为1。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

#### 3.0 任务执行成功

```
{
    "request_id": "340f0d7d-bf7e-4c8f-9c03-xxxxxx",
    "output": {
        "task_id": "24f5c51e-d67b-44dc-9acb-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-27 21:30:32.575",
        "scheduled_time": "2026-03-27 21:30:32.603",
        "end_time": "2026-03-27 21:31:09.177",
        "video_url": "https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx",
        "watermark_video_url": "https://v2-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx"
    },
    "usage": {
        "duration": 5,
        "size": "1280*720",
        "fps": 24,
        "video_count": 1,
        "audio": false,
        "SR": "720"
    }
}
```

#### 4.0 任务执行成功

以下示例为传入参考视频的 4.0 Omni 任务。无视频输入时，`input_video_duration` 为0.00，且不返回 `reference_type`。

```
{
    "request_id": "bd547b6a-be36-9a46-857f-xxxxxxxxxxxx",
    "output": {
        "task_id": "6c44c3ee-9c48-462b-8186-xxxxxxxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-11-16 15:53:34.236",
        "scheduled_time": "2026-11-16 15:53:34.309",
        "end_time": "2026-11-16 15:54:20.367",
        "video_url": "https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx",
        "watermark_video_url": "https://v4-fdl.kechuangai.com/ksc2/xxx.mp4?xxxx"
    },
    "usage": {
        "video_count": 1,
        "SR": "720",
        "duration": 7.63,
        "input_video_duration": 4.63,
        "output_video_duration": 3.0,
        "reference_type": "video",
        "size": "940*940",
        "audio": true,
        "fps": 24
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The parameter is invalid xxxxxx"
    }
}
```

#### 任务查询过期

task\_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。

```
{
    "request_id": "a4de7c32-7057-9f82-8581-xxxxxx",
    "output": {
        "task_id": "502a00b1-19d9-4839-a82f-xxxxxx",
        "task_status": "UNKNOWN"
    }
}
```

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
