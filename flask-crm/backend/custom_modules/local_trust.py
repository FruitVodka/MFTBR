import pandas as pd
import numpy as np

base_sim_path = ""
base_csv_path = ""

def clean_reviews(review_df):
    review_df.sort_values(by = ['iduser','idproduct','date'], ascending = [True, True, False], inplace = True)
    review_df.drop_duplicates(subset = ['iduser', 'idproduct'], keep = "first", inplace = True)
    return review_df

review_folded_df = pd.DataFrame()
product_df = pd.DataFrame()
product_folded_df = pd.DataFrame()
user_df = pd.DataFrame()
user_folded_df = pd.DataFrame()
trust_df = pd.DataFrame()
trust_list_df = pd.DataFrame()
idfold = 5

def init_LT_module(fold = 5):

    global idfold
    global review_folded_df
    global product_df
    global product_folded_df
    global trust_df
    global trust_list_df
    global user_df
    global user_folded_df

    idfold = fold

    review_folded_df = pd.read_csv(base_csv_path+"reviewfolded.csv")
    review_folded_df = review_folded_df[review_folded_df['idfold']!=idfold]
    review_folded_df = clean_reviews(review_folded_df)
    
    product_df = pd.read_csv(base_csv_path+"product.csv")
    product_df = product_df.set_index('idproduct')
    
    product_folded_df = pd.read_csv(base_csv_path+"product_folded.csv")
    product_folded_df = product_folded_df.astype({'idproduct':int})
    product_folded_df = product_folded_df.set_index('idproduct')

    user_df = pd.read_csv(base_csv_path+"user.csv")

    user_folded_df = pd.read_csv(base_csv_path+"userfolded.csv")
    user_folded_df = user_folded_df.set_index('iduser')

    trust_df = pd.read_csv(base_csv_path+"trust.csv")
        
    trust_list_df = pd.read_csv(base_csv_path+"trust_list.csv")
    trust_list_df = trust_list_df.set_index('iduser')

class local_trust_ratings:
    def __init__(self, iduser):
        # self.review_df = self.clean_reviews(review_df)
        self.review_df = review_folded_df
        self.iduser = iduser
#         self.idproduct = idproduct
        if(self.iduser in trust_list_df.index):
            self.local_trusted_users = trust_list_df['idtrusted'][self.iduser]
            tl = self.local_trusted_users.replace(" ","")
            tl = str(tl[1:-1]).split(",")
            for t in range(len(tl)):
                tl[t] = int(tl[t])
            self.local_trusted_users = tl
        else:
            self.local_trusted_users = []
        
    def clean_reviews(self, review_df):
        review_df.sort_values(by = ['iduser','idproduct','date'], ascending = [True, True, False], inplace = True)
        review_df.drop_duplicates(subset = ['iduser', 'idproduct'], keep = "first", inplace = True)
        return review_df   
    
    def get_average_rating(self,row):
        #Assuming row['iduser'] is a valid iduser
        row['average_user_rating'] = float(user_folded_df['f'+str(idfold)+'_train_avg'][row['iduser']])
        return row

    def get_rating_prediction(self, idproduct):
#         trusted_users = trust_df[trust_df['iduser'] == self.iduser]['idtrusted']
        self.trusted_user_ratings = pd.DataFrame()
        if(len(self.local_trusted_users) == 0):
            return np.nan
        trusted_user_ratings = self.review_df[(self.review_df['idproduct'] == idproduct) & (self.review_df['iduser'].isin(self.local_trusted_users))][['iduser','rating','review_rating','date']]
        if(trusted_user_ratings.empty == True):
            return np.nan
        trusted_user_ratings['average_user_rating'] = ""
        trusted_user_ratings = trusted_user_ratings.apply(self.get_average_rating, axis = 1)
        self.trusted_user_ratings = trusted_user_ratings
        # target_user_average_rating = float(user_folded_df['f'+str(idfold)+'_train_avg'][self.iduser])
        # final_rating = target_user_average_rating + (trusted_user_ratings['rating'] - trusted_user_ratings['average_user_rating']).mean()
        final_rating = (trusted_user_ratings['rating'] - trusted_user_ratings['average_user_rating']).mean()
        return final_rating

    def get_local_trust_rating_df(self):
        return self.trusted_user_ratings

# local_trust_instance = local_trust_ratings(review_folded_df, 1265)

# local_trust_instance.get_rating_prediction(8013)

# local_trust_instance.get_local_trust_rating_df()


