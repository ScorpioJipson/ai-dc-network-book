#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《万卡时代》Markdown -> 在线阅读 HTML 站点构建脚本

用法:
    python build_site.py

输入:
    book/chapters/*.md   前言 + 章节正文 + 附录
输出:
    book/build/*.html    每篇一个页面 + index.html 入口

读者可见内容 = 前言 + 18 章正文 + 附录 A–F。
内部工作文件（写作规范 / 贯穿案例参数卡 / 数据锚点索引 / 目录定稿）刻意不进入读者导航——
它们是写作期的「准绳」，不是成书内容；源文件仍在 book/*.md，只是不随书发布。
对外版的主线案例参数见附录 F。
"""

import os
import re
import html
import shutil

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")

# ---------------------------------------------------------------- 目录结构定义
# (模块名, [(章号, 文件名 slug, 中文标题)])
MODULES = [
    ("序", [
        (None, "00-前言", "前言"),
    ]),
    ("模块一　智算中心网络基石与顶层设计", [
        (1, "m1-ch01-训练通信挑战", "第 1 章　大模型训练对网络的极致挑战"),
        (2, "m1-ch02-五平面架构", "第 2 章　智算中心「五平面」网络架构设计哲学"),
        (3, "m1-ch03-拓扑与端口配比", "第 3 章　算力网络拓扑设计实战"),
    ]),
    ("模块二　物理层与硬件选型防坑指南", [
        (4, "m2-ch04-光模块与光纤", "第 4 章　光模块与光纤物理层深度剖析"),
        (5, "m2-ch05-服务器网卡与互联", "第 5 章　服务器、网卡与芯片级互联"),
    ]),
    ("模块三　两大算力网络阵营", [
        (6, "m3-ch06-InfiniBand", "第 6 章　InfiniBand（IB）无损网络全景"),
        (7, "m3-ch07-RoCEv2", "第 7 章　超大规模无损以太网（RoCEv2）组网实战"),
        (8, "m3-ch08-选型决策", "第 8 章　IB vs. RoCEv2 多维对比与选型决策"),
        (9, "m3-ch09-国产化生态", "第 9 章　国产算力网络与信创生态"),
    ]),
    ("模块四　存储网络与辅助平面构建", [
        (10, "m4-ch10-存储网络", "第 10 章　高性能智算存储网络"),
        (11, "m4-ch11-辅助平面", "第 11 章　带外管理、带内调度与高精度时间同步"),
    ]),
    ("模块五　工程实施、验收测试与性能调优", [
        (12, "m5-ch12-施工打缆", "第 12 章　千卡／万卡集群工程打缆与物理施工"),
        (13, "m5-ch13-压测与排障", "第 13 章　网络性能压测与故障排查"),
        (14, "m5-ch14-可观测性", "第 14 章　网络可观测性与运维体系"),
        (15, "m5-ch15-通信库调优", "第 15 章　通信库与集合通信调优"),
    ]),
    ("模块六　商业预算评估与项目交付管理", [
        (16, "m6-ch16-预算与招投标", "第 16 章　预算评估、BOM 编制与招投标"),
        (17, "m6-ch17-交付管理", "第 17 章　项目全周期交付管理"),
        (18, "m6-ch18-技术趋势", "第 18 章　技术趋势与架构演进"),
    ]),
    ("附录", [
        (None, "appendix-a", "附录 A　光模块端面与混插速查表"),
        (None, "appendix-b", "附录 B　端口配比计算表（可填参数）"),
        (None, "appendix-c", "附录 C　压测基线数据模板"),
        (None, "appendix-d", "附录 D　术语中英对照表"),
        (None, "appendix-e", "附录 E　现场检查清单汇总（第 1–18 章）"),
        (None, "appendix-f", "附录 F　主线案例参数速查"),
    ]),
]

SITE_TITLE = "万卡时代"
SITE_SUB = "智算中心全栈网络架构与工程落地实战"

CSS = """
:root{
  --bg:#ffffff; --bg-soft:#f7f7f5; --fg:#1a1a1a; --fg-soft:#5c5c58;
  --line:#dcdcd6; --line-soft:#ececE7; --accent:#1f4e79;
  --code-bg:#f5f5f2; --warn:#8a4b00;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--fg);
  font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.85;
}
.wrap{display:flex; max-width:1400px; margin:0 auto; align-items:flex-start}
nav{
  width:290px; flex:0 0 290px; padding:28px 20px 60px 28px;
  border-right:1px solid var(--line-soft); position:sticky; top:0;
  max-height:100vh; overflow-y:auto;
}
nav .brand{font-size:17px; font-weight:600; letter-spacing:.5px; margin-bottom:2px}
nav .brand-sub{font-size:12px; color:var(--fg-soft); margin-bottom:20px; line-height:1.5}
nav .grp{margin-bottom:16px}
nav .grp-t{font-size:12px; font-weight:600; color:var(--fg-soft); margin-bottom:6px; letter-spacing:.3px}
nav a{
  display:block; padding:5px 9px; margin:1px 0; font-size:13px; line-height:1.5;
  color:var(--fg); text-decoration:none; border-radius:5px; border-left:2px solid transparent;
}
nav a:hover{background:var(--bg-soft)}
nav a.on{background:var(--bg-soft); border-left-color:var(--accent); font-weight:600}
nav span.todo{display:block; padding:5px 9px; font-size:13px; color:#a8a8a2; line-height:1.5}
nav .legend{margin-top:24px; padding-top:14px; border-top:1px solid var(--line-soft); font-size:11.5px; color:var(--fg-soft); line-height:1.7}

main{flex:1 1 auto; min-width:0; padding:44px 56px 120px 56px; max-width:1000px}
main h1{font-size:26px; font-weight:600; margin:0 0 6px; line-height:1.4; letter-spacing:.2px}
main h2{
  font-size:19px; font-weight:600; margin:44px 0 14px; padding-bottom:8px;
  border-bottom:1px solid var(--line); line-height:1.5;
}
main h3{font-size:16px; font-weight:600; margin:30px 0 10px; line-height:1.5}
main h4{font-size:14.5px; font-weight:600; margin:22px 0 8px; color:#333}
main p{margin:11px 0}
main ul,main ol{margin:11px 0; padding-left:24px}
main li{margin:5px 0}
main li input[type=checkbox]{margin-right:7px; vertical-align:-1px}
main a{color:var(--accent)}
blockquote{
  margin:16px 0; padding:10px 16px; border-left:3px solid var(--line);
  background:var(--bg-soft); color:#41413d; font-size:14px;
}
blockquote p{margin:6px 0}
code{
  font-family:Consolas,"NSimSun","Courier New",monospace; font-size:13px;
  background:var(--code-bg); padding:1px 5px; border-radius:3px;
  border:1px solid var(--line-soft);
}
pre{
  background:var(--code-bg); border:1px solid var(--line); border-radius:6px;
  padding:14px 16px; overflow-x:auto; margin:16px 0; line-height:1.6;
}
pre code{background:none; border:none; padding:0; font-size:12.5px}
table{border-collapse:collapse; width:100%; margin:18px 0; font-size:13.5px}
th,td{border:1px solid var(--line); padding:8px 11px; text-align:left; vertical-align:top; line-height:1.6}
th{background:var(--bg-soft); font-weight:600; white-space:nowrap}
tr:nth-child(even) td{background:#fbfbf9}
hr{border:none; border-top:1px solid var(--line-soft); margin:34px 0}
figure.fig{margin:22px 0; text-align:center}
figure.fig svg{max-width:100%; height:auto; border:1px solid var(--line-soft); border-radius:6px}
main p code{white-space:normal}
.meta{font-size:12.5px; color:var(--fg-soft); margin-bottom:26px; padding-bottom:14px; border-bottom:1px solid var(--line-soft)}
.tag{display:inline-block; font-size:11px; padding:1px 7px; border:1px solid var(--line); border-radius:10px; margin-right:6px; color:var(--fg-soft)}
.todo-note{margin:14px 0; padding:14px 16px; border:1px dashed var(--line); border-radius:6px; color:var(--fg-soft); font-size:13.5px; background:#fbfbf9}
.toc-grp{margin:26px 0 0}
.toc-grp h2{margin-top:0}
.toc-grp p{margin:3px 0}
@media (max-width:900px){
  .wrap{display:block}
  nav{width:auto; flex:none; position:static; max-height:none; border-right:none; border-bottom:1px solid var(--line-soft); padding:20px}
  main{padding:24px 20px 80px; max-width:none}
}
@media print{
  nav{display:none}
  main{padding:0; max-width:none}
  body{font-size:11pt}
  a{color:inherit; text-decoration:none}
  main h2{page-break-after:avoid}
  table,pre,blockquote{page-break-inside:avoid}
}
"""

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def parse_front_matter(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    meta = {}
    for line in raw.splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[m.end():]


def gfm_checkboxes(body):
    """把 - [ ] / - [x] 列表项转成真实 checkbox（紧凑列表与松散列表都支持）"""
    def repl(m):
        checked = " checked" if m.group(1).lower() == "x" else ""
        return ('<li class="task"><input type="checkbox" disabled%s> %s</li>'
                % (checked, m.group(2).strip()))

    return re.sub(
        r'<li>\s*(?:<p>)?\[([ xX])\]\s*([\s\S]*?)(?:</p>)?\s*</li>',
        repl,
        body,
    )


IMG_RE = re.compile(r'<img alt="([^"]*)" src="([^"]+\.svg)"\s*/?>')


