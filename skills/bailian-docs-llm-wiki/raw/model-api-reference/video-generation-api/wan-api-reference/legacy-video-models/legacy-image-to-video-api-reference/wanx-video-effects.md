# 万相-图生视频-视频特效列表

万相提供视频特效功能， 无需输入提示词，只需指定特效模板 ，即可轻松生成预设的动态效果。

视频特效列表仅支持在“[图生视频-基于首帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)”和“[图生视频-基于首尾帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)”中使用。

## 使用方法

视频特效与图生视频的使用方式不同，请遵循以下规则：

-   **仅需一张首帧图像**：无论选用的是“基于首帧”还是“基于首尾帧”的模型，**只需要提供一张首帧图像**。
-   **无需任何提示词**：在特效模式下，模型会忽略 prompt 字段。建议不传入该参数，专注于选择视觉效果。
-   **选择一个模板**：通过 `template` 参数从特效列表中选择一个动态效果。模型将根据模板生成指定的动态效果。

**说明**不同的模型支持的特效模板有所不同。请务必参考[特效列表-首帧生视频](https://help.aliyun.com/zh/model-studio/wanx-video-effects#89f64eb5a812c)和[特效列表-首尾帧生视频](https://help.aliyun.com/zh/model-studio/wanx-video-effects#6e5be7aaa1rc2)，确保所使用的 template 值与模型匹配。

**图生视频-基于首帧**

**输入首帧**

**输入提示词**

**输入template**

**输出视频**

![wanx-demo-1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0458180571/p976602.png)

无需传入

flying

> 使用“魔法悬浮”特效

**图生视频-基于首尾帧**

**输入首帧**

**输入尾帧**

**输入提示词**

**输入template**

**输出视频**

![首尾帧生视频-视频特效-demo](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8150385571/p1000087.png)

无需传入

无需传入

hanfu-1

> 使用“唐韵翩然”特效

**示例代码**

#### 图生视频-基于首帧

**首帧特效**：对首帧图像生成特效视频。

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

> 完整代码请参见[图生视频-基于首帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)。

#### Python SDK

```
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call():
    # 异步提交视频生成任务
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                model='wanx2.1-i2v-turbo',
                                img_url='https://cdn.translate.alibaba.com/r/wanx-demo-1.png',
                                template='flying',
                                resolution='720P')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 查询任务状态
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 等待任务完成
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call()
```

#### 图生视频-基于首尾帧

**首尾帧特效**：只需提供一张首帧图像，无需尾帧图像，即可生成视频特效。

-   若同时提供first\_frame\_url、last\_frame\_url、template，将忽略last\_frame\_url。
-   若仅提供last\_frame\_url、template，请求将报错。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-kf2v-plus",
    "input": {
        "first_frame_url": "https://ty-yuanfang.oss-cn-hangzhou.aliyuncs.com/lizhengjia.lzj/tmp/11.png",
        "template": "hanfu-1"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
    }
}'
```

> 完整代码请参见[图生视频-基于首尾帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

## 特效列表-首帧生视频

视频特效的使用方式请参见[使用方法](https://help.aliyun.com/zh/model-studio/wanx-video-effects#17153ae3a3x2r)。

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其“输入图像建议”，再使用您自己的图片进行尝试。

### 通用特效

**特效名称**

**template参数值**

**示例效果**

**支持模型**

**输入图像建议**

解压捏捏

**squish**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

转圈圈

**rotation**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

戳戳乐

**poke**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

气球膨胀

**inflate**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

分子扩散

**dissolve**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

热浪融化

**melt**

wanx2.1-i2v-plus

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

冰淇淋星球

**icecream**

wanx2.1-i2v-plus

-   支持任意主体
-   建议使用主体突出，与背景有明显区分度的图片

### 单人特效

**特效名称**

**template参数值**

**示例效果**

**支持模型**

**输入图像建议**

时光木马

**carousel**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持单人照片
-   建议使用半身至全身的正面照片

爱你哟

**singleheart**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持单人照片
-   建议使用半身至全身的正面照片

摇摆时刻

**dance1**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

头号甩舞

**dance2**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用全身正面照片

星摇时刻

**dance3**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用全身正面照片

指感节奏

**dance4**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

舞动开关

**dance5**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

人鱼觉醒

**mermaid**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身的正面照片

学术加冕

**graduation**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

巨兽追袭

**dragon**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

财从天降

**money**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

水母之约

**jellyfish**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

瞳孔穿越

**pupil**

wanx2.1-i2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

### 单人或动物特效

**特效名称**

**template参数值**

**示例效果**

**支持模型**

**输入图像建议**

魔法悬浮

**flying**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持单人或动物照片
-   建议使用全身的正面照片

赠人玫瑰

**rose**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持单人或动物照片
-   建议使用半身至全身的正面照片，避免露出手部

闪亮玫瑰

**crystalrose**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持单人或动物照片
-   建议使用半身至全身的正面照片，避免露出手部

### 双人特效

**特效名称**

**template参数值**

**示例效果**

**支持模型**

**输入图像建议**

爱的抱抱

**hug**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持双人照片
-   建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照

唇齿相依

**frenchkiss**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持双人照片
-   建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照

双倍心动

**coupleheart**

wanx2.1-i2v-plus

wanx2.1-i2v-turbo

-   支持双人照片
-   建议两人正面看向镜头或相对站立 （面对面），可为半身或全身照

## 特效列表-首尾帧生视频

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其“输入图像建议”，再使用您自己的图片进行尝试。

**说明**首尾帧生视频的特效是基于首尾帧模型训练，但实际使用时**仅需传入首帧图像**，无需提供尾帧，效果等同于首帧生成视频。具体请参见[使用方法](https://help.aliyun.com/zh/model-studio/wanx-video-effects#17153ae3a3x2r)。

### 单人特效

**特效名称**

**template参数值**

**示例效果**

**支持模型**

**输入图像建议**

唐韵翩然

**hanfu-1**

wanx2.1-kf2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

机甲变身

**solaron**

wanx2.1-kf2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

闪耀封面

**magazine**

wanx2.1-kf2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

机械觉醒

**mech1**

wanx2.1-kf2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

赛博登场

**mech2**

wanx2.1-kf2v-plus

-   支持单人照片
-   建议使用半身至全身的正面照片

## API参考

-   API参数说明和完整代码示例，请参见[图生视频-基于首帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)、[图生视频-基于首尾帧](raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

、
