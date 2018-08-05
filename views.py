from django.shortcuts import render
from .models import user_data
from collections import defaultdict
import pandas as pd
import os


def login(request):
    return render(request, 'chat/index.html')


def home(request):
    if request.GET.get('LogOut') == 'LogOut':
        os.remove('chat/pkl files/Logout.pkl')

    try:
        pd.read_pickle('chat/pkl files/Logout.pkl')
        return render(request, 'chat/home_2.html')
    except:
        return render(request, 'chat/home.html')


def profile(request):
    df = pd.read_pickle('chat/pkl files/Username.pkl')

    Uid = df.at[0,'A']
    kl = [{'Uid':Uid}]

    name_dict = {}
    instance = user_data.objects.all()
    ss = []
    for index, name in enumerate(instance):
        user = {}
        uu = user_data.objects.filter(uid=name.uid)
        for i, k in enumerate(uu):
            if Uid != k.uid:
                user['name'] = k.uid
                user['email'] = k.email
                name_dict[k.uid] = k.name
            else:
                kl[0]['Uid'] = k.name
        if len(user) != 0:
            ss.append(user)

    All_user = pd.read_pickle('chat/pkl files/User_data/' + Uid + '.pkl')

    All_user_len = All_user.shape[0]
    # print(All_user_len)
    name_user = []
    for i in range(All_user_len):
        data = {}
        k = All_user.at[i, 'A']
        if k != Uid:
            data['name'] = k
            data['Uid'] = Uid
            data['u1'] = name_dict[k]
        if len(data) != 0:
            name_user.append(data)

    if request.GET.get('ChatRoom') == 'ChatRoom':
        return render(request, 'chat/chat_room.html', {'ss': name_user,
                                                       'l': 1}
                      )
    else:
        return render(request, 'chat/profile.html',{'ss':name_user,
                                                'Uid':kl,
                                                })


def signup(request):
    return render(request, 'chat/Sign_In.html')


def page(request):
    Uid = request.GET.get('uid')
    Name = request.GET.get('name')
    Email = request.GET.get('email')
    Password = request.GET.get('Password')
    re_password = request.GET.get('1')
    data = defaultdict(str)
    instance = user_data.objects.all()
    for index,name in enumerate(instance):
        uu = user_data.objects.filter(uid = name.uid)
        for i,k in enumerate(uu):
            data[k.uid] = 1

    if data[Uid] == 1 and Uid == 'Username' and Uid == 'User' and Uid == 'All_user' and Uid == 'Logout':
        return render(request, 'chat/Sign_In_2.html')
    else:
        if Password != re_password:
            return render(request, 'chat/Sign_In_3.html')
        else:
            l = []
            instance = user_data.objects.all()
            for index, name in enumerate(instance):
                uu = user_data.objects.filter(uid=name.uid)
                for i, k in enumerate(uu):
                    l.append(k.uid)
            for i in range(len(l)):
                t1 = Uid+l[i]
                t2 = l[i]+Uid
                df = pd.DataFrame(columns=list("ABC"))
                df.to_pickle('chat/pkl files/' + t1 + '.pkl')
                df.to_pickle('chat/pkl files/' + t2 + '.pkl')

            df = pd.read_pickle('chat/pkl files/All_user.pkl')
            df = df.append({'A':Uid},ignore_index=True)
            df.to_pickle('chat/pkl files/All_user.pkl')

            df2 = pd.DataFrame(columns=list('A'))
            df2.to_pickle('chat/pkl files/User_data/'+Uid+'.pkl')

            data[Uid] = 1
            database = user_data(uid=Uid,name=Name,email=Email,password=Password)
            database.save()
            return render(request, 'chat/index.html')


def qq(request):
    Uid = request.GET.get('1')
    Password = request.GET.get('2')
    m = []
    m.append(Uid)
    m.append(Password)
    return (m)


def index(request):
    Uid,Password = qq(request)
    data = defaultdict(str)
    instance = user_data.objects.all()
    # ss = []
    name_dict = {}
    for index, name in enumerate(instance):
        user = {}
        uu = user_data.objects.filter(uid=name.uid)
        for i, k in enumerate(uu):
            data[k.uid] = k.password
            if Uid != k.uid:
                name_dict[k.uid] = k.name

    try:
        All_user = pd.read_pickle('chat/pkl files/User_data/' + Uid + '.pkl')
    except:
        return render(request, 'chat/index_2.html')

    All_user_len = All_user.shape[0]
    # print(All_user_len)
    name_user = []
    for i in range(All_user_len):
        data1 = {}
        k = All_user.at[i, 'A']
        if k != Uid:
            data1['name'] = k
            data1['u1'] = name_dict[k]
            data1['Uid'] = Uid
        if len(data1) != 0:
            name_user.append(data1)

    if Password == data[Uid]:
        os.remove('chat/pkl files/Username.pkl')
        df = pd.DataFrame(columns=list('A'))
        df = df.append({'A':Uid},ignore_index=True)
        df.to_pickle('chat/pkl files/Username.pkl')

        df = pd.DataFrame(columns=list('A'))
        df.to_pickle('chat/pkl files/Logout.pkl')

        return render(request, 'chat/chat_room.html', {'ss':name_user,
                                                       'l':1}
                      )
    else:
        return render(request, 'chat/index_2.html')


