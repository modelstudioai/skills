# 机密推理

百炼机密推理服务基于硬件机密计算技术，面向高安全等级场景，数据在传输、计算和存储过程中均处于加密状态，保障用户提示词在云端推理过程中的隐私与安全。

<a id="1-机密推理简介"></a>

<a id="h2sec1overview"></a>

## 1 机密推理简介

机密推理基于 TEE（可信执行环境）硬件级机密计算技术构建，可有效抵御包括特权攻击在内的多层次安全威胁。其核心安全特性包括：

-   **端到端加密**：在 HTTPS 之上建立业务层加密通道，覆盖从客户端到机密推理节点的完整链路。每台节点随机生成根私钥用于会话密钥协商，每次会话独立派生临时密钥；所有密钥仅驻留于加密的易失性存储中，不落盘、不持久化，会话结束即销毁。
-   **安全加固与度量**：依托芯片级硬件隔离与软件加固双重机制，对启动链路及运行时环境实施全链路度量；块存储层面，根分区基于 Merkle Tree 机制保障完整性，数据分区采用一次性密钥加密保障机密性。
-   **软硬件透明度**：客户端直接访问 TEE 厂商验证硬件生成的远程证明报告真实性，并检查透明日志服务以确认服务端软件制品的完整性。

支持的模型及价格详见[计费说明](confidential-inference.md#h2sec5billing)。

适用对象：对数据安全有较高要求的企业级场景，典型行业见[应用场景](confidential-inference.md#h2sec7scenario)。

使用流程：

<a id="code-block"></a>

```text
开通服务（签署《特别规则》）
  │
  ▼
创建部署（每个要使用的模型独立创建）
  │
  ▼
SDK 调用（model 参数 = 部署列表的「模型Code」）
```

<a id="2-机密推理优势"></a>

<a id="h2sec2advantages"></a>

## 2 机密推理优势

-   **纵深安全防护**：从芯片级硬件隔离、端到端加密传输到客户端可验证的远程证明，构建覆盖硬件、传输与软件的多层防护体系。平台不留存明文提示词、模型输出与加密密钥，密钥与内容由用户掌握。
-   **低侵入式接入**：兼容现有调用方式，业务代码无需重构，仅需替换调用入口与客户端 SDK，机密与非机密路径可在同一账号下并存。调用方式详见[部署后调用](confidential-inference.md#h2sec6call)。

<a id="3-计费说明"></a>

<a id="h2sec5billing"></a>

## 3 计费说明

机密推理部署按 Token 目录价计费，分输入、输出、上下文缓存（隐式）命中三项。

支持的模型：`cmaas-qwen3.8-flash`、`cmaas-glm-5.3`、`cmaas-glm-5.2`（即将下线）、`cmaas-deepseek-v4.1-flash`、`cmaas-deepseek-v4-flash-0731`、`cmaas-deepseek-v4-pro-0813`。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

<a id="sec-tabs-2"></a>

<a id="qwen"></a>

<a id="qwen-h4"></a>

#### Qwen

| 模型 code | **输入**<br><br>**元/百万 token** | **输出**<br><br>**元/百万 token** | **缓存命中**<br><br>**元/百万 token** |
| --- | --- | --- | --- |
| `cmaas-qwen3.8-flash` | 3.2 | 10 | 0.4 |

<a id="glm"></a>

<a id="glm-h4"></a>

#### GLM

| 模型 code | **输入**<br><br>**元/百万 token** | **输出**<br><br>**元/百万 token** | **缓存命中**<br><br>**元/百万 token** |
| --- | --- | --- | --- |
| `cmaas-glm-5.3` | 16 | 56 | 4 |
| `cmaas-glm-5.2`（即将下线） | 16 | 56 | 4 |

<a id="deepseek"></a>

<a id="deepseek-h4"></a>

#### DeepSeek

<table><thead><tr><th><p><strong>模型 code</strong></p></th><th><p><strong>输入</strong></p><p><strong>元/百万 token</strong></p></th><th><p><strong>输出</strong></p><p><strong>元/百万 token</strong></p></th><th><p><strong>缓存命中</strong></p><p><strong>元/百万 token</strong></p></th></tr></thead><tbody><tr><td><p><code>cmaas-deepseek-v4.1-flash</code></p></td><td><p>4</p></td><td><p>16</p></td><td><p>0.08</p></td></tr><tr><td rowspan="2"><p><code>cmaas-deepseek-v4-flash-0731</code></p></td><td><p>6（忙时）</p></td><td><p>18（忙时）</p></td><td><p>0.6（忙时）</p></td></tr><tr><td><p>3（闲时）</p></td><td><p>9（闲时）</p></td><td><p>0.3（闲时）</p></td></tr><tr><td><p><code>cmaas-deepseek-v4-pro-0813</code></p></td><td><p>27</p></td><td><p>54</p></td><td><p>2.7</p></td></tr></tbody></table>

> 忙时：北京时间 8:00 - 22:00，闲时：北京时间 22:00 - 次日 8:00。

计费公式：

<a id="code-block-2"></a>

```text
总费用 = ((输入 token - 隐式缓存命中 token) × 输入单价 + 缓存命中 token × 缓存命中单价 + 输出 token × 输出单价) ÷ 1,000,000
```

<a id="4-开通与部署"></a>

<a id="h2sec3open"></a>

## 4 开通与部署

开通机密推理需满足以下前提：

1.  **开通服务**：需联系阿里云商务申请开通。
2.  **地域**：当前支持华北2（北京）地域。
3.  **合规签署**：部署前须签署[《阿里云百炼机密推理服务特别规则》](https://terms.alicdn.com/legal-agreement/terms/common_product_agreement/20260529140548196/20260529140548196.html)。

进入[机密推理页面](https://bailian.console.aliyun.com/cn-beijing/model/confidential-inference)后，若提示“尚未开通百炼机密推理服务（按量付费）商品”，请按页面引导阅读《特别规则》并单击“请确认开通并使用”完成开通。

<a id="创建部署"></a>

<a id="h2sec4deploy"></a>

### 创建部署

部署前需确认业务侧使用机密推理支持的模型（见计费说明）。

部署步骤：

1.  登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/confidential-inference)，在左侧导航栏选择**模型推理** > **机密推理**，进入机密推理页面（页面展示已有部署列表，包含模型 Code、计费方式、限流详情、创建时间与操作等信息），单击**创建机密推理**。
2.  在弹窗中配置部署参数：在**选择模型**下拉中选择模型（已创建部署的模型会显示“已部署”标记）；**计费方式**固定为“按Token计费”；**限流配置**中 TPM/RPM 会在选定模型后自动按上限值填充，无需编辑。
3.  单击**确定创建**，部署完成后列表新增对应记录。

> **说明**
>
> 每个模型需创建一个独立的部署才能调用；调用时使用的模型 Code 即部署列表中的“模型Code”列。

部署参数说明见下表。计费按 Token 目录价（详见[计费说明](confidential-inference.md#h2sec5billing)）；TPM/RPM 默认按上限值配置，无需编辑。

<table><thead><tr><th><strong>参数</strong></th><th><strong>说明与取值</strong></th></tr></thead><tbody><tr><td><p>选择模型</p></td><td><p>支持的模型见<a href="confidential-inference.md#h2sec5billing">计费说明</a></p></td></tr><tr><td><p>计费方式</p></td><td><p>按 Token 目录价计费（输入/输出/缓存命中三项）</p></td></tr><tr><td><p>TPM 每分钟 Token 数</p></td><td><p>每分钟 Token 限流上限，默认按上限值配置（未申请提升时默认 500000）；接近上限会被限流；</p></td></tr><tr><td><p>RPM 每分钟请求数</p><blockquote><p>当前密钥协商请求也计入 RPM 限额，因此实际可用的推理 RPM 可能略低于配置值。</p></blockquote></td><td><p>每分钟请求限流上限，默认按上限值配置（未申请提升时默认 300）；</p></td></tr></tbody></table>

部署后监控指标见下表，据此判断是否需要扩容或优化 prompt。

| 指标名称 | 含义 | 正常范围 | 异常操作建议 |
| --- | --- | --- | --- |
| Token 用量 | 单位时间内的输入、输出与缓存命中 token 消耗量 | 低于配置的 TPM 限流上限 | 用量突增时排查业务请求量与 prompt 长度，必要时评估扩容或优化 prompt 结构 |
| 缓存命中率 | 命中缓存的请求占请求总量的比例 | 越高越省成本（无固定阈值） | 命中率偏低时优化 prompt 结构提升复用度，提高单位综合成本优势 |
| 资源池占用 | 独立资源池的容量使用情况 | 不溢出（独立资源池完全不会溢出） | 无需处理 |

> **说明**
>
> 部署后可查看详情、扩缩容或释放部署。删除/释放通常不可恢复，请谨慎操作。

<a id="5-部署后调用"></a>

<a id="h2sec6call"></a>

## 5 部署后调用

模型部署成功后，支持通过机密推理 SDK 调用。

调用示例中的 `{WorkspaceId}` 为业务空间 ID：在控制台顶栏单击当前业务空间（如“默认业务空间”）展开下拉，单击“管理业务空间”，在业务空间管理页面的“业务空间ID”列查看（形如 `ws-xxxxxxxxxxxxxxx`）；“API Host”列的公网地址即调用域名。

<a id="sdk-安装与构建"></a>

<a id="call-h3-sdk-install"></a>

### SDK 安装与构建

前提条件：

-   已安装 Go 开发环境。更多信息，请参见[安装 Go](https://golang.org/doc/install)。
-   已安装 make 编译工具。

安装好[机密推理 SDK](https://github.com/dashscope/dashscope-confidential-maas)之后，在 SDK 根目录下执行 `make` 命令，在 `bin` 目录下构建出机密推理样例命令行程序 cmaas-client 与本地 API 转换代理工具 openai-proxy/anthropic-proxy。您也可参考 SDK 目录中 README 文档，自行开发构建适用于业务场景的机密推理工具。

<a id="sec-tabs-3"></a>

<a id="使用机密推理命令行工具-cmaas-client"></a>

<a id="使用机密推理命令行工具-cmaas-client-h4"></a>

#### 使用机密推理命令行工具 cmaas-client

<a id="code-block-3"></a>

```bash
# MacOS/Linux
# 请将您的百炼API Key配置在环境变量中
export DASHSCOPE_API_KEY="sk-xxx"
# 请将 --model 后的参数替换为实际模型code
./cmaas-client --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --model <code> --prompt "简短介绍大语言模型" --stream

# Windows Powershell
$env:DASHSCOPE_API_KEY = "sk-xxx"
.\cmaas-client.exe --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --model <code> --prompt "简短介绍大语言模型" --stream
```

<a id="openai-proxy-openai-兼容接口"></a>

<a id="openai-proxy-openai-兼容接口-h4"></a>

#### openai-proxy（OpenAI 兼容接口）

基于 SDK 构建了 OpenAI 兼容接口的 HTTP 本地代理工具，便于集成现有 OpenAI 客户端。

1.  本地启动 `openai-proxy` 代理工具

<a id="code-block-4"></a>

```bash
# MacOS/Linux
# 请将您的百炼API Key配置在环境变量中
export DASHSCOPE_API_KEY="sk-xxx"
./openai-proxy --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --listen :8080

# Windows Powershell
# 请将您的百炼API Key配置在环境变量中
$env:DASHSCOPE_API_KEY = "sk-xxx"
.\openai-proxy.exe --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --listen :8080
```

2.  在新的终端中使用 OpenAI Python SDK 发送 OpenAI 兼容请求

<a id="sec-tabs-4"></a>

<a id="chat-请求"></a>

<a id="chat-请求-h4"></a>

#### Chat 请求

文本输入示例：

<a id="code-block-5"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="http://localhost:8080",
)

completion = client.chat.completions.create(
    model="xxx",  # 请替换为实际模型code
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    extra_body={"enable_thinking": False},
)

print(completion.choices[0].message.content)
```

图片输入示例（Base64 编码）：

<a id="code-block-6"></a>

```python
import os
import base64
from openai import OpenAI

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="http://localhost:8080",
)

completion = client.chat.completions.create(
    model="xxx",  # 请替换为实际模型code
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 传入 Base64 时，图像格式（即 image/{format}）需与实际图片一致
                    # PNG图像：  f"data:image/png;base64,{base64_image}"
                    # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                    # WEBP图像： f"data:image/webp;base64,{base64_image}"
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

<a id="responses-api-请求"></a>

<a id="responses-api-请求-h4"></a>

#### Responses API 请求

文本输入示例：

<a id="code-block-7"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="http://localhost:8080",
)

response = client.responses.create(
    model="xxx",  # 请替换为实际模型code
    input="你是谁？"
)

print(response.output_text)
```

图片输入示例（Base64 编码）：

<a id="code-block-8"></a>

```python
import os
import base64
from openai import OpenAI

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="http://localhost:8080",
)

response = client.responses.create(
    model="xxx",  # 请替换为实际模型code
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    # 传入 Base64 时，图像格式（即 image/{format}）需与实际图片一致
                    # PNG图像：  f"data:image/png;base64,{base64_image}"
                    # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                    # WEBP图像： f"data:image/webp;base64,{base64_image}"
                    "image_url": f"data:image/png;base64,{base64_image}",
                },
                {"type": "input_text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)

print(response.output_text)
```

接口功能限制：

-   不支持显式缓存及相关参数功能。
-   多模态视觉理解仅支持以 [Base64 编码](../model-experience/text-generation-model/vision.md#d987f8de5395x) 形式的图片输入，不支持公网 URL 输入，且单次请求的原始图片大小总和不超过 8 MB；不支持 max\_pixels、min\_pixels、vl\_high\_resolution\_images 参数与 HEIC 图片格式，其他图片输入限制可参考[输入文件限制](../model-experience/text-generation-model/vision.md#8211ccbe85avh)。
-   出于数据安全隐私考虑，不支持联网搜索，代码解释器等内置工具。
-   Responses API 仅支持无状态调用（创建响应），不支持已存储会话等相关参数功能（previous\_response\_id、conversation、store）。

<a id="anthropic-proxy-anthropic-兼容-messages-接口"></a>

<a id="anthropic-proxy-anthropic-兼容-messages-接口-h4"></a>

#### anthropic-proxy（Anthropic 兼容 Messages 接口）

我们提供了基于 SDK 构建的 Anthropic 兼容 Messages 接口的 HTTP 本地代理工具，便于集成现有 Anthropic 客户端。

1.  本地启动 `anthropic-proxy` 代理工具

<a id="code-block-9"></a>

```bash
# MacOS/Linux
# 请将您的百炼API Key配置在环境变量中
export DASHSCOPE_API_KEY="sk-xxx"
./anthropic-proxy --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --listen :8080

# Windows Powershell
# 请将您的百炼API Key配置在环境变量中
$env:DASHSCOPE_API_KEY = "sk-xxx"
.\anthropic-proxy.exe --endpoint https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services --listen :8080
```

2.  在新的终端中使用 Anthropic Python SDK 发送 Anthropic 兼容 Messages 请求

文本输入示例：

<a id="code-block-10"></a>

```python
import os
import anthropic

client = anthropic.Anthropic(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="http://localhost:8080",
)

message = client.messages.create(
    model="xxx",  # 请替换为模型部署成功后的code
    max_tokens=1024,
    system="You are a helpful assistant",
    messages=[
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    thinking={"type": "disabled"},
)

print(message.content[0].text)
```

图片输入示例（Base64 编码）：

<a id="code-block-11"></a>

```python
import os
import base64
import anthropic

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = anthropic.Anthropic(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="http://localhost:8080",
)

message = client.messages.create(
    model="xxx",  # 请替换为模型部署成功后的code
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        # 传入 Base64 时，media_type 需与实际图片格式一致（如 image/png）
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image,
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)

print(message.content[0].text)
```

接口功能限制：

-   不支持显式缓存及相关参数功能。
-   多模态视觉理解仅支持以 [Base64 编码](../model-experience/text-generation-model/vision.md#d987f8de5395x) 形式的图片输入，不支持公网 URL 输入，且单次请求的原始图片大小总和不超过 8 MB；不支持 max\_pixels、min\_pixels、vl\_high\_resolution\_images 参数与 HEIC 图片格式，其他图片输入限制可参考[输入文件限制](../model-experience/text-generation-model/vision.md#8211ccbe85avh)。

<a id="查看本地透明度报告"></a>

<a id="call-h3-transparency"></a>

### 查看本地透明度报告

您可在本地以下目录查看机密推理请求的透明度报告：

<a id="sec-tabs-5"></a>

<a id="macos"></a>

<a id="macos-h4"></a>

#### macOS

`~/Library/Application\ Support/dashscope-confidential-maas/transparency-reports`

<a id="linux"></a>

<a id="linux-h4"></a>

#### Linux

`$XDG_DATA_HOME/dashscope-confidential-maas/transparency-reports/`

若未设置 `$XDG_DATA_HOME`，则默认为：`~/.local/share/dashscope-confidential-maas/transparency-reports/`

<a id="windows"></a>

<a id="windows-h4"></a>

#### Windows

`%APPDATA%\dashscope-confidential-maas\transparency-reports\`

通常对应 `C:\Users\<用户名>\AppData\Roaming\dashscope-confidential-maas\transparency-reports\`

SDK 中还额外提供了 cmaas-audit 命令行工具，用于对本地透明度报告进行离线安全审计，相关详情可参考 SDK 中的对应文档。

默认情况下，本地透明度报告会记录请求提示词用于审计。如需关闭提示词记录功能，可在启动 `openai-proxy` 或 `anthropic-proxy` 时添加 `--no-prompt-in-transparency-report` 参数。关闭后，远程证明等其他审计材料仍会保留。

认证方式与错误码详见 SDK 调用响应。

<a id="6-应用场景"></a>

<a id="h2sec7scenario"></a>

## 6 应用场景

机密推理面向这样的场景：业务需调用云端大模型，但客户数据、业务数据或模型权重至少有一方存在"明文不能让对方看到"的硬约束。

**金融风控与反欺诈推理**

-   适用：信贷审核、反欺诈识别、风控辅助决策
-   优势：数据/模型双盲；对齐 JR/T 0197 C3/C4 级金融数据加密与访问控制要求

**政务与央国企大模型应用**

-   适用：内部知识检索、决策辅助、智能问答
-   优势：敏感文档密文上送、硬件保护区推理、加密回传

**其他典型场景：**

-   医疗影像/病历 AI 诊断（受《个人信息保护法》与 HIPAA 约束）
-   法律/合同智能审阅（安全环境中处理合同明文）
-   智能座舱与车端助手（符合《汽车数据安全管理若干规定》）
-   智能客服与售后工单（含身份证号、银行卡片段等敏感信息）

**两类共性：**

-   数据出域受限（金融、医疗、政企、车载典型）
-   数据/模型双盲（金融、法律典型）

机密推理部署基于独立资源池与 Token 目录价计费，面向高安全机密推理场景。概念详见[机密推理简介](confidential-inference.md#h2sec1overview)与[计费说明](confidential-inference.md#h2sec5billing)。

保险（核保/理赔反欺诈）、HR（简历筛选/面试纪要）、跨境业务（需符合 GDPR 的多语言客服）等同样具备上述特征。选型时按数据受保护场景与独占容量需求，评估是否适用机密推理。
