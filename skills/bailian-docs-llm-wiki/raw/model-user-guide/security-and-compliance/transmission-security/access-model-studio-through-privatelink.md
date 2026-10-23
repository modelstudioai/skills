# 通过终端节点私网访问阿里云百炼模型或应用 API

为了在 VPC 内直接调用阿里云百炼的模型或应用 API，且确保流量不经过公网，可以在百炼控制台添加私网连接，将通信完全限制在阿里云内网。

## 工作原理

百炼网关支持以下两种接入方式：

-   **公网调用**：直接访问公网 MaaS 域名 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com`，流量经公网到达百炼。
-   **PrivateLink 私网连接**：在百炼控制台为 VPC 添加私网连接后，通过私网域名访问百炼，流量全程走阿里云内网，不经过公网。

在百炼控制台添加私网连接后，阿里云私网连接服务（PrivateLink）将为您的 VPC 与阿里云百炼建立一条私网连接（终端节点连接）。该连接为单向设计，仅允许您的 VPC 内的资源主动访问阿里云百炼，阿里云百炼无法通过此连接反向访问您 VPC 内的资源。

VPC 内的计算资源访问私网域名时，流量将通过 PrivateLink 转发至阿里云百炼服务端，不经过公网。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5798507871/CAEQYxiBgMCtvojh0RkiIDEzOTVhZTNhNGQxYTQ3YTQ5MjlhODJjZjM4MTY2NjQw5274221_20250627113930.173.svg)

阿里云百炼私网访问支持的地域（以控制台地域下拉列表为准）：

-   华北2（北京）
-   华东2（上海）
-   华东1（杭州）
-   华南1（深圳）
-   华北6（乌兰察布）
-   华北3（张家口）

## 通过私网连接访问阿里云百炼 API

### 步骤一：在百炼控制台添加私网连接

1.  登录[百炼控制台](https://bailian.console.aliyun.com/)，单击页面右上角的**设置**，选择**网络配置**。
    
2.  首次使用时，在**添加私网连接**面板中按照指引完成以下准备：
    
    -   **授权私网连接服务关联角色**：单击**立即授权**，自动创建服务关联角色 `AliyunServiceRoleForBackrouterAccessNet`。
    -   **开通私网连接**：单击**立即开通**，开通私网连接（PrivateLink）服务。
3.  在**VPC私网访问**区域单击**添加**，配置以下各项参数，其他参数保持默认即可。
    
    -   **地域**：根据阿里云百炼服务地域选择，例如“**华北2（北京）**”。
    -   **VPC**：选择计划用于访问阿里云百炼服务的 VPC。私网连接将被创建到该 VPC 内，仅该 VPC 内的 ECS、容器等资源才能通过私网域名访问阿里云百炼服务。如无可用 VPC，可单击**创建VPC**跳转至专有网络控制台创建。如需使用其他账号共享的 VPC，直接选择该共享 VPC，具体参见[跨账号访问](#cross-account-vpc-sharing)。
    -   **可用区与交换机**：选择阿里云百炼支持且包含交换机的可用区及对应交换机。私网连接会占用所选可用区下交换机的一个内网 IP 地址，作为百炼私网域名的内网解析地址。最多可添加 2 个可用区与交换机组合，建议添加 2 个以实现高可用：当某个可用区发生故障时，流量可自动切换至其他可用区，避免服务中断。如无可用交换机，可单击**创建交换机**跳转至专有网络控制台创建。
    -   **安全组**：选择关联到私网连接的安全组，用于控制谁可以访问该私网连接。因此请确保安全组在入方向允许 443（https）访问。如无可用安全组，可单击**创建安全组**跳转至云服务器 ECS 控制台创建。
4.  单击**确认**，等待**状态**变为**创建成功**。添加完成后预计延迟 1～3min 生效，生效期间该 VPC 下任意云服务器均可使用私网域名访问百炼服务。
    

### 步骤二：关联业务空间

需要通过私网访问阿里云百炼的业务空间，须与私网连接建立关联。

1.  在百炼控制台左侧导航栏选择**业务空间管理**，新建业务空间或编辑目标业务空间。
2.  在**高级配置**中，将**私网连接**设置为目标私网连接。下拉选项展示终端节点 ID 及其所属地域和 VPC；如无目标选项，可在下拉框中单击**新建私网连接**创建。关联后，该业务空间可通过对应 VPC 的私网连接访问百炼服务。
3.  如需解除关联：编辑业务空间并清空**私网连接**后保存；或在**网络配置**页面展开目标私网连接行，在**关联业务空间**中单击**解绑**，跳转至对应业务空间处理。已关联业务空间的私网连接需先解绑才能删除。

### 步骤三：获取私网域名

完成步骤二的关联后，系统为每个已关联的业务空间生成私网域名。在**网络配置**页面的**VPC私网访问**列表中展开目标私网连接，在 **Endpoint** 列获取私网域名，**关联业务空间**列展示该域名所属的业务空间 ID。私网域名格式为 `{WorkspaceId}-{VpcId}.{地域ID}.maas.aliyuncs.com`，其中 `WorkspaceId` 为业务空间 ID，`VpcId` 为私网连接所属的 VPC ID。

您也可以在左侧导航栏选择**业务空间管理**，在目标业务空间的 **API Host** 列查看**私网**域名。

私网域名仅在所选 VPC 内可解析和访问，通过 HTTPS（443 端口）调用阿里云百炼 API。未关联业务空间时，展开行的 **Endpoint** 列为空。

### 步骤四：调用验证

将阿里云百炼 API base\_url 中的域名，替换为上一步骤中获取到的私网域名，然后在对应 VPC 发起调用即可。

以 OpenAI 兼容模式调用[通义千问文本模型](raw/model-api-reference/qwen-api-reference.md)为例：

-   替换前：`https://{WorkspaceId}.{RegionId}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`
-   替换后：`https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

调用示例：

HTTP

```
# 将原始域名替换为上一步骤中获取到的私网域名
curl -X POST https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-flash",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}'
```

OpenAI Python SDK

```
import os
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 将原始域名替换为上一步骤中获取到的私网域名
    base_url="https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-flash",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)
