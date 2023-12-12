# Collab_Number_Wall
This project is looking to investigate generating Number Walls primarily using
the Paper Folding sequence, looking to find a complete set of tiling for mod 7, and more.

## Quickstart Testing
TODO

## Function Overview
TODO

## Expected Outputs
Below is a list of the expected outputs from core functions for common/expected
input parameters. This will allow you to quickly verify that the code has run correctly,
which is useful when altering functionality or improving computational complexity.

TODO - add more

### Tiling Function
Input:
- prime_input=3
- sequence=paper_folding_seq (pap_f)
- tile_length=8
Output= 211 unique tiles after approx 200 slices

Input:
- prime_input=7
- sequence=paper_folding_seq (pap_f)
- tile_length=8
Output= 302,835 unique tiles after approx 15,000 slices (stabilising at 7500 slices)

## External links
You can find several papers discussing the background to this work below:
- [link_text1](https://<add a link here>)
- [link_text2](https://<add another link here>)

## Git Cheat Sheet
Below is a list of Git commands, and their general usage + notes.
To use git commands, you should be running a terminal inside the folder with the
Collab_Number_Wall code - you can navigate to this place via the `cd folder_name`
and `dir` commands (in CMD).
Any references to 'repositories' (or 'repo') means either your local copy of the code (local repository)
or the Github-hosted copy of the code (remote repository).

- **git status**
This command gives you an overview of the current state of your local repository.
It will list:
1. What branch you are on
2. whether your branch is up to date with the latest changes to the remote repo (based on your last git fetch)
3. Any files that you have added to your 'staging area' (ready to be committed), in green
4. Any files that have been changed, but not yet added to your 'staging area', in red

- **git fetch**
This command will retrieve an up-to-date history of changes in the remote repository, such as
new branches, and code commits. It is helpful to run this at the start of each work session you do.

- **git pull**
This command will pull any new changes from the remote repository version of your current branch
into your local copy of that branch. This is useful for when someone else has completed work on
the same branch as you, and you would like to get their updates.
**NOTE:** If you have made changes to the same lines in the same files as the changes in the remote
repository, you will have what is called a merge conflict, and will need to solve the conflict by
picking whose changes should be kept. You would then need to push that completed merge to the remote
repository for the other person to also get the resolved code.

- **git checkout**
This command lets you swap between branches, by stating the name of the new branch you would like
to move to. If it is a branch that does not exist in either the remote repository or your local
repository, then you can create it by adding the -b parameter, e.g.
```
git checkout test_branch -b
```
Once you have created a new branch locally, you would need to push it to the remote repository
to be able to view it in Github.
**HINT:** If you've made changes to your current branch (that you have not yet added to your 'staging area'), you can remove all the changes and reset your local branch to the last commit
by running `git checkout .`

- **git diff**
This command runs you through all the **unstaged** changes (adding new content shows in green,
removing old content shows in red) that you have currently made to the branch you are currently
on locally. It is useful to spot typos and trailing white space (shown as red blocks), that can
then be fixed before you commit. Use the up/down arrow keys to move through the diff line-by-line,
and press `Q` when you have finished viewing it to break out.

- **git add**
This command lets you add your file/code changes to your 'staging' area. This is essentially a
list of file changes that you would like to commit to your local repository (and eventually the
remote repository). This is useful, as you may not always want to commit all of your changes/new
files! You can add files by name, e.g.
```
git add file_test1.sh file_test2.txt file_test3.py
```
Or you can add all 'unstaged' file changes, e.g.
```
git add -A
```

- **git commit**
This command lets you bundle all of your 'staged' file changes (via `git add`) into a single
'commit' object that is added to your repository. A commit holds the details of every line change
that you have added to it (viewable easily in Github), as well as your configured git identity, and your repository holds the
history of every single commit added to it (unless you use special parameters to alter the history).
When you create a commit, you should always add a meaningful message to the commit, so it is clear
to others (and your future self!) what that commit contained, e.g.
```
git commit -m "Updated documentation of collate.py and fixed a rare edge-case bug."
```
Commits are added to your local repository first, and should be pushed up to the remote repository
when you are ready.

- **git push**
This command lets you push any committed changes you have made to your local repository, up to the
remote repository. This will allow others to view your changes, and deploy/test those changes themselves.

- **git merge**
Just ask for help if you're needing to do a merge, they can be complex to get right.

### Example Daily Workflow
Check for any new commits to the remote repository (Github) before starting:
```
git fetch
git status
```
If required, pull new changes into your local code:
(This may cause code conflicts if you have changed lines that have also changed in the remote repository)
```
git pull
```
Complete some work on the codebase, and inspect changed files + lines:
(Use arrow keys to search through the git diff, and 'q' to break out of it)
```
git status
git diff
```
Add code changes to your 'staged' area, and then commit those changes:
(You can add multiple space-separated files in one git add, or use -A to add all)
```
git add <file name>
git commit -m "<Add a meaningful Commit message>"
```
Push your changes to the remote repository (Github):
```
git push
```
Relax after a hard day's work...