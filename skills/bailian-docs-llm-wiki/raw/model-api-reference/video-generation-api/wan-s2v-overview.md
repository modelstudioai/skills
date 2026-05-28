# 万相-数字人

数字人wan2.2-s2v模型支持基于**单张图片和音频**，生成动作自然的说话、唱歌或表演视频，不限制形象画幅，支持**肖像、全身或半身**的人物图像。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型概览**

##### **效果示例**

**输入示例**

**输出视频**

![input\_image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8144216571/p1001125.jpeg)

**输入音频**

##### 模型与价格

**模型名称**

**模型简介**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**任务下发接口RPS限制**

**同时处理中任务数量**

wan2.2-s2v-detect

检查输入图像是否满足要求（如清晰度、单人、正面）。

0.004元/张

5

同步接口无限制

200张

wan2.2-s2v

根据检测通过的图片和一段音频，生成人物动态视频。

480P：0.5元/秒

720P：0.9元/秒

5

1

100秒

生成数字人视频的流程为：

-   **步骤一**：调用 wan2.2-s2v-detect 接口，传入图片URL，确认图片合规。
    
-   **步骤二**：若检测通过，调用 wan2.2-s2v 异步接口，传入图片URL和音频URL，提交视频生成任务，并轮询获取结果。
    

## **快速开始**

#### **前提条件**

在调用前，您需要[开通模型服务并获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### **示例代码**

本文的示例图片已通过图像检测，以下展示视频生成的示例代码。

**说明**

HTTP 请求分两步：先创建任务，再获取结果。初学者建议使用 [Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)调用API。

##### **步骤1：创建任务获取任务ID**

该请求会返回一个`task_id`用于查询结果。

```
curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis/' \
 --header 'X-DashScope-Async: enable' \
 --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
 --header 'Content-Type: application/json' \
 --data '{
     "model": "wan2.2-s2v",
     "input": {
            "image_url": "https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg",
            "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/iaqpio/input_audio.MP3"
        },
        "parameters": {
            "style": "speech"
        }
    }'
```

##### **步骤2：根据任务ID查询结果**

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

> 若使用新加坡地域的模型，需将base\_url替换为https://dashscope-intl.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

`task_id`查询有效期为24小时，过期将无法查询，接口将返回任务状态为`UNKNOWN`。

## **模型对比**

**模型选型建议**：如需生成包含人物全身或大半身的视频，推荐使用 wan2.2-s2v 模型；若追求性价比，可选择悦动人像EMO。

**功能对比**

**数字人wan2.2-s2v**

**悦动人像EMO**（[查看](https://help.aliyun.com/zh/model-studio/emo-quick-start/)）

**模型简介**

动作幅度更大更自然，画幅支持范围广（尤其全身），支持卡通人物形象

更适合人物特写或肖像，对口型表情自然

**适用画幅**

全身、半身、肖像

肖像、半身（推荐）

**调用方式**

两步调用，检测接口仅用于合规性校验，接入更简单

两步调用，检测接口返回的坐标是生成接口的必需入参

**风格控制**

场景驱动（说话, 唱歌, 表演）

风格驱动（适中、平静、活泼）

**输出规格**

按分辨率（480P, 720P）

按画幅比（1:1, 3:4）

**模型调用价格**

-   图像检测：0.004元/张
    
-   视频生成：
    
    -   480P: 0.5元/秒
        
    -   720P: 0.9元/秒
        

-   图像检测：0.004元/张
    
-   视频生成：
    
    -   1:1画幅: 0.08元/秒 
        
    -   3:4画幅: 0.16元/秒
        

## **下一步**

根据您的具体需求，查阅API文档开始您的开发工作：

[图像检测API](https://help.aliyun.com/zh/model-studio/wan-s2v-detect-api)

[视频生成API](https://help.aliyun.com/zh/model-studio/wan-s2v-api)