def inline_svg(body_html):
    """把指向 assets/figs 的 <img> 替换为内联 SVG，使 HTML 自包含、打印/PDF 无路径依赖。"""
    def repl(m):
        alt, src = m.group(1), m.group(2)
        path = os.path.normpath(os.path.join(ROOT, "chapters", src))
        if not os.path.isfile(path):
            path = os.path.normpath(os.path.join(ROOT, src))
        if not os.path.isfile(path):
            return m.group(0)
        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()
        return '<figure class="fig">%s</figure>' % svg

    return IMG_RE.sub(repl, body_html)


def md_to_html(text):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "attr_list", "sane_lists"],
    )
    return inline_svg(gfm_checkboxes(md.convert(text)))


def render_page(title, meta, body_html, nav_html):
    tags = ""
    for k in ("module", "chapter", "status"):
        if meta.get(k):
            tags += '<span class="tag">%s %s</span>' % (html.escape(k), html.escape(meta[k]))
    if meta.get("word_count"):
        tags += '<span class="tag">%s 字</span>' % html.escape(meta["word_count"])
    meta_line = '<div class="meta">%s</div>' % tags if tags else ""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s | %s</title>
<style>%s</style>
</head>
<body>
<div class="wrap">
<nav>
  <div class="brand">%s</div>
  <div class="brand-sub">%s</div>
  %s
  <div class="legend">6 模块 · 18 章 · 附录 A–F</div>
