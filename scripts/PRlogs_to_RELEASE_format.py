#!/usr/bin/env python3

import re
import subprocess

format_separator = "||"
readme_pr_format = "* PR #{pr_num} {pr_desc} (@{pr_author})"

git_command = 'git log origin/master ^origin/release --merges --pretty="%s{}%b"'.format(format_separator)

p = subprocess.Popen(git_command + ' | grep "pull request"',
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
retval = p.wait()

merged_pull_requests = p.stdout.readlines()

regex = re.compile('Merge pull request \#([\d]+) from ([^/]+)/.+?')

non_matched_prs = []
matched_prs = []
for byte_pr in merged_pull_requests:
    pr = byte_pr.decode().strip()
    pr_s, pr_desc = pr.split(format_separator)
    if not re.fullmatch(regex, pr_s):
        non_matched_prs << pr
        continue
    groups = re.match(regex, pr_s).groups()

    matched_prs.append((int(groups[0]), pr_desc, groups[1]))


matched_prs = sorted(matched_prs, key=lambda pr: pr[0])

for pr in matched_prs:
    formatted = readme_pr_format.format(pr_num=pr[0],
                                        pr_desc=pr[1],
                                        pr_author=pr[2])
    print(formatted)

if len(non_matched_prs) > 0:
    print("WARNING: Following prs were not included")
    for pr in non_matched_prs:
        print("\t{}".format(pr))
