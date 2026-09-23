# 析言GBI最佳实践

本文基于析言GBI的API实现了智能数据问答功能。旨在帮助您快速熟悉API的使用，以便在实际项目中灵活运用API。

## 前提条件

-   已开通阿里云百炼。
-   已获取WorkspaceID：[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
-   已获取AccessKey ID和AccessKey Secret：[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
-   RAM用户已添加`AliyunDataAnalysisGBIFullAccess`权限策略：[管理RAM用户的权限](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
-   已在析言GBI的**[数据表管理](https://bailian.console.aliyun.com/xiyan#/dataManagement/dataSourceM)**中授权联接了数据库。具体操作，请参见[数据库连接](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#8e5d17697392b)。

## 操作步骤

#### Java

#### 步骤1：安装析言GBI的JavaSDK

1.  获取析言GBI [Java SDK](https://api.aliyun.com/api-tools/sdk/DataAnalysisGBI?version=2024-08-23&language=java-async-tea&tab=primer-doc)最新版本号。
2.  打开您的Maven项目的`pom.xml`文件。
3.  在`<dependencies>`标签内添加以下依赖信息，并将`<version></version>`标签中的版本号替换为最新的版本号。

```
<dependency>
            <groupId>com.aliyun</groupId>
            <artifactId>alibabacloud-dataanalysisgbi20240823</artifactId>
            <version>1.0.0</version>
        </dependency>
```

4.  保存`pom.xml`文件。
5.  更新项目依赖，将SDK添加到您的项目中。

#### 步骤2：实现智能数据问答功能

基于析言GBI的[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)（例如：本示例中的`RunDataAnalysisRequest`类），通过实现智能数问场景来帮助您熟悉API的使用。

请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码正常运行并返回正确的结果。

```
package com.alibaba.iic.llmsolution.gbi.util;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.dataanalysisgbi20240823.AsyncClient;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunDataAnalysisRequest;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunDataAnalysisResponseBody;
import com.google.gson.Gson;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

public class CommonExample {
    public static void main(String[] args) throws Exception {

        StaticCredentialProvider provider = StaticCredentialProvider.create(
                Credential.builder()
                        .accessKeyId("accessKeyId")
                        .accessKeySecret("accessKeySecret")
                        .build()
        );

        AsyncClient client = AsyncClient.builder()
                .region("cn-beijing")
                .credentialsProvider(provider)
                .serviceConfiguration(Configuration.create()
                        .setSignatureVersion(SignatureVersion.V3)
                )
                .overrideConfiguration(
                        ClientOverrideConfiguration.create()
                                .setProtocol("HTTPS")
                                .setEndpointOverride("dataanalysisgbi.cn-beijing.aliyuncs.com")
                )
                .build();
        // 进行对话分析时，整体的参数控制
        RunDataAnalysisRequest request = RunDataAnalysisRequest.builder()
                // 当前对话请求所使用的业务空间id
                .workspaceId("workspaceId")
                // 当前对话请求的用户问题
                .query("查询销量最高的五个产品")
                // 当前对话请求所希望使用的版本，如未购买所指定的版本则会使用默认业务空间的版本
                .specificationType("STANDARD_MIX")
                // 当前对话请求是否只生成sql,跳过后续的可视化模块
                .generateSqlOnly(true)
                .build();

        // 获取流式内容，并进行解析处理
        ResponseIterable<RunDataAnalysisResponseBody> x = client.runDataAnalysisWithResponseIterable(request);
        ResponseIterator<RunDataAnalysisResponseBody> iterator = x.iterator();
        while (iterator.hasNext()) {
            RunDataAnalysisResponseBody event = iterator.next();
            System.out.println(new Gson().toJson(event.getData()));
            // sql_part为sql流式输出事件，流式获取生成的sql内容
            if (event.getData().getEvent().equals("sql_part")) {
                System.out.println(event.getData().getSql());
            }
            // sql为最终的sql生成事件，非流式，直接获取最终sql
            if (event.getData().getEvent().equals("sql")) {
                System.out.println(event.getData().getSql());
            }
            // 当前请求的结果中,包含可视化模型执行结果，可进行渲染
            if (event.getData().getVisualization() != null) {
                System.out.println("当前对话分析内容，包含可视化模块内容，可进行渲染");
            }
        }
        System.out.println("ALL***********************");
        System.out.println("请求成功的请求头值：");
        System.out.println(x.getStatusCode());
        System.out.println(x.getHeaders());
    }

}
```

#### 返回结果示例

参数说明请参见[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)的**返回参数**。

```
{"event":"rewrite","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6"}
{"event":"selector","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6"}
{"event":"evidence","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"]}
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"sql"}
sql
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":""}

{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT"}
SELECT
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity)"}
SELECT p.product_name, SUM(o.quantity)
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales "}
SELECT p.product_name, SUM(o.quantity) AS total_sales
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p "}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON"}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d"}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id =
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id "}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product"}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY"}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product_name ORDER BY
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sales DESC "}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product_name ORDER BY total_sales DESC
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 5; "}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 5;
{"event":"sql_part","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 5; "}
SELECT p.product_name, SUM(o.quantity) AS total_sales FROM products p JOIN orders o ON p.product_id = o.product_id GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 5;
{"event":"sql","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales\nFROM products p\nJOIN orders o ON p.product_id \u003d o.product_id\nGROUP BY p.product_name\nORDER BY total_sales DESC\nLIMIT 5;\n"}
SELECT p.product_name, SUM(o.quantity) AS total_sales
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 5;

{"event":"sql_data","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales\nFROM products p\nJOIN orders o ON p.product_id \u003d o.product_id\nGROUP BY p.product_name\nORDER BY total_sales DESC\nLIMIT 5;\n","sqlData":{"column":["product_name","total_sales"],"data":[{"total_sales":"265","product_name":"丝巾"},{"total_sales":"197","product_name":"男士电动化妆刷套装"},{"total_sales":"158","product_name":"女士电动化妆刷套装"},{"total_sales":"157","product_name":"戒指"},{"total_sales":"136","product_name":"真皮皮包"}]}}
{"event":"result","evidence":"对于所有的指标（metric），如果没有对所有维度（dimension）都进行了限制，就要进行求和SUM再进行其他聚合或是筛选","requestId":"8499A3E6-C1B2-5D2E-845F-2F63F8795B4D","rewrite":"查询销量最高的五个产品及其销量","selector":["products","orders"],"sessionId":"8db26af8-721c-49bd-95f5-cceb0053ecf6","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sales\nFROM products p\nJOIN orders o ON p.product_id \u003d o.product_id\nGROUP BY p.product_name\nORDER BY total_sales DESC\nLIMIT 5;\n","sqlData":{"column":["product_name","total_sales"],"data":[{"total_sales":"265","product_name":"丝巾"},{"total_sales":"197","product_name":"男士电动化妆刷套装"},{"total_sales":"158","product_name":"女士电动化妆刷套装"},{"total_sales":"157","product_name":"戒指"},{"total_sales":"136","product_name":"真皮皮包"}]},"visualization":{"data":{"plotType":"bar","xAxis":["product_name"],"yAxis":["total_sales"]},"text":"销量最高的五个产品及其销量分别是：丝巾，总销量为265件；男士电动化妆刷套装，销量为197件；女士电动化妆刷套装，销量为158件；戒指，销量为157件；真皮皮包，销量为136件。"}}
ALL***********************
请求成功的请求头值：
200
{Transfer-Encoding=chunked, Keep-Alive=timeout=25, Access-Control-Expose-Headers=*, Access-Control-Allow-Origin=*, x-acs-request-id=8499A3E6-C1B2-5D2E-845F-2F63F8795B4D, Connection=keep-alive, Date=Thu, 14 Nov 2024 08:16:49 GMT, Content-Type=text/event-stream;charset=utf-8, x-acs-trace-id=26e2559443d87082911aa44f656072df}
```

如果未授权连接数据库，会返回以下结果：

```
{"errorMessage":"data source is empty","event":"error"}
ALL***********************
请求成功的请求头值：
200
{Transfer-Encoding=chunked, Keep-Alive=timeout=25, Access-Control-Expose-Headers=*, Access-Control-Allow-Origin=*, x-acs-request-id=CB1F6A3B-43DC-5D9D-8FDC-57A9474B0DF3, Connection=keep-alive, Date=Thu, 14 Nov 2024 06:20:33 GMT, Content-Type=text/event-stream;charset=utf-8, x-acs-trace-id=dfa7db76cf65dcc933292999274fa687}
```

#### Python

#### 步骤1：安装依赖

```
pip install alibabacloud-tea-openapi-sse==1.0.2
```

#### 步骤2：实现智能数据问答功能

基于析言GBI的[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)的API代码示例如下。

请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码正常运行并返回正确的结果。

```
from alibabacloud_tea_openapi_sse.client import Client as OpenApiClient
from alibabacloud_tea_openapi_sse import models as open_api_models
from alibabacloud_tea_util_sse import models as util_models
import asyncio
import json

class RunDataAnalysis:
    def __init__(self) -> None:
        self.endpoint = None
        self._client = None
        self._api_info = self._create_api_info()
        self._runtime = util_models.RuntimeOptions(read_timeout=1000 * 100)
        self._init_app()

    def _init_app(self):
        endpoint = 'dataanalysisgbi.cn-beijing.aliyuncs.com'
        access_key_id = '${access_key_id}'
        access_key_secret = '${access_key_secret}'
        assert endpoint is not None and access_key_id is not None and access_key_secret is not None

        self._client = self._create_client(access_key_id, access_key_secret, endpoint)

    def _create_client(
            self,
            access_key_id: str,
            access_key_secret: str,
            endpoint: str,
    ) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        config.endpoint = endpoint if endpoint is not None else 'dataanalysisgbi.cn-beijing.aliyuncs.com'
        return OpenApiClient(config)

    def _create_api_info(self) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称
            action='RunDataAnalysis',
            # 接口版本
            version='2024-08-23',
            # 接口协议
            protocol='HTTPS',
            # 接口 HTTP 方法
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname='/${workspaceId}/gbi/runDataAnalysis',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='sse'
        )
        return params

    async def do_sse_query(self, query: str):
        assert self._client is not None
        assert isinstance(query, str), '"query" is mandatory and should be str'

        body = {
            'specificationType': 'STANDARD_MIX',
            'query': query,
        }
        request = open_api_models.OpenApiRequest(
            body=body
        )
        sse_receiver = self._client.call_sse_api_async(params=self._api_info, request=request, runtime=self._runtime)
        return sse_receiver

# 模型初始化

async def query():
    xiyan_gbi = RunDataAnalysis()
    frame_count = 0
    async for res in await xiyan_gbi.do_sse_query('查询全部关键字数据，并用饼图展示'):
        try:
            data = json.loads(res.get('event').data)
            print(data)
        except json.JSONDecodeError:
            print('------json.JSONDecodeError--------')
            print(res.get('headers'))
            print(res.get('event').data)
            print('------json.JSONDecodeError-end--------')
            continue
    print('------end--------')

if __name__ == '__main__':
    asyncio.run(query())
```

#### 返回结果示例

参数说明请参见[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)的**返回参数**。

```
{'data': {'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'sessionId': '10148716_1f8ebf09-df4b-4b0c-9493-66a1895a9ba4', 'event': 'rewrite', 'rewrite': '查询user表中的全部数据，并用饼图展示'}}
{'data': {'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-df4b-4b0c-9493-66a1895a9ba4', 'event': 'selector', 'rewrite': '查询er表中的全部数据，并用饼图展示'}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'selector': ['user'], 'event': 'evidence', 'rewrite': '查询user表中的全部数据，并用饼图展示'}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-5a9ba4', 'event': 'sql_part', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': ''}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-5a9ba4', 'event': 'sql_part', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select *'}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-5a9ba4', 'event': 'sql_part', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select * from user '}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-5a9ba4', 'event': 'sql_part', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select * from user '}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sessionId': '10148716_1f8ebf09-5a9ba4', 'event': 'sql', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select * from user\n'}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sqlData': {}, 'sessionId': '101b0c-9493-66a1895a9ba4', 'event': 'sql_data', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select * from user\n'}}
{'data': {'evidence': 'KKK是指客单价。KKK=总销售额/订单总数，保留2位小数。', 'requestId': '93DE1D26-153E-5386-BA8F-9D2E2F8B3381', 'selector': ['user'], 'sqlData': {}, 'sessionId': '101b0c-9493-66a1895a9ba4', 'event': 'result', 'rewrite': '查询user表中的全部数据，并用饼图展示', 'sql': 'select * from user\n'}}
------end--------
```

#### Go

#### 步骤1：安装依赖

在Go项目的go.mod文件中添加以下信息，指定依赖的模块路径和版本号。

```
go 1.16

require (
	github.com/alibabacloud-go/darabonba-openapi/v2 v2.1.2 // indirect
	github.com/alibabacloud-go/openapi-util v0.1.1 // indirect
	github.com/alibabacloud-go/tea v1.3.2 // indirect
	github.com/alibabacloud-go/tea-utils/v2 v2.0.7 // indirect
)
```

#### 步骤2：实现智能数据问答功能

基于析言GBI的[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)的API代码示例如下。

请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码正常运行并返回正确的结果。

```
// This file is auto-generated, don't edit it. Thanks.
package main

import (
	"fmt"
	"io"
	"os"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	openapiutil "github.com/alibabacloud-go/openapi-util/service"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

/**
 * API 相关
 * @param path params
 * @return OpenApi.Params
 */
func CreateApiInfo() (_result *openapi.Params) {
	params := &openapi.Params{
		// 接口名称
		Action: tea.String("RunDataAnalysis"),
		// 接口版本
		Version: tea.String("2024-08-23"),
		// 接口协议
		Protocol: tea.String("HTTPS"),
		// 接口 HTTP 方法
		Method:   tea.String("POST"),
		AuthType: tea.String("AK"),
		Style:    tea.String("ROA"),
		// 接口 PATH
		Pathname: tea.String("/{workspaceId}/gbi/runDataAnalysis"),
		// 接口请求体内容格式
		ReqBodyType: tea.String("json"),
		// 接口响应体内容格式，注意一定得是binary格式，CallApi才会透传出response body进行ReadAsSSE
		BodyType: tea.String("binary"), //sse binary
	}
	_result = params
	return _result
}

func _main(args []*string) (_err error) {
	// 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
	// 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378661.html。
	config := &openapi.Config{
		AccessKeyId:     tea.String("{accessKeyId}"),
		AccessKeySecret: tea.String("{accessKeySecret}"),
	}
	config.Endpoint = tea.String("dataanalysisgbi.cn-beijing.aliyuncs.com")
	client, err := openapi.NewClient(config)
	if err != nil {
		return err
	}

	params := CreateApiInfo()
	body := map[string]interface{}{
		"query":             "列举10条数据",
		"specificationType": "STANDARD_MIX",
	}
	// runtime options
	runtime := &util.RuntimeOptions{}
	request := &openapi.OpenApiRequest{
		Body: openapiutil.Query(body),
	}
	// 复制代码运行请自行打印 API 的返回值
	// 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
	resp, err := client.CallApi(params, request, runtime)
	if err != nil {
		return err
	}

	// 迭代读取SSE内容
	events, err1 := util.ReadAsSSE(resp["body"].(io.ReadCloser))

	if err1 != nil {

	}

	for event := range events {
		fmt.Println("-------------------------------------")
		fmt.Printf("Event ID: %s, Event name: %s, Data: %s\n", tea.StringValue(event.ID), tea.StringValue(event.Event), tea.StringValue(event.Data))
	}
	return nil
}

func main() {
	err := _main(tea.StringSlice(os.Args[1:]))
	if err != nil {
		panic(err)
	}
}
```

#### 返回结果示例

参数说明请参见[Chat对话接口](raw/_short/api-dataanalysisgbi-2024-08-23-rundataanalysis-697fa2953fc095a1.md)的**返回参数**。

```
-------------------------------------
Event ID: , Event name: rewrite, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"rewrite","rewrite":"列举10条数据"}}
-------------------------------------
Event ID: , Event name: selector, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"selector","rewrite":"列举10条数据"}}
-------------------------------------
Event ID: , Event name: refine, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"refine","rewrite":"列举10条数据","attempts":[{"sql":""}]}}
-------------------------------------
Event ID: , Event name: refine, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"refine","rewrite":"列举10条数据","attempts":[{"sql":"SELECT * FROM customers LIMIT"}]}}
-------------------------------------
Event ID: , Event name: refine, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"refine","rewrite":"列举10条数据","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
-------------------------------------
Event ID: , Event name: refine, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"refine","rewrite":"列举10条数据","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
-------------------------------------
Event ID: , Event name: refine, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"refine","rewrite":"列举10条数据","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
-------------------------------------
Event ID: , Event name: sql, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sqlData":{"data":[{"join_date":"2023-10-25","name":"朵莉亚","customer_id":"1","email":"tjia@example.com"},{"join_date":"2024-01-11","name":"完颜烈","customer_id":"2","email":"yexiulan@example.com"},{"join_date":"2022-10-16","name":"林东","customer_id":"3","email":"gkang@example.net"},{"join_date":"2023-09-18","name":"何慧","customer_id":"4","email":"taohe@example.net"},{"join_date":"2024-06-26","name":"李玉珍","customer_id":"5","email":"zhouxiuying@example.com"},{"join_date":"2023-10-12","name":"萧建","customer_id":"6","email":"xiuying64@example.com"},{"join_date":"2023-04-17","name":"邓秀兰","customer_id":"7","email":"qiang76@example.org"},{"join_date":"2023-12-25","name":"傅伟","customer_id":"8","email":"guojie@example.org"},{"join_date":"2022-08-06","name":"王雷","customer_id":"9","email":"li74@example.net"},{"join_date":"2022-12-18","name":"龚淑英","customer_id":"10","email":"qiangshi@example.net"}],"column":["customer_id","name","email","join_date"]},"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"sql","rewrite":"列举10条数据","sql":"SELECT * FROM customers LIMIT 10\n","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
-------------------------------------
Event ID: , Event name: sql_data, Data: {"data":{"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sqlData":{"data":[{"join_date":"2023-10-25","name":"朵莉亚","customer_id":"1","email":"tjia@example.com"},{"join_date":"2024-01-11","name":"完颜烈","customer_id":"2","email":"yexiulan@example.com"},{"join_date":"2022-10-16","name":"林东","customer_id":"3","email":"gkang@example.net"},{"join_date":"2023-09-18","name":"何慧","customer_id":"4","email":"taohe@example.net"},{"join_date":"2024-06-26","name":"李玉珍","customer_id":"5","email":"zhouxiuying@example.com"},{"join_date":"2023-10-12","name":"萧建","customer_id":"6","email":"xiuying64@example.com"},{"join_date":"2023-04-17","name":"邓秀兰","customer_id":"7","email":"qiang76@example.org"},{"join_date":"2023-12-25","name":"傅伟","customer_id":"8","email":"guojie@example.org"},{"join_date":"2022-08-06","name":"王雷","customer_id":"9","email":"li74@example.net"},{"join_date":"2022-12-18","name":"龚淑英","customer_id":"10","email":"qiangshi@example.net"}],"column":["customer_id","name","email","join_date"]},"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"sql_data","rewrite":"列举10条数据","sql":"SELECT * FROM customers LIMIT 10\n","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
-------------------------------------
Event ID: , Event name: result, Data: {"data":{"visualization":{"text":"查询结果列出了10条客户数据，包括客户ID、姓名、邮箱和加入日期。这些客户的加入日期分布在2022年到2024年之间，涵盖了不同的时间段。"},"requestId":"122453F5-B4F3-52B9-BCA5-3BA3097DA2D4","selector":["customers","products","orders"],"sqlData":{"data":[{"join_date":"2023-10-25","name":"朵莉亚","customer_id":"1","email":"tjia@example.com"},{"join_date":"2024-01-11","name":"完颜烈","customer_id":"2","email":"yexiulan@example.com"},{"join_date":"2022-10-16","name":"林东","customer_id":"3","email":"gkang@example.net"},{"join_date":"2023-09-18","name":"何慧","customer_id":"4","email":"taohe@example.net"},{"join_date":"2024-06-26","name":"李玉珍","customer_id":"5","email":"zhouxiuying@example.com"},{"join_date":"2023-10-12","name":"萧建","customer_id":"6","email":"xiuying64@example.com"},{"join_date":"2023-04-17","name":"邓秀兰","customer_id":"7","email":"qiang76@example.org"},{"join_date":"2023-12-25","name":"傅伟","customer_id":"8","email":"guojie@example.org"},{"join_date":"2022-08-06","name":"王雷","customer_id":"9","email":"li74@example.net"},{"join_date":"2022-12-18","name":"龚淑英","customer_id":"10","email":"qiangshi@example.net"}],"column":["customer_id","name","email","join_date"]},"sessionId":"10204244_4e2e5e96-51c7-419b-8390-137f48b4459e","event":"result","rewrite":"列举10条数据","sql":"SELECT * FROM customers LIMIT 10\n","attempts":[{"sql":"SELECT * FROM customers LIMIT 10\n"}]}}
```
