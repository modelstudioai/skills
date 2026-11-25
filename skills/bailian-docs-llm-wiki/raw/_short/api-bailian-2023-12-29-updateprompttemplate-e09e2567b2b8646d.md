# UpdatePromptTemplate - 更新Prompt模板

基于模板Id增量更新Prompt模板。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/UpdatePromptTemplate)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:UpdatePromptTemplate</td><td>update</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
PATCH /{workspaceId}/promptTemplates/{promptTemplateId} HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 Id | llm-us9hjmt32nysdxxx |
| promptTemplateId | string | 是 | prompt 模板 Id | 6e49109bfeb94a39bb268f4e483ccxxx |
| name | string | 否 | 模板名称 | 小红书文案助手 |
| content | string | 否 | prompt 模板内容 | 请写一篇小红书种草笔记，增加丰富的emoji元素，结尾作总结，并加上相关标签。主题为：${theme} |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| requestId | string | 请求 Id | FE9B6CBF-47E6-5D76-9C5D-B814DD5ABxxx |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "requestId": "FE9B6CBF-47E6-5D76-9C5D-B814DD5ABxxx\n"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | PromptTemplate.ContentInvalid | Input parameter Content is invalid. | 入参Content的格式无效。 |
| 400 | PromptTemplate.NameInvalid | Input parameter Name is invalid. | 输入参数Name的格式无效。 |
| 404 | PromptTemplate.TemplateNotFound | Prompt template not found. | 未找到Prompt模板 |
| 500 | PromptTemplate.InternalError | Prompt template service inner exception. | prompt模板服务内部异常 |

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。
