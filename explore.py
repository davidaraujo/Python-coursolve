import sys
import json
import re
import operator
import countries
from heapq import nlargest
from operator import itemgetter

locations_dic = {} # location statistics
skills_desired_dic = {} # skills desired statistics 
skills_acquired_dic = {} # skills acquired statistics 


# Print all users and skills
def print_coursolvers(fp):

    for line in fp:
        keys = json.loads(line).keys()
        
        for x in keys:
            print " --------------------------------------------------- "
            print "Skills for User ID = ", x 
            skills = json.loads(line)[x]
            for i in skills:
                
                if i == "Acquired Skills":
                    print "Acquired Skills:"
                    for k in skills[i]:
                        print "       " , k
                elif i == "Desired Skills":
                    print "Desired Skills:"
                    for k in skills[i]:
                        print "       " , k
                else:
                    print i, " = ", skills[i]
            print " --------------------------------------------------- "    
         

# Print most popular acquired and desired skills among coursolvers
# usage: most_popular_skills(input file, number of top skills to return)
def most_popular_skills(fp, top_number):
    
    for line in fp:
        keys = json.loads(line).keys()
        
        # the keys contain the userid
        for x in keys:
            skills = json.loads(line)[x]
            
            # user_info contains user location, acquired and desired skills
            for user_info in skills:
                
                for i in skills.keys():
                    if i == "Desired Skills":
                        desired_skills = skills[i]
                        
                        for skill in desired_skills:
                            if skill in skills_desired_dic.keys():
                                skills_desired_dic[skill] += 1 
                            else:
                                skills_desired_dic[skill] = 1 

                    elif i == "Acquired Skills":
                        acquired_skills = skills[i]
                                        
                        for skill in acquired_skills:
                            if skill in skills_acquired_dic.keys():
                                skills_acquired_dic[skill] += 1 
                            else:
                                skills_acquired_dic[skill] = 1 
                
        print ' --------- MOST POPULAR ACQUIRED SKILLS AND DESIRED SKILLS FOR COURSOLVERS | TOP ', top_number

        top = 1    
        print 
        print 'TOP SKILLS ACQUIRED:'
        for skill_acquired, count in nlargest(int(top_number), skills_acquired_dic.iteritems(), key=itemgetter(1)):                   
            print 'Top', top , ':' ,  skill_acquired, '#', count
            top +=1    

        top = 1
        print
        print 'TOP SKILLS DESIRED:'
        for skill_desired, count in nlargest(int(top_number), skills_desired_dic.iteritems(), key=itemgetter(1)):                   
            print 'Top', top, ':', skill_desired, '#',count
            top +=1
            
            
# return continent given a country
def get_continent(country):
    
    for x  in countries.countries:
        if x['name'].lower().decode('utf-8') == country.lower():
            return x['continent']

# return number of users per country
def coursolvers_by_country(fp):
    
    total_coursolvers = 0

    for line in fp:
        keys = json.loads(line).keys()
        
        for x in keys:
            total_coursolvers +=1
            skills = json.loads(line)[x]
            for i in skills:
                
                if i == "Location":
                    location = skills[i]
                    if location in locations_dic.keys():
                        locations_dic[location] += 1 
                    else:
                        locations_dic[location] = 1

    print 'Total number of coursolvers is ', total_coursolvers
    for w in sorted(locations_dic, key=locations_dic.get, reverse=True):
        print w, locations_dic[w]
    
