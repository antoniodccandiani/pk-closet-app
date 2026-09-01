"""
PK Closet — Social Media App v0.4
Bom Dia + Funcionamento + Produto (estrutura)
Legendas humanizadas + 5 hashtags + copy fácil
"""

import streamlit as st
from datetime import date
from pathlib import Path
import sys
import random

sys.path.insert(0, str(Path(__file__).parent))
from composer import create_bom_dia, create_funcionamento, gerar_legenda_produto, create_produto

st.set_page_config(
    page_title="PK Closet | Social Media",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { max-width: 820px; margin: 0 auto; }
    h1, h2, h3 { color: #3C2D28; }
    .stButton>button {
        background-color: #C49595;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.65rem 1.4rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover { background-color: #B08080; color: white; }
    .legenda-box {
        background: #F9F1EE;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #E8D5CF;
        font-size: 15px;
        line-height: 1.5;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# Estado
for key, default in [
    ("fluxo", None), ("bom_dia_step", 0), ("func_step", 0),
    ("func_data", {}), ("arte_path", None), ("prod_step", 0), ("prod_data", {})
]:
    if key not in st.session_state:
        st.session_state[key] = default

with st.sidebar:
    logo_path = Path("assets/logo_oficial.png")
    if logo_path.exists():
        st.image(str(logo_path), width=110)
    st.markdown("### PK Closet")
    st.caption("Social Media App")
    st.divider()
    if st.button("🏠 Início", use_container_width=True):
        for k in ["fluxo", "bom_dia_step", "func_step", "arte_path", "prod_step"]:
            st.session_state[k] = None if k == "fluxo" else (0 if "step" in k else None)
        st.session_state.func_data = {}
        st.session_state.prod_data = {}
        st.rerun()
    st.caption("v0.4")

def gerar_frase_emocional():
    inicios = [
        "A gente sabe como é difícil se sentir bem alguns dias.",
        "Tem dias que a gente só precisa de um carinho e de se sentir especial.",
        "Você não precisa estar perfeita para se sentir especial.",
        "Que hoje você se olhe com mais carinho.",
        "A beleza real não pede permissão.",
        "Se permitir ser quem você é já é um ato de coragem.",
        "Hoje o mundo pode esperar. Cuide de você primeiro.",
        "Você merece se sentir leve e bonita do seu jeito.",
    ]
    meios = [
        "Que este dia te lembre do quanto você é capaz de brilhar.",
        "A PK Closet acredita na sua beleza real — inclusive a sua.",
        "Estamos aqui para te acompanhar nesse sentimento.",
        "A gente existe para te ajudar a se sentir especial.",
        "Que a delicadeza de hoje te acompanhe em cada passo.",
        "Permita-se ocupar espaço com a sua autenticidade.",
        "Sua presença já é suficiente.",
        "Aqui você é bem-vinda do jeito que está.",
    ]
    return f"{random.choice(inicios)} {random.choice(meios)}"

def mostrar_download_e_legenda(path, legenda=None, is_story=True):
    st.image(str(path), use_container_width=True)

    with open(path, "rb") as f:
        st.download_button(
            "⬇️ Baixar PNG (salvar nas Fotos do celular)",
            data=f,
            file_name=path.name,
            mime="image/png",
            use_container_width=True,
        )

    st.markdown("**Como salvar no celular:**")
    st.caption("1. Toque em Baixar → 2. Abra a imagem → 3. Mantenha pressionada → 4. Salvar em Fotos/Imagens")

    if legenda:
        st.markdown("---")
        st.markdown("### Legenda pronta (copie e cole)")
        st.markdown(f'<div class="legenda-box">{legenda}</div>', unsafe_allow_html=True)
        st.code(legenda, language=None)
        st.caption("Toque no texto acima para selecionar e copiar. Apenas 5 hashtags.")

    st.markdown("---")
    st.markdown("### Publicar")
    formato = "Story" if is_story else "Post 4:5"
    st.info(f"Depois de salvar a imagem nas Fotos, abra o Instagram ou TikTok e publique como **{formato}**.")
    st.caption("No Instagram: + → Story ou Post → selecione a imagem das suas Fotos.")

# ========== TELA INICIAL ==========
if st.session_state.fluxo is None:
    st.title("PK Closet")
    st.markdown("Escolha o que deseja criar hoje:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☀️ Bom Dia", use_container_width=True):
            st.session_state.fluxo = "bom_dia"
            st.session_state.bom_dia_step = 1
            st.rerun()
    with col2:
        if st.button("🕐 Funcionamento", use_container_width=True):
            st.session_state.fluxo = "funcionamento"
            st.session_state.func_step = 1
            st.session_state.func_data = {}
            st.rerun()
    with col3:
        if st.button("👗 Produto", use_container_width=True):
            st.session_state.fluxo = "produto"
            st.session_state.prod_step = 1
            st.session_state.prod_data = {}
            st.rerun()
    st.divider()
    st.caption("Uma pergunta por vez • Respostas simples • Arte + legenda prontas")

# ========== BOM DIA ==========
elif st.session_state.fluxo == "bom_dia":
    st.title("Bom Dia — Story 9:16")
    if st.session_state.bom_dia_step == 1:
        if "frase_bom_dia" not in st.session_state:
            st.session_state.frase_bom_dia = gerar_frase_emocional()
        st.markdown("### Proposta de frase")
        st.info(st.session_state.frase_bom_dia)
        st.markdown("**A frase está aprovada?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="bd_sim"):
                st.session_state.bom_dia_step = 2
                st.rerun()
        with col2:
            if st.button("❌ Não (gerar outra)", key="bd_nao"):
                st.session_state.frase_bom_dia = gerar_frase_emocional()
                st.rerun()
    elif st.session_state.bom_dia_step == 2:
        st.success("Frase aprovada! Gerando arte...")
        with st.spinner("Montando a arte..."):
            path = create_bom_dia(st.session_state.frase_bom_dia)
            st.session_state.arte_path = path
        legenda_bd = f"{st.session_state.frase_bom_dia}\n\n#PKCloset #BomDia #ModaFeminina #RibeiraoPreto #ModaBrasil"
        mostrar_download_e_legenda(path, legenda=legenda_bd, is_story=True)
        if st.button("← Voltar ao início"):
            st.session_state.fluxo = None
            st.session_state.bom_dia_step = 0
            if "frase_bom_dia" in st.session_state:
                del st.session_state.frase_bom_dia
            st.rerun()

# ========== FUNCIONAMENTO ==========
elif st.session_state.fluxo == "funcionamento":
    st.title("Funcionamento — Story 9:16")
    step = st.session_state.func_step
    data = st.session_state.func_data
    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
            "Sexta-feira", "Sábado", "Domingo"]

    if step == 1:
        st.markdown("**Qual a data do comunicado?**")
        data_input = st.date_input("Data", value=date.today(), key="func_date")
        if st.button("Continuar"):
            st.session_state.func_data["data"] = data_input
            st.session_state.func_step = 2
            st.rerun()
    elif step == 2:
        data_obj = data["data"]
        st.markdown(f"**Data:** {dias[data_obj.weekday()]}, {data_obj.strftime('%d/%m/%Y')}")
        st.markdown("**Vamos usar o horário habitual deste dia?**")
        st.caption("Seg–Sex 09:00–19:00 | Sáb 09:00–15:00 | Dom/Feriado fechado")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="func_hab_sim"):
                if data_obj.weekday() == 5:
                    horario = "09:00 às 15:00"
                elif data_obj.weekday() == 6:
                    horario = "Fechado"
                else:
                    horario = "09:00 às 19:00"
                st.session_state.func_data["horario"] = horario
                st.session_state.func_step = 4
                st.rerun()
        with col2:
            if st.button("❌ Não", key="func_hab_nao"):
                st.session_state.func_step = 3
                st.rerun()
    elif step == 3:
        st.markdown("**Qual o horário correto?**")
        horario_custom = st.text_input("Ex: 10:00 às 18:00", key="horario_custom")
        if st.button("Continuar") and horario_custom.strip():
            st.session_state.func_data["horario"] = horario_custom.strip()
            st.session_state.func_step = 4
            st.rerun()
    elif step == 4:
        st.markdown("**Quer aplicar variação sazonal?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="func_saz_sim"):
                st.session_state.func_data["sazonal"] = True
                st.session_state.func_step = 5
                st.rerun()
        with col2:
            if st.button("❌ Não", key="func_saz_nao"):
                st.session_state.func_data["sazonal"] = False
                st.session_state.func_step = 5
                st.rerun()
    elif step == 5:
        data_obj = data["data"]
        st.markdown("### Proposta")
        st.write(f"**Data:** {dias[data_obj.weekday()]}, {data_obj.strftime('%d/%m/%Y')}")
        st.write(f"**Horário:** {data['horario']}")
        st.write(f"**Variação sazonal:** {'Sim' if data.get('sazonal') else 'Não'}")
        st.write("**CTA:** Te esperamos na loja")
        st.markdown("**A proposta está aprovada?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim — Gerar arte", key="func_aprov_sim"):
                st.session_state.func_step = 6
                st.rerun()
        with col2:
            if st.button("❌ Não", key="func_aprov_nao"):
                st.session_state.func_step = 1
                st.rerun()
    elif step == 6:
        st.success("Proposta aprovada! Gerando arte...")
        with st.spinner("Montando a arte..."):
            path = create_funcionamento(data_obj=data["data"], horario=data["horario"])
            st.session_state.arte_path = path
        legenda_f = f"Hoje estamos abertas! {data['horario']}\nTe esperamos com carinho.\n\n#PKCloset #RibeiraoPreto #ModaFeminina #LojaDeRoupas #ModaBrasil"
        mostrar_download_e_legenda(path, legenda=legenda_f, is_story=True)
        if st.button("← Voltar ao início"):
            st.session_state.fluxo = None
            st.session_state.func_step = 0
            st.rerun()


# ========== PRODUTO ==========
elif st.session_state.fluxo == "produto":
    st.title("Produto")
    step = st.session_state.prod_step
    pdata = st.session_state.prod_data

    if step == 1:
        st.markdown("**Envie a foto da peça**")
        foto = st.file_uploader("Foto do produto", type=["jpg", "jpeg", "png"])
        if foto and st.button("Continuar"):
            st.session_state.prod_data["foto"] = foto
            st.session_state.prod_step = 2
            st.rerun()

    elif step == 2:
        st.markdown("**A foto já mostra a peça em uma modelo real?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="prod_modelo_real_sim"):
                st.session_state.prod_data["tem_modelo_real"] = True
                st.session_state.prod_data["usar_modelo_virtual"] = False
                st.session_state.prod_step = 3
                st.rerun()
        with col2:
            if st.button("❌ Não", key="prod_modelo_real_nao"):
                st.session_state.prod_data["tem_modelo_real"] = False
                st.session_state.prod_step = 2.5
                st.rerun()

    elif step == 2.5:
        st.markdown("**Deseja criar uma versão com modelo virtual?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="prod_virt_sim"):
                st.session_state.prod_step = 2.6
                st.rerun()
        with col2:
            if st.button("❌ Não (usar só a peça)", key="prod_virt_nao"):
                st.session_state.prod_data["usar_modelo_virtual"] = False
                st.session_state.prod_step = 3
                st.rerun()

    elif step == 2.6:
        st.warning("A modelo virtual cria uma **simulação**. Alguns detalhes da peça (cor, tecido, modelagem) podem não ficar idênticos ao produto real.")
        st.markdown("**Deseja continuar mesmo assim?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim, continuar", key="prod_virt_confirm_sim"):
                st.session_state.prod_data["usar_modelo_virtual"] = True
                st.session_state.prod_step = 3
                st.rerun()
        with col2:
            if st.button("❌ Não, usar só a peça", key="prod_virt_confirm_nao"):
                st.session_state.prod_data["usar_modelo_virtual"] = False
                st.session_state.prod_step = 3
                st.rerun()

    elif step == 3:
        st.markdown("**Qual o nome da peça?**")
        nome = st.text_input("Ex: Vestido Midi Floral", key="prod_nome")
        if st.button("Continuar") and nome.strip():
            st.session_state.prod_data["nome"] = nome.strip()
            st.session_state.prod_step = 4
            st.rerun()

    elif step == 4:
        st.markdown("**Quais as cores disponíveis?**")
        cores = st.text_input("Ex: Off-white, Rosé, Preto", key="prod_cores")
        if st.button("Continuar") and cores.strip():
            st.session_state.prod_data["cores"] = cores.strip()
            st.session_state.prod_step = 5
            st.rerun()

    elif step == 5:
        st.markdown("**Qual a grade disponível?**")
        grade = st.text_input("Ex: P ao GG", key="prod_grade")
        if st.button("Continuar") and grade.strip():
            st.session_state.prod_data["grade"] = grade.strip()
            st.session_state.prod_step = 6
            st.rerun()

    elif step == 6:
        st.markdown("**Deseja incluir o preço?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key="prod_preco_sim"):
                st.session_state.prod_step = 7
                st.rerun()
        with col2:
            if st.button("❌ Não", key="prod_preco_nao"):
                st.session_state.prod_data["preco"] = None
                st.session_state.prod_step = 8
                st.rerun()

    elif step == 7:
        st.markdown("**Qual o valor?**")
        preco = st.text_input("Ex: R$ 189,90", key="prod_valor")
        if st.button("Continuar") and preco.strip():
            st.session_state.prod_data["preco"] = preco.strip()
            st.session_state.prod_step = 8
            st.rerun()

    elif step == 8:
        st.markdown("**É para Story 9:16?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim (Story)", key="prod_story_sim"):
                st.session_state.prod_data["formato"] = "story"
                st.session_state.prod_step = 9
                st.rerun()
        with col2:
            if st.button("❌ Não (Post 4:5)", key="prod_story_nao"):
                st.session_state.prod_data["formato"] = "post"
                st.session_state.prod_step = 9
                st.rerun()

    elif step == 9:
        st.markdown("### Proposta")
        st.write(f"**Peça:** {pdata.get('nome')}")
        st.write(f"**Cores:** {pdata.get('cores')}")
        st.write(f"**Grade:** {pdata.get('grade')}")
        st.write(f"**Preço:** {pdata.get('preco') or 'Não informado'}")
        st.write(f"**Formato:** {'Story 9:16' if pdata.get('formato') == 'story' else 'Post 4:5'}")
        if pdata.get("tem_modelo_real"):
            st.write("**Modelo:** Foto com modelo real (será preservada intacta)")
        elif pdata.get("usar_modelo_virtual"):
            st.write("**Modelo:** Virtual (simulação — detalhes podem variar)")
        else:
            st.write("**Modelo:** Somente a peça")
        st.markdown("**A proposta está aprovada?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim — Gerar arte + legenda", key="prod_aprov_sim"):
                st.session_state.prod_step = 10
                st.rerun()
        with col2:
            if st.button("❌ Não", key="prod_aprov_nao"):
                st.session_state.prod_step = 1
                st.rerun()

    elif step == 10:
        st.success("Proposta aprovada! Gerando arte...")
        foto = pdata.get("foto")
        if foto is None:
            st.error("Foto não encontrada. Volte e envie novamente.")
        else:
            temp_dir = Path("output/temp")
            temp_dir.mkdir(exist_ok=True)
            temp_foto = temp_dir / "produto_temp.png"
            with open(temp_foto, "wb") as f:
                f.write(foto.getbuffer())

            usar_virtual = pdata.get("usar_modelo_virtual", False)

            if usar_virtual:
                st.warning("⚠️ **Modelo Virtual (Simulação)**\n\nA imagem da modelo é conceitual. Cores, tecido e modelagem podem não ficar idênticos ao produto real.")
                with st.spinner("Gerando versão conceitual com modelo virtual..."):
                    # Por enquanto geramos a arte com a peça original
                    # e marcamos claramente como simulação.
                    # A geração avançada de modelo vestindo a peça
                    # pode ser feita sob demanda neste chat com Grok Imagine.
                    path = create_produto(
                        foto_path=temp_foto,
                        nome=pdata.get("nome", "Peça") + " (Simulação)",
                        cores=pdata.get("cores", ""),
                        grade=pdata.get("grade", ""),
                        preco=pdata.get("preco"),
                        formato=pdata.get("formato", "story"),
                    )
                    st.session_state.arte_path = path
                st.info("Para uma modelo virtual mais realista, me envie a foto da peça neste chat e eu gero a simulação com IA.")
            else:
                with st.spinner("Inserindo a foto original intacta..."):
                    path = create_produto(
                        foto_path=temp_foto,
                        nome=pdata.get("nome", "Peça"),
                        cores=pdata.get("cores", ""),
                        grade=pdata.get("grade", ""),
                        preco=pdata.get("preco"),
                        formato=pdata.get("formato", "story"),
                    )
                    st.session_state.arte_path = path

            legenda = gerar_legenda_produto(
                nome_peca=pdata.get("nome", "peça"),
                cores=pdata.get("cores", ""),
                preco=pdata.get("preco") or "",
            )

            is_story = pdata.get("formato") == "story"
            mostrar_download_e_legenda(path, legenda=legenda, is_story=is_story)

            st.markdown("### Copiar legenda")
            st.code(legenda, language=None)
            st.caption("Toque no texto → Selecionar tudo → Copiar. Depois cole no Instagram ou TikTok.")

        if st.button("← Voltar ao início"):
            st.session_state.fluxo = None
            st.session_state.prod_step = 0
            st.session_state.prod_data = {}
            st.rerun()
