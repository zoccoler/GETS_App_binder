#!/usr/bin/env python
# coding: utf-8

# ## Funções de tratamento da lista de equipamentos

# In[2]:


def load_equip_data(file_path_list):
    import pandas as pd
    import os
    lista_eqp_list = []
    for file_path in file_path_list:
        lista_eqp = pd.read_excel(file_path,skiprows=3,header=2,dtype={'Patrimônio': str, 'Tipo Equipamento': str})
        lista_eqp = lista_eqp.drop(['Localização','Modelo','Fornecedor','Núm. Doc. da Aquisição','Nota Fiscal','Garantia',
                                'Parecer Desativação','Contrato','Vida Útil','Equipamento Crítico',
                                   'Descrição Complementar'], axis=1)
        lista_eqp['Aquisição'] = pd.to_datetime(lista_eqp['Aquisição'],dayfirst=True)
        lista_eqp['Data Desativação'] = pd.to_datetime(lista_eqp['Data Desativação'],dayfirst=True)
        lista_eqp.sort_values(by=['Aquisição'], inplace=True)
        lista_eqp_list.append(lista_eqp)
    lista_eqp = pd.concat(lista_eqp_list,ignore_index=True)
    lista_eqp.drop_duplicates(inplace=True)
    return(lista_eqp)


# In[3]:


def clean_equip_data(lista_eqp):
    import pandas as pd
    # Delete invalid dates ( =-1, which is equivalent to dates before 1900)
    lista_eqp = lista_eqp.drop(lista_eqp[lista_eqp['Aquisição'] < pd.to_datetime(1900, format='%Y')].index)
    
    # Delete equipments with 'DESATIVADO=SIM' AND without disable date
    lista_eqp = lista_eqp.drop(lista_eqp[(lista_eqp['Desativado']=='SIM') & (pd.isna(lista_eqp['Data Desativação']))].index)
    
    # Delete equipments tagged with 'DESATIVADO=NÃO' AND without disable date AND also tagged with 'BAIXADO=SIM'
    lista_eqp = lista_eqp.drop(lista_eqp[(lista_eqp['Desativado']=='NÃO') & (pd.isna(lista_eqp['Data Desativação'])) & ((lista_eqp['Baixado']=='SIM'))].index)
    
    
    # Consider active (i.e., remove disable date) equipments tagged with 'DESATIVADO=NÃO' AND 'BAIXADO=NÃO', even if they have disable date 
    # Flags for filtering
    is_not_disabled = lista_eqp['Desativado']=='NÃO'
    is_not_down = lista_eqp['Baixado']=='NÃO'
    has_disable_date = pd.notna(lista_eqp['Data Desativação']) 
    lista_eqp.loc[lista_eqp[is_not_disabled & has_disable_date & is_not_down].index , ['Data Desativação']] = pd.NaT
    
    #Consider active equipments tagged with 'DESATIVADO=SIM', AND that have an disable date, 
    #     AND tagged with 'PERMITIR O.S.=SIM', AND tagged with 'BAIXADO=NÃO'
    # Flags for filtering
    is_disabled = lista_eqp['Desativado']=='SIM'
    has_disable_date = pd.notna(lista_eqp['Data Desativação'])
    allow_OS = lista_eqp['Permitir O.S.']=='SIM'
    is_not_down = lista_eqp['Baixado']=='NÃO'
    lista_eqp.loc[lista_eqp[(is_disabled & has_disable_date & allow_OS & is_not_down)].index,['Data Desativação']] = pd.NaT
    
    return(lista_eqp)


# In[4]:


