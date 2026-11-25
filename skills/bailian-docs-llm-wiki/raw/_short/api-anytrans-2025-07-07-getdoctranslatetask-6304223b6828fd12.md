# GetDocTranslateTask - 文档翻译结果获取

通义多模态翻译获取文档翻译结果

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

文档翻译结果查询接口

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AnyTrans/2025-07-07/GetDocTranslateTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>anytrans:GetDocTranslateTask</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /anytrans/translate/doc/get HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 当前请求所使用的百炼业务空间 id | llm-kqtrcpdee4xm29xx |
| taskId | string | 是 | 文档翻译任务 id | d3a2397bc2c14ab4a2e40a4f5b46241b |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>code</td><td>string</td><td><div><p>响应状态码</p></div></td><td>success</td></tr><tr><td>message</td><td>string</td><td><div><p>响应消息</p></div></td><td>success</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id，用于追溯 API 调用链路</p></div></td><td>AC642EEB-C29D-54DF-8F52-622565BBB78A</td></tr><tr><td>success</td><td>boolean</td><td><div><p>接口调用是否成功</p></div></td><td>true</td></tr><tr><td>httpStatusCode</td><td>string</td><td><div><p>http 响应码</p></div></td><td>200</td></tr><tr><td>data</td><td>object</td><td><div><p>返回数据</p></div></td><td></td></tr><tr><td>taskId</td><td>string</td><td><div><p>文档翻译任务 id</p></div></td><td>d3a2397bc2c14ab4a2e40a4f5b46241b</td></tr><tr><td>status</td><td>string</td><td><div><p>翻译状态</p></div><div><div>枚举值：</div><ul><li>translating：翻译中。</li><li>translated：翻译完成。</li></ul></div></td><td>translated</td></tr><tr><td>charactersCount</td><td>integer</td><td><div><p>字符统计</p></div></td><td>4</td></tr><tr><td>pageCount</td><td>integer</td><td><div><p>页数统计</p></div></td><td>2</td></tr><tr><td>translateFileUrl</td><td>string</td><td><div><p>翻译结果 URL</p></div></td><td><a href="http://translate-ai-data-dev.oss-cn-hangzhou.aliyuncs.com/tongyiTranslate/123456789/a7630164ce894c799cca0f0822c36f84_merge.md">http://translate-ai-data-dev.oss-cn-hangzhou.aliyuncs.com/tongyiTranslate/123456789/a7630164ce894c799cca0f0822c36f84_merge.md</a></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "code": "success",
  "message": "success",
  "requestId": "AC642EEB-C29D-54DF-8F52-622565BBB78A",
  "success": true,
  "httpStatusCode": 200,
  "data": {
    "taskId": "d3a2397bc2c14ab4a2e40a4f5b46241b",
    "status": "translated",
    "charactersCount": 4,
    "pageCount": 2,
    "translateFileUrl": "http://translate-ai-data-dev.oss-cn-hangzhou.aliyuncs.com/tongyiTranslate/123456789/a7630164ce894c799cca0f0822c36f84_merge.md"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 |
| --- | --- | --- |
| 400 | IdempotentParameterMismatch | The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical. |

访问[错误中心](https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |

暂无变更历史
