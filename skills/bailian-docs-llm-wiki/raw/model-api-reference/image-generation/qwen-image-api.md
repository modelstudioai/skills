# 千问-文生图API参考

千问-文生图模型（Qwen-Image）是一款通用图像生成模型，支持多种艺术风格，尤其擅长**复杂文本渲染**。模型支持多行布局、段落级文本生成以及细粒度细节刻画，可实现复杂的图文混合布局设计。

**快速入口：**[使用指南](https://help.aliyun.com/zh/model-studio/text-to-image) **|** 在线体验（[北京](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=qwen-image-max) | [新加坡](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/vision?currentTab=imageGenerate&modelId=qwen-image-max)） **|** [技术博客](https://qwen.ai/blog?id=9467b4bff9c638e847f08443802c6b96ab116a87&from=research.research-list)

## **效果展示**

**输入提示词**

**输出图像**

冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。

![image (10)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9373463771/p1058343.png)

## 模型概览

**模型名称**

**模型简介**

**输出图像规格**

qwen-image-2.0-pro `**推荐**`

> 当前与qwen-image-2.0-pro-2026-04-22能力相同

千问图像生成与编辑模型Pro系列。文字渲染、真实质感、语义遵循能力更强。

> 图像编辑请参考[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)。

图像分辨率：支持自由设置宽高，输出图像总像素需在512\*512至2048\*2048之间。默认分辨率为2048\*2048。

图像格式：png

图像张数：1-6张

qwen-image-2.0-pro-2026-04-22 `**推荐**`

qwen-image-2.0-pro-2026-03-03

qwen-image-2.0 `**推荐**`

> 当前与qwen-image-2.0-2026-03-03能力相同

千问图像生成与编辑模型加速版，兼顾效果与响应速度。

> 图像编辑请参考[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)。

qwen-image-2.0-2026-03-03 `**推荐**`

qwen-image-max

> 当前与qwen-image-max-2025-12-30能力相同

千问图像生成模型Max系列。真实感、自然度更强，AI合成痕迹更低。

图像分辨率：可选分辨率及对应宽高比例请参见[size参数设置](#1c7b41f2d13sv)

图像格式：png

图像张数：固定1张

qwen-image-max-2025-12-30

qwen-image-plus

> 当前与qwen-image能力相同

千问图像生成模型Plus系列，擅长多样化艺术风格与文字渲染。

qwen-image-plus-2026-01-09

qwen-image

各地域支持的模型请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

## 前提条件

在调用前，先[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

**重要**

北京和新加坡地域拥有独立的 **API Key** 与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

## **同步接口（推荐）**

### **HTTP调用**

千问图像模型支持同步接口，一次请求即可获得结果，调用流程简单，推荐用于多数场景。

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

#### 请求参数

## **文生图**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "qwen-image-2.0-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "negative_prompt": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        "prompt_extend": true,
        "watermark": false,
        "size": "2048*2048"
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。示例值：`qwen-image-2.0-pro`。

**input** `_object_` **（必选）**

输入的基本信息。

**属性**

**messages** `_array_` **（必选）**

请求内容数组。**当前仅支持单轮对话**，数组内**有且只有一个元素**。

**属性**

**role** `_string_` **（必选）**

消息的角色。此参数必须设置为`user`。

**content** `_array_` **（必选）**

消息内容数组。

**属性**

**text** `_string_` **（必选）**

正向提示词用于描述您期望生成的图像内容、风格和构图。

支持中英文，qwen-image-2.0系列模型长度上限为 1300 Token，其他模型为 800 Token，超出部分将自动截断。

**注意**：仅支持传入一个text，不传或传入多个将报错。

**parameters** `_object_` （可选）

图像处理参数。

**属性**

**negative\_prompt** `_string_` （可选）

反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。

支持中英文，长度不超过500个字符，超出部分将自动截断。

示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。

**size** `_string_` （可选）

输出图像的分辨率，格式为`宽*高`。

**qwen-image-2.0系列模型**：输出图像总像素需在`512*512`至`2048*2048`之间，默认分辨率为`2048*2048`。推荐分辨率：

-   `2688*1536` ：16:9
    
-   `1536*2688` ：9:16
    
-   `2048*2048`（**默认值）**：1:1
    
-   `2368*1728` ：4:3
    
-   `1728*2368` ：3:4
    

**qwen-image-max、qwen-image-plus系列模型**：默认分辨率为`1664*928`。**可选**的分辨率及其对应的图像宽高比例为：

-   `1664*928`（**默认值**）：16:9
    
-   `1472*1104`：4:3
    
-   `1328*1328`：1:1
    
-   `1104*1472`：3:4
    
-   `928*1664`：9:16
    

**n** `_integer_` （可选）

输出图像的数量，默认值为1。

对于qwen-image-2.0系列模型，可选择输出1-6张图片。

对于qwen-image-max、qwen-image-plus系列模型，此参数固定为1，设置其他值将导致报错。

**prompt\_extend** `_bool_` （可选）

是否开启 Prompt（提示词）智能改写功能。开启后模型将对正向提示词进行优化与润色。此功能不会修改反向提示词。

-   `true`：**默认值**，开启智能改写。如果希望图像内容更多样化，由模型补充细节，建议开启此选项。
    
-   `false`：关闭智能改写。如果图像细节更可控，建议关闭此选项，并参考[文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt)进行优化，
    

点击查看改写示例

> 当前仅异步接口返回实际提示词。

**原始提示词（orig\_prompt）**：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**实际提示词（actual\_prompt）**：一只坐着的橘黄色猫咪，毛发蓬松柔软，阳光透过窗户洒在它身上，呈现出温暖的光泽。猫咪体型匀称，四肢自然弯曲，稳稳地坐在木质地板上，尾巴轻轻卷曲在身侧，显得格外放松而优雅。它的大眼睛圆润明亮，瞳孔微微收缩，流露出愉悦而灵动的神情，嘴角微扬，仿佛正享受着美好的时光。耳朵微微向前倾斜，透露出活泼与好奇。背景是一间温馨的现代家居客厅，浅色木地板、一扇半开的窗户透进柔和的自然光，窗外可见绿意盎然的庭院，窗台上摆放着几盆绿植。画面采用真实摄影风格，细节逼真，光影层次丰富，突出猫咪的毛发质感、眼神神态与整体姿态的生动自然，整体氛围轻松愉快，充满生活气息。

**watermark** `_bool_` （可选）

是否在图像右下角添加 "Qwen-Image" 水印。默认值为 `false`。水印样式：![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8972029571/p1012089.jpg)

**seed** `_integer_` （可选）

随机数种子，取值范围`[0,2147483647]`。

使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。

**注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。

#### 响应参数

## 任务执行成功

图像URL仅保留24小时，超时后会被自动清除，请及时保存生成的图像。

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": [
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "height": 2048,
        "image_count": 1,
        "width": 2048
    },
    "request_id": "d0250a3d-b07f-49e1-bdc8-6793f4929xxx"
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "a4d78a5f-655f-9639-8437-xxxxxx",
    "code": "InvalidParameter",
    "message": "num_images_per_prompt must be 1"
}
```

**output** `_object_`

任务输出信息。

**属性**

**choices** `_array_`

模型生成的输出内容。此数组仅包含一个元素。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**image** `_string_`

生成图像的 URL，图像格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。

**task\_metric** `_object_`

任务结果统计。使用qwen-image-2.0系列时无此返回值。

**属性**

**TOTAL** `_integer_`

总的任务数。

**SUCCEEDED** `_integer_`

任务状态为成功的任务数。

**FAILED** `_integer_`

任务状态为失败的任务数。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

模型生成图像的数量，当前固定为1。

**width** `_integer_`

模型生成图像的宽度（像素）。

**height** `_integer_`

模型生成图像的高度（像素）。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

* * *

### **DashScope SDK调用**

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据语言特性进行封装。同步调用参数说明可参考[HTTP调用](#90575c8228nmq)。

## Python

**说明**

请先确认已安装最新版DashScope Python SDK，否则可能运行报错：[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

##### **请求示例**

```
import json
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

messages = [
    {
        "role": "user",
        "content": [
            {"text": "冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。"}
        ]
    }
]

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

response = MultiModalConversation.call(
    api_key=api_key,
    model="qwen-image-2.0-pro",
    messages=messages,
    result_format='message',
    stream=False,
    watermark=False,
    prompt_extend=True,
    negative_prompt="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
    size='2048*2048'
)

if response.status_code == 200:
    print(json.dumps(response, ensure_ascii=False))
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

##### **响应示例**

> 图像链接的有效期为24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "d2d1a8c0-325f-9b9d-8b90-xxxxxx",
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
                    "content": [
                        {
                            "image": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "width": 2048,
        "image_count": 1,
        "height": 2048
    }
}
```

## Java

**说明**

请先确认已安装最新版DashScope Java SDK，否则可能运行报错：[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

##### **请求示例**

```
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class QwenImage {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：static String apiKey ="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

        MultiModalConversation conv = new MultiModalConversation();

        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "冬日北京的都市街景，青灰瓦顶、朱红色外墙的两间相邻中式商铺比肩而立，檐下悬挂印有剪纸马的暖光灯笼，在阴天漫射光中投下柔和光晕，映照湿润鹅卵石路面泛起细腻反光。左侧为书法店：靛蓝色老旧的牌匾上以遒劲行书刻着“文字渲染”。店门口的玻璃上挂着一幅字，自上而下，用田英章硬笔写着“专业幻灯片 中英文海报 高级信息图”，落款印章为“1k token”朱砂印。店内的墙上，可以模糊的辨认有三幅竖排的书法作品，第一幅写着“阿里巴巴”，第二幅写着“通义千问”，第三幅写着“图像生成”。一位白发苍苍的老人背对着镜头观赏。右侧为花店，牌匾上以鲜花做成文字“真实质感”；店内多层花架陈列红玫瑰、粉洋牡丹和绿植，门上贴了一个圆形花边标识，标识上写着“2k resolution”，门口摆放了一个彩色霓虹灯，上面写着“细腻刻画 人物 自然 建筑”。两家店中间堆放了一个雪人，举了一老式小黑板，上面用粉笔字写着“Qwen-Image-2.0 正式发布”。街道左侧，年轻情侣依偎在一起，女孩是瘦脸，身穿米白色羊绒大衣，肉色光腿神器。女孩举着心形透明气球，气球印有白色的字：“生图编辑二合一”。里面有一个毛茸茸的卡皮巴拉玩偶。男孩身着剪裁合体的深灰色呢子外套，内搭浅色高领毛衣。街道右侧，一个后背上写着“更小模型，更快速度”的骑手疾驰而过。整条街光影交织、动静相宜。")
                )).build();

        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", false);
        parameters.put("prompt_extend", true);
        parameters.put("negative_prompt", "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。");
        parameters.put("size", "2048*2048");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(apiKey)
                .model("qwen-image-2.0-pro")
                .messages(Collections.singletonList(userMessage))
                .parameters(parameters)
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

