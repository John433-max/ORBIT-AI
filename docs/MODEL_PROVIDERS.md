# Model providers

| Provider | Env | Notes |
|----------|-----|--------|
| `echo` | `ORBIT_MODEL_PROVIDER=echo` | Tests / offline |
| `tinylm` | `ORBIT_MODEL_PROVIDER=tinylm` | Educational weights |
| `ollama` | `ORBIT_MODEL_PROVIDER=ollama` | Local Ollama HTTP |
| `openai` | `ORBIT_MODEL_PROVIDER=openai` | OpenAI-compatible |
| `gguf` | `ORBIT_MODEL_PROVIDER=gguf` + path | llama-cpp-python |
| `auto` | default | Ollama → TinyLM → echo |

```bash
ORBIT_MODEL_PROVIDER=gguf ORBIT_MODEL_NAME=/path/model.gguf ORBIT_GGUF_N_GPU_LAYERS=0 python run_orbit.py chat "hello"
ORBIT_CHAT_PROVIDER=1 ORBIT_MODEL_PROVIDER=echo python run_orbit.py chat "hi"
```
