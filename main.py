# Importa a função responsável por ler, cifrar/decifrar e escrever o conteúdo do arquivo
from file_handler import processar_arquivo

def main():
    print("=== Cifra de Blocos - Projeto Inn Seguros ===")

    try:
        # Solicita ao usuário que informe uma chave de 32 bits no formato hexadecimal (ex: A1B2C3D4)
        chave_input = input("Informe a chave (em hexadecimal, ex: A1B2C3D4): ").strip()
        
        # Converte a chave hexadecimal em um número inteiro
        chave = int(chave_input, 16)

        # Verifica se a chave está no intervalo válido de 32 bits (0 até 2^32 - 1)
        if not (0 <= chave <= 0xFFFFFFFF):
            raise ValueError("A chave deve ter exatamente 32 bits.")

        # Solicita ao usuário o modo de operação: 'cifrar' ou 'decifrar'
        modo = input("Digite 'cifrar' para encriptar ou 'decifrar' para decriptar: ").strip().lower()
        
        # Valida o modo de operação
        if modo not in ['cifrar', 'decifrar']:
            raise ValueError("Modo inválido. Use apenas 'cifrar' ou 'decifrar'.")

        # Solicita o nome do arquivo de entrada (de onde os dados serão lidos)
        nome_entrada = input("Nome do arquivo de entrada (ex: entrada.txt): ").strip()

        # Solicita o nome do arquivo de saída (onde o resultado será salvo)
        nome_saida = input("Nome do arquivo de saída (ex: saida.enc): ").strip()

        # Chama a função principal de processamento, passando os parâmetros
        processar_arquivo(nome_entrada, nome_saida, chave, modo)

        # Mensagem de sucesso ao final do processo
        print(f"Arquivo '{nome_saida}' gerado com sucesso.")

    except Exception as e:
        # Captura qualquer erro ocorrido durante o processo e exibe uma mensagem amigável
        print(f"Erro: {e}")

# Ponto de entrada do script: se o arquivo for executado diretamente, a função main() é chamada
if __name__ == "__main__":
    main()