##### **响应示例**

> 图像链接的有效期为24小时，请及时下载图像。

```
{
    "requestId": "5b6f2d04-b019-40db-a5cc-xxxxxx",
    "usage": {
        "image_count": 1,
        "width": 2048,
        "height": 2048
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png?Expires=xxx"
                        }
                    ]
                }
            }
        ]
    }
}
```

## **异步接口**

**重要**

当前仅qwen-image-plus、qwen-image模型支持异步接口调用。

### **HTTP调用**

调用流程分为两步：

1.  **创建任务获取任务ID**：发送一个请求创建任务，该请求会返回**任务ID（task\_id）**。
    
2.  **根据任务ID查询结果**：使用task\_id轮询任务状态，直到任务完成并获得图像URL。
    

#### **步骤1：创建任务获取任务ID**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

**新加坡地域**：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

##### **请求参数**

## 文生图

当前仅`qwen-image-plus`、`qwen-image`模型支持异步接口调用。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "qwen-image-plus",
    "input": {
        "prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。"
    },
    "parameters": {
        "negative_prompt":" ",
        "size": "1664*928",
        "n": 1,
        "prompt_extend": true,
        "watermark": false
    }
}'
```

###### **请求头（Headers）**

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

###### **请求体（Request Body）**

**model** `_string_` **（必选）**

模型名称。当前仅`qwen-image-plus`、`qwen-image`模型支持异步接口调用。

示例值：`qwen-image-plus`。

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` **（必选）**

