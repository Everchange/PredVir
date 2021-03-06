def refining_expGrp(base,keep,rename,dropna_col,index_col=None):
    XpG = pd.read_csv(base+r'/'+base+'_exp_grp.csv',index_col=index_col)
    XpG = XpG[keep]
    XpG = XpG.rename(index=str,columns=rename)
    XpG = XpG.dropna(axis=0,subset=dropna_col)
    return XpG

def refining_trscr(base,transpose=False):
    Trscr = pd.read_csv(base+r'/'+base+'_data.csv',index_col=0)
    if transpose:
        Trscr = Trscr.transpose()
    return Trscr

def refining_platform(base,keep,rename,dtype):
    Plt = pd.read_csv(base+r'/'+base+'_platform.csv',dtype=dtype)
    Plt = Plt[Plt['SPOT_ID']!='--Control']
    Plt = Plt[keep]
    Plt = Plt.rename(index=str,columns=rename)
    return Plt

def barsplot(df,titre='',figsize=(6,4)):
    
    valeurs = df.unique()
    
    categories_sain = []
    categories_malade = []
    
    for v in valeurs:
        
        if pd.isnull(v):
            categories_sain.append(Clinique['id_pathology'].loc[Index_sain].apply(pd.isnull).sum())
            categories_malade.append(Clinique['id_pathology'].loc[Index_malade].apply(pd.isnull).sum())
        else:
            categories_malade.append((df.loc[Index_malade].values == v).sum())
            categories_sain.append((df.loc[Index_sain].values == v).sum())

    index = np.arange(valeurs.shape[0])
    
    fig=plt.figure(figsize=figsize)
    
    p1 = plt.bar(index,categories_malade)
    p2 = plt.bar(index,categories_sain,bottom=categories_malade)

    plt.ylabel('N')
    plt.title(titre)
    plt.xticks(index,valeurs)
    plt.legend((p2[0],p1[0]),('Sain','Malade'))
    plt.show()

def OHEncoding(filename,categorical_columns):
    DF = pd.read_csv(filename,index_col=ID)
    DF = pd.get_dummies(DF,columns=categorical_columns)
    return DF

def Create_Patient_Index_Regression(df):
    return df[DEAD].index.values

def Create_Patient_Drop_Index_Classification(df,n_mois):
    I = [(k[-1]=='+' and int(k[:-1])<n_mois) for k in df[OS].values]
    return np.setdiff1d(df.index.values,I)

def X_transcriptome(base,index):
    X = pd.read_csv(base+r'/'+base+'_trscr.csv',index_col=0)
    return X.loc[index]

def get_function_survival(n_mois):
    return lambda x: 1 if x[-1]=='+' else int((int(x) > n_mois))

def Y_clinique(base,index,n_mois=None):
    Y = pd.read_csv(base+r'/'+base+'_clinique_OH.csv',index_col=0)
    Y = Y.loc[index]
    if n_mois is None:
        Y = Y['os_months']
    else:
        Y = Y[OS].apply(get_function_survival(n_mois))
    return Y