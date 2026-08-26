import random
import unicodedata
import streamlit as st
from classico import TermoooClassico
from dueto import TermoooDueto
from unidecode import unidecode

# =========================================================
# CONSTANTES E CORES OFICIAIS
# =========================================================

LINHAS = 6
COLUNAS = 5

CORES = {
    "verde": "#538d4e",
    "amarelo": "#b59f3b",
    "cinza_escuro": "#3a3a3c",
    "cinza_borda": "#d3d6da",
    "fundo": "#ffffff",
    "texto": "#1a1a1a",
}

# =========================================================
# ESTADO E INICIALIZAÇÃO DO JOGO
# =========================================================

def remover_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).upper()


def iniciar_estado():
    """Inicializa ou reseta o estado do jogo utilizando o backend."""
    modo = st.session_state.get("modo_jogo", "Clássico")
    
    st.session_state.modo_jogo = modo
    
    if modo == "Clássico":
        st.session_state.jogo_backend = TermoooClassico()
    else:
        st.session_state.jogo_backend = TermoooDueto()

    st.session_state.tentativas1 = []
    st.session_state.tentativas2 = []  
    
    st.session_state.linha_atual = 0
    st.session_state.posicao_foco = 0
    st.session_state.slots_atuais = [""] * COLUNAS
    
    st.session_state.jogo_terminado = False
    st.session_state.venceu = False
    st.session_state.mensagem = ""


def garantir_estado():
    if "modo_jogo" not in st.session_state:
        st.session_state.modo_jogo = "Clássico"
    if "jogo_backend" not in st.session_state:
        iniciar_estado()


# =========================================================
# LÓGICA DO JOGO E VALIDAÇÕES RIGOROSAS
# =========================================================

def processar_entrada_fisica():
    """Captura o texto digitado e valida rigorosamente para impedir palavras > 5 letras."""
    texto_raw = st.session_state.get("campo_fisico", "").upper().strip()
    if not texto_raw or st.session_state.jogo_terminado:
        return

    # TRAVA DE SEGURANÇA: Se a string digitada/colada for maior que 5 caracteres
    if len(texto_raw) > COLUNAS:
        st.session_state.mensagem = f"A palavra deve ter no máximo {COLUNAS} caracteres!"
        st.session_state.campo_fisico = ""
        return

    # Extrai apenas caracteres alfabéticos válidos
    letras = [c for c in texto_raw if c.isalpha()]

    # Validação de Tamanho Exato
    if len(letras) != COLUNAS:
        st.session_state.mensagem = f"A palavra deve ter exatamente {COLUNAS} letras!"
        st.session_state.campo_fisico = ""
        return

    palpite_bruto = "".join(letras)
    backend = st.session_state.jogo_backend

    # Validação de Caracteres (A-Z)
    if not backend.entrada_valida(palpite_bruto):
        st.session_state.mensagem = "Use apenas letras de A a Z, sem acentos ou caracteres especiais."
        st.session_state.campo_fisico = ""
        return

    # Validação no Repositório/Wordlist
    palavra_chave = unidecode(palpite_bruto)
    if palavra_chave not in backend.word_map:
        st.session_state.mensagem = "Palavra não encontrada na base de dados!"
        st.session_state.campo_fisico = ""
        return

    # SE PASSOU EM TODAS AS VALIDAÇÕES: Aplica no grid e avança a linha
    st.session_state.slots_atuais = letras
    palavra_com_acento = backend.word_map[palavra_chave]

    if st.session_state.modo_jogo == "Clássico":
        res1 = backend.avaliar_palavra_dados(palavra_com_acento)
        st.session_state.tentativas1.append(res1)

        if palavra_com_acento == backend.palavraSecreta:
            st.session_state.jogo_terminado = True
            st.session_state.venceu = True
        elif st.session_state.linha_atual + 1 >= LINHAS:
            st.session_state.jogo_terminado = True
            st.session_state.venceu = False
    else:
        # Modo Dueto
        p1, p2 = backend.palavrasSecretas

        if not getattr(st.session_state, "acertou1", False):
            res1 = backend.avaliar_palavra_dados(palavra_com_acento, p1)
            st.session_state.tentativas1.append(res1)
            if palavra_com_acento == p1:
                st.session_state.acertou1 = True
        else:
            st.session_state.tentativas1.append([{"letra": c, "estado": "green"} for c in backend.remover_acentos(p1)])

        if not getattr(st.session_state, "acertou2", False):
            res2 = backend.avaliar_palavra_dados(palavra_com_acento, p2)
            st.session_state.tentativas2.append(res2)
            if palavra_com_acento == p2:
                st.session_state.acertou2 = True
        else:
            st.session_state.tentativas2.append([{"letra": c, "estado": "green"} for c in backend.remover_acentos(p2)])

        v1 = getattr(st.session_state, "acertou1", False)
        v2 = getattr(st.session_state, "acertou2", False)

        if v1 and v2:
            st.session_state.jogo_terminado = True
            st.session_state.venceu = True
        elif st.session_state.linha_atual + 1 >= LINHAS:
            st.session_state.jogo_terminado = True
            st.session_state.venceu = False

    st.session_state.mensagem = ""
    st.session_state.linha_atual += 1
    st.session_state.slots_atuais = [""] * COLUNAS
    st.session_state.posicao_foco = 0
    st.session_state.campo_fisico = ""


