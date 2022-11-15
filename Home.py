import gc
import streamlit as st
import pandas as pd

st.title("Eleições Cachorreira 2022")

# Loga o usuário no sistema (Lifecycle)
def login_screen():
    # Dados de Usuário
    el_id = st.text_input("ID de Eleitor")
    user = st.text_input("Username")
    sent = st.button("Enviar")
    # Se o botão tiver sido apertado, prosseguir
    if sent:
        try:
            # Caso o ID seja válido (numérico), buscar a região, do contrário, há um erro de acesso
            el_id_int = int(el_id)
            user_region = login(el_id_int, user)
            if user_region:
                st.session_state.electoral_id = el_id
                st.session_state.voting_region = user_region
            else:
                sent = False
        except:
            # Erro de acesso encontrado
            sent = False
            st.error('Acesso negado!')
        # Recarregar essa aplicação ao fim desse lifecycle
        st.experimental_rerun()

# Vê se o usuário pode prosseguir ao voto
def login(el_id, user):
    # Spinner para carregar a tela de login
    with st.spinner('Logando, por favor aguarde...'):
        # Ler os dados eleitorais e encontrar o usuário buscaso
        elector_data = pd.read_csv("./election_ids.csv")
        cur_elector = elector_data.loc[elector_data['election_id'] == el_id].reset_index()
        cur_elector = cur_elector.drop(columns=['index'])
        if user == cur_elector['username'][0]:
            # Checar se o usuário já votou
            voted = check_if_voted(el_id)
            if not voted:
                st.success("Logado!")
                cur_region = elector_data.loc[elector_data['election_id'] == el_id]['region']
                cur_region = cur_region.reset_index()
                cur_region = cur_region.drop(columns=['index'])
                st.write(cur_region['region'][0])
                return cur_region['region'][0]
            else:
                st.error('Você já votou nessas eleições!')
        else :
            st.error('Acesso negado!')
            return False

# Checa se o usuário votou ou não
def check_if_voted(el_id):
    # Checa se o ID de eleitor do usuário se encontra no Dataset
    voted_dataset = pd.read_csv("voters_that_voted.csv")
    vote_check = voted_dataset.loc[voted_dataset['election_id'] == el_id]
    # Caso tenha votado, retornar um erro e True
    if not vote_check.empty:
        st.session_state.vote_data = True
        st.error('Você já votou nessas eleições!')
        return True
    # Caso não tenha votado, retornar False e deletar o dataset de votos depositados da memória
    else:
        del voted_dataset
        gc.collect()
        return False

# Mostra aos usuários os candidatos disponíveis para receber o seu voto
def voting_screen():
    # Mostra a tela de eleição
    regions_df = pd.read_csv("region_dataset.csv")
    # Bucas os candidatos na região do eleitor
    region_set = regions_df.loc[regions_df['microregion'] == st.session_state.voting_region]
    region_set = region_set.reset_index()
    region_set = region_set.drop(columns=['index'])
    st.write(
        f"Você está votando no pote {st.session_state.voting_region}, para o grupo eleitoral {region_set['mesoregion'][0]}")
    total_candidates = pd.read_csv("candidate_dataset.csv")
    # Opções de candidatos + botão de enviar
    region_candidates = total_candidates.loc[total_candidates['region'] == st.session_state.voting_region]
    vote_data = st.radio("Escolha seu candidato", region_candidates)
    sent = st.button("Enviar Voto")
    # Caso enviado, escrever o voto no Dataset
    if sent:
        st.session_state.vote_data = vote_data
        write_vote()

def write_vote():
    # Checar se o eleitor já depositou voto
    unable_to_vote = check_if_voted(st.session_state.electoral_id)
    if not unable_to_vote:
        # Escrever o voto em votes_deposited.csv
        new_vote = [st.session_state.vote_data, st.session_state.voting_region]
        deposited_votes = pd.read_csv('votes_deposited.csv')
        deposited_votes.loc[len(deposited_votes.index)] = new_vote
        deposited_votes.to_csv('votes_deposited.csv', index=False)
        # Escrever o ID de eleitor em voters_that_voted.csv
        new_voter = [st.session_state.electoral_id, 1]
        voted_df = pd.read_csv('voters_that_voted.csv')
        voted_df.loc[len(voted_df.index)] = new_voter
        voted_df.to_csv('voters_that_voted.csv', index=False)
    # Recarregar a aplicação ao fim desse lifecycle
    st.experimental_rerun()

# Se o eleitor ainda não tiver logado, jogar na página de login
if 'electoral_id' not in st.session_state:
    login_screen()
# Se o eleitor tiver logado, checar se ele já votou ou não
else:
    if 'vote_data' not in st.session_state:
        voting_screen()
    else:
        st.success("Obrigado por votar nas Eleições Cachorreira!")