</nav>
<main>
<h1>%s</h1>
%s
%s
</main>
</div>
</body>
</html>
""" % (
        html.escape(title), html.escape(SITE_TITLE), CSS,
        html.escape(SITE_TITLE), html.escape(SITE_SUB), nav_html,
        html.escape(title), meta_line, body_html,
    )


def build_nav(current_slug, existing, rel_prefix=""):
    out = []
    for mod_name, items in MODULES:
        out.append('<div class="grp"><div class="grp-t">%s</div>' % html.escape(mod_name))
        for num, slug, label in items:
            if slug in existing:
                cls = ' class="on"' if slug == current_slug else ""
                out.append('<a href="%s%s.html"%s>%s</a>' % (rel_prefix, slug, cls, html.escape(label)))
            else:
                out.append('<span class="todo">%s　·　待写</span>' % html.escape(label))
        out.append("</div>")
    return "\n".join(out)


def main():
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)

    existing = set()
    for _, items in MODULES:
        for _, slug, _ in items:
            if os.path.isfile(os.path.join(ROOT, "chapters", slug + ".md")):
                existing.add(slug)

    built = []
    for mod_name, items in MODULES:
        for num, slug, label in items:
            src = os.path.join(ROOT, "chapters", slug + ".md")
            if not os.path.isfile(src):
                continue
            with open(src, "r", encoding="utf-8") as f:
                raw = f.read()
            meta, body = parse_front_matter(raw)
            # 若正文以一级标题开头，抽出来当页面 H1，避免与页面标题重复
            h1 = re.match(r"^#\s+(.+?)\s*\n", body)
            if h1:
                title = h1.group(1).strip()
                body = body[h1.end():]
            else:
                title = label if num is not None else meta.get("title", label)
            body_html = md_to_html(body)
            page = render_page(title, meta, body_html, build_nav(slug, existing))
            with open(os.path.join(BUILD, slug + ".html"), "w", encoding="utf-8") as f:
                f.write(page)
            built.append((slug, title, label, mod_name))

    # index：目录页
    rows = []
    cur_mod = None
    for mod_name, items in MODULES:
        if mod_name != cur_mod:
            if cur_mod is not None:
                rows.append("</div>")
            rows.append('<div class="toc-grp"><h2>%s</h2>' % html.escape(mod_name))
            cur_mod = mod_name
        for num, slug, label in items:
            if slug in existing:
                rows.append('<p><a href="%s.html">%s</a></p>' % (slug, html.escape(label)))
            else:
                rows.append('<p style="color:#a8a8a2">%s　·　待写</p>' % html.escape(label))
    rows.append("</div>")

    n_ch = sum(1 for s, _, _, _ in built if s.startswith("m"))
    n_ap = sum(1 for s, _, _, _ in built if s.startswith("appendix"))
    idx_body = ('<div class="todo-note">共 %d 篇：前言 + 正文 %d 章 + 附录 %d 篇。'
                '本页构建自 Markdown 单一源。</div>' % (len(built), n_ch, n_ap)) + "\n".join(rows)
    with open(os.path.join(BUILD, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_page("目录", {}, idx_body, ""))

    print("built %d pages -> %s" % (len(built) + 1, BUILD))
    for s, _, label, _ in built:
        print("  ", s + ".html", "|", label)


if __name__ == "__main__":
    main()
