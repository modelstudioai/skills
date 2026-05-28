# 通过终端节点私网访问阿里云百炼模型或应用 API

为了在 VPC 内直接调用阿里云百炼的模型或应用 API，且确保流量不经过公网，可以创建私网终端节点，将通信完全限制在阿里云内网。

## **工作原理**

在专有网络（VPC）中创建接口终端节点后，阿里云私网连接服务（PrivateLink）将为您的VPC与阿里云百炼建立一条私网连接（终端节点连接）。该连接为单向设计，仅允许您的 VPC 内的资源主动访问阿里云百炼，阿里云百炼无法通过此连接反向访问您 VPC 内的资源。

VPC 内的计算资源访问终端节点时，流量将通过 PrivateLink 转发至阿里云百炼服务端，不经过公网。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3813439771/CAEQYxiBgMCtvojh0RkiIDEzOTVhZTNhNGQxYTQ3YTQ5MjlhODJjZjM4MTY2NjQw5274221_20250627113930.173.svg)

如需从其他地域的VPC内进行私网访问，请参考[跨地域私网访问阿里云百炼 API](#a576f2631au0h)。

阿里云百炼服务所在地域：

-   公共云：华北2（北京）、新加坡。
    
    > 美国（弗吉尼亚）地域暂不支持私网访问。
    

## **通过终端节点访问阿里云百炼 API**

### **步骤一：创建接口终端节点**

## 公共云

1.  登录[终端节点控制台](https://vpc.console.aliyun.com/endpoint/cn-beijing/endpoints)。
    
    > 如果首次使用终端节点，按照界面指引开通私网连接服务。
    
2.  在**接口终端节点**页签下，单击**创建终端节点**，并配置以下各项参数，其他参数保持默认即可。
    
    -   **所属地域**：根据阿里云百炼服务地域选择“**华北2（北京）**”或“**新加坡**”。
        
    -   **节点名称**：可自定义，例如“阿里云百炼私网连接点”。
        
    -   **终端节点类型**：选择**接口终端节点**。
        
    -   **终端节点服务**：选择**阿里云服务**，在下方输入框中筛选后选中**com.aliyuncs.dashscope**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4538798271/p857590.png)
        
    -   **专有网络**：选择计划用于访问阿里云百炼服务的 VPC。终端节点将被创建到 VPC 内，VPC 内的 ECS、容器等资源才能通过私网域名访问阿里云百炼服务。
        
    -   **可用区与交换机**：接口终端节点会在所选交换机对应的可用区中，创建终端节点网卡（Endpoint ENI）用于接收来自 VPC 内部的私网流量。建议至少选择两个不同可用区的交换机，以实现高可用：当某个可用区发生故障时，流量可自动切换至其他可用区的网卡，避免服务中断。
        
    -   **安全组**：选择关联到终端节点网卡的安全组，用于控制谁可以访问该终端节点。因此请确保安全组在入方向允许 80（http）、443（https）访问。
        
3.  单击**确定创建**，完成创建。
    

### **步骤二：获取**终端节点服务域名

## 公共云

完成接口终端节点创建后，可以在接口终端节点的详情页中获取服务域名，用于后续私网访问阿里云百炼 API。

**默认服务域名**仅支持 HTTP 协议，如需 HTTPS 访问，可使用**自定义服务域名**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8721814471/p936726.png)

### **步骤三：调用验证**

将阿里云百炼 API base\_url 中的域名，替换为上一步骤中获取到的终端节点服务域名，然后在对应 VPC 发起调用即可。

## 公共云

以 OpenAI 兼容模式调用北京地域的[通义千问文本模型](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#a9b7b197e2q2v)为例：

-   替换前：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
    
-   替换后：
    
    -   **默认服务域名**：`http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/compatible-mode/v1/chat/completions`
        
    -   **自定义服务域名**：`https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
        

调用示例：

## HTTP

```
# 将原始域名替换为上一步骤中获取到的终端节点服务域名
curl -X POST http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/compatible-mode/v1/chat/completions \
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

## OpenAI Python SDK

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 将原始域名替换为上一步骤中获取到的终端节点服务域名
    base_url="http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-flash",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)
