def clean_time(df):
    df['estimated_time']=df['time'].str[-5:]
    df['estimated_date_time']=df['date'] + ' ' +df['estimated_time']
    df['estimated_date_time']=pd.to_datetime(df['estimated_date_time'])
    df.drop(columns=['date','estimated_time'],inplace=True)
    return df

clean_df=clean_time(df)
clean_df.to_parquet('all_flight_data_2025_02_26.parquet')