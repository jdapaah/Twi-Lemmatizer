# Twi Lemmatizer
## Jeremy Dapaah, Princeton University
Fall 2022 Indpendent Research

Advised by Christiane Fellbaum

to use, install google, nltk, enchant
you will need to install some packages for nltk (via python) and enchant (via homebrew)
you also need to install the nlp core server
```
    curl https://downloads.cs.stanford.edu/nlp/software/stanford-corenlp-full-2018-02-27.zip --output server.zip
    unzip server.zip
    rm server.zip
```
The server can be started with ./nlpserver start and stopped with ./nlpserver kill

Create a google cloud account
create a project
enable the cloud translation api for the project
create a service account with a private key

download the key json to `service-account.json`
