Para el uso de esta aplicación s necesario tener descargado algún modelo LLM que sirva como agente, en mi caso, las  pruebas se hicieron de forma
local usando Llama 3.1 8B, es decir el modelo 3.1 de meta con 8 billones de parametros.

Para acceder a este modelo es necesario descargar la aplicación ollama, y dentro del cuaderno esta una celda que ejecuta ! ollama pull llama3.1:8b
esto descarga el modelo para su posterior usoen caso de que no este descargado

tambien se hicieron pruebas con deepseek v2 de 16 billones de parametros

Es necesario descargar las muestras en cod_json_data para ejecutar las pruebas

Ollama se integra con la api de langchain para utilizar al modelo como agente al momento de ejecutar el RAG
