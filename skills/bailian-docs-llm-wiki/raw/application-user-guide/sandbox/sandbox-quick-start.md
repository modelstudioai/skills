# 快速开始

通过控制台完成服务授权、创建模版、生成 API Key 并发起首次调用，几分钟内启动第一个沙箱。

## 前置准备

-   已开通[阿里云百炼](https://bailian.console.aliyun.com/)。
-   当前账号具备 Sandbox 操作权限。

## 步骤 1：完成服务授权

首次使用 Sandbox 时，需完成服务关联角色（SLR）授权，以便阿里云百炼创建与管理沙箱运行环境。

进入[阿里云百炼控制台 > Sandbox](https://bailian.console.aliyun.com/cn-beijing/sandbox/quick-start)，首次创建模版时弹出「阿里云服务授权」对话框：

**字段**

**值**

角色名称

`AliyunServiceRoleForSFMSandbox`

角色权限策略

`AliyunServiceRolePolicyForSFMSandbox`

权限说明

允许阿里云百炼服务访问沙箱计算与网络资源，完成沙箱实例的创建、运行与释放

勾选《数据访问授权协议》后点击**确认授权**，即完成一次性授权。

## 步骤 2：创建模版

模版定义沙箱的运行环境。进入 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template)，点击**创建模版**，配置以下字段：

**字段**

**说明**

选择镜像

三选一：`code-interpreter-v1`（代码执行）、`browser`（浏览器操作）、`all-in-one`（综合能力）

模版名称

必填，自定义

资源配置

必选。配置 1（1 Core｜2 GB，推荐）或配置 2（4 Core｜8 GB）

如需文件挂载、网络白/黑名单、环境变量或生命周期控制，展开**高级配置**按需设置。填写完成后点击**创建**。创建成功后模版出现在列表中，记录其 `templateCode` 用于后续调用。

**说明**生命周期控制中，空闲超时与最大存活时间二选一，最长保持 7 天。

## 步骤 3：获取 API Key

调用沙箱需使用阿里云百炼 API Key 进行鉴权。在 [Sandbox 页左下角点击 API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key)，创建或复制一个 API Key（格式 `sk-...`）。

## 步骤 4：发起首次调用

Sandbox 兼容 E2B SDK。安装 SDK 后，使用阿里云百炼沙箱接入地址与 API Key 创建实例并执行代码。

安装 SDK：

```
pip install "e2b==2.31.0"
# 如需 run_code 等 Code Interpreter 能力
pip install "e2b-code-interpreter==2.8.1"
```

创建实例并执行：

```
from e2b import Sandbox

ALIYUN_UID = "your aliyunUid"       # 阿里云 UID
BAILIAN_API_KEY = "sk-..."            # 阿里云百炼 API Key

sbx = Sandbox.create(
    api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
    api_key=f"e2b_{ALIYUN_UID}",      # 占位参数，满足 E2B SDK 格式即可
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},  # 阿里云百炼 API Key，用于鉴权
    template="你的模版 code",
)

# 执行命令
result = sbx.commands.run("python --version")
print(result.stdout)

# 写入并读取文件
sbx.files.write("/home/user/workspace/hello.md", "hello bailian")
print(sbx.files.read("/home/user/workspace/hello.md"))
```

**说明**`api_key` 是 E2B SDK 的必填参数，只需满足 `e2b_` 后跟十六进制字符的格式即可，推荐填写 `e2b_${ALIYUN_UID}`。阿里云百炼侧的真实鉴权使用 `Authorization: Bearer <阿里云百炼 API Key>`，不使用 `api_key`。

## 下一步

-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：配置镜像、资源规格与生命周期
-   [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)：实例生命周期与数据面操作
-   [Sandbox API](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)：兼容 E2B 协议的 REST API
