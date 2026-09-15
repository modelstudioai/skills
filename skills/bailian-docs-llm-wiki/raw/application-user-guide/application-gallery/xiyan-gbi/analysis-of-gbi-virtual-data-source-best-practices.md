# 析言GBI虚拟数据源最佳实践

部分客户基于数据安全性考虑，不允许云服务访问其数据库。因此，析言GBI提出了虚拟数据源形式的无数据库托管连接方案，该方案能够在将数据库执行的操作保留在本地的同时，使客户享受到云端生成SQL的能力。

## 前提条件

-   已开通阿里云百炼。
-   已获取WorkspaceID：[获取Workspace ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id#732535cfc959h)。
-   已获取AccessKey ID和AccessKey Secret：[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/developer-reference/get-accesskey-appid-and-agentkey)。
-   RAM用户已添加`AliyunDataAnalysisGBIFullAccess`权限策略：[通过RAM控制台授权](https://help.aliyun.com/zh/model-studio/developer-reference/use-and-authorize-ram-user#8976a2506dqx4)。
-   已安装析言GBI的Java SDK，具体操作请参见[安装析言GBI的Java SDK](raw/application-user-guide/application-gallery/xiyan-gbi/gbi-best-practices.md)。

## 数据库连接方式介绍

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5627337371/p907073.png)

-   常规的**数据库托管连接方式**接入析言GBI云服务，具有集成便利的特点。用户只需在产品页面上进行数据源的授权关联，析言GBI便能直接访问您的业务数据库，以获取SQL查询结果。
-   **无数据库托管连接方式**接入析言GBI云服务，具有较高的数据安全性，但用户需要在客户端本地自行执行SQL并获取查询结果。**虚拟数据源**是析言GBI云服务为降低用户使用成本和开发难度而提供的官方解决方案，旨在实现无数据库托管连接方式的接入。

## 虚拟数据源方案简介

为了解决用户因数据安全考虑，而无法直接采用数据库托管连接方式的问题，析言GBI推出了**虚拟数据源**解决方案。用户可以利用析言GBI云服务提供的SDK，构建与其业务数据库属性相同的虚拟数据源，并将该虚拟数据源与析言GBI云服务中的业务空间进行关联，从而在不直接访问用户真实业务数据库的情况下，仍能够生成SQL查询。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5627337371/p907169.png)

## 创建、关联和授权虚拟数据源

### 步骤一：创建虚拟数据源实例

您可以通过析言GBI云服务提供的创建虚拟数据源实例接口（createVirtualDatasourceInstance）创建最多十个虚拟数据源实例（每个业务空间下）。当前实例可以视为一个空的数据库实例（RDS实例）。

java

```
/**
     * 创建虚拟数据源实例
     *
     * @param client
     */
    public void create(AsyncClient client) {
        CreateVirtualDatasourceInstanceRequest createVirtualDatasourceInstanceRequest = CreateVirtualDatasourceInstanceRequest.builder()
                // 填写创建虚拟数据源实例所属的业务空间id
                .workspaceId("workspaceId")
                // 虚拟数据源实例的名字
                .name("name")
                // 虚拟数据源实例的描述
                .description("description")
                // 虚拟数据源实例的方言类型，51：mysql类型虚拟数据源，52：postgresql类型虚拟数据源实例
                .type(51)
                .build();
        CompletableFuture<CreateVirtualDatasourceInstanceResponse> virtualDatasourceInstance = client.createVirtualDatasourceInstance(createVirtualDatasourceInstanceRequest);
        CreateVirtualDatasourceInstanceResponse createVirtualDatasourceInstanceResponse = virtualDatasourceInstance.join();
        System.out.println(createVirtualDatasourceInstanceResponse.getBody().getData());
    }
```

python

```
def create_virtual_datasource_instance(
    args: List[str],
) -> None:
    client = Sample.create_client()
    create_virtual_datasource_instance_request = data_analysis_gbi20240823_models.CreateVirtualDatasourceInstanceRequest()
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        # 复制代码运行请自行打印 API 的返回值
        client.create_virtual_datasource_instance_with_options(create_virtual_datasource_instance_request, headers, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
```

### 步骤二：查看虚拟数据源实例列表

您可以通过析言GBI云服务提供的查看虚拟数据源实例列表接口（listVirtualDatasourceInstanceRequest）查看当前业务空间下的全部虚拟数据源实例（以业务空间为维度），以获取关键的虚拟数据源唯一标识符（vdbId）。

java