正向提示词，用来描述生成图像中期望包含的元素和视觉特点。

支持中英文，长度不超过800个字符，每个汉字、字母、数字或符号计为一个字符，超出部分将自动截断。

示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**negative\_prompt** `_string_` （可选）

反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。

支持中英文，长度不超过500个字符，超出部分将自动截断。

示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。

**parameters** `_object_` （可选）

图像处理参数。

**属性**

**size** `_string_` （可选）

输出图像的分辨率，格式为`宽*高`。

**qwen-image-2.0系列模型**：输出图像总像素需在`512*512`至`2048*2048`之间，默认分辨率为`2048*2048`。推荐分辨率：

-   `2688*1536` ：16:9
    
-   `1536*2688` ：9:16
    
-   `2048*2048`（**默认值）**：1:1
    
-   `2368*1728` ：4:3
    
-   `1728*2368` ：3:4
    

**qwen-image-max、qwen-image-plus系列模型**：默认分辨率为`1664*928`。**可选**的分辨率及其对应的图像宽高比例为：

-   `1664*928`（**默认值**）：16:9
    
-   `1472*1104`：4:3
    
-   `1328*1328`：1:1
    
-   `1104*1472`：3:4
    
-   `928*1664`：9:16
    

**n** `_integer_` （可选）

