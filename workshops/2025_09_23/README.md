# Swiss Dev Confederation 2025

The Docling team is joining the [Swiss Dev Confederation 2025](https://www.redhat.com/en/events/devconf-zurich) event with a joint session with Red Hat presenting the Llama Stack project.


- Docling Your Docs: Level Up Llama Stack Workflows, 14:00 - 14:30.


## Lab code and demo

Launch Llama Stack:

```sh
export LLAMA_STACK_PORT=8321
podman run \
        -it \
        --pull always \
        -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
        -v ~/.llama:/root/.llama \
        llamastack/distribution-starter:0.2.22 \
        --port $LLAMA_STACK_PORT \
        --env MILVUS_URL=http://localhost:19530 \
        --env VLLM_URL=http://host.containers.internal:1234/v1
```
