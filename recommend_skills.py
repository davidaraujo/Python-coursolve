import MapReduce
import sys
import sys
import json
import re
import operator
import countries
from heapq import nlargest
from operator import itemgetter


"""
Join in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

debug = 0

# record contains information of a user
def mapper(record):
    
    skills_dic = {}
    user_dic = {}
    user_keys = record.keys()
    
    #print user_keys

    for user_id in user_keys:
        
        user_info = record[user_id]
        
        # user_info contains user location, acquired and desired skills
        acquired_skills = user_info['Acquired Skills']
            
        # transverse the acquired_skills for the user
        for ac_skill in acquired_skills:
            if ac_skill in skills_dic.keys():
                # append user to list of users in the dic
                skills_dic[ac_skill].append(user_id.encode('utf-8'))   
            else:
                # create new key for the skill and in the value put the user
                skills_dic[ac_skill] = [user_id.encode('utf-8')]

            # user x skills binary matrix    
            if user_id in user_dic.keys(): 
                user_dic[user_id][ac_skill] = 1
            else:
                user_dic[user_id] = {ac_skill:1}
            
        mr.emit_intermediate(1, skills_dic)
        
def reducer(key, list_of_values):
    
    recommend_skills_dic = {}

    for dic in list_of_values:
        
        # get a skill from the dic
        for skill in dic.keys():
            
            # list of users for that skill as A
            list_users = (dic[skill])
            
            # get remaining skills in the dic
            for remaining_skill in dic.keys():
                
                # list of users for that skill as B
                remaining_users = dic[remaining_skill]
                
                # intersect A and B and remove duplicates (create a set)
                intersection_users = set(list_users).intersection( set(remaining_users) )
                
# idea: check if the number of users that intersect is >= to the number that dont intersect
# if it is then recomment this skills to user that dont intersect
# if not then skip the recommendation of this skill
                
                sizeListUsers = len(list_users)
                sizeRemUsers = len(remaining_users)
                sizeShareUser = len(intersection_users)

                if sizeListUsers > sizeRemUsers: 
                    unequal_users = set(list_users) - set(remaining_users)
                else:    
                    unequal_users = set(remaining_users) - set(list_users) 
                    
                if debug == 1:
                    print '---------- ', skill, 'VS', remaining_skill
                    print 'number of shared users: ', sizeShareUser
                    print 'number of not shared users: ', max(sizeListUsers, sizeRemUsers)-len(intersection_users)
                
                    if (sizeShareUser == 0):
                        print 'List A :',list_users
                        print 'List B:',remaining_users
                        print 'List Dif', unequal_users
                
                sizeUnequalUsers = len(unequal_users)        
                if sizeUnequalUsers > 0 and sizeShareUser > sizeUnequalUsers:
                    #print '\nSKILL *', skill, '* should be recommented to users:'
                    for user_id in unequal_users:
                        #print '-> ', user_id
                                                
                        if skill in recommend_skills_dic.keys():
                            # append user to list of users in the dic
                            recommend_skills_dic[skill].append(user_id.encode('utf-8'))   
                        else:
                            # create new key for the skill and in the value put the user
                            recommend_skills_dic[skill] = [user_id.encode('utf-8')]
                            
            #if skill in recommend_skills_dic.keys():
            #    print '### Checked skill ', skill, ' and users to recommend are :',recommend_skills_dic[skill]
                            
    for skill_r in recommend_skills_dic.keys():
        print '### Recommend skill ', skill_r, 'to :',recommend_skills_dic[skill_r]
                
                        
                #print 'For intersection of skill "', skill , '" VS skill "', remaining_skill, '" the USERS ID are ', intersection_users


                # check the number of users that intersect in A and B
                
                #if len(intersection_users) == 10:
                    
                    
                    
                #print 'For intersection of skill "', skill , '" VS skill "', remaining_skill, '" the USERS ID are ', intersection_users
                    #print 'users a' , list_users
                    #print 'list b ' , remaining_users
                #print 'The unequal of skill "', skill , '" VS skill "', remaining_skill, '" the USERS ID are ', unequal_users
                    
                            
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  
  args_size = len(sys.argv)
  
  if args_size >=3:
      if sys.argv[2] == '-debug':
          debug = 1
  mr.execute(inputdata, mapper, reducer)
  