```
/**
     * 获取虚拟数据源实例的列表
     *
     * @param client
     */
    public void list(AsyncClient client) {
        ListVirtualDatasourceInstanceRequest listVirtualDatasourceInstanceRequest = ListVirtualDatasourceInstanceRequest.builder()
                // 填写需要获取数据源实例列表的业务空间id
                .workspaceId("")
                .build();
        ListVirtualDatasourceInstanceResponse listVirtualDatasourceInstanceResponse = client.listVirtualDatasourceInstance(listVirtualDatasourceInstanceRequest).join();
        Gson gson = new Gson();
        String jsonString = gson.toJson(listVirtualDatasourceInstanceResponse.getBody().getData());
        System.out.println(jsonString);
    }
```

python

```
def list_virtual_datasource_instance(
    args: List[str],
) -> None:
    client = Sample.create_client()
    list_virtual_datasource_instance_request = data_analysis_gbi20240823_models.ListVirtualDatasourceInstanceRequest()
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        # 复制代码运行请自行打印 API 的返回值
        client.list_virtual_datasource_instance_with_options(list_virtual_datasource_instance_request, headers, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
```

### 步骤三：向虚拟数据源实例中添加ddl语句

您可以通过析言GBI云服务提供的向虚拟数据源中添加ddl语句接口（saveVirtualDatasourceDdl），将ddl语句添加到您指定的虚拟数据源实例（vdbId）中。析言GBI云服务将对您的ddl语句进行解析，生成相应的数据表和数据列的结构化信息，并予以维护。

java

```
/**
     * 向虚拟数据源添加ddl语句
     * @param client
     */
    public void addDdlForVirtualDatasource(AsyncClient client){
        SaveVirtualDatasourceDdlRequest saveVirtualDatasourceDdlRequest = SaveVirtualDatasourceDdlRequest.builder()
                // 需要添加ddl的虚拟数据源实例属于哪个业务空间
                .workspaceId("workspaceId")
                // 需要添加ddl的虚拟数据源实例的唯一标识符id
                .vdbId("vdb-id")
                // 需要添加的ddl语句，可以添加多个ddl语句，用";"隔开
                .ddl("CREATE TABLE user (id int NOT NULL AUTO_INCREMENT comment 'ID',name varchar(10) NOT NULL comment '姓名', dept_id int NOT NULL comment '部门ID', salary bigint NULL DEFAULT 0 comment '薪水',  PRIMARY KEY (`id`),   KEY `idx_name` (`name`),   KEY `d_id` (`dept_id`),    CONSTRAINT `d_id` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`)) COMMENT='用户表' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                .build();
        SaveVirtualDatasourceDdlResponse  saveVirtualDatasourceDdlResponse = client.saveVirtualDatasourceDdl(saveVirtualDatasourceDdlRequest).join();
        System.out.println(saveVirtualDatasourceDdlResponse.getBody().getData());
    }
