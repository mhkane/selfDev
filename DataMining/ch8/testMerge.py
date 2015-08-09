def merge(dic1,dic2):
    dic3 = {}
    assert len(dic1)>0
    assert len(dic2)>0
    for key in dic1.keys():
        if key in dic2:
            op1 = dic1[key][1]
            op2 = dic2[key][1]
            print dic1[key][0]
            print dic2[key][0]


            if op1<op2:
                dic3[key]=(dic1[key][0],op1)
            else:
                dic3[key]=(dic2[key][0],op2)
    return dic3 
dic1 = {}
dic2 = {}
dic1[1]=((0,1),1.0254481)
dic1[2]=((0,2), 0.463418)
dic1[3]=((0,3), 2.5212)
dic1[4]=((0,4), 2.417)
dic1[5]=((0,5), 1.317255)
dic2[0]=((0,8), 0.231)
dic2[1]=((1,8), 1.2550)
dic2[2]=((2,8), 0.69512)
dic2[3]=((3,8), 2.3065)
dic2[4]=((4,8), 2.6437)
print merge(dic1,dic2)