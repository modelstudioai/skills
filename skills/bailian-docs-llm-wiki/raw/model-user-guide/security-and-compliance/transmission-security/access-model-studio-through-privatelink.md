# 通过终端节点私网访问阿里云百炼模型或应用 API

为了在 VPC 内直接调用阿里云百炼的模型或应用 API，且确保流量不经过公网，可以在百炼控制台添加私网连接，将通信完全限制在阿里云内网。

## 工作原理

百炼网关支持以下两种接入方式：

-   **公网调用**：直接访问公网 MaaS 域名 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com`，流量经公网到达百炼。
-   **PrivateLink 私网连接**：在百炼控制台为 VPC 添加私网连接后，通过私网域名访问百炼，流量全程走阿里云内网，不经过公网。

在百炼控制台添加私网连接后，阿里云私网连接服务（PrivateLink）将为您的 VPC 与阿里云百炼建立一条私网连接（终端节点连接）。该连接为单向设计，仅允许您的 VPC 内的资源主动访问阿里云百炼，阿里云百炼无法通过此连接反向访问您 VPC 内的资源。

VPC 内的计算资源访问私网域名时，流量将通过 PrivateLink 转发至阿里云百炼服务端，不经过公网。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5798507871/CAEQYxiBgMCtvojh0RkiIDEzOTVhZTNhNGQxYTQ3YTQ5MjlhODJjZjM4MTY2NjQw5274221_20250627113930.173.svg)

阿里云百炼服务所在地域：

-   公共云：华北2（北京）、中国香港。
    
    > 其他地域暂不支持私网访问。
    

## 通过私网连接访问阿里云百炼 API

### 步骤一：在百炼控制台添加私网连接

1.  登录[百炼控制台](https://bailian.console.aliyun.com/)，在左侧导航栏选择**管理** > **网络配置**。
    
2.  首次使用时，在**添加私网连接**面板中按照指引完成以下准备：
    
    -   **授权私网连接服务关联角色**：单击**立即授权**，自动创建服务关联角色 `AliyunServiceRoleForBackrouterAccessNet`。
    -   **开通私网连接**：单击**立即开通**，开通私网连接（PrivateLink）服务。
3.  在**VPC私网访问**区域单击**添加**，配置以下各项参数，其他参数保持默认即可。
    
    -   **地域**：根据阿里云百炼服务地域选择，例如“**华北2（北京）**”。
    -   **VPC**：选择计划用于访问阿里云百炼服务的 VPC。私网连接将被创建到该 VPC 内，仅该 VPC 内的 ECS、容器等资源才能通过私网域名访问阿里云百炼服务。如无可用 VPC，可单击**创建VPC**跳转至专有网络控制台创建。
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

## 计费说明

使用私网连接（PrivateLink）会产生额外费用，可参考[私网连接计费说明](https://help.aliyun.com/zh/privatelink/private-link-billing-description)来了解和评估成本。

## 常见问题

1.  **为什么我的 ECS 实例无法通过私网连接访问阿里云百炼 API？**
    
    请按照以下步骤排查：
    
    1.  确认是否在同一 VPC。
        
        如果ECS实例的 VPC，与配置私网连接的 VPC 不同，则无法通过私网访问阿里云百炼 API，需要先配置 [VPC互连](https://help.aliyun.com/zh/vpc/cross-vpc-interconnection-overview/)。
        
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