```

python

```
def save_virtual_datasource_ddl(self):
    save_virtual_datasource_ddl_request = data_analysis_gbi20240823_models.SaveVirtualDatasourceDdlRequest(
        workspace_id= workspace_id,
        # 需要添加ddl的虚拟数据源实例的唯一标识符id
        vdb_id='vdb_id',
        # 需要添加的ddl语句，可以添加多个ddl语句，用";"隔开
        ddl="CREATE TABLE user (id int NOT NULL AUTO_INCREMENT comment 'ID',name varchar(10) NOT NULL comment '姓名', dept_id int NOT NULL comment '部门ID', salary bigint NULL DEFAULT 0 comment '薪水',  PRIMARY KEY (`id`),   KEY `idx_name` (`name`),   KEY `d_id` (`dept_id`),    CONSTRAINT `d_id` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`)) COMMENT='用户表' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        # 复制代码运行请自行打印 API 的返回值
        self._client.save_virtual_datasource_ddl_with_options(save_virtual_datasource_ddl_request, headers, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
```

### 步骤四：将虚拟数据源实例与您的业务空间进行绑定

您可以通过析言GBI云服务提供的关联虚拟数据源实例接口（createDatasourceAuthorization）将指定的虚拟数据源实例（vdbId）与业务空间进行关联。

java

```
/**
     * 授权关联数据源实例，将数据源与业务空间进行关联
     * @param client
     */
    public void createAuthorize(Client client){
        CreateDatasourceAuthorizationRequest createAuthorizeRequest = new CreateDatasourceAuthorizationRequest();
        // 关联的数据源实例的类型，具体类型可以参考sdk调用文档，关联虚拟数据源实例时，默认使用创建时所填写的类型
        createAuthorizeRequest.setType(51);
        // 关联的业务空间id
        createAuthorizeRequest.setWorkspaceId("workspaceId");
        // 如果关联的是虚拟数据源则需要添加虚拟数据源实例id
        createAuthorizeRequest.setVdbId("vdb-id");
        try {
            CreateDatasourceAuthorizationResponse createDatasourceAuthorizationResponse = client.createDatasourceAuthorization(createAuthorizeRequest);
            System.out.println(createDatasourceAuthorizationResponse.getBody().getData());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```

python

```
def create_datasource_authorization(
    args: List[str],
) -> None:
    client = Sample.create_client()
    create_datasource_authorization_request = data_analysis_gbi20240823_models.CreateDatasourceAuthorizationRequest()
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        # 复制代码运行请自行打印 API 的返回值
        client.create_datasource_authorization_with_options(create_datasource_authorization_request, headers, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
```

### 步骤五：在您的虚拟数据源中选择您需要的数据表

您可以通过析言GBI云服务提供的关联数据表到析言GBI云服务接口（syncRemoteTables）将指定的数据表信息关联到析言GBI云服务，后续的智能问数和SQL生成将依赖于您所选择的数据表。

java

```
/**
     * 关联数据源中的数据表到所指定的业务空间，智能问数将基于所关联的数据表来进行问答
     * @param client
     */
    public void syncRemoteTables(AsyncClient client){
        ArrayList<String> tableNames = new ArrayList<>();
        tableNames.add("user");
        SyncRemoteTablesRequest syncRemoteTablesRequest = SyncRemoteTablesRequest
                .builder()
                // 需要关联的数据表的业务空间
                .workspaceId("workspaceId")
                .tableNames(tableNames)
                .build();
        SyncRemoteTablesResponse syncRemoteTablesResponse = client.syncRemoteTables(syncRemoteTablesRequest).join();
        System.out.println(syncRemoteTablesResponse.getBody().getData());
    }
```

python

```
def sync_remote_tables(
    args: List[str],
) -> None:
    client = Sample.create_client()
    sync_remote_tables_request = data_analysis_gbi20240823_models.SyncRemoteTablesRequest()
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        # 复制代码运行请自行打印 API 的返回值
        client.sync_remote_tables_with_options(sync_remote_tables_request, headers, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
```

## 使用虚拟数据源实例代码示例

基于析言GBI云服务所提供的SDK，以下示例代码将通过创建、关联和授权虚拟数据源等全链路场景，帮助您熟悉API的使用。在使用之前，请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码能够正常运行并返回正确的结果。

以下示例代码中，从创建、修改、删除和查看四个角度对虚拟数据源实例进行管理。并给出如何授权虚拟数据源实例关联到您所指定的业务空间，以及如何将虚拟数据源实例中您所指定的表与析言GBI建立关联关系。

java

```
package com.alibaba.iic.llmsolution.gbi.util;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.dataanalysisgbi20240823.AsyncClient;
import com.aliyun.sdk.service.dataanalysisgbi20240823.models.*;
import com.google.gson.Gson;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;

public class VirtualDatasourceTest {
    public static void main(String[] args) {
        StaticCredentialProvider provider = StaticCredentialProvider.create(
                Credential.builder()
                        .accessKeyId("")
                        .accessKeySecret("")
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
    }

    /**
     * 创建虚拟数据源实例
     *
     * @param client
     */
    public void create(AsyncClient client) {
        CreateVirtualDatasourceInstanceRequest createVirtualDatasourceInstanceRequest = CreateVirtualDatasourceInstanceRequest.builder()
                // 填写创建虚拟数据源实例所属的业务空间id
                .workspaceId("workspaceId")
                // 虚拟数据源实例的名字
                .name("name")
                // 虚拟数据源实例的描述
                .description("description")
                // 虚拟数据源实例的方言类型，51：mysql类型虚拟数据源，52：postgresql类型虚拟数据源实例
                .type(51)
                .build();
        CompletableFuture<CreateVirtualDatasourceInstanceResponse> virtualDatasourceInstance = client.createVirtualDatasourceInstance(createVirtualDatasourceInstanceRequest);
        CreateVirtualDatasourceInstanceResponse createVirtualDatasourceInstanceResponse = virtualDatasourceInstance.join();
        System.out.println(createVirtualDatasourceInstanceResponse.getBody().getData());
    }

    /**
     * 获取虚拟数据源实例的列表
     *
     * @param client
     */
    public void list(AsyncClient client) {
        ListVirtualDatasourceInstanceRequest listVirtualDatasourceInstanceRequest = ListVirtualDatasourceInstanceRequest.builder()
                // 填写需要获取数据源实例列表的业务空间id
                .workspaceId("")
                .build();
        ListVirtualDatasourceInstanceResponse listVirtualDatasourceInstanceResponse = client.listVirtualDatasourceInstance(listVirtualDatasourceInstanceRequest).join();
        Gson gson = new Gson();
        String jsonString = gson.toJson(listVirtualDatasourceInstanceResponse.getBody().getData());
        System.out.println(jsonString);
    }

    /**
     * 修改虚拟数据源实例的信息
     * @param client
     */
    public void update(AsyncClient client) {
        UpdateVirtualDatasourceInstanceRequest virtualDatasourceInstanceRequest = UpdateVirtualDatasourceInstanceRequest.builder()
                // 填写创建虚拟数据源实例所属的业务空间id
                .workspaceId("")
                // 虚拟数据源实例的名字
                .name("name")
                // 虚拟数据源实例的描述
                .description("description")
                // 虚拟数据源实例的唯一标识符id，可通过虚拟数据源实例列表获取
                .vdbId("vdb-id")
                .build();
        UpdateVirtualDatasourceInstanceResponse updateVirtualDatasourceInstanceResponse = client.updateVirtualDatasourceInstance(virtualDatasourceInstanceRequest).join();
        System.out.println(updateVirtualDatasourceInstanceResponse.getBody().getData());
    }

    /**
     * 删除虚拟数据源实例
     * @param client
     */
    public void delete(AsyncClient client){
        DeleteVirtualDatasourceInstanceRequest deleteVirtualDatasourceInstanceRequest = DeleteVirtualDatasourceInstanceRequest.builder()
                // 需要删除的虚拟数据源实例属于哪个业务空间
                .workspaceId("workspaceId")
                // 需要删除的虚拟数据源实例的唯一标识符id
                .vdbId("vdb-id")
                .build();
        DeleteVirtualDatasourceInstanceResponse deleteVirtualDatasourceInstanceResponse = client.deleteVirtualDatasourceInstance(deleteVirtualDatasourceInstanceRequest).join();
        System.out.println(deleteVirtualDatasourceInstanceResponse.getBody().getData());
    }

    /**
     * 向虚拟数据源添加ddl语句
     * @param client
     */
    public void addDdlForVirtualDatasource(AsyncClient client){
        SaveVirtualDatasourceDdlRequest saveVirtualDatasourceDdlRequest = SaveVirtualDatasourceDdlRequest.builder()
                // 需要添加ddl的虚拟数据源实例属于哪个业务空间
                .workspaceId("workspaceId")
                // 需要添加ddl的虚拟数据源实例的唯一标识符id
                .vdbId("vdb-id")
                // 需要添加的ddl语句，可以添加多个ddl语句，用";"隔开
                .ddl("CREATE TABLE user (id int NOT NULL AUTO_INCREMENT comment 'ID',name varchar(10) NOT NULL comment '姓名', dept_id int NOT NULL comment '部门ID', salary bigint NULL DEFAULT 0 comment '薪水',  PRIMARY KEY (`id`),   KEY `idx_name` (`name`),   KEY `d_id` (`dept_id`),    CONSTRAINT `d_id` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`)) COMMENT='用户表' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
                .build();
        SaveVirtualDatasourceDdlResponse  saveVirtualDatasourceDdlResponse = client.saveVirtualDatasourceDdl(saveVirtualDatasourceDdlRequest).join();
        System.out.println(saveVirtualDatasourceDdlResponse.getBody().getData());
    }

    /**
     * 授权关联数据源实例，将数据源与业务空间进行关联
     * @param client
     */
    public void createAuthorize(Client client){
        CreateDatasourceAuthorizationRequest createAuthorizeRequest = new CreateDatasourceAuthorizationRequest();
        // 关联的数据源实例的类型，具体类型可以参考sdk调用文档，关联虚拟数据源实例时，默认使用创建时所填写的类型
        createAuthorizeRequest.setType(51);
        // 关联的业务空间id
        createAuthorizeRequest.setWorkspaceId("workspaceId");
        // 如果关联的是虚拟数据源则需要添加虚拟数据源实例id
        createAuthorizeRequest.setVdbId("vdb-id");
        try {
            CreateDatasourceAuthorizationResponse createDatasourceAuthorizationResponse = client.createDatasourceAuthorization(createAuthorizeRequest);
            System.out.println(createDatasourceAuthorizationResponse.getBody().getData());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 关联数据源中的数据表到所指定的业务空间，智能问数将基于所关联的数据表来进行问答
     * @param client
     */
    public void syncRemoteTables(AsyncClient client){
        ArrayList<String> tableNames = new ArrayList<>();
        tableNames.add("user");
        SyncRemoteTablesRequest syncRemoteTablesRequest = SyncRemoteTablesRequest
                .builder()
                // 需要关联的数据表的业务空间
                .workspaceId("workspaceId")
                .tableNames(tableNames)
                .build();
        SyncRemoteTablesResponse syncRemoteTablesResponse = client.syncRemoteTables(syncRemoteTablesRequest).join();
        System.out.println(syncRemoteTablesResponse.getBody().getData());
    }

}
```

python

```
# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_dataanalysisgbi20240823.client import Client as DataAnalysisGBI20240823Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dataanalysisgbi20240823 import models as data_analysis_gbi20240823_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

workspace_id = 'ws_xxxxx'

class XiyanGbiService:
    def __init__(self) -> None:
        self._client = None
        self.create_client()

    def create_client(self) -> None:
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
        # Endpoint 请参考 https://api.aliyun.com/product/DataAnalysisGBI
        config.endpoint = f'dataanalysisgbi.cn-beijing.aliyuncs.com'
        self._client = DataAnalysisGBI20240823Client(config)

    def create_virtual_datasource_instance(self):
        create_virtual_datasource_instance_request = data_analysis_gbi20240823_models.CreateVirtualDatasourceInstanceRequest(
            workspace_id=workspace_id,
            name='name',
            description='description',
            type=51
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.create_virtual_datasource_instance_with_options(create_virtual_datasource_instance_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def list_virtual_datasource_instance(self):
        list_virtual_datasource_instance_request = data_analysis_gbi20240823_models.ListVirtualDatasourceInstanceRequest(
            workspace_id= workspace_id
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.list_virtual_datasource_instance_with_options(list_virtual_datasource_instance_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def update_virtual_datasource_instance(self):
        update_virtual_datasource_instance_request = data_analysis_gbi20240823_models.UpdateVirtualDatasourceInstanceRequest(
            workspace_id= workspace_id,
            name='name',
            description='description',
            vdb_id='vdb_id',
            type=51
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.update_virtual_datasource_instance_with_options(update_virtual_datasource_instance_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def delete_virtual_datasource_instance(self):
        delete_virtual_datasource_instance_request = data_analysis_gbi20240823_models.DeleteVirtualDatasourceInstanceRequest(
            workspace_id= workspace_id,
            # 需要添加ddl的虚拟数据源实例的唯一标识符id
            vdb_id='vdb_id',
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.delete_virtual_datasource_instance_with_options(delete_virtual_datasource_instance_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def save_virtual_datasource_ddl(self):
        save_virtual_datasource_ddl_request = data_analysis_gbi20240823_models.SaveVirtualDatasourceDdlRequest(
            workspace_id= workspace_id,
            # 需要添加ddl的虚拟数据源实例的唯一标识符id
            vdb_id='vdb_id',
            # 需要添加的ddl语句，可以添加多个ddl语句，用";"隔开
            ddl="CREATE TABLE user (id int NOT NULL AUTO_INCREMENT comment 'ID',name varchar(10) NOT NULL comment '姓名', dept_id int NOT NULL comment '部门ID', salary bigint NULL DEFAULT 0 comment '薪水',  PRIMARY KEY (`id`),   KEY `idx_name` (`name`),   KEY `d_id` (`dept_id`),    CONSTRAINT `d_id` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`)) COMMENT='用户表' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.save_virtual_datasource_ddl_with_options(save_virtual_datasource_ddl_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def create_datasource_authorization(self):
        create_datasource_authorization_request = data_analysis_gbi20240823_models.CreateDatasourceAuthorizationRequest(
            workspace_id=workspace_id,
            # 需要添加ddl的虚拟数据源实例的唯一标识符id
            vdb_id='vdb_id',
            type=51
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.create_datasource_authorization_with_options(create_datasource_authorization_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def sync_remote_tables(self):
        sync_remote_tables_request = data_analysis_gbi20240823_models.SyncRemoteTablesRequest(
            workspace_id= workspace_id,
            table_names=['table_1']
        )
        runtime = util_models.RuntimeOptions()
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            self._client.sync_remote_tables_with_options(sync_remote_tables_request, headers, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

if __name__ == '__main__':
    xiyanGbiService = XiyanGbiService()
    xiyanGbiService.create_virtual_datasource_instance()
```
