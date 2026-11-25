# 万相-数字人

数字人wan2.2-s2v模型支持基于 单张图片和音频 ，生成动作自然的说话、唱歌或表演视频，不限制形象画幅，支持 肖像、全身或半身 的人物图像。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="模型概览"></a>

<a id="8ed6166014a83"></a>

<a id="a2429cf3ebvbq"></a>

## 模型概览

<a id="72ea9ffa162uw"></a>

<a id="5f20476c46vtj"></a>

##### 效果示例

| 输入示例 | 输出视频 |
| --- | --- |
| ![input\_image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8144216571/p1001125.jpeg)**输入音频** |  |

生成数字人视频的流程为：

-   **步骤1**：调用 wan2.2-s2v-detect 接口，传入图片URL，确认图片合规。
-   **步骤2**：若检测通过，调用 wan2.2-s2v 异步接口，传入图片URL和音频URL，提交视频生成任务，并轮询获取结果。

<a id="快速开始"></a>

<a id="e5bdbcf4deej1"></a>

<a id="81171c677cvwd"></a>

## 快速开始

<a id="前提条件"></a>

<a id="d3e92944e3t55"></a>

<a id="8b74b54246ib7"></a>

#### 前提条件

在调用前，您需要[开通模型服务并获取API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](../../preparations/get-api-key.md)。

<a id="示例代码"></a>

<a id="fa053a9e29u3k"></a>

<a id="9a919c58acvrt"></a>

#### 示例代码

本文的示例图片已通过图像检测，以下展示视频生成的示例代码。

> **说明**
>
> HTTP 请求分两步：先创建任务，再获取结果。初学者建议使用 [Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)调用API。

<a id="a4ac549258mtq"></a>

<a id="752f63a499kjw"></a>

##### 步骤1：创建任务获取任务ID

该请求会返回一个`task_id`用于查询结果。

<a id="code-block"></a>

```bash
curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
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

<a id="26c6e917d9j74"></a>

<a id="adaad8ba0flc1"></a>

##### 步骤2：根据任务ID查询结果

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

> 若使用新加坡地域的模型，需将base\_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。

<a id="code-block-2"></a>

```bash
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

`task_id`查询有效期为24小时，过期将无法查询，接口将返回任务状态为`UNKNOWN`。

<a id="下一步"></a>

<a id="8129d25e7067o"></a>

<a id="2849fa3c9aebl"></a>

## 下一步

根据您的具体需求，查阅API文档开始您的开发工作：

[图像检测API](wan-s2v-overview/wan-s2v-detect-api.md)

[视频生成API](wan-s2v-overview/wan-s2v-api.md)
