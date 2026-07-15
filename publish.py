#!/usr/bin/env python3
"""发布新文章到博客"""
import sys, os
from datetime import datetime

BLOG = os.path.expanduser("~/blog")

def publish(title, content):
    slug = datetime.now().strftime("%Y-%m-%d-") + title.replace(" ", "-").lower()[:30]
    date = datetime.now().strftime("%Y-%m-%d")

    # 写 Markdown 文件
    md_path = f"{BLOG}/posts/{slug}.md"
    with open(md_path, "w") as f:
        f.write(f"# {title}\n\n> {date}\n\n{content}\n")

    # 更新首页
    with open(f"{BLOG}/index.html") as f:
        html = f.read()

    card = f'<div class="post"><h2><a href="posts/{slug}.md">{title}</a></h2><time>{date}</time><p class="summary">{content[:100]}...</p></div>\n'

    start = html.find("<!-- POSTS_START -->") + len("<!-- POSTS_START -->")
    end = html.find("<!-- POSTS_END -->")
    html = html[:start] + "\n" + card + html[start:end] + html[end:]

    with open(f"{BLOG}/index.html", "w") as f:
        f.write(html)

    print(f"✅ 已发布: {title}")
    print(f"📄 Markdown: {md_path}")
    print(f"🌐 首页已更新: {BLOG}/index.html")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 publish.py '标题' '内容'")
        sys.exit(1)
    publish(sys.argv[1], sys.argv[2])