def send(request):
    if not request.GET.get('search'):
        # k = ''
        # if request.GET.get('name'):
        #     k = request.GET.get('name')
        # elif request.GET.get('user'):
        k = request.GET.get('user')
        print(k)
        if not request.GET.get('q'):
            os.remove('chat/pkl files/User.pkl')
            df = pd.DataFrame(columns=['A'])
            df = df.append({'A': k}, ignore_index=True)
            df.to_pickle('chat/pkl files/User.pkl')

        pkl1 = pd.read_pickle('chat/pkl files/User.pkl')
        pkl2 = pd.read_pickle('chat/pkl files/Username.pkl')
        uid = pkl1.at[0,'A']
        Uid = pkl2.at[0,'A']

        instance = user_data.objects.all()
        name_dict = {}
        for index, name in enumerate(instance):
            uu = user_data.objects.filter(uid=name.uid)
            for i, k in enumerate(uu):
                if Uid != k.uid:
                    name_dict[k.uid] = k.name

        All_user = pd.read_pickle('chat/pkl files/User_data/'+Uid+'.pkl')

        All_user_len = All_user.shape[0]
        # print(All_user_len)
        name_user = []
        for i in range(All_user_len):
            data = {}
            k = All_user.at[i,'A']
            if k != Uid:
                data['name'] = k
                data['u1'] = name_dict[k]
            if len(data) != 0:
                name_user.append(data)

        p = Uid + uid
        p2 = uid + Uid

        if request.GET.get('q'):
            message = request.GET.get('q')
            df = pd.read_pickle('chat/pkl files/'+p+'.pkl')
            df = df.append({'A':p,'B':0,'C':message}, ignore_index=True)
            df.to_pickle('chat/pkl files/'+p+'.pkl')

            df2 = pd.read_pickle('chat/pkl files/' + p2 + '.pkl')
            df2 = df2.append({'A': p2, 'B': 1, 'C': message}, ignore_index=True)
            df2.to_pickle('chat/pkl files/' + p2 + '.pkl')

            df3 = pd.read_pickle('chat/pkl files/User_data/' + Uid + '.pkl')
            shape = df3.shape[0]
            co = defaultdict(int)
            for i in range(shape):
                co[df3.at[i,'A']] = 1
            if co[uid] != 1:
                df3 = df3.append({'A': uid}, ignore_index=True)
                df3.to_pickle('chat/pkl files/User_data/' + Uid + '.pkl')

            df4 = pd.read_pickle('chat/pkl files/User_data/' + uid + '.pkl')
            if co[uid] != 1:
                df4 = df4.append({'A': Uid}, ignore_index=True)
                df4.to_pickle('chat/pkl files/User_data/' + uid + '.pkl')

        l = []
        df = pd.read_pickle('chat/pkl files/'+p+'.pkl')
        # print(df)
        # print(pd.read_pickle('chat/pkl files/' + p2 + '.pkl'))
        n = df.shape[0]
        for i in range(n):
            d = {}
            if df.at[i, 'B'] == 0:
                d['u1'] = df.at[i, 'C']
            else:
                d['u2'] = df.at[i, 'C']
            l.append(d)

        # print(l)

        list = [{'name':uid}]
        # print(list)

        return render(request, 'chat/ch_data.html',{
            'list':l,
            'data':list,
            'ss':name_user,
        })
    elif request.GET.get('search'):
        se = request.GET.get('search')
        se = se.lower()
        pkl2 = pd.read_pickle('chat/pkl files/Username.pkl')
        Uid = pkl2.at[0, 'A']

        instance = user_data.objects.all()
        ss = []
        for index, name in enumerate(instance):
            user = {}
            uu = user_data.objects.filter(uid=name.uid)
            for i, k in enumerate(uu):
                if Uid != k.uid:
                    us = k.uid
                    us = us.lower()
                    nam = k.name
                    nam = nam.lower()
                    if se in us or se in nam:
                        user['name'] = k.uid
                        user['u1'] = k.name
            if len(user) != 0:
                ss.append(user)

        return render(request, 'chat/chat_room.html', {'ss': ss,
                                                       'l': 1}
                      )


def send_data(request):
    pkl2 = pd.read_pickle('chat/pkl files/Username.pkl')
    Uid = pkl2.at[0, 'A']

    if request.GET.get('All_Contact'):
        All_user = pd.read_pickle('chat/pkl files/All_user.pkl')
    else:
        All_user = pd.read_pickle('chat/pkl files/User_data/' + Uid + '.pkl')

    instance = user_data.objects.all()
    name_dict = {}
    for index, name in enumerate(instance):
        uu = user_data.objects.filter(uid=name.uid)
        for i, k in enumerate(uu):
            if Uid != k.uid:
                name_dict[k.uid] = k.name

    All_user_len = All_user.shape[0]
    # print(All_user_len)
    name_user = []
    for i in range(All_user_len):
        data = {}
        k = All_user.at[i, 'A']
        if k != Uid:
            data['name'] = k
            data['u1'] = name_dict[k]
        if len(data) != 0:
            name_user.append(data)

    return render(request, 'chat/chat_room.html', {
        'ss': name_user,
    })


def All_Contact(request):
    k = request.GET.get('name')
    print(k)
    return render(request, 'chat/home_2.html')