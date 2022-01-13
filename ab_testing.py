import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control=pd.read_csv("05_hafta/ab_testing_control.csv")
df_control_=df_control.copy()

df_test = pd.read_csv("05_hafta/ab_testing_test.csv")
df_test_=df_test.copy()

#Güven aralıklarını inceleyelim

sms.DescrStatsW(df_control_["Impression"].dropna()).tconfint_mean()
#(95218.50401213673, 108204.39412325788)
sms.DescrStatsW(df_control_["Click"].dropna()).tconfint_mean()
#(4675.307376598384, 5526.007368556174)
sms.DescrStatsW(df_control_["Purchase"].dropna()).tconfint_mean()
#(508.0041754264924, 593.7839421139709)
sms.DescrStatsW(df_control_["Earning"].dropna()).tconfint_mean()
#(1811.6904932901255, 2005.4461063153728)

sms.DescrStatsW(df_test_["Impression"].dropna()).tconfint_mean()
#(114497.4978773465, 126527.32563772256)
sms.DescrStatsW(df_test_["Click"].dropna()).tconfint_mean()
#(3672.3296353187875, 4262.769886293253)
sms.DescrStatsW(df_test_["Purchase"].dropna()).tconfint_mean()
#(530.5670226990062, 633.6451705979289)
sms.DescrStatsW(df_test_["Earning"].dropna()).tconfint_mean()
#(2424.469019772786, 2605.3124455284496)

# Satın almanın tıklanmaya oranı

p_control= (df_control_["Purchase"] / df_control_["Click"]).mean()   # Max bidding grubunun reklam izleme / satın alma oranı
#0.11592561427164819
p_test=(df_test_["Purchase"] / df_test_["Click"]).mean() # Average bidding grubunun reklam izleme / satın alma oranı
#0.15656625309447395

#Average ve Max bidding arasındaki fark gözlemlenmiştir. Bu farkın anlamlı olmasını hipotez testleri ile kontrol edeceğiz.

#H0= P1=P2 ,Max bidding purchase-click oranı ile Average bidding purchase-click oranı arasında anlamlı bir fark yoktur.
#H1= P1!=P2... fark vardır.



# Varsayımlar
# Normallik varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

sum_click = np.array([df_control_["Click"].sum(), df_test_["Click"].sum()]) # İki grubun toplam reklam izleme sayısı.
# Oran testinde nobs argümanına girilecek.
sum_purchase = np.array([df_control_["Purchase"].sum(), df_test_["Purchase"].sum()]) # İki grubun toplam ürün satın alma sayısı.
# Oran testinde count argümanına girilecek.

# Oran testi:
test_stat, pvalue = proportions_ztest(count=sum_purchase,nobs=sum_click)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#Test Stat = -34.9800, p-value = 0.0000
#p-value değeri 0.05 te küçük olduğu için H0 hipotezini reddediyoruz.Böylece anlıyoruz ki anlamlı bir fark vardır.




