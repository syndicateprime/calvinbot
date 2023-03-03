# Calvinbot - A ChatGPT Reformed Catechizer

Note: This is very WIP and subject to change. It's got some weird kinks to it too.

Calvinbot uses ChatGPT to generate html files with educational information according to the Westminster Shorter Catechism.
It is instructed to use sources including: The Bible, The Westminster Confession of Faith, and John Calvin's writing. However, 
ChatGPT has a degree of randomness, so while the sources are similar, the outputs of the program can be very different in style!

## Examples
To see examples of it's output, see the `html` directory, the files that begin with `example_` are the ones provided. 

Here are quick links to the outputs.
1. [What is the chief end of man?](html/example_WSC_Q_1_v0.html)
1. [What rule hath God given to direct us how we may glorify and enjoy Him? ](html/example_WSC_Q_2_v0.html)
1. [What do the Scriptures principally teach?](html/example_WSC_Q_3_v0.html)
1. [What is God](html/example_WSC_Q_4_v0.html)
1. [Are there more Gods than one?](html/example_WSC_Q_5_v0.html)
1. [How many persons are there in the Godhead?](html/example_WSC_Q_6_v0.html)
1. [What are the decrees of God? ](html/example_WSC_Q_7_v0.html)
1. [How doth God execute His decrees? ](html/example_WSC_Q_8_v0.html)
1. [What is the work of creation?](html/example_WSC_Q_9_v0.html)
1. [How did God create man?](html/example_WSC_Q_10_v0.html)

## Known issues
- Calvinbot will sometimes pick the wrong question to respond to
- Sometimes Calvinbot responds with plaintext before the HTML response.
- The formatting output is very different between runs.


## How to use:

Assumptions:
- You have python installed into your terminal
- You have a secret key for openapi

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
