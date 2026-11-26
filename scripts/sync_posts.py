"""Convert writer-hub published posts into Jekyll posts for jorzel.github.io.

Usage (from the blog root):
    python3 -I scripts/sync_posts.py ~/Coding/writer-hub . scripts/tags.json
    python3 -I tag_generator.py

Every post in published_posts.md except OLD_POSTS (hand-maintained blog posts) and
SKIP is regenerated from writer-hub on each run, together with its images.
OLD_POSTS files are never modified. A new post needs an entry in tags.json and,
if its markdown lacks images, an EXTRA_IMAGES entry.
"""
import glob
import json
import os
import re
import shutil
import sys

SKIP = {"toward-successful-teams.md"}  # earlier version of "5 traits of a successful team"

# writer-hub file -> blog _posts stem (without date) for posts already on the blog
OLD_POSTS = {
    "persistence-and-domain-model-separation-using-sqlalchemy-orm.md": "persistance-and-domain-model-separation-using-sqlalchemy-orm",
    "flask-mvt-refactor-to-service-layer.md": "flask-mvt-refactor-to-service-layer",
    "coupling-two-perspectives.md": "two-perspectives-of-coupling",
    "graphql-api-and-rest-api-mirror-implementations-in-python.md": "graphql-api-and-rest-api-mirror-impementations-in-python",
    "graphql-authentication-and-authorization.md": "graphql-authentication-and-authorization",
    "ports-and-adapters-architecture-python-nameko-microexample.md": "ports-and-adapters-architecture-python-nameko-microexample",
    "value-object-persistence-strategies.md": "value-object-persistance",
    "concurrent-write-problem.md": "concurrent-write-problem",
    "an-orm-can-bite-you.md": "an-orm-can-bite-you",
    "different-types-of-application-logic.md": "different-types-of-application-logic",
    "when-a-database-query-is-unexpectedly-slow.md": "when-a-database-query-is-unexpectedly-slow",
    "how-to-build-postgresql-full-text-search-engine-in-any-language.md": "how-to-build-postgresql-full-text-search-engine-in-any-language",
    "continuous-learning-framework.md": "continuous-learning-framework",
    "atomic-habits-implemented.md": "atomic-habits-implemented",
    "deep-work.md": "deep-work-essentialism-in-asynchronous-culture",
    "how-to-visualize-your-system-architecture-using-the-c4-model.md": "how-to-visualize-your-system-architecture-using-the-c4-model",
    "5-traits-of-a-successful-team.md": "5-traits-of-a-successful-team",
    "kubernetes-first-steps.md": "kubernetes-first-steps",
    "efficiency-traps.md": "efficency-traps",
    "how-to-use-prometheus-for-web-application-monitoring.md": "how-to-use-prometheus-for-web-application-monitoring",
    "6-nonobvious-tools-that-should-be-in-your-command-line-toolbox.md": "6-nonobvious-tools-that-should-be-in-your-command-line-toolbox",
    "finding-enjoyment.md": "finding-enjoyment",
    "step-by-step-guide-to-safely-introducing-high-risk-changes-in-your-software-system.md": "step-by-step-guide-to-introducing-high-risk-changes-in-your-software",
    "how-to-build-an-alerting-system-with-prometheus-and-alertmanager.md": "how-to-build-an-alerting-system-with-prometheus-and-alertmanager",
    "finding-flow-how-to-experience-greater-engagement-in-your-work.md": "finding-flow-how-to-experience-greater-engagement-in-your-work",
    "talent-is-overestimated.md": "talent-is-overestimated",
    "repository-pattern-in-golang-redis-and-external-api-as-providers.md": "repository-pattern-in-golang",
    "power-of-conventions.md": "the-power-of-conventions-in-software-development",
    "strategic-ddd-subdomains.md": "strategic-domain-driven-design-by-example-subdomains",
    "dangerous-short-term-gains.md": "dangerous-short-term-gains",
    "how-codebase-structure-shapes-system-predictability.md": "how-codebase-structure-shapes-system-predictability",
    "continuous-learning-framework-vol-2.md": "continuous-learning-framework-vol-2",
    "understanding-distributed-tracing-a-python-guide-with-opentelemetry-and-grafana-tempo.md": "understanding-distributed-tracing",
}

# hashnode slugs that differ from any writer-hub frontmatter slug -> writer-hub file
HASHNODE_SLUG_ALIASES = {
    "the-power-of-conventions-in-software-development": "power-of-conventions.md",
    "strategic-domain-driven-design-subdomains-identification": "strategic-ddd-subdomains.md",
}

