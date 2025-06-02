from crypto_core import cifrar_bloco, decifrar_bloco

def processar_arquivo(nome_entrada, nome_saida, chave, modo):
    # Abre o arquivo de entrada em modo binário para leitura (rb)
    # e o arquivo de saída em modo binário para escrita (wb)
    with open(nome_entrada, 'rb') as entrada, open(nome_saida, 'wb') as saida:
        # Lê o arquivo de entrada em blocos de 4 bytes (32 bits)
        while True:
            bloco_bytes = entrada.read(4)  # lê 4 bytes = 32 bits
             # Encerra o loop quando o final do arquivo for alcançado
            if not bloco_bytes:
                break

            # Caso o último bloco tenha menos de 4 bytes, aplica padding com zeros (0x00) para o último bloco
            # Isso garante que todos os blocos tenham exatamente 32 bits (4 bytes)
            if len(bloco_bytes) < 4:
                bloco_bytes += b'\x00' * (4 - len(bloco_bytes))

            # Converte os 4 bytes lidos em um inteiro de 32 bits no formato big-endian
            bloco = int.from_bytes(bloco_bytes, byteorder='big')

            # CIFRAGEM: Aplica a função de cifragem e grava o bloco cifrado no arquivo de saída
            if modo == 'cifrar':
                bloco_cifrado = cifrar_bloco(bloco, chave)
                saida.write(bloco_cifrado.to_bytes(4, byteorder='big'))
            # DECIFRAGEM: Aplica a função de decifragem e grava o bloco decifrado no arquivo de saída
            elif modo == 'decifrar':
                bloco_decifrado = decifrar_bloco(bloco, chave)
                saida.write(bloco_decifrado.to_bytes(4, byteorder='big'))
            # Em caso de modo inválido, interrompe com erro
            else:
                raise ValueError("Modo inválido. Use 'cifrar' ou 'decifrar'.")
