# 支持的文件与限制

查看 Parse 和 Extract 支持的输入类型、体验页上传限制及可复用结果边界。

Parse 支持图文、音频和视频；Extract 仅支持图文输入。提交前请先确认能力与文件类型匹配。

## 能力范围

输入类型

Parse

Extract

文档、图片、扫描件、表格与文本

支持

支持

音频

支持

不支持

视频

支持

不支持

有效的图文 ParseResult

—

支持复用

## Parse 支持的格式

### 图文文件

类别

格式

文档

`.pdf`、 `.doc`、`.docx`、`.rtf`、`.pages` 、`.ppt`、`.pptx`、`.key` 、`.xls`、`.xlsx`、`.xlsm`、`.csv`、`.numbers`

图片

`.png`、`.jpg`、`.jpeg`、`.bmp`、`.gif`

文本

`.md`、`.markdown`、`.txt`

网页

`.html`、`.htm`

电子书

`.epub`、`.mobi`

### 音频和视频

类别

格式

音频

`.mp3`、`.wav`、`.aac`、`.amr`、`.flac`、`.ogg`、`.opus`、`.wma`

视频

`.mp4`、`.mkv`、`.avi`、`.mov`、`.wmv`、`.flv`、`.mpeg`、`.webm`

## Extract 支持的格式

Extract 支持上方列出的**图文文件**，不支持音频和视频。输入可以是：

类别

格式

文档

`.pdf`、`.doc`、`.docx`、`.rtf`、`.ppt`、`.pptx`、`.xls`、`.xlsx`、`.xlsm`、iWork（Keynote、Numbers、Pages）

图片

`.png`、`.jpg`、`.jpeg`、`.bmp`、`.gif`

文本

`.md`、`.markdown`、`.txt`

网页

`.html`、`.htm`

电子书

`.epub`、`.mobi`

复用 ParseResult 可以避免再次解析同一文件。音频或视频 ParseResult 不能用于 Extract。

## 单个文件大小上限

**输入类型**

**API**

**控制台上传**

文档、文本、网页、电子书

1 GB

200 MB

图片

20 MB

20 MB

音频

2 GB

200 MB

视频

10 GB

200 MB