# "(link)" placeholders in sources: link text -> writer-hub file
PLACEHOLDER_LINKS = {
    "The Myth of Natural Talent": "the-myth-of-natural-talent.md",
    "Does Mastery Require Giftedness?": "the-talent-debate-does-mastery-require-giftedness.md",
    "Talent is a Loop": "talent-is-a-loop.md",
    "Talent as a Loop, Not a Gift": "talent-is-a-loop.md",
    "Why You Must Invest Before You Know": "why-you-must-invest-before-you-know.md",
    "Why Child Prodigies Rarely Become Superstars": "why-child-prodigies-rarely-become-superstars.md",
    "The Scaffolding Trick": "the-scaffolding-trick.md",
    "When Deliberate Practice Isn't Enough": "when-deliberate-practice-isnt-enough.md",
    "Karen Carpenter": "coming-out-of-the-shadows-how-karen-carpenter-developed-her-talent.md",
}

BLOG_URL = "https://jorzel.github.io"

DROPBOX = os.path.expanduser("~/Dropbox/prezentacje")
HUB_ASSETS = os.path.expanduser("~/Coding/writer-hub/assets")
HUB_IMAGES = os.path.expanduser("~/Coding/writer-hub/posts/published/images")

# Images missing from the source markdown, placed by an anchor in the text:
#   ("replace", <regex of placeholder line>) | ("after", <text in paragraph>) | ("before", <line prefix>) | ("top", None)
# Entries: (source file, published name, anchor kind, anchor, alt text, caption or None)
EXTRA_IMAGES = {
    "the-scaffolding-trick.md": [
        (f"{DROPBOX}/scaffolding/loop.excalidraw.png", "scaffolding-loop.png", "replace", r"<!-- DIAGRAM: Scaffolding-to-Loop.*-->",
         "Scaffolding as a ladder to the first rotation of the loop", None),
        (f"{DROPBOX}/scaffolding/zpd.excalidraw.png", "scaffolding-zpd.png", "replace", r"<!-- DIAGRAM: Zone of Proximal Development.*-->",
         "Zone of Proximal Development", None),
        (f"{DROPBOX}/scaffolding/support.excalidraw.png", "scaffolding-support.png", "replace", r"<!-- DIAGRAM: Fading Spectrum.*-->",
         "Autonomous competence against the scaffolded support period: a sweet spot between too little and too much support", None),
        (f"{HUB_ASSETS}/scaffolding-trick/painting_progress_small.gif", "scaffolding-painting-progress.gif", "replace", r"<!-- TODO: embed painting_progress.*-->",
         "Painting by numbers, step by step", None),
    ],
    "winston-star.md": [
        (f"{DROPBOX}/winston-star/winston-star.png", "winston-star.png", "replace", r"<!-- DIAGRAM: Five-pointed star.*-->",
         "The Winston Star: Symbol, Slogan, Surprise, Salient Idea, Story", None),
    ],
    "the-talent-manufacturing-pipeline.md": [
        (f"{DROPBOX}/talent-pipleine/loop-pipeline.excalidraw.png", "talent-pipeline-loop-pipeline.png", "replace", r"<!-- DIAGRAM: loop-pipeline\.png.*-->",
         "Loop strength against pipeline strength", None),
        (f"{DROPBOX}/talent-pipleine/scaffolded-gifted.png", "talent-pipeline-scaffolded-gifted.png", "replace", r"<!-- DIAGRAM: scaffolded-gifted\.png.*-->",
         "Two paths to similar performance with different scaffold density", None),
    ],
    "the-compassionate-lie.md": [
        (f"{DROPBOX}/antiessentialism/multiplier_effect.png", "compassionate-lie-multiplier-effect.png", "replace", r"<!-- DIAGRAM: multiplier-divergence\.png.*-->",
         "Multiplier and inverse multiplier: two ability trajectories diverging over time", None),
    ],
    "why-child-prodigies-rarely-become-superstars.md": [
        (f"{DROPBOX}/prodigies/prodigies.excalidraw.png", "prodigies-performance.png", "after", "The authors offer three potential explanations.",
         "Accelerated early progress against a multidisciplinary approach over age", None),
        (f"{DROPBOX}/prodigies/local_optimum.excalidraw.png", "prodigies-local-optimum.png", "after", "Early specialization always risks finding a local minimum.",
         "Local and global optimum", None),
    ],
    "oh-my-claude-how-software-development-is-changing-with-agentic-coding.md": [
        (f"{DROPBOX}/agentic_coding/complexity_field.excalidraw.png", "agentic-coding-complexity-field.png", "after", "**Complexity and field maturity**",
         "Productivity gains by task complexity and project maturity", None),
        (f"{DROPBOX}/agentic_coding/context_window.excalidraw.png", "agentic-coding-context-window.png", "after", "**Context management is everything**",
         "Long-context performance drops as context length grows", None),
        (f"{DROPBOX}/agentic_coding/leverage.excalidraw.png", "agentic-coding-leverage.png", "after", "If you fail at the specification stage",
         "A bad decision in research grows through plan and implementation", None),
    ],
    "why-you-must-invest-before-you-know.md": [
        (f"{DROPBOX}/pragmatic-talent/compounding.excalidraw.png", "invest-compounding.png", "after", "We're bad at visualizing compounding.",
         "Compounding against linear growth over time", None),
    ],
    "what-does-it-mean-to-accept-emotions.md": [
        (f"{DROPBOX}/emotion_regulation/distance.excalidraw.png", "emotions-distance.png", "after", "Both Magness and Wright arrive at the same fundamental insight",
         "Emotion leading straight to a reaction, versus distance leading to a response", None),
    ],
    "coming-out-of-the-shadows-how-karen-carpenter-developed-her-talent.md": [
        (f"{HUB_IMAGES}/Karen_Carpenter_on_drumkit.jpg", "karen-carpenter-on-drumkit.jpg", "after", "Or maybe not.",
         "Karen Carpenter behind the drum kit",
         "Karen Carpenter behind the kit. A&M publicity photo, 1973. Public domain, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Karen_Carpenter_on_drumkit.jpg)"),
        (f"{HUB_IMAGES}/lead_sister.jpg", "karen-carpenter-lead-sister.jpg", "after", "## A Girl in the Shadows",
         "Lead Sister: The Story of Karen Carpenter book cover",
         "\"Lead Sister: The Story of Karen Carpenter\" by Lucy O'Brien (Manilla Press, 2023) — the main source for this essay."),
    ],
    "a-life-which-is-a-warning.md": [
        (f"{HUB_IMAGES}/oblomov-chichagov-zakhar.jpg", "oblomov-chichagov-zakhar.jpg", "after", "He spends almost all of his time lying on the sofa.",
         "Oblomov lying in bed while Zakhar stands beside him, illustration by Chichagov", None),
    ],
    "what-went-wrong-with-out-happiness.md": [
        (f"{HUB_IMAGES}/happiness-hammershoi-interior.jpg", "happiness-hammershoi-interior.jpg", "top", None,
         "Vilhelm Hammershøi, interior with open doors and a woman in the next room", None),
    ],
}


