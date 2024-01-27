import streamlit as st
import platform

# Obtém a versão do Python
python_version = platform.python_version()

# Exibe a versão do Python no console do Streamlit
st.write("Versão do Python:", python_version)

import subprocess

# Executa o comando pip list para listar todas as bibliotecas instaladas
output = subprocess.check_output(["pip", "list"]).decode("utf-8")

# Exibe a lista de bibliotecas no console do Streamlit
st.write("Bibliotecas instaladas:")
st.code(output)