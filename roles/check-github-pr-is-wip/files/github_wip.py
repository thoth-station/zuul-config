#!/usr/bin/python3
#
# Job testing a GitHub PR for presence of specific WIP labels
# or specific WIP keywords in PR title, in order to block merging.
#
# Copyright 2018 Thierry Carrez <thierry@openstack.org>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import json
import re
import sys
import urllib.request


def get_github_PR(change_url):
    match = re.search(r".*/([^/]+/[^/]+)/pulls?/(\d+)", change_url)
    repository = match.group(1)
    prnumber = match.group(2)

    url = "https://api.github.com/repos/%s/pulls/%s" % (repository, prnumber)

    with urllib.request.urlopen(url) as link:
        data = json.loads(link.read().decode())
    return data


def is_wip(change, wip_keywords, wip_labels):
    for wip_keyword in wip_keywords:
        if wip_keyword in change["title"]:
            print("%s is mentioned in PR title" % wip_keyword)
            return True

    for label in change["labels"]:
        for wip_label in wip_labels:
            if label["name"] == wip_label:
                print("PR is labeled %s" % wip_label)
                return True

    print("No blocking marker found, this PR is OK to merge")
    return False


def main():
    parser = argparse.ArgumentParser(description="Is the PR blocked ?")
    parser.add_argument("change_url", help="GitHub PR URL")
    parser.add_argument("keywords", help="Key words in PR title to block on")
    parser.add_argument("labels", help="Names of labels to block on")
    args = parser.parse_args()

    change = get_github_PR(args.change_url)
    sys.exit(is_wip(change, args.keywords.split(), args.labels.split()))


if __name__ == "__main__":
    main()