def image_block(name, alt, caption):
    block = f"![{alt}](/images/{name})"
    return block + (f"\n\n*{caption}*" if caption else "")


def place_images(post, body, blog_dir, copies):
    """Rewrite local image refs to /images/ and insert EXTRA_IMAGES; record files to copy."""
    def local_ref(m):
        copies.append((os.path.join(HUB_IMAGES, m.group(2)), m.group(2)))
        return f"![{m.group(1)}](/images/{m.group(2)})"

    body = re.sub(r"!\[([^\]]*)\]\(images/([^)\s]+)\)", local_ref, body)
    for src, name, kind, anchor, alt, caption in EXTRA_IMAGES.get(post, []):
        block = image_block(name, alt, caption)
        if kind == "replace":
            body, n = re.subn(anchor, lambda _m: block, body)
        elif kind == "top":
            body, n = block + "\n\n" + body, 1
        else:  # after: insert after the paragraph (or heading line) containing the anchor
            paras = body.split("\n\n")
            idx = [i for i, p in enumerate(paras) if anchor in p]
            n = len(idx)
            if n == 1:
                paras.insert(idx[0] + 1, block)
                body = "\n\n".join(paras)
        if n != 1:
            raise SystemExit(f"{post}: anchor {anchor!r} matched {n} times")
        copies.append((src, name))
    return body


def parse_index(path):
    rows = []
    for line in open(path, encoding="utf8"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\S+\.md)\s*\|", line)
        if m:
            title = m.group(2)
            if title.startswith('"') and title.count('"') == 2 and title.endswith('"'):
                title = title[1:-1]
            rows.append({"title": title, "date": m.group(3), "file": m.group(4)})
    return rows


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---", 4)
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            fm[key.strip()] = value.rstrip('"')
    body = text[end + 4:].lstrip("\n")
    return fm, body


def blog_stem_to_url(blog_dir):
    urls = {}
    for path in glob.glob(os.path.join(blog_dir, "_posts", "*.md")):
        stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", os.path.basename(path)[:-3])
        fm, _ = split_frontmatter(open(path, encoding="utf8").read())
        urls[stem] = fm.get("slug") or stem
    return urls


def strip_draft_notes(name, body):
    """Remove author-only scaffolding left in two published sources."""
    if name == "the-compassionate-lie.md":
        body = body[body.index('### 1. "It\'s okay'):]
        body = body[: body.index("\n## Notes from research used")].rstrip().rstrip("-").rstrip()
        body = re.sub(r"^### \d\. ", "## ", body, flags=re.M)
    elif name == "the-talent-manufacturing-pipeline.md":
        body = body[body.index("## 1. The Scene"):]
        body = re.sub(r"^## \d\. ", "## ", body, flags=re.M)
    elif name == "the-trap-of-knowing-what-you-want.md":
        body = body[body.index("## The Modern Promise"):]
        body = body[: body.index("\n## Notes")].rstrip().rstrip("-").rstrip()
    return body


