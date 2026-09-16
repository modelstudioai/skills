# 析言GBI对于数据在本地最佳实践

本文基于析言GBI的两段式问答API实现了智能数据问答功能。本文旨在帮助您快速熟悉API的使用，以便在实际项目中灵活运用API。

## 适用场景

当数据库在本地，无法通过公网或是VPC的方式连接析言时，您可以参考本文运用API进行集成开发。

## 前提条件

-   已开通阿里云百炼。
-   已[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
-   已[获取AccessKey ID和AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
-   RAM用户已添加`AliyunDataAnalysisGBIFullAccess`权限策略：[管理RAM用户的权限](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
-   已在析言GBI的**[数据表管理](https://bailian.console.aliyun.com/xiyan#/dataManagement/dataSourceM)**中授权联接了数据库。具体操作，请参见[数据库连接](https://help.aliyun.com/zh/model-studio/xiyan-gbi-user-guide#8e5d17697392b)。

## 操作步骤

### 步骤一：准备数据

具体操作，请参见[官方提供演示用的数据库样例](raw/application-user-guide/application-gallery/xiyan-gbi/official-database-sample-for-demonstration.md)。

### 步骤二：关联虚拟数据源

具体操作，请参见[析言GBI虚拟数据源最佳实践](raw/application-user-guide/application-gallery/xiyan-gbi/analysis-of-gbi-virtual-data-source-best-practices.md)。

### 步骤三：调API生成SQL

基于析言GBI的[运行sql生成](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-local-sql-execution-mode/api-dataanalysisgbi-2024-08-23-runsqlgeneration.md)（例如：本示例中的`RunSqlGenerationRequest`类），通过实现智能数问场景来帮助您熟悉API的使用。

#### Java

**安装析言GBI的Java SDK**

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

1.  保存`pom.xml`文件。
2.  更新项目依赖，将SDK添加到您的项目中。

**实现生成SQL功能**

请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码正常运行并返回正确的结果。

```
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.dataanalysisgbi20240823.AsyncClient;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunDataResultAnalysisRequest;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunDataResultAnalysisResponseBody;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunSqlGenerationRequest;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.RunSqlGenerationResponseBody;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Map;

public class CommonExample_prod_generation {

    public static void main(String[] args) throws Exception {

        StaticCredentialProvider provider = StaticCredentialProvider.create(
                Credential.builder()
                        .accessKeyId("accessKeyId")
                        .accessKeySecret("accessKeySecret")
                        .build()
        );

        AsyncClient client = AsyncClient.builder()
                .region("cn-beijing") // Region ID
                .credentialsProvider(provider)
                .serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3))
                .overrideConfiguration(
                        ClientOverrideConfiguration.create()
                                .setProtocol("HTTPS")
                                .setEndpointOverride("dataanalysisgbi.cn-beijing.aliyuncs.com")
                )
                .build();

        runSqlGeneration(client);

    }

    public static void runSqlGeneration(AsyncClient client) {
        RunSqlGenerationRequest runSqlGenerationRequest = RunSqlGenerationRequest.builder()
                .query("最畅销的3个商品")
                .workspaceId("workspaceId")
                .specificationType("STANDARD_MIX")
                .build();
        ResponseIterator<RunSqlGenerationResponseBody> iterator = client.runSqlGenerationWithResponseIterable(runSqlGenerationRequest).iterator();
        while (iterator.hasNext()) {
            RunSqlGenerationResponseBody event = iterator.next();
            System.out.println(new Gson().toJson(event.getData()));
        }

        System.out.println("ALL***********************");
    }

}
```

#### Python

**安装依赖**
```
pip install alibabacloud-tea-openapi-sse==1.0.2
```
**实现生成SQL功能**

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
    access_key_id = 'accessKeyId'
    access_key_secret = 'accessKeySecret'
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
      action='RunSqlGeneration',
      # 接口版本
      version='2024-08-23',
      # 接口协议
      protocol='HTTPS',
      # 接口 HTTP 方法
      method='POST',
      auth_type='AK',
      style='RPC',
      # 接口 PATH,
      pathname='/gbi/runSqlGeneration',
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
        body=body,
        query={
          'workspaceId': 'workspaceId'
        }

    )
    sse_receiver = self._client.call_sse_api_async(params=self._api_info, request=request, runtime=self._runtime)
    return sse_receiver

async def query():
    run_data_analysis = RunDataAnalysis()
    frame_count = 0
    async for res in await run_data_analysis.do_sse_query('最畅销的3个商品'):
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

```
{"event":"rewrite","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32"}
{"event":"selector","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32"}
{"event":"evidence","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"]}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":""}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sold DESC"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sold DESC LIMIT 3"}
{"event":"sql_part","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold FROM products p JOIN orders o ON p.product_id \u003d o.product_id GROUP BY p.product_name ORDER BY total_sold DESC LIMIT 3; "}
{"event":"sql","requestId":"06735DAF-FAA6-5532-B059-3317953E0E93","rewrite":"最畅销的3个商品是什么？","selector":["products","orders"],"sessionId":"10145656_9cd7d644-d034-4d2d-84bf-809273e43a32","sql":"SELECT p.product_name, SUM(o.quantity) AS total_sold\nFROM products p\nJOIN orders o ON p.product_id \u003d o.product_id\nGROUP BY p.product_name\nORDER BY total_sold DESC\nLIMIT 3;\n"}
```

### 步骤四：手动查询数据

在可信环境内连接数据库，再执行SQL，得到查询结果集。

#### Java

在`<dependencies>`标签内添加以下依赖信息，以下依赖是可选的。

```
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.9</version>
</dependency>
```
**连接数据库并查询数据**

请将代码示例中的`URL`、`USER`及`PASSWORD`替换为实际值，以确保代码正常运行并返回正确的结果。

```
public void executeSql(String sql) {
        String URL = "jdbc:mysql://localhost:3306/your_database_name"; // 替换为你的数据库名
        String USER = "your_username"; // 替换为你的数据库用户名
        String PASSWORD = "your_password"; // 替换为你的数据库密码

        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(URL, USER, PASSWORD);

            preparedStatement = connection.prepareStatement(sql);
            resultSet = preparedStatement.executeQuery();
            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");
                int age = resultSet.getInt("age");
                System.out.println("ID: " + id + ", Name: " + name + ", Age: " + age);
            }
        } catch (ClassNotFoundException e) {
            System.err.println("MySQL 驱动未找到！");
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println("数据库操作失败！");
            e.printStackTrace();
        } finally {
            try {
                if (resultSet != null) resultSet.close();
                if (preparedStatement != null) preparedStatement.close();
                if (connection != null) connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
```

#### Python

**安装依赖**
```
pip install mysql-connector-python
```
**连接数据库并查询数据**

请将代码示例中的`URL`、`DATABASE`、`USER`及`PASSWORD`替换为实际值，以确保代码正常运行并返回正确的结果。

```
import mysql.connector

# 数据库连接配置
config = {
    'user': 'USER',
    'password': 'PASSWORD',
    'host': 'URL',
    'database': 'DATABASE',
    'raise_on_warnings': True
}

# 连接到数据库
cnx = mysql.connector.connect(**config)

# 创建游标对象
cursor = cnx.cursor()

# 执行SQL查询
query = '''select c.`name`, p.product_name, o.* from orders o
			left join customers c on c.customer_id=o.customer_id
			left join products p on p.product_id=o.product_id
		'''
cursor.execute(query)

# 获取查询结果
results = cursor.fetchall()

# 打印结果
for row in results:
    print(row)

# 关闭游标和连接
cursor.close()
cnx.close()
```

### 步骤五：调API进行结果分析

基于析言GBI的[执行结果分析](raw/application-user-guide/application-gallery/xiyan-gbi/api-reference-4/api-dataanalysisgbi-2024-08-23-dir/api-dataanalysisgbi-2024-08-23-dir-intelligent-asking-number/api-dataanalysisgbi-2024-08-23-dir-local-sql-execution-mode/api-dataanalysisgbi-2024-08-23-rundataresultanalysis.md)（例如：本示例中的`RunDataResultAnalysisRequest`类），通过实现智能数问场景来帮助您熟悉API的使用。

**说明**入参中的RequestId参数，需要填入步骤三的结果中返回的RequestId，以此来满足上下文一致。

#### Java

请将代码示例中的`workspaceId`、`requestId`及`sqlData`替换为实际值，以确保代码正常运行并返回正确的结果。

```
public static void runDataResultAnalysis(AsyncClient client) {
    ArrayList<String> columns = new ArrayList<>();
    columns.add("product_name");
    columns.add("quantity");
    String jsonString = "[\n" +
            "            {\n" +
            "                \"product_name\": \"小米手环\",\n" +
            "                \"quantity\": \"28\"\n" +
            "            },\n" +
            "            {\n" +
            "                \"product_name\": \"全自动豆浆机\",\n" +
            "                \"quantity\": \"14\"\n" +
            "            },\n" +
            "            {\n" +
            "                \"product_name\": \"护眼台灯\",\n" +
            "                \"quantity\": \"10\"\n" +
            "            }\n" +
            "        ]";
    // 使用 Gson 来解析 JSON 字符串
    Gson gson = new Gson();
    Type type = new TypeToken<ArrayList<Map<String, String>>>() {}.getType();
    ArrayList<Map<String, String>> data = gson.fromJson(jsonString, type);

    RunDataResultAnalysisRequest.SqlData sqlData = new RunDataResultAnalysisRequest.SqlData.Builder().column(columns).data(data).build();
    RunDataResultAnalysisRequest request = RunDataResultAnalysisRequest.builder()
            .workspaceId("workspaceId")
            .requestId("1261756A-739E-1E79-AD45-xxxxxxx")
            .analysisMode("all")
            .sqlData(sqlData)
            .build();
    ResponseIterator<RunDataResultAnalysisResponseBody> iterator = client.runDataResultAnalysisWithResponseIterable(request).iterator();
    while (iterator.hasNext()) {
        RunDataResultAnalysisResponseBody event = iterator.next();
        System.out.println(new Gson().toJson(event.getData()));
    }
    System.out.println("ALL***********************");
}
```

#### Python

请将代码示例中的`workspaceId`、`requestId`及`sqlData`替换为实际值，以确保代码正常运行并返回正确的结果。

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
    access_key_id = '******'
    access_key_secret = '******'
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
      action='RunDataResultAnalysis',
      # 接口版本
      version='2024-08-23',
      # 接口协议
      protocol='HTTPS',
      # 接口 HTTP 方法
      method='POST',
      auth_type='AK',
      style='RPC',
      # 接口 PATH,
      pathname='/gbi/runDataResultAnalysis',
      # 接口请求体内容格式,
      req_body_type='json',
      # 接口响应体内容格式,
      body_type='sse'
    )
    return params

  async def do_sse_query(self):
    assert self._client is not None

    self._api_info.pathname='/gbi/runDataResultAnalysis'

    sql_data_data_0 = {
        'month': '10',
        'amount': '111'
    }
    sql_data_data_1 = {
        'month': '12',
        'amount': '100'
    }
    sql_data = {
        'data': [
            sql_data_data_0,
            sql_data_data_1
        ],
        'column': [
            'month',
            'amount'
        ]
    }

    body = {
      'sqlData': sql_data,
      'requestId': 'xxxA8903-776C-5CBA-A6E6-E5xxxx',
      'workspaceId': 'ws_SKuxxxxzWcfx'
    }
    request = open_api_models.OpenApiRequest(
        body=body,
        query={
          'workspaceId': 'ws_SKuqhbsS5zWcfzI2'
        }

    )
    sse_receiver = self._client.call_sse_api_async(params=self._api_info, request=request, runtime=self._runtime)
    return sse_receiver

async def query():
    run_data_analysis = RunDataAnalysis()
    frame_count = 0
    async for res in await run_data_analysis.do_sse_query():
        try:
            data = json.loads(res.get('event').data)
            print(data)
        except Exception as e:
          print(f"Error: {e}")
    print('------end--------')

if __name__ == '__main__':
    asyncio.run(query())
```

#### 返回结果示例

```
{'data': {'visualization': {'data': {'plotType': 'bar', 'yAxis': ['total_sold'], 'xAxis': ['product_name']}, 'text': '最畅销的3个商品分别是：小米手环，共售出28件；全自动豆浆机，共售出14件；护眼台灯，共售出10件。'}, 'requestId': 'F6DFA93F-9006-5BF1-A356-A3B60459ED90', 'event': 'result', 'rewrite': '最畅销的3个商品是什么？', 'sql': 'SELECT p.product_name, SUM(o.quantity) AS total_sold\nFROM products p\nJOIN orders o ON p.product_id = o.product_id\nGROUP BY p.product_name\nORDER BY total_sold DESC\nLIMIT 3;\n'}}
```

### 完整示例代码

#### Java

压缩包链接或github地址：[xiyan-sdk-practice.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250224/pntard/xiyan-sdk-practice.zip)

#### Python

压缩包链接或github地址：[xiyan-sdk-practice.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250224/omtmvo/xiyan-sdk-practice.py)
