Fail if any WIP labels are attached to a given GitHub PR, or if
any WIP keywords are included in a given GitHub PR title.

**Role Variables**

.. zuul:rolevar:: github_pr

   URL for the GitHub PR to check. Should be something like:
   https://github.com/kata-containers/runtime/pull/1112

.. zuul:rolevar:: wip_labels

   Space-separated label names to consider as WIP labels.

.. zuul:rolevar:: wip_keywords

   Space-separated keywords to consider as WIP keywords in PR titles.

This is a straight forward port of https://opendev.org/kata-containers/zuul-config/