生成图像的数量。**此参数当前固定为1，设置其他值将导致报错。**

**prompt\_extend** `_bool_` （可选）

是否开启 Prompt（提示词）智能改写功能。开启后模型将对正向提示词进行优化与润色。此功能不会修改反向提示词。

-   `true`：**默认值**，开启智能改写。如果希望图像内容更多样化，由模型补充细节，建议开启此选项。
    
-   `false`：关闭智能改写。如果图像细节更可控，建议关闭此选项，并参考[文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt)进行优化，
    

点击查看改写示例

> 当前仅异步接口返回实际提示词。

**原始提示词（orig\_prompt）**：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**实际提示词（actual\_prompt）**：一只坐着的橘黄色猫咪，毛发蓬松柔软，阳光透过窗户洒在它身上，呈现出温暖的光泽。猫咪体型匀称，四肢自然弯曲，稳稳地坐在木质地板上，尾巴轻轻卷曲在身侧，显得格外放松而优雅。它的大眼睛圆润明亮，瞳孔微微收缩，流露出愉悦而灵动的神情，嘴角微扬，仿佛正享受着美好的时光。耳朵微微向前倾斜，透露出活泼与好奇。背景是一间温馨的现代家居客厅，浅色木地板、一扇半开的窗户透进柔和的自然光，窗外可见绿意盎然的庭院，窗台上摆放着几盆绿植。画面采用真实摄影风格，细节逼真，光影层次丰富，突出猫咪的毛发质感、眼神神态与整体姿态的生动自然，整体氛围轻松愉快，充满生活气息。

**watermark** `_bool_` （可选）

是否在图像右下角添加 "Qwen-Image" 水印。默认值为 `false`。水印样式：![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8972029571/p1012089.jpg)

**seed** `_integer_` （可选）

随机数种子，取值范围`[0,2147483647]`。

使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。

**注意**：模型生成过程具有概率性，即使使用相同的`seed`，也不能保证每次生成结果完全一致。

##### **响应参数**

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

创建任务失败，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

#### **步骤2：根据任务ID查询结果**

##### **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

##### 新加坡

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：图像生成过程耗时较长，建议采用**轮询**机制，并设置合理的查询间隔（如 10 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回图像链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

##### **请求参数**

## 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

###### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

###### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

##### **响应参数**

## 任务执行成功

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。

