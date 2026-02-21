# 📖 Manual do Operador: Reabastecimento e Controle de Estoque (Fibrag Vending)

Este manual descreve os passos para acessar o painel administrativo da máquina diretamente pela tela OLED usando o **Controle Remoto Infravermelho (IR)**. 

Através deste painel, o operador pode verificar quantos itens restam e atualizar o sistema após colocar novos produtos físicos na máquina.

## 🎛️ Guia de Botões do Controle Remoto

Antes de começar, familiarize-se com os botões que serão utilizados no controle:
* **`POWER` (Botão Vermelho):** Entrar no modo Admin / Sair para a tela inicial.
* **`0` a `9`:** Digitar senhas, IDs de produtos e quantidades.
* **`PLAY / PAUSE` (⏯️ ou `#`):** Botão de **CONFIRMAR / ENTER**.
* **`VOLTAR` (⏪ ou `*`):** Cancelar ação ou voltar ao menu anterior.
* **`AVANÇAR` (⏭️ ou `>`) e `ANTERIOR` (⏮️ ou `<`):** Navegar entre os produtos.

---

## 🔐 Passo 1: Acessar o Painel Administrativo (Login)

1. Com a máquina na tela de descanso (mostrando "Faz tua compra..." ou o QR Code), aponte o controle remoto para o sensor e pressione o botão **`POWER`**.
2. A tela OLED exibirá: `ADMIN LOGIN - Ingrese Pass:`.
3. Digite a senha padrão de 4 dígitos: **`1` `2` `3` `4`**.
4. Pressione o botão **`PLAY`** para confirmar. 
   * *Nota: Se a senha estiver correta, a tela mudará para o MENU ADMIN. Se errar, a máquina emitirá um bipe longo de erro e limpará a tela para você tentar novamente.*

---

## 📦 Passo 2: Como Verificar o Estoque Atual

Antes de abrir a máquina, você pode ver o que está faltando:

1. No `MENU ADMIN`, pressione o botão **`1`** (Ver Estoque).
2. A tela mostrará o nome do Produto 1 (ex: *batata*) e a quantidade atual (`Q: 8`).
3. Use os botões **`AVANÇAR (>)`** ou **`ANTERIOR (<)`** para folhear todos os 16 produtos e anotar o que precisa ser reposto.
4. Quando terminar, pressione o botão **`VOLTAR (*)`** para retornar ao menu principal.

---

## 🔄 Passo 3: Como Registrar o Reabastecimento (Reset de Dados)

Após colocar os produtos físicos nas molas/compartimentos da máquina, você precisa informar ao sistema a nova quantidade:

1. No `MENU ADMIN`, pressione o botão **`2`** (Edit Estoque).
2. A tela exibirá `ID Prod (1-16):`. Digite o **número do compartimento** que você acabou de reabastecer (ex: digite `4` para Biscoito).
3. Pressione **`PLAY`** para confirmar o produto.
4. A tela agora exibirá o nome do produto selecionado e pedirá a `Nova Quantidade:`.
5. Digite a **quantidade total** que ficou na máquina (ex: se o compartimento cabe 10 unidades e você encheu, digite `10`).
6. Pressione **`PLAY`** para salvar.
7. A máquina emitirá um **bipe de confirmação** e voltará para a tela de seleção de ID, permitindo que você digite o número do próximo produto que deseja atualizar.
8. Se digitou um ID errado sem querer, basta apertar **`VOLTAR (*)`** para cancelar.

---

## 🚪 Passo 4: Sair e Voltar à Operação Normal

É extremamente importante fechar o painel administrativo após o reabastecimento para que a máquina volte a aceitar compras.

* **A qualquer momento**, não importa em qual tela do menu você esteja, basta pressionar o botão **`POWER`**.
* A tela voltará instantaneamente para a mensagem rotativa da Fibrag e os sensores voltarão a ler o ambiente de forma automática.

---

### ⚠️ Dicas de Resolução de Problemas
* **O controle não responde:** Verifique se você está apontando diretamente para o pino do sensor IR na frente da máquina e se não há luz solar direta ofuscando o receptor.
* **Produto mostra "FORA DE ESTOQUE":** Se a máquina apitar 3 vezes e recusar uma compra, significa que o estoque no sistema chegou a zero. O operador deve ir presencialmente, abastecer o compartimento e realizar o **Passo 3** deste manual.
