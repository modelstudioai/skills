# Tripo-动画重定向

Tripo动画重定向可将预设动画应用到已绑骨的3D模型上，单次最多5个动画。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先通过[Tripo-自动绑骨](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)创建任务（`spec`不能为`mixamo`），待任务执行成功后，将其`task_id`传入`original_model_task_id`。

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

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

模型名称。固定值：`Tripo/Tripo-AnimationRetarget`。

**input** `object` **（必选）**

输入信息。

属性

**original\_model\_task\_id** `string` **（必选）**

前序任务ID。仅支持[Tripo-自动绑骨](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)任务，传入该任务创建时返回的`task_id`，系统会自动使用该任务输出的已绑骨模型。

-   前序任务必须已执行成功。
-   发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。
-   使用`mixamo`规格（`spec`）绑骨的模型不能用于动画重定向。

**parameters** `object` （可选）

动画重定向参数。

属性

**animations** `array[string]` （条件必填）

预设动画名称列表，最多5个，**按动画个数计费**。与`animation`互斥，只能二选一。

每个元素须为带`preset:`前缀的预制动画名称（如`preset:walk`），区分大小写。不在列表中的名称在创建任务时返回400错误，不扣费。

完整的动画名称请参见[动画名称列表](#tre801h2anim)。

**animation** `string` （条件必填）

单个预设动画名称，取值要求与`animations`相同。与`animations`互斥，只能二选一。此参数为旧版参数，计为1个动画，计费与`animations`只传1个动画时相同。

**out\_format** `string` （可选）

输出格式。默认值为`glb`。可选值：

-   `glb`：二进制glTF格式，适用于Web。
-   `fbx`：FBX格式，适用于DCC工具和游戏引擎。

**bake\_animation** `boolean` （可选）

是否烘焙动画。该参数已废弃，传入不会报错，也不会生效或计费，仅为向后兼容保留，无需传入。

**export\_with\_geometry** `boolean` （可选）

导出时是否包含几何体。默认值为`true`。

**animate\_in\_place** `boolean` （可选）

是否原地播放动画。默认值为`false`。设为`true`时，模型在动画中不产生位移。

#### 单个动画

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-AnimationRetarget",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx"
    },
    "parameters": {
        "animations": ["preset:walk"],
        "out_format": "fbx"
    }
}'
```

#### 多个动画

通过`animations`传入多个动画名称，最多5个。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-AnimationRetarget",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx"
    },
    "parameters": {
        "animations": ["preset:walk", "preset:run"],
        "out_format": "glb"
    }
}'
```

#### 非人形骨骼

