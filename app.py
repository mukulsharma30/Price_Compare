import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



def compare(med_name):
    client = serpapi.Client(api_key="7f8901944763eb7d28f7411f74a89adca0f14d9db3e1f0e7414316e216a7eb39")
    results = client.search({
        "engine": "google_shopping",
        "q": med_name,
        "gl":"in"
    })
    shopping_results = results["shopping_results"]
    return shopping_results


c1,c2 = st.columns(2)

with c1:
    st.image("e_pharmacy.png",width=200)

with c2:
    st.header("E-pharmacy price comparison system")

"""----------------------------------------------"""

st.sidebar.title("Enter the name of Medicine")
med_name = st.sidebar.text_input("Enter name here 👇:")
number = st.sidebar.text_input("Enter number of options here 👇:")

medicine_company=[]
med_price=[]


if med_name is not None:
    if st.sidebar.button("price compare"):
       shopping_results = compare(med_name)
       lowest_price = float((shopping_results[0].get('price'))[1:])  # list indexing done to remove $ & float is used to change string to float
       print(f"{lowest_price}")
       lowest_price_index = 0
       st.sidebar.image(shopping_results[0].get('thumbnail'))

       for i in range(int(number)):
           current_price = float((shopping_results[i].get('price'))[1:])
           medicine_company.append(shopping_results[i].get('source'))
           med_price.append(float((shopping_results[i].get('price'))[1:]))


           st.title(f"option {i+1}")   # when search options will be there
           c1,c2 = st.columns(2)

           c1.write("Company:")
           c2.write(shopping_results[i].get('source'))

           c1.write("Title:")
           c2.write(shopping_results[i].get('title'))

           c1.write("Price:")
           c2.write(shopping_results[i].get('price'))     # till here it is print 3 rows only

           url = shopping_results[i].get('product_link')
           c1.write("Buy Link:")
           c2.markdown('[Link](%s)'%url)
           """ _______________________________"""
           if (current_price < lowest_price):
               lowest_price = current_price
               lowest_price_index = i
       # this is best option
       st.title("Best option: ")  # when search options will be there
       c1, c2 = st.columns(2)

       c1.write("Company:")
       c2.write(shopping_results[lowest_price_index].get('source'))

       c1.write("Title:")
       c2.write(shopping_results[lowest_price_index].get('title'))

       c1.write("Price:")
       c2.write(shopping_results[lowest_price_index].get('price'))  # till here it is print 3 rows only

       url = shopping_results[lowest_price_index].get('product_link')
       c1.write("Buy Link:")
       c2.markdown('[Link](%s)' % url)

    #__________graph-comparison__________#
       df=pd.DataFrame(med_price,medicine_company)
       st.title("Chart Comparison")
       st.bar_chart(df)

       fig,ax=plt.subplots()
       ax.pie(med_price,labels=medicine_company,shadow=True)
       ax.axis("equal")
       st.pyplot(fig)
