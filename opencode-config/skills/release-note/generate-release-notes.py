#!/usr/bin/env python3
"""Generate semantic release notes from git changes.

Usage:
  generate-release-notes.py [<range>]

If <range> is not specified, auto-detects last tag -> HEAD.
<range> can be:
  - A single ref (e.g., v1.0) -> v1.0..HEAD
  - A range (e.g., v1.0..v2.0)
"""

import argparse
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime

CATEGORIES = [
    {
        'name': 'Features',
        'emoji': '\U0001f680',
        'prefixes': ['feat', 'feature'],
        'keywords': ['add', 'new', 'implement', 'support', 'introduce', 'create', 'enable'],
    },
    {
        'name': 'Bug Fixes',
        'emoji': '\U0001f41b',
        'prefixes': ['fix', 'bugfix', 'hotfix'],
        'keywords': ['fix', 'bug', 'crash', 'incorrect', 'wrong', 'error', 'issue', 'patch'],
    },
    {
        'name': 'Performance',
        'emoji': '\u26a1',
        'prefixes': ['perf'],
        'keywords': ['performance', 'speed', 'fast', 'optimize', 'latency', 'slow', 'cache'],
    },
    {
        'name': 'Cleanup',
        'emoji': '\U0001f9f9',
        'prefixes': ['refactor', 'chore', 'test', 'ci', 'build'],
        'keywords': ['cleanup', 'refactor', 'rename', 'move', 'remove', 'delete',
                      'simplif', 'deprecat', 'extract', 'restructur'],
    },
    {
        'name': 'Cosmetic',
        'emoji': '\U0001f484',
        'prefixes': ['style', 'docs', 'cosmetic', 'typo'],
        'keywords': ['typo', 'cosmetic', 'format', 'lint', 'beautify', 'prettif', 'spelling'],
    },
]

DEFAULT_CATEGORY = 'Other'


def git(*args):
    try:
        result = subprocess.run(['git'] + list(args), capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"git error: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("git: command not found", file=sys.stderr)
        sys.exit(1)


def last_tag():
    try:
        return git('describe', '--tags', '--abbrev=0').strip()
    except SystemExit:
        return None


def resolve_range(range_arg):
    if not range_arg:
        tag = last_tag()
        if tag:
            return f"{tag}..HEAD", tag, 'HEAD'
        print("No tags found. Specify a range (e.g. v1.0..HEAD).", file=sys.stderr)
        sys.exit(1)
    if '..' in range_arg:
        a, b = range_arg.split('..', 1)
        return range_arg, a, b
    return f"{range_arg}..HEAD", range_arg, 'HEAD'


RECORD_SEP = '\x1e'
FIELD_SEP = '\x1f'


def get_commits(range_spec):
    raw = git('log', '--no-merges',
              f'--format=%H{FIELD_SEP}%an{FIELD_SEP}%ae{FIELD_SEP}%ai{FIELD_SEP}%s{FIELD_SEP}%b{RECORD_SEP}',
              range_spec)
    if not raw.strip():
        return []
    commits = []
    for record in raw.split(RECORD_SEP):
        record = record.strip()
        if not record:
            continue
        parts = record.split(FIELD_SEP)
        if len(parts) < 5:
            continue
        commits.append({
            'hash': parts[0],
            'author_name': parts[1],
            'author_email': parts[2],
            'date': parts[3],
            'subject': parts[4],
            'body': parts[5] if len(parts) > 5 else '',
        })
    return commits


def get_stats(range_spec):
    raw = git('diff', '--numstat', range_spec)
    if not raw.strip():
        return {'files': 0, 'ins': 0, 'del': 0}
    files = 0
    ins = 0
    dels = 0
    for line in raw.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) >= 3:
            files += 1
            if parts[0] != '-':
                ins += int(parts[0])
            if parts[1] != '-':
                dels += int(parts[1])
    return {'files': files, 'ins': ins, 'del': dels}


