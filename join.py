import MapReduce
import sys

"""
Join in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # table_orig: table the record is originated from 
    # values: record contents
    table_orig = record[0]
    order_id = record[1]
    
    order_num = 10
    lineitem = 17
    i = 2
    
    #if table_orig == 'order':
    #    while i < order_num:
    #            i +=1
            
    #elif table_orig == 'line_item':
    #    while i < lineitem:
    #            i +=1
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: table_orig
    # value: list of join for tables order and line_item
    join_list = []
    
    #print "DEBUG" , key , list_of_values
    
    order = list_of_values[0]
    
    items_num = len(list_of_values) 
    
    if items_num == 0:
        mr.emit(order)
    else:     
        for x in range (1, items_num):
            mr.emit(order + list_of_values[x])
            
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
