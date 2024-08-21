# Aurora Echo

Aurora Echo is a visual-audio feedback system with maximized security.

## Get Started

### Requirements

> Alternatively, you can run the setup script directly:
> 
> - Windows:
>  ```pwsh
>   .\setup.ps1
>  ```
> - macOS / Linux:
>  ```sh
>  . ./setup.sh
>  ```

#### Port Audio

Before install the dependencies in Python, you should check the installation of `portaudio` for installing PyAudio.

```shell
sudo apt update
sudo apt install portaudio19-dev
```

Or if you are using macOS, please run:

```shell
brew install portaudio
```

First, you need to install requirements:

```shell
pip install -r requirements.txt
```

Then you need to install the language library for `spaCy`.

```shell
python -m spacy download en_core_web_sm
```

### Devices

Then, you need to prepare GPUs, including NVIDIA GPUs and CUDA Toolkit, or using MPS by Apple.

#### NVIDIA GPUs

You need to use `nvidia-smi` to check the status of GPUs.

#### CUDA Toolkit

You need to install CUDA Toolkit to use NVIDIA GPUs.

#### MPS by Apple

If you are using Apple Silicon, feel free to use MPS device for acceleration except the LLMs.

### Configuration

You need to configure the system by editing `config.yaml`.

#### OpenAI Key

If you are using ChatGPT in Aurora Echo, you need to provide OpenAI key. Aurora Echo guarantees that your key will not be leaked.

For example, your key is `sk-proj-114514`, then you need to edit `config.yaml` as follows:

```yaml
openai:
  key: sk-proj-114514
```

If you are using other servers, e.g. Microsoft Azure, please specify the server in `config.yaml`:

```yaml
openai:
  base: https://models.inference.ai.azure.com
```

#### Llama Installation Path

We use `Llama` or `Qwen` as the local LLM.

You should download the `Llama` model from Hugging Face, and move the LLM to `./data/models`, and then specify the model.

```yaml
models:
  llama:
    path: ./data/models
    name: meta-llama/Meta-Llama-3.1-8B-Instruct
```

Sams as `Qwen`:

```yaml
models:
  qwen:
    path: ./data/models
    name: Qwen/Qwen2-1.5B-Instruct
```

#### Wav2Vec Installation Path

We use `Wav2Vec` as the local ASR.

You should download the `Wav2Vec` model from Hugging Face, and move the ASR to `./data/models`, and then specify the model.

```yaml
models:
  wav2vec:
    path: ./data/models/
    name: facebook/wav2vec2-base-960h
```

### Training Datasets

If you want to train the model, you are required to specify train datasets.

#### Facial Sentiment Analysis

You need to tell facial expressions apart with `angry`, `disgust`, `fear`, `happy`, `sad`, `surprise`, and `neutral`. If there's also unknown, you can use `others`.

We will use the `ImageFolder` to serialize the dataset.

Or you can use the pretrained file and move it to `./data/sentiment/model.pth`.

#### Sentiment Analysis

You can use `IMDB` dataset provided by Standford University, and using `PyTorch`, it will automatically download to `.data`.

Or you can use the pretrained file and move it to `./data/models/facial.pth`.

### Run the application

Before starting to run, you need to install `uvicorn` to run the server.

```shell
pip install uvicorn
```

Then you can run the server by:

```shell
uvicorn main:app --reload
```

Now, please open [https://aurora-echo.zzdev.org](https://aurora-echo.zzdev.org) to use Aurora Echo. If you don't have the chance to access the International Internet, please manually build the frontend by running:

```shell
cd client
# Suppose you have installed nodejs and pnpm
pnpm install
pnpm run build
```

Then you can use `http.server` module to serve the frontend.