# return top_number of skills acquired and desired by continent requested    
def skills_by_continent(fp, continent_to_work, top_number):
    
    number_users = 0
    for line in fp:
 
        keys = json.loads(line).keys()
        
        for x in keys:
            skills = json.loads(line)[x]
            
            country = skills['Location']
            continent = get_continent(country)
            
            # if user continent not match the searched continent move to next user
            if not continent == continent_to_work and not continent_to_work == 'all':
                continue
            
            # count number of users
            number_users +=1
            
            for i in skills.keys():
                
                if i == "Desired Skills":
                    desired_skills = skills[i]
                    
                    for skill in desired_skills:
                        if skill in skills_desired_dic.keys():
                            skills_desired_dic[skill] += 1 
                        else:
                            skills_desired_dic[skill] = 1 

                if i == "Acquired Skills":
                    acquired_skills = skills[i]
                                        
                    for skill in acquired_skills:
                        if skill in skills_acquired_dic.keys():
                            skills_acquired_dic[skill] += 1 
                        else:
                            skills_acquired_dic[skill] = 1 
                            
        print ' --------- SKILLS STATISTICS FOR CONTINENT ', continent_to_work , ' ----------'                    
        print
        print ' --------- NUMBER OF USERS ANALYZED = ', number_users
        print
        print '---------> SKILLS ACQUIRED TOP ', top_number
        print
        for skill_acquired, count in nlargest(int(top_number), skills_acquired_dic.iteritems(), key=itemgetter(1)):                   
            print skill_acquired, count
        print
        print '---------> SKILLS DESIRED TOP ', top_number
        print
        for skill_desired, count in nlargest(int(top_number), skills_desired_dic.iteritems(), key=itemgetter(1)):                   
            print skill_desired, count

            #for w in sorted(skills_desired_dic, key=skills_desired_dic.get, reverse=True):
            #print continent_to_work
            #print w, skills_desired_dic[w]

# dump all skills into a file           
def dump_skills(fp, output_file):
    
    file = open(output_file,'w')

    # create an empty skills list
    list_skills = []
    
    for line in fp:
        keys = json.loads(line).keys()
        
        # the keys contain the userid
        for x in keys:
            user = json.loads(line)[x]
            
            # user_info contains user location, acquired and desired skills
            for user_info in user:
                if user_info == ("Desired Skills" or "Acquired Skills"):
                    for skill in user[user_info]:
                        # split the skill by , since there are cases where users put multiple skills in same line
                        skill_clean = re.split(r'(?<=[,.])(?<!\d.)\s', skill)
                        for a in skill_clean:
                            # trim spaces
                            a = a.strip()
                            a = a.strip(',')
                            list_skills.append(a)
       
    # remove the duplicates from the bag list_skills 
    list_skills = list(set(list_skills))  
    for i in list_skills:
        file.writelines(["%s\n" % item.encode('utf-8')  for item in list_skills])
    file.close()
    
def main():
    
    skills_file = open(sys.argv[1])
    operation = sys.argv[2]

    # HELP
    if operation == '--help':
        print 'print_coursolvers: print all coursolvers information'
        print 'coursolvers_by_country: number coursolvers by country'
        print 'most_popular_skills: most popular acquired and desired skills among coursolvers'
        print 'skills_by_continent: most popular acquired and desired skills among coursolvers by continent'
        print 'dump_skills: dump all the skills to a file'
        
    # PRINT ALL COURSOLVERS SKILLS
    if operation == 'print_coursolvers':
        print_coursolvers(skills_file)

    # NUMBER COURSOLVERS BY COUNTRY
    if operation == 'coursolvers_by_country':
        coursolvers_by_country(skills_file)
    
    # MOST POPULAR SKILLS
    elif operation == 'most_popular_skills':
        if not len(sys.argv) == 4:
            print 'Usage: explore.py $input_file most_popular_skills $top_number'
            return
        else:
            top_number = sys.argv[3]
            most_popular_skills(skills_file, top_number)
            
    # MOST POPULAR SKILLS BY CONTINENT        
    elif operation == 'skills_by_continent':
        if not len(sys.argv) == 5:
            print 'Usage: explore.py $input_file skills_by_continent $continent $top_number'
            return
        continent = sys.argv[3]
        top_number = sys.argv[4]
        skills_by_continent(skills_file , continent, top_number)
    
    # DUMP SKILLS TO FILE        
    elif operation == 'dump_skills':
        if not len(sys.argv) == 4:
            print 'Usage: explore.py $input_file dump_skills $output_file'
            return
        output_file = sys.argv[3]
        dump_skills(skills_file , output_file)

if __name__ == '__main__':
    main()
