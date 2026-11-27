import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "data" / "crm.db"
DB_PATH.parent.mkdir(exist_ok=True)

st.set_page_config(
    page_title="DAVIA CRM | Gestão de Vendas",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- ESTILO VISUAL --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f7fb; }
[data-testid="stHeader"] { background: rgba(245,247,251,.85); }
[data-testid="stSidebar"] { background: #101b32; }
[data-testid="stSidebar"] * { color: #edf3ff !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 10px 12px; border-radius: 10px; margin: 3px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: #22314e; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px; }
.hero {
    background: linear-gradient(115deg,#142542 0%,#244c7c 100%);
    border-radius: 18px; padding: 24px 28px; color: white; margin-bottom: 22px;
    box-shadow: 0 10px 25px rgba(20,37,66,.12);
}
.hero h1 { color: white; font-size: 28px; margin: 0 0 5px 0; font-weight: 800; }
.hero p { color: #d7e5f8; margin: 0; font-size: 14px; }
.metric-card {
    background: white; border: 1px solid #e8edf5; border-radius: 15px;
    padding: 17px 18px; box-shadow: 0 4px 14px rgba(25,45,75,.035);
    min-height: 112px;
}
.metric-label { color: #758198; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .055em; }
.metric-value { color: #17243b; font-size: 25px; font-weight: 800; margin-top: 8px; }
.metric-note { color: #8792a5; font-size: 11px; margin-top: 3px; }
.section-title { font-size: 18px; font-weight: 800; color: #1c2b45; margin: 8px 0 12px 0; }
.panel {
    background: white; border: 1px solid #e8edf5; border-radius: 15px;
    padding: 18px 20px; margin-bottom: 14px;
}
.small-muted { color: #7c879b; font-size: 12px; }
div[data-testid="stForm"] {
    background: white; border: 1px solid #e8edf5; border-radius: 14px;
    padding: 18px;
}
.stButton button, .stFormSubmitButton button {
    border-radius: 10px; font-weight: 700; min-height: 40px;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: #2563eb; border-color: #2563eb;
}
div[data-testid="stDataFrame"] { border: 1px solid #e8edf5; border-radius: 12px; overflow: hidden; }
[data-testid="stMetric"] {
    background: white; border: 1px solid #e8edf5; border-radius: 14px; padding: 12px 15px;
}
hr { border-color: #e8edf5; }
</style>
""", unsafe_allow_html=True)

# -------------------- BANCO DE DADOS --------------------
def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            empresa TEXT,
            telefone TEXT,
            email TEXT,
            origem TEXT,
            etapa TEXT NOT NULL DEFAULT 'Novo',
            valor REAL DEFAULT 0,
            responsavel TEXT,
            observacoes TEXT,
            criado_em TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            lead_id INTEGER,
            vencimento TEXT,
            prioridade TEXT DEFAULT 'Média',
            status TEXT DEFAULT 'Pendente',
            notas TEXT,
            FOREIGN KEY(lead_id) REFERENCES leads(id)
        );
        """)

def query_df(sql, params=()):
    with connect() as con:
        return pd.read_sql_query(sql, con, params=params)

def money(v):
    return f"R$ {float(v or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def metric_card(label, value, note, icon):
    st.markdown(f"""
    <div class="metric-card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div class="metric-label">{label}</div><div style="font-size:21px">{icon}</div>
      </div>
      <div class="metric-value">{value}</div>
      <div class="metric-note">{note}</div>
    </div>""", unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

init_db()

# -------------------- MENU --------------------
with st.sidebar:
    st.markdown("## 📈 DAVIA CRM")
    st.caption("GESTÃO COMERCIAL")
    st.divider()
    page = st.radio(
        "MENU PRINCIPAL",
        ["Visão geral", "Contatos", "Funil de vendas", "Tarefas", "Relatórios"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("**Atalhos**")
    if st.button("＋ Novo contato", use_container_width=True):
        st.session_state["abrir_novo_contato"] = True
        st.session_state["pagina_destino"] = "Contatos"
        st.rerun()
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.caption("DAVIA CRM • Protótipo 1.1")
    st.caption("Seus relacionamentos em um só lugar.")

leads = query_df("SELECT * FROM leads")
tasks = query_df("SELECT * FROM tarefas")

# -------------------- VISÃO GERAL --------------------
if page == "Visão geral":
    hero("Visão geral", "Acompanhe seus resultados e saiba o que precisa de atenção hoje.")
    total = len(leads)
    ativos = len(leads[leads["etapa"].isin(["Novo", "Contato feito", "Qualificado", "Proposta enviada", "Negociação"])]) if total else 0
    ganhos = leads[leads["etapa"] == "Ganho"] if total else leads
    pipeline = leads[~leads["etapa"].isin(["Perdido", "Ganho"])]["valor"].sum() if total else 0
    receita = ganhos["valor"].sum() if len(ganhos) else 0
    atrasadas = len(tasks[(tasks["status"] == "Pendente") & (tasks["vencimento"].fillna("") < date.today().isoformat())]) if len(tasks) else 0

    cols = st.columns(4)
    vals = [
        ("Contatos", str(total), "Pessoas e empresas cadastradas", "👥"),
        ("Oportunidades ativas", str(ativos), "Negociações em andamento", "🎯"),
        ("Em negociação", money(pipeline), "Valor potencial no funil", "💼"),
        ("Vendas ganhas", money(receita), f"{len(ganhos)} oportunidade(s) convertida(s)", "🏆"),
    ]
    for col, item in zip(cols, vals):
        with col:
            metric_card(*item)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    left, right = st.columns([1.45, 1])
    with left:
        st.markdown('<div class="panel"><div class="section-title">📊 Desempenho do funil</div>', unsafe_allow_html=True)
        if total:
            order = ["Novo", "Contato feito", "Qualificado", "Proposta enviada", "Negociação", "Ganho", "Perdido"]
            counts = leads["etapa"].value_counts().reindex(order, fill_value=0)
            st.bar_chart(counts, color="#3978d4", height=250)
        else:
            st.info("Cadastre seu primeiro contato para visualizar o funil.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="section-title">⏰ Atenção para hoje</div>', unsafe_allow_html=True)
        pendentes = tasks[tasks["status"] == "Pendente"] if len(tasks) else tasks
        if len(pendentes):
            hoje = pendentes[pendentes["vencimento"] == date.today().isoformat()]
            st.metric("Tarefas para hoje", len(hoje))
            st.metric("Tarefas atrasadas", atrasadas)
            st.caption("Acesse Tarefas para atualizar seus acompanhamentos.")
        else:
            st.success("Tudo em dia! Você não possui tarefas pendentes.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🕘 Contatos adicionados recentemente</div>', unsafe_allow_html=True)
    if total:
        recent = leads.sort_values("id", ascending=False).head(6)
        st.dataframe(recent[["nome", "empresa", "telefone", "etapa", "valor", "responsavel"]].rename(columns={
            "nome":"Contato", "empresa":"Empresa", "telefone":"Telefone", "etapa":"Etapa",
            "valor":"Valor estimado", "responsavel":"Responsável"
        }), use_container_width=True, hide_index=True)
    else:
        st.info("Sua área de trabalho está pronta. Comece cadastrando um contato.")

# -------------------- CONTATOS --------------------
elif page == "Contatos":
    hero("Contatos", "Centralize seus leads, clientes e oportunidades em uma lista fácil de gerenciar.")
    tab_lista, tab_novo = st.tabs(["📇 Lista de contatos", "＋ Adicionar contato"])
    with tab_novo:
        with st.form("novo_lead", clear_on_submit=True):
            st.markdown("**Informações principais**")
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome *", placeholder="Nome do contato")
            empresa = c2.text_input("Empresa", placeholder="Nome da empresa")
            telefone = c1.text_input("Telefone / WhatsApp", placeholder="(00) 00000-0000")
            email = c2.text_input("E-mail", placeholder="contato@empresa.com")
            st.markdown("**Informações comerciais**")
            c3, c4, c5 = st.columns(3)
            origem = c3.selectbox("Como chegou até você?", ["Indicação", "Instagram", "WhatsApp", "Site", "Anúncio", "Prospecção", "Outro"])
            etapa = c4.selectbox("Etapa atual", ["Novo", "Contato feito", "Qualificado", "Proposta enviada", "Negociação", "Ganho", "Perdido"])
            valor = c5.number_input("Valor potencial (R$)", min_value=0.0, step=50.0)
            responsavel = st.text_input("Responsável pelo atendimento")
            observacoes = st.text_area("Anotações", placeholder="Preferências, necessidades, histórico da conversa...")
            submitted = st.form_submit_button("Salvar contato", type="primary", use_container_width=True)
            if submitted:
                if not nome.strip():
                    st.error("O nome é obrigatório.")
                else:
                    with connect() as con:
                        con.execute("""INSERT INTO leads
                        (nome, empresa, telefone, email, origem, etapa, valor, responsavel, observacoes, criado_em)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (nome.strip(), empresa, telefone, email, origem, etapa, valor, responsavel, observacoes, datetime.now().isoformat(timespec="seconds")))
                    st.success("Contato salvo com sucesso!")
                    st.rerun()

    with tab_lista:
        if len(leads):
            f1, f2, f3 = st.columns([1, 1.3, 1])
            filtro_etapa = f1.selectbox("Etapa", ["Todas"] + sorted(leads["etapa"].dropna().unique().tolist()))
            busca = f2.text_input("Buscar contato", placeholder="Nome, empresa, telefone ou e-mail")
            ordenar = f3.selectbox("Ordenar por", ["Mais recentes", "Nome A–Z", "Maior valor"])
            df = leads.copy()
            if filtro_etapa != "Todas":
                df = df[df["etapa"] == filtro_etapa]
            if busca:
                mask = df[["nome","empresa","telefone","email"]].fillna("").astype(str).apply(
                    lambda col: col.str.contains(busca, case=False, na=False)).any(axis=1)
                df = df[mask]
            if ordenar == "Nome A–Z":
                df = df.sort_values("nome")
            elif ordenar == "Maior valor":
                df = df.sort_values("valor", ascending=False)
            else:
                df = df.sort_values("id", ascending=False)
            st.caption(f"{len(df)} contato(s) encontrado(s)")
            st.dataframe(df[["id","nome","empresa","telefone","email","etapa","valor","responsavel"]].rename(columns={
                "id":"ID","nome":"Nome","empresa":"Empresa","telefone":"Telefone","email":"E-mail",
                "etapa":"Etapa","valor":"Valor (R$)","responsavel":"Responsável"
            }), use_container_width=True, hide_index=True)
            st.markdown("**Gerenciar contato**")
            selected = st.selectbox("Selecione pelo ID", df["id"].tolist(), format_func=lambda x: f"#{x} — {df.loc[df.id == x, 'nome'].iloc[0]}")
            row = query_df("SELECT * FROM leads WHERE id=?", (int(selected),)).iloc[0]
            with st.expander("✏️ Editar informações", expanded=False):
                with st.form("editar_lead"):
                    a,b = st.columns(2)
                    e_nome = a.text_input("Nome", value=row["nome"])
                    e_empresa = b.text_input("Empresa", value=row["empresa"] or "")
                    e_tel = a.text_input("Telefone", value=row["telefone"] or "")
                    e_email = b.text_input("E-mail", value=row["email"] or "")
                    etapas = ["Novo","Contato feito","Qualificado","Proposta enviada","Negociação","Ganho","Perdido"]
                    e_etapa = a.selectbox("Etapa", etapas, index=etapas.index(row["etapa"]))
                    e_valor = b.number_input("Valor potencial (R$)", min_value=0.0, value=float(row["valor"] or 0), step=50.0)
                    e_resp = st.text_input("Responsável", value=row["responsavel"] or "")
                    e_obs = st.text_area("Anotações", value=row["observacoes"] or "")
                    save = st.form_submit_button("Salvar alterações", type="primary")
                    if save:
                        with connect() as con:
                            con.execute("""UPDATE leads SET nome=?, empresa=?, telefone=?, email=?, etapa=?, valor=?, responsavel=?, observacoes=? WHERE id=?""",
                            (e_nome,e_empresa,e_tel,e_email,e_etapa,e_valor,e_resp,e_obs,int(selected)))
                        st.success("Contato atualizado.")
                        st.rerun()
            with st.expander("🗑️ Excluir contato", expanded=False):
                st.warning("A exclusão também remove as tarefas vinculadas a este contato.")
                confirm = st.checkbox("Confirmo que desejo excluir este contato.", key="confirm_delete_lead")
                if st.button("Excluir definitivamente", disabled=not confirm):
                    with connect() as con:
                        con.execute("DELETE FROM tarefas WHERE lead_id=?", (int(selected),))
                        con.execute("DELETE FROM leads WHERE id=?", (int(selected),))
                    st.success("Contato excluído.")
                    st.rerun()
        else:
            st.info("Nenhum contato cadastrado ainda. Use a aba “Adicionar contato” para começar.")

# -------------------- FUNIL --------------------
elif page == "Funil de vendas":
    hero("Funil de vendas", "Visualize em que etapa cada oportunidade está e acompanhe o valor potencial.")
    etapas = ["Novo", "Contato feito", "Qualificado", "Proposta enviada", "Negociação", "Ganho", "Perdido"]
    if len(leads):
        resumo = leads.groupby("etapa").agg(quantidade=("id","count"), valor=("valor","sum")).reindex(etapas, fill_value=0).reset_index()
        cols = st.columns(4)
        for i, etapa_nome in enumerate(etapas[:4]):
            r = resumo[resumo["etapa"] == etapa_nome].iloc[0]
            with cols[i]:
                metric_card(etapa_nome, str(int(r["quantidade"])), money(r["valor"]) + " em oportunidades", "🔹")
        cols2 = st.columns(3)
        for i, etapa_nome in enumerate(etapas[4:]):
            r = resumo[resumo["etapa"] == etapa_nome].iloc[0]
            with cols2[i]:
                metric_card(etapa_nome, str(int(r["quantidade"])), money(r["valor"]), "🏁" if etapa_nome=="Ganho" else "•")
        st.markdown('<div class="section-title">Oportunidades por etapa</div>', unsafe_allow_html=True)
        for etapa_nome in etapas:
            grupo = leads[leads["etapa"] == etapa_nome]
            with st.expander(f"{etapa_nome} · {len(grupo)} oportunidade(s) · {money(grupo['valor'].sum())}"):
                if len(grupo):
                    st.dataframe(grupo[["nome","empresa","telefone","valor","responsavel"]], use_container_width=True, hide_index=True)
                else:
                    st.caption("Nenhuma oportunidade nesta etapa.")
    else:
        st.info("Cadastre contatos para começar a acompanhar seu funil.")

# -------------------- TAREFAS --------------------
elif page == "Tarefas":
    hero("Tarefas e acompanhamentos", "Organize retornos, ligações e próximos passos para não perder oportunidades.")
    tab_pend, tab_add = st.tabs(["☑️ Minhas tarefas", "＋ Nova tarefa"])
    with tab_add:
        leads_for_task = query_df("SELECT id, nome FROM leads ORDER BY nome")
        with st.form("nova_tarefa", clear_on_submit=True):
            titulo = st.text_input("O que precisa ser feito? *", placeholder="Ex.: Retornar proposta para o cliente")
            opts = {"Sem vínculo": None}
            for _, r in leads_for_task.iterrows():
                opts[f'{r["nome"]} · #{r["id"]}'] = int(r["id"])
            vinculo = st.selectbox("Contato relacionado", list(opts.keys()))
            c1,c2 = st.columns(2)
            vencimento = c1.date_input("Data de vencimento", value=date.today())
            prioridade = c2.selectbox("Prioridade", ["Baixa","Média","Alta"], index=1)
            notas = st.text_area("Detalhes")
            ok = st.form_submit_button("Criar tarefa", type="primary", use_container_width=True)
            if ok:
                if not titulo.strip():
                    st.error("Informe o que precisa ser feito.")
                else:
                    with connect() as con:
                        con.execute("INSERT INTO tarefas (titulo,lead_id,vencimento,prioridade,notas) VALUES (?,?,?,?,?)",
                                    (titulo,opts[vinculo],vencimento.isoformat(),prioridade,notas))
                    st.success("Tarefa criada.")
                    st.rerun()
    with tab_pend:
        task_df = query_df("""SELECT t.id,t.titulo,l.nome AS contato,t.vencimento,t.prioridade,t.status,t.notas
                              FROM tarefas t LEFT JOIN leads l ON l.id=t.lead_id ORDER BY
                              CASE WHEN t.status='Pendente' THEN 0 ELSE 1 END, t.vencimento""")
        if len(task_df):
            f1,f2 = st.columns(2)
            status_filter = f1.selectbox("Status", ["Todas","Pendente","Concluída"])
            priority_filter = f2.selectbox("Prioridade", ["Todas","Alta","Média","Baixa"])
            view = task_df.copy()
            if status_filter != "Todas": view = view[view["status"] == status_filter]
            if priority_filter != "Todas": view = view[view["prioridade"] == priority_filter]
            st.dataframe(view[["id","titulo","contato","vencimento","prioridade","status"]].rename(columns={
                "id":"ID","titulo":"Tarefa","contato":"Contato","vencimento":"Vencimento",
                "prioridade":"Prioridade","status":"Status"
            }), use_container_width=True, hide_index=True)
            pend = task_df[task_df["status"] == "Pendente"]["id"].tolist()
            if pend:
                chosen = st.selectbox("Concluir tarefa (ID)", pend)
                if st.button("✓ Marcar como concluída", type="primary"):
                    with connect() as con:
                        con.execute("UPDATE tarefas SET status='Concluída' WHERE id=?", (int(chosen),))
                    st.success("Tarefa concluída.")
                    st.rerun()
            all_ids = task_df["id"].tolist()
            with st.expander("Excluir tarefa"):
                remove_id = st.selectbox("ID da tarefa", all_ids, key="remove_task")
                if st.button("Excluir tarefa selecionada"):
                    with connect() as con:
                        con.execute("DELETE FROM tarefas WHERE id=?", (int(remove_id),))
                    st.rerun()
        else:
            st.info("Você ainda não possui tarefas. Crie um acompanhamento na aba “Nova tarefa”.")

# -------------------- RELATÓRIOS --------------------
elif page == "Relatórios":
    hero("Relatórios", "Entenda os resultados da operação e exporte os dados para análise.")
    if len(leads):
        ganhos = leads[leads["etapa"] == "Ganho"]
        perdidos = leads[leads["etapa"] == "Perdido"]
        total_valor = leads["valor"].sum()
        conversao = (len(ganhos) / len(leads) * 100) if len(leads) else 0
        c1,c2,c3 = st.columns(3)
        with c1: metric_card("Valor potencial", money(total_valor), "Soma das oportunidades cadastradas", "💰")
        with c2: metric_card("Vendas ganhas", money(ganhos["valor"].sum()), f"{len(ganhos)} negócio(s)", "🏆")
        with c3: metric_card("Conversão", f"{conversao:.1f}%".replace(".",","), "Negócios ganhos / contatos cadastrados", "📈")
        st.markdown('<div class="section-title">Resumo por etapa</div>', unsafe_allow_html=True)
        resumo = leads.groupby("etapa", as_index=False).agg(Quantidade=("id","count"), Valor=("valor","sum"))
        st.dataframe(resumo, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Exportar contatos em CSV", leads.to_csv(index=False).encode("utf-8-sig"),
                           file_name="relatorio_crm.csv", mime="text/csv", type="primary")
    else:
        st.info("Cadastre contatos para gerar relatórios.")

st.markdown("<div style='height:18px'></div><hr>", unsafe_allow_html=True)
st.markdown('<div class="small-muted">DAVIA CRM • Organize relacionamentos, acompanhe oportunidades e venda com mais clareza.</div>', unsafe_allow_html=True)
