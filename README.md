## Cifra de Blocos - Projeto Inn Seguros

Este projeto implementa um algoritmo de criptografia e descriptografia de arquivos `.txt` utilizando uma cifra de blocos customizada, desenvolvida em Python puro, sem a necessidade de bibliotecas externas.

### Funcionalidades

*   Criptografia de arquivos `.txt` para arquivos `.enc`.
*   Descriptografia de arquivos `.enc` para arquivos `.txt`.
*   Utilização de uma chave hexadecimal de 32 bits fornecida pelo usuário.
*   Implementação de padding para blocos incompletos.

### Estrutura dos Arquivos

*   `main.py`: Ponto de entrada do programa. Responsável por:
    *   Receber as entradas do usuário (chave, modo, arquivos).
    *   Validar os dados de entrada.
    *   Chamar as funções de criptografia ou descriptografia.
*   `crypto_core.py`: Contém a lógica principal da cifra de blocos:
    *   Conversão da chave hexadecimal.
    *   Divisão do texto em blocos de 4 bytes.
    *   Implementação das operações de cifra e decifra (substituição e permutação).
    *   Implementação do algoritmo de padding (preenchimento com `0x00`).
*   `file_handler.py`: Responsável pela manipulação de arquivos:
    *   Leitura de arquivos `.txt` (modo texto).
    *   Escrita e leitura de arquivos `.enc` (modo binário).

### Fluxo de Funcionamento

1.  O usuário fornece uma chave hexadecimal de 32 bits (ex: `A1B2C3D4`, `DEADBEEF`, `0F0F0F0F`).
2.  O arquivo de texto é processado em blocos de 4 bytes. Se o bloco final for menor que 4 bytes, ele será preenchido com bytes `0x00`.
3.  O arquivo é criptografado, gerando um novo arquivo com a extensão `.enc`, ou descriptografado de volta para um arquivo `.txt`.

### Pré-requisitos

*   Python 3.12.6 ou superior instalado no sistema.
*   Um arquivo de entrada `.txt` com algum conteúdo (ex: `entrada.txt`).

### Exemplos de Chaves Válidas

*   `A1B2C3D4`
*   `DEADBEEF`
*   `12345678`
*   `0F0F0F0F`
*   `FFFFFFFF`
*   `00000001`

### Como Utilizar

1.  **Criptografar um arquivo:**

    ```bash
    python main.py
    ```

    *   O script solicitará a chave, o modo (`cifrar`), o nome do arquivo de entrada e o nome do arquivo de saída.
    *   Exemplo de preenchimento dos prompts:
        *   Chave hexadecimal: `DEADBEEF`
        *   Ação: `cifrar`
        *   Nome do arquivo de entrada: `entrada.txt`
        *   Nome do arquivo de saída: `saida.enc`
    *   Um arquivo chamado `saida.enc` será criado com o conteúdo criptografado.

2.  **Descriptografar um arquivo:**

    ```bash
    python main.py
    ```

    *   O script solicitará a chave, o modo (`decifrar`), o nome do arquivo de entrada (o arquivo `.enc`) e o nome do arquivo de saída. Use a mesma chave utilizada para a criptografia.
    *   Exemplo de preenchimento dos prompts:
        *   Chave hexadecimal: `DEADBEEF` (a mesma da etapa de cifragem)
        *   Ação: `decifrar`
        *   Nome do arquivo de entrada: `saida.enc`
        *   Nome do arquivo de saída: `resultado.txt`
    *   O arquivo `resultado.txt` será gerado com o conteúdo original.

3.  **Verificação (Opcional):**

    *   Compare o conteúdo de `resultado.txt` com o de `entrada.txt`. Eles devem ser idênticos.