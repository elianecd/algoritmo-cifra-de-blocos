# Importa a função responsável por ler, cifrar/decifrar e escrever o conteúdo do arquivo
import hashlib
from file_handler import processar_arquivo

def main():
    print("=== Cifra de Blocos - Projeto Inn Seguros ===")

    try:
        # Entrada da string usada para gerar a chave
        senha = input("Digite uma palavra-chave (ela será usada para gerar a chave criptográfica): ").strip()

        # Gera um hash SHA-256 da string e extrai os primeiros 4 bytes (32 bits)
        hash_sha256 = hashlib.sha256(senha.encode()).digest()
        chave = int.from_bytes(hash_sha256[:4], byteorder='big')
        print(f"Chave de 32 bits gerada automaticamente: {hex(chave)}")

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