def arrange_equip_data(lista_eqp):
    import pandas as pd
    import numpy as np
    # Copy dataframe
    lista_eqp2 = lista_eqp.copy()
    # On original dataframe, create column 'Ativo' (with Trues) and renames column 'Aquisição' as 'Data'
    lista_eqp.loc[:,'Ativo'] = np.ones(len(lista_eqp),dtype=bool)
    lista_eqp.rename(columns={'Aquisição':'Data'}, inplace=True)
    # On dataframe copy, remove active equipments and creates column 'Ativo' (with Falses)
    # also removes column 'Aquisição' and renames column 'Data Desativação' as 'Data'
    lista_eqp2 = lista_eqp2[pd.notna(lista_eqp2['Data Desativação'])]
    lista_eqp2.loc[:,'Ativo'] = np.zeros(len(lista_eqp2),dtype=bool)
    lista_eqp2 = lista_eqp2.drop(['Aquisição'], axis=1)
    lista_eqp2.rename(columns={'Data Desativação':'Data'}, inplace=True)
    # Concatenates original and copy
    double_lista_eqp = pd.concat([lista_eqp,lista_eqp2],sort=True)
    # Redesign indexes as double indexes 'Data' and 'Patrimônio'
    double_lista_eqp = double_lista_eqp.set_index(['Data','Patrimônio'])
    double_lista_eqp = double_lista_eqp.sort_index()
    # Remove duplicates
    double_lista_eqp = double_lista_eqp[~double_lista_eqp.index.duplicated()]
    
    return(double_lista_eqp)


# In[5]:


def get_all_equips_data(file_path_list):
    df = load_equip_data(file_path_list)
    df = clean_equip_data(df)
    df = arrange_equip_data(df)
    return(df)


# In[6]:


def get_equip_amount(df,equip,start_date=0, end_date=10):
    import pandas as pd
    import numpy as np

    selected_equip = df['Tipo Equipamento']==equip[0]
    for eq in equip:
        selected_equip = (selected_equip) | (df['Tipo Equipamento']==eq)
    acquired = df['Ativo']==True
    deactivated = df['Ativo']==False
    
    equip_acquired_cumsum = (selected_equip & acquired).cumsum()
    equip_deactivated_cumsum = (selected_equip & deactivated).cumsum()
    
    equip_amount = equip_acquired_cumsum - equip_deactivated_cumsum
    equip_amount_data = df[selected_equip].copy()
    equip_amount_data.loc[:,'Quantidade de Equipamentos'] = equip_amount
    # Sort dates in accending order
    equip_amount_data.sort_index(level=0,inplace=True)
    return(equip_amount_data)


# ## Funções de tratamento das OS Encerradas

# In[8]:


def load_OS_data(closed_OS_path_list):
    import pandas as pd
    import numpy as np
    whole_data = []
    for file_path in closed_OS_path_list:
        closed_OS = pd.read_excel(file_path,skiprows=3,header=2,dtype={'Núm. O.S.': str, 'Tipo Equip.':str, 'Patrimônio': str, 'Tempo SOS-OSP (horas)':np.float64})
        closed_OS = closed_OS.drop(['Grupo','Programa MP','Modelo','Duração (dias)','Equipamento Crítico',
                               'Tempo SOS-OSP (dias)','Indisponibilidade (dias)'], axis=1)
        closed_OS['Abertura'] = pd.to_datetime(closed_OS['Abertura'],dayfirst=True)
        closed_OS['Encerramento'] = pd.to_datetime(closed_OS['Encerramento'],dayfirst=True)
        closed_OS.sort_values(by=['Abertura'], inplace=True)
        closed_OS.loc[closed_OS['Tempo SOS-OSP (horas)']==0, 'Tempo SOS-OSP (horas)'] = 1/60
        whole_data.append(closed_OS)
    whole_data = pd.concat(whole_data,ignore_index=True)
    whole_data.drop_duplicates(inplace=True)

    return(whole_data)


# # Função de tratamento de OS Pendente

# In[ ]:


