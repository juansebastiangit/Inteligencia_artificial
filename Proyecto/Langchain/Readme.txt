Para el uso de esta aplicación s necesario tener descargado algún modelo LLM que sirva como agente, en mi caso, las  pruebas se hicieron de forma
local usando Llama 3.1 8B, es decir el modelo 3.1 de meta con 8 billones de parametros.

Para acceder a este modelo es necesario descargar la aplicación ollama, y ejecutar en el terminal el comando ollama  pull <model-name>
de esta forma se descargará de forma local el modelo que se desea, en este caso Llama 3.1 8B, y se puede correr de forma local.

Ollama se integra con la api de langchain para utilizar al modelo como agente al momento de ejecutar el RAG
