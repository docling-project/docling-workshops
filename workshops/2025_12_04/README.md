# IBM TechXchange Dev Day: Paris

## Event links

- Event registration: https://www.ibm.com/events/reg/flow/ibm/4phiuhmb/landing/page/landing

## Workshop labs

- [Lab 1: Document Conversion and Exploration](./docling_lab_1.ipynb)
- [Lab 2: Getting Started with RAG](./docling_lab_2.ipynb)
- [Lab 3: Advanced RAG with Multimodal Support and Visual Grounding](./docling_lab_3.ipynb)
- [Lab 4: Document Extraction](./docling_lab_4.ipynb)
- Lab 5: Agentic Applications. TBA

## Running the Docling Notebooks Locally

### Install Jupyter

> [!TIP]
> Before installing dependencies and to avoid conflicts in your environment, it is advisable to use a [virtual environment (venv)](https://docs.python.org/3/library/venv.html) We advise to use the [uv](https://docs.astral.sh/uv/) tool to manage virtual environments and dependencies. You can install it with
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
    uv pip install notebook ipywidgets ipykernel
    ```

    For more information, see the [Jupyter installation instructions](https://jupyter.org/install)

1. To open a notebook in Jupyter (in the active virtual environment), run:

    ```shell
    jupyter notebook <notebook-file-path>
    ```


## Running the Docling Notebooks Remotely (Colab)

The following steps will enable you to run all the steps on [Google Colab](https://colab.research.google.com), without installing any tool locally.

> [!TIP]
> The default execution runtime in Colab uses a CPU. Consider using a different Colab runtime to increase execution speed, especially in situations where you may have other constraints such as a slow network connection. From the navigation bar, select `Runtime->Change runtime type`, then select either GPU- or TPU-based hardware acceleration.

### Colab Prerequisites

- [Google Colab](https://colab.research.google.com) requires a Google account that you're logged into

### Serving the AI Models for Colab

Some steps of the lab require AI models to be served by an AI model runtime so that the models can be invoked or called.

## watsonx.ai credentials

The parts of the lab which leverage medium-size models will rely on credentials for watsonx.ai. Please rely on the information provided by the instructors for retrieving the credentials.

Once you have the credentials, make sure to set them in the `.env` file:

1. Copy the `env.example` to `.env`

    ```console
    cp env.example .env
    ```

2. Set the values in `.env`

