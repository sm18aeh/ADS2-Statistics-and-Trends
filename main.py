# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 17:13:24 2022

@author: sm18aeh
"""

import pandas as pd
import matplotlib.pyplot as plt


def read_file(file_name):
    """
    Takes a filename as a parameter
    reads from said file and returns two dataframes:
    -df having empty data removed and unnecessary colums removed
    -countries_df being a transposed version of df
    """
    #converted file from xls to xlsx in order to avoid
    #xlrd module conflict
    df = pd.read_excel(file_name,
                       sheet_name="Data",header=3)
    
    #Removing empty years (no data for all countries at x year column)
    df.dropna(how="all", axis=1, inplace=True)
    #dropping unnecessary columns
    df = df.drop(columns = ["Country Code","Indicator Name","Indicator Code"])
    #Transposing the dataframe with countries as colums
    countries_df = df.set_index("Country Name").T
    
    return countries_df, df

def line_graph(countries, countries_df,labels):
    """
    Takes a list of countries to be plotted;
    Takes the dataframe the to plot the data with;
    Takes a list of two strings that contain the label names
    
    Produces a line plot
    """
    #setting values for the x-axis markings
    start_year = int(min(countries_df.index))
    end_year = int(max(countries_df.index))
    interval = (end_year - (start_year+1)) // 8
    
    plt.figure()
    plt.plot(countries_df[countries],label=countries)
    plt.xlim(str(start_year),str(end_year))
    #reducing clutter on x-axis markings
    plt.xticks([str(i) for i in range(start_year,end_year+1,interval)])
    #setting labels from received parameter
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.grid()
    plt.legend()
    plt.show()


def heatmap(country, dataframes, labels):
    """
    Takes the country the heatmap will be generated for;
    Takes the list of dataframes to plot the heatmap for;
    Takes a list of strings to create the labels
    
    Produces a heat map
    """
    #extracting the data for the selected country
    #from the passed dataframes
    single_dfs = []
    for i in range(len(dataframes)):
        single_dfs.append(dataframes[i][[country]])
    
    #merging the dataframes into a single dataframe
    heat_df = pd.concat(single_dfs,axis=1,join="inner")
    heat_df.columns.values[0:len(labels)] = labels
    #creating the correlation matrix
    heat_df = heat_df.corr(method="pearson")
    #output the converted data to xlsx 
    #heat_df.to_excel("output.xlsx")

    #creating heatmap
    fig, ax = plt.subplots(figsize=(len(labels),len(labels)))
    im = ax.imshow(heat_df, interpolation='nearest')
    #adding a colour bar
    fig.colorbar(im, orientation='vertical', fraction = 0.05)
    
    #adding the title
    plt.title(country)
    
    #adjusting the labels
    ax.set_xticks(range(len(labels)), labels=labels)
    ax.set_xticklabels(labels,rotation=35,ha="right",
                       rotation_mode="anchor")
    ax.set_yticks(range(len(labels)), labels=labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, round(heat_df.to_numpy()[i, j], 2),
                    ha="center", va="center", color="black")
    plt.show()


if __name__ == "__main__":
    #obtaining CO2/capita emissions data
    co2_df, co2_val_df = read_file("WB CO2 Emissions mT Per Capita.xlsx")
    # print(countries_df.head(5))
    
    #Selecting the countries to create the line graph with
    countries = ["United Kingdom","Germany","Romania","Bulgaria",
                 "Ghana","Nigeria"]
    line_graph(countries,co2_df,["Year","CO2 Emissions (Metric Tons)/Capita"])
    
    #Selecting the countr
    countries_df,values_df = read_file("WB Access to Electricity.xlsx")
    line_graph(["Ghana","Indonesia"],countries_df,
               ["Year","Access to Electricty (%)"])
    #obtaining GDP/capita data
    gdp_df, gdp_val_df = read_file("WB GDP Per Capita.xlsx")
    
    line_graph(countries,gdp_df,["Year","GDP Per Capita.xlsx"])
    #obtaining KWh Electricity used/capita data
    electric_df, electric_val_df = read_file("WB KWh Electricity Used Per Capita.xlsx")
    #obtaining Population Growth (%) data
    pop_growth_df, pop_growth_val_df = read_file("WB Population Growth.xlsx")
    
    heatmap("Japan",[co2_df,gdp_df,electric_df,pop_growth_df],
            ["CO2 (Metric Tons)/Capita","GDP/Capita","Electricity Usage (KWh)/Capita",
             "Population Growth (%)"])
    heatmap("United Kingdom",[co2_df,gdp_df,electric_df,pop_growth_df],
            ["CO2 (Metric Tons)/Capita","GDP/Capita","Electricity Usage (KWh)/Capita",
             "Population Growth (%)"])

    
         
    
