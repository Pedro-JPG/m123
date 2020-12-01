import csv

lista2=[' 0000006846258', '27273696', '38580090', '27273696', '38580090']
lista=[]
with open("test.txt", "r") as pfile:
    contenido=csv.reader(pfile, delimiter='|')
    valor=None
    for i in contenido:
        print i
        lista.append(i[4])
        if i[0]=='5':
            print i[3]

        if i[4] in lista2:
            print 'Si'
        if i[4] not in lista2:
            print 'No esta'
        # else:
        #     print "no encontre"
        # print i    



