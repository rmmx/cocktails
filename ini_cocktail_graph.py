#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 17:09:41 2018

@author: rolando M
"""
import pandas as pd
import networkx as nx
import random
 
def replacechar(x):  
    return x.replace(" ", ",")

def pairs_function(source):
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1+1,len(source)):
            if ((source[p1]!='nan') & (source[p2]!='nan')):
                result.append([source[p1],source[p2]])
    return result


'''
Start function to modifiy the data and cerate the graph.
This should be in a class and under the constructor
Returns modifies dataframe and Graph object
'''
def initialize_cocktail_graph():
    

    df= pd.read_csv("all_drinks.csv")
    
    df.strIngredient1 = df.strIngredient1.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient2 = df.strIngredient2.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient3 = df.strIngredient3.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient4 = df.strIngredient4.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient5 = df.strIngredient5.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient6 = df.strIngredient6.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient7 = df.strIngredient7.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient8 = df.strIngredient8.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient9 = df.strIngredient9.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient10 = df.strIngredient10.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient11 = df.strIngredient11.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient12 = df.strIngredient12.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient13 = df.strIngredient13.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient14 = df.strIngredient14.apply(lambda x : (str(x).replace(" ", "_")).lower())
    df.strIngredient15 = df.strIngredient15.apply(lambda x : (str(x).replace(" ", "_")).lower())

    df_ingredients=df.strIngredient1
    df_ingredients=df_ingredients.append(df.strIngredient2)
    df_ingredients=df_ingredients.append(df.strIngredient3)
    df_ingredients=df_ingredients.append(df.strIngredient4)
    df_ingredients=df_ingredients.append(df.strIngredient5)
    df_ingredients=df_ingredients.append(df.strIngredient6)
    df_ingredients=df_ingredients.append(df.strIngredient7)
    df_ingredients=df_ingredients.append(df.strIngredient8)
    df_ingredients=df_ingredients.append(df.strIngredient9)
    df_ingredients=df_ingredients.append(df.strIngredient10)
    df_ingredients=df_ingredients.append(df.strIngredient11)
    df_ingredients=df_ingredients.append(df.strIngredient12)
    df_ingredients=df_ingredients.append(df.strIngredient13)
    df_ingredients=df_ingredients.append(df.strIngredient14)
    df_ingredients=df_ingredients.append(df.strIngredient15)
    df_ingredients=df_ingredients.drop_duplicates()
    df_ingredients=df_ingredients.dropna() 
    df_ingredients = df_ingredients.rename(columns={0: 'ingredient'})
    
    #One column with all the ingridients as a list
    df['string_ingredients']= df["strIngredient1"].map(str) + ' ' + \
       df["strIngredient2"].map(str) + ' '  + \
       df["strIngredient3"].map(str) + ' '  + \
       df["strIngredient4"].map(str) + ' '  + \
       df["strIngredient5"].map(str) + ' '  + \
       df["strIngredient6"].map(str)  + ' '  + \
       df["strIngredient7"].map(str)  + ' '  + \
       df["strIngredient8"].map(str)  + ' '  + \
       df["strIngredient9"].map(str)  + ' '  + \
       df["strIngredient10"].map(str)  + ' '  + \
       df["strIngredient11"].map(str)  + ' '  + \
       df["strIngredient12"].map(str)  + ' '  + \
       df["strIngredient13"].map(str)  + ' '  + \
       df["strIngredient14"].map(str)  + ' '  + \
       df["strIngredient15"].map(str)  
       
    df['string_ingredients'] = df['string_ingredients'].map(replacechar)
    df['string_ingredients']= df['string_ingredients'].apply(lambda x : str(x).split(","))
    
    #Load ingredient features
    df_ing_features=pd.read_csv('ingredients_features.csv')
    df_ing_features['ingredient']=df_ing_features.ING.apply(lambda x : (str(x).replace(" ", "_")).lower())
    

    #Create graph
    E=nx.Graph()

    #nodes= df_ingredients.reset_index()
    edges= df['string_ingredients'].apply(pairs_function)

    dff = pd.DataFrame([],columns=['I1','I2','weight'])

    #Loop to create datafreme of edges and add weights
    for x in edges:
        for y in x:      
            #a=(str(y[0]))
            #b=(str(y[1]))
            data = {'I1':y[0],'I2':y[1],'weight':1}
            dff = dff.append(data, ignore_index=True)
        
    #Group by both ingedients and aggregate by weigh column..the aggregation sum will be the weight of the edge
    
    df_group = dff.groupby(['I1', 'I2']).agg({'weight':sum})
    df_group = df_group.sort_values(by='weight', ascending=False)
    df_group =df_group.reset_index()


    #nodes=nodes.reset_index()  
    
    #nodes=nodes[0].apply(lambda x: str(x))
    
    #Add nodes to the graph no features
    #E.add_nodes_from(nodes)
    
    #Add nodes to the graph with features
    for i,r in df_ing_features.iterrows():
        E.add_node(r['ingredient'],aromatic= r['aromatic'],
                               sweet= r['sweet'],
                               sour= r['sour'],
                               spicy= r['spicy'],
                               creamy= r['creamy'],                            
                               salty= r['salty'],
                               fruity= r['fruity'],
                               nutty= r['nutty'],
                               alcoholic= r['alcoholic'],
                               drink= r['drink'],
                               fizzy_drink= r['fizzy_drink'],
                               fruit_juice= r['fruit juice'],
                               dairy= r['dairy'],
                               syrups= r['syrups']               
                              )

    
    #Add weighted edges to the graph
    for index,row in df_group.iterrows():   
        E.add_weighted_edges_from([(row['I1'],row['I2'],row['weight'])])
       
  


    return df,E



    '''
    Returns  all related ingridients distance N from an ingredient
    Parameters:
    w: weight of the edge, minimum threshold to start searching for.
    The smallest the weight the largest the list of related ingredients
    v_ingredient: Ingredient to search
    
    Example:
    get_related_ingredients(4,'tequila')
    >>>['lime_juice', 'lemon', 'salt']
    
    get_related_ingredients(3,'tequila')
    >>>['lemon_juice', 'coca-cola', 'tabasco_sauce', 'lime_juice', 'lemon', 'salt', 'orange_juice', 'grenadine']
    '''
    
    
def get_related_ingredients(w,v_ingredient,E):
    
    #TODO: Validate  v_ingredient exists
    #TODO Raise error
    
    #Get all edges.......................................weight threshold......either side of the edge
    all_edges = ((u,v) for u,v,d in E.edges(data=True) if (d['weight']>=w) and (u==v_ingredient or v==v_ingredient))
    #initialize return list
    l=[]
    #Loop through edges [list of lists]
    for a in all_edges:
        #Loop through ingredients in pair
        for b in a:
            #Dont add the original ingridient to the final list
            if (str(b) not in l) and (str(b) != v_ingredient):
                #append to a list
                l.insert(0, str(b))
    return l



'''
Ingredients related in a recipie
Intersection of common ingredients for all the related recipies
Because it is the intersection..the larger the weight the less probaility to get a result

Parameters:
w:threshold weight
ingredients:list of ingredients to search

Example:
intersection_ingredients(['tequila','lemon'],3)
['maraschino_cherry',
 'club_soda',
 'powdered_sugar',
 'carbonated_water',
 'lime',
 'tequila',
 'sugar',
 'blended_whiskey',
 'vodka',
 'light_rum',
 'gin']
'''
def intersection_ingredients(ingredients,weight,E):
    #TODO: Validate ingredients in v_ingredient exist
    ret=[]
    count=0
    intersection=[]
    for i in ingredients:
        #Get related ingredients for each ingredient selected by the user
        rel_ing=get_related_ingredients(weight,i,E)
        
        
        if count>0:
            ret=set(rel_ing).intersection(ret)
        else:
            ret=rel_ing
            count=count+1 
            
    for x in rel_ing:
        intersection.append(x)
          
    return list(dict.fromkeys(intersection))

'''
Returns the name of the cocktail based on a list of ingredients received
Only returns the cocktail if all the ingreients are provided
@params
list_ : list of ingidients
df: dataframe modified by 
'''
def search_cocktail(list_,df):
    exists=''
    for z ,r in df.iterrows():
        if exists!='':            
            #print ("COCKTAIL: " + r['strDrink'])
            return r['strDrink'] #Found! get out
        #print(r['string_ingredients'])
        for i in list_:
            #print (i)
            for y in i:
                #print (y)            
                if (y in r['string_ingredients']):
                    #print ('yay') ingredient in cocktail
                    exists="COCKTAIL: " + r['strDrink']
                else:
                    #print ('boo') ingredient not in cocktail
                    exists=''
                    break
      
    return False       

'''
Check if ingredients are present in the graph
Use 
try: assert search_ingredients(['tequila','xx']) ==['tequila']
except: print ('Test Failed')
'''
def search_ingredients(values,E):
    lf=[]
    l=[]
    for v in values:
        #print(v)
        filter_res = (n for n in E if (n==v) or (n==v))
        l=list(filter_res)
        lf= lf+l        
    return lf

'''
Returns random cocktail name fron list of ingredients
'''
def get_cocktail_name(final_list):
     #Weird cocktail name
                
    words=[]
    c=0
    random.shuffle(final_list)
    for e in final_list:
        if c<=2:
            w=e.split("_") 
            if c % 2 ==0:
                try:
                    words.append(w[1])
                except IndexError:
                    words.append(w[0])
            else:
                words.append(w[0])
            c=c+1
        else:
            break  

    cocktail_name=''
    for n in words:    
        cocktail_name=cocktail_name+n  +'_' 
        
    return cocktail_name

'''
retieves ingredients with the attribute
'''
def _attribute_ingredient_search(ingredients,attr,E):
    ret = []
    for ing in ingredients:        
        for (p, d) in E.nodes(data=True):
            for a in attr:                
                if d[a] == 1:
                    if ing==p:
                        ret.append(p)   
    
    
    return list(dict.fromkeys(ret)) 

'''
Returns additional ingredients for a cocktail given a list of favorite ingredients and ingredient attributes
and
a randon cocktail name fom taken from the list of suggested ingredients
Example:
a,b=selected_ingredients(['tequila','lemon'],['spicy','sweet'],2)
>>>a
['absolut_citron', 'ginger', 'benedictine', 'sugar', 'cointreau', 'lemonade', 'powdered_sugar', 'triple_sec', 'maraschino_cherry', 'sweet_and_sour']
>>>b
citron_ginger_benedictine_'
'''
def selected_ingredients(ingredients, attributes,weight,E):
    list1= intersection_ingredients(ingredients,weight,E)
    final_list=_attribute_ingredient_search(list1,attributes,E)
    
    random.shuffle(final_list)
    cocktail_name=get_cocktail_name(final_list)
   
    
    return final_list,cocktail_name

####################################################################      
    

#Initialize graph  
    
df,G=initialize_cocktail_graph()

a,b=selected_ingredients(['tequila','lemon'],['spicy','sweet'],3,G)
print(a,b)

a,b=selected_ingredients(['vodka','gin'],['sweet'],3,G)
print(a,b)

a,b=selected_ingredients(['chocolate','milk'],['creamy','sweet'],3,G)
print(a,b)

a,b=selected_ingredients(['cointreau','ginger'],['fizzy_drink'],3,G)
print(a,b)

a,b=selected_ingredients(['rum','scothch'],['aromatic','sweet'],3,G)
print(a,b)