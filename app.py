from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

playstore = pd.read_csv("data/googleplaystore.csv")
playstore 

# bagian ini untuk menghapus row 10472 karena nilai data tersebut tidak tersimpan pada kolom yang benar
playstore.drop([10472], inplace=True)

playstore.Category = playstore.Category.astype('category')

playstore.Installs =playstore.Installs.apply(lambda x: x.replace('+',''))
playstore.Installs = playstore.Installs.apply(lambda x: x.replace(',',''))

# Bagian ini untuk merapikan kolom Size, Anda tidak perlu mengubah apapun di bagian ini
playstore['Size'].replace('Varies with device', np.nan, inplace = True ) 
playstore.Size = (playstore.Size.replace(r'[kM]+$', '', regex=True).astype(float) * \
             playstore.Size.str.extract(r'[\d\.]+([kM]+)', expand=False)
            .fillna(1)
            .replace(['k','M'], [10**3, 10**6]).astype(int))
playstore['Size'].fillna(playstore.groupby('Category')['Size'].transform('mean'),inplace = True)
,inplace = True)

playstore.Price= playstore.Price.apply(lambda x: x.replace('$',''))
playstore['Price'] = playstore.Price.astype('float')

# Ubah tipe data Reviews, Size, Installs ke dalam tipe data integer
playstore.Reviews=playstore.Reviews.astype('int64')
playstore.Size=playstore.Size.astype('int64')
playstore.Installs=playstore.Installs.astype('int64')

@app.route("/")
# This fuction for rendering the table
def index():
    df2 = playstore.copy()

    # Statistik
  top_category=pd.crosstab(
    index=df2['Category'],
    columns='Jumlah', 
).sort_values('Jumlah',ascending=False)
top_category

    # Dictionary stats digunakan untuk menyimpan beberapa data yang digunakan untuk menampilkan nilai di value box dan tabel
    stats = {
        'most_categories'=top_category ['Jumlah'].head(1)
most_categories,
        'total': ____________,
         'rev_table' = pd.DataFrame({
    'Category': ['Social', 'Communication', 'Social', 'Tools', 'Productivity',
                 'Game', 'Social', 'Game', 'Social', 'Game'],
    'App': ['Facebook', 'WhatsApp Messenger', 'Instagram', 'Google Drive', 'Microsoft Word',
            'Subway Surfers', 'Facebook Lite', 'Candy Crush Saga', 'Snapchat', 'Clash of Clans'],
    'Reviews': [78158306, 69119316, 66577446, 59064087, 58347731,
                27722264, 25655305, 22426677, 20364716, 20313533],
    'Rating': [4.0, 4.3, 4.5, 4.4, 4.5,
               4.5, 4.2, 4.6, 4.0, 4.6]
})
rev_table

    ## Bar Plot
    cat_order = df2.groupby('Category').agg({
'App' : 'count'
}).rename({'App':'Total'}, axis=1).sort_values('Total', ascending=False).head()
X = cat_order.index.tolist()
Y = cat_order['Total'].tolist()
my_colors = ['r','g','b','k','y','m','c']
plt.barh(X,Y, color=my_colors)

cat_order

        X = df2['Reviews'].values # axis x
Y = df2['Rating'].values # axis y
area = playstore['Installs'].values/10000000 # ukuran besar/kecilnya lingkaran scatter plot
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
plt.scatter(x=X, y=Y, s=area, alpha=0.3)
plt.xlabel('Reviews')
plt.ylabel('Rating')
plt.savefig('rev_rat.png',bbox_inches="tight")
  

    # bagian ini digunakan untuk mengconvert matplotlib png ke base64 agar dapat ditampilkan ke template html
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    # variabel result akan dimasukkan ke dalam parameter di fungsi render_template() agar dapat ditampilkan di 
    # halaman html
    result = str(figdata_png)[2:-1]
    
    ## Scatter Plot
  X = df2[______].values # axis x
Y = df2[______].values # axis y
area = playstore[_______].values/10000000 # ukuran besar/kecilnya lingkaran scatter plot
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
# isi nama method untuk scatter plot, variabel x, dan variabel y
plt._______(x=_____,y=______, s=area, alpha=0.3)
plt.xlabel('Reviews')
plt.ylabel('Rating')
plt.savefig('rev_rat.png',bbox_inches="tight")
        
    # isi nama method untuk scatter plot, variabel x, dan variabel y
   X=(df2['Size']/1000000).values
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
plt.hist(X,bins=100, density=True, alpha=0.75)
plt.xlabel('Size')
plt.ylabel('Frequency')
plt.savefig('hist_size.png',bbox_inches="tight")

    ## Histogram Size Distribution
   ## code here

X = df2['Reviews'].values # axis x
Y = df2['Installs'].values # axis y
area = df2['Installs'].values/10000000 # ukuran besar/kecilnya lingkaran scatter plot
fig = plt.figure(figsize=(5,5))
fig.add_subplot()
plt.scatter(x=X, y=Y, s=area, alpha=0.3)
plt.xlabel('Reviews')
plt.ylabel('Installs (in 10 million)')
plt.savefig('reviews_installs.png',bbox_inches="tight")


    ## Buatlah sebuah plot yang menampilkan insight di dalam data 
    ____________________________
    ____________________________
    ____________________________

    # Tambahkan hasil result plot pada fungsi render_template()
    return render_template('index.html', stats=stats, result=result, result2=result2, result3=result3)

if __name__ == "__main__": 
    app.run(debug=True)
