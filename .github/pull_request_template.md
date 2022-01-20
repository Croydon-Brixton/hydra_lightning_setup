<!-- Pull request template -->

## 🚀 Description

<!--
Describe the big picture of your changes here to communicate
to the team lead and the rest of your team why they should accept
this pull request. If it fixes a bug or resolves a feature request,
be sure to link to that issue on Trello.
-->

Please explain the changes you have made.

Major changes:

- Added a `foo` function to do xyz.
- Changed init signature of `bar` class to accomodate xyz.

Other changes:

- Updated docstring for `myfunc`

## 🧐 Other information

<!--
If this is a relatively large or complex change,
kick off the discussion by explaining why you
chose the solution you did and what alternatives
you considered, etc.
-->

Delete this section, if you don't need it.

## ⬇️ Dependencies

Delete this section, if you don't need it.
This PR improves on the following work and should therefore be merged afterward:

- PR #1
- PR #3
- e.g.

---

<!--
Please check if your PR fulfills the following requirements.
Put an `x` in the boxes that apply. You can also fill these
out after creating the PR. If you're unsure about any of them,
don't hesitate to ask.
This is a reminder of what we are going to look for  before
merging your code.
-->

> 🚨 **Checklist**
>
> - [ ] **DO** keep pull requests small so they can be easily reviewed.
> - [ ] **REMOVE** notebooks or files that are not absolutely needed on the remote from the git cache (`git rm --cached <filepath>`)
> - [ ] **ADHERE** to the [Coding guidelines](https://google.github.io/styleguide/pyguide.html)
> - [ ] **DOCUMENT** all functions with more than 10 lines of code with a [docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
> - [ ] **FORMAT** (`make format`) your code locally push any changes
> - [ ] **LINT** (`make lint`) your code locally and fix any failures
