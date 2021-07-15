import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Average per 48 Win Shares by Draft Class (2000-2020)
def avg_win_shares():
    #Let's check which draft class is the most winningest
    avg_WS48 = draft.groupby('Draft_Year').Win_Shares_per_48.mean()

    #Use seaborn package to style our graph with a white background
    sns.set_style("darkgrid")

    #initialize size of graph
    plt.figure(figsize=(10,8))

    #identify independent and dependent variables
    x_var = draft.Draft_Year.unique()
    y_var = avg_WS48

    #title graph and axis labels
    plt.title("Average per 48 Win Shares by Draft Class (2000-2020)", fontsize=25)
    plt.ylabel("Per 48 Win Share Average", fontsize=15)
    plt.xlabel("Draft Year", fontsize=15)

    #limit axes
    plt.xlim(2000,2020)
    plt.ylim(0,0.075)

    plt.grid(axis='y',color='grey',linestyle='--',lw=0.5,alpha=0.5)

    #change tick labels for axes
    plt.tick_params(axis="both", labelsize=14)

    #Remove graph borders with inbuilt function
    sns.despine(left=True, bottom=True)

    #plot/create the line graph
    plt.plot(x_var, y_var)
    plt.show()

#Colleges that Produced the Most NBA Players (2000-2020)
def college_count():
    #create empty lists to house the colleges and counts of players from each college respectively
    college = []
    count = []

    #counting all players that attended each college
    college_count = draft.College.value_counts()

    #collecting colleges/counts of colleges that produced at least 20 nba players since 2000
    for i,v in college_count.items():
        if v >= 20:
            if i == "College":
                college.append("N/A")    
            else:
                college.append(i)
            count.append(v)

    #zipping together the two lists and sorting in ascending order
    display = zip(college, count)
    display = list(sorted(display, key = lambda x: x[1]))

    #unzipping lists to be able to separate the variables
    college, count = zip(*display)

    x_var = college
    y_var = count

    #locations for the labels
    range = np.arange(len(x_var))
    bar_width = 0.5

    graph, axes = plt.subplots(figsize=(10,6))
    bars = axes.bar(range, y_var, bar_width)
    axes.set_ylabel("NBA Players Produced")
    axes.set_xlabel("Colleges")
    axes.set_title("Colleges that Produced the Most NBA Players (2000-2020)")
    axes.set_xticks(range)
    axes.set_xticklabels(x_var)

    axes.bar_label(bars, padding = 3)
    graph.tight_layout()

    # another attempted method for the same graph
    # graph = plt.figure()
    # axes = graph.add_axes([0,0,1,1])
    # axes.bar(college, count)
    plt.show()

def category_leaders():
    stat = (str)(input("Choose the statistic you would like to see: MPG, PPG, RPG, APG.\n"))
    extreme = (str)(input("Would you like to know the player at the top or bottom of the category?\n"))
    if stat.upper() == "MPG":
        df = draft[['Player', 'MP_pg']]
        df.sort_values(by=["MP_pg"], ascending=False, inplace=True)
        if extreme.upper() == "TOP":
            print(df.iloc[0:1])
        elif extreme.upper() == "BOTTOM":
            print(df.iloc[df.last_valid_index()-2:df.last_valid_index()-1])

#average win shares per 48 by each first round draft pick location from 2000-2020
def win_shares_by_pick():
    #making sure that we are only considering top 30 picks per draft
    top30 = draft[(draft['Pk'] < 31)]

    #grouping the entries by pick to average WS/48
    avg = top30.groupby('Pk').Win_Shares_per_48.mean()
    
    sns.set_style("darkgrid")

    x_var = top30.Pk.unique()
    y_var = avg

    graph, axes = plt.subplots(figsize=(10,7))
    axes.set_ylabel("Average Win Shares per 48 Mins")
    axes.set_xlabel("Draft Pick Number")
    axes.set_title("Average Win Shares per 48 minutes for each\n"
    "NBA Draft Pick (2000-2020)")
    axes.tick_params(axis='both', labelsize=12)
    axes.set_xlim(-1,31)
    axes.set_xticks(np.arange(1,31))
    axes.yaxis.grid(color='white')

    axes.bar(x_var, y_var)
    sns.despine(left=True, bottom=True)
    plt.show()




if __name__ == "__main__":
    #read in csv file
    draft = pd.read_csv("draft_data_2000s.csv", index_col= 0)
    loop = 1
    while loop:
        try:
            loop = (int)(input("What would you like to do?\n"
            "1:Average per 48 Win Shares by Draft Class.\n" 
            "2:Colleges that Produced the Most NBA Players.\n"
            "3:Average per 48 Win Shares by Draft Pick Number\n"
            "Enter any other number to exit.\n"))
        except ValueError:
            print("You did not enter an integer!")
            continue
        if (loop == 1):
            avg_win_shares()
        elif (loop ==2):
            college_count()
        elif (loop ==3):
            win_shares_by_pick()
        else:
            loop = 0
            print("Goodbye!")
