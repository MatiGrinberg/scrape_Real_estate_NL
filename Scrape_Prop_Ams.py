from Dependencies import *
# Pr x Sqm => New 5.2, Land 1, Built 4.2, Rent 1.3
#df=scrape_huurwoningen_rent(["den-haag", "utrecht", "amsterdam","leiden"])
#df=scrape_funda([r_funda,land,b_funda,p_funda],prop_typ=["Rent", "Land", "Buy", "Project"])
funda_dfs,huurw_df={f"funda_{t}": d for t,d in pd.read_csv("funda.csv").groupby("type")}, pd.read_csv("rent_huurwoningen.csv")
datasets={"huurwoningen_Rent": huurw_df}
datasets.update(funda_dfs)
print(datasets.keys())
k='funda_Rent'
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
df=prepare_data(df,drop_cols=drop_cols) # if  Project => skip drop_dupl
print(df.shape)
round(df.describe(),1)

#Analyse
locs=mean_by_location(df[df['Bedrooms']==1],pr_per_u)
#print(df[(df["Location"].isin(locs[:7])) & (df["Bedrooms"] == 1)].sort_values(pr_per_u))
locs=mean_by_location(df[df['Bedrooms']!=1],pr_per_u)
#print(df[(df["Location"].isin(locs[:8])) & (df["Bedrooms"] != 1)].sort_values(pr_per_u))
locs=mean_by_location(df,pr_per_u)
fil_loc=filter_per_loc(df,'Amsterdam',pr_per_u)
print(fil_loc)
pprint(fil_loc.Link.tolist())
#df_by_string=filter_by_string(df,'Link','1524872')

# Filtering Rows via individual criteria
df=df.join(backup_df['Y'])
exc_loc,inc_loc=[],[]
if rent: # rent
    filt=filter_rent_rows(df,mx_pr_1h=0.4,mx_pr_room=0.5,min_area_1h=55,min_area_2h=70,min_area_3h=90,exclude=exc_loc,include=inc_loc).sort_values(['Bedrooms','Area','Price'])#.drop('Location',axis=1)
else: 
    if not proj: # Built
        filt=filter_buy_rows(df,min_h=1,min_price_sqm=2,max_price_sqm=4.5,min_area_any=55,min_area_large=100,min_hab_large=3,max_size=140,fr=2010,to=2040).sort_values(['Price/SqM','Area']).drop('Bedrooms',axis=1)
    else: # Project
        df=df.join(backup_df['Name_Prop'])
        filt=filter_buy_rows(df,min_h=0,min_price_sqm=2.3,max_price_sqm=5.5,min_area_any=50,min_area_large=0,min_hab_large=0,max_size=140).sort_values(['Price/SqM','Area']).drop('Bedrooms',axis=1)
print(len(filt),'\n',filt)
mean_by_location(filt,pr_per_u)
#group_idxs=print_by_group(filt.drop("Link",axis=1),'Bedrooms',pr_per_u)
group_idxs=print_by_group(filt,'Location',pr_per_u,dr=[])


# Analysis Data
boxplot_location_groups(df[df['Bedrooms']==1],y_col=pr_per_u)
boxplot_location_groups(df[df['Bedrooms']!=1],y_col=pr_per_u)
boxplot_location_groups(df,y_col=pr_per_u)
#ams=filter_per_loc(df,'Amsterdam',pr_per_u)
#print_df_by_var(df,['Price', 'Area', pr_per_u],k)
plot_price_vs_size(df,k+' => Price vs Size','Price','Area')
plot_price_vs_size(df,k+' => Size vs '+pr_per_u,pr_per_u,'Area')
plot_histogram(df[df['Bedrooms']==1],k+"_1b",pr_per_u)
plot_histogram(df[df['Bedrooms']!=1],k+"_>1b",pr_per_u)
plot_correlation_heatmap(df, ['Price', 'Area', pr_per_u],k)



