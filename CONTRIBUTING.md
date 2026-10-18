# Working on this repo

This covers how we name branches and how to get your changes from your laptop into `main` without stepping on anyone else's work. If you've used git a lot before, skim the branch naming and "rules" bits and skip the rest. If you haven't, read it top to bottom once. It's long, but most of it is copy-paste commands.

## The short version

1. Never commit straight to `main`.
2. Pull `main` before you start anything.
3. Make a branch for your task, named using the convention below.
4. Commit small and often, push your branch.
5. Open a PR, get one teammate to review it, then merge.
6. Delete the branch once it's merged.

---

## Branch naming

Format:

```
<type>/<short-description>
```

All lowercase, words separated with hyphens, no spaces. Keep the description to a few words so it's obvious what the branch is for when you're looking at a list of them.

| Type | Use it for | Example |
|---|---|---|
| `feat/` | new functionality | `feat/abdlop-commitment` |
| `fix/` | fixing a bug | `fix/ntt-wrong-modulus` |
| `test/` | adding or fixing tests only | `test/rejection-sampling-stats` |
| `bench/` | benchmark scripts, results | `bench/sig-size-vs-ring-size` |
| `docs/` | README, notes, report drafts | `docs/setup-instructions` |
| `refactor/` | restructuring without changing behaviour | `refactor/split-poly-module` |
| `chore/` | config, dependencies, CI, gitignore etc. | `chore/add-gitignore` |
| `exp/` | throwaway experiments, might never get merged | `exp/try-smaller-p` |

If the work is tied to a GitHub issue, stick the issue number on the end:

```
feat/recursive-proof-12
fix/verify-rejects-valid-sig-27
```

Don't do these:

- `tushar-branch`, `my-changes`, `test`, `new`: they don't say what's in them
- `Feat/ABDLOP_Commitment`: no capitals, no underscores
- `feat/implement-the-abdlop-commitment-scheme-from-section-2-6`: too long

`main` is the only long-lived branch. Everything else is temporary.

---

## Commit messages

Nothing fancy. Write a short line in the present tense saying what the commit does:

```
Add ABDLOP commit and open functions
Fix off-by-one in tensor product index
Add tests for bimodal rejection rate
```

If it needs explaining, leave a blank line and write a few more lines underneath. Avoid `update`, `fix stuff`, `asdf`, `final`, `final2`. The commit history is part of how markers see who did what, so make it readable.

---

## One-time setup

### 1. Install git

- Windows: https://git-scm.com/download/win (Git Bash comes with it)
- Mac: run `git --version` in a terminal and it'll offer to install it
- Linux: `sudo apt install git` or whatever your distro uses

### 2. Tell git who you are

Use your real name, and the email that's on your GitHub account, so your commits get linked to you:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 3. Set up an SSH key for GitHub

The repo uses an SSH remote (`git@github.com:...`), so you need a key. Check if you already have one:

```bash
ls ~/.ssh
```

If you see `id_ed25519.pub` (or `id_rsa.pub`), skip to "add it to GitHub". Otherwise make one:

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

Press enter through the prompts (a passphrase is optional but a good idea). Then copy the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Go to GitHub → Settings → SSH and GPG keys → New SSH key, paste it in and save. Test it:

```bash
ssh -T git@github.com
```

You should see "Hi <username>! You've successfully authenticated". If it asks about trusting the host, type `yes`.

### 4. Get access to the repo

Ask Tushar to add you as a collaborator on `tjain-glitch/bloom` if you haven't been already. Accept the invite email.

### 5. Clone it

Go to wherever you keep your uni stuff and run:

```bash
git clone git@github.com:tjain-glitch/bloom.git
cd bloom
```

That's the setup done. You only do this once per machine.

---

## Day-to-day workflow

### Step 1: Get the latest `main`

Do this every time before starting something new:

```bash
git checkout main
git pull origin main
```

### Step 2: Make your branch

```bash
git checkout -b feat/abdlop-commitment
```

`-b` creates the branch and switches to it in one go. Check which branch you're on any time with:

```bash
git branch
```

The one with the `*` is your current branch.

### Step 3: Do the work, then commit

See what you've changed:

```bash
git status
git diff
```

Stage the files you want in this commit:

```bash
git add src/commitment.py tests/test_commitment.py
```

(`git add .` adds everything. That's fine, but check `git status` first so you don't commit junk like `.venv`, build output or big result files.)

Commit:

```bash
git commit -m "Add ABDLOP commit and open functions"
```

Repeat as you go. Lots of small commits is better than one giant one at the end.

### Step 4: Push your branch

The first time you push a new branch:

```bash
git push -u origin feat/abdlop-commitment
```

