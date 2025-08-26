# AI_dev

_Link to this workshop: <https://ibm.biz/aidev-docling>_


The Docling team is joining the [AI_dev](https://events.linuxfoundation.org/ai-dev-europe/) conference with two sessions as well as lots of networking opportunities at the LFAI booth.

- 💬 [Docling: Get Your Documents Ready for Gen AI](https://aideveu2025.sched.com/event/25Tts/docling-get-your-documents-ready-for-gen-ai-michele-dolfi-peter-staar-ibm-research?iframe=no&w=100%25&sidebar=yes&bg=no)
- 🛠️ [Technical Workshop: Meet Docling: The “Pandas” for Document AI](https://aideveu2025.sched.com/event/279gj/technical-workshop-meet-docling-the-pandas-for-document-ai-peter-staar-cesar-berrospi-ibm-research?iframe=no&w=100%25&sidebar=yes&bg=no)


## Lab codes

### Lab 1: Transform Your Documents into AI-Ready Data with Docling

Code in [./LabCode/Docling_Lab1_code.ipynb](./LabCode/Docling_Lab1_code.ipynb).

Topics:

- Install Docling and convert documents
- Navigate the output DoclingDocument (tables, pictures, etc.)
- Enrich document components

[![View on GitHub](https://badgen.net/badge/icon/github?icon=github&label=View%20on "View on GitHub")](https://github.com/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab1_code.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab1_code.ipynb)


### Lab 2: Enhanced Chunking and Vectorization with Docling

Code in [./LabCode/Docling_Lab2_code.ipynb](./LabCode/Docling_Lab2_code.ipynb).

Topics:

- Chunk a document by page
- Use the HierarchicalChunker
- Use the HybridChunker
- Compare the chunker techniques by reviewing the chunks statistics

[![View on GitHub](https://badgen.net/badge/icon/github?icon=github&label=View%20on "View on GitHub")](https://github.com/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab2_code.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab2_code.ipynb)


### Lab 3: Building an AI-powered multimodal RAG system with Docling

Code in [./LabCode/Docling_Lab3_code.ipynb](./LabCode/Docling_Lab3_code.ipynb).

Topics:

- Build a RAG pipeline with Docling and LangChain
- Enhance and customize the content serialization
- Turn the RAG pipeline into multi-modal with image annotations
- Use visual grounding to highlight the provenance of the information on the original document

[![View on GitHub](https://badgen.net/badge/icon/github?icon=github&label=View%20on "View on GitHub")](https://github.com/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab3_code.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/docling-workshops/blob/main/workshops/2025_08_29/LabCode/Docling_Lab3_code.ipynb)


### Lab 4: Run Docling as MCP tool

TODO

Topics:

- Use the Docling MCP tools
- Experiment with Agentic RAG


## Running the Docling Notebooks Locally

### Install Jupyter

> [!TIP]
> Before installing dependencies and to avoid conflicts in your environment, it is advisable to use a [virtual environment (venv)](https://docs.python.org/3/library/venv.html) We advise to use the [uv]() tool to manage virtual environments and dependencies. You can install it with
>
>   ```shell
>   curl -LsSf https://astral.sh/uv/install.sh | sh
>   ```
>
>   More [install guides](https://docs.astral.sh/uv/getting-started/installation/).

1. Create virtual environment:

    ```shell
    uv venv
    ```

1. Activate the virtual environment by running:

    ```shell
    source .venv/bin/activate
    ```

1. Install Jupyter notebook in the virtual environment:

    ```shell
    uv pip install notebook ipywidgets
    ```

    For more information, see the [Jupyter installation instructions](https://jupyter.org/install)

1. To open a notebook in Jupyter (in the active virtual environment), run:

    ```shell
    jupyter notebook <notebook-file-path>
    ```

### Replicate AI Cloud Platform

[Replicate](https://replicate.com/) is a cloud platform that will host and serve AI models for you.

1. Create a [Replicate](https://replicate.com/) account. You will need a [GitHub](https://github.com/) account to do this.

1. Add credit to your Replicate Account (optional). To remove a barrier to entry to try the models on the Replicate platform, use [this link](https://replicate.com/invites/a8717bfe-2f3d-4a52-88ed-1356231cdf03) to add a small amount of credit to your Replicate account.

1. Create a Replicate [API Token](https://replicate.com/account/api-tokens).

1. Set your Replicate API Token as an environment variable in your terminal where you will run the notebook:

    ```shell
    export REPLICATE_API_TOKEN=<your_replicate_api_token>
    ```


## Running the Docling Notebooks Remotely (Colab)

The following steps will enable you to run all the steps on [Google Colab](https://colab.research.google.com), without installing any tool locally.

> [!TIP]
> The default execution runtime in Colab uses a CPU. Consider using a different Colab runtime to increase execution speed, especially in situations where you may have other constraints such as a slow network connection. From the navigation bar, select `Runtime->Change runtime type`, then select either GPU- or TPU-based hardware acceleration.

### Colab Prerequisites

- [Google Colab](https://colab.research.google.com) requires a Google account that you're logged into

### Serving the AI Models for Colab

Some steps of the lab require AI models to be served by an AI model runtime so that the models can be invoked or called.

#### Replicate AI Cloud Platform for Colab

[Replicate](https://replicate.com/) is a cloud platform that will host and serve AI models for you.

1. Create a [Replicate](https://replicate.com/) account. You will need a [GitHub](https://github.com/) account to do this.

1. Add credit to your Replicate Account (optional). To remove a barrier to entry to try the Granite models on the Replicate platform, use [this link](https://replicate.com/invites/a8717bfe-2f3d-4a52-88ed-1356231cdf03) to add a small amount of credit to your Replicate account.

1. Create a Replicate [API Token](https://replicate.com/account/api-tokens).

1. Add your Replicate API Token to the Colab Secrets manager to securely store it. Open [Google Colab](https://colab.research.google.com) and click on the 🔑 Secrets tab in the left panel. Click "New Secret" and enter `REPLICATE_API_TOKEN` as the key, and paste your token into the value field. Toggle the button on the left to allow notebook access to the secret.
