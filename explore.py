

#imports

import pandas as pd
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import scipy
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


st.title("Data Explorer Pro Max")
st.sidebar.title("Welcome")
opt = st.sidebar.radio("How do you want to import the dataset", ("Upload CSV", "import via link"), index=0)
df = None
if opt == "Upload CSV":
    x = st.file_uploader(label = "Upload your dataset", type=['csv'])
    if x is not None:
        df = pd.read_csv(x)
else:
    x = st.text_input("Paste the link of the csv here")

    numrows = st.number_input("Number of rows you want to import", min_value=10, value=1000)
    check = st.checkbox("Import")
    if check:
        df = pd.read_csv(x, nrows=numrows)
    


#data cleaning
if isinstance(df, pd.core.frame.DataFrame):
    st.table(df.head())

    st.sidebar.subheader("Remove some columns")
    rmcol = st.sidebar.radio("Do you want to remove some columns", ('Yes', 'No'), index=1)
    if rmcol == 'Yes':
        colsToRm = st.sidebar.multiselect("Choose the columns you want to remove",
            df.columns)
        df.drop(colsToRm, axis='columns', inplace=True)
        st.subheader("Updated Table:")
        st.table(df.head())

    sm = [df.isna().sum()[i] for i in df.columns]
    st.sidebar.subheader("Missing values in dataset")
    if any(df.isna().sum()):

        st.sidebar.write(f"You have {sum(sm)} na values in your dataset")
        rmna = st.sidebar.radio("Do you want to replace NA values or remove", ('Replace', 'Remove', 'Do Nothing'), index=2)
        if rmna == 'Remove':
            df.dropna(inplace=True)
            st.write('NA values have been removed')
            st.write(df)

        
        elif rmna == "Replace":
            repmet = st.sidebar.selectbox("Choose the statistic you want to replace it with",
                ['--','Mean', 'Median'])
            if repmet == 'Mean':
                df.fillna(df.mean(), inplace=True)
                
            elif repmet == 'Median':
                df.fillna(df.median(), inplace=True)
            st.write(df)  
    else:
        st.write("Dataset has no missing values! You are good to go")   

    st.sidebar.title("Data Exploration")

    descol = st.sidebar.multiselect("Select columns to get statistics", df.columns)
    if descol:
        st.subheader("Column Statistics")
        st.table(df[descol].describe())

    st.sidebar.subheader("Graphs")
    typeOfData = st.sidebar.radio("What type of data you want to categorize", ("Numerical", "Categorical"))
    if typeOfData == "Numerical":
        dfnew = df.select_dtypes(include=np.number)
        graphtype = st.sidebar.selectbox("Select the type of graph", ['Line Graph', 'Histogram'])
        if graphtype == "Line Graph":

            try:
                inde = st.sidebar.selectbox("Which column should be treated as index ", ['default'] + list(df.columns) )
                

                if inde == 'default':
                    # st.write(df)
                    st.subheader("Line Graph")
                    start, end = st.select_slider("reduce graph using slider", 
                        options=list(df.index.values), value=(1, list(df.index.values)[-1]))
                    
                    
                    
                    sel = st.sidebar.multiselect("Select columns for line graph", dfnew.columns)
                    st.line_chart(df[start:end][sel])
                else:
                    st.subheader("Line Graph")
                    # st.write(df[inde])
                    start, end = st.select_slider("reduce graph using slider", 
                        options=list(df[inde]), value=(str(df[inde][0]), str(df[inde][df[inde].shape[0]-1])))
                    
                    
                    sel = st.sidebar.multiselect("Select columns for line graph", dfnew.columns)
                    st.line_chart(df[df.loc[:, inde] > start][df.loc[:, inde] < end][sel])
                    st.subheader("Histogram")
                    sel = st.sidebar.multiselect("Select columns for histogram", dfnew.columns)
            except ValueError:
                st.write("The column you choose can't be treated as Index choose another")
                
        elif graphtype == "Histogram":
            st.subheader("Histogram")
            sel = st.sidebar.multiselect("Select columns for line graph", dfnew.columns)
            start, end = st.select_slider("reduce graph using slider", 
                        options=list(df.index.values), value=(1, list(df.index.values)[-1]))
            
            fig = ff.create_distplot([df[start:end][select] for select in sel] , sel)
            st.plotly_chart(fig)
    elif typeOfData == "Categorical":
        dfnew = df.select_dtypes(include='object')
        st.write(dfnew)
        typeOfGraph = st.sidebar.selectbox("select the type of graph", ["Piechart", "Bar Graph"])
        if typeOfGraph == "Piechart":
            sel = st.sidebar.selectbox("Select column for Pie chart", dfnew.columns)
            start, end = st.select_slider("reduce graph using slider", 
                        options=list(df.index.values), value=(1, list(df.index.values)[-1]))
            dfplot = pd.DataFrame({sel:df[start:end][sel].value_counts().index, 'freq':df[start:end][sel].value_counts()})
            fig = px.pie(dfplot, values='freq', names=sel)
            st.plotly_chart(fig)
            st.write(df[start:end][sel].value_counts())

        elif typeOfGraph == 'Bar Graph':
            sel = st.sidebar.selectbox("Select column for Pie chart", dfnew.columns)
            start, end = st.select_slider("reduce graph using slider", 
                        options=list(df.index.values), value=(1, list(df.index.values)[-1]))
            dfplot = pd.DataFrame({sel:df[start:end][sel].value_counts().index, 'freq':df[start:end][sel].value_counts()})
            fig = px.bar(dfplot, x=sel, y='freq')
            st.plotly_chart(fig)
            st.write(df[start:end][sel].value_counts())
    
    import base64
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
            




    

    
    
        



