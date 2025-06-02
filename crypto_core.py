# Define a lista de símbolos exportados ao usar 'from crypto_core import *'
# Isso controla explicitamente quais funções/métodos estarão disponíveis externamente
__all__ = [
    "gerar_subchaves",
    "substituicao",
    "substituicao_inversa",
    "permutacao",
    "cifrar_bloco",
    "decifrar_bloco"
]

# S-box (Substitution box): usada para aplicar confusão, ou seja, substituir padrões previsíveis
# Cada entrada de 4 bits (nibble) é mapeada para outra entrada, baseada nessa tabela fixa.
# Esse processo é inspirado em criptografias reais como o AES.
sbox = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]

# S-box inversa: realiza o processo reverso da substituição, necessária na decifragem
# Para cada valor de 0 a 15, encontra qual índice da sbox o gera
sbox_inv = [sbox.index(i) for i in range(16)]

def gerar_subchaves(chave_32_bits):
    # A partir de uma chave de 32 bits, gera 3 subchaves para as 3 rodadas da cifra.
    # Cada subchave é obtida por uma rotação circular da chave original, garantindo variação.

    assert 0 <= chave_32_bits <= 0xFFFFFFFF, "A chave deve ter exatamente 32 bits"
    subchaves = []
    for i in range(3):
        # Rotação à esquerda de i * 5 bits, com máscara para manter 32 bits
        sub = ((chave_32_bits << (i * 5)) | (chave_32_bits >> (32 - i * 5))) & 0xFFFFFFFF
        subchaves.append(sub)
    return subchaves

def substituicao(bloco, subchave):
    # Aplica substituição bit a bit (nibble a nibble), misturando dados do bloco com a subchave.
    # Isso cria confusão, que é um dos pilares de segurança em cifragem simétrica.

    assert 0 <= bloco <= 0xFFFFFFFF, "O bloco deve ter exatamente 32 bits"
    resultado = 0
    for i in range(8): # 8 nibbles = 32 bits
        nibble = (bloco >> (i * 4)) & 0xF # Extrai o i-ésimo nibble do bloco
        chave_nibble = (subchave >> (i * 4)) & 0xF # Extrai o i-ésimo nibble da subchave
        substituido = sbox[nibble ^ chave_nibble] # Aplica XOR e usa o valor na S-box
        resultado |= (substituido << (i * 4)) # Junta no resultado, deslocando ao lugar correto
    return resultado

def substituicao_inversa(bloco, subchave):
    # Desfaz a substituição anterior, aplicando a S-box inversa.
    # Isso permite recuperar os dados originais durante a decifragem.

    resultado = 0
    for i in range(8):
        # Cada bloco de 32 bits é composto por 8 nibbles (4 bits cada).
        # Este laço processa um nibble por vez, da posição 0 à 7.

        nibble = (bloco >> (i * 4)) & 0xF
        # Desloca o bloco para a direita para alinhar o nibble desejado com os 4 bits menos significativos.
        # Em seguida, aplica uma máscara (0xF = 00001111) para extrair apenas os 4 bits do nibble.
        # Exemplo: se i = 0, extrai o nibble menos significativo. Se i = 7, o mais significativo.

        chave_nibble = (subchave >> (i * 4)) & 0xF
        # Extrai o nibble correspondente da subchave.
        # A subchave também é tratada como um bloco de 32 bits, dividido em 8 nibbles de 4 bits.

        original = sbox_inv[nibble] ^ chave_nibble # Inverte a S-box e o XOR
        # Aplica a S-box inversa no nibble cifrado para reverter a substituição feita durante a cifra.
        # Em seguida, desfaz o XOR com o nibble da subchave para obter o valor original antes da cifragem.

        resultado |= (original << (i * 4))
        # Posiciona o nibble recuperado na posição correta dentro do bloco de 32 bits,
        # usando deslocamento à esquerda (para restaurar a posição original),
        # e adiciona ao resultado usando OR bit a bit.
    return resultado

def permutacao(bloco, subchave, inverso=False):
    #A plica rotação circular nos bits do bloco, com quantidade baseada na subchave.
    # Isso promove difusão, espalhando pequenos padrões por todo o bloco.

    assert 0 <= bloco <= 0xFFFFFFFF, "O bloco deve ter exatamente 32 bits"
    rot = subchave & 0x1F # Usa apenas os 5 bits menos significativos da subchave (0 a 31)

    if inverso:
        # Rotação para a direita (desfaz a rotação feita na cifra)
        return ((bloco >> rot) | (bloco << (32 - rot))) & 0xFFFFFFFF
    else:
        # Rotação para a esquerda (usada na cifra), espalha bits para dificultar análise
        return ((bloco << rot) | (bloco >> (32 - rot))) & 0xFFFFFFFF

def cifrar_bloco(bloco, chave):
    # Aplica 3 rodadas de cifragem sobre um bloco de 32 bits:
    # 1. Gera subchaves
    # 2. Para cada rodada: aplica substituição + permutação

    # Gera 3 subchaves de 32 bits a partir da chave principal, para usar uma diferente em cada rodada
    subchaves = gerar_subchaves(chave)
    for i in range(3):
        bloco = substituicao(bloco, subchaves[i]) # Aplica substituição com a subchave atual (confusão)
        bloco = permutacao(bloco, subchaves[i]) # Aplica permutação com a subchave atual (difusão)
    return bloco # Retorna o bloco cifrado final após as 3 rodadas

def decifrar_bloco(bloco, chave):
    # Desfaz as 3 rodadas aplicadas na cifra:
    # 1. Gera as mesmas subchaves
    # 2. Aplica as operações inversas em ordem reversa: permutação inversa + substituição inversa

    # Gera as mesmas subchaves que foram usadas na cifra
    subchaves = gerar_subchaves(chave)
    # Aplica as 3 rodadas em ordem reversa (última até a primeira)
    for i in reversed(range(3)):
        bloco = permutacao(bloco, subchaves[i], inverso=True) # Primeiro desfaz a permutação aplicada anteriormente (rotação para a direita)
        bloco = substituicao_inversa(bloco, subchaves[i]) # Depois desfaz a substituição (aplicando a S-box inversa)
    return bloco # Retorna o bloco original restaurado