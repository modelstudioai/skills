# Tripo 3D模型生成

通过阿里云百炼平台调用 Tripo 模型，支持三种生成模式： 文生3D模型、单图生3D模型和多图生3D模型 。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## 快速开始

> 以**文生3D模型**为例。

**输入提示词**

**输出预览**

一只可爱的猫

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb)

在调用前，[开通Tripo模型服务](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)。

#### 步骤1：创建任务获取任务ID

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "prompt": "一只可爱的猫"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

返回 `task_id`，示例值：`0385dc79-5ff8-4d82-bcb6-xxxxxx`。

#### 步骤2：根据任务ID获取结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

> 任务状态流转：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）/ `FAILED`（失败）。

> 3D 生成通常需要数分钟，建议**轮询**间隔 15 秒，如需事件通知替代轮询，请参见[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。

**输出示例**
```
{
    "request_id": "c1209113-8437-424f-a386-xxxxxx",
    "output": {
        "task_id": "966cebcd-dedc-4962-af88-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "pbr_model_url": "https://openapi.cdn.tripo3d.com/xxxx.glb?auth_key=xxxx",  // PBR材质的3D模型（GLB格式），有效期2小时
                "rendered_image_url": "https://openapi.cdn.tripo3d.com/xxxx.webp?auth_key=xxxx"  // 渲染预览图，有效期2小时
            }
        ]
        ...
    },
    ...
}
```

## 模型选型

**模型名称**

**能力支持**

**产物最高面数**

**速度**

**适用场景**

Tripo/Tripo-H3.1

文生3D模型

单图生3D模型

多图生3D模型

200 万面

较慢

影视级渲染、高精度数字资产

Tripo/Tripo-P1.0

文生3D模型

单图生3D模型

多图生3D模型

2 万面

更快

快速预览、游戏/AR 场景、实时应用

如果不确定选哪个，建议先用 Tripo-P1.0 快速验证效果，再用 Tripo-H3.1 生成高精度版本。

## 核心能力

三种模式通过 `input` 中的不同字段区分。`prompt`、`image`、`images` 三个字段互斥，每次请求只能选一种。

### 文生3D模型

通过 `prompt` 传入文本提示词，描述期望生成的3D模型。支持多语言（中文、英文等）。

**输入提示词**

**输出预览**

一辆红色跑车

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260508/smfsql/red_car.glb)

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "prompt": "一辆红色跑车"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

### 单图生3D模型

通过 `image` **传入单张图片**的URL，从图片生成3D模型。

**图片要求**：JPEG 或 PNG 格式，宽高范围 20~6000 像素（建议 > 256 像素），不超过 20MB。

**输入图像（单张）**

**输出预览**

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/lqsfqk/tripo-image-to-3d-result.glb)

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/cfbxhg/tripo-single.jpg"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

### 多图生3D模型

通过 `images` **传入2~4张多角度图片**的URL列表，生成还原度更高的3D模型。多张图片的分辨率和宽高比不要求一致，每张图片的格式要求与单图相同。

**输入图像（多张）**

**输出预览**

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/qoomsm/tripo-multi-image-to-3d-result.glb)

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "images": [
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png" },
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/slgluy/tripo-images-2.png" },
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/zjqhyn/tripo-images-3.png" },
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mqfzww/tripo-images-4.png" }
        ]
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

## 贴图与几何精度

### 贴图质量

贴图是覆盖在 3D 模型表面的纹理图像，决定外观细节。通过 `parameters.texture_quality` 控制贴图质量：

-   `standard`：默认值，标清贴图，满足大多数场景。
-   `detailed`：高清贴图，适合需要精细表面细节的场景。

**输出模型是否贴图**

**输入参数配置**

**输出预览**

**有贴图**

```
"parameters": {
    "texture_quality": "standard"
}
```

> 返回结果中包含 `pbr_model_url`

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb)

**无贴图**

```
"parameters": {
    "texture": false,
    "pbr": false
}
```

> 需同时设置 `texture` 和 `pbr` 为 `false`

> 返回结果中包含 `base_model_url`

> 上图为效果展示，实际产物为[3D文件](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260508/wwonyw/cat-no-texture.glb)

### 几何精度

仅 `Tripo/Tripo-H3.1` 支持。通过 `parameters.geometry_quality` 控制几何精度：

-   `standard`：默认值，最高150万面。
-   `ultra`：超清版，最高200万面。

## 输出产物

任务成功后，响应中包含：

-   `pbr_model_url`：PBR 材质的 3D 模型（GLB 格式），可直接导入 Blender、Unity 等工具。
-   `base_model_url`：无贴图基础模型（GLB 格式）。当 `texture` 和 `pbr` 均为 `false` 时返回。
-   `rendered_image_url`：3D 模型的渲染预览图（1 张）。

以上链接有效期均为 **2 小时**，请及时下载保存。

## API参考

[Tripo-3D模型生成API参考](raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)

## 常见问题

#### prompt、image、images 能同时传入吗？

不能。三个字段互斥，每次请求只能选择其中一种生成模式。同时传入多个字段会导致请求失败。
