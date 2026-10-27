# Tripo-文生/图生3D模型

Tripo 3D模型生成支持文生3D模型、单图生3D模型和多图生3D模型。

**相关文档**：[使用指南](raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 前提条件

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

由于3D模型生成任务耗时较长，API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
-   新手指引请参见[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

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

模型名称。可选值：

-   `Tripo/Tripo-H3.1`：高精度3D模型生成，输出产物最高200万面。对应 Tripo 官方 API 版本 `v3.1-20260211`。
-   `Tripo/Tripo-P1.0`：专业3D模型生成，输出产物最高2万面，速度更快。对应 Tripo 官方 API 版本 `P1-20260311`。

**input** `object` **（必选）**

输入信息。`prompt`、`image`、`images` 三者互斥，仅能选择其中一种输入方式。同时传入多个将会报错。

属性

**prompt** `string` （条件必填）

文本提示词，用于描述期望生成的3D模型。**仅在文生3D模型时必填。**

支持多语言（中文、英文等），每个字符（含中文汉字、英文字母等）均计为1个字符，最大长度1024个字符。

示例值：一只可爱的猫。

**image** `string` （条件必填）

单张图像的URL。**仅在单图生3D模型时必填。**

图像限制：

-   格式：JPEG、PNG。
-   分辨率：宽和高的范围为\[20, 6000\]像素，建议边长大于256像素。
-   文件大小：不超过20MB。

公网URL：

-   支持 HTTP 和 HTTPS 协议。
-   示例值：`https://xxx/xxx.jpg`。

**images** `array[object]` （条件必填）

多张图像的对象列表。**仅在多图生3D模型时必填。**

数组长度固定为4，对应图片顺序为**前、左、后、右**。

-   某个视角不需要图片时传入空对象`{}`；前视角（第1个元素）必须传入图片，有效图片数量为2~4张。
-   每张图像的限制与`image`参数相同，分辨率和宽高比不要求一致。
-   建议所有图像为同一物体在一致光照下的不同视角，多视角输入可提高几何精度和贴图覆盖度。

每个图像对象包含以下字段：

-   `type`：图像格式，可选值为`jpeg`或`png`。
-   `file_token`：图像的公网URL。

**parameters** `object` （可选）

3D模型生成参数。

属性

**texture\_quality** `string` （可选）

贴图质量。贴图是覆盖在3D模型表面的纹理图像，决定了模型的外观细节和视觉效果。

可选值：

-   `standard`：默认值，标清贴图，兼顾质量与速度。
-   `detailed`：高清贴图，保真度更高，生成速度较慢。
-   `extreme`：8K贴图，保真度最高。

**geometry\_quality** `string` （可选）

支持模型：`Tripo/Tripo-H3.1`。`Tripo/Tripo-P1.0`传入此参数会被忽略，不会报错。

几何精度。可选值：

-   `standard`：默认值，标准版，兼顾质量与速度。生成的3D模型最高150万面。
-   `ultra`：超清版，几何细节更精细。生成的3D模型最高200万面。等同于 Tripo 官方 API 的`detailed`。

**pbr** `boolean` （可选）

是否生成PBR材质模型。PBR材质包含基础色（base\_color）、金属度（metallic）、粗糙度（roughness）和法线（normal）贴图。默认值为`true`。

当`pbr`设为`true`时，会强制启用贴图（即`texture`也会被设为`true`），返回结果中包含`pbr_model_url`。

**texture** `boolean` （可选）

是否生成贴图。默认值为`true`。

如需生成无贴图模型，需同时设置`texture`和`pbr`为`false`，返回结果中包含`base_model_url`。

**quad** `boolean` （可选）

支持模型：`Tripo/Tripo-H3.1`。`Tripo/Tripo-P1.0`传入此参数会被忽略，不会报错。

是否输出四边面网格（而非三角面）。默认值为`false`。

开启后，输出格式强制为FBX；未设置`face_limit`时，默认面数为10,000。

**smart\_low\_poly** `boolean` （可选）

支持模型：`Tripo/Tripo-H3.1`。`Tripo/Tripo-P1.0`传入此参数会被忽略，不会报错。

是否生成智能低模，即具有手工建模风格、拓扑干净的低面数模型。默认值为`false`。适合结构简单的输入，复杂模型可能偶尔生成失败。

开启后，`face_limit`的取值范围为：三角面500~20,000，四边面500~10,000。与`generate_parts`同时开启时，`generate_parts`不生效。

**generate\_parts** `boolean` （可选）

支持模型：`Tripo/Tripo-H3.1`。`Tripo/Tripo-P1.0`传入此参数会被忽略，不会报错。

是否生成可编辑的分割部件。默认值为`false`。

开启后，与以下参数不兼容：

-   `texture`、`pbr`：不传时二者默认按`false`处理。设置`texture`或`pbr`为`true`，或传入`texture_quality`时，返回400错误。
-   `quad`：设置为`true`时会被忽略，返回的部件为三角面网格。
-   `smart_low_poly`：同时开启时，`smart_low_poly`优先，不会生成部件。

如需生成部件，`texture`和`pbr`可不传或设置为`false`，且不要传入`texture_quality`、`quad`和`smart_low_poly`。

**compress** `string` （可选）

支持模型：`Tripo/Tripo-H3.1`。

压缩模式。不传则不压缩。可选值：

-   `geometry`：使用 meshopt 压缩几何数据，减小文件体积。

**negative\_prompt** `string` （可选）

反向提示词，用于描述不希望在3D模型中出现的内容。最大长度255个字符。

**face\_limit** `integer` （可选）

生成的3D模型面数上限。不传时由模型自适应决定。取值范围：

-   `Tripo/Tripo-H3.1`：三角面不超过1,500,000（`geometry_quality`为`ultra`时不超过2,000,000）；四边面（`quad`为`true`）不超过150,000。未开启`smart_low_poly`时建议不低于500，需要更低面数时请开启`smart_low_poly`或使用[Tripo-重拓扑](raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)。开启`smart_low_poly`时的取值范围见该参数说明。
-   `Tripo/Tripo-P1.0`：50~20,000，超出范围返回400错误。

建议值：游戏资产50,000~100,000，Web和移动端10,000~50,000。

**model\_seed** `integer` （可选）

几何体生成的随机种子。取值范围：-2147483648~2147483647。

使用相同种子和相同输入将生成相同的3D网格。不设置时每次使用随机种子。

**image\_seed** `integer` （可选）

图像生成环节的随机种子。取值范围：-2147483648~2147483647。

主要用于文生3D模型时根据提示词生成参考图。单图、多图生3D模型仅在开启`enable_image_autofix`，或`texture_quality`为`detailed`、`extreme`时生效，一般无需设置。

**texture\_seed** `integer` （可选）

贴图生成的随机种子。取值范围：-2147483648~2147483647。

使用相同种子将生成相同的贴图。不设置时每次使用随机种子。如需获取几何体相同、贴图不同的模型，请保持`model_seed`不变并更改`texture_seed`。

**texture\_alignment** `string` （可选）

贴图对齐方式。可选值：

-   `original_image`：默认值，优先匹配输入图像的颜色。
-   `geometry`：优先匹配生成的几何体。

**orientation** `string` （可选）

模型朝向。仅当`texture`为`true`时生效。可选值：

-   `default`：默认值，自动朝向。
-   `align_image`：将模型对齐至输入图像的视角。

**export\_orientation** `string` （可选）

导出模型的朝向（前向轴）。可选值：

-   `+x`：默认值，X轴正方向朝前。
-   `-x`：X轴负方向朝前。
-   `+y`：Y轴正方向朝前。
-   `-y`：Y轴负方向朝前。

**说明**

-   此参数仅作用于本次生成。如需将模型用于后续的贴图、绑定、重定向、格式转换等后处理任务，不建议设置此参数。
-   设置此参数后再进行后处理，可能因模型方向错误影响最终效果，但任务状态仍为`SUCCEEDED`，不会报错。
-   如计划对模型做后处理，建议不设置此参数，在最后一步通过格式转换调整朝向。

**auto\_size** `boolean` （可选）

是否自动将模型缩放至真实世界尺寸。默认值为`false`。开启后模型尺寸以米为单位，适用于AR/VR或游戏引擎场景。

**export\_uv** `boolean` （可选）

是否在生成过程中进行UV展开。默认值为`true`。设为`false`可加快生成速度并减小文件体积，UV展开将在贴图阶段处理。

**enable\_image\_autofix** `boolean` （可选）

是否自动修复输入图像。默认值为`false`。仅在单图生3D模型（传入`image`）时生效。

#### 文生3D模型（有贴图）

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
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

#### 单图生3D模型（有贴图）

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
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

#### 单图生3D模型（H3.1超清）

仅`Tripo/Tripo-H3.1`支持`geometry_quality`和`quad`参数。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-H3.1",
    "input": {
        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/cfbxhg/tripo-single.jpg"
    },
    "parameters": {
        "texture_quality": "detailed",
        "geometry_quality": "ultra",
        "quad": true
    }
}'
```

#### 多图生3D模型（有贴图）

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
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

#### 多图生3D模型（传入2张图）

图片顺序为前、左、后、右，不需要的视角传入空对象`{}`即可。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "images": [
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png" },
            {},
            { "type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/zjqhyn/tripo-images-3.png" },
            {}
        ]
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

#### 无贴图生成

需同时将`texture`和`pbr`设为`false`。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
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
        "texture": false,
        "pbr": false
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

-   **轮询建议**：3D模型生成通常需要30~120秒，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
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
-   当状态变为 SUCCEEDED 时，响应中将包含生成的3D模型URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results**`array`

生成结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**model\_url** `string`

3D模型的URL。生成任务均返回。

**pbr\_model\_url** `string`

PBR材质模型的URL。未开启`quad`时为GLB格式，开启`quad`时为FBX格式。当`pbr`为`true`（默认）且未开启`generate_parts`时返回。`texture`为`true`、`pbr`为`false`时不返回，带贴图的模型通过`model_url`获取。

**base\_model\_url** `string`

无贴图基础模型的URL。未开启`quad`时为GLB格式，开启`quad`时为FBX格式。当请求参数中`texture`和`pbr`均为`false`时返回。

**rendered\_image\_url** `string`

3D模型预览渲染图的URL（1张）。

**generated\_image\_url** `string`

文生3D模型时，根据提示词生成的中间图像的URL。

**orig\_prompt** `string`

原始输入的prompt，对应请求参数`prompt`。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

3D模型生成任务类型。枚举值：

-   `text-to-3d`：文生3D模型。
-   `image-to-3d`：单图生3D模型。
-   `multi-image-to-3d`：多图生3D模型。

**credits\_consumed** `integer`

本次任务消耗的积分。计算公式：

`credits_consumed` = 基础项积分 + `texture_quality` + `geometry_quality` + `quad` + `smart_low_poly` + `generate_parts`

-   基础项积分由模型和任务类型决定，不单独返回。各计费项的积分请参见[模型调用价格](https://help.aliyun.com/zh/model-studio/model-pricing#trp002a0h2001)。
-   公式中的计费参数为`usage`中返回的积分增量，积分增量为0的计费参数不返回，按0计算。

**texture\_quality** `integer`

生成贴图增加的积分，按贴图质量计算。生成贴图但未传`texture_quality`时（包括不传任何贴图参数），按`standard`计费。生成无贴图模型（`texture`和`pbr`均为`false`）时不返回。

**geometry\_quality** `integer`

使用高精度几何增加的积分。仅`Tripo/Tripo-H3.1`且`geometry_quality`为`ultra`时返回。

**quad** `integer`

输出四边面网格增加的积分。仅`Tripo/Tripo-H3.1`开启`quad`时返回。

**smart\_low\_poly** `integer`

生成智能低模增加的积分。仅`Tripo/Tripo-H3.1`开启`smart_low_poly`时返回。

**generate\_parts** `integer`

按部件生成增加的积分。仅`Tripo/Tripo-H3.1`开启`generate_parts`且生效时返回。

#### 任务执行成功

```
{
    "request_id": "5fc8c4c2-f8b1-9ea2-bdda-xxxxxx",
    "output": {
        "task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-16 16:39:53.349",
        "scheduled_time": "2026-10-16 16:39:53.388",
        "end_time": "2026-10-16 16:41:36.379",
        "results": [
            {
                "rendered_image_url": "https://openapi.cdn.tripo3d.com/xxxx/legacy_mesh.webp?auth_key=xxxx",
                "model_url": "https://openapi.cdn.tripo3d.com/xxxx/tripo_base_model_xxxx.glb?auth_key=xxxx",
                "generated_image_url": "https://openapi.cdn.tripo3d.com/xxxx/text2image_xxxx.jpeg?auth_key=xxxx"
            }
        ]
    },
    "usage": {
        "3d_task_type": "text-to-3d",
        "credits_consumed": 40,
        "texture_quality": 10
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-xxxxxx",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-xxxxxx",
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

如果模型调用失败并返回报错信息，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)进行解决。
