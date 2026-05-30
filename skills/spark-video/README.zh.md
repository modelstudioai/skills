# spark-video

> [English version →](README.md)

AI 视频制作 skill — premise → 剧本 → 分镜 → 渲染 → 审片 → 成片 mp4,
角色/布景/道具一致。跨 agent 平台(Claude Code / Cursor / Qwen Code /
Codex / …)。

## 示例

> **提示：** GitHub README 不支持内嵌 `<video>` 播放，**点击右侧封面图**可在新标签页观看完整成片。

<table>
<tr>
<th width="44%">📝 Prompt</th>
<th width="56%">🎬 成片</th>
</tr>

<tr>
<td valign="top">

**① 日剧风 · 青涩初恋**（≈2 分钟，16:9）

> 日剧风格，高中女生的青涩初恋故事，剧情高甜，让人看了想谈恋爱，2 分钟左右。16:9

</td>
<td>

<a href="https://cloud.video.taobao.com/vod/ToFBk3q6IrT1L6k9TAW3Qu0GdJAWN80uyb75zNelvE8.mp4" target="_blank">
<img src="https://img.alicdn.com/imgextra/i4/6000000000158/O1CN01Nko87m1D2Pip5isBr_!!6000000000158-0-tbvideo.jpg" alt="日剧风 · 青涩初恋 — 点击播放" width="100%">
</a>

</td>
</tr>

<tr>
<td valign="top">

**② 悬疑短剧 · 末班车** — 纯旁白、无 BGM、指定 TTS 音色

<details>
<summary>完整 prompt</summary>

使用 spark-video 生成一段帮我生成一个悬疑短剧。

故事梗概如下：我搭上了一列特快车，大概在还差 10 分就午夜 12 点的时候，在中途站有一名男子也上了列车，他在车门关闭后，像是突然回复意识一般，开始左右环视着周遭乘客的脸。"恕我愚昧，请问您今年 28 岁吗？"他如此的向我问道，"是的，不过您怎么知道呢？"我如此反问他，但被他无视，只是自顾自的和别人说话。"您今年 45 岁吧？""是没错。""您是 62 岁吗？""你怎么知道的？"一直和看似不相识的乘客群重复着诸如此类的对话，看来这名男子，似乎有着只要看着别人的脸就能知道其年龄的特殊能力。此时到下个停车站还有 15 分钟左右的时间，全车箱包括我在内的乘客都对这名男子投以好奇的注目眼光，一直到他问到最后一名女士。"您是 50 岁吗？""是的，不过还有五分钟就 51 岁了！"那名女士如此微笑的回答道。霎时，那名男子的脸色铁青，仿佛震撼到无以复加。

采用旁白模式，将故事改成第三人称叙事。故事的最后，旁白加一句：原来，这个男子看到的数字，是寿命而不是年龄，他察觉到大家头上的数字和实际年龄非常吻合，猜测到这趟火车即将发生事故，因此疯狂地和大家确认年龄，就是希望在火车到站时马上逃离这趟火车，可现在，似乎来不及了。旁白音色用 qwen3-tts 的 Ebona。注意不要让模型生成背景音乐。

</details>

</td>
<td>

<a href="https://cloud.video.taobao.com/vod/MZx8KDUpGBygpU3SuTShGzyVxh0CbeJjpzhfNqSWz1Y.mp4" target="_blank">
<img src="https://img.alicdn.com/imgextra/i4/O1CN01UrL0Si1tTAiwIC1f3_!!6000000005902-2-tps-5032-2830.png_640x360q90.jpg" alt="悬疑短剧 · 末班车 — 点击播放" width="100%">
</a>

</td>
</tr>

<tr>
<td valign="top">

**③ 趣味科普 · 人类肌肉之谜** — 指定本地 BGM 文件

> 使用 spark-video，帮我生成一段 3 分钟以内的趣味科普视频，从科学的角度介绍为什么人类相比其他哺乳动物，不容易保持强大的肌肉。背景音乐采用 `~/Documents/darktown-strutters-ball.mp3`。

</td>
<td>

<a href="https://cloud.video.taobao.com/vod/s589nKcgwi15bqIZyn8923w-F53_ZIDprlsmbaaodzo.mp4" target="_blank">
<img src="https://img.alicdn.com/imgextra/i3/O1CN01sStqZg20wfXgzHgEI_!!6000000006914-2-tps-5032-2830.png_640x360q90.jpg" alt="趣味科普 · 人类肌肉之谜 — 点击播放" width="100%">
</a>

</td>
</tr>

<tr>
<td valign="top">

**④ 产品广告 · iPhone Pro** — 参考图 + 5 段文案 + 循环 BGM

<details>
<summary>完整 prompt</summary>

使用 spark-video，帮我创作一款高端手机的广告，名字叫 iPhone Pro。

广告文案如下：

1、你，与众不同，你喜欢超越。你有梦想，你有力量，你从不把成就作为终点，记住，你的名字叫做：成功！ iPhone Pro，钛合金 24°黄金角立体切割，荷兰进口小牛皮，视网膜高清屏幕，128G 顶配内存，1300 万高清摄像，向成功的人生致敬。

2、 iPhone Pro，专属一对一保密钥匙。人机分离 10 米，自动报警。很好与优秀只差一点点距离，这段距离叫安全。忘带会提醒，丢失就报警，手机不忘带，机密不泄露。