def load_open_OS_data(df,open_OS_path):
    import pandas as pd
    import numpy as np
    import os

    open_OS = pd.read_excel(open_OS_path,skiprows=3,header=2,dtype={'Num.': str, 'Patrimônio': str, 'Estado':str})
    open_OS = open_OS.drop(['Núm.Orgão','N. Série','Grupo','Marca','Modelo','No Nec','Equipamento Crítico'], axis=1)
    # Put dates in the right format
    open_OS['Dt. Abertura'] = pd.to_datetime(open_OS['Dt. Abertura'],dayfirst=True)
    open_OS['Dt. Última Transição'] = pd.to_datetime(open_OS['Dt. Última Transição'],dayfirst=True)
    open_OS.sort_values('Dt. Abertura', inplace=True)
    
    # Find OS that are ready to treat separatedly
    OS_ready = open_OS['Estado']=='OSP - OS Pronta'
    open_OS = open_OS.drop(['Estado'], axis=1)
    # Create column 'Processada' (with Falses) (at first treat all OS as unfinished)
    open_OS.loc[:,'Processada'] = np.zeros(len(open_OS),dtype=bool)
    # Create a copy with just the OS that are ready
    open_OS_ready = open_OS.loc[OS_ready].copy()
    # Change status of column 'Processada' to True in this copy and redefines 'Dt. Abertura' as 'Dt. Última Transição'
    open_OS_ready.loc[:,'Processada'] = True
    open_OS_ready.loc[:,'Dt. Abertura'] = open_OS_ready.loc[:,'Dt. Última Transição']
    #################################
    #### Now, in both dataframes ####
    # Insert new column 'Encerramento' (empty), but attribute 'Dt. Última Transição' to OS that are ready
    open_OS.insert(4,'Encerramento','')
    open_OS.loc[OS_ready,'Encerramento'] = open_OS.loc[OS_ready,'Dt. Última Transição']
    open_OS_ready.insert(4,'Encerramento','')
    open_OS_ready.loc[:,'Encerramento'] = open_OS_ready.loc[:,'Dt. Última Transição']
    # Insert new column 'Classe' (with 'Manutenção Corretiva'). Obs: tha excel table was generated with the 
    #    filter 'Manutenção Corretiva', so all OS's should be of this class
    open_OS.insert(1,'Classe','Manutenção Corretiva')
    open_OS_ready.insert(1,'Classe','Manutenção Corretiva')
    # delete the column 'Dt. Última Transição' (not necessary anymore) and renames some column to match those of the 
    #    closed_OS dataframe
    open_OS = open_OS.drop(['Dt. Última Transição'], axis=1)
    open_OS_ready = open_OS_ready.drop(['Dt. Última Transição'], axis=1)
    open_OS.rename(columns={"Num.": "Núm. O.S.", "Dt. Abertura": "Abertura"},inplace=True)
    open_OS_ready.rename(columns={"Num.": "Núm. O.S.", "Dt. Abertura": "Abertura"},inplace=True)
    ################################
    # Concatenate closed_OS dataframe with open_OS and open_OS_ready dataframes
    df = pd.concat([df,open_OS,open_OS_ready],ignore_index=True)
    return(df)


# # Organiza dados de OS (junta pendente com fechada e trata dados de duração de OS)

# In[9]:


