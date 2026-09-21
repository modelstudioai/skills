# 实例管理与使用

通过 E2B SDK 管理沙箱实例的生命周期并执行数据面操作。使用阿里云百炼沙箱接入地址与 API Key，即可创建实例、执行命令、运行代码与读写文件。

Sandbox 兼容 [E2B](https://e2b.dev/docs) SDK。安装 E2B 官方 SDK 后，将接入地址指向阿里云百炼沙箱、用阿里云百炼 API Key 鉴权，即可创建实例、执行命令、运行代码与读写文件。

## 推荐版本

本文示例基于以下版本验证：

```
pip install "e2b==2.31.0"
# 如需 run_code 等 Code Interpreter 能力
pip install "e2b-code-interpreter==2.8.1"
```

更高版本的 SDK（Python 与 Node.js 均含）创建实例时返回 405，安装时固定上述版本。

## 鉴权与接入

**参数**

**说明**

`api_url`

阿里云百炼沙箱接入地址，形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`

`Authorization`

`Bearer <阿里云百炼 API Key>`，用于真实鉴权

`api_key`

E2B SDK 必填参数，仅用于满足 SDK 格式，推荐填写 `e2b_${ALIYUN_UID}`

`template`

模版 code，即控制台创建的 `templateCode`

**说明**`api_key` 只需满足 `e2b_` 后跟十六进制字符的格式。阿里云 UID 为纯数字，天然满足校验（如 `e2b_your aliyunUid`）。阿里云百炼侧不使用 `api_key` 做业务鉴权。

## 步骤 1：创建实例

使用阿里云百炼 API Key 根据模版 code 创建一个云端沙箱，成功后得到 `sandbox_id`，后续访问与管理均使用它。

```
from e2b import Sandbox

ALIYUN_UID = "your aliyunUid"
BAILIAN_API_KEY = "sk-..."
BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox"

sbx = Sandbox.create(
    api_url=BASE_URL,
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
    template="你的模版 code",
)

print(sbx.sandbox_id)
```

## 步骤 2：访问实例

连接到沙箱后，可执行命令、运行代码，也可像操作本地文件一样读写文件。

```
# 执行命令
result = sbx.commands.run("python --version")
print(result.stdout)

# 创建目录
sbx.files.make_dir("/home/user/workspace/e2b")

# 写入文件
sbx.files.write(
    "/home/user/workspace/hello_bailian_sandbox.md",
    "hello bailian",
)

# 读取文件
content = sbx.files.read(
    "/home/user/workspace/hello_bailian_sandbox.md"
)
print(content)

# 运行代码（需 e2b-code-interpreter）
execution = sbx.run_code("print(1 + 1)")
print(execution.text)
```

## 步骤 3：管理实例生命周期

空闲时暂停沙箱，需要时重新连接会从暂停点恢复；不再使用时释放资源。

```
sandbox_id = sbx.sandbox_id

# 暂停沙箱，保留文件系统与内存状态
sbx.pause()

# 重新连接沙箱，连接后可继续使用
sbx = Sandbox.connect(
    sandbox_id=sandbox_id,
    api_url=BASE_URL,
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
)

# 不再使用时释放沙箱
sbx.kill()
```

## 支持的能力

### 实例生命周期

**能力**

**SDK 方法**

创建实例

`Sandbox.create(template=...)`

获取实例信息

`sbx.get_info()`

连接实例

`Sandbox.connect(sandbox_id=...)`

暂停实例

`sbx.pause()`

释放实例

`sbx.kill()`

### 数据面操作

数据面操作推荐通过 SDK 完成，SDK 会使用连接实例返回的 domain 与 token 直接访问沙箱运行时。

**能力**

**SDK 方法**

**底层数据面请求**

执行命令

`sbx.commands.run(...)`

`POST /process.Process/Start`

创建目录

`sbx.files.make_dir(path)`

SDK 文件系统 RPC

写文件

`sbx.files.write(path, content)`

`POST /files?path=...`

读文件

`sbx.files.read(path)`

`GET /files?path=...`

运行代码

`sbx.run_code(...)`

`POST :49999/execute`

**说明**模版管理没有稳定的 SDK 对象方法，需通过 raw HTTP 调用管控面接口，详见 [Sandbox API - 模版管理](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。实例生命周期与数据面操作使用上述 SDK 方法即可。

## 下一步

-   [Sandbox API](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)：兼容 E2B 协议的 REST API 与模版管理
-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：配置镜像、资源规格与生命周期