print(completion.model_dump_json())
```

DashScope Python SDK

```
import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
import dashscope
from dashscope import Generation
# 将原始域名替换为上一步骤中获取到的私网域名
dashscope.base_http_api_url = "https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/api/v1"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
messages = [{
    'role': 'user', 'content': '你是谁？'
}]
response = Generation.call(
    model="qwen-flash",
    messages=messages,
    result_format='message'
)
if response.status_code == HTTPStatus.OK:
    print(response)
else:
    print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
        response.request_id, response.status_code,
        response.code, response.message
    ))
```

DashScope Java SDK

```
// 建议DashScope SDK的版本 >= 2.12.0
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.utils.JsonUtils;
public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        // 将原始域名替换为上一步骤中获取到的私网域名
        Generation gen = new Generation(Protocol.HTTP.getValue(), "https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/api/v1");
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-flash")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 打印错误信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
    }
}
```

> 调用前，需要您已完成[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。如需要直接传入 API Key，请将`$DASHSCOPE_API_KEY` 替换为您的 API Key。

## 跨账号访问

默认情况下，私网连接只能创建在当前账号的 VPC 内，且仅该 VPC 内的资源可以通过私网域名访问百炼。如果调用方资源所在 VPC 属于其他阿里云账号，可以选择以下任一方式：

-   **方式一：VPC 共享**：将调用方 VPC 的交换机共享给百炼账号，私网连接直接创建在调用方 VPC 内。
-   **方式二：VPC 互联**：私网连接创建在百炼账号自己的 VPC 内，调用方 VPC 通过 VPC 对等连接或云企业网与该 VPC 互联后访问该私网连接。

两种方式都不需要在账号之间共享私网连接本身。调用方不是百炼账号时，由百炼账号将私网域名和业务空间 API Key 提供给调用方。

### 方式一：VPC 共享

VPC 共享涉及两个账号：

-   **VPC 所有者账号**：拥有 VPC 和交换机，负责共享交换机。
-   **百炼账号**：接受共享，在百炼控制台添加私网连接并关联业务空间。

私网连接创建在共享 VPC 内，该 VPC 内属于任一账号的资源都可以使用这条连接。也可以由 VPC 所有者账号自己在该 VPC 内创建私网连接，供共享 VPC 内的其他账号使用。无论哪种情况，PrivateLink 费用都由创建私网连接的账号承担。以下以百炼账号创建私网连接为例。

#### 步骤一：VPC 所有者账号共享交换机

登录资源共享控制台，单击**创建共享单元**，依次完成**配置基本信息并添加资源**（添加需要共享的交换机）、**关联权限**（选择 `AliyunRSDefaultPermissionVSwitch`）、**关联资源使用者**（输入百炼账号的 UID）和**确认并提交**。共享的是交换机而不是整个 VPC，详细操作参见[共享 VPC](https://help.aliyun.com/zh/vpc/vpc-sharing)。

#### 步骤二：百炼账号接受共享

使用百炼账号登录资源共享控制台，在**共享给我**页面接受共享。如果共享单元已自动关联，可跳过此步。

#### 步骤三：百炼账号添加私网连接

登录百炼控制台，按本文[步骤一](#726a487d813ji)添加私网连接。配置时注意：

-   **地域**：选择共享 VPC 所在地域，且该地域需支持百炼私网访问。
-   **VPC**：选择共享过来的 VPC。
-   **可用区与交换机**：选择共享 VPC 下的共享交换机。
-   **安全组**：选择共享 VPC 内可用的安全组，并确保入方向允许调用方资源访问 443 端口。

其他参数与同账号流程一致。

#### 步骤四：完成后续配置并调用

私网连接创建成功后，按本文[步骤二](#2e9d4c7b61pvl)、[步骤三](#7688834737rep)、[步骤四](#2559e347f69hu)关联业务空间并获取私网域名。调用方在共享 VPC 内使用该私网域名和业务空间 API Key 发起调用。

### 方式二：VPC 互联

VPC 互联涉及两个账号：

-   **百炼账号**：在自己的 VPC（下称百炼 VPC）内创建私网连接并关联业务空间。
-   **调用方账号**：拥有调用方资源所在的 VPC（下称调用方 VPC）。

VPC 互联后两个 VPC 的网络是双向连通的，任一账号都可以在自己的 VPC 内创建私网连接供另一账号调用，即两个账号都可以作为百炼账号。

#### 步骤一：打通网络

通过以下任一方式连通百炼 VPC 与调用方 VPC，两端 VPC 网段不能重叠。两种方式的选型和计费对比参见[VPC 互联概述](https://help.aliyun.com/zh/vpc/cross-vpc-interconnection-overview)。

-   **VPC 对等连接**
    
    1.  任一账号在专有网络控制台创建对等连接，**接收端账号类型**选择**跨账号**，并填写对端账号 UID 和对端 VPC ID。
    2.  对端账号在专有网络控制台的 VPC 对等连接页面接收该连接。
    3.  两端账号分别在各自 VPC 的路由表中添加路由，目标网段为对端 VPC 网段，下一跳为该对等连接。
    
    详细操作参见[VPC 对等连接](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)。
    
-   **云企业网**
    
    1.  任一账号创建云企业网实例，并在 VPC 所在地域创建转发路由器。
    2.  对端账号将自己的 VPC 授权给该云企业网实例。
    3.  在转发路由器中为两个 VPC 分别创建 VPC 连接，将两个 VPC 接入同一个转发路由器。
    
    详细操作参见[使用企业版转发路由器实现跨地域跨账号 VPC 互通](https://help.aliyun.com/zh/cen/getting-started/use-enterprise-edition-transit-routers-to-connect-vpcs-across-regions-and-accounts)。
    

#### 步骤二：放行私网连接安全组

网络打通后，调用方仍需经过私网连接安全组的放行才能访问私网连接。百炼账号在私网连接关联的安全组中添加以下入方向规则：

参数

取值

授权策略

允许

协议类型

自定义 TCP

端口范围

443

授权对象

调用方 VPC 网段，例如 `192.168.0.0/16`。可在专有网络控制台的 VPC 详情页查看

未放行时，即使网络已打通，调用也会连接超时。

#### 步骤三：发起调用

百炼账号将私网域名和业务空间 API Key 提供给调用方账号，调用方 VPC 内的资源按本文[步骤四](#2559e347f69hu)发起调用。如果返回 `Failed to connect to <私网域名> port 443` 等连接超时错误，请检查步骤一的网络配置和步骤二的安全组规则。

## 计费说明

使用私网连接（PrivateLink）会产生额外费用，可参考[私网连接计费说明](https://help.aliyun.com/zh/privatelink/private-link-billing-description)来了解和评估成本。

私网连接和模型调用费用由创建该私网连接的账号承担，与 VPC 属于哪个账号无关。VPC 对等连接和云企业网计费参见[VPC 对等连接](https://help.aliyun.com/zh/vpc/vpc-peer-to-peer-connection)和[云企业网计费规则](https://help.aliyun.com/zh/cen/product-overview/billing-rules)。

## 常见问题

1.  **为什么我的 ECS 实例无法通过私网连接访问阿里云百炼 API？**
    
    请按照以下步骤排查：
    
    1.  确认是否在同一 VPC。
        
        如果ECS实例的 VPC，与配置私网连接的 VPC 不同，则无法通过私网访问阿里云百炼 API，需要先配置 [VPC互连](https://help.aliyun.com/zh/vpc/cross-vpc-interconnection-overview/)，例如 VPC 对等连接或云企业网，并放行私网连接安全组，具体参见[方式二：VPC 互联](#cross-account-vpc-interconnection)。
        
    2.  检查私网连接关联的安全组，确认已添加入方向规则，允许来自发起端ECS实例所在网段对 443（HTTPS）端口的访问。
        
    3.  确认私网连接状态。
        
        私网连接状态为**创建成功**且已生效（添加完成后预计延迟 1～3min）后，才能通过私网域名访问阿里云百炼 API。
        
    4.  确认业务空间已关联。
        
        私网域名在业务空间与私网连接关联后才生成。如果展开行的 **Endpoint** 列为空，请先按步骤二关联业务空间。
        
2.  **终端节点能否从公网访问？**
    
    不可以。私网连接（PrivateLink）仅用于在阿里云内网建立私有连接。终端节点不具备公网访问能力，终端节点网卡也无法绑定弹性公网IP (EIP)。
    
3.  **通过旧方式创建的存量私网连接，还需要关联业务空间吗？**
    
    不需要。此前在私网连接（专有网络 VPC）控制台创建接口终端节点所建立的存量私网连接，默认关联所有业务空间，可直接用于私网访问阿里云百炼 API，无需执行步骤二。
    
    在**网络配置**页面展开存量私网连接，**Endpoint** 列展示 `vpc-{地域ID}.dashscope.aliyuncs.com`（例如 `vpc-cn-beijing.dashscope.aliyuncs.com`），**关联业务空间**列显示**所有业务空间**；这与新流程按业务空间逐条展示 `{WorkspaceId}-{VpcId}.{地域ID}.maas.aliyuncs.com` 不同。
    
    旧方式已不再支持创建新的私网连接。如需新增，请按步骤一在百炼控制台创建，并按步骤二关联需要私网访问的业务空间。