def arrange_OS_data(whole_data,open_OS_path_list):
    import pandas as pd
    import numpy as np
    # Copy dataframe
    whole_data2 = whole_data.copy()
    whole_data3 = whole_data.copy()
    # On original dataframe, create column 'Processada' (with Falses)
    whole_data.loc[:,'Processada'] = np.zeros(len(whole_data),dtype=bool)
    # load open_OS data and concatenate it with original dataframe (whole_data, which contains closed OS's)
    whole_data = load_open_OS_data(whole_data,open_OS_path_list[0])
    # On copy, changes date 'Abertura' to the moment when the OS was processed
    whole_data2['Abertura'] = whole_data2['Abertura'] + pd.to_timedelta(whole_data2['Tempo SOS-OSP (horas)'], unit='h')
    # On copy, create column 'Processada' (with Trues)
    whole_data2.loc[:,'Processada'] = np.ones(len(whole_data2),dtype=bool)
    # Concatenate data
    double_whole_data = pd.concat([whole_data,whole_data2])
    # Renames column 'Abertura' as 'Data'
    double_whole_data.rename(columns={'Abertura':'Data'}, inplace=True)
    # Redesign indexes as double indexes 'Data' and 'Núm. O.S.'
    double_whole_data = double_whole_data.set_index(['Data','Núm. O.S.'])
    # Sort dates in accending order
    double_whole_data = double_whole_data.sort_index()
    # Remove duplicates (I downloaded the same day twice somewhere)
    double_whole_data = double_whole_data[~double_whole_data.index.duplicated()]
    
    ## Arrange data for OS duration ##
    # Change 'Abertura' date to OS processed date
    whole_data3['Abertura'] = whole_data3['Abertura'] + pd.to_timedelta(whole_data3['Tempo SOS-OSP (horas)'], unit='h')
    # Rename 'Abertura' (which is now processed date) to 'Data'
    whole_data3.rename(columns={'Abertura':'Data'}, inplace=True)
    # Drop 'Encerramento' (not used for OS duration because we use duration from openning to processed)
    whole_data3 = whole_data3.drop(['Encerramento'],axis=1)
    # Set index to 'Data' and 'Núm O.S.'
    whole_data3 = whole_data3.set_index(['Data','Núm. O.S.'])
    # Sort index by date (when equal dates, sort by 'Núm OS' string)
    whole_data3 = whole_data3.sort_index()
    # Drop duplicated items (same date and same 'Núm O.S.')
    whole_data3 = whole_data3[~whole_data3.index.duplicated()]
    # Remove 'Núm O.S.' from index (leave just the dates as index now)
    whole_data3 = whole_data3.reset_index(level=['Núm. O.S.'])
    
    return(double_whole_data, whole_data3)


# In[10]:


def get_all_OS_data(closed_OS_path_list,open_OS_path_list):
    df = load_OS_data(closed_OS_path_list)
    df, df2 = arrange_OS_data(df,open_OS_path_list)
    return(df, df2)


# In[11]:


def get_equip_break_rate(df,equip,start_date=0, end_date=10):
    import pandas as pd
    import numpy as np
    selected_equip = df['Tipo Equip.']==equip[0]
    for eq in equip:
        selected_equip = (selected_equip) | (df['Tipo Equip.']==eq)

    maintenance_type = 'Manutenção Corretiva'
    selected_maintenance = df['Classe']==maintenance_type
    opened = df['Processada']==False
    closed = df['Processada']==True

    OS_opened_cumsum = (selected_equip & selected_maintenance & opened).cumsum()
    OS_processed_cumsum = (selected_equip & selected_maintenance & closed).cumsum()

    break_rate = OS_opened_cumsum - OS_processed_cumsum
    break_rate_data = df[selected_equip & selected_maintenance].copy()
    if break_rate_data.empty==False:
        break_rate_data['Taxa de Quebra'] = break_rate
    return(break_rate_data)


# In[ ]:


def get_equip_OS_duration(equip,df):
    import pandas as pd
    import numpy as np
    selected_equip = df['Tipo Equip.']==equip[0]
    for eq in equip:
        selected_equip = (selected_equip) | (df['Tipo Equip.']==eq)

    maintenance_type = 'Manutenção Corretiva'
    selected_maintenance = df['Classe']==maintenance_type
    
    duration_data = df[selected_equip & selected_maintenance]
    return(duration_data)


# ## Função de aquisição de equipamentos totais e disponíveis

# In[12]:


