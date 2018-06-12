#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 17:09:41 2018

@author: rolando Medellin
Offiste LBG January 2918
"""



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
    import random             
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
def attribute_ingredient_search(ingredients,attr,E):
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
    list1= intersection_ingredients(ingredients,weight)
    final_list=attribute_ingredient_search(list1,attributes,E)
    
    cocktail_name=get_cocktail_name(final_list)
   
    
    return final_list,cocktail_name
