# GetVideoAnalysisTask

轻应用-获取视频理解异步任务结果。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

阿里云百炼轻应用-视频理解-获取异步任务状态和结果：通过这个接口可以查看“提交异步任务”接口提交的视频理解任务状态和结果。欢迎前往[视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)体验。

> **说明**
>
> 当返回结果中包含`header -> errorCode = ViolationOfSecurityPolicy`时，表明该请求触发了系统的安全策略限制，请对请求内容进行相应的修改。此时，`videoAnalysisResult`等业务数据返回为空。

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| quanmiaolightapp:GetVideoAnalysisTask | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/quanmiao/lightapp/videoAnalysis/getVideoAnalysisTask HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | llm-xxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| taskId | string | 是 | 任务唯一标识 | a3d1c2ac-f086-4a21-9069-f5631542f5a2 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>requestId</td><td><p>string</p></td><td><div><p>Id of the request</p></div></td><td><p>5D0E915E-655D-59A8-894F-93873F73AAE5</p></td></tr><tr><td>code</td><td><p>string</p></td><td><div><p>状态码：仅代表 http 请求状态</p></div></td><td><p>successful</p></td></tr><tr><td>message</td><td><p>string</p></td><td><div><p>错误说明</p></div></td><td><p>success</p></td></tr><tr><td>httpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr><tr><td>success</td><td><p>boolean</p></td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td><p>True</p></td></tr><tr><td>data</td><td><p>object</p></td><td><div><p>结果</p></div></td><td></td></tr><tr><td>header</td><td><p>object</p></td><td><div><p>event 名称</p></div></td><td></td></tr><tr><td>errorCode</td><td><p>string</p></td><td><div><p>异常错误码</p></div></td><td><p>ERR-00000000</p></td></tr><tr><td>errorMessage</td><td><p>string</p></td><td><div><p>异常错误信息</p></div></td><td><p>url download error: http://xx</p></td></tr><tr><td>event</td><td><p>string</p></td><td><div><p>事件类型：任务执行状态</p><ul><li><p>task-finished：任务结束（成功）</p></li><li><p>task-failed：任务结束（失败）</p></li><li><p>task-xxx：中间态，可以不关注</p></li></ul></div></td><td><p>task-finshed</p></td></tr><tr><td>eventInfo</td><td><p>string</p></td><td><div><p>事件描述</p></div></td><td><p>url download error: http://xx</p></td></tr><tr><td>sessionId</td><td><p>string</p></td><td><div><p>会话唯一标识</p></div></td><td><p>d5c38cf6-a4bf-4a57-a697-9f449926f0c9</p></td></tr><tr><td>taskId</td><td><p>string</p></td><td><div><p>生成唯一标识</p></div></td><td><p>6e223291-729b-4e84-9271-c13ada1a776b</p></td></tr><tr><td>traceId</td><td><p>string</p></td><td><div><p>全量路 ID</p></div></td><td><p>215045f817272303448235204efdef</p></td></tr><tr><td>payload</td><td><p>object</p></td><td><div><p>结果</p></div></td><td></td></tr><tr><td>output</td><td><p>object</p></td><td><div><p>结果</p></div></td><td></td></tr><tr><td>videoAnalysisResult</td><td><p>object</p></td><td><div><p>语言分析对应生成内容</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>vl 生成文本结果</p></div></td><td><p>xxx</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>Token 数量</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>imageTokens</td><td><p>integer</p></td><td><div><p>图片 token</p></div></td><td><p>1</p></td></tr><tr><td>videoShotAnalysisResults</td><td><p>array&lt;object&gt;</p></td><td><div><p>视频每个分镜对应语言分析结果：：因内容较大，请从 resultJsonFileUrl 文件中获取</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>视频分镜结果</p></div></td><td></td></tr><tr><td>endTime</td><td><p>integer</p></td><td><div><p>结束时间，相对时间，单位毫秒</p></div></td><td><p>10000</p></td></tr><tr><td>startTime</td><td><p>integer</p></td><td><div><p>开始时间，相对时间，单位毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>生成原始内容</p></div></td><td><p>xxxx</p></td></tr><tr><td>videoCaptionResult</td><td><p>object</p></td><td><div><p>视频字幕</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>videoCaptions</td><td><p>array&lt;object&gt;</p></td><td><div><p>视频字幕</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>视频字幕</p></div></td><td></td></tr><tr><td>endTime</td><td><p>integer</p></td><td><div><p>结束时间，相对时间，单位毫秒</p></div></td><td><p>20000</p></td></tr><tr><td>endTimeFormat</td><td><p>string</p></td><td><div><p>结束时间，格式化结果</p></div></td><td><p>00:01</p></td></tr><tr><td>startTime</td><td><p>integer</p></td><td><div><p>开始时间，相对时间，单位毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>startTimeFormat</td><td><p>string</p></td><td><div><p>开始时间，格式化结果</p></div></td><td><p>00:01</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>字幕内容</p></div></td><td><p>xxxx</p></td></tr><tr><td>speaker</td><td><p>string</p></td><td><div><p>角色</p></div></td><td><p>张三</p></td></tr><tr><td>videoGenerateResult</td><td><p>object</p></td><td><div><p>文本总结结果：多任务时，请从 videoGenerateResults 字段获取结果</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>生成文本</p></div></td><td><p>xxx</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>输出 Token 数量</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 Token 数量</p></div></td><td><p>2</p></td></tr><tr><td>modelId</td><td><p>string</p></td><td><div><p>模型 id</p></div></td><td><p>qwen-max-latest</p></td></tr><tr><td>modelReduce</td><td><p>boolean</p></td><td><div><p>模型是否被降级：如果模型是 qwen-max 或 qwen-max-latest，且超过 prompt 输入上限时，会尝试降级到 qwen-plus-latest 模型，保证信息完整性</p></div></td><td><p>qwen-plus-latest</p></td></tr><tr><td>reasonText</td><td><p>string</p></td><td><div><p>模型思考过程</p></div></td><td><p>xx</p></td></tr><tr><td>index</td><td><p>integer</p></td><td><div><p>多任务标号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>videoMindMappingGenerateResult</td><td><p>object</p></td><td><div><p>脑图生成结束</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>生成文本</p></div></td><td><p>小吃街</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>输入 Token 数量</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 Token 数量</p></div></td><td><p>2</p></td></tr><tr><td>videoMindMappings</td><td><p>array&lt;object&gt;</p></td><td><div><p>脑图结果</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>子节点</p></div></td><td></td></tr><tr><td>childNodes</td><td><p>array&lt;object&gt;</p></td><td><div><p>子节点</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>子节点</p></div></td><td></td></tr><tr><td>childNodes</td><td><p>array&lt;object&gt;</p></td><td><div><p>子节点</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>节点描述</p></div></td><td></td></tr><tr><td>name</td><td><p>string</p></td><td><div><p>节点描述</p></div></td><td><p>三级节点</p></td></tr><tr><td>name</td><td><p>string</p></td><td><div><p>节点描述</p></div></td><td><p>二级节点</p></td></tr><tr><td>name</td><td><p>string</p></td><td><div><p>节点描述</p></div></td><td><p>三级节点</p></td></tr><tr><td>videoTitleGenerateResult</td><td><p>object</p></td><td><div><p>标题生成结果</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>文本生成结果</p></div></td><td><p>xxxx</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>Token 数量</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>resultJsonFileUrl</td><td><p>string</p></td><td><div><p>结果 json 文件地址：</p><p>由于响应结果过大，部分数据获取改为文件方式，可以通过当前字段 url 下载文件，并解析使用：</p><ul><li>当前包含的字段：数据结构定义见 RunVideoAnalysis 接口<ul><li><p>videoShotSnapshotResult：每个分片抽帧信息，包括每帧 url</p></li><li><p>videoShotAnalysisResults：每个分片语言分析结果明细</p></li></ul></li><li><p>其他字段获取方式不变，文本方式返回。</p></li><li><p>文件类型：json</p></li><li><p>文件内容：全量报文，包含文本方式返回的 返回 event：task-finished</p></li></ul></div></td><td><p>http://xxx</p></td></tr><tr><td>videoGenerateResults</td><td><p>array&lt;object&gt;</p></td><td><div><p>当入参为多任务时（textProcessTasks 有值），返回文本加工结果对应这个字段，可以通过数据所在数组位置（下标）或 index（1 开始）找到对应结果。</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>文本加工任务结果</p></div></td><td></td></tr><tr><td>generateFinished</td><td><p>boolean</p></td><td><div><p>当前任务是否已生成结束</p></div></td><td><p>true</p></td></tr><tr><td>modelId</td><td><p>string</p></td><td><div><p>模型 id</p></div></td><td><p>xx</p></td></tr><tr><td>index</td><td><p>integer</p></td><td><div><p>多任务标号：1 开始</p></div></td><td><p>1</p></td></tr><tr><td>text</td><td><p>string</p></td><td><div><p>生成内容</p></div></td><td><p>xx</p></td></tr><tr><td>reasonText</td><td><p>string</p></td><td><div><p>模型思考过程</p></div></td><td><p>xx</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>用量</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>1</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 token 数</p></div></td><td><p>1</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 token</p></div></td><td><p>2</p></td></tr><tr><td>videoRoleRecognitionResult</td><td><p>object</p></td><td><div><p>自动识别结果</p></div></td><td></td></tr><tr><td>videoRoles</td><td><p>array&lt;object&gt;</p></td><td><div><p>角色列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td>roleName</td><td><p>string</p></td><td><div><p>角色名称</p></div></td><td><p>xx</p></td></tr><tr><td>roleInfo</td><td><p>string</p></td><td><div><p>人物信息</p></div></td><td><p>xx</p></td></tr><tr><td>timeIntervals</td><td><p>array&lt;object&gt;</p></td><td><div><p>角色出场时间段列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>startTime</td><td><p>integer</p></td><td><div><p>开始时间</p></div></td><td><p>0</p></td></tr><tr><td>endTime</td><td><p>integer</p></td><td><div><p>结束时间</p></div></td><td><p>342463553646</p></td></tr><tr><td>timestamp</td><td><p>integer</p></td><td><div><p>当前时间段角色出场时间</p></div></td><td><p>42553453253</p></td></tr><tr><td>url</td><td><p>string</p></td><td><div><p>角色图片</p></div></td><td><p>http://</p></td></tr><tr><td>ratio</td><td><p>number</p></td><td><div><p>出场率</p></div></td><td><p>0.2</p></td></tr><tr><td>isAutoRecognition</td><td><p>boolean</p></td><td><div><p>自动识别是否使用的是自动识别单独的视频地址（是：则人脸图片无法使用时间与视频帧用时间对应，因为可能是不同的视频）</p></div></td><td></td></tr><tr><td>videoCalculatorResult</td><td><p>object</p></td><td><div><p>费用估算结果</p></div></td><td></td></tr><tr><td>items</td><td><p>array&lt;object&gt;</p></td><td><div><p>计费项明细</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>计费项明细</p></div></td><td></td></tr><tr><td>name</td><td><p>string</p></td><td><div><p>计费项名称</p></div></td><td><p>xxx</p></td></tr><tr><td>type</td><td><p>string</p></td><td><div><p>类型</p></div></td><td><p>token</p></td></tr><tr><td>inputToken</td><td><p>integer</p></td><td><div><p>输入 token</p></div></td><td><p>1</p></td></tr><tr><td>outputToken</td><td><p>integer</p></td><td><div><p>输出 token</p></div></td><td><p>1</p></td></tr><tr><td>time</td><td><p>integer</p></td><td><div><p>计费时长</p></div></td><td><p>1</p></td></tr><tr><td>inputExpense</td><td><p>number</p></td><td><div><p>输入 token 计费</p></div></td><td><p>1</p></td></tr><tr><td>outputExpense</td><td><p>number</p></td><td><div><p>输入 token 计费</p></div></td><td><p>1</p></td></tr><tr><td>timeExpense</td><td><p>number</p></td><td><div><p>输出 token 计费</p></div></td><td><p>1</p></td></tr><tr><td>totalExpense</td><td><p>number</p></td><td><div><p>费用</p></div></td><td><p>0.098</p></td></tr><tr><td>addDatasetDocumentsResult</td><td><p>object</p></td><td><div><p>自动保存执行结果</p></div></td><td></td></tr><tr><td>status</td><td><p>integer</p></td><td><div><p>自动保存任务状态：1 成功，0 失败</p></div></td><td><p>1</p></td></tr><tr><td>title</td><td><p>string</p></td><td><div><p>视频名称</p></div></td><td><p>xx</p></td></tr><tr><td>docId</td><td><p>string</p></td><td><div><p>视频 docId</p></div></td><td><p>xxx</p></td></tr><tr><td>errorMessage</td><td><p>string</p></td><td><div><p>如果自动保存失败，则输出错误信息</p></div></td><td><p>xx</p></td></tr><tr><td>docUuid</td><td><p>string</p></td><td><div><p>视频的 docUuid</p></div></td><td><p>xxx</p></td></tr><tr><td>usage</td><td><p>object</p></td><td><div><p>token 描述</p></div></td><td></td></tr><tr><td>inputTokens</td><td><p>integer</p></td><td><div><p>输入 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>outputTokens</td><td><p>integer</p></td><td><div><p>输出 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>totalTokens</td><td><p>integer</p></td><td><div><p>总 Token 数量</p></div></td><td><p>0</p></td></tr><tr><td>taskRunInfo</td><td><p>object</p></td><td><div><p>运行信息</p></div></td><td></td></tr><tr><td>concurrentChargeEnable</td><td><p>boolean</p></td><td><div><p>是否使用付费并发：true 时，按照实际运行时长计量</p></div></td><td><p>true</p></td></tr><tr><td>responseTime</td><td><p>integer</p></td><td><div><p>运行时长：从任务被调度开始到任务完成的耗时，单位毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>taskStatus</td><td><p>string</p></td><td><div><p>任务状态：代表任务调度执行状态，如果任务状态 SUCCESSED，请查看 event 字段取真实业务状态。</p><ul><li><p>PENDING：待执行</p></li><li><p>RUNNING：执行中</p></li><li><p>SUCCESSED：成功</p></li><li><p>SUSPENDED：暂停</p></li><li><p>FAILED：失败</p></li><li><p>CANCELED： 取消</p></li></ul></div></td><td><p>SUCCESSED</p></td></tr><tr><td>taskId</td><td><p>string</p></td><td><div><p>任务 ID</p></div></td><td><p>3feb69ed02d9b1a17d0f1a942675d300</p></td></tr><tr><td>errorMessage</td><td><p>string</p></td><td><div><p>异常错误信息</p></div></td><td><p>Access was denied, message: No such namespace namespaces/mjp-test-default.</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "requestId": "5D0E915E-655D-59A8-894F-93873F73AAE5",
  "code": "successful",
  "message": "success",
  "httpStatusCode": 200,
  "success": true,
  "data": {
    "header": {
      "errorCode": "ERR-00000000",
      "errorMessage": "url download error: http://xx",
      "event": "task-finshed",
      "eventInfo": "url download error: http://xx",
      "sessionId": "d5c38cf6-a4bf-4a57-a697-9f449926f0c9",
      "taskId": "6e223291-729b-4e84-9271-c13ada1a776b",
      "traceId": "215045f817272303448235204efdef"
    },
    "payload": {
      "output": {
        "videoAnalysisResult": {
          "generateFinished": true,
          "text": "xxx",
          "usage": {
            "inputTokens": 0,
            "outputTokens": 0,
            "totalTokens": 0,
            "imageTokens": 1
          },
          "videoShotAnalysisResults": [
            {
              "endTime": 10000,
              "startTime": 1000,
              "text": "xxxx"
            }
          ]
        },
        "videoCaptionResult": {
          "generateFinished": true,
          "videoCaptions": [
            {
              "endTime": 20000,
              "endTimeFormat": "00:01",
              "startTime": 1000,
              "startTimeFormat": "00:01",
              "text": "xxxx",
              "speaker": "张三"
            }
          ]
        },
        "videoGenerateResult": {
          "generateFinished": true,
          "text": "xxx",
          "usage": {
            "inputTokens": 1,
            "outputTokens": 1,
            "totalTokens": 2
          },
          "modelId": "qwen-max-latest",
          "modelReduce": true,
          "reasonText": "xx",
          "index": 1
        },
        "videoMindMappingGenerateResult": {
          "generateFinished": true,
          "text": "小吃街",
          "usage": {
            "inputTokens": 1,
            "outputTokens": 1,
            "totalTokens": 2
          },
          "videoMindMappings": [
            {
              "childNodes": [
                {
                  "childNodes": [
                    {
                      "name": "三级节点"
                    }
                  ],
                  "name": "二级节点"
                }
              ],
              "name": "三级节点"
            }
          ]
        },
        "videoTitleGenerateResult": {
          "generateFinished": true,
          "text": "xxxx",
          "usage": {
            "inputTokens": 0,
            "outputTokens": 0,
            "totalTokens": 0
          }
        },
        "resultJsonFileUrl": "http://xxx",
        "videoGenerateResults": [
          {
            "generateFinished": true,
            "modelId": "xx",
            "index": 1,
            "text": "xx",
            "reasonText": "xx",
            "usage": {
              "inputTokens": 1,
              "outputTokens": 1,
              "totalTokens": 2
            }
          }
        ],
        "videoRoleRecognitionResult": {
          "videoRoles": [
            {
              "roleName": "xx",
              "roleInfo": "xx",
              "timeIntervals": [
                {
                  "startTime": 0,
                  "endTime": 342463553646,
                  "timestamp": 42553453253,
                  "url": "http://"
                }
              ],
              "ratio": 0.2,
              "isAutoRecognition": true
            }
          ]
        },
        "videoCalculatorResult": {
          "items": [
            {
              "name": "xxx",
              "type": "token",
              "inputToken": 1,
              "outputToken": 1,
              "time": 1,
              "inputExpense": 1,
              "outputExpense": 1,
              "timeExpense": 1,
              "totalExpense": 0.098
            }
          ]
        },
        "addDatasetDocumentsResult": {
          "status": 1,
          "title": "xx",
          "docId": "xxx",
          "errorMessage": "xx",
          "docUuid": "xxx"
        }
      },
      "usage": {
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0
      }
    },
    "taskRunInfo": {
      "concurrentChargeEnable": true,
      "responseTime": 1000
    },
    "taskStatus": "SUCCESSED",
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300",
    "errorMessage": "Access was denied, message: No such namespace namespaces/mjp-test-default."
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action , Please check the assignment of the workspaceId. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisTask#workbench-doc-change-demo)。
