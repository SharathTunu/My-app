from django.db import models
import pandas as pd
import numpy as np
from multiprocessing import Pool
import math
from functools import partial
import pytz
from pandas_drf_tools.serializers import DataFrameIndexSerializer
# Create your models here.


class CapTableReport():

    def clean(self, series):
        series = series.astype(str)
        series = series.str.replace(',', '')
        series = series.str.extract('(\-?\d*\.\d+|\d+)', expand=False)
        series = pd.to_numeric(series, errors='coerce')
        series.fillna(0, inplace=True)
        return series

    def process_captable(self, captable):
        """
        A method to process captable when the portfolio is uploaded.
        """
        results = pd.DataFrame(columns=captable.columns)
        bad_data = []
        try:
            captable = captable.replace(r'^\s*$', np.nan, regex=True)
            new_df = captable.dropna()
            bad_data.append(pd.concat([captable, new_df]).drop_duplicates(keep=False))

            for c in results.columns:
                # Clean Integer Fields.
                if c == "SHARES PURCHASED":
                    results[c] =  self.clean(new_df[c]).astype(int)
                # Clean Float Fields.
                elif c == "CASH PAID":
                    results[c] = self.clean(new_df[c]).astype(float)
                # Clean Date Fields with proper format.
                elif c == "INVESTMENT DATE":
                    results[c] = pd.to_datetime(new_df[c], errors='coerce', format='%Y-%m-%d')
                    bad_data.append(new_df.loc[~results.index.isin(results.dropna(subset=[c]).index)])
                    results = results.dropna(subset=[c])
                # Clean string Fields and save them as uppercase letters.
                elif c == "INVESTOR":
                    results[c] = new_df[c]
                    results[c] = new_df[c].str.lower().str.capitalize()

            nums = results._get_numeric_data().columns
            bad_numerics = (results[nums] == 0).any(1)
            bad_numerics = results[bad_numerics]

            good_data = pd.concat([results, bad_numerics]).drop_duplicates(keep=False)

            bad_data.append(bad_numerics)
            bad_data = pd.concat(bad_data, sort=True).dropna(how='all')
            return [good_data, bad_data]

        except Exception as ex:
            raise

    def captable_as_df(self, path):
        """
        1. Read csv file and strip whtespaces at the start and end of column names.
        2. Process the records before summarizing by using multi processing tool for faster speeds
        when the file is too large.
        3. Check to see if any therads failed else send the good and bad data back to views.
        """
        # 1.
        captable = pd.read_csv(path, low_memory=False, na_filter=False)
        captable = captable.rename(columns=lambda x: x.strip())
        # 2.
        number_of_splits = math.ceil(captable.shape[0]/4000)
        record_dfs = np.array_split(captable, number_of_splits)
        p = Pool(processes=number_of_splits)
        results = p.map(partial(self.process_captable), 
                        [df for df in record_dfs])
        p.close()
        # 3.
        failed_threads = [i for i in results if not isinstance(i, list)]
        if failed_threads:
            error = ". ".join(failed_threads)
            return error
        
        passed_threads = [i for i in results if isinstance(i, list)]
        good_data = pd.concat([i[0] for i in passed_threads if isinstance(i[0], pd.DataFrame)])
        bad_data = pd.concat([i[1] for i in passed_threads if isinstance(i[1], pd.DataFrame)])

        return [good_data, bad_data]

    def get_summary(self, path, filter_date=pytz.datetime.datetime.today().strftime("%Y-%m-%d")):
        """
        1. Get the csv as a dataframe and filter_date in date format.
        2. Apply filter
        3. Calculate summary and build response
        """
        response = dict()
        # 1.
        captable = self.captable_as_df(path)[0]
        filter_date = pytz.datetime.datetime.strptime(filter_date, "%Y-%m-%d")
        # 2.
        captable = captable[captable['INVESTMENT DATE']<= filter_date]
        # 3.
        # Convert date to string.
        response['date'] = filter_date.strftime("%m/%d/%Y")
        # Get the sum of cash and shares after filtering.
        response['cash_raised'] = captable['CASH PAID'].sum()
        response['total_number_of_shares'] =  captable['SHARES PURCHASED'].sum()
        # Get the sum of cash and shares after filtering for each investor.
        captable['shares'] = captable.groupby(['INVESTOR'])['SHARES PURCHASED'].transform('sum')
        captable['cash_paid'] = captable.groupby(['INVESTOR'])['CASH PAID'].transform('sum')
        # Drop duplicate records.
        new_df = captable.drop_duplicates(subset=['INVESTOR'])
        # Calculate the ownership values for each investor.
        new_df['ownership'] = new_df['shares']/response['total_number_of_shares']
        new_df = new_df.round({'ownership': 2})
        new_df['investor'] = new_df['INVESTOR']
        new_df = new_df.drop(columns=['INVESTMENT DATE', 'SHARES PURCHASED', 'CASH PAID', 'INVESTOR'], errors='ignore')
        # serialize the response.
        response["ownership"] = new_df.to_dict('r')

        return response

