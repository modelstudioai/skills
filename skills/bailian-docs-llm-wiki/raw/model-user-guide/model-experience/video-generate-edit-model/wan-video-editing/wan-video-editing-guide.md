# 视频编辑2.7

万相视频编辑模型支持对输入视频进行内容增删改、背景替换、风格转换、动作/特效/运镜复刻等编辑操作，提供以下两种方式：

-   **指令编辑**：通过文字指令修改视频内容，如替换人物服饰、更改场景元素、调整画面风格等。
-   **指令+参考图编辑**：除指令外，还支持传入参考图像，将图像中的元素（如人物、服饰、道具）应用到视频中。

**说明**视频编辑（尤其是复刻指定视频的动作/运镜/特效）推荐使用**视频编辑 2.7**。若需视频续写能力，推荐使用[万相2.7-图生视频](raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

## 快速开始

**输入提示词和参考图**

**输入视频（特效视频）**

**输出视频**

参考视频的特效，将这个特效应用到图片中的这个长发的女人身上，场景为晚会。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1065994.png)

在调用前，先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。通过SDK进行调用，请[安装DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### Python SDK

**重要**请确保 DashScope Python SDK 版本**不低于**`1.25.16`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
# -*- coding: utf-8 -*-
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。获取URL：https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

media = [
    {
        "type": "video",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/eclvbm/21_refined.mp4"
    },
    {
        "type": "reference_image",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/jgekix/wan2.7-videoedit-demo.webp"
    }
]

def sample_sync_call():
    print('----sync call, please wait a moment----')
    rsp = VideoSynthesis.call(
        api_key=api_key,
        model="wan2.7-videoedit",
        media=media,
        resolution="720P",
        prompt_extend=True,
        watermark=True,
        prompt="参考视频的特效，将这个特效应用到图片中的这个长发的女人身上，场景为晚会。",
    )
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call()
```

#### Java SDK

**重要**请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class VideoEdit {

    static {
        // 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        final String prompt = "参考视频的特效，将这个特效应用到图片中的这个长发的女人身上，场景为晚会。";
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/eclvbm/21_refined.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/jgekix/wan2.7-videoedit-demo.webp")
                    .type("reference_image")
                    .build());
        }};
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt(prompt)
                        .media(media)
                        .resolution("720P")
                        .promptExtend(true)
                        .watermark(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-videoedit",
    "input": {
        "prompt": "参考视频的特效，将这个特效应用到图片中的这个长发的女人身上，场景为晚会。",
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/eclvbm/21_refined.mp4"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/jgekix/wan2.7-videoedit-demo.webp"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**输出示例**

> `video_url` 有效期24小时，请及时下载视频。

```
{
    "request_id": "c1209113-8437-424f-a386-xxxxxx",
    "output": {
        "task_id": "966cebcd-dedc-4962-af88-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
         ...
    },
    ...
}
```

## 适用范围

-   各地域支持的模型有所差异，且资源相互独立。各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。
-   调用时，确保**模型、Endpoint URL 和 API Key 均属于同一地域**，跨地域调用将会失败。

**说明**本文的示例代码适用于**华北2（北京）地域**。

## 核心能力

### 纯指令编辑

**支持模型**：`wan2.7-videoedit`。

**功能介绍**：仅传入视频和文本提示词，通过指令直接修改视频内容。适用于风格转换、动作修改、运镜调整等场景。

**参数设置**：

-   `media`：传入一个待编辑的视频（`type=video`），无需传入参考图像。
-   `prompt`：描述编辑意图，如“视频改为8bit像素风格”。

**输入提示词**

**输入视频**

**输出视频**

视频改为8bit像素风格

#### Python SDK

**重要**请确保 DashScope Python SDK 版本**不低于**`1.25.16`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
# -*- coding: utf-8 -*-
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。获取URL：https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

media = [
    {
        "type": "video",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
    }
]

def sample_sync_call():
    print('----sync call, please wait a moment----')
    rsp = VideoSynthesis.call(
        api_key=api_key,
        model="wan2.7-videoedit",
        media=media,
        resolution="720P",
        prompt_extend=True,
        watermark=True,
        prompt="将整个画面转换为黏土风格",
    )
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call()
```

#### Java SDK

**重要**请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class VideoEdit {

    static {
        // 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        final String prompt = "将整个画面转换为黏土风格";
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4")
                    .type("video")
                    .build());
        }};
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt(prompt)
                        .media(media)
                        .resolution("720P")
                        .promptExtend(true)
                        .watermark(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-videoedit",
    "input": {
        "prompt": "视频改为8bit像素风格",
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260409/rkjvku/1.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 指令+参考图编辑

**支持模型**：`wan2.7-videoedit`。

**功能介绍**：传入视频、文本提示词和参考图像，将参考图中的元素（如服饰、道具等）应用到视频中。

**参数设置**：

-   `media`：传入一个待编辑的视频（`type=video`）和参考图像（`type=reference_image`）。最多支持4张参考图像。
-   `prompt`：描述编辑意图，如“让视频中的马头人身角色穿上图片中的条纹毛衣”。

**输入提示词和参考图**

**输入视频**

**输出视频**

让视频中的马头人身角色穿上图片中的条纹毛衣

![2560154123\_RF-jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1066250.webp)

#### Python SDK

**重要**请确保 DashScope Python SDK 版本**不低于**`1.25.16`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
# -*- coding: utf-8 -*-
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。获取URL：https://help.aliyun.com/zh/model-studio/wan-video-editing-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

media = [
    {
        "type": "video",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
    },
    {
        "type": "reference_image",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"
    }
]

def sample_sync_call():
    print('----sync call, please wait a moment----')
    rsp = VideoSynthesis.call(
        api_key=api_key,
        model="wan2.7-videoedit",
        media=media,
        resolution="720P",
        prompt_extend=True,
        watermark=True,
        prompt="将视频中女孩的衣服替换为图片中的衣服",
    )
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call()
```

#### Java SDK

**重要**请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.List;

public class VideoEdit {

    static {
        // 以下为华北2（北京）地域的URL。调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void syncCall() {
        VideoSynthesis videoSynthesis = new VideoSynthesis();
        final String prompt = "将视频中女孩的衣服替换为图片中的衣服";
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png")
                    .type("reference_image")
                    .build());
        }};
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt(prompt)
                        .media(media)
                        .resolution("720P")
                        .promptExtend(true)
                        .watermark(true)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-videoedit",
    "input": {
        "prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/dozxak/Wan_Video_Edit_33_1.mp4"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260415/hynnff/wan-video-edit-clothes.webp"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 使用场景及效果示例

### 添加/删除/修改元素

对视频内特定元素进行添加、删除或替换。

**类型**

**输入提示词和参考图**

**输入视频**

**输出视频**

添加

杯子里加一块黑色正方形巧克力

删除

将视频中的火车删除，其他保持不变。

修改

将视频中的胶片替换为图片中的盘子

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1065812.png)

修改

让视频中的马男穿上图片中的条纹毛衣

![2560154123\_RF-jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1066250.webp)

修改

把猫换成狗

修改

将画面唱歌的女生替换为一只可爱的拟人猫咪在唱歌，其他保持不变。

### 修改环境或背景

通过指令变换视频的光照条件、季节色彩，修改地理空间，也支持变换视频背景，让物体穿越到任意空间。

**类型**

**输入提示词**

**输入视频**

**输出视频**

修改季节

背景修改季节为白雪皑皑的冬天，树上全是积雪，河流保持不变。

修改天气

人物动作不变，整个场景由现在的阴天改为晴天，其他保持不变

修改光影

其他保持不变，画面整体的光的颜色和滤镜由白色变为暖色调，保持人物肤色细节，使人物与背景统一和谐。

修改背景

主体女人动作不变，将视频背景修改为健身房。

### 修改视频风格

将既有视频快速转化为多种艺术风格，如动画、3D、黏土、毛线等。

**类型**

**输入提示词**

**输入视频**

**输出视频**

修改风格

视频改为图片的C4D卡通风格![2402534429\_RF](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1066256.webp)

修改风格

将整个画面转变为真人电影风格

修改风格

将整个画面转换为水彩画风格

### 修改角色行为/台词/拍摄方式

对已经拍摄或生成的视频内容，通过指令修改剧情内容（如角色行为或台词）和拍摄方法，实现二次创作。

**类型**

**输入提示词**

**输入视频**

**输出视频**

修改角色行为

让视频里的男人盛一勺汤并喝下，其他保持不变。

修改角色情绪

画面中的女孩表情变得悲伤并开始流泪，其他保持不变。

修改角色台词

保持人物音色和语气，将 左边女生的说话内容改为：“Mom, what color is this?”，将右边女生说话内容改为：“It's green, baby”

修改拍摄方式

将相机运镜改为顺时针环绕人物拍摄，人物跟随镜头移动。

修改拍摄方式

将视频运镜改为向上抬高并同时向下俯视。

### 复刻动作/运镜/特效

复刻参考视频的动作序列、运镜轨迹与视觉特效，生成动态特征一致的视频。

**类型**

**输入提示词或参考图**

**输入视频**

**输出视频**

复刻单人动作

让图片中的人物模仿视频中的人的动作。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1065453.png)

复刻多人动作

参考视频五个人物动作，改为五个人在城市街道的路边摊上唱歌弹琴。

复刻运镜

参考原视频运镜方式，镜头快速移动，场景更改为在颁奖典礼上，参考图片中的女人在走红毯。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1065445.png)

复刻特效

参考视频的特效，将这个特效应用到图片中女人身上，场景为街边。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2257046771/p1065444.png)

## 如何输入视频和图像

### 输入视频

-   **视频数量**：必传，有且仅有1个。
    
-   **输入方式**：
    
    -   **公网URL**：支持 HTTP 或 HTTPS 协议。示例：[](https://xxxx/xxx.mp4)[https://xxxx/xxx.mp4](https://xxxx/xxx.mp4)。
    -   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。示例：oss://dashscope-instant/xxx/xxx.mp4。

### 输入参考图像

-   **图像数量**：可选，最多4张。
    
-   **输入方式**：
    
    -   **公网URL**：支持 HTTP 或 HTTPS 协议。示例：[](https://xxxx/xxx.png)[https://xxxx/xxx.png](https://xxxx/xxx.png)。
        
    -   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。示例：oss://dashscope-instant/xxx/xxx.png。
        
    -   **Base64 编码字符串**：示例：data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......（示例已截断，仅做演示）**。**
        
        -   格式：`data:{MIME_type};base64,{base64_data}` ，其中：
            
            -   {base64\_data}：图像文件经过 Base64 编码后的字符串。
            -   {MIME\_type}：图像的媒体类型，需与文件格式对应。
            
            图像格式
            
            MIME Type
            
            JPEG
            
            image/jpeg
            
            JPG
            
            image/jpeg
            
            PNG
            
            image/png
            
            BMP
            
            image/bmp
            
            WEBP
            
            image/webp
            
            示例代码
            
            ```
            import base64
            import mimetypes
            
            # 格式为 data:{MIME_type};base64,{base64_data}
            def encode_file(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type or not mime_type.startswith("image/"):
                    raise ValueError("不支持或无法识别的图像格式")
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:{mime_type};base64,{encoded_string}"
            
            # 将 your_image.jpg 替换为真实的图像路径
            base64_str = encode_file("your_image.jpg")
            print(base64_str)
            ```
            

## 输出视频

-   **视频数量**：1个。
-   **视频规格**：格式为MP4。具体请参见[视频规格范围](https://help.aliyun.com/zh/model-studio/wan-video-editing-guide#ve01scopeh)。
-   **视频URL有效期**：**24小时**。
-   **视频尺寸**：由[参数resolution](raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)指定视频分辨率，[参数ratio](raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)指定视频宽高比。

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#5c3d28ad8a4x8)。
    
-   模型限流请参见[万相系列](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入图像不计费，输入视频和输出视频计费，按视频秒数计费。即：`总计费时长（秒）= 输入视频时长（秒）+ 输出视频时长（秒）`。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。

## API文档

[万相2.7-视频编辑](raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)

## 常见问题

#### Q：视频编辑2.7（wan2.7-videoedit）与视频编辑2.1（wanx2.1-vace-plus）有什么区别？

A：视频编辑2.7通过指令直接编辑视频，使用简单，能力全面升级。[视频编辑2.1](raw/model-user-guide/model-experience/video-generate-edit-model/wan-video-editing/wan-vace-guide.md)需指定`function`参数，侧重掩码局部编辑、画面扩展等功能。推荐优先选用**视频编辑 2.7**。

#### Q：如何传入多张参考图像？

A：在`media`数组中添加多个`type=reference_image`的对象即可，最多4张。示例：

```
{
    "media": [
        {"type": "video", "url": "<输入视频URL>"},
        {"type": "reference_image", "url": "<参考图1 URL>"},
        {"type": "reference_image", "url": "<参考图2 URL>"},
        {"type": "reference_image", "url": "<参考图3 URL>"},
        {"type": "reference_image", "url": "<参考图4 URL>"}
    ]
}
```
