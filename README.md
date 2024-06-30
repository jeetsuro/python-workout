# In Normal case(without docker usages) then set ENV variable 'APP_COLOR' for below OS if possible;

  # 1 ) Windows : set APP_COLOR=blue
  # 2 ) Linux   : export APP_COLORb=blue
  
  #  python simple.py # [ Not working under docker, but for normal execution ] 
  #  python simple.py --color red

 - docker build -t 198404/simple:v1 .
 - docker run 198404/simple:v1 --color red
 - docker run 198404/simple:v1 --color BLACK

  Docker image push process: 
  
  docker login  -u <my docker-hub-id> -p <my docker-hub-password>
  docker tag 198404/simple:v1 198404/simple:v1
  docker push 198404/simple:v1