```
{
    "request_id": "cf4a3304-fa4d-97b6-bc72-xxxxxx",
    "output": {
        "task_id": "18e7cde0-8c17-42aa-afc5-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-05 11:33:20.542",
        "scheduled_time": "2025-09-05 11:33:20.581",
        "end_time": "2025-09-05 11:33:40.807",
        "results": [
            {
                "orig_prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。",
                "actual_prompt": "一副典雅庄重的对联悬挂于中式厅堂之中，对联左侧书写“义本生知人机同道善思新”，右侧书写“通云赋智乾坤启数高志远”，横批为“智启千问”，字体为飘逸洒脱的书法体，墨色浓淡相宜，展现出浓厚的文化气息与艺术美感。对联中央悬挂一幅中国风画作，描绘的是著名的岳阳楼景观，楼阁飞檐翘角，依水而建，远处山水氤氲，云雾缭绕，展现出古典诗意之美。\n\n整个画面背景为一个安静、布置典雅的中式房间，室内木质结构古朴，光线柔和，营造出宁静庄重的氛围。对联悬挂于房间正中墙面，下方为一长案几，案上摆放数件青花瓷器，器型古雅，纹饰精美，蓝白相间，与整体环境和谐统一。整体画面风格为中国水墨风，线条流畅，色彩淡雅，富有传统美学韵味。",
                "url": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/7d/xxx.png?Expires=xxxx"
            }
        ]
    },
    "usage": {
        "image_count": 1
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "c61fe158-c0de-40f0-b4d9-964625119ba4",
    "output": {
        "task_id": "86ecf553-d340-4e21-xxxxxxxxx",
        "task_status": "FAILED",
        "submit_time": "2025-11-11 11:46:28.116",
        "scheduled_time": "2025-11-11 11:46:28.154",
        "end_time": "2025-11-11 11:46:28.255",
        "code": "InvalidParameter",
        "message": "xxxxxxxx"
    }
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results** `_array_`

任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。

**属性**

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**actual\_prompt** `_string_`

开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。

**url** `_string_`

模型生成图像的URL地址。有效期为24小时，请及时下载并保存图像。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

模型生成图像的数量，当前固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

### **DashScope SDK调用**

DashScope SDK目前已支持[Python](#a3ad9a3b6d9if)和[Java](#589b80853e6rn)。

SDK与HTTP接口的参数名基本一致，参数结构根据不同语言的SDK封装而定。异步调用参数说明可参考[HTTP调用](#42703589880ts)。

由于图像模型处理时间较长，底层服务采用异步方式。SDK在此基础上封装了两种调用模式：

-   **同步调用（阻塞模式）**： SDK会自动等待任务完成，然后直接返回最终结果，调用体验与常规同步调用一致。
    
-   **异步调用（非阻塞模式）**： 调用后将立即返回任务ID，需要用户根据该ID自行查询任务状态和最终结果。
    

#### **Python SDK调用**

**说明**

请先确认已安装最新版DashScope Python SDK，否则可能运行报错：[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## 同步调用

##### **请求示例**

```
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

prompt = "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。"

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")

print('----同步调用，请等待任务执行----')
rsp = ImageSynthesis.call(api_key=api_key,
                          model="qwen-image-plus", # 当前仅qwen-image-plus、qwen-image模型支持异步接口
                          prompt=prompt,
                          negative_prompt=" ",
                          n=1,
                          size='1664*928',
                          prompt_extend=True,
                          watermark=False)
print(f'response: {rsp}')
if rsp.status_code == HTTPStatus.OK:
    # 在当前目录下保存图像
    for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)
else:
    print(f'同步调用失败, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "03b1ef03-480d-4ea5-ba52-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "3cefd9bc-fcb2-4de9-a8bc-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxxxxx",
                "orig_prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。",
                "actual_prompt": "一副典雅庄重的对联悬挂于中式厅堂正中，整体空间为安静、古色古香的中国传统布置。厅堂内木质家具沉稳大气，墙面为淡色仿古纸张质感，地面铺设深色木质地板，营造出宁静而庄重的氛围。对联以飘逸的书法字体书写，左侧上联为“义本生知人机同道善思新”，右侧下联为“通云赋智乾坤启数高志远”，横批“智启千问”，文字排列对称，墨色深邃，书法流畅有力，体现出浓厚的文化气息与哲思内涵。\n\n对联中央悬挂一幅中国风画作，内容为岳阳楼，楼阁依水而建，背景为浩渺洞庭湖，远处山峦起伏，云雾缭绕，画面采用传统水墨技法绘制，笔触细腻，意境悠远。画作下方为一张中式红木长桌，桌上错落摆放着几件青花瓷器，包括花瓶与茶具，瓷器釉色清透，纹饰典雅，与整体环境风格和谐统一。整体画面风格为中国古典水墨风，空间布局层次分明，氛围宁静雅致，展现出浓厚的东方文化底蕴。"
            }
        ],
        "submit_time": "2025-09-09 13:41:54.041",
        "scheduled_time": "2025-09-09 13:41:54.087",
        "end_time": "2025-09-09 13:42:22.596"
    },
    "usage": {
        "image_count": 1
    }
}
```

## 异步调用

##### 请求示例

```
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os
import dashscope
import time

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