def get_available_equip(selected_equip,equips_data,OS_data):
    import pandas as pd
    import numpy as np
    # get selected equipment amount (over time)
    equip_amount_data = get_equip_amount(equips_data,selected_equip)
    
    # get selected equipment break rate (over time)
    break_data = get_equip_break_rate(OS_data,selected_equip)
        
    # Replaces content of columns 'Ativo' and 'Processada' by 1 (when equipment is acquired or fixed) or -1 (when equipment
    #       is disabled or broken)
    dates1 = equip_amount_data.index.get_level_values(0)
    amounts = equip_amount_data['Ativo'].astype(int)
    amounts[amounts==0] = -1
    
    if break_data.empty:
        available_equips = pd.concat([amounts])
        available_equips.rename(0, inplace=True)
    else:
        dates2 = break_data.index.get_level_values(0)
        breaks = break_data['Processada'].astype(int)
        breaks[breaks==0] = -1
        #concatenate data
        available_equips = pd.concat([amounts,breaks])
    #removes second index and sort by date
    available_equips = available_equips.reset_index(level=[1])
    available_equips = available_equips.drop(['Patrimônio'],axis=1)
    available_equips.sort_index(inplace=True)
    # Adds a new column 'Quantidade Disponível' with the cumulative sum
    available_equips.loc[:,'Quantidade Disponível'] = available_equips.cumsum()[0]
    return(available_equips,equip_amount_data,break_data)


# In[13]:


def arrange_equip_data_to_plot(available_equips,equip_amount_data,start_date,end_date):
    import pandas as pd
    import numpy as np
    
    x_data1 = equip_amount_data.index.get_level_values(0).values
    y_data1 = equip_amount_data['Quantidade de Equipamentos'].values.astype(int)
    first_record = x_data1[0]
    
    x_data2 = available_equips.index.values
    y_data2 = available_equips['Quantidade Disponível'].values.astype(int)

    return(x_data1,y_data1,x_data2,y_data2)


# In[ ]:


def check_for_empty_data(df,start_date,end_date):
    import pandas as pd
    import numpy as np
    # Checks if dataframe is single index or multiindex
    if isinstance(df.index, pd.MultiIndex): 
        after_start_date = df.index.get_level_values(0) >= start_date
        before_end_date = df.index.get_level_values(0) <= end_date
        between_two_dates = after_start_date & before_end_date
        empty_flag = df[between_two_dates].index.get_level_values(0).empty
    else:
        after_start_date = df.index >= start_date
        before_end_date = df.index <= end_date
        between_two_dates = after_start_date & before_end_date
        empty_flag = df[between_two_dates].index.empty
    return(empty_flag,between_two_dates)


# # Funções de aquisição de custo de material

# In[1]:


def load_material_cost_data(material_path_list):
    import pandas as pd
    import os
    material_cost_data_list = []
    for file_path in material_path_list:
        material_cost_data = pd.read_excel(file_path,skiprows=3,header=2)
        material_cost_data['Data Saida'] = pd.to_datetime(material_cost_data['Data Saida'],dayfirst=True)
        material_cost_data.sort_values(by=['Data Saida'], inplace=True)  
        material_cost_data_list.append(material_cost_data)
    material_cost_data = pd.concat(material_cost_data_list,ignore_index=True)
    material_cost_data.drop_duplicates(inplace=True)
    material_cost_data.set_index(['Data Saida'],inplace=True)
    return(material_cost_data)


# In[ ]:


def load_external_cost_data(external_path_list):
    import pandas as pd
    import os   
    external_cost_data_list = []
    for file_path in external_path_list:
        external_cost_data = pd.read_excel(file_path,skiprows=3,header=2)
        external_cost_data['Data Encerramento'] = pd.to_datetime(external_cost_data['Data Encerramento'],dayfirst=True)
        external_cost_data.sort_values(by=['Data Encerramento'], inplace=True)  
        external_cost_data_list.append(external_cost_data)
    external_cost_data = pd.concat(external_cost_data_list,ignore_index=True)
    external_cost_data.drop_duplicates(inplace=True)
    external_cost_data.set_index(['Data Encerramento'],inplace=True)
    return(external_cost_data)


# In[1]:


