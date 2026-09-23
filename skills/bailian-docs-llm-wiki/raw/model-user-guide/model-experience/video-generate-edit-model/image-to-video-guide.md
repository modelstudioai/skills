# 万相-图生视频-基于首帧

万相-图生视频模型支持 多模态输入 （文本/图像/音频），可生成最长15秒、分辨率为1080P的视频。

-   **基础设置**：支持整数级视频时长（2～15 秒）、指定视频分辨率（480P/720P/1080P）、智能改写prompt、添加水印。
-   **音频能力**：支持自动配音或上传音频，实现声画同步。**（wan2.5、wan2.6支持）**
-   **多镜头叙事**：可生成包含多个镜头的视频，镜头切换时保持主体一致。**（仅wan2.6支持）**
-   **视频特效**：部分模型内置“魔法悬浮”、“气球膨胀”等模板，可直接使用。

**快速入口：**在线体验（[北京](https://bailian.console.aliyun.com/cn-beijing/model/experience/vision)｜[新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/experience/vision)｜[弗吉尼亚](https://bailian.console.aliyun.com/us-east-1/model/experience/vision)）**｜**[API参考](raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)**｜** [视频特效列表](raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)

## 快速开始

**输入提示词**

**输入首帧图像**

**输出视频（多镜头，有声视频）**

镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。

![wan-i2v-haigui](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4554630771/p1047607.webp)

在调用前，先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。通过SDK进行调用，请[安装DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### Python SDK

**重要**请确保 DashScope Python SDK 版本**不低于**`1.25.8`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

print('please wait...')
rsp = VideoSynthesis.call(api_key=api_key,
                          model='wan2.6-i2v-flash',
                          prompt='镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。',
                          img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp",
                          resolution="720P",
                          duration=10,
                          shot_type="multi",
                          prompt_extend=True,
                          watermark=True)
print(rsp)
if rsp.status_code == HTTPStatus.OK:
    print("video_url:", rsp.output.video_url)
else:
    print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
```

#### Java SDK

**重要**请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Image2Video {

    static {
        // 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。")
                        .imgUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp")
                        .duration(10)
                        .resolution("720P")
                        .shotType("multi")
                        .promptExtend(true)
                        .watermark(true)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
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
    "model": "wan2.6-i2v-flash",
    "input": {
        "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true,
        "duration": 10,
        "shot_type":"multi"
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

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

**说明**本文的示例代码适用于**北京地域**。

## 核心能力

### 制作多镜头视频

**支持模型**：`wan2.6系列模型`。

**功能介绍**：模型可自动进行分镜切换，例如从全景切换到特写，适合制作MV等场景。

**参数设置**：

-   `shot_type`: 必须设为 `"multi"`。
-   `prompt_extend`: 必须设为 `true`（开启智能改写以优化分镜描述）。

**输入提示词**

**输入首帧图像**

**输出视频（wan2.6，多镜头视频）**

一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。

![rap-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5568778571/p1011609.webp)

**输入音频**：

#### Python SDK

> 请确保 DashScope Python SDK 版本不低于 `1.25.8`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='wan2.6-i2v-flash',
                                    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。',
                                    img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                                    audio_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3",
                                    resolution="720P",
                                    duration=10,
                                    shot_type="multi",  # 多镜头
                                    prompt_extend=True,
                                    watermark=True,
                                    negative_prompt="",
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_i2v()
```

#### Java SDK

> 请确保 DashScope Java SDK 版本不低于 `2.22.6`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Image2Video {
    static {
        // 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //设置输入图像url
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";
    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .shotType("multi")
                        .duration(10)
                        .resolution("720P")
                        .negativePrompt("")
                        .promptExtend(true)
                        .watermark(true)
                        .seed(12345)
                        .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-i2v-flash",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "duration": 10,
        "shot_type":"multi"
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 实现声画同步

**支持模型**：`wan2.5和wan2.6系列模型`。

**功能介绍**：让照片中的人物“开口说话”或唱歌，嘴型与音频匹配。更多示例请参见[视频声音生成](https://help.aliyun.com/zh/model-studio/text-to-video-prompt#2cac7fc462so6)。

**参数设置：**

-   **传入音频文件**：传入 `audio_url`。模型会根据音频文件对齐口型。
-   **自动配音**：无需传入 `audio_url`，默认输出有声视频。模型会根据画面自动生成背景音效、音乐或人声。

**输入提示词**

**输入首帧图像**

**输出视频（有声视频）**

一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。

![rap-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5568778571/p1011609.webp)

**输入音频**：

#### Python SDK

> 请确保 DashScope Python SDK 版本不低于 `1.25.8`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='wan2.6-i2v-flash',
                                    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。',
                                    img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                                    audio_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3",
                                    resolution="720P",
                                    duration=10,
                                    prompt_extend=True,
                                    watermark=True,
                                    negative_prompt="",
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_i2v()
```

#### Java SDK

> 请确保 DashScope Java SDK 版本不低于 `2.22.6`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Image2Video {
    static {
        // 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //设置输入图像url
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";
    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .resolution("720P")
                        .negativePrompt("")
                        .promptExtend(true)
                        .watermark(true)
                        .seed(12345)
                        .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**

传入音频文件

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.5-i2v-preview",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
    }
}'
```

自动配音

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.5-i2v-preview",
    "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
    }
}'
```

**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

步骤1：创建任务获取任务ID

#### 自动配音

#### 传入音频文件

Tab 2 正文

步骤2：根据任务ID获取结果

### 生成无声视频

**支持模型**：`wan2.6-i2v-flash`、`wan2.2系列模型`、`wanx2.1系列模型`。

**功能介绍**：适用于无需音频的纯视觉展示场景，如动态海报、无声短视频等。

**参数设置**：

-   `wan2.6-i2v-flash`：默认生成有声视频。若需生成无声视频，必须显式设置 `audio=false`。即使传入 `audio_url`，只要 `audio=false`，输出仍为无声视频，并按[无声视频计费](raw/model-user-guide/get-started-with-models/models.md)。
-   `wan2.2及以下版本模型`：默认生成无声视频，无需额外配置。

**提示词**

**输入首帧图像**

**输出视频（无声视频）**

一只猫在草地上奔跑

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6805468571/p1007038.png)

#### Python SDK

> 请确保 DashScope Python SDK 版本不低于 `1.25.8`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='wan2.6-i2v-flash',
                                    prompt='一只猫在草地上奔跑',
                                    img_url="https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
                                    audio=False,   # 必须显式设置为False，表示输出无声视频
                                    resolution="720P",
                                    duration=5,
                                    prompt_extend=True,
                                    watermark=True,
                                    negative_prompt="",
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_i2v()
```

#### Java SDK

> 请确保 DashScope Java SDK 版本不低于 `2.22.6`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Image2Video {
    static {
        // 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一只猫在草地上奔跑")
                        .imgUrl("https://cdn.translate.alibaba.com/r/wanx-demo-1.png")
                        .audio(false)   /*必须显式设置为false，表示输出无声视频*/
                        .duration(10)
                        .resolution("720P")
                        .negativePrompt("")
                        .promptExtend(true)
                        .watermark(true)
                        .seed(12345)
                        .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**

wan2.6-i2v-flash

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-i2v-flash",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
    },
    "parameters": {
        "audio": false,
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true,
        "duration": 5
    }
}'
```

wan2.2及以下版本模型

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.2-i2v-plus",
    "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true
    }
}'
```

**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 使用视频特效

**支持模型**：`wanx2.1-i2v-turbo`、`wanx2.1-i2v-plus`。

**功能介绍**：无需传入Prompt，直接使用内置的特效模板（如“魔法悬浮”、“气球膨胀”），让静态图片动起来。

**参数设置：**

-   `template`：**必填**，指定特效名称（例如 "flying" 表示魔法悬浮）。调用前请查阅[视频特效列表](raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)，确认模型是否支持，以免调用失败。
-   `prompt`：**忽略**，在使用特效时，prompt 字段无效，建议留空或不传。

**提示词**

**输入首帧图像**

**输出视频（“魔法悬浮”特效）**

无

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6805468571/p1007038.png)

#### Python SDK

> 请确保 DashScope Python SDK 版本不低于 `1.25.8`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call_i2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='wanx2.1-i2v-turbo',
                                    img_url="https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
                                    template="flying",  # 模型特效
                                    resolution="720P",
                                    watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_i2v()
```

#### Java SDK

> 请确保 DashScope Java SDK 版本不低于 `2.22.6`，可参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

```
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Image2Video {
    static {
        // 以下为北京地域URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-i2v-turbo")
                        .imgUrl("https://cdn.translate.alibaba.com/r/wanx-demo-1.png")
                        .template("flying")   /*模型特效*/
                        .resolution("720P")
                        .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

**步骤1：创建任务获取任务ID**
```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-i2v-turbo",
    "input": {
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
        "template": "flying"
    },
    "parameters": {
        "resolution": "720P"
    }
}'
```
**步骤2：根据任务ID获取结果**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 如何传入图像和音频

### 传入图像

-   **图像个数**：1个。
-   **输入方式**：图像URL、本地文件路径、Base64 编码字符串。

方式一：图像URL（HTTP 接口、SDK） 推荐

-   **公网URL**：支持 HTTP 或 HTTPS 协议。
    
    -   示例值：[](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)[https://help-static-aliyun-doc.aliyuncs.com/xxx.png](https://help-static-aliyun-doc.aliyuncs.com/xxx.png)。
-   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
    
    -   示例值：oss://dashscope-instant/xxx/xxx.png。

方式二：本地文件路径（仅限SDK）

不同编程语言（Python/Java）对文件路径的要求略有不同，请严格参照下方规则拼写。

**Python SDK**：支持**绝对路径和相对路径**。文件路径规则如下：

**操作系统**

**传入的文件路径**

**示例（绝对路径）**

**示例（相对路径）**

Linux / macOS

file://{文件的绝对路径或相对路径}

file:///home/images/test.png

file://./images/test.png

Windows

file://D:/images/test.png

file://./images/test.png

**Java SDK**：仅支持**绝对路径**。文件路径规则如下：

**操作系统**

**传入的文件路径**

**示例（绝对路径）**

Linux / macOS

file://{文件的绝对路径}

file:///home/images/test.png

Windows

file:///{文件的绝对路径}

file:///D:/images/test.png

方式三：Base64 编码字符串（HTTP 接口、SDK）

-   **示例值**：`data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......`（示例已截断，仅做演示）**。**
    
-   **格式要求**：遵循 `data:{MIME_type};base64,{base64_data}` 的格式，其中：
    
    -   {base64\_data}：图像文件经过 Base64 编码后的字符串。
        
    -   {MIME\_type}：图像的媒体类型，需与文件格式对应。
        
        **图像格式**
        
        **MIME Type**
        
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
        

##### 示例代码：三种输入方式

Python SDK

```
import base64
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import mimetypes
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# 获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

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

# 【方式一】使用公网可访问的图片URL
# 示例：使用一个公开的图片URL
img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# img_url = "file://" + "/path/to/your/img.png"    # Linux/macOS
# img_url = "file://" + "/C:/path/to/your/img.png"  # Windows
# 示例（相对路径）：
# img_url = "file://" + "./img.png"                # 相对当前执行文件的路径

# 【方式三】使用Base64编码的图片
# img_url = encode_file("./img.png")

# 设置音频audio url
audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

def sample_call_i2v():
    # 同步调用，直接返回结果
    print('please wait...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model='wan2.6-i2v-flash',
                              prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。',
                              img_url=img_url,
                              audio_url=audio_url,
                              resolution="720P",
                              duration=10,
                              prompt_extend=True,
                              watermark=False,
                              negative_prompt="",
                              seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("video_url:", rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_call_i2v()
```

Java SDK

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
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

public class Image2Video {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        // 获取URL：https://help.aliyun.com/zh/model-studio/image-to-video-api-reference
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    //【方式二】本地文件路径（file://+绝对路径）
    // static String imgUrl = "file://" + "/your/path/to/img.png";    // Linux/macOS
    // static String imgUrl = "file://" + "/C:/your/path/to/img.png";  // Windows

    //【方式三】Base64编码
    // static String imgUrl = Image2Video.encodeFile("/your/path/to/img.png");

    // 设置音频audio url
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-i2v-flash")
                        .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
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
        try {
            image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

### 传入音频

-   **音频个数**：1个。
    
-   **输入方式**：
    
    -   **公网 URL**：支持 HTTP 或 HTTPS 协议。
    -   **临时URL**：支持OSS协议，必须通过[上传文件获取临时 URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

## 输出视频

-   **视频个数**：1个。
    
-   **输出视频规格**：不同模型支持的输出规格有所差异，请参见[适用范围](https://help.aliyun.com/zh/model-studio/image-to-video-guide#06f39eafa2dwt)。
    
-   **输出视频URL有效期**：**24小时**。
    
-   **输出视频尺寸**：由输入图像和设置的分辨率`resolution`决定。
    
    -   模型将尽量保持输入图像的宽高比不变，缩放至总像素数接近目标值。因编码规范，长宽必须被16整除，模型会自动微调尺寸。
    -   例如：输入图像750×1000（宽高比 3:4 = 0.75），设置 resolution = "720P"（目标总像素约 92 万）。最终输出可能为 816 × 1104（宽高比 ≈ 0.739，总像素 ≈ 90 万），且长宽均为 16 的倍数。

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#27fb5ee25b6gv)。
    
-   模型限流请参见[万相系列](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入不计费，输出计费。按成功生成的 **视频秒数** 计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
    -   图生视频还支持[节省计划](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

## API文档

[图生视频-基于首帧API参考](raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)

## 常见问题

#### Q: 为什么不能直接设置视频宽高比（如 16:9）？

A：当前 API 不支持直接指定视频宽高比。您只能通过 `resolution` 参数设置视频的分辨率。

`resolution` 控制的是视频的总像素数量，而非固定比例。模型会优先保留输入首帧图像的原始宽高比（近似），并在此基础上进行微调，以满足视频编码要求（即长和宽均需为 16 的整数倍）。

#### Q: 为什么运行SDK代码时出现 “url error, please check url!” 错误？

A：请确保：

-   DashScope Python SDK 版本不低于 `1.25.8`。
-   DashScope Java SDK 版本不低于 `2.22.6`。

若版本过低，可能会触发 “url error, please check url!” 的错误。请参考[升级SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。
