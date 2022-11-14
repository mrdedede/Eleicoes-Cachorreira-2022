import streamlit as st
import pandas as pd

st.title("Eleições Cachorreira 2022")

# Loga o Usuário no sistema
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

def login(el_id, user):
    # Spinner para carregar a tela de login
    with st.spinner('Logando, por favor aguarde...'):
        #Ler os dados eleitorais e encontrar o usuário buscado
        elector_data = pd.read_csv("./election_ids.csv")
        # Checar se o usuário votou, caso tenha, negar o acesso
        if user == elector_data.iloc[el_id-1]['username']:
            voted = check_if_voted(el_id)
            if voted:
                return elector_data.loc[elector_data['election_id'] == el_id]['region'][el_id-1]
            else:
                pass
        else :
            st.error('Acesso negado!')
            return False

def check_if_voted(el_id):
    # Checa se o ID de eleitor do usuário se encontra no Dataset
    voted_dataset = pd.read_csv("voters_that_voted.csv")
    # Caso tenha votado, retornar o erro de que o voto foi dado
    if not voted_dataset.loc[voted_dataset['election_id'] == el_id].empty:
        st.error('Você já votou nessas eleições!')
        return False
    else:
        st.success("Logado!")
        return True

def voting_screen():
    #Mostra a tela de eleição
    regions_df = pd.read_csv("region_dataset.csv")
    # Busca os candidatos na região do eleitor
    region_set = regions_df.loc[regions_df['microregion'] == st.session_state.voting_region]
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
# Se o eleitor tiver logado, checar se ele ele já votou ou não
else:
    if 'vote_data' not in st.session_state:
        voting_screen()
    else:
        st.success("Obrigado por votar nas Eleições Cachorreira!")