`-u` links your local branch to the remote one, so after that you can just run:

```bash
git push
```

Push at least at the end of every session you work, even if it's not finished. If your laptop dies the work is still on GitHub.

### Step 5: Open a pull request

1. Go to https://github.com/tjain-glitch/bloom
2. There'll usually be a yellow banner saying your branch had recent pushes, with a **Compare & pull request** button. Click it. (If not: **Pull requests** tab → **New pull request** → set base to `main` and compare to your branch.)
3. Title: a short description of what the PR does, e.g. "ABDLOP commitment scheme"
4. In the description, write:
   - what you did
   - how you tested it (commands you ran, what the output was)
   - anything you're unsure about, or anything you changed from the paper
   - `Closes #12` if it finishes an issue (GitHub will auto-close the issue on merge)
5. Add at least one teammate as a **Reviewer** (right-hand sidebar)
6. Click **Create pull request**

If it's not ready yet but you want early feedback, use the dropdown on the button to make it a **Draft pull request** instead.

### Step 6: Review

When you're the reviewer:

- Go to the **Files changed** tab and read through it
- Pull the branch and actually run it if it touches anything important:
  ```bash
  git fetch origin
  git checkout feat/abdlop-commitment
  ```
- Leave comments on specific lines by clicking the `+` next to them
- When you're done, click **Review changes** and choose **Comment**, **Approve** or **Request changes**

Reviewing isn't just a formality. Any of us can get asked about any part of the code in the Q&A, so reading each other's PRs is how we all end up understanding the whole thing.

If you're the author and you get comments, fix them on the same branch, commit, `git push`, and the PR updates automatically.

### Step 7: Merge

Once it's approved and there are no conflicts:

1. Click **Squash and merge** (keeps `main`'s history tidy, one commit per PR), or **Create a merge commit** if the individual commits are worth keeping
2. Click **Delete branch** on the button that appears after

Then locally:

```bash
git checkout main
git pull origin main
git branch -d feat/abdlop-commitment
```

And you're back to step 1 for the next task.

---

## Keeping your branch up to date

If `main` has moved on while you were working (someone else merged something), bring those changes into your branch:

```bash
git checkout main
git pull origin main
git checkout feat/your-branch
git merge main
```

Do this before opening a PR if your branch has been around for more than a day or two. It makes conflicts smaller and easier to deal with.

---

## Merge conflicts

They happen when two people change the same lines. Git will tell you which files are conflicted. Open them and you'll see something like:

```
<<<<<<< HEAD
your version
=======
the other version
>>>>>>> main
```

Edit the file so it has the right final version, and delete the `<<<<<<<`, `=======` and `>>>>>>>` lines. Then:

```bash
git add path/to/file
git commit
```

If you're not sure which version is right, ask whoever wrote the other half. Don't just pick yours.

To bail out of a merge and go back to how things were:

```bash
git merge --abort
```

---

## "Oh no" situations

**I committed to `main` by accident (haven't pushed yet)**

```bash
git branch feat/what-i-was-doing     # save the work on a new branch
git reset --hard origin/main         # put main back to how it was
git checkout feat/what-i-was-doing
```

**I want to undo my last commit but keep the changes**

```bash
git reset --soft HEAD~1
```

**I've got changes but need to switch branches**

```bash
git stash          # put changes aside
git checkout other-branch
# ... do whatever ...
git checkout original-branch
git stash pop      # bring them back
```

**I want to throw away changes to one file**

```bash
git restore path/to/file
```

**Push got rejected ("updates were rejected because the remote contains work...")**

Someone pushed to the same branch. Pull first, then push:

```bash
git pull
git push
```

**Never** run `git push --force` on `main`. On your own branch it's OK if you know why you need it, but give a heads up in the group chat if anyone else has pulled that branch.

---

## Rules

- No direct pushes to `main`. Everything goes through a PR.
- At least one approval before merging. Don't merge your own PR without anyone looking at it.
- Don't commit secrets, API keys, `.env` files, virtual environments, or big generated files. The spec specifically says not to include these.
- If you used AI to help write some code, mention it in the PR description. We need this for the provenance section of the README and report, and it's easier to note it at the time than to remember it in Week 14.
- If you copied or adapted code from anywhere, put the link in the PR and a comment in the code.

## Quick reference

```bash
git checkout main && git pull origin main      # get latest
git checkout -b type/short-description         # new branch
git status                                     # what's changed
git add <files>                                # stage
git commit -m "message"                        # commit
git push -u origin type/short-description      # first push
git push                                       # later pushes
git merge main                                 # update branch from main
git branch -d type/short-description           # delete after merge
```