prompt = "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def async_call():
    print('----创建任务----')
    task_info = create_async_task()
    print('----轮询任务状态----')
    poll_task_status(task_info)

# 创建异步任务
def create_async_task():
    rsp = ImageSynthesis.async_call(api_key=api_key,
                                    model="qwen-image-plus", # 当前仅qwen-image-plus、qwen-image模型支持异步接口
                                    prompt=prompt,
                                    negative_prompt=" ",
                                    n=1,
                                    size='1664*928',
                                    prompt_extend=True,
                                    watermark=False)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
    else:
        print(f'创建任务失败, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')
    return rsp

# 轮询异步任务状态，每5秒查询一次，最多轮询1分钟
def poll_task_status(task):
    start_time = time.time()
    timeout = 60  # 1分钟超时
    
    while True:
        # 检查是否超时
        if time.time() - start_time > timeout:
            print('轮询超时（1分钟），任务未完成')
            return
            
        # 获取任务状态
        status_rsp = ImageSynthesis.fetch(task)
        print(f'任务状态查询结果: {status_rsp}')
        
        if status_rsp.status_code != HTTPStatus.OK:
            print(f'获取任务状态失败, status_code: {status_rsp.status_code}, code: {status_rsp.code}, message: {status_rsp.message}')
            return
        task_status = status_rsp.output.task_status
        print(f'当前任务状态: {task_status}')
        
        if task_status == 'SUCCEEDED':
            print('任务已完成，正在下载图像...')
            for result in status_rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open(f'./{file_name}', 'wb+') as f:
                    f.write(requests.get(result.url).content)
                print(f'图像已保存为: {file_name}')
            break
        elif task_status == 'FAILED':
            print(f'任务执行失败, status: {task_status}, code: {status_rsp.code}, message: {status_rsp.message}')
            break
        elif task_status == 'PENDING' or task_status == 'RUNNING':
            print('任务正在进行中，5秒后继续查询...')
            time.sleep(5)
        elif task_status == 'CANCELED':
            print('任务已被取消。')
            break
        else:
            print(f'未知任务状态: {task_status}，5秒后继续查询...')
            time.sleep(5)

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    rsp = ImageSynthesis.cancel(task)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.task_status)
    else:
        print(f'取消任务失败, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')

if __name__ == '__main__':
    async_call()
```

##### **响应示例**

1、创建任务的响应示例

```
{
	"status_code": 200,
	"request_id": "31b04171-011c-96bd-ac00-xxxxxx",
	"code": "",
	"message": "",
	"output": {
		"task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
		"task_status": "PENDING",
		"results": []
	},
	"usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "03b1ef03-480d-4ea5-ba52-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "3cefd9bc-fcb2-4de9-a8bc-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxxxxx",
                "orig_prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。",
                "actual_prompt": "一副典雅庄重的对联悬挂于中式厅堂正中，整体空间为安静、古色古香的中国传统布置。厅堂内木质家具沉稳大气，墙面为淡色仿古纸张质感，地面铺设深色木质地板，营造出宁静而庄重的氛围。对联以飘逸的书法字体书写，左侧上联为“义本生知人机同道善思新”，右侧下联为“通云赋智乾坤启数高志远”，横批“智启千问”，文字排列对称，墨色深邃，书法流畅有力，体现出浓厚的文化气息与哲思内涵。\n\n对联中央悬挂一幅中国风画作，内容为岳阳楼，楼阁依水而建，背景为浩渺洞庭湖，远处山峦起伏，云雾缭绕，画面采用传统水墨技法绘制，笔触细腻，意境悠远。画作下方为一张中式红木长桌，桌上错落摆放着几件青花瓷器，包括花瓶与茶具，瓷器釉色清透，纹饰典雅，与整体环境风格和谐统一。整体画面风格为中国古典水墨风，空间布局层次分明，氛围宁静雅致，展现出浓厚的东方文化底蕴。"
            }
        ],
        "submit_time": "2025-09-09 13:41:54.041",
        "scheduled_time": "2025-09-09 13:41:54.087",
        "end_time": "2025-09-09 13:42:22.596"
    },
    "usage": {
        "image_count": 1
    }
}
```

#### **Java SDK调用**

**说明**

请先确认已安装最新版DashScope Java SDK，否则可能运行报错：[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## 同步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.HashMap;
import java.util.Map;

public class Text2Image {
    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：static String apiKey = "sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void basicCall() throws ApiException, NoApiKeyException {
        String prompt = "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。";
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("negative_prompt", " ");
        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        // 当前仅qwen-image-plus、qwen-image模型支持异步接口
                        .model("qwen-image-plus")
                        .prompt(prompt)
                        .n(1)
                        .size("1664*928")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---同步调用，请等待任务执行----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args){
        try{
            basicCall();
        }catch(ApiException|NoApiKeyException e){
            System.out.println(e.getMessage());
        }
    }
}
```