def alterar_modo():
    st.session_state.modo_jogo = st.session_state.modo_selecionado
    st.session_state.acertou1 = False
    st.session_state.acertou2 = False
    iniciar_estado()


# =========================================================
# CSS CUSTOMIZADO
# =========================================================

def injetar_css():
    st.markdown(
        f"""
        <style>
            #MainMenu, header, footer {{ visibility: hidden; }}
            .stApp {{ background: {CORES["fundo"]}; }}

            * {{
                font-family: "Helvetica Neue", Arial, sans-serif;
                user-select: none;
                box-sizing: border-box;
            }}

            .block-container {{
                padding-top: 0.5rem !important;
                padding-bottom: 0.5rem !important;
                width: 100%;
                max-width: {"800px" if st.session_state.modo_jogo == "Dueto" else "340px"};
                margin: 0 auto;
            }}

            .termo-header {{
                text-align: center;
                font-size: 2rem;
                font-weight: 800;
                letter-spacing: 6px;
                color: {CORES["texto"]};
                margin-top: 0;
                margin-bottom: 8px;
                line-height: 1.2;
            }}

            .termo-board {{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                margin: 0 auto;
                padding: 0;
                margin-bottom: 16px;
            }}

            .termo-row-spacer {{
                width: 100%;
                height: 10px !important;
                min-height: 10px !important;
                max-height: 10px !important;
                margin: 0 !important;
                padding: 0 !important;
                display: block;
            }}

            .termo-linha {{
                width: 100%;
                display: flex;
                justify-content: center;
                margin: 0;
                padding: 0;
            }}

            /* Espaço vertical fixo entre linhas */
            .termo-row-spacer {{
                width: 100%;
                height: 10px !important;
                min-height: 10px !important;
                max-height: 10px !important;
                margin: 0 !important;
                padding: 0 !important;
            }}

            div[data-testid="column"] {{
                padding: 0 !important;
                margin: 0 !important;
                min-width: 0 !important;
                width: auto !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
            }}

            /* QUADRADOS DO TABULEIRO */
            .termo-tile {{
                width: 48px !important;
                height: 48px !important;
                min-width: 48px !important;
                max-width: 48px !important;
                min-height: 48px !important;
                max-height: 48px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 0 !important;
                margin: 0 !important;
                box-sizing: border-box !important;
                font-size: 1.4rem;
                font-weight: 700;
                text-transform: uppercase;
                border-radius: 4px;
                border: 2px solid {CORES["cinza_borda"]};
                background: {CORES["fundo"]};
                color: {CORES["texto"]};
                line-height: 1 !important;
                overflow: hidden;
            }}

            .termo-tile.focado {{
                border-color: {CORES["texto"]} !important;
                border-width: 3px !important;
            }}

            /* ESTADOS DE COR DAS TENTATIVAS */
            .termo-tile.green {{
                background: {CORES["verde"]} !important;
                border-color: {CORES["verde"]} !important;
                color: #ffffff !important;
            }}

            .termo-tile.yellow {{
                background: {CORES["amarelo"]} !important;
                border-color: {CORES["amarelo"]} !important;
                color: #ffffff !important;
            }}

            .termo-tile.gray {{
                background: {CORES["cinza_escuro"]} !important;
                border-color: {CORES["cinza_escuro"]} !important;
                color: #ffffff !important;
            }}

            div[data-testid="column"] button.tile-btn,
            div[data-testid="column"] button {{
                width: 48px !important;
                height: 48px !important;
                min-width: 48px !important;
                max-width: 48px !important;
                min-height: 48px !important;
                max-height: 48px !important;
                padding: 0 !important;
                margin: 0 !important;
                border-radius: 4px !important;
                font-size: 1.4rem !important;
                font-weight: 700 !important;
                line-height: 1 !important;
                box-sizing: border-box !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }}

            div[data-testid="stTextInput"] input {{
                text-transform: uppercase !important;
                text-align: center !important;
                font-weight: 700 !important;
                letter-spacing: 2px !important;
                height: 40px !important;
                border-radius: 6px !important;
            }}

            .termo-mensagem {{
                text-align: center;
                font-weight: 700;
                margin-top: 10px;
                margin-bottom: 10px;
                font-size: 0.95rem;
            }}

            .termo-mensagem.sucesso {{ color: {CORES["verde"]}; }}
            .termo-mensagem.erro {{ color: #b3261e; }}

            div[data-testid="stButton"] > button {{
                width: 100% !important;
                height: 40px !important;
                border-radius: 4px !important;
                border: none !important;
                background: {CORES["texto"]} !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                margin-top: 8px !important;
            }}

            /* Espaço entre os dois tabuleiros do Dueto */
            div[data-testid="stHorizontalBlock"]:has(.dueto-titulo) {{
               column-gap: 110px !important;
            }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# COMPONENTES VISUAIS
# =========================================================

def renderizar_tabuleiro(tentativas, tag="p1"):
    """Renderiza uma grade 6x5 com tamanho fixo."""

    # Largura total do tabuleiro:
    # 5 quadrados de 48px + 4 espaços de 3px
    largura_tabuleiro = (COLUNAS * 48) + ((COLUNAS - 1) * 3)

    # Container do tabuleiro
    st.markdown(
        f"""
        <div
            class="termo-board"
            style="
                width: {largura_tabuleiro}px;
                margin-left: auto;
                margin-right: auto;
            "
        >
        """,
        unsafe_allow_html=True,
    )

    for i in range(LINHAS):

        # Linha
        st.markdown(
            '<div class="termo-linha">',
            unsafe_allow_html=True
        )

        cols = st.columns(COLUNAS, gap="small")

        # =====================================================
        # LINHA JÁ PREENCHIDA
        # =====================================================

        if i < len(tentativas):

            for j in range(COLUNAS):

                item = tentativas[i][j]

                letra_char = item.get(
                    "letra",
                    item.get("char", "")
                )

                estado_cor = item.get(
                    "estado",
                    item.get("status", "")
                )

                # Converte estados antigos para os estados CSS
                if estado_cor == "correct":
                    estado_cor = "green"

                elif estado_cor == "present":
                    estado_cor = "yellow"

                elif estado_cor == "absent":
                    estado_cor = "gray"

                cols[j].markdown(
                    f"""
                    <div class="termo-tile {estado_cor}">
                        {letra_char}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # =====================================================
        # LINHA ATUAL
        # =====================================================

        elif (
            i == st.session_state.linha_atual
            and not st.session_state.jogo_terminado
        ):

            for j in range(COLUNAS):

                val = (
                    st.session_state.slots_atuais[j]
                    or " "
                )

                is_focado = (
                    j == st.session_state.posicao_foco
                )

                with cols[j]:

                    if st.button(
                        val,
                        key=f"slot_{tag}_{i}_{j}"
                    ):
                        st.session_state.posicao_foco = j
                        st.rerun()

                    st.markdown(
                        f"""
                        <script>
                        setTimeout(function() {{

                            const buttons =
                                window.parent.document
                                .querySelectorAll('button');

                            buttons.forEach(function(btn) {{

                                if (
                                    btn.innerText.trim()
                                    === "{val.strip()}"
                                ) {{

                                    btn.classList.add(
                                        "tile-btn"
                                    );

                                    {"btn.classList.add('focado');"
                                    if is_focado else ""}

                                }}

                            }});

                        }}, 50);
                        </script>
                        """,
                        unsafe_allow_html=True,
                    )

        # =====================================================
        # LINHA VAZIA
        # =====================================================

        else:

            for j in range(COLUNAS):

                cols[j].markdown(
                    '<div class="termo-tile"></div>',
                    unsafe_allow_html=True,
                )

        # Fecha linha
        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # Espaçamento entre linhas
        if i < LINHAS - 1:

            st.markdown(
                '<div class="termo-row-spacer"></div>',
                unsafe_allow_html=True
            )

    # Fecha o board
    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# INTERFACE PRINCIPAL
# =========================================================

def main():
    st.set_page_config(page_title="Termo Streamlit", page_icon="🟩", layout="centered")
    garantir_estado()
    injetar_css()

    st.markdown('<div class="termo-header">TERMO</div>', unsafe_allow_html=True)

    # Seletor de Modo
    st.selectbox(
        "Modo de Jogo:",
        ["Clássico", "Dueto"],
        index=0 if st.session_state.modo_jogo == "Clássico" else 1,
        key="modo_selecionado",
        on_change=alterar_modo,
        label_visibility="collapsed",
    )

    # Campo de Entrada (Trava física de max_chars=5)
    if not st.session_state.jogo_terminado:
        st.text_input(
            "Digite a palavra e pressione Enter:",
            key="campo_fisico",
            max_chars=5,
            on_change=processar_entrada_fisica,
            placeholder="Digite 5 letras e dê Enter...",
            label_visibility="collapsed",
        )

    # Renderização dos Tabuleiros
    if st.session_state.modo_jogo == "Clássico":
        renderizar_tabuleiro(st.session_state.tentativas1, tag="clas")
    else:
        col_esq, col_dir = st.columns(
            [1, 1],
            gap="large"
        )

        with col_esq:

            st.markdown(
                """
                <div class="dueto-titulo">
                    Palavra 1
                </div>
                """,
                unsafe_allow_html=True
            )

            renderizar_tabuleiro(
                st.session_state.tentativas1,
                tag="due1"
            )

        with col_dir:

            st.markdown(
                """
                <div class="dueto-titulo">
                    Palavra 2
                </div>
                """,
                unsafe_allow_html=True
            )

            renderizar_tabuleiro(
                st.session_state.tentativas2,
                tag="due2"
            )

    # Exibição de Erros e Mensagens
    if st.session_state.mensagem:
        st.markdown(f'<div class="termo-mensagem erro">{st.session_state.mensagem}</div>', unsafe_allow_html=True)
    elif st.session_state.jogo_terminado:
        backend = st.session_state.jogo_backend
        if st.session_state.venceu:
            st.markdown('<div class="termo-mensagem sucesso">🎉 Parabéns! Você venceu!</div>', unsafe_allow_html=True)
        else:
            if st.session_state.modo_jogo == "Clássico":
                revelacao = backend.palavraSecreta
            else:
                revelacao = f"{backend.palavrasSecretas[0]} e {backend.palavrasSecretas[1]}"
            st.markdown(f'<div class="termo-mensagem erro">Fim de jogo! As palavras eram: {revelacao}</div>', unsafe_allow_html=True)

    # Botão para Reiniciar
    if st.button("Nova Partida", key="btn_reiniciar"):
        iniciar_estado()
        st.rerun()


if __name__ == "__main__":
    main()  