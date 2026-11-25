# SubmitEssayCorrectionTask

提交作文批改任务。

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
| quanmiaolightapp:SubmitEssayCorrectionTask | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/quanmiao/lightapp/submitEssayCorrectionTask HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | [业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | xxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>tasks</p></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><p>批改任务列表</p></td><td><p>[{&quot;grade&quot;: &quot;高中二年级&quot;, &quot;subject&quot;: &quot;语文&quot;, &quot;totalScore&quot;: 60, &quot;question&quot;: &quot;请以我的梦想为主题写一篇作文&quot;, &quot;answer&quot;: &quot;我的梦想是成为一名科学家...&quot;, &quot;customId&quot;: &quot;task-001&quot;}]</p></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>子任务</p></td><td></td></tr><tr><td><p>grade</p></td><td><p>string</p></td><td><p>否</p></td><td><p>年级，可选值有： [ &quot;初中一年级&quot;, &quot;初中二年级&quot;, &quot;初中三年级&quot;, &quot;高中一年级&quot;, &quot;高中二年级&quot;, &quot;高中三年级&quot; ]</p></td><td><p>高中二年级</p></td></tr><tr><td><p>subject</p></td><td><p>string</p></td><td><p>否</p></td><td><p>科目，可选值有：[ &quot;语文&quot;, &quot;英语应用文&quot;, &quot;英语读后续写&quot; ]</p></td><td><p>语文</p></td></tr><tr><td><p>totalScore</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>总分</p></td><td><p>60</p></td></tr><tr><td><p>question</p></td><td><p>string</p></td><td><p>否</p></td><td><p>作文题目</p></td><td><p>xxx</p></td></tr><tr><td><p>answer</p></td><td><p>string</p></td><td><p>否</p></td><td><p>作文回答</p></td><td><p>xxx</p></td></tr><tr><td><p>otherReviewPoints</p></td><td><p>string</p></td><td><p>否</p></td><td><p>其他审阅要点</p></td><td><p>xxx</p></td></tr><tr><td><p>customId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>用户自定义 ID。用来唯一标识每个任务，不能重复</p></td><td><p>xxxxx</p></td></tr><tr><td><p>grade</p></td><td><p>string</p></td><td><p>否</p></td><td><p>年级（公共值，优先取子任务中的 grade）</p></td><td><p>高中二年级</p></td></tr><tr><td><p>subject</p></td><td><p>string</p></td><td><p>否</p></td><td><p>科目（公共值，优先取子任务中的 subject）</p></td><td><p>语文</p></td></tr><tr><td><p>totalScore</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>总分（公共值，优先取子任务中的 totalScore）</p></td><td><p>60</p></td></tr><tr><td><p>question</p></td><td><p>string</p></td><td><p>否</p></td><td><p>作文题目（公共值，优先取子任务中的 question）</p></td><td><p>xxx</p></td></tr><tr><td><p>otherReviewPoints</p></td><td><p>string</p></td><td><p>否</p></td><td><p>其他评阅要点（公共值，优先取子任务中的 otherReviewPoints ）</p></td><td><p>xxx</p></td></tr><tr><td><p>modelId</p></td><td><p>string</p></td><td><p>否</p></td><td><p>模型 ID</p><p>可参考模型列表如下：</p><a id="code-block-2"></a><pre class="language-json"><code>
[
                    {
                        &quot;ModelName&quot;: &quot;自定义批改模型&quot;,
                        &quot;ModelId&quot;: &quot;qwen-custom-correction-v1&quot;
                    },
                    {
                        &quot;ModelName&quot;: &quot;作文批改模型 1&quot;,
                        &quot;ModelId&quot;: &quot;qwen-correction-v1&quot;
                    },
                    {
                        &quot;ModelName&quot;: &quot;作文批改轻量模型&quot;,
                        &quot;ModelId&quot;: &quot;qwen-correction-v1-lite&quot;
                    }
                ]
</code></pre></td><td><p>qwen-correction-v1</p></td></tr><tr><td><p>dimensions</p></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><p>自定义评分维度列表（仅 qwen-custom-correction-v1 模型支持）</p></td><td><p>[{&quot;name&quot;: &quot;内容完整度&quot;, &quot;rubric&quot;: &quot;文章内容是否完整，是否涵盖了题目的核心要求&quot;, &quot;maxScore&quot;: 30}]</p></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>自定义评分维度</p></td><td></td></tr><tr><td><p>name</p></td><td><p>string</p></td><td><p>否</p></td><td><p>维度名称</p></td><td><p>内容完整度</p></td></tr><tr><td><p>rubric</p></td><td><p>string</p></td><td><p>否</p></td><td><p>维度细则描述</p></td><td><p>文章内容是否完整，是否涵盖了题目的核心要求</p></td></tr><tr><td><p>maxScore</p></td><td><p>integer</p></td><td><p>否</p></td><td><p>维度满分</p></td><td><p>30</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PlainResult |  |
| code | string | 状态码 | NoData |
| httpStatusCode | integer | http 状态码 | 200 |
| message | string | 错误说明 | success |
| requestId | string | 请求唯一标识 | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| success | boolean | 是否成功：true 成功，false 失败 | true |
| data | object | 任务结果 |  |
| taskId | string | 任务 ID | 3feb69ed02d9b1a17d0f1a942675d300 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```json
{
  "code": "NoData",
  "httpStatusCode": 200,
  "message": "success",
  "requestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "success": true,
  "data": {
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitEssayCorrectionTask#workbench-doc-change-demo)。
