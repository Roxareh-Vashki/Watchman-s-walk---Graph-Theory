import itertools as it
import math
#n is the number of vertices in the path
#a vertex is represented by an index from 0 to n-1
#g = (v0,turn1,turn2) is a guard who starts on vertex v0 at t=0, travels towards vertex turn1, then turns and walks to turn2, and repeat.
#m is the number of guards
#S is a list of distances between guards in a shared walk strategy
def period(g):
    return 2*abs(g[2]-g[1])

def all_guards(n): #creates all possible single guard strategies on a graph with n vertices, as list of order ~n^3
    strats = list()
    for turn1 in range(1,n-1):
        for turn2 in range(1,n-1):
            vL=min(turn1,turn2)
            vR=max(turn1,turn2)
            for v in range(vL,vR+1):
                strats.append([v,turn1,turn2])
    return strats

def monitored(g):
    #g is a guard [v,turn1,turn2]
    #returns all vertices monitored by g wihtin the period, as a subset
    vL = min(g[1],g[2])
    vR = max(g[1],g[2])
    vertices = set(i for i in range(vL-1,vR+2))
    return vertices

def is_good(strategy,n):
     #strategy is a list of guards
     #returns True if the guards collectively monitor all vertices in Pn
     vertices = set()
     for g in strategy:
         vertices = vertices.union(monitored(g))
     if len(vertices)==n:
         return True
     return False

