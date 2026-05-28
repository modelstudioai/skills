# 知识库SearchFilters

如果您在请求 Retrieve 接口时返回的结果包含较多干扰信息，可以参考本文示例，在请求时传入SearchFilters设置个性化的检索条件，对语义检索结果进行过滤，以排除与查询Query无关的信息（该方法尤其适合结构化数据）。

> 指知识库的[Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)接口。

## **效果对比**

**请求Retrieve接口（未传入SearchFilters）**

**请求Retrieve接口（传入SearchFilters）**

Retrieve请求体：

```
{
  "indexId": "o73yjlxxxx",
  "query": "公司中姓名为张三的员工"
}
```

Retrieve请求体：

```
{
  "indexId": "o73yjlxxxx",
  "query": "公司中姓名为张三的员工",
  "searchFilters": [
    {
      "姓名": "张三"
    }
  ]
}
```

Retrieve请求返回：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8891260471/p920375.png)

传统语义检索返回了一些与查询Query（张三）不太相关的文本切片。

Retrieve接口返回：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8891260471/p920378.png)

通过设置检索条件（SearchFilters），过滤语义检索结果中与查询Query（张三）无关的文本切片。

## **语法说明**

SearchFilters可以包含一个或多个子分组（如下方示例包含了两个子分组）。每个子分组由一组或多组Key-Value键值对（检索字段：字段值）组成，对通过用户提示词找到的文本切片进行进一步过滤。子分组之间默认采用 **AND** 语义，且不可更改。﻿关于如何使用子分组，请参见[子分组查询示例](#be34f9cc36xnv)。

```
{
  "searchFilters": [
    {
      "姓名": "张三",
      "性别": "男"
    },
    {
      "岗位": "技术员"
    }
  ]
}
```

子分组内的检索字段支持**单值查询**、**多值查询**、**范围查询**、**模糊查询**和**标签（Tag）查询**。

-   **单值查询：**字段类型只支持数值（long或double）、字符串（string）。关于如何使用单值查询，请参见[单值查询示例](#8b1bb2d6f4xm1)。
    
-   **多值查询：**只支持由纯数值（long或double）或纯字符串（string）组成的数组。关于如何使用多值查询，请参见[多值查询示例](#c174680d7bd3x)。
    
-   **范围查询：**支持**等值查询**和**区间查询**。关于如何使用范围查询，请参见[范围查询示例](#b9cbe02a96577)。
    
    -   **等值查询**：支持 `eq`（等于）、`neq`（不等于） 属性，字段类型支持数值（long或double）和字符串（string）。一个字段不可配置多个值（不区分大小写）。
        
    -   **区间查询**：支持 `gt`（大于）、`gte`（大于等于）、`lt`（小于）、`lte`（小于等于） 属性，字段类型只支持数值（long, double）。
        
-   **模糊查询：**字段类型只支持字符串（string）。支持`like` 属性。关于如何使用模糊查询，请参见[模糊查询示例](#6a1b236cc0wuo)。
    
-   **标签（Tag）查询：**只支持文档搜索、音视频搜索类知识库。关于如何使用标签查询，请参见[标签（Tag）查询示例](#2846aa89bddag)。
    

## **前置步骤**

-   [子账号](https://help.aliyun.com/zh/model-studio/application-permission-management-overview#24ca2dad7djzs)（主账号不需要）需[获取AliyunBailianDataFullAccess策略](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)，并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)，然后才能使用阿里云API操作知识库。
    
    > 子账号只能操作自己已加入的业务空间中的知识库；主账号可操作所有业务空间下的知识库。
    
-   [获取业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace)。
    
-   安装了[阿里云百炼SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29&language=java-tea&tab=primer-doc)并配置好了环境。
    
-   [获取并配置AccessKey和AccessKey Secret到环境变量](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)。
    
-   准备员工信息表[员工信息表.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250224/ghwuqu/%E5%91%98%E5%B7%A5%E4%BF%A1%E6%81%AF%E8%A1%A8.xlsx)（包含三条记录），用于创建知识库（下文示例中会用到）。[创建和使用知识库说明](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)
    
    -   **知识库配置：**
        
        -   **知识库类型：**数据查询
            
        -   **数据来源：**上传数据表
            
        -   **数据表字段结构：**姓名、性别、岗位（string类型）和年龄（double类型）
            
        -   **索引设置：**所有字段均参与检索与模型回复
            
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8891260471/p919990.png)
        

## **完整代码示例**

展开下方折叠面板，查看本文提供的Python和Java完整示例代码（其他语言需参考示例自行实现）。

> 在调用示例代码之前，需[获取AccessKey和AccessKey Secret并配置到环境变量](https://help.aliyun.com/zh/sdk/developer-reference/configure-the-alibaba-cloud-accesskey-environment-variable-on-linux-macos-and-windows-systems)。

## Python

**SearchFiltersFullExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class SearchFiltersFullExample:
    class QueryObject:
        def __init__(self, prefix):
            self.like = prefix

        def to_dict(self):
            return {
                "like": self.like
            }

    class Range:
        def __init__(self, gte, lte):
            self.gte = gte
            self.lte = lte

        def to_dict(self):
            return {
                "gte": self.gte,
                "lte": self.lte
            }

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def sub_group_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中叫张三的员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 分组1查询属性为姓名，值为张三。分组2查询属性为性别，值为女。可替换为实际需要查询的属性和值。
            retrieve_request.search_filters = [
                {"姓名": "张三"},
                {"性别": "女"}
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def single_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中叫张三的员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 单值查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            retrieve_request.search_filters = [
                {"姓名": "张三"}
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def multi_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中所有员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 创建一个列表，用于存放多值。
            names = ["张三", "李四"]
            # 多值查询属性为姓名，对应上方names列表。值为上方指定的多值“张三”和“李四”。可替换为实际需要查询的属性和值。
            retrieve_request.search_filters = [{"姓名": json.dumps(names)}]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def range_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中所有员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 查询属性为年龄，值为范围。可替换为实际需要查询的属性和值。
            age_range = SearchFiltersFullExample.Range(20, 27)
            retrieve_request.search_filters = [
                {"岗位": "技术员"},  # 分组1: 岗位筛选条件
                {"年龄": json.dumps(age_range.to_dict())}  # 分组2: 年龄范围筛选条件
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def wildcard_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中的男性员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 模糊查询属性为岗位，值为技 % 员，此处 % 代表匹配任意字符（包括零个字符）。可替换为实际值。
            position = SearchFiltersFullExample.QueryObject('技%员')
            retrieve_request.search_filters = [
                {"姓名": "张三"},  # 姓名筛选条件。可替换为实际要查询的属性和值。
                {"岗位": json.dumps(position.to_dict())}  # 岗位（模糊查询）筛选条件。可替换为实际要查询的属性和值。
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
    
    @staticmethod
    def tag_query() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '请提供一些候选人'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 创建一个列表，用于存放标签。多个标签之间是或（OR）的关系，不是与（AND）的关系。
            tags = ["A大学", "学生会主席"]
            retrieve_request.search_filters = [
                {"tags": json.dumps(tags)}
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def tag_query2() -> None:
        try:
            client = SearchFiltersFullExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '请提供一些候选人'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 创建两个列表，用于存放标签。
            tag1 = ["A大学"]
            tag2 = ["体育特长生"]
            retrieve_request.search_filters = [
                {"tags": json.dumps(tag1)},
                {"tags": json.dumps(tag2)}
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

    @staticmethod
    def main(args: List[str]) -> None:
        SearchFiltersFullExample.sub_group_query()
        SearchFiltersFullExample.single_query()
        SearchFiltersFullExample.multi_query()
        SearchFiltersFullExample.range_query()
        SearchFiltersFullExample.wildcard_query()
        SearchFiltersFullExample.tag_query()
        SearchFiltersFullExample.tag_query2()

if __name__ == '__main__':
    SearchFiltersFullExample.main(sys.argv[1:])
```

## Java

**SearchFiltersFullExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;
import com.google.gson.JsonArray;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SearchFiltersFullExample {    
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     *
     * @return Client
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void subgroupQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中叫张三的员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map1 = new HashMap<>();
            // 分组1查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            map1.put("姓名", "张三");
            Map<String, String> map2 = new HashMap<>();
            // 分组2查询属性为性别，值为女。可替换为实际需要查询的属性和值。
            map2.put("性别", "女");
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }

    public static void singleQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中叫张三的员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map = new HashMap<>();
            // 单值查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            map.put("姓名", "张三");
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }

    public static void multiQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中所有员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放多值
            JsonArray array = new JsonArray();
            array.add("张三");
            array.add("李四");
            Map<String, String> map = new HashMap<>();
            // 多值查询属性为姓名，值为上方指定的多值“张三”和“李四”。可替换为实际需要查询的属性和值。
            map.put("姓名", array.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
    
    public static void rangeQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中所有员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map1 = new HashMap<>();
            // 分组1查询属性为性别，值为男。可替换为实际需要查询的属性和值。
            map1.put("性别", "男");
            // 分组2查询属性为年龄，值为范围。可替换为实际需要查询的属性和值。
            Map<String, String> map2 = new HashMap<>();
            Range range = new Range(20, 27);
            map2.put("年龄", new Gson().toJson(range));
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }

    public static void wildcardQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中的男性员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 分组1查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            Map<String, String> map1 = new HashMap<>();
            map1.put("姓名", "张三");
            // 分组2查询属性为岗位，值为技%员，此处%代表匹配任意字符（包括零个字符）。可替换为实际需要查询的属性和值。
            Map<String, String> map2 = new HashMap<>();
            QueryObject queryObject = new QueryObject("技%员");
            map2.put("岗位", new Gson().toJson(queryObject));
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
    
    public static void tagQuery() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("请提供一些候选人");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放标签。多个标签之间是或（OR）的关系，不是与（AND）的关系。
            JsonArray array = new JsonArray();
            array.add("A大学");
            array.add("学生会主席");
            Map<String, String> map = new HashMap<>();
            map.put("tags", array.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
    
    public static void tagQuery2() {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("请提供一些候选人");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放标签。
            JsonArray tag1 = new JsonArray();
            tag1.add("A大学");
            JsonArray tag2 = new JsonArray();
            tag2.add("体育特长生");
            Map<String, String> map1 = new HashMap<>();
            map1.put("tags", tag1.toString());
            Map<String, String> map2 = new HashMap<>();
            map2.put("tags", tag2.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) {
        subgroupQuery();
        singleQuery();
        multiQuery();
        rangeQuery();
        wildcardQuery();
        tagQuery();
        tagQuery2();
    }
    
    static class Range {
        double gte;
        double lte;

        public Range(double gte, double lte) {
            this.gte = gte;
            this.lte = lte;
        }
    }

    static class QueryObject {
        String like;

        public QueryObject(String prefix) {
            this.like = prefix;
        }

        public String getLike() {
            return like;
        }

        public void setLike(String like) {
            this.like = like;
        }
    }
}
```

## **快速开始**

以下介绍如何使用SearchFilters进行查询。

### **子分组查询示例**

子分组用于过滤知识库的召回结果，仅返回满足特定条件的文本切片。可将多个子分组（条件）添加到SearchFilters中。子分组之间默认采用 **AND** 语义，且不可更改。

**示例：**检索员工信息知识库，并筛选出`姓名`为**张三**且`性别`为**女**的记录（该知识库中不存在这样的记录）。

```
{
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "性别": "女"
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**SubGroupQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class SubGroupQueryExample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        try:
            client = SubGroupQueryExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中叫张三的员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 分组1查询属性为姓名，值为张三。分组2查询属性为性别，值为女。可替换为实际需要查询的属性和值。
            retrieve_request.search_filters = [
                {"姓名": "张三"},
                {"性别": "女"}
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    SubGroupQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中叫张三的员工",
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "性别": "女"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": []
  },
  "message": "success",
  "requestId": "5BA30772-xxxx-560C-B1F7-C1DA737A9D80",
  "status": "200",
  "success": true
}
```

## Java

**SubGroupQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SubGroupQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     * @return Client
     *
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中叫张三的员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map1 = new HashMap<>();
            // 分组1查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            map1.put("姓名","张三");
            Map<String, String> map2 = new HashMap<>();
            // 分组2查询属性为性别，值为女。可替换为实际需要查询的属性和值。
            map2.put("性别","女");
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中叫张三的员工",
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "性别": "女"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": []
  },
  "message": "success",
  "requestId": "5BA30772-xxxx-560C-B1F7-C1DA737A9D80",
  "status": "200",
  "success": true
}
```

### 单值查询示例

在单值查询时，需要为检索字段传入唯一的值。

**示例：**检索员工信息知识库，并筛选出`姓名`为**张三**的记录。

```
{
  "searchFilters": [
    {
      "姓名": "张三"
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**SingleQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class SingleQueryExample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        client = SingleQueryExample.create_client()
        # 创建retrieve_request对象。
        retrieve_request = bailian_20231229_models.RetrieveRequest()
        # 必填，可传入用户实际输入的提示词。
        retrieve_request.query = '公司中叫张三的员工'
        # 必填，请传入实际的知识库ID。
        retrieve_request.index_id = '请传入实际的知识库ID'
        # 单值查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
        retrieve_request.search_filters = [
            {"姓名": "张三"}
        ]
        try:
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    SingleQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中叫张三的员工",
  "searchFilters": [
    {
      "姓名": "张三"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.32581159472465515,
          "_q_score": 1,
          "source": "0",
          "_score": 0.4556944966316223,
          "doc_id": "table_xxxx75507aab4bd9a24c18d098b2e8ac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_200275507aab4bd9a24c18d098b2e8ac_10285263_1",
          "年龄": "25",
          "岗位": "技术员"
        },
        "score": 0.4556944966316223,
        "text": "姓名:张三 年龄:25 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "2FA4113E-xxxx-59C1-BDB2-5B930D8C9B1C",
  "status": "200",
  "success": true
}
```

## Java

**SingleQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SingleQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     * @return Client
     *
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中叫张三的员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map = new HashMap<>();
            // 单值查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            map.put("姓名","张三");
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中叫张三的员工",
  "searchFilters": [
    {
      "姓名": "张三"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.32581159472465515,
          "_q_score": 1,
          "source": "0",
          "_score": 0.4556944966316223,
          "doc_id": "table_xxxx75507aab4bd9a24c18d098b2e8ac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxx75507aab4bd9a24c18d098b2e8ac_10285263_1",
          "年龄": "25",
          "岗位": "技术员"
        },
        "score": 0.4556944966316223,
        "text": "姓名:张三 年龄:25 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "2FA4113E-xxxx-59C1-BDB2-5B930D8C9B1C",
  "status": "200",
  "success": true
}
```

### 多值查询示例

多值查询允许为检索字段传入多个值，效果类似于SQL中的IN操作符。

**示例：**检索员工信息知识库，并筛选出`姓名`为**张三**或**李四**的记录。

```
{
  "searchFilters": [
    {
      "姓名": ["张三","李四"]
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**MultiQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class MultiQueryExample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        try:
            client = MultiQueryExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中所有员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 创建一个列表，用于存放多值。
            names = ["张三", "李四"]
            # 多值查询属性为姓名，对应上方names列表。值为上方指定的多值“张三”和“李四”。可替换为实际需要查询的属性和值。
            retrieve_request.search_filters = [{"姓名": json.dumps(names)}]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    MultiQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中所有员工",
  "searchFilters": [
    {
      "姓名": ["张三", "李四"]
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.3016361088048254,
          "_q_score": 1,
          "source": "0",
          "_score": 0.3322954773902893,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.3322954773902893,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      },
      {
        "metadata": {
          "_rc_v_score": 0.2531493306159973,
          "_q_score": 0.8392540654998252,
          "source": "0",
          "_score": 0.25632044672966003,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_2",
          "性别": "女",
          "_rc_score": 0,
          "姓名": "李四",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_2",
          "年龄": "31.0",
          "岗位": "销售"
        },
        "score": 0.25632044672966003,
        "text": "姓名:李四 年龄:31.0 岗位:销售 性别:女"
      }
    ]
  },
  "message": "success",
  "requestId": "1DFE5E9E-xxxx-5C37-8011-8FA2E2875309",
  "status": "200",
  "success": true
}
```

## Java

**MultiQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;
import com.google.gson.JsonArray;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MultiQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     * @return Client
     *
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中所有员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放多值
            JsonArray array = new JsonArray();
            array.add("张三");
            array.add("李四");
            Map<String, String> map = new HashMap<>();
            // 多值查询属性为姓名，值为上方指定的多值“张三”和“李四”。可替换为实际需要查询的属性和值。
            map.put("姓名", array.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中所有员工",
  "searchFilters": [
    {
      "姓名": ["张三", "李四"]
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.3016361088048254,
          "_q_score": 1,
          "source": "0",
          "_score": 0.3322954773902893,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.3322954773902893,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      },
      {
        "metadata": {
          "_rc_v_score": 0.2531493306159973,
          "_q_score": 0.8392540654998252,
          "source": "0",
          "_score": 0.25632044672966003,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_2",
          "性别": "女",
          "_rc_score": 0,
          "姓名": "李四",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_2",
          "年龄": "31.0",
          "岗位": "销售"
        },
        "score": 0.25632044672966003,
        "text": "姓名:李四 年龄:31.0 岗位:销售 性别:女"
      }
    ]
  },
  "message": "success",
  "requestId": "1DFE5E9E-xxxx-5C37-8011-8FA2E2875309",
  "status": "200",
  "success": true
}
```

### 范围查询示例

通过范围查询，可找出检索字段（如年龄）值在指定范围内满足条件的所有记录。

**示例：**检索员工信息知识库，并筛选出`岗位`为**技术员**（单值查询），且`年龄`在**20**至**25**岁之间（范围查询）的记录。

```
{
  "searchFilters": [
    {
      "岗位": "技术员"
    },
    {
      "年龄": {
        "gte": 20,
        "lte": 25
      }
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**RangeQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class RangeQueryExample:
    class Range:
        def __init__(self, gte, lte):
            self.gte = gte
            self.lte = lte

        def to_dict(self):
            return {
                "gte": self.gte,
                "lte": self.lte
            }

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        try:
            client = RangeQueryExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中所有员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 查询属性为年龄，值为范围。可替换为实际需要查询的属性和值。
            age_range = RangeQueryExample.Range(20, 27)
            retrieve_request.search_filters = [
                {"岗位": "技术员"},  # 分组1: 岗位筛选条件
                {"年龄": json.dumps(age_range.to_dict())}  # 分组2: 年龄范围筛选条件
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    RangeQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中所有员工",
  "searchFilters": [
    {
      "性别": "男"
    },
    {
      "年龄": "{\"gte\":20.0,\"lte\":27.0}"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.3016361088048254,
          "_q_score": 1,
          "source": "0",
          "_score": 0.3322954773902893,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.3322954773902893,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "AE0B5ABC-xxxx-54A1-9ED4-91865B859DF6",
  "status": "200",
  "success": true
}
```

## Java

**RangeQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class RangeQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     * @return Client
     *
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中所有员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            Map<String, String> map1 = new HashMap<>();
            // 分组1查询属性为性别，值为男。可替换为实际需要查询的属性和值。
            map1.put("性别", "男");
            // 分组2查询属性为年龄，值为范围。可替换为实际需要查询的属性和值。
            Map<String, String> map2 = new HashMap<>();
            Range range = new Range(20, 27);
            map2.put("年龄", new Gson().toJson(range));
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
    
    static class Range {
        double gte;
        double lte;

        public Range(double gte, double lte) {
            this.gte = gte;
            this.lte = lte;
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中所有员工",
  "searchFilters": [
    {
      "性别": "男"
    },
    {
      "年龄": "{\"gte\":20.0,\"lte\":27.0}"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.3016361088048254,
          "_q_score": 1,
          "source": "0",
          "_score": 0.3322954773902893,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.3322954773902893,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "AE0B5ABC-xxxx-54A1-9ED4-91865B859DF6",
  "status": "200",
  "success": true
}
```

### 模糊查询示例

模糊查询通过指定通配符查找包含特定字符序列的记录，效果类似于SQL中的LIKE操作符。

SearchFilters模糊查询支持以下通配符（和SQL语法一致）：

**通配符**

**描述**

%

替代 0 个或多个字符。

\_

替代一个字符。

**示例：**检索员工信息知识库，并筛选出`姓名`为**张三**，`岗位`包含**技**和**员**两个字（可能是技术员，也可能是技术人员等）的记录。

```
{
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "岗位": {
        "like": "技%员"
      }
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**WildcardQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class WildcardQueryExample:
    class QueryObject:
        def __init__(self, prefix):
            self.like = prefix

        def to_dict(self):
            return {
                "like": self.like
            }

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        try:
            client = WildcardQueryExample.create_client()
            # 创建retrieve_request对象。
            retrieve_request = bailian_20231229_models.RetrieveRequest()
            # 必填，可传入用户实际输入的提示词。
            retrieve_request.query = '公司中的男性员工'
            # 必填，请传入实际的知识库ID。
            retrieve_request.index_id = '请传入实际的知识库ID'
            # 模糊查询属性为岗位，值为技 % 员，此处 % 代表匹配任意字符（包括零个字符）。可替换为实际值。
            position = WildcardQueryExample.QueryObject('技%员')
            retrieve_request.search_filters = [
                {"姓名": "张三"},  # 姓名筛选条件。可替换为实际要查询的属性和值。
                {"岗位": json.dumps(position.to_dict())}  # 岗位（模糊查询）筛选条件。可替换为实际要查询的属性和值。
            ]
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    WildcardQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中的男性员工",
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "岗位": "{\"like\":\"技%员\"}"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.41137335930387275,
          "_q_score": 1,
          "source": "0",
          "_score": 0.46098726987838745,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.46098726987838745,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "FA759FEC-xxxx-50B7-A64D-BE49A7DF56B8",
  "status": "200",
  "success": true
}
```

## Java

**WildcardQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class WildcardQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     *
     * @return Client
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args_) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("公司中的男性员工");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 分组1查询属性为姓名，值为张三。可替换为实际需要查询的属性和值。
            Map<String, String> map1 = new HashMap<>();
            map1.put("姓名", "张三");
            // 分组2查询属性为岗位，值为技%员，此处%代表匹配任意字符（包括零个字符）。可替换为实际需要查询的属性和值。
            Map<String, String> map2 = new HashMap<>();
            QueryObject queryObject = new QueryObject("技%员");
            map2.put("岗位", new Gson().toJson(queryObject));
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }

    static class QueryObject {
        String like;

        public QueryObject(String prefix) {
            this.like = prefix;
        }

        public String getLike() {
            return like;
        }

        public void setLike(String like) {
            this.like = like;
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "indexId": "27ubwxxxxx",
  "WorkspaceId":"llm-4u5xpd1xdjxxxxxx",
  "query": "公司中的男性员工",
  "searchFilters": [
    {
      "姓名": "张三"
    },
    {
      "岗位": "{\"like\":\"技%员\"}"
    }
  ]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "code": "Success",
  "data": {
    "nodes": [
      {
        "metadata": {
          "_rc_v_score": 0.41137335930387275,
          "_q_score": 1,
          "source": "0",
          "_score": 0.46098726987838745,
          "doc_id": "table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "性别": "男",
          "_rc_score": 0,
          "姓名": "张三",
          "doc_name": "员工表",
          "_id": "llm-xxxxpd1xdjqp8itj_27ubwxxxxx_table_xxxxad1c331c424780a8023376a73fac_10285263_1",
          "年龄": "25.0",
          "岗位": "技术员"
        },
        "score": 0.46098726987838745,
        "text": "姓名:张三 年龄:25.0 岗位:技术员 性别:男"
      }
    ]
  },
  "message": "success",
  "requestId": "FA759FEC-xxxx-50B7-A64D-BE49A7DF56B8",
  "status": "200",
  "success": true
}
```

### **标签（Tag）查询示例**

检索文档搜索、音视频搜索类知识库时，可通过[标签](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#0a4efa5d7dta6)筛选文件，提高检索效率与准确性。

**示例：**创建一个文档搜索类知识库，其中包含张三、李四和王五三人的信息。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8207307471/p953161.png)

以上文件分别添加了以下标签：

**文件**

**标签**

张三简历

`A大学`、`体育特长生`

李四简历

`B大学`

王五简历

`B大学`、`学生会主席`

例如使用SearchFilters查询人才知识库，要求返回文件标签含**A大学**或**学生会主席**的相关文本切片：

> 多个标签之间是逻辑或（OR）的关系，不是逻辑与（AND）的关系。[可通过子分组查询实现“逻辑与”](#a95c838b79jne)。

```
{
  "searchFilters": [
    {
      "tags": ["A大学","学生会主席"]
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**TagQueryExample.py**

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class TagQueryExample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        client = TagQueryExample.create_client()
        # 创建retrieve_request对象。
        retrieve_request = bailian_20231229_models.RetrieveRequest()
        # 必填，可传入用户实际输入的提示词。
        retrieve_request.query = '请提供一些候选人'
        # 必填，请传入实际的知识库ID。
        retrieve_request.index_id = '请传入实际的知识库ID'
        # 创建一个列表，用于存放标签。多个标签之间是或（OR）的关系，不是与（AND）的关系。
        tags = ["A大学", "学生会主席"]
        retrieve_request.search_filters = [
            {"tags": json.dumps(tags)}
        ]
        try:
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    TagQueryExample.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "IndexId": "8mbtdxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjxxxxxx",
  "Query": "请提供一些候选人",
  "SearchFilters": [{"tags":["A大学", "学生会主席"]}]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "Code": "Success",
  "Data": {
    "Nodes": [
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E5%BC%A0%E4%B8%89%E7%AE%80%E5%8E%86_1746760910599.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=roY%2Falbh6smkLdPuA6wjnZRVMa4%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1422617520249937,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|b99e98835c3c6d8f6496df5a43de0ba5|aa3ed8fc4aae8bbb78872994b01e0fda",
          "_q_score": 0.8935035934804278,
          "source": "0",
          "_score": 0.1736905574798584,
          "title": "",
          "doc_id": "file_e787926158704f95aad6bc967619f176_10285263",
          "content": "姓名：张三性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "张三简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_e787926158704f95aad6bc967619f176_10285263_0_0"
        },
        "Score": 0.1736905574798584,
        "Text": "姓名：张三性别：男年龄：23"
      },
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E7%8E%8B%E4%BA%94%E7%AE%80%E5%8E%86_1746760946844.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=gTGPTce5xUu9mtcMcmyMEeb5azk%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1592178845871759,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|d4a048b6799ce07e08430f018af091a0|fe90f8248ea64f70ea37c0df7afcfc12",
          "_q_score": 1,
          "source": "0",
          "_score": 0.15737050771713257,
          "title": "",
          "doc_id": "file_63563df5df66488cb8e28bfff11e40eb_10285263",
          "content": "姓名：王五性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "王五简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_63563df5df66488cb8e28bfff11e40eb_10285263_0_0"
        },
        "Score": 0.15737050771713257,
        "Text": "姓名：王五性别：男年龄：23"
      }
    ]
  },
  "Message": "success",
  "RequestId": "12A5F9C6-xxxx-5593-8955-86D52585EE27",
  "Status": 200,
  "Success": true
}
```

## Java

**TagQueryExample.java**

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;
import com.google.gson.JsonArray;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TagQueryExample {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     *
     * @return Client
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("请提供一些候选人");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放标签。多个标签之间是或（OR）的关系，不是与（AND）的关系。
            JsonArray array = new JsonArray();
            array.add("A大学");
            array.add("学生会主席");
            Map<String, String> map = new HashMap<>();
            map.put("tags", array.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "IndexId": "8mbtdxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjxxxxxx",
  "Query": "请提供一些候选人",
  "SearchFilters": "[{\"tags\":[\\\"A大学\\\", \\\"学生会主席\\\"]}]"
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "Code": "Success",
  "Data": {
    "Nodes": [
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E5%BC%A0%E4%B8%89%E7%AE%80%E5%8E%86_1746760910599.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=roY%2Falbh6smkLdPuA6wjnZRVMa4%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1422617520249937,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|b99e98835c3c6d8f6496df5a43de0ba5|aa3ed8fc4aae8bbb78872994b01e0fda",
          "_q_score": 0.8935035934804278,
          "source": "0",
          "_score": 0.1736905574798584,
          "title": "",
          "doc_id": "file_e787926158704f95aad6bc967619f176_10285263",
          "content": "姓名：张三性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "张三简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_e787926158704f95aad6bc967619f176_10285263_0_0"
        },
        "Score": 0.1736905574798584,
        "Text": "姓名：张三性别：男年龄：23"
      },
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E7%8E%8B%E4%BA%94%E7%AE%80%E5%8E%86_1746760946844.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=gTGPTce5xUu9mtcMcmyMEeb5azk%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1592178845871759,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|d4a048b6799ce07e08430f018af091a0|fe90f8248ea64f70ea37c0df7afcfc12",
          "_q_score": 1,
          "source": "0",
          "_score": 0.15737050771713257,
          "title": "",
          "doc_id": "file_63563df5df66488cb8e28bfff11e40eb_10285263",
          "content": "姓名：王五性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "王五简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_63563df5df66488cb8e28bfff11e40eb_10285263_0_0"
        },
        "Score": 0.15737050771713257,
        "Text": "姓名：王五性别：男年龄：23"
      }
    ]
  },
  "Message": "success",
  "RequestId": "12A5F9C6-xxxx-5593-8955-86D52585EE27",
  "Status": 200,
  "Success": true
}
```

**示例：**使用SearchFilters查询人才知识库，要求返回文档标签含**A大学**与**体育特长生**的相关文本切片（逻辑与）：

```
{
  "searchFilters": [
    {
      "tags": ["A大学"]
    },
    {
      "tags": ["体育特长生"]
    }
  ]
}
```

> 展开下方折叠面板查看示例代码。

## Python

**TagQueryExample2.py**

```
import json
import os
import sys
from typing import List

from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient

class TagQueryExample2:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> bailian20231229Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = f'bailian.cn-beijing.aliyuncs.com'
        return bailian20231229Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        client = TagQueryExample2.create_client()
        # 创建retrieve_request对象。
        retrieve_request = bailian_20231229_models.RetrieveRequest()
        # 必填，可传入用户实际输入的提示词。
        retrieve_request.query = '请提供一些候选人'
        # 必填，请传入实际的知识库ID。
        retrieve_request.index_id = '请传入实际的知识库ID'
        # 创建两个列表，用于存放标签。
        tag1 = ["A大学"]
        tag2 = ["体育特长生"]
        retrieve_request.search_filters = [
            {"tags": json.dumps(tag1)},
            {"tags": json.dumps(tag2)}
        ]
        try:
            # 进行检索，传入业务空间ID和retrieve_request对象。
            resp = client.retrieve('请传入实际的业务空间ID', retrieve_request)
            print(UtilClient.to_jsonstring(resp.body))
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)

if __name__ == '__main__':
    TagQueryExample2.main(sys.argv[1:])
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "IndexId": "8mbtdxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjxxxxxx",
  "Query": "请提供一些候选人",
  "SearchFilters": [{"tags":["A大学"]},{"tags":["体育特长生"]}]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "Code": "Success",
  "Data": {
    "Nodes": [
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E5%BC%A0%E4%B8%89%E7%AE%80%E5%8E%86_1746760910599.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=roY%2Falbh6smkLdPuA6wjnZRVMa4%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1422617520249937,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|b99e98835c3c6d8f6496df5a43de0ba5|aa3ed8fc4aae8bbb78872994b01e0fda",
          "_q_score": 1,
          "source": "0",
          "_score": 0.1736905574798584,
          "title": "",
          "doc_id": "file_e787926158704f95aad6bc967619f176_10285263",
          "content": "姓名：张三性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "张三简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_e787926158704f95aad6bc967619f176_10285263_0_0"
        },
        "Score": 0.1736905574798584,
        "Text": "姓名：张三性别：男年龄：23"
      }
    ]
  },
  "Message": "success",
  "RequestId": "1ED6CECE-xxxx-5B21-91DB-410E0219412A",
  "Status": 200,
  "Success": true
}
```

## Java

**TagQueryExample2.java**

```
import com.aliyun.bailian20231229.models.RetrieveRequest;
import com.aliyun.bailian20231229.models.RetrieveResponse;
import com.google.gson.Gson;
import com.google.gson.JsonArray;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TagQueryExample2 {
    /**
     * <b>description</b> :
     * <p>使用AK&SK初始化账号Client</p>
     *
     * @return Client
     * @throws Exception
     */
    public static com.aliyun.bailian20231229.Client createClient() throws Exception {
        // 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        // 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378657.html。
        com.aliyun.teaopenapi.models.Config config = new com.aliyun.teaopenapi.models.Config()
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
                .setAccessKeyId(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
                // 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
                .setAccessKeySecret(System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"));
        // Endpoint 请参考 https://api.aliyun.com/product/bailian
        config.endpoint = "bailian.cn-beijing.aliyuncs.com";
        return new com.aliyun.bailian20231229.Client(config);
    }

    public static void main(String[] args) {
        try {
            com.aliyun.bailian20231229.Client client = createClient();
            // 创建RetrieveRequest对象。
            RetrieveRequest request = new RetrieveRequest();
            // 必填，可传入用户实际输入的提示词。
            request.setQuery("请提供一些候选人");
            // 必填，请传入实际的知识库ID。
            request.setIndexId("请传入实际的知识库ID");
            // 创建一个JsonArray，用于存放标签。
            JsonArray tag1 = new JsonArray();
            tag1.add("A大学");
            JsonArray tag2 = new JsonArray();
            tag2.add("体育特长生");
            Map<String, String> map1 = new HashMap<>();
            map1.put("tags", tag1.toString());
            Map<String, String> map2 = new HashMap<>();
            map2.put("tags", tag2.toString());
            List<Map<String, String>> searchFilters = new ArrayList<>();
            searchFilters.add(map1);
            searchFilters.add(map2);
            request.setSearchFilters(searchFilters);
            // 进行检索，传入业务空间ID和RetrieveRequest。
            RetrieveResponse resp = client.retrieve("请传入实际的业务空间ID", request);
            System.out.println(new Gson().toJson(resp.getBody()));
        } catch (Exception e) {
            // 知识库检索失败处理。
            // 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            System.out.println(e.getMessage());
        }
    }
}
```

**请求示例**

[请求参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-35)

```
{
  "IndexId": "8mbtdxxxxx",
  "WorkspaceId": "llm-4u5xpd1xdjxxxxxx",
  "Query": "请提供一些候选人",
  "SearchFilters": [{"tags":["A大学"]},{"tags":["体育特长生"]}]
}
```

**响应示例**

[返回参数说明](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-40)

```
{
  "Code": "Success",
  "Data": {
    "Nodes": [
      {
        "Metadata": {
          "file_path": "https://bailian-datahub-data-prod.oss-cn-beijing.aliyuncs.com/10285263/multimodal/docJson/%E5%BC%A0%E4%B8%89%E7%AE%80%E5%8E%86_1746760910599.json?Expires=1747020348&OSSAccessKeyId=LTAI************&Signature=roY%2Falbh6smkLdPuA6wjnZRVMa4%3D",
          "is_displayed_chunk_content": "true",
          "_rc_v_score": 0.1422617520249937,
          "image_url": [],
          "nid": "ba8a14099f43308734538c29271cc7cd|b99e98835c3c6d8f6496df5a43de0ba5|aa3ed8fc4aae8bbb78872994b01e0fda",
          "_q_score": 1,
          "source": "0",
          "_score": 0.1736905574798584,
          "title": "",
          "doc_id": "file_e787926158704f95aad6bc967619f176_10285263",
          "content": "姓名：张三性别：男年龄：23",
          "_rc_score": 0,
          "workspace_id": "llm-4u5xpd1xdjxxxxxx",
          "hier_title": "",
          "page_number": [
            0
          ],
          "doc_name": "张三简历",
          "pipeline_id": "8mbtdxxxxx",
          "_id": "llm-4u5xpd1xdjxxxxxx_8mbtdxxxxx_file_e787926158704f95aad6bc967619f176_10285263_0_0"
        },
        "Score": 0.1736905574798584,
        "Text": "姓名：张三性别：男年龄：23"
      }
    ]
  },
  "Message": "success",
  "RequestId": "1ED6CECE-xxxx-5B21-91DB-410E0219412A",
  "Status": 200,
  "Success": true
}
```

## **相关文档**

**知识库用户指南**

请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

**检索知识库**

可调用[Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)接口检索知识库并返回文本切片。

**子账号调用**

RAM用户（子账号）请先获取阿里云百炼的数据权限再调用[Retrieve](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve)接口，请参见[授权RAM用户API权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)。

## 错误码

如果调用失败并收到报错信息，请参见[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)进行解决。
