import pandas as pd
from google.colab import files
import io

# 1. Solicita o upload do arquivo na tela
uploaded = files.upload()

if uploaded:
    # Assuming only one file is uploaded, get the filename and content
    filename = list(uploaded.keys())[0]
    file_content = uploaded[filename]

    # Use io.StringIO to wrap the byte string
    csv_file = io.StringIO(file_content.decode('utf-8'))

    # 2. Lê o documento e divide em novos arquivos em csv com até 500 registros
    # Lê o CSV para um pandas DataFrame, tratando todas as colunas como strings
    df = pd.read_csv(csv_file, dtype=str)

    if not df.empty:
        row_count = df.shape[0]
        chunk_size = 500
        num_chunks = (row_count + chunk_size - 1) // chunk_size
        dfs = []
        for i in range(num_chunks):
            start_row = i * chunk_size
            end_row = min((i + 1) * chunk_size, row_count)
            dfs.append(df.iloc[start_row:end_row])

        # 3. Salva e baixa os novos arquivos divididos com o mesmo cabeçalho
        print("Gerando e baixando arquivos divididos:")
        for i, smaller_df in enumerate(dfs):
            output_filename = f"output_part_{i + 1}.csv"
            smaller_df.to_csv(output_filename, index=False)
            print(f"Arquivo '{output_filename}' gerado.")
            # Baixar o arquivo automaticamente
            files.download(output_filename)

    else:
        print("O arquivo CSV está vazio.")

else:
    print("Nenhum arquivo foi carregado.")