print(completion.model_dump_json())
```

## DashScope Python SDK

```
import os
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
import dashscope
from dashscope import Generation

# 将原始域名替换为上一步骤中获取到的终端节点服务域名
dashscope.base_http_api_url = "http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1"
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

## DashScope Java SDK

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
        // 将原始域名替换为上一步骤中获取到的终端节点服务域名
        Generation gen = new Generation(Protocol.HTTP.getValue(), "http://ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com/api/v1");
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

> 调用前，需要您已完成[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。如需要直接传入 API Key，请将`$DASHSCOPE_API_KEY` 替换为您的 API Key。

## **跨地域私网访问**阿里云**百炼 API**

百炼服务部署在华北2（北京）和新加坡。从其他地域 VPC 内私网访问百炼 API 时，根据互通范围选择以下方式之一：

-   **同境内或同境外跨地域**（例如华东1（杭州）VPC 调用华北2（北京）百炼）：推荐使用[方式一：启用跨地域端点](#1850951664d08)。
    
-   **跨境跨地域**（中国内地与境外之间，例如华北2（北京）VPC 调用新加坡百炼）：使用[方式二：通过 CEN 跨地域 VPC 互通](#8761dd25447d4)。
    

### **方式一：启用跨地域端点（推荐）**

详细操作参见 [使用接口终端节点访问跨地域的阿里云服务](https://help.aliyun.com/zh/privatelink/create-and-manage-endpoints/#231de8ecd49y6)。百炼场景的关键配置：

-   **地域**：选择发起端 VPC 所在地域。
    
-   **类型**：选择**阿里云服务**。
    
-   **服务地域**：勾选**启用跨地域端点**，并选择**华北2（北京）**或**新加坡**。
    
-   **终端节点服务**：从下方列表中选择 `com.aliyuncs.dashscope`。
    
-   **跨地域配置**：跨地域流量费由 CDT 结算；带宽根据互通范围分级（中国内地与中国内地互通默认 1000 Mbps；非中国内地与非中国内地互通默认 100 Mbps）。
    

其他参数与同地域配置一致。完成后，在终端节点关联的安全组中添加入方向规则，允许发起端 VPC 内资源访问 80、443 端口。

> 方式一不支持中国内地与境外之间的互通。如需跨境访问，请使用方式二。

配置完成后，在发起端 VPC 内访问该终端节点的默认服务域名时，PrivateLink 直接将流量路由至阿里云百炼服务所在地域，实现跨地域私网访问。

### **方式二：通过云企业网（CEN）跨地域 VPC 互通（适用于跨境场景）**

用于中国内地与境外之间的跨境跨地域访问。终端节点须与百炼服务位于同一地域，通过 CEN 实现跨地域 VPC 互通：

1.  参考前文，完成[通过终端节点访问阿里云百炼 API](#77efa790086jo)的配置。
    
2.  通过云企业网（CEN）配置[跨地域VPC互通](https://help.aliyun.com/zh/cen/getting-started/inter-region-vpc-interworking)。需要注意：
    
    -   请在两端选择不同网段的 VPC，避免网段冲突导致互通失败。
        
    -   中国内地和其他地域之间通过 CEN 实现跨地域 VPC 互通，需要按照控制台提示提交申请。审批时间通常为 1~2 工作日，更多问题可查阅[跨境常见问题](https://help.aliyun.com/zh/cen/support/faq-about-cross-border-network-communication)。
        
3.  在终端节点关联的安全组中，添加入方向规则，允许发起端内的资源访问 80、443 端口。
    

配置完成后，在发起端 VPC 内访问前文中配置好的终端节点默认服务域名时，转发路由器（TR）会将流量路由至阿里云百炼服务所在地域的终端节点，实现跨地域私网访问阿里云百炼 API。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3813439771/CAEQZhiBgICUtYmu2RkiIDk3YWZiYjVkYWUyNTQwNDI4ZTQyZGMyMTk5MDIyYzg45274221_20250627113930.173.svg)

默认情况下，终端节点的默认服务域名可以在跨地域互联的 VPC 内直接被访问，但自定义服务域名仅在终端节点所在地域 VPC 内有效。因此，如需在发起端通过自定义域名私网访问阿里云百炼 API ，可参考[快速使用内网域名解析](https://help.aliyun.com/zh/dns/pvtz-quickly-use-the-built-in-domain-name-resolution)，创建一个与自定义服务域名同名的内网域名，将该域名通过 CNAME 记录解析至该终端节点的默认服务域名：

1.  添加一条和自定义服务域名同名的内网权威域名，如：`vpc-cn-beijing.dashscope.aliyuncs.com`，生效范围选择发起端 VPC。
    
2.  添加解析记录：记录类型选择 **CNAME**，主机记录输入`@`，记录值填写目标终端节点的默认服务域名，如：`ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com`。
    
    **注意**：进行内网域名解析配置时，主机记录或完整域名中请勿使用下划线（\_），否则可能导致API调用失败。建议域名仅包含字母、数字和短划线（-），例如`test-for-dns.dashscope.aliyuncs.com`，而不是`test_for_dns.dashscope.aliyuncs.com`。
    

配置完成后，即可在发起端 VPC 内通过自定义服务域名访问阿里云百炼 API。若使用不同名的内网域名进行配置，请参见[配置内网域名解析](#3b86fad821p5p)。

## **计费说明**

使用私网连接（PrivateLink）和内网域名解析（Private Hosted Zone）会产生额外费用；跨境场景另需云企业网（CEN）跨地域费用。可参考对应计费说明来了解和评估成本：

-   [私网连接计费说明](https://help.aliyun.com/zh/privatelink/private-link-billing-description)
    
-   [云企业网计费说明](https://help.aliyun.com/zh/cen/product-overview/billing-rules)（仅跨境场景使用）
    
-   [内网域名解析计费说明](https://help.aliyun.com/zh/dns/pvtz-product-billing)
    

## **常见问题**

1.  **为什么我的 ECS 实例无法通过私网链接访问阿里云百炼 API？**
    
    请按照以下步骤排查：
    
    1.  确认是否在同一 VPC。
        
        如果ECS实例的 VPC，与配置终端节点的 VPC 不同，则无法通过私网访问阿里云百炼 API，需要先配置 [VPC互连](https://help.aliyun.com/zh/vpc/cross-vpc-interconnection-overview/)。
        
    2.  检查终端节点关联的安全组，确认已添加入方向规则，允许来自发起端ECS实例所在网段对 80（HTTP）或 443（HTTPS）端口的访问。
        
    3.  确认终端节点服务域名。
        
        通过默认服务域名私网访问阿里云百炼平台仅支持 HTTP。
        
2.  **终端节点能否从公网访问？**
    
    不可以。私网连接（PrivateLink）仅用于在阿里云内网建立私有连接。终端节点不具备公网访问能力，终端节点网卡也无法绑定弹性公网IP (EIP)。
    
3.  **为什么使用**[**内网域名解析**](https://help.aliyun.com/zh/dns/pvtz-quickly-use-the-built-in-domain-name-resolution)**时，通过我自定义的域名调用模型报错？**
    
    该问题通常是由于您在配置内网域名解析时，使用的主机记录（或完整域名）包含了下划线（\_）等不合规字符。建议域名由字母、数字和短划线（-）组成。
    
    您可参考以下方法配置解析记录：
    
    1.  **权威域名**：在内网域名解析中，为 `dashscope.aliyuncs.com` 权威域名添加解析记录。
        
    2.  **主机记录**：记录类型选择 **CNAME**，输入您的自定义域名前缀，例如 `test-for-dns-right`。**请注意**：主机记录不可使用下划线（\_）。
        
        **正确示例**
        
        **错误示例**
        
        ![2025-12-17\_19-47-04](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8354116671/p1036091.jpg)
        
        ![2025-12-17\_19-47-44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8354116671/p1036092.jpg)
        
    3.  **记录值**：填写百炼终端节点的默认服务域名。例如：`ep-***.dashscope.cn-beijing.privatelink.aliyuncs.com`。
        
    
    配置完成后，即可通过 `https://test-for-dns-right.dashscope.aliyuncs.com/api/v1`（OpenAI兼容模式为`https://test-for-dns-right.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`）进行模型调用。
    
    > 使用带下划线的域名 `https://test_for_dns_wrong.dashscope.aliyuncs.com/api/v1` 会导致调用报错。
