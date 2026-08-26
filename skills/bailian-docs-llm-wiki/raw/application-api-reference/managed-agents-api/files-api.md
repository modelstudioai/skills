# File

文件是独立资源：上传一次后可被多个会话挂载至沙箱供工具读写，也可作为消息内容（图像、音频、附件）传给智能体。

## 配额与状态

-   单文件直传上限 **20 MB**；单个工作空间总容量上限 **100 GB**；保留期 **30 天**，超期可能被自动清理。
-   上传后进入安全审核，`status` 取值：`checking` / `available` / `rejected` / `type_rejected`。仅 `available` 可挂载到会话或作为消息内容引用。
-   挂载到会话沙箱时服务端会做内部拷贝并生成新的 `file_id`，副本元数据带 `scope: {"type": "session", "id": "sesn_..."}`，仅对应会话可见。

## 文件操作

**操作**

**端点**

**说明**

[上传 File](https://help.aliyun.com/zh/model-studio/file-upload)

`POST /files`

`multipart/form-data` 直传，初始状态 `checking`

[查询 File](https://help.aliyun.com/zh/model-studio/file-get)

`GET /files/{file_id}`

查询文件元数据与审核状态（不含内容）

[列出 File](https://help.aliyun.com/zh/model-studio/file-list)

`GET /files`

分页列出工作空间下的文件，支持按会话 ID 过滤

[删除 File](https://help.aliyun.com/zh/model-studio/file-delete)

`DELETE /files/{file_id}`

硬删除；已挂载到会话的内部拷贝不受影响
