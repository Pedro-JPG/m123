# -*- coding: utf_8 -*-

#import ipdb as pdb
import math
import base64
import datetime
import cPickle as pickle
import datetime
from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
import csv



class res_company(models.Model):
    _inherit = 'res.company'
    
    bps_id = fields.Char(string=u'Nro Bps')
    

class hr_employee(models.Model):
    _inherit = 'hr.employee'
    acum_laboral = fields.Integer(string='Acumulacion Laboral')
    bps_seg_salud = fields.Integer(string='Seguro de Salud')
    bps_fecha_ingreso = fields.Datetime(string='Fecha Ingreso')
    bps_tipo_contribucion = fields.Integer(string='Tipo Contribucion')
    bps_codigo_funcional = fields.Integer(string='Codigo funcional')
    bps_fecha_baja = fields.Datetime(string='Fecha Baja')




    

     
   

    


class dtm_importar_empleados_v10(models.TransientModel):

    _name = 'dtm.importar.empleados.v10'

    csv_data = fields.Binary(string='Archivo CSV', filters='*.csv')
    csv_ok = fields.Boolean(default=False)
    
    hrs_moves = fields.Text(string='Movimientos')
    pickle_empresa = fields.Text(string='empresa')
    pickle_empleados = fields.Text(string='empleados')
   

    
    empresa={'nroBps':None,
            'nroRut':None,
            'denominacion':None,
            'tipo_aportacion':None,
            'tipo_contribuyente':None,
            'direccion':None,
            'telefono':None,  
            }

    lista_personas=[]

    una_persona={'id':None,
                 'doc':None,
                 'pais_doc':None,
                 'acum_laboral':None,
                 'tipo_doc':None,
                 'primer_apellido':None,
                 'segundo_apellido':None,
                 'primer_nombre':None,
                 'segundo_nombre':None,
                 'seg_salud':None,
                 'fecha_nacimiento':None,
                 'sexo':None,
                 'nacionalidad':None,
                 'fecha_ingreso':None,
                 'tipo_remuneracion':None,
                 'horas_semanales':None,
                 'vinculo_funcional':None,
                 'cod_exoneracion':None,
                 'computos_especiales':None,
                 'causal_baja':None,
                 'fecha_baja':None
                 }
    
    id_personas=[]


    @api.onchange('csv_data')
    def _onchange_csv_data(self):
        nro_linea=0

        if self.csv_data:
            self.csv_ok = True
            
            #with open("test.txt", "r") as pfile:
            #contenido=csv.reader(pfile,delimiter='|')
            largos_indices_archivo = {

                "1": 10,
                "4": 6,
                "5": 11,
                "6": 20,
                "7":10,
                "12":7

            }
                # if (len(i) == largos[i[0]])

            contenido = base64.b64decode(self.csv_data)
            contenido = contenido.splitlines()
            
            for i in contenido:

                # Contabilizar
                nro_linea += 1

                i=i.split('|')

                #controlo que el indice de la linea
                
                if (len(i) == largos_indices_archivo[i[0]]):

                    

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
                                 'cod_exoneracion':i[10],
                                 'computos_especiales':i[11],
                                 'causal_baja':i[18],
                                 'fecha_baja':i[19]
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
                                a['computos_especiales']=i[11]
                                a['causal_baja']=i[18]
                                a['fecha_baja']=i[19]
                                     
                                


                    if i[0]=='7' and i[4] in self.id_personas:
                        pass
                else:
                    raise Warning ('Se encontraron errores en archivo Atyr, Nro de linea',nro_linea, 'detalle de linea: ', i) 
        # print 'lista de IDS', self.id_personas

        #serializo los datos con pickle
        self.pickle_empleados = pickle.dumps(self.lista_personas)
        self.pickle_empresa = pickle.dumps(self.empresa)


       


    @api.multi
    def import_info_empresa(self):

        #obtengo los datos serializados
        total_personas=pickle.loads(str(self.pickle_empleados))
        datos_empresa=pickle.loads(str(self.pickle_empresa))

        
        #da el caso que "tipo de aportacion" solo el 01 esta de dos digitos desp todos con un digito
        aux_emp = str(datos_empresa['tipo_aportacion'])
        if aux_emp=='1':
            aux_emp='01'

        #formateo el valor de tipo de aportacion 2 -> 02 ya que en las tablas esta como string y en dos digitos
        aux_contrib = str('%02d' % int(datos_empresa['tipo_contribuyente'])) 
                
        
        #obtengo los ids de tipo_aportacion y nro Contribuyente
        
        #sql_contrib_y_codAport= '''
        #  SELECT t.id as id_tipoContrib, a.id id_Aportacion
        #   from hr_uy_bps_taxpayer_type t
        #   inner join  hr_uy_bps_contributions_type a
        #   on t.link_cont=a.id
        #   where a.contribution_code= %(cod_contribucion)s and t.code_type_of_taxpayer= %(tipo_aportacion)s
            
        #'''
       
        #self.env.cr.execute(sql_contrib_y_codAport,{'cod_contribucion': aux_emp, 'tipo_aportacion':aux_contrib})
        #res = self.env.cr.fetchall()

        #obtengo el tipo de contribuyente y tipo de aportacion del SQL
        #id_tipoContribuyente=res[0][0]
        #id_aportacion=res[0][1]

        #obtengo la descripcion de la empresa
        #legal_nature =self.env['hr.uy.bps.legal.nature'].search([('code_of_legal_nature','=',datos_empresa['tipo_contribuyente'])])
        #id_legal_nature= legal_nature.id
        
        #concateno UY al rut, ya que ODOO lleva el UY delante del RUT
        vat='UY'+str(int(datos_empresa['nroRut']))

            

        carga_empresa={
        'id':2,
        'bps_id': datos_empresa['nroBps'],
        'name': datos_empresa['denominacion'],
        #'contribution_id':id_aportacion,
        #'taxpayer_id':id_tipoContribuyente,
        #'legal_nature': id_legal_nature,
        'street':datos_empresa['direccion'],
        'phone':datos_empresa['telefono'],
        'vat':vat,
        'rml_paper_format': 'a4',
        'currency_id':47,
        'paperformat_id':1,
        'tax_calculation_rounding_method':'round_per_line',
         }


        #Sobreescribo los datos de la Empresa creada por defecto
        self.env['res.company'].browse(1).write(carga_empresa)

        #recorro el listado de diccionarios de personas
        for i in total_personas:
            
            #Algunos valores necesitan ser formateados
            td=i['tipo_doc']
            if i['tipo_doc']=='DO':
                td='CI'
            name_related=i['primer_apellido']+" "+i['segundo_apellido']+" "+i['primer_nombre']+" "+i['segundo_nombre']

            #Busco en la base de datos el id que le pertenece al seguro de salud correspondiente al Empleado
            #self.env.cr.execute('SELECT id from hr_uy_bps_health_insurance where health_insurance_code = %(cod_salud)s',{'cod_salud': i['seg_salud']})
            #ss=self.env.cr.fetchall()
            #seg_salud=ss[0][0]
            
            #Busco en la base de datos el id sino esta las hs las creo
            #hs_sem=None
            #self.env.cr.execute('SELECT id from hr_uy_hours_per_week where hour=%(cant_hs_semanal)s',{'cant_hs_semanal': i['horas_semanales']})
            #hs=self.env.cr.fetchall()
            
            #if hs !=[]:
            #    hs_sem=hs[0][0]
            #if hs == []:
            #    self.env.cr.execute('INSERT INTO hr_uy_hours_per_week (hour, create_uid, write_uid) VALUES (%(cant_hs_semanal)s,1,1)',{'cant_hs_semanal': i['horas_semanales']})
            #    self.env.cr.execute('SELECT id from hr_uy_hours_per_week where hour=%(cant_hs_semanal)s',{'cant_hs_semanal': i['horas_semanales']})
            #    hs=self.env.cr.fetchall()
            #    hs_sem=hs[0][0]
               

            #busco el id del Vinculo funcional para el nro de vinculo funcional que tiene el empleado
            #self.env.cr.execute('SELECT id from hr_uy_bps_functional_link where functional_code_link=%(vf)s',{'vf': i['vinculo_funcional']})
            #sql_vf=self.env.cr.fetchall()
            #vf=sql_vf[0][0]
            
            #busco el id para tipo de contribuccion 
            #self.env.cr.execute('SELECT id from hr_uy_bps_exemption_of_contribution where exemption_code=%(cod_ex)s',{'cod_ex':i['cod_exoneracion']})
            #sql_cod_ex=self.env.cr.fetchall()
            #cod_ex=sql_cod_ex[0][0]
           
             #busco el id para computo especial
            #self.env.cr.execute('SELECT id from hr_uy_bps_special_computing where computing_code=%(com_esp)s',{'com_esp':i['computos_especiales']})
            #sql_com_esp=self.env.cr.fetchall()
            #com_esp=sql_com_esp[0][0]

             #Creo un departamento por defecto ya que el campo departamento es requerido
            #self.env.cr.execute("INSERT INTO HR_DEPARTMENT (create_uid, create_date, name, company_id, write_uid, write_date) Values (1,current_timestamp, 'Servicio',1,1,current_timestamp)")
            

            #formateo de fechas para cargar a la base
            nac= datetime.datetime.strptime(i['fecha_nacimiento'], '%d%m%Y')
            fecha_nac=nac.strftime("%Y-%m-%d")
            

            ingreso=datetime.datetime.strptime(i['fecha_ingreso'], '%d%m%Y')
            fecha_ing=ingreso.strftime("%Y-%m-%d")
            
            hoy=datetime.datetime.now()

            fecha_baja=None
            baja=None
            if i['fecha_baja']:
                baja=datetime.datetime.strptime(i['fecha_baja'], '%d%m%Y')
                fecha_baja=baja.strftime("%Y-%m-%d")
                   

            


            carga_persona= {
                     'create_date':hoy,
                     'children':0,
                     'identification_id':i['doc'],
                     'country_id':i['pais_doc'],      #NTEGER
                     'acum_laboral':i['acum_laboral'],    #integer "LaborAccumulation"
                     # 'tipo_de_documento':td,
                     # 'first_name':i['primer_nombre'],
                     # 'second_name' :i['segundo_nombre'],
                     # 'first_surname':i['primer_apellido'],
                     # 'second_surname':i['segundo_apellido'],
                     'name':name_related,
                     'bps_seg_salud':i['seg_salud'],
                     'birthday':fecha_nac,
                     # 'nacimiento':fecha_nac,
                     'gender_id':i['sexo'],     #Integer
                     # 'nationality':i['nacionalidad'],  #INTEGER
                     # 'country_of_birth':i['nacionalidad'], #INTEGER
                     'bps_fecha_ingreso':fecha_ing,
                     'bps_tipo_contribucion':i['tipo_remuneracion'], #INTEGER
                     'bps_codigo_funcional':i['vinculo_funcional'],
                     # 'ContributionsExoneration':cod_ex,
                     # 'job_company':1,
                     # 'bps_category_type':'1',
                     # 'employee_journal_h':8,
                     # 'SpecialComputing':com_esp,
                     # 'termination_code':i['causal_baja'], #integer,
                     'bps_fecha_baja':fecha_baja,

                    }
                

            
            # print carga_persona
            self.env['hr.employee'].create(carga_persona)

            

        # print 'total personas', total_personas
        print 'Carga procesada' 

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'action_warn',
        #     'name': 'Notificación',
        #     'params': {
        #         'title': 'Importacion de Empresa y sus Empleados',
        #         'text': 'LA IMPORTACION SE REALIZO CORRECTAMENTE.',
        #         'sticky': False
        #     }
        #     }



