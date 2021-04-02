import matplotlib.pyplot as plt
import csv
import numpy as np

#https://perso.telecom-paristech.fr/eagan/class/igr204/datasets
#No electric cars in the csv file
#0 - Car;1 - MPG;2 - Cylinders;3 - Displacement;4 - Horsepower;5 - Weight;6 - Acceleration;7 - Model_Year;8 - Origin

def read_data(filename): # Task B.1
    car_list=[]
    with open(filename) as csvfile:
        read = csv.reader(csvfile, delimiter=';')w

        for row in read:
            # Ensure if a row is not the standart length it is not inclded
            # Determining which variable is missing is possible but I am not accounting for that
            if len(row) == 9: 
                for i in range(9):
                    if row[i] == '': # If an element is an empty string it will be replaced with string N/A 
                        row[i] = 'N/A'
                #0 - Car;1 - MPG;2 - Cylinders;3 - Displacement;4 - Horsepower;5 - Weight;6 - Acceleration;7 - Model_Year;8 - Origin
                car_list.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
    
        for car in range (len(car_list)):   # Replace 0's where the values are unknown with N/A's 
            # No atributes in our specific data can be equal to 0 so any 0 that shows up should not be 
            for atribute in range (1,7):
                if float(car_list[car][atribute])==0:
                    car_list[car][atribute]='N/A'
    # There aren't many different cars in the csv file and not much more in the world so complexity is not a big concern for a computer
    return car_list

def calc_atribute_avg_value(datastruct,atribute_index):  # Returns the average value of a numerical atribute
    total=0
    sample_size=0
    for i in range (len(datastruct)):
        if datastruct[i][atribute_index] != 'N/A':
            total += float(datastruct[i][atribute_index])
            sample_size += 1
    atribute_avg_value = float(total/sample_size)
    atribute_avg_value="{:.2f}".format(atribute_avg_value) # Round answer to 2 decimal places
     
    return atribute_avg_value            
def filter_by_region(datastruct,region):     # 'US' / 'Japan' / 'Europe'  returns a subset of the datastructure 
    region_cars=[]
    for i in range (len(datastruct)):
        if datastruct[i][8] == region:
            region_cars.append(datastruct[i])
    return region_cars
def filter_by_cylinder_count(datastruct,count):     # integer 3/4/5/6/8, returns a subset of the datastructure 
    cylinder_count_cars=[]
    for i in range (len(datastruct)):
        if int(datastruct[i][2]) == int(count):
            cylinder_count_cars.append(datastruct[i])
    return cylinder_count_cars
def how_many_unique_values(datastruct,aspect_index):  # Returns the ammount of unique values are there between all cars for a given index
    so_far=[]
    for i in range(len(datastruct)):
        if datastruct[i][aspect_index] not in so_far:
            so_far.append(datastruct[i][aspect_index])
    return len(so_far)

def get_region_num_cars(datastruct,region):  # 'US' / 'Japan' / 'Europe'
    total=0
    for i in range (len(datastruct)):
        if datastruct[i][8] == region:
            total+=1
    return total
def get_cylinder_num_cars(datastruct,cylinder_count): # Returns number of cars in our datastructure with the specific cylinder count
    total=0
    for i in range (len(datastruct)):
        if datastruct[i][2] == cylinder_count:
            total+=1
    return total
def get_year_num_cars(datastruct,model_year): # Returns cumber of cars in our datastructure form the specific mode year
    total=0
    for i in range (len(datastruct)):
        if datastruct[i][7] == model_year:
            total+=1
    return total

def get_pie_chart(datastruct):
    reg = ['US','Japan','Europe']
    num_of_cars = [] # Order matters, first part is num of cars from US, second from Japan and third from Europe

    for i in range (len(reg)):
        num_of_cars.append(get_region_num_cars(datastruct,reg[i]))

    plt.pie(num_of_cars, labels = reg, autopct='%1.2f%%', startangle=90)
    plt.show()

# Ordering functions for the specific datastructures
def smallest_val(datastruct,aspect):       # return the index for the car with smallest aspect value
    if len(datastruct) <= 0:
        return None
    small_index =0
    for i in range (len(datastruct)):
        if datastruct[small_index][aspect] != 'N/A' and datastruct[i][aspect] != 'N/A' :
            if float(datastruct[small_index][aspect]) > float(datastruct[i][aspect]):
                small_index=i
    return small_index
def reorder(datastruct,aspect): # Order with respect to aspect (aspect index in datastructure), smallest to largest
    if len(datastruct) <=0:
        return datastruct
    else:
        try:
            small_index = smallest_val(datastruct,aspect)
            datastruct[0], datastruct[small_index] = datastruct[small_index], datastruct[0]  # Swap cars
            return [datastruct[0]] + reorder(datastruct[1:],aspect)
        except:
            return datastruct # return the original datastructure is values cannot be compared
# Ordering functions for lists
def smallest_val_in_list(list_to_reorder):
    if len(list_to_reorder) <= 0:
        return 
    small_index =0
    for i in range (len(list_to_reorder)):
        if float(list_to_reorder[small_index]) > float(list_to_reorder[i]):
            small_index=i
    return small_index
def reorder_list(list_to_reorder): 
    if len(list_to_reorder) <=0:
        return list_to_reorder
    else:
        small_index = smallest_val_in_list(list_to_reorder)
        list_to_reorder[0], list_to_reorder[small_index] = list_to_reorder[small_index], list_to_reorder[0]  # Swap cars
        return [list_to_reorder[0]] + reorder_list(list_to_reorder[1:])

