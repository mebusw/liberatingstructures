## 任务概述

将 `structures.entries.json` 中的 34 条目转换为博客 Markdown 文件

## 输出要求

### 文件命名

- 文件名 = 中文标题 (`content[0].title`)
- 路径：`_posts/<filename>.md`

### Frontmatter



```yaml
---
title: <中文标题>
tags:
    - liberating-structures
    - <第一个标签>
---
```

### 内容格式（金标准：`structures-1-2-4-all.sample.md`）

- H1：中文标题 + `（英文: <英文标题>）`
- 图片：`![](<iconURL>)`
- 摘要引用：`> <summary>`
- 编号：`**编号**：第 <sequence> 号微结构`
- 时长：`**时长**：<minDuration>-<maxDuration> 分钟`
- 三个章节：`## What` / `## How` / `## Why`

### HTML 转 Markdown 规则

| 来源                                              | 转换结果         |
| ------------------------------------------------- | ---------------- |
| 内部 LS 链接 `<a href="http://结构名">结构名</a>` | `[[结构名]]`     |
| 外部 URL `<a href="http://xxx.com">xxx.com</a>`   | `<xxx.com>`      |
| `<h3>标题</h3>`                                   | `### 标题`       |
| `<li>内容</li>`                                   | `- 内容`         |
| 嵌套 HTML 标签                                    | 剥离标签保留文本 |

### 模板路径

- 模板文件：`ai-template.md`
- JSON 数据：`structures.entries.json`
- 金标准：`structures-1-2-4-all.sample.md`