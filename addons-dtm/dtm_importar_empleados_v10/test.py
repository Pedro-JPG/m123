import math
import base64
import datetime
import cPickle as pickle
import csv
import re

class nomina:
    acum_laboral=int
    pais_doc=str
    tipo_doc=None
    doc=int
    primer_apellido=str
    segundo_apellido=str
    primer_nombre=str
    segundo_nombre=str
    seg_salud=int
    fecha_nacimiento=None
    sexo=int
    nacionalidad=int
    fecha_ingreso=None
    tipo_remuneracion=int
    horas_semanales=int
    vinculo_funcional=int
    cod_exoneracion=int
    aux=None
    
    empresa={'nroBps':None,
            'nroRut':None,
            'denominacion':None,
            'tipo_contribuyente':None,
            'direccion':None,
            'telefono':None,  
            }

    lista_personas=[]

    una_persona={'id':doc,
                 'doc':doc,
                 'pais_doc':pais_doc,
                 'acum_laboral':acum_laboral,
                 'tipo_doc':tipo_doc,
                 'primer_apellido':primer_apellido,
                 'segundo_apellido':segundo_apellido,
                 'primer_nombre':primer_nombre,
                 'segundo_nombre':segundo_nombre,
                 'seg_salud':seg_salud,
                 'fecha_nacimiento':fecha_nacimiento,
                 'sexo':sexo,
                 'nacionalidad':nacionalidad,
                 'fecha_ingreso':fecha_ingreso,
                 'tipo_remuneracion':tipo_remuneracion,
                 'horas_semanales':horas_semanales,
                 'vinculo_funcional':vinculo_funcional,
                 'cod_exoneracion':cod_exoneracion
                }
    id_personas=[]
    
    def carga_datos(self):
        
        # with open("nom_para pruebas.txt", "r") as pfile:
        with open("nom.txt", "r") as pfile:
            
            contenido=csv.reader(pfile,delimiter='|')
        
            valor=None
        
            for i in contenido:
                if i[0]=='1':
                    self.empresa={'nroBps':i[4],
                                    'nroRut':i[5],
                                    'tipo_aportacion':i[6],
                                    'denominacion':i[7],
                                    'direccion':i[8],
                                    'telefono':i[9],  
                                       }

                if i[0]=='4':
                    self.empresa['tipo_contribuyente']=i[2]

                
                if i[0]=='5' and i[3] in self.id_personas:
                    
                    for a in self.lista_personas:
                        print 'ingreso al 5 exitiendo usr ya', i 
                        print  'valor de a', a

                        if(i[3]==a['id']):
                            a['id']=i[3]
                            a['doc']=i[3]
                            a['pais_doc']=i[1]
                            a['tipo_doc']=i[2]
                            a['primer_apellido']=i[4]
                            a['segundo_apellido']=i[5]
                            a['primer_nombre']=i[6]
                            a['segundo_nombre']=i[7]
                            a['fecha_nacimiento']=i[8]
                            a['sexo']=i[9]
                            a['nacionalidad']=i[10]
                        


                if i[0]=='5' and i[3] not in self.id_personas:
                    
                    una_persona={'id':i[3],
                                 'doc':i[3],
                                 'pais_doc':i[1],
                                 #'acum_laboral':acum_laboral,
                                 'tipo_doc':i[2],
                                 'primer_apellido':i[4],
                                 'segundo_apellido':i[5],
                                 'primer_nombre':i[6],
                                 'segundo_nombre':i[7],
                                 'fecha_nacimiento':i[8],
                                 'sexo':i[9],
                                 'nacionalidad':i[10]
                                }

                    self.lista_personas.append(una_persona)
                    self.id_personas.append(i[3])

                if i[0]=='6' and i[4] not in self.id_personas:
                    #6||1|DO|27273696|1|19102018|1|8|12|10.9|99||||30|0|16||
                    print 'al 6 y not in ',i
                    una_persona={'id':i[4],
                                'doc':i[4],
                                 'pais_doc':i[2],
                                 'acum_laboral':i[5],
                                 'tipo_doc':i[3],
                                 'seg_salud':i[17],
                                 #'fecha_nacimiento':i[8],
                                 #'sexo':sexo,
                                 #'nacionalidad':nacionalidad,
                                 'fecha_ingreso':i[6],
                                 'tipo_remuneracion':i[7],
                                 'horas_semanales':i[8],
                                 'vinculo_funcional':i[9],
                                 'cod_exoneracion':i[10]
                                }
                    self.lista_personas.append(una_persona)
                    self.id_personas.append(i[4])

                if i[0]=='6' and i[4] in self.id_personas:
                    #6||1|DO|27273696|1|19102018|1|8|12|10.9|99||||30|0|16||
                    for a in self.lista_personas:
                        if i[4] == a['id']:
                            
                            a['acum_laboral']=i[5]
                            a['fecha_ingreso']=i[6]
                            a['tipo_remuneracion']=i[7]
                            a['horas_semanales']=i[8]
                            a['vinculo_funcional']=i[9]
                            a['cod_exoneracion']=i[10]
                            a['seg_salud']=i[17]
                

                
                if i[0]=='7' and i[4] in self.id_personas:
                    pass

        # print 'datos de la Empresa: ', self.empresa
        print 'ID de las Personas', self.id_personas
        print 'Lista de Personas: ', self.lista_personas
        

                   
        

    # def test(self):
    #     aa=open("test.txt", "r")
    #     mensaje=aa.read()
    #     mensaje=str(mensaje)
    #     mensaje.split("|")
    #     print mensaje
    #     aa.close()
        
si=nomina()
si.carga_datos()
