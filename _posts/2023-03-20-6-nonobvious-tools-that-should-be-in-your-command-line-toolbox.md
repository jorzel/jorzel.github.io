---
title: 6 nonobvious tools that should be in your command-line toolbox
description: "In this short post, I would like to present some tools that can be useful when working with command line terminals."
tags: linux programming learning command-line efficiency

---

## Introduction

In this short post, I would like to present some tools that can be useful when working with command line terminals.

I am using `zsh` shell (a shell is the name of the program that runs in the terminal) on MacOS, but most of the following suggestions should work on Linux and other shells.

## asciinema - recording your terminal

The first tool [asciinema](https://github.com/asciinema/asciinema) is a kind of meta-tool that can record our terminal session. It is extremely helpful for presentations and blog posts to make interactive examples by using `gif` files.

**Installation**

```bash
$ brew install pipx
$ pipx ensurepath
$ pipx install asciinema
```

**Usage**

To start a session we have to execute the following instruction.

```bash
$ asciinema record <filename>
asciinema: recording asciicast to <filename>
asciinema: press <ctrl-d> or type "exit" when you're done
```

Now, our terminal actions are recorded until we stop the program by hitting `exit` or `ctrl+d` . We can run the recording using `asciinema play <filename>` or convert our file into a `gif` format (e.g. using [online program](https://dstein64.github.io/gifcast/)).

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679305257776/8390a406-d488-4dd0-87db-0ee875b3c42d.gif)

## z plugin - move between folders quickly

[z plugin](https://github.com/agkozak/zsh-z) is a tool that enables us to move between our directories (that were visited frequently in the past) quickly without typing full absolute or relative paths.

**Installation**

I recommend installing this plugin using a manager like [oh-my-zsh](https://ohmyz.sh/#install). However, you can choose other options suggested in the [docs](https://github.com/agkozak/zsh-z#installation).

**Usage**

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679311065131/6fcb7cde-7c1c-4ad2-8c96-8792a6de1cc1.gif)

## bat - inline syntax highlighter

[bat](https://github.com/sharkdp/bat) is a program that supports inline syntax highlighting for many programming and markup languages.

**Installation**

```bash
$ brew install bat
```

**Usage**

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679312022359/31d7169c-1f22-4fe9-8eaa-b7fed03ee063.gif)

## ctr+r - history search

`ctr+r` is the keyboard shortcut that is built-in functionality in a terminal. It enables recursive search through your command usage history.

**Usage**

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679313302668/76ac15e0-f4dd-41e5-bb97-30575446879c.gif)

## ultimate plumber - explore textual data

[Ultimate plumber](https://github.com/akavel/up) is a tool that can interactively show us the results of text processing using Linux pipes. It gives us a playground with immediate feedback on our operations.

**Installation**

```bash
$ brew install up
```

**Usage**

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679314361495/30316220-d3ea-48fa-b7db-003559fc5090.gif)

## navi - cheatsheets

[navi](https://github.com/denisidoro/navi) is a popular tool that provides interactive [cheatsheets](https://github.com/denisidoro/cheats) for many programs like `git`, `docker`, `kubectl`, etc.

**Installation**

```bash
$ brew install navi
```

**Usage**

To start using navi, we should first import some cheatsheets (using `navi repo browse`) that would be interesting and helpful for us.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1679317665701/7d2274ee-0e01-4095-948d-035e0c024524.gif align="center")

## Conclusion

I have shown some useful features of `zsh` shell for your terminal. I hope it would be helpful. If you seek more, I recommend you to visit:

* https://github.com/dpokusa/linux-terminal-efficiency
    
* https://github.com/agarrharr/awesome-cli-apps