def get_scatter_info(datastruct,index_of_var1_x,index_of_var2_y):  # Returns a list of 2 lists ready for a scatterplot 
    output = [[],[]]
    reordered = reorder(datastruct,index_of_var1_x)
    for i in range (len(reordered)):
        if reordered[i][index_of_var1_x] != 'N/A' and reordered[i][index_of_var2_y] != 'N/A':
            output[0].append(float(reordered[i][index_of_var1_x]))
            output[1].append(float(reordered[i][index_of_var2_y]))
    return output
def get_scatter(datastruct,preset):   # index_of_var1_x = explanatory variable and index_of_var2_y = response variable
    if preset == 1:
        index_of_var1_x = 3
        index_of_var2_y = 4
    elif preset == 2:
        index_of_var1_x = 5
        index_of_var2_y = 6
    elif preset == 3:
        index_of_var1_x = 5
        index_of_var2_y = 1

    # Label for x axis
    if index_of_var1_x == 3:
        x_label = 'Displacement'
    elif index_of_var1_x == 5:
        x_label = 'Weight'
    # Label for y axis
    if index_of_var2_y == 4:
        y_label = 'Horsepower'
    elif index_of_var2_y == 6:
        y_label = 'Acceleration'
    elif index_of_var2_y == 1:
        y_label = 'MPG'

    x, y = get_scatter_info(datastruct,index_of_var1_x,index_of_var2_y)
    plt.scatter(x,y,alpha=0.5,s=40)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    

    plt.show()

def get_histogram(datastruct,index_of_var):
    hist_data=[]
    for i in range(len(datastruct)):
        if datastruct[i][index_of_var] != 'N/A':
            hist_data.append(float(datastruct[i][index_of_var]))
    hist_data = reorder_list(hist_data)
    if index_of_var == 2:
        hist_data = reorder_list(hist_data)
        plt.hist(hist_data, bins = 6, color='teal',align='mid')
        plt.ylabel('Counts')
        plt.xlabel('Number of cylinders')
        plt.show()
    elif index_of_var == 1:
        bins = []
        i=0
        while i < 48:
            bins.append(i)
            i+=5
        plt.hist(hist_data, bins = bins,rwidth=0.98)
        plt.ylabel('Counts')
        plt.xlabel('Fuel consumption, MPG')
        plt.show()


def main():
    cars = read_data('cars.csv')
    print('Hello, this is the interface for the user')
    print('At any moment you can write "quit" to quit the program')
    print('The program reads in info from a .csv file and saves it in a datastructure')
    user_input = 'N/A'
    while user_input != 'quit':
        user_input = input('Write "hist" for histogram, "scatter" for a scatterplot, "pie" for pie chart, "other" for other functions, "quit" to quit the program: ' )
        if user_input == "hist" or user_input == "scatter" or user_input == 'pie' or user_input == "other" or user_input == 'quit':
            if user_input == 'other':
                user_input = input('Write "avg" to get an avearge value of a characteristic, "filter" to filter the base datastructure, "order" to reorder the datastructure and print it, "print" to print the datastructure: ')
                if user_input == "avg" or user_input == "filter" or user_input == "order" or user_input == 'print':
                    if user_input == 'avg':
                        user_input = input('Type in the integers for respective average values 1 - MPG;2 - Cylinders;3 - Displacement;4 - Horsepower;5 - Weight;6 - Acceleration: ')
                        try:
                            user_input = int(user_input)
                            print(calc_atribute_avg_value(cars,user_input))
                        except: 
                            print('Input error')

                    elif user_input == 'filter':
                        print('This will modify the core datastructure and following actions will work with with it')
                        user_input = input('If want to filter the out the cars by region type "region", if by cylinder count type "cylinder": ')
                        if user_input == 'region':
                            user_input = input('Type in "US", "Japan", "Europe": ')
                            if user_input != "US" and user_input != "Japan" and user_input != "Europe":
                                print('Input error')
                            else:
                                cars = filter_by_region(cars,user_input)
                            
                        elif user_input == 'cylinder':
                            user_input = input('Type in the cylinder count you want to filter by (3/4/5/6/8): ')
                            if user_input != '3' and user_input != '4' and user_input != '5' and user_input != '6' and user_input != '8':
                                print('Input error')
                            else:
                                cars = filter_by_cylinder_count(cars,int(user_input))

                    elif user_input == 'print':
                        for car in cars:
                            print(car)

                    elif user_input == 'order':
                        user_input = input('Write to reorder for respective aspect "1"  MPG; "2" Cylinders; "3" Displacement;"4" Horsepower;"5" Weight;"6" Acceleration;7" Model_Year: ')
                        try:
                            cars = reorder(cars,int(user_input))
                            for car in cars:
                                if car[int(user_input)] != 'N/A':
                                    print(car[int(user_input)],car)
                        except:
                            print('Input error')
                else:
                    print('Input error')
            elif user_input == 'hist':
                user_input = input('Type in "1" for MPG, "2" for cylinder count histograms: ')
                if user_input != "1" and user_input != "2":
                    print('Input error')
                else:
                    get_histogram(cars,int(user_input))
            elif user_input == 'scatter':
                user_input = input('Type "1" for displacement and horsepower, "2" for weight and acceleration or "3" wight and MPG scatterplots: ')
                if user_input != "1" and user_input != "2" and user_input != '3':
                    print('Input error')
                else:
                    get_scatter(cars,int(user_input))
            elif user_input == 'pie':
                    get_pie_chart(cars)
        else:
            print('Input error')



if __name__ == '__main__':
    main()


