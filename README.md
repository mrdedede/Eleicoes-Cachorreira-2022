# Eleições Cachorreira 2022

A small voting system built with [Streamlit](https://streamlit.io/) for a group of friends who wanted to elect their next representative.

The app has four parts:

- **Login screen**: voters identify themselves with an electoral ID and username.
- **Voting screen**: each voter sees only the candidates from their own region ("pote") and casts one vote.
- **Pre-vote analytics**: charts describing the pool of eligible voters (by network, group and region).
- **Results**: partial results overall, per mesoregion (electoral group) and per region, including turnout (votes vs. abstentions).

## Table of contents

- [Requirements](#requirements)
- [Running the project](#running-the-project)
- [How the app works](#how-the-app-works)
- [Project structure](#project-structure)
- [Data files](#data-files)
- [Preparing an election](#preparing-an-election)
- [Known limitations](#known-limitations)

## Requirements

- Python 3
- [streamlit](https://pypi.org/project/streamlit/)
- [pandas](https://pypi.org/project/pandas/)
- [matplotlib](https://pypi.org/project/matplotlib/) (used by both analytics pages)

There is no `requirements.txt` yet, so install the dependencies manually:

```bash
pip install streamlit pandas matplotlib
```

## Running the project

From the project folder:

```bash
streamlit run Home.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in the browser.

The app is multipage: Streamlit automatically adds the files in `pages/` to the sidebar. Home is the login/voting page; the other two pages are read-only dashboards.

## How the app works

### Login (`Home.py`)

1. The voter enters their **ID de Eleitor** (a number) and **Username**.
2. The app looks up the ID in `election_ids.csv`. The username must match the one stored for that ID.
3. The app checks `voters_that_voted.csv`. If the ID is already there, access is denied with the message "Você já votou nessas eleições!".
4. On success, the voter's region is stored in the session and the voting screen is shown.

Any failure (non-numeric ID, unknown ID, wrong username) shows "Acesso negado!".

### Voting (`Home.py`)

1. The app shows the candidates whose `region` matches the voter's region in `candidate_dataset.csv`.
2. The voter picks one candidate and clicks **Enviar Voto**.
3. The app checks again that the voter has not voted yet (protects against two tabs or a refresh).
4. If the check passes, the app:
   - appends a row `vote, region` to `votes_deposited.csv`;
   - appends a row `election_id, has_voted` (with `1`) to `voters_that_voted.csv`.
5. The voter sees "Obrigado por votar nas Eleições Cachorreira!".

### Analytics and results (`pages/`)

- **Pre-vote analytics** (`pages/Pre-vote_analytics.py`): counts eligible voters (rows of `election_ids.csv`) by macroregion ("Rede"), by mesoregion ("Grupo Eleitoral") and by region ("pote"). A dropdown lets you pick a macroregion to see the breakdown of its regions.
- **Results** (`pages/Vote_results.py`):
  - an overall pie chart of votes per party, plus votes vs. abstentions;
  - for each mesoregion, the party breakdown and turnout;
  - for each region in that mesoregion, the candidate breakdown and turnout.

  If a section fails to build (for example, because there are no votes yet), the page shows "Essa eleição ainda não começou" ("This election hasn't started yet").

## Project structure

```
.
├── Home.py                      # Login and voting screen (entry point)
├── pages/
│   ├── Pre-vote_analytics.py    # Voter pool charts
│   └── Vote_results.py          # Results charts
├── election_ids.csv             # Eligible voters
├── candidate_dataset.csv        # Candidates
├── region_dataset.csv           # Geographic hierarchy of regions
├── voters_that_voted.csv        # Voters who have already voted (generated)
└── votes_deposited.csv          # Votes cast (generated)
```

## Data files

| File | Columns | Purpose | Edited by |
| --- | --- | --- | --- |
| `election_ids.csv` | `election_id`, `username`, `region` | Eligible voters, their login and their region | You, before the election |
| `candidate_dataset.csv` | `candidate_name`, `party`, `region` | Candidates and the region they run in | You, before the election |
| `region_dataset.csv` | `microregion`, `mesoregion`, `macroregion` | Hierarchy: region (pote) → mesoregion (group) → macroregion (network) | You, before the election |
| `voters_that_voted.csv` | `election_id`, `has_voted` | Voters who have voted | The app |
| `votes_deposited.csv` | `vote`, `region` | One row per vote | The app |

Notes:

- `region` in `election_ids.csv` and `candidate_dataset.csv` must match a `microregion` in `region_dataset.csv`.
- `vote` in `votes_deposited.csv` must match a `candidate_name` in `candidate_dataset.csv`.
- `voters_that_voted.csv` and `votes_deposited.csv` start empty (headers only). Do not delete their headers.

## Preparing an election

1. **Voters**: edit `election_ids.csv` with one row per voter. `election_id` must be numeric and unique.
2. **Candidates**: edit `candidate_dataset.csv`. Each candidate needs a unique `candidate_name`, a `party` and a `region`.
3. **Regions**: edit `region_dataset.csv` so every region used above has a row with its mesoregion and macroregion.
4. **Party colors**: the colors used in the results charts are hard-coded in `pages/Vote_results.py` (the `party_colors` table at the top). Add a line there for every party in `candidate_dataset.csv`. A party missing from that table will be dropped from the charts.
5. **Reset the vote data**: before a real election, make sure `voters_that_voted.csv` and `votes_deposited.csv` contain only their headers.

## Known limitations

- Votes are stored in plain CSV files. There is no encryption and no real authentication: the ID and username are the only check.
- Concurrent writes from several users at once are not protected against.
- Party colors are hard-coded in the results page.
- The results charts only work for parties listed in `party_colors`, and only for candidates whose region exists in `region_dataset.csv`.
- The app uses `st.experimental_rerun`, which was removed in recent Streamlit versions. If you upgrade Streamlit and see an error, replace it with `st.rerun`.
