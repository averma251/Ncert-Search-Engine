from django.shortcuts import render
from .models import qas,hist
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def func2():
    from haystack.document_stores import InMemoryDocumentStore
    document_store = InMemoryDocumentStore()
    from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
    doc_dir = "static/data/"
    docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
    document_store.write_documents(docs)
    from haystack.nodes import TfidfRetriever
    retriever = TfidfRetriever(document_store=document_store)
    from haystack.nodes import FARMReader
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
    from haystack.pipelines import ExtractiveQAPipeline
    pipe = ExtractiveQAPipeline(reader, retriever)
    return pipe
def func(question,pipe=func2()):
    
    import pandas as pd
    prediction = pipe.run(
      query=question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    )
    k=len(prediction['answers'])
    temp=[]
    single=[]
    for i in range(k):
        lst=[]
        lst.append(question)
        lst.append(prediction['answers'][i].answer)
        lst.append(prediction['answers'][i].context)
        lst.append(prediction['answers'][i].meta['name'])
        temp.append(lst)
    import numpy as np
    temp=np.array(temp)
    print(temp.shape)
    df = pd.DataFrame(temp, columns = ['question','answer','context','document_name'])
    lst=[]
    temp2 = []
    lst.append(df['question'][0])
    for i in range(5):
        lst.append(df['answer'][i])
    for i in range(5):
        lst.append(df['context'][i])
    for i in range(5):
        lst.append(df['document_name'][i])
    temp2.append(lst)
    for i in range(len(temp2)):
        qa = qas(question=temp2[i][0],a1=temp2[i][1],a2=temp2[i][2],a3=temp2[i][3],a4=temp2[i][4],a5=temp2[i][5],cx1=temp2[i][6],cx2=temp2[i][7],cx3=temp2[i][8],cx4=temp2[i][9],cx5=temp2[i][10],t1="/static/textfiles/" + temp2[i][11],t2="/static/textfiles/" + temp2[i][12],t3="/static/textfiles/" + temp2[i][13],t4="/static/textfiles/" + temp2[i][14],t5="/static/textfiles/" + temp2[i][15])
        qa.save()
    return None

def index(request):
    if 'q' in request.GET:
        if request.GET['q'] == '':
            return render(request, 'searcher/index.html')
        q = request.GET['q']
        if qas.objects.filter(question__icontains=q).first() == None: #continue here
            func(q)
        histr = hist(cur_user=request.user.username,cur_question=q)
        histr.save()
        data = qas.objects.filter(question__icontains=q)
        context = {
        'data': data
        }
        return render(request, 'searcher/results.html', context)
    else:
        data = None
    context = {
        'data': data
    }
    return render(request, 'searcher/index.html', context)

def history(request):
    data = hist.objects.filter(cur_user=request.user.username).order_by('-cur_time')
    context = {
        'data': data
    }
    return render(request, 'searcher/history.html', context)

def view_profile(request):
    user = User.objects.get(username=request.user.username)
    user_email = user.email
    data = {}
    data['username'] = request.user.username
    data['email'] = user_email
    context = {
        'data': data
    }
    return render(request, 'searcher/View.html', context)
 
def csvtodata(request):
    import numpy as np
    import pandas as pd
    import os
    temp=[]
    for item in os.listdir("X:/asd/aa"):
        df=pd.read_csv("X:/asd/aa/"+item)
        lst=[]
        lst.append(df['question'][0])
        for i in range(5):
            lst.append(df['answer'][i])
        for i in range(5):
            lst.append(df['context'][i])
        for i in range(5):
            lst.append(df['document_name'][i])
        temp.append(lst)
    for i in range(len(temp)):
        qa = qas(question=temp[i][0],a1=temp[i][1],a2=temp[i][2],a3=temp[i][3],a4=temp[i][4],a5=temp[i][5],cx1=temp[i][6],cx2=temp[i][7],cx3=temp[i][8],cx4=temp[i][9],cx5=temp[i][10],t1="/static/textfiles/" + temp[i][11],t2="/static/textfiles/" + temp[i][12],t3="/static/textfiles/" + temp[i][13],t4="/static/textfiles/" + temp[i][14],t5="/static/textfiles/" + temp[i][15])
        qa.save()
    return HttpResponse("Done")
