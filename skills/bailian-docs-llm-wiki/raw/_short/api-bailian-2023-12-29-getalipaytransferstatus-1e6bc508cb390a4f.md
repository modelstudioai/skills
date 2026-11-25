# GetAlipayTransferStatus - 查询支付宝打赏状态

查询应用中绑定的支付宝钱包的打赏状态。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/GetAlipayTransferStatus)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:GetAlipayTransferStatus</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /openapi/alipay/transfer/status HTTP/1.1
POST /openapi/alipay/transfer/status HTTP/1.1GET /openapi/alipay/transfer/status HTTP/1.1
POST /openapi/alipay/transfer/status HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspace\_id | string | 否 | 百炼工作空间 ID | llm-cxxxxxxb8d47ks |
| code | string | 否 | 支付宝打赏链接请求返回的打赏 code | xxx-xxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求的唯一 ID</p></div></td><td>6a71f2d9-f1c9-913b-818b-11402910xxxx</td></tr><tr><td>data</td><td>object</td><td><div><p>打赏的结果数据</p></div></td><td></td></tr><tr><td>code</td><td>string</td><td><div><p>打赏对应的 code</p></div></td><td>0</td></tr><tr><td>walletItemCode</td><td>string</td><td><div><p>支付宝商品钱包 code</p></div></td><td>xsdfsdf</td></tr><tr><td>mainAccountId</td><td>string</td><td><div><p>主账号 id（API 忽略）</p></div></td><td>1007576424487905</td></tr><tr><td>accountId</td><td>string</td><td><div><p>子账号 id（API 忽略）</p></div></td><td>1348393307144609</td></tr><tr><td>alipayOrderId</td><td>string</td><td><div><p>支付宝的订单 id</p></div></td><td>1234234</td></tr><tr><td>status</td><td>long</td><td><div><p>打赏状态</p><ul><li>1 （成功）</li><li>0 （删除）</li><li>2 （待打赏）</li><li>3 （取消）</li><li>4 （退款）</li><li>5（关闭）</li><li>6（失败）</li><li>7（纠纷、异常）</li></ul></div></td><td>1</td></tr><tr><td>creator</td><td>string</td><td><div><p>创建者（API 忽略）</p></div></td><td>234234</td></tr><tr><td>modifier</td><td>string</td><td><div><p>修改者（API 忽略）</p></div></td><td>234234</td></tr><tr><td>alipayOrderDetail</td><td>string</td><td><div><p>支付细节（API 忽略）</p></div></td><td>{}</td></tr><tr><td>title</td><td>string</td><td><div><p>转账标题</p></div></td><td>test</td></tr><tr><td>qrURL</td><td>string</td><td><div><p>打赏链接（API 忽略）</p></div></td><td><a href="https://xxx.aliyun.com">https://xxx.aliyun.com</a></td></tr><tr><td>transAmount</td><td>string</td><td><div><p>订单总金额，单位为：元。</p></div></td><td>0.22</td></tr><tr><td>scope</td><td>string</td><td><div><p>打赏应用的所属状态</p></div></td><td>publish</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "requestId": "6a71f2d9-f1c9-913b-818b-11402910xxxx\n",
  "data": {
    "code": 0,
    "walletItemCode": "xsdfsdf",
    "mainAccountId": 1007576424487905,
    "accountId": 1348393307144609,
    "alipayOrderId": 1234234,
    "status": 1,
    "creator": 234234,
    "modifier": 234234,
    "alipayOrderDetail": {},
    "title": "test",
    "qrURL": "https://xxx.aliyun.com",
    "transAmount": 0.22,
    "scope": "publish"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。