3、 iPhone Pro，隐形拨号，加密通话，无痕迹沟通。幸福往往是分享，而苦痛却常常隐藏。这就是男人，你的世界，别人不懂。隐形拨号，加密通话，无痕迹沟通，能谈吐有方，会进退自如。

4、懂生活才能会工作， iPhone Pro，双密码，双空间，工作生活分别存储，互不干扰。记住：跑得快不一定赢，不跌跟头才是成功。一部手机，两个密码，两个空间，分别存储，互不干扰。

5、成功并不是高瞻远瞩，而是你本来就站在高处，运筹帷幄，掌控未来，这才是 iPhone Pro，这才是胸怀天下。顶峰的目标，钛金的气概，真皮的情怀，让我们向成功的人生致敬。

产品图片在 `~/Documents/product-item.webp`，广告代言人物形象参考 `~/Documents/jason1.jpg` 和 `~/Documents/jason2.jpg`。采用全旁白，代言人不需要说话。背景音乐用 `~/Documents/励志奋斗.mp3`，如果音乐时长不够可以循环播放。

</details>

</td>
<td>

<a href="https://cloud.video.taobao.com/vod/x_UZpW3zyL0JC1x6uhATnVRwwrkq9PIEjIsaNuzUPZA.mp4" target="_blank">
<img src="https://img.alicdn.com/imgextra/i3/O1CN01nN98IX1P7FI0i1bs7_!!6000000001793-2-tps-5032-2830.png_640x360q90.jpg" alt="产品广告 · iPhone Pro — 点击播放" width="100%">
</a>

</td>
</tr>
</table>

## 安装 — 一句话交给 agent

整个安装就是**一段 prompt**。打开任意支持 skills 的 agent
(Claude Code / Cursor / Qwen Code / Gemini CLI / …),把下面这段粘进去:

> 帮我装 spark-video skill:
> 1. 识别我当前所在 agent 在这个操作系统下的 skills 目录
>    (比如 `~/.claude/skills/`、`~/.qwen/skills/`、
>    `~/.cursor/skills/` …),把
>    `https://github.com/JohnKeating1997/spark-video.git` clone 到那里,
>    目录名叫 `spark-video`。
> 2. 提醒我新开一个会话,让 skill 被加载。
> 3. 新会话里读 `spark-video/SKILL.md`,跑 `./scripts/doctor.sh`,
>    用我系统的包管理器装上缺的依赖(`bl` / `ffmpeg` / `uv`),
>    每条命令都先问我确认。
> 4. 问我要不要顺手 `./scripts/install-deps.sh` 拉 山音 craft 引用
>    (失败不影响主流程)。
> 5. 再跑一次 doctor,全绿后告诉我可以开工了。

完事。不需要记路径,也不需要复制 platform-specific 的命令 —— agent 读
`SKILL.md`(里面有完整的安装 runbook)自己驱动后面的步骤。

<details>
<summary>手动 fallback(如果你的 agent 不识别 skills)</summary>

```bash
# 挑你所在平台对应的目录:
git clone https://github.com/JohnKeating1997/spark-video.git \
  ~/.claude/skills/spark-video
# 或  ~/.qwen/skills/spark-video
# 或  ~/.cursor/skills/spark-video
# …
```

然后新开 agent 会话发一句:
**"帮我把 spark-video 装好"**
agent 会按 `SKILL.md` 里的安装 runbook 继续。

</details>

## 用起来

新会话发一句任意一种:

**一键模式(推荐)**
> 用 spark-video 帮我做一集 3 分钟短剧,项目叫 demo,第一集,
> premise:[你的故事点子]

**分步模式**
> 用 spark-video 的 screenwriter 帮我写剧本,项目 demo episode 001,
> premise:…

agent 读 `SKILL.md` 自动路由到对应 sub-skill,按 4+2 gate 流程跑。

## 产物

```
projects/<project>/<episode>/
├── final/<project>-<episode>.mp4     ← 成片
├── clips/*.mp4                       ← 所有 shot
├── reviews/*.json                    ← 逐 clip 评分
└── logs/model_calls.jsonl            ← 每一次模型调用的 prompt(PE 友好)
```

## 排障

大多数情况直接交给 agent 处理 —— 说"帮我修 XX"就行。

- 安装后 agent 不认识 `spark-video` → 重启 agent / 新开会话
- `bl: command not found` → `npm install -g bailian-cli && npx skills add modelstudioai/skills --all -g && bl auth login`
  (完整安装说明：<https://bailian.aliyun.com/cli/install.md>)
- `Permission denied: scripts/bl` → `chmod +x scripts/*.sh scripts/bl`
- 渲染卡住 → `tail -f projects/<p>/<e>/logs/model_calls.jsonl | jq .`

## 更新 / 卸载

直接交给 agent:

> 帮我更新一下 spark-video。
> 帮我卸载 spark-video。

或者手动:

```bash
# 更新
cd ~/.claude/skills/spark-video && git pull

# 卸载
rm -rf ~/.claude/skills/spark-video
```

## 想看细节?

- 架构 + agent 调度规则: [`SKILL.md`](SKILL.md)
- 6 个子技能的详细文档: [`references/spark-video-*/SKILL.md`](references/)
- 每个脚本的 `--help`: 用 `uv run scripts/<name>.py --help`
