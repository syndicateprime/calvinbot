# Calvinbot - A ChatGPT Reformed Catechizer

Note: This is very WIP and subject to change. It's got some weird kinks to it too.

Calvinbot uses ChatGPT to generate html files with educational information according to the Westminster Shorter Catechism.
It is instructed to use sources including: The Bible, The Westminster Confession of Faith, and John Calvin's writing.

To see examples of it's output, see the `html` directory, the files that begin with `example_` are the ones provided. As you can see,
the output can be weird!

## Known issues
- Sometimes ChatGPT responds with plaintext before the HTML response. I've just deleted it from the examples, but it's there.
- The formatting output is very different between runs.

## How to use:

Assumptions:
- You have python installed

### Install openapi
Run `pip install openapi`

### Set your OPENAI_API_KEY
Ensure you have a valid openapi key. Export it like:
    `export OPENAI_API_KEY=sk-gobbldygook`

### Set how many questions to generate
The `html` directory has examples of output Calvinbot generates. To generate your own,
edit the parameters section of the `calvinbot.py` file.

The most important parameters are `start_q`, and `end_q`, which tells it which questions to
generate. Each question takes about ~30 seconds to generate, so don't choose a big value the first
few times. It's set to generate 1 - 5 the first time around.

### Generating HTML
From this directory

`python calvinbot.py`.

In addition to populating the `html` output with your files, after every question it will show you
how many GPT tokens it used.