前序自动绑骨任务的`rig_type`为非人形骨骼（如`quadruped`）时，动画名称须使用`preset:<体型>:<动作>`格式，可用名称请参见[非人形骨骼](#tre803h3nonh)。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-AnimationRetarget",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx"
    },
    "parameters": {
        "animations": ["preset:quadruped:walk"]
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

-   **轮询建议**：建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
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
-   当状态变为 SUCCEEDED 时，响应中将包含重定向后的3D模型URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results**`array`

重定向结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**model\_url** `string`

重定向后3D模型的URL。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

任务类型。动画重定向固定为`animation-retarget`。

**credits\_consumed** `integer`

本次任务消耗的积分，按动画数量计费。动画数量为`animations`中非空元素的个数；使用`animation`时计为1个动画。

#### 任务执行成功

```
{
    "request_id": "36a8ae2d-e929-9315-8394-xxxxxx",
    "output": {
        "task_id": "00195645-f254-41bd-8354-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-19 12:56:48.349",
        "scheduled_time": "2026-10-19 12:56:48.399",
        "end_time": "2026-10-19 12:57:04.742",
        "results": [
            {
                "model_url": "https://openapi.cdn.tripo3d.com/xxxx/tripo_retarget_xxxx.fbx?auth_key=xxxx"
            }
        ]
    },
    "usage": {
        "3d_task_type": "animation-retarget",
        "credits_consumed": 10
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

## 动画名称列表

以下为`parameters.animations`和`parameters.animation`参数的可选值。名称须带`preset:`前缀，区分大小写。

### 常用动画

-   `preset:idle`：待机
-   `preset:walk`：行走
-   `preset:run`：奔跑
-   `preset:jump`：跳跃
-   `preset:climb`：攀爬
-   `preset:dive`：俯冲
-   `preset:slash`：挥砍
-   `preset:shoot`：射击
-   `preset:hurt`：受击
-   `preset:fall`：跌落
-   `preset:turn`：转身

### 非人形骨骼

非人形骨骼仅支持以下名称，写法为`preset:<体型>:<动作>`。

-   四足（`quadruped`）：`preset:quadruped:walk`、`preset:quadruped:catwalk`
-   水生（`aquatic`）：`preset:aquatic:march`
-   蛇形（`serpentine`）：`preset:serpentine:march`
-   六足（`hexapod`）：`preset:hexapod:walk`
-   八足（`octopod`）：`preset:octopod:walk`

### 人形骨骼

人形骨骼（`biped`）的动作名有两种等价写法：`preset:<动作>`或`preset:biped:<动作>`，例如`preset:walk`与`preset:biped:walk`效果相同。

-   `preset:afraid`、`preset:agree`、`preset:angry_01`、`preset:angry_02`、`preset:angry_03`
-   `preset:basketball_shot`、`preset:blade_wraparound_test`、`preset:bow`、`preset:box_01`、`preset:box_02`、`preset:box_03`
-   `preset:cast_a_spell`、`preset:cheer`、`preset:chop`、`preset:clap`、`preset:climb`、`preset:complain_01`、`preset:complain_02`、`preset:cpr`、`preset:cross_body_crunch`、`preset:crossover_dribble`、`preset:cry`
-   `preset:dance_01`、`preset:dance_02`、`preset:dance_03`、`preset:dance_04`、`preset:dance_05`、`preset:dance_06`、`preset:defeat_02`、`preset:defeat_03`、`preset:depressed`、`preset:dig`、`preset:dive`、`preset:dribble`
-   `preset:fall`、`preset:fire`、`preset:flee_01`、`preset:flee_02`、`preset:flip`、`preset:fold_arms`、`preset:football_catch`、`preset:football_pass`、`preset:football_save`、`preset:freaky`、`preset:frightened`、`preset:front_kick_01`、`preset:front_kick_02`、`preset:frustrated_01`、`preset:frustrated_02`
-   `preset:golf`、`preset:greet_01`、`preset:greet_02`、`preset:greet_03`、`preset:greet_04`
-   `preset:heart_pose`、`preset:hit_to_body_01`、`preset:hit_to_body_02`、`preset:hit_to_head`、`preset:hit_to_side`、`preset:hit_to_stomach`、`preset:hug`、`preset:hurt`
-   `preset:idle`
-   `preset:jump`、`preset:jump_down`、`preset:jump_rope_01`、`preset:jump_rope_02`
-   `preset:laugh_01`、`preset:laugh_02`、`preset:lift_heavy`、`preset:look_around`
-   `preset:make_a_call_01`、`preset:make_a_call_02`
-   `preset:pitch_baseball`、`preset:play_mobile_game`、`preset:play_video_game`、`preset:press-up`
-   `preset:run`、`preset:run_upstairs`
-   `preset:scared_01`、`preset:scared_02`、`preset:scratch`、`preset:shoot`、`preset:shovel`、`preset:sing_01`、`preset:sing_02`、`preset:sing_03`、`preset:sing_04`、`preset:sit`、`preset:slash`、`preset:sob`、`preset:standing_relax`、`preset:surf`、`preset:swagger`、`preset:swim`、`preset:sword_judgment_test`
-   `preset:turn`
-   `preset:victory_celebration`、`preset:volleyball`
-   `preset:wait`、`preset:walk`、`preset:warm_up`、`preset:wave_goodbye_01`、`preset:wave_goodbye_02`

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)进行解决。
