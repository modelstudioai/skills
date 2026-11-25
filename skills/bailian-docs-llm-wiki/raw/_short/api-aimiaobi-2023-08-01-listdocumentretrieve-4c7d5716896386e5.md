# ListDocumentRetrieve

根据复杂条件进行政务公文库的检索。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](iframe-embedding-scheme-6f73b86f9f7bdf41.md)

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
| aimiaobi:ListDocumentRetrieve | list | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST  HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td><p>llm-</p></td></tr><tr><td>MaxResults</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>最大返回结果数</p></div></td><td><p>94</p></td></tr><tr><td>NextToken</td><td><p>string</p></td><td><p>否</p></td><td><div><p>下一页的 token</p></div></td><td><p>cEoBWREAXdxaOyjq/cqAbg==</p></td></tr><tr><td>Query</td><td><p>string</p></td><td><p>否</p></td><td><div><p>搜索条件</p></div></td><td><p>检索Query</p></td></tr><tr><td>ContentType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章体裁，0（null）:全部(默认值), 1：公文，2：重要文章 5:政策解读 6：法律条文 7：规章法规 8：总书记</p></div></td><td><p>1</p></td></tr><tr><td>SubContentType</td><td><p>string</p></td><td><p>否</p></td><td><div><ul><li>文章体裁二级分类，文章体裁为总书记时：1：动态 2：讲话 3：思想 4：理论<ul><li><p>文章体裁为公文时：-1： 其他 0：决议 1：决定 2：令 3：公报 4：公告 5：通告 6：意见 7：通知 8：通报 9：报告 10：请示 11：批复 12： 议案 13：函</p></li><li><p>14： 纪要</p></li><li><p>文章体裁为重要文章时：1：重要评论 2：重要理论 3：其他文章</p></li><li><p>文章体裁为规章法规时：3：行政法规 4：监察法规 5：地方性法规 7：部门规章 8：其他 9：党章党规</p></li><li><p>文章体裁为法律条文时：1：宪法 2：法律 6：司法解释</p></li></ul></li></ul></div></td><td><p>1</p></td></tr><tr><td>Region</td><td><p>string</p></td><td><p>否</p></td><td><div><p>区域 可直接输入 省 或者市 如吉林省 或者北京市</p></div></td><td><p>北京市</p></td></tr><tr><td>Source</td><td><p>string</p></td><td><p>否</p></td><td><div><p>来源，0：内部（本单位） 1：外部（外单位）</p></div></td><td><p>1</p></td></tr><tr><td>StartDate</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发文起始时间，yyyy-MM-dd</p></div></td><td><p>2025-10-10</p></td></tr><tr><td>EndDate</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发文结束时间，yyyy-MM-dd</p></div></td><td><p>2025-07-03</p></td></tr><tr><td>Office</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发文单位</p></div></td><td><p>国务院办公室</p></td></tr><tr><td>WordSize</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发文字号</p></div></td><td><p>宁民规〔2020〕5号</p></td></tr><tr><td>ElementScope</td><td><p>string</p></td><td><p>否</p></td><td><div><p>检索要素范围，1:标题 0:全文(标题和内容)，默认</p></div></td><td><p>0</p></td></tr><tr><td>SubjectClassify</td><td><p>string</p></td><td><p>否</p></td><td><div><p>支持如下分类</p><table><thead><tr><th>一级分类</th><th>二级分类</th></tr></thead><tbody><tr><td>国防和交流合作事务</td><td>国防, 对外事务, 军事工作, 港澳台侨工作</td></tr><tr><td>综合政务</td><td>二十大, 政务公开与督查, 联合政务, 党建工作, 会议及提案, 政务文件管理, 其他政务</td></tr><tr><td>国务院组织机构</td><td>国务院, 国务院办公厅, 国务院机构</td></tr><tr><td>行政监管与市场监管</td><td>行政监管, 信用监管, 产品质量监督, 安全生产监管, 市场监管</td></tr><tr><td>经济管理</td><td>国民经济, 市场经济, 经济体制改革, 国有资产监管</td></tr><tr><td>财政金融商贸</td><td>财政, 金融, 审计, 商贸, 海关</td></tr><tr><td>人事工作与社会保障</td><td>人事工作, 人口与计划生育, 妇女儿童工作, 扶贫, 减灾救灾, 公共服务, 社会福利与救助, 优抚安置, 社会保障</td></tr><tr><td>公共安全与社会管理</td><td>公安, 安全, 司法, 消防, 民族, 宗教</td></tr><tr><td>科教文体</td><td>文化, 科技创新, 教育, 知识产权, 新闻出版, 广电与互联网, 体育, 旅游</td></tr><tr><td>医疗卫生</td><td>卫生, 医疗, 动物医学</td></tr><tr><td>城乡建设与工业发展</td><td>城乡建设, 工业, 交通</td></tr><tr><td>自然资源与环境保护</td><td>国土资源、能源, 土木, 气象, 环境保护</td></tr><tr><td>农林水渔牧类</td><td>农业, 林业, 水利, 渔业, 畜牧业</td></tr><tr><td>其他</td><td>其他</td></tr></tbody></table></div></td><td><p>国防和交流合作事务</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| Code | string | 状态码 | successful |
| Data | array<object> | 业务数据 | data |
|  | object | 业务数据 |  |
| Title | string | 标题 | 文章标题 |
| Essay | string | 正文 | 文章正文 |
| Link | string | 链接 | 文章链接 |
| IssuingAuthority | string | 发布机构 | 发布机构 |
| PublicationDate | string | 发布日期 | 2023-02-01 |
| HttpStatusCode | integer | http 状态码 | 200 |
| MaxResults | integer | 返回的最大记录数 | 71 |
| Message | string | 错误说明 | success |
| NextToken | string | 下一页 Token | cEoBWREAXdxaOyjq/cqAbg== |
| RequestId | string | Id of the request | F2F366D6-E9FE-1006-BB70-2C650896AAB5 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |
| TotalCount | integer | 总数 | 100 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Code": "successful",
  "Data": [
    {
      "Title": "文章标题",
      "Essay": "文章正文",
      "Link": "文章链接",
      "IssuingAuthority": "发布机构",
      "PublicationDate": "2023-02-01"
    }
  ],
  "HttpStatusCode": 200,
  "MaxResults": 71,
  "Message": "success",
  "NextToken": "cEoBWREAXdxaOyjq/cqAbg==",
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "Success": true,
  "TotalCount": 100
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDocumentRetrieve#workbench-doc-change-demo)。
