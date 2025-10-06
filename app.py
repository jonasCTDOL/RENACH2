# app.py

import streamlit as st
import pandas as pd
import io
import zipfile

# --- Configuração da Página ---
st.set_page_config(
    page_title="Divisor de CSV",
    page_icon="✂️",
    layout="centered"
)

# --- Título e Descrição ---
st.title("✂️ Divisor de Arquivos CSV")
st.write(
    "Faça o upload de um arquivo CSV e esta ferramenta o dividirá em múltiplos arquivos "
    "menores, com no máximo 500 linhas cada."
)

# --- Lógica de Upload ---
uploaded_file = st.file_uploader(
    "Escolha um arquivo CSV",
    type="csv",
    help="O arquivo será processado e dividido em partes menores."
)

if uploaded_file is not None:
    try:
        # Lê o arquivo CSV garantindo que todas as colunas sejam tratadas como texto (string)
        df = pd.read_csv(uploaded_file, dtype=str)

        if df.empty:
            st.warning("⚠️ O arquivo CSV está vazio. Por favor, carregue um arquivo com dados.")
        else:
            st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso! Ele contém **{len(df)}** linhas.")

            # --- Lógica de Divisão ---
            chunk_size = 500
            list_of_dfs = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

            # Prepara o nome base para os arquivos de saída
            original_filename = uploaded_file.name.replace('.csv', '')

            # --- Lógica para criar o ZIP em memória ---
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for i, chunk_df in enumerate(list_of_dfs):
                    # Cria o nome do arquivo individual
                    output_filename = f"{original_filename}_parte_{i + 1}.csv"
                    # Converte o dataframe para CSV em formato de string
                    csv_data = chunk_df.to_csv(index=False).encode('utf-8')
                    # Adiciona o arquivo CSV ao zip
                    zip_file.writestr(output_filename, csv_data)
            
            # Posiciona o buffer no início para a leitura
            zip_buffer.seek(0)

            # --- Botão de Download ---
            st.download_button(
                label=f"📥 Baixar Arquivos Divididos ({len(list_of_dfs)} partes) em .zip",
                data=zip_buffer,
                file_name=f'{original_filename}_dividido.zip',
                mime='application/zip',
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
