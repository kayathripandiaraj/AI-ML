import streamlit as st
import pandas as pd
import pyttsx3
engine=pyttsx3.init()
engine.setProperty('rate',150)
st.title("Cracker Shop")
st.subheader("Welcome to our CrackerShop")
engine.save_to_file('welcome to our cracker Shop','sample.mp3')
engine.runAndWait()
st.audio('sample.mp3')
prices={'sparklers':10,'Baby Rocket':50,'FlowerPots':100,'chakkar':75,'Snake':85}
text=st.multiselect("What would you like to an order?",('sparklers','Baby Rocket','FlowePots','chakkar','Snake'))
order={}
total=0
sum = 0
for i in text:
    q1 = st.number_input(f"enter your quantity for {i}")
    order[i] = q1
data=[]
for i in order:
    quantity=order[i]
    price=prices[i]
    total_i=quantity*price
    sum += total_i
    data.append({"Products":i,"Quantity":q1,"Prices":price,"Total":sum})
st.write(order)
if st.button("Confirm Your Order"):
    df=pd.DataFrame(data)
    st.table(data)
    say="Hey Customer. Thank You for Your Order. You Have ordering The following Items:"
    for i in data:
        say+=f"{i['Quantity']} of {i['Products']} at {i['Prices']} rupees each."
        say+=f"Your Total Amount is ₹ {sum} rupees. Your order will be delivered in 2 days."
    engine.save_to_file(say,'sample.mp3')
    engine.runAndWait()
    st.audio('sample.mp3')
    st.success(f"Your Order placed,total amount is ₹{sum}")








    