def good_strategies(n,m):
    #returns all the good m-guard strategies for Pn
    guards = all_guards(n)
    num_guards = len(guards)
    strategy = it.combinations(guards,m) #creates iterator of all possible 3 guard strategies
    good = []
    for l in range(math.factorial(num_guards)//(math.factorial(m)*math.factorial(num_guards-m))):
        S = next(strategy)
        if is_good(S,n):
            good.append(S)
    return good

#print(good_strategies(11,2))



#g = (v,turn1,turn2) is a guard who starts on vertex v at t=0,
#travels towards vertex turn1, then turns and walks to turn2, and repeat.
# for example, g = (4,2,7) is different from g=(4,7,2)
g=(4,2,7)
    #returns the vertex of a guard g at time t
def position(g,time):
    v=g[0]
    turn1=g[1]
    turn2=g[2]
    vL= min(turn1,turn2)
    vR= max(turn1,turn2)
    p = period(g)
    if p==0:
        return g[0]
    t = time%p

    if v>turn1:
        if t<((v - vL)+1):
            return (v - t)
        if t<((vR-vL)+ (v-vL)) and t>( v - vL):
                return t+(vL-(v-vL))
        else:
            return p-t+v

    if v<=turn1:
        if t<((vR - v)+1):
            return (v + t)
        if t>(vR-v) and t<(vR-v + vR-vL):
            return vR-(t-(vR-v))
        else:
            return v-(p-t)

def vertices_monitored_by_g(g,t):
    #returns the set of vertices of Pn monitored by a guard g, at time t
    return [(position(g,t))-1, position(g,t), position(g,t)+1]

def lcm(a):
    l = a[0]
    for i in a[1:]:
        l = l*i//math.gcd(l, i)
    return l


def strategy_period(S):
    nonzero_periods = [period(g) for g in S if period(g)>0]
    if nonzero_periods==[]:
        return(1)
    else:
        return lcm(nonzero_periods)
    

#S is a "strategy", an m-tuple of guards, each a 3-tuple
def vertices_monitored(S,t):
    #returns the set of vertices of G monitored by *any* guard in strategy S at time t
    vertices = set()
    for g in S:
        vertices = vertices.union(vertices_monitored_by_g(g,t))
    return vertices


def monitored_times(S,v):
    #returns a list of the times at which vertex v is monitored via strategy S
    periods = (period(g) for g in S)
    p = strategy_period(S)
    times = []
    for t in range(p):
        if v in vertices_monitored(S,t):
            times.append(t)
    return times


#print(t, monitored_times(S,t))
def unmonitored_intervals(S,v):
    #returns a list of the unmonitored interval lengths for vertex v under strategy S
    times = monitored_times(S,v)
    unmon = []
    p = strategy_period(S)
    for i in range(1,len(times)):
        ut = times[i]-times[i-1]-1
        unmon.append(ut)

    unmon.append(p+(times[0]-times[-1]-1))
    return unmon

def unmonitored_time(S,v):
    #returns the maximum length of time that vertex v is unmonitored in strategy S
    return max(unmonitored_intervals(S,v))
g1 = (2,1,28)
g2 = (8,1,28)
g3 = (14,1,28)
g4 = (21,1,28)
g5 = (27,1,28)


S = (g1,g2,g3,g4,g5)
#for i in range(0, 30):
 #   print("V", i+1 , ":" ,  "unmonitored_intervals: ",unmonitored_intervals(S, i), " unmonitored_time:" , unmonitored_time(S, i))
   # print("V", i+1 , ":" , "monitored_times:" , monitored_times(S,i), "unmonitored_intervals: ",unmonitored_intervals(S, i), " unmonitored_time:" , unmonitored_time(S, i))


def unmonitored_time_list(n,S):
    #returns a list of the unmonitored times of the vertices in Pn
    return [unmonitored_time(S,v) for v in range(n)]


def max_unmonitored_time(n,S):
    #returns the max unmonitored time over all vertices, for fixed S
    return max(unmonitored_time_list(n,S))

def average_unmonitored_time(n,S):
    #returns the average unmonitored time over all vertices, for fixed S
    ut_list = unmonitored_time_list(n,S)
    return sum(ut_list)/len(ut_list)




def min_max_unmonitored_time(n,m):
    list_of_strategies = good_strategies(n,m)
    mut_list = [max_unmonitored_time(n,S) for S in list_of_strategies]
    min_mut = min(mut_list)
    best_strategies = [S for S in list_of_strategies if max_unmonitored_time(n,S)==min_mut]
    return (min_mut,best_strategies)



def min_ave_unmonitored_time(n,m):
    #returns the minimum ave_unmon_time over all possible *shared* stragies S with m guards
    list_of_strategies = good_strategies(n,m)
    #aut_list = [average_unmonitored_time(n,S) for S in list_of_strategies]
    best_strategies = []
    period_S = []
    min_ave=2*(n-3)
    count = 0
    for S in list_of_strategies:
        count = count + 1
        autS = average_unmonitored_time(n,S)
        if autS<=min_ave:
            best_strategies.append(S)
            period_S.append(strategy_period(S))
            if autS<min_ave:
                min_ave=autS
                best_strategies=[S]
                period_S.append(strategy_period(S))
                
        #if (count % 1000) == 0:
            #print (count)
    return (min_ave, best_strategies, period_S )


#for n in range(4,30):
   # for m in range(2,4):
        #print("n= ", n, " , ", "m= ", m, min_ave_unmonitored_time(n, m))

#def m_guards_disjoint_str(n,m):
c=0    
for j in range(1,24):
    g1= (1,1,23)
    g2= (j,23,1)
    g3= (j,1,23)
    S = (g1,g2)
    c=c+1
    print( c ,"g1:", g1, "g2:", g2, unmonitored_time_list(25, S), "aut" , average_unmonitored_time(25,S)) 
   
   



       
def difference (list1, list2):
    list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2 ]  # 
    return list_dif

for n in range(9,10):
    for m in range(2,3):
        list1= min_max_unmonitored_time(n, m)[1]
        list2= min_ave_unmonitored_time(n, m)[1] 
        #print("n=", n , "m=" , m ,"difference" , difference(list1, list2))
     


f = open("list_dif.txt","w")
#f.write("n \t m \t min_max \t min_ave \n")
#print("n \t m \t min_max \t min_ave \n")  
      
for n in range(4,30):
    for m in range(2,3):
      # print("%d \t %d \t %d \t %f \n" %(n, m , min_max_unmonitored_time(n, m)[0] , min_ave_unmonitored_time(n, m)[0] ))
        #f.write("%d \t %d \t %d \t %f \n" %(n, m, min_max_unmonitored_time(n, m)[0] , min_ave_unmonitored_time(n, m)[0] ))

        f.close()
        