def first_paragraph(body):
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p[0] in "#>!-*|<`[" or p.startswith("%[") or re.match(r"\d+\.", p):
            continue
        p = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", p)
        p = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", p)
        p = re.sub(r"[*_`]", "", p)
        return " ".join(p.split())
    return ""


def main(hub_dir, blog_dir, tags_path=None):
    published = os.path.join(hub_dir, "posts", "published")
    rows = parse_index(os.path.join(hub_dir, "posts", "published_posts.md"))
    tags = json.load(open(tags_path)) if tags_path else {}
    old_urls = blog_stem_to_url(blog_dir)

    # writer-hub file -> blog url path, and hashnode slug -> writer-hub file
    url_of, by_hashnode_slug, posts = {}, dict(HASHNODE_SLUG_ALIASES), []
    for row in rows:
        name = row["file"]
        fm, body = split_frontmatter(open(os.path.join(published, name), encoding="utf8").read())
        slug = fm.get("slug") or name[:-3]
        by_hashnode_slug[slug] = name
        by_hashnode_slug[name[:-3]] = name
        if name in OLD_POSTS:
            url_of[name] = old_urls[OLD_POSTS[name]]
        elif name not in SKIP:
            url_of[name] = slug
            posts.append((row, fm, body, slug))

    unresolved, copies = [], []

    def link_for(name):
        return f"{BLOG_URL}/{url_of[name]}/"

    def rewrite_hashnode(m):
        slug, anchor = m.group(1), m.group(2) or ""
        name = by_hashnode_slug.get(slug)
        if name not in url_of:
            unresolved.append(m.group(0))
            return m.group(0)
        anchor = anchor.replace("#heading-", "#")
        return link_for(name) + anchor

    for row, fm, body, slug in posts:
        name = row["file"]
        if not fm:
            body = re.sub(r"\A\s*# .*\n+", "", body)  # title line; the layout renders the title
        else:
            body = re.sub(r"\A(\s*)# ", r"\1## ", body)  # a leading section heading must not compete with the title
        leading = re.match(r"\A\s*#+ (.*)\n+", body)
        if leading and leading.group(1).strip().lower() == row["title"].lower():
            body = body[leading.end():]  # repeated title; the layout renders the title
        body = strip_draft_notes(name, body)
        body = re.sub(r'\s+align="[^"]*"\)', ")", body)
        body = re.sub(r"^%\[(\S+)\]\s*$", r"[\1](\1)", body, flags=re.M)
        body = re.sub(r"https?://jorzel\.hashnode\.dev/([a-z0-9-]+)(#[a-z0-9-]+)?/?", rewrite_hashnode, body)

        def rewrite_placeholder(m):
            target = PLACEHOLDER_LINKS.get(m.group(1))
            if not target:
                unresolved.append(m.group(0))
                return m.group(0)
            return f"[{m.group(1)}]({link_for(target)})"

        body = re.sub(r"\[([^\]]+)\]\(link\)", rewrite_placeholder, body)

        def rewrite_relative(m):
            target = by_hashnode_slug.get(m.group(2))
            if target not in url_of:
                return m.group(0)
            return f"[{m.group(1)}]({link_for(target)})"

        body = re.sub(r"\[([^\]]+)\]\(([a-z0-9]+(?:-[a-z0-9]+)+)\)", rewrite_relative, body)

        body = place_images(name, body, blog_dir, copies)

        if "{{" in body or "{%" in body:
            body = "{% raw %}\n" + body.rstrip() + "\n{% endraw %}"

        description = fm.get("seoDescription") or first_paragraph(body)
        post_tags = tags.get(name, [])
        front = [
            "---",
            f"title: {json.dumps(row['title'], ensure_ascii=False)}",
            f"description: {json.dumps(description, ensure_ascii=False)}",
            f"slug: {slug}",
            f"tags: {' '.join(post_tags)}".rstrip(),
            "",
            "---",
            "",
        ]
        out = os.path.join(blog_dir, "_posts", f"{row['date']}-{name[:-3]}.md")
        with open(out, "w", encoding="utf8") as f:
            f.write("\n".join(front) + body.rstrip() + "\n")

    images_dir = os.path.join(blog_dir, "images")
    for src, name in copies:
        dest = os.path.join(images_dir, name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)  # e.g. images/url-shortener/
        shutil.copyfile(src, dest)
    print(f"written: {len(posts)} posts, {len(copies)} images")
    for u in unresolved:
        print("UNRESOLVED LINK:", u)


if __name__ == "__main__":
    main(*sys.argv[1:])
