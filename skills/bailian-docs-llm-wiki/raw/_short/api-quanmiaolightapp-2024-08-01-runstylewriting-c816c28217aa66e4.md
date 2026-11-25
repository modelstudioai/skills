# RunStyleWriting

传媒/零售文章风格与格式学习。

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
| quanmiaolightapp:RunStyleWriting | none | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/quanmiao/lightapp/runStyleWriting HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | [业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | llm-2setzb9xb8mx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>learningSamples</td><td><p>array</p></td><td><p>否</p></td><td><div><p>需要作为学习样本的文章集合</p></div></td><td><p>[&quot;在这个快节奏的时代，文字似乎成了慢生活的奢侈品。但你是否还记得，那些温柔的字句是如何悄悄潜入心田，激荡起久违的涟漪？今天，就让我们一同走进【妙笔写作】的世界，探索那些让文字跃然纸上的秘密，让灵感在指尖轻轻舞动，绽放独一无二的光彩。 &quot;]</p></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>需要作为学习样本的文章</p></div></td><td><p>在这个快节奏的时代，文字似乎成了慢生活的奢侈品。但你是否还记得，那些温柔的字句是如何悄悄潜入心田，激荡起久违的涟漪？今天，就让我们一同走进【妙笔写作】的世界，探索那些让文字跃然纸上的秘密，让灵感在指尖轻轻舞动，绽放独一无二的光彩。</p></td></tr><tr><td>writingTheme</td><td><p>string</p></td><td><p>否</p></td><td><div><p>用户输入的写作主题，可以对主题进行自定义调整效果</p></div></td><td><p>帮我写一篇关于妙笔产品等文案</p></td></tr><tr><td>styleFeature</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文体特征标识符。如果指定了此参数，接口会按照指定的文体特征进行写作</p></div></td><td><p>文章特点1：标题采用话题标签形式，增强社交媒体传播性。\n文章特点2：开篇通过引言简述背景，快速关联当下热点话题。\n文章特点3：使用记者调查作为支撑，列举具体行业实例，增强论述的现实基础。\n文章特点4：引入法律观点平衡论述，提供政策依据，并倡导正面价值观。\n\n示例文章特点总结：该文以社会热点为导向，运用具有传播力的标题设计，通过现象观察引入话题，结合实地调查数据展现广泛的社会现象，同时援引法律规定进行评析，确保论述客观性，并在结尾处倡导积极健康的职场文化，整体结构紧凑，信息丰富且具有引导性。</p></td></tr><tr><td>referenceMaterials</td><td><p>array</p></td><td><p>否</p></td><td><div><p>大模型生成功能的内容素材模型集合</p></div></td><td><p>是否还记得，那些温柔的字句是如何悄悄潜入心田，激荡起久违的涟漪？今天，就让我们一同走进【妙笔写作】的世界，探索那些让文字跃然纸上的秘密，让灵感在指尖轻轻舞动，绽放独一无二的光彩。 &quot;]</p></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>大模型生成功能的内容素材</p></div></td><td><p>在这个快节奏的时代，文字似乎成了慢生活的奢侈品。但你是否还记得，那些温柔的字句是如何悄悄潜入心田，激荡起久违的涟漪？今天，就让我们一同走进【妙笔写作】的世界，探索那些让文字跃然纸上的秘密，让灵感在指尖轻轻舞动，绽放独一无二的光彩。</p></td></tr><tr><td>processStage</td><td><p>string</p></td><td><p>否</p></td><td><div><ul><li>代表处理阶段<ul><li><p>&quot;full&quot;: 生成特点分析和创作内容</p></li><li><p>&quot;analysisStage&quot;: 仅生成特点分析</p></li><li><p>&quot;creationStage&quot;: 仅生成创作内容</p></li></ul></li></ul></div></td><td></td></tr><tr><td>useSearch</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否自动检索互联网补充素材</p></div></td><td></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| end | boolean | 输出是否完成，true 表示完成 | true |
| header | object | 流式输出 header 头，包含返回通用信息 | {"event":"task-progress-start-generating","sessionId":"3cd10828-0e42-471c-8f1a-931cde20b035","taskId":"d3be9981-ca2d-4e17-bf31-1c0a628e9f99","traceId":"66bef4a7f5d61ff3c43f3b710574e175"} |
| errorCode | string | 异常错误码 | 403 |
| errorMessage | string | 异常错误信息 | Pop sign mismatch, please check log. |
| event | string | 事件类型 | task-progress-start-generating |
| eventInfo | string | 事件描述 | 模型生成事件 |
| requestId | string | 请求 ID | 0EB27AE3-CA53-5FAE-83C6-EE66CA4DF5DF |
| sessionId | string | 一次会话 ID | 3cd10828-0e42-471c-8f1a-931cde20b035 |
| taskId | string | 一次生成任务 ID | d3be9981-ca2d-4e17-bf31-1c0a628e9f99 |
| traceId | string | 链路 traceid | 2150451a17191950923411783e2927 |
| payload | object | 返回结果的 payload,json 结构，不同 event 结构不同 | { "output": { "text": "这是测试输出" }, "usage": { "inputTokens": 1816, "outputTokens": 96, "totalTokens": 1912 } } |
| output | object | 输出内容对象 | { "text": "这是测试输出" } |
| text | string | 输出内容 | 这是测试输出 |
| usage | object | 大模型 token 用量信息 | { "inputTokens": 1816, "outputTokens": 96, "totalTokens": 1912 } |
| inputTokens | integer | 输入 Token 数量 | 100 |
| outputTokens | integer | 输出 Token 数量 | 100 |
| totalTokens | integer | 总 oken 数量 | 200 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "end": true,
  "header": {
    "errorCode": "403",
    "errorMessage": "Pop sign mismatch, please check log.",
    "event": "task-progress-start-generating",
    "eventInfo": "模型生成事件",
    "requestId": "0EB27AE3-CA53-5FAE-83C6-EE66CA4DF5DF",
    "sessionId": "3cd10828-0e42-471c-8f1a-931cde20b035",
    "taskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "traceId": "2150451a17191950923411783e2927"
  },
  "payload": {
    "output": {
      "text": "这是测试输出"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunStyleWriting#workbench-doc-change-demo)。