##### **响应示例**

> url 有效期24小时，请及时下载图像。

```
{
    "request_id": "f2153409-3950-9b73-9980-xxxxxx",
    "output": {
        "task_id": "2fc2e1de-0245-442d-b664-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。",
                "actual_prompt": "一副典雅庄重的对联悬挂于中式厅堂中央，对联左侧书写“义本生知人机同道善思新”，右侧书写“通云赋智乾坤启数高志远”，横批为“智启千问”，整体采用飘逸洒脱的书法字体，墨色浓淡相宜，展现出浓厚的传统韵味。对联中间悬挂一幅中国风画作，描绘的是著名的岳阳楼景观：楼阁飞檐翘角，依水而建，远处湖光潋滟，烟波浩渺，天空中有几缕轻云缭绕，营造出诗意盎然的意境。背景房间为安静古典的中式布置，木质家具线条流畅，桌上摆放着数件青花瓷器，纹饰精美，釉色莹润。整体空间光线柔和，营造出庄重、宁静的文化氛围。画面风格为传统中国水墨风，笔触细腻，层次分明，充满古典美感。",
                "url": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxxx"
            }
        ]
    },
    "usage": {
        "image_count": 1
    }
}
```

## 异步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.HashMap;
import java.util.Map;

public class Text2Image {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：static String apiKey = "sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public void asyncCall() {
        System.out.println("---创建任务----");
        String taskId = this.createAsyncTask();
        System.out.println("--等待任务结束返回图像url----");
        this.waitAsyncTask(taskId);
    }

    public String createAsyncTask() {
        String prompt = "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。";
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("negative_prompt", " ");
        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        // 当前仅qwen-image-plus、qwen-image模型支持异步接口
                        .model("qwen-image-plus")
                        .prompt(prompt)
                        .n(1)
                        .size("1664*928")
                        .parameters(parameters)
                        .build();

        try {
            ImageSynthesisResult result = new ImageSynthesis().asyncCall(param);
            System.out.println(JsonUtils.toJson(result));
            String taskId = result.getOutput().getTaskId();
            System.out.println("task_id=" + taskId);
            return taskId;
        } catch (Exception e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public void waitAsyncTask(String taskId) {
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        long startTime = System.currentTimeMillis();
        int timeout = 60 * 1000; // 1分钟超时
        int interval = 5 * 1000;  // 5秒轮询间隔

        while (true) {
            if (System.currentTimeMillis() - startTime > timeout) {
                System.out.println("轮询超时（1分钟），任务未完成");
                return;
            }

            try {
                ImageSynthesisResult result = imageSynthesis.fetch(taskId, apiKey);
                System.out.println("任务状态查询结果: " + JsonUtils.toJson(result));
                if (result.getOutput() == null) {
                    System.out.println("获取任务状态失败，输出结果为空");
                    return;
                }
                String taskStatus = result.getOutput().getTaskStatus();
                System.out.println("当前任务状态: " + taskStatus);
                switch (taskStatus) {
                    case "SUCCEEDED":
                        System.out.println("任务已完成");
                        System.out.println(JsonUtils.toJson(result));
                        return;
                    case "FAILED":
                        System.out.println("任务执行失败, status: " + taskStatus);
                        return;
                    case "PENDING":
                    case "RUNNING":
                        System.out.println("任务正在进行中，5秒后继续查询...");
                        Thread.sleep(interval);
                        break;
                    default:
                        System.out.println("未知任务状态: " + taskStatus + "，5秒后继续查询...");
                        Thread.sleep(interval);
                        break;
                }
            } catch (ApiException | NoApiKeyException e) {
                System.err.println("API调用异常: " + e.getMessage());
                return;
            } catch (InterruptedException e) {
                System.err.println("线程中断异常: " + e.getMessage());
                Thread.currentThread().interrupt();
                return;
            }
        }
    }

    public static void main(String[] args){
        Text2Image text2Image = new Text2Image();
        text2Image.asyncCall();
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "request_id": "f2153409-3950-9b73-9980-xxxxxx",
    "output": {
        "task_id": "2fc2e1de-0245-442d-b664-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。",
                "actual_prompt": "一副典雅庄重的对联悬挂于中式厅堂中央，对联左侧书写“义本生知人机同道善思新”，右侧书写“通云赋智乾坤启数高志远”，横批为“智启千问”，整体采用飘逸洒脱的书法字体，墨色浓淡相宜，展现出浓厚的传统韵味。对联中间悬挂一幅中国风画作，描绘的是著名的岳阳楼景观：楼阁飞檐翘角，依水而建，远处湖光潋滟，烟波浩渺，天空中有几缕轻云缭绕，营造出诗意盎然的意境。背景房间为安静古典的中式布置，木质家具线条流畅，桌上摆放着数件青花瓷器，纹饰精美，釉色莹润。整体空间光线柔和，营造出庄重、宁静的文化氛围。画面风格为传统中国水墨风，笔触细腻，层次分明，充满古典美感。",
                "url": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxxx"
            }
        ]
    },
    "usage": {
        "image_count": 1
    }
}
```

## **计费与限流**

-   模型免费额度和计费单价请参见[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#11a4ac6ea62wt)。
    
-   模型限流请参见[千问（Qwen-Image）](https://help.aliyun.com/zh/model-studio/rate-limit#f812e7c63axvx)。
    
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q：prompt\_extend参数应该开启还是关闭？**

A：如果希望图像内容更多样化，由模型补充细节，建议开启此选项（默认）。如果图像细节更可控，建议关闭此选项，并参考[文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt)进行优化，

#### **Q：qwen-image、qwen-image-plus、qwen-image-max、qwen-image-2.0、qwen-image-edit 等模型的区别是什么？**

A：

-   **图像生成与编辑融合模型：**同时支持文生图和图像编辑。
    
    -   `qwen-image-2.0-pro`、`qwen-image-2.0-pro-2026-03-03`：当前两者能力相同，Pro系列具备更专业的文字渲染能力、更细腻的真实质感，细腻刻画写实场景，以及更强的语义遵循能力。仅支持同步接口。
        
    -   `qwen-image-2.0`、`qwen-image-2.0-2026-03-03`：当前两者能力相同，加速版有效实现了模型效果和性能的最佳平衡。仅支持同步接口。
        
-   **文生图模型：**根据文本描述生成图像。
    
    -   `qwen-image-max`、`qwen-image-max-2025-12-30`：当前两者能力相同，相较于`qwen-image-plus`提升了生成图像的真实感与自然度，在人物质感、纹理细节和文字渲染等方面效果更佳。
        
    -   `qwen-image`、`qwen-image-plus`：当前两者能力相同，但`qwen-image-plus`的价格更优惠。
        
    -   `qwen-image-plus-2026-01-09`：千问图像生成的全新快照版模型，为`qwen-image-max`的蒸馏加速版，支持快速生成高质量图像。
        
-   **图像编辑模型**：  
    `qwen-image-edit`：根据输入的图像和文本指令，执行图生图、局部修改等操作，详情请参见[千问-图像编辑](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)。
    

### **Q：如何获取图像存储的访问域名白名单？**

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
