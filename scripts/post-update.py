"""Prepare a manual announcement locally. This script never commits or pushes."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
START = "        <!-- posts:start -->"
END = "        <!-- posts:end -->"


def render_post(post):
    stamp = date.fromisoformat(post["date"])
    label = "Important" if post["important"] else "Update"
    lines = [
        '            <article class="update-post">',
        '              <div class="update-meta">',
        f'                <span class="update-badge">{label}</span>',
        f'                <time datetime="{stamp.isoformat()}">{stamp.day} {stamp:%B %Y}</time>',
        '              </div>',
        f'              <h3>{escape(post["title"])}</h3>',
        f'              <p>{escape(post["message"])}</p>',
    ]
    if post["link"]:
        lines.append(f'              <a class="update-link" href="{escape(post["link"], quote=True)}">{escape(post["link_label"])} <span aria-hidden="true">↗</span></a>')
    return "\n".join(lines + ['            </article>'])


def render(posts):
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    recent = [post for post in posts if not post.get("archive_only", False)][:5]
    lines = [START]
    if posts:
        lines += [
            '        <section class="updates" aria-labelledby="updates-title">',
            '          <details class="updates-archive">',
            '            <summary class="updates-heading">',
            '              <h2 id="updates-title">Noticeboard</h2>',
            f'              <span class="updates-show-all">View all history ({len(posts)}) <span aria-hidden="true">＋</span></span>',
            '              <span class="updates-show-recent">Back to latest five <span aria-hidden="true">−</span></span>',
            '            </summary>',
            '            <div class="updates-history">',
            '              <p class="updates-caption">All announcements · newest first</p>',
            *[render_post(post) for post in posts],
            '            </div>',
            '          </details>',
            '          <div class="updates-list">',
            '            <p class="updates-caption">Latest announcements</p>',
            *[render_post(post) for post in recent],
            '          </div>',
            '        </section>',
        ]
    return "\n".join(lines + [END])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--important", action="store_true")
    parser.add_argument("--archive-only", action="store_true",
                        help="Show this post only in expanded history.")
    parser.add_argument("--link", default="")
    parser.add_argument("--link-label", default="Read more")
    args = parser.parse_args()
    date.fromisoformat(args.date)
    if not args.title.strip() or not args.message.strip():
        parser.error("Title and message must not be empty.")
    if args.link and not (args.link.startswith("https://") or re.fullmatch(r"\./pdfs/[a-z0-9-]+\.pdf(?:#page=[1-9][0-9]*)?", args.link)):
        parser.error("Use an https:// URL or a local ./pdfs/course.pdf link.")
    if args.link.startswith("./") and not (ROOT / "dist" / args.link.split("#")[0]).is_file():
        parser.error("The linked PDF does not exist.")

    index_path = ROOT / "dist/index.html"
    posts_path = ROOT / "dist/posts.json"
    # Preserve every byte outside the announcement region, including line endings.
    index = index_path.read_bytes().decode("utf-8")
    if index.count(START) != 1 or index.count(END) != 1 or index.index(START) > index.index(END):
        parser.error("Expected exactly one announcement region in index.html.")
    posts = json.loads(posts_path.read_text(encoding="utf-8")) if posts_path.exists() else []
    post = {"date": args.date, "title": args.title, "message": args.message,
            "important": args.important, "link": args.link, "link_label": args.link_label,
            "archive_only": args.archive_only}
    if any(p["title"] == post["title"] and p["date"] == post["date"] for p in posts):
        parser.error("A post with this title and date already exists.")
    posts = sorted([post, *posts], key=lambda p: p["date"], reverse=True)
    region = render(posts)
    newline = "\r\n" if "\r\n" in index else "\n"
    index = index[:index.index(START)] + region.replace("\n", newline) + index[index.index(END) + len(END):]
    posts_path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index_path.write_bytes(index.encode("utf-8"))
    print("Announcement prepared locally. Nothing has been committed or uploaded.")


if __name__ == "__main__":
    main()