def load_ipca(ipca_path_list):
    import pandas as pd
    import os
    ipca_list = []
    for file_path in ipca_path_list:
        ipca = pd.read_excel(file_path,skiprows=3,header=0,skipfooter=1).T
        new_header = ipca.iloc[0] #grab the first row for the header
        ipca = ipca[1:] #take the data except the header row
        ipca.columns = new_header #set the header row as the df header
        ipca.dropna(inplace=True)
    #     import dateparser
    #     ipca.index = ipca.index.map(dateparser.parse)
        from datetime import datetime
        dict_month_pt = {'janeiro':'1','fevereiro':'2','março':'3','abril':'4','maio':'5','junho':'6','julho':'7','agosto':'8',
                            'setembro':'9','outubro':'10','novembro':'11','dezembro':'12'}
        new_indexes = []
        for c,idx in enumerate(ipca.index):
            for mes,number in dict_month_pt.items():
                idx = idx.replace(mes, number)
            new_indexes.append(datetime.strptime(idx, '%m %Y'))
        ipca.index = new_indexes

        ipca.reset_index(inplace=True)
        ipca = ipca.rename(columns = {'index':'Data'})
        ipca_list.append(ipca)
    ipca = pd.concat(ipca_list)
    ipca.drop_duplicates(inplace=True)
    ipca.dropna(inplace=True)
    ipca.set_index(['Data'],inplace=True)
    ipca = ipca.squeeze()
    return(ipca)


# In[2]:


def get_equip_monthly_cost(equip,cost_data,ipca):
    import dateparser
    import pandas as pd
    lacking_inflation_corr = True
    try:
        selected_equip = cost_data['Tipo Equipamento']==equip[0]
        for eq in equip:
            selected_equip = (selected_equip) | (cost_data['Tipo Equipamento']==eq)
    except:
        selected_equip = cost_data['Tipo']==equip[0]
        for eq in equip:
            selected_equip = (selected_equip) | (cost_data['Tipo']==eq)
        
    cost = cost_data[selected_equip]['Custo']
    cost = cost.sort_index()
    monthly_cost = cost.groupby(pd.Grouper(freq="M")).sum()  # DataFrameGroupBy (grouped by Month start frequency)
    
    if (not ipca.empty) & (not monthly_cost.empty):
        lacking_inflation_corr = False
        diff_days = pd.Timestamp(monthly_cost.index[-1].strftime('%Y-%m')) - pd.Timestamp(ipca.index[-1].strftime('%Y-%m'))

        if (diff_days>=pd.Timedelta(28,'D')) & (diff_days<=pd.Timedelta(31,'D')):

            ipca = ipca.append(ipca.tail(1))

            as_list = ipca.index.tolist()
            as_list[-1] = monthly_cost.index[-1]
            ipca.index = as_list

        for idx in monthly_cost.index.strftime('%B %Y'):
            #if ipca contains the corresponding month/year -> correct inflation in that month/year
            if ipca.index.strftime('%B %Y').str.contains(idx).any():
                monthly_cost[idx] *= ipca[-1]/ipca[ipca.index.strftime('%B %Y').get_loc(idx)]
            #otherwise -> do nothing but warn user up to which date inflation was corrected
            else:
                lacking_inflation_corr = True
    return(monthly_cost,lacking_inflation_corr)


# In[3]:


def arrange_cost_data_to_plot(material_monthly_cost,external_monthly_cost,equip_amount_data):
    import pandas as pd
    import numpy as np

    #Apply masks
    x_data1 = equip_amount_data.index.get_level_values(0).values
    y_data1 = equip_amount_data['Quantidade de Equipamentos'].values.astype(int)

    
    x_data2 = material_monthly_cost.index.values
    y_data2 = material_monthly_cost.values 
    
    x_data3 = external_monthly_cost.index.values
    y_data3 = external_monthly_cost.values

    return(x_data1,y_data1,x_data2,y_data2,x_data3,y_data3)


# In[ ]:




