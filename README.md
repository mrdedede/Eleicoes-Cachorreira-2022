# Eleições Cachorreira 2022
## This is a project in Streamlit that contains:
- A Login Screen
- A Voting System
- Analytics related to the pool of voters
- Analytics related to the results

It has been created as a project for a group of friends that wanted to vote for our next representative

## What does each of the files mean?
### Home.py
Contains the login and voting system
It's the file that should be run when starting the project

### pages/Vote_results.py
Contains the results of the voting so far as well as the parcial results per riding

### pages/Pre-vote_analytics.py
Shows an analysis of the pool of voters we have so far, including which place has more voters

### election_ids.csv
Has all the voter information which will be needed for the login screen as well as which riding is each voter voting for

### candidate_dataset.csv
Includes all candidates, their parties and their ridings

### region_dataset.csv
Includes all regions, starting from the city, to the state/province and, finally, the country

### voters_that_voted.csv
Will be updated as the programme runs and people vote.
Includes the voter ID and a boolean operator that would confirm that the votes were deposited

### votes_deposited.csv
Will be updated as the programme runs and people vote.
Includes the candidate that received a vote and the region that the vote came from

## How can I run this project?
First of all, I'd recommend you change or add data to the candidate_dataset.csv and election_ids.csv files as needed
In case you need to run it locally, just run it with streamlit as:
```
streamlit run Home.py
```
Also, do remember to add the party color data in "Vote_results.py" as there hasn't been enough time to create a separate dataset with this specific purpose