def detect_remote():
    try:
        url = git('remote', 'get-url', 'origin').strip()
    except SystemExit:
        return None
    patterns = [
        (r'github\.com[:/]([^/]+)/(.*?)\.git$', 'github', 'compare/%s...%s'),
        (r'gitlab\.com[:/]([^/]+)/(.*?)\.git$', 'gitlab', '-/compare/%s...%s'),
        (r'bitbucket\.org[:/]([^/]+)/(.*?)\.git$', 'bitbucket', 'branches/compare/%s%%0D%s'),
    ]
    for pat, host, tmpl in patterns:
        m = re.search(pat, url)
        if m:
            owner, repo = m.group(1), m.group(2)
            base = f'https://{host}.com/{owner}/{repo}'
            return {'base': base, 'compare_tmpl': f'{base}/{tmpl}'}
    return {'base': None, 'compare_tmpl': None}


def link_issues(text, remote):
    if not remote or not remote.get('base'):
        return text
    base = remote['base']
    text = re.sub(r'(?<!\w)#(\d+)', lambda m: f'[#{m.group(1)}]({base}/issues/{m.group(1)})', text)
    text = re.sub(r'GH[-#](\d+)', lambda m: f'[GH-{m.group(1)}]({base}/issues/{m.group(1)})', text)
    return text


def clean_subject(subject):
    s = re.sub(r'^(fixup!|squash!)\s*', '', subject)
    s = re.sub(r'^\w+(\([^)]*\))?!?:\s*', '', s).strip()
    return s[0].upper() + s[1:] if s else s


def categorize(commit):
    subj = commit['subject'].lower().strip()
    for cat in CATEGORIES:
        for prefix in cat['prefixes']:
            if re.match(rf'^{re.escape(prefix)}[(!]', subj):
                return cat['name']
    full = subj + ' ' + commit['body'].lower()
    # "typo" overrides generic "fix"
    if 'typo' in full:
        return 'Cosmetic'
    for cat in CATEGORIES:
        for kw in cat['keywords']:
            if kw in full:
                return cat['name']
    return DEFAULT_CATEGORY


def format_date(s):
    try:
        return datetime.fromisoformat(s).strftime('%Y-%m-%d')
    except Exception:
        return s[:10] if s else ''


def build(commits, stats, remote, from_ref, to_ref):
    lines = [f"## {from_ref} \u2192 {to_ref}", ""]
    plural = 's' if len(commits) != 1 else ''
    meta = f"{len(commits)} commit{plural}"
    if stats['files']:
        plural_f = 's' if stats['files'] != 1 else ''
        meta += f" \u00b7 {stats['files']} file{plural_f} changed \u00b7 +{stats['ins']}/\u2212{stats['del']}"
    lines.append(f"**{format_date(commits[0]['date'])}** \u00b7 {meta}")
    lines.append("")

    groups = OrderedDict()
    all_cat_names = [c['name'] for c in CATEGORIES] + [DEFAULT_CATEGORY]
    for n in all_cat_names:
        groups[n] = []

    for c in commits:
        groups[categorize(c)].append(c)

    for cat in CATEGORIES:
        entries = groups[cat['name']]
        if not entries:
            continue
        lines.append(f"### {cat['emoji']} {cat['name']}")
        lines.append("")
        for c in entries:
            subj = link_issues(clean_subject(c['subject']), remote)
            lines.append(f"- {subj}")
        lines.append("")

    other = groups[DEFAULT_CATEGORY]
    if other:
        lines.append("### Other")
        lines.append("")
        for c in other:
            subj = link_issues(clean_subject(c['subject']), remote)
            lines.append(f"- {subj}")
        lines.append("")

    if remote and remote.get('compare_tmpl'):
        lines.append(f"**Full Changelog**: {remote['compare_tmpl'] % (from_ref, to_ref)}")
        lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Generate semantic release notes from git changes.")
    ap.add_argument('range', nargs='?',
                    help="Range (e.g. v1.0..v2.0) or ref (e.g. v1.0 for v1.0..HEAD)")
    args = ap.parse_args()

    range_spec, from_ref, to_ref = resolve_range(args.range)
    commits = get_commits(range_spec)
    if not commits:
        print(f"No commits in range {range_spec}", file=sys.stderr)
        sys.exit(1)
    stats = get_stats(range_spec)
    remote = detect_remote()
    print(build(commits, stats, remote, from_ref, to_ref))


if __name__ == "__main__":
    main()
