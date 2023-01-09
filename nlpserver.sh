#!sh
if [[ $1 == 'start' ]]
then
  cd stanford-corenlp-full-2018-02-27
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos \
-status_port 9000 -port 9000 -timeout 15000
elif [[ $1 == 'kill' ]]
then
  kill $(lsof -t -i:9000) 2> /dev/null
  if [[ $? -eq 1 ]]
  then
  echo "No process is using port 9000"
  fi
else
echo "No arguments given, does nothing"
fi

