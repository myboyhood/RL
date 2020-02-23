import pickle
import json
f = open('plane-v3-q-learning.pickle','rb')
content = pickle.load(f,encoding='utf-8')
#print (content)
f_tran = open("planeQv0","w")
f.writelines(json.dumps(content)+'\n')
f.close()
