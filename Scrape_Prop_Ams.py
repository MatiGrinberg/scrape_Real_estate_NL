from Dependencies import *
#df=scrape_huurwoningen_rent(["den-haag", "utrecht", "amsterdam","leiden"])
#df=scrape_funda([r_funda,land,b_funda,p_funda],prop_typ=["Rent", "Land", "Buy", "Project"])
funda_dfs,huurw_df={f"funda_{t}": d for t,d in pd.read_csv("funda.csv").groupby("type")}, pd.read_csv("rent_huurwoningen.csv")
datasets={"huurwoningen_Rent": huurw_df}
datasets.update(funda_dfs)
print(datasets.keys())
k='funda_Project'
backup_df,df=datasets[k].copy(),datasets[k].copy()
#print(len(df.property_url.unique()))
print(df.shape)
inspect_dataframe(df)
print_null_rows(df,'property_url','Location')
drop_dupl=['Link']
rent,proj=("Rent" in k),("Proj"in k)
if "huurw" in k:
    pr_per_u='Price/room'
    drop_cols=['OriginalSearch','SearchCity','Terrace','Price/SqM']
else:
    df = df.rename(columns={"property_url": "Link"})
    drop_cols=['page','search_url','type','Y','Energy', 'NumUnits', 'Sale', 'Build','Delivery', 'Name_Prop', 'Units']
    if rent:
        pr_per_u='Price/room'
        drop_cols.append('Price/SqM')
    else:
        pr_per_u='Price/SqM'
        drop_cols.append('Price/room')
print(drop_cols)
df=prepare_data(df,rent=rent,drop_cols=drop_cols) # add if not Project => drop_dupl
print(df.shape)
round(df.describe(),1)

#Analyse
locs=mean_by_location(df,pr_per_u)
fil_loc=filter_per_loc(df,'Amsterdam',pr_per_u)
print(fil_loc)
pprint(fil_loc.Link.tolist())
#df_by_string=filter_by_string(df,'Link','1524872')

# Filtering Rows via individual criteria
df=df.join(backup_df['Y'])
exc_loc,inc_loc=[],[]
if rent:
    filt=filter_rent_rows(df,mx_pr_1h=1.4,mx_pr_room=0.7,min_area_1h=55,min_area_2h=75,min_area_3h=90,exclude=exc_loc,include=inc_loc).sort_values(['Bedrooms','Area','Price'])#.drop('Location',axis=1)
else:
    if not proj:
        filt=filter_buy_rows(df,min_h=1,min_price_sqm=2,max_price_sqm=6,min_area_any=47,min_area_large=100,min_hab_large=3,max_size=140).sort_values(['Price/SqM','Area']).drop('Bedrooms',axis=1)
    else:
        df=df.join(backup_df['Name_Prop'])
        filt=filter_buy_rows(df,min_h=0,min_price_sqm=3.3,max_price_sqm=5.9,min_area_any=47,min_area_large=0,min_hab_large=0,max_size=140).sort_values(['Price/SqM','Area']).drop('Bedrooms',axis=1)
print(len(filt),'\n',filt)
mean_by_location(filt,pr_per_u)
#group_idxs=print_by_group(filt.drop("Link",axis=1),'Bedrooms',pr_per_u)
group_idxs=print_by_group(filt,'Location',pr_per_u)


# Analysis Data
boxplot_location_groups(df[df['Bedrooms']==1],y_col=pr_per_u)
boxplot_location_groups(df[df['Bedrooms']!=1],y_col=pr_per_u)
#ams=filter_per_loc(df,'Amsterdam',pr_per_u)
#print_df_by_var(df,['Price', 'Area', pr_per_u],k)
plot_price_vs_size(df,k+' => Price vs Size','Price','Area')
plot_price_vs_size(df,k+' => Size vs '+pr_per_u,pr_per_u,'Area')
plot_histogram(df[df['Bedrooms']==1],k+"_1b",pr_per_u)
plot_histogram(df[df['Bedrooms']!=1],k+"_>1b",pr_per_u)
plot_correlation_heatmap(df, ['Price', 'Area', pr_per_u],k)















# Rent_Analyse
#Filtering Rows via individual criteria
excl_locs=['Vilafranca del Penedès']
fil_row=filter_buy_rows(df,min_h=1,min_price_sqm=0,max_price_sqm=1.5,min_area_any=70,min_area_large=100,min_hab_large=1,max_size=250).sort_values(['Area','Price/SqM']).drop('Hab',axis=1)
print(len(fil_row),'\n',fil_row)
locs=mean_by_location(fil_row,'Price/SqM')
filter_per_loc(fil_row,'Vilafranca del Penedès')
#df[df['Price/SqM']<0.2].sort_values('Area')


# Analysis Data
boxplot_location_groups(df,y_col='Price')
print_df_by_var(df,['Price', 'Area', 'Price/room'],k)
plot_price_vs_size(df,k+' => Price vs Size','Price','Area')
plot_price_vs_size(df,k+' => Price/room vs Hab','Price/room','Hab')
plot_price_vs_size(df,k+' => Price/room vs Size','Price/room','Area')
plot_histogram(df,k,'Price/room')
plot_histogram(df,k,'Price')
plot_histogram(df,k,'Area')
plot_correlation_heatmap(df,['Price', 'Area', 'Hab', 'Price/room'],k)



