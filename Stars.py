

#walk_distances = []
#while m<=numg:
#    wd = int(input("wd="))
#    walk_distances.append(wd)


def pos(t,wd,k,j):
    t = (t-wd)%(k*2*(j-1))
    b = (int(t/(2*(j-1)))+1)%4
    branch_walk_position = t % (2*(j-1))
    if branch_walk_position < j-1:
        #going up
        i= t % (j-1)
    else:
        #going down
        i = (j-1)-(t % (j-1) )
    if i==0:
        return(0,0)
    return (b,i)

def mon_g(t,wd,k,j):  #all vertices monitored by guard with walk dist wd
    b = pos(t,wd,k,j)[0]
    i = pos(t,wd,k,j)[1]
    if i==0:   #guard is on the root
        return {(b,1) for b in range(k)}.union({(0,0)})
    elif i==1:      #guard is not on root
        return {(0,0),(b,1),(b,2)}
    else:
        return {(b,i-1),(b,i),(b,i+1)}

def mon(t,walk_distances,k,j): #all vertices monitored by any of the guards at time t
    vertices = set()
    for wd in walk_distances:
        vertices = vertices.union(mon_g(t,wd,k,j))
    return vertices

def mon_times(b,i,walk_distances,k,j): #outputs the times at which vertex (b,i) is monitored
    d = {t: mon(t,walk_distances,k,j) for t in range(2*k*(j-1))}
    times = []
    for t in d:
        if (b,i) in d[t]:
            times.append(t)
    return times



def unmon_intervals(b,i,walk_distances,k,j): #returns unmonitored intervals for each vertex
    times = mon_times(b,i,walk_distances,k,j)
    unmon = []
    for n in range(1,len(times)):
        ut = times[n]-times[n-1]-1
        unmon.append(ut)
    #print(b,i,mon_times(b,i))
    unmon.append(2*k*(j-1)+(times[0]-times[-1]-1))
    return unmon



def mutv(b,i,walk_distances,k,j):  # the maximum of the length of unmonitored intervals of each vertex
    return max(unmon_intervals(b,i,walk_distances,k,j))

for i in range(1,8):
    print(f"v1{i}", mutv(1,i,[0,25],4,7))
#def autv(.....)

#def max_ave_ut_G:

#def ave_ave_ut_G:

def mutS(walk_distances,k,j): #the maximum of maximum of the length of unmonitored intervals of each vertex
    muts = [mutv(b,i,walk_distances,k,j) for b in range(k) for i in range(1,j+1)]
    muts.append(mutv(0,0,walk_distances,k,j))
    return max(muts)
#print (mutS([0,16,32], 4, 7))


def autS(walk_distances,k,j): #the average of maximum of the length of unmonitored intervals of each vertex
    muts = [mutv(b,i,walk_distances,k,j) for b in range(k) for i in range(1,j+1)]
    muts.append(mutv(0,0,walk_distances,k,j))
#    print("mutS=",muts)
    aut = sum(muts)/len(muts)

#    print(walk_distances)
    return aut
#print (autS([0,16,32],4,7))

def shared2_mutG(k,j): #assuming 2 guards, shared walk, output: the minimum(best) 
    mut_list = []      #of all maximum unmonitored times in all strategies
    for wd in range(2,2*k*(j-1)):
        my_distances = [0]
        my_distances.append(wd)
        mut_list.append(mutS(my_distances,k,j))
    min_mut = min(mut_list)
    min_wd = mut_list.index(min_mut)+2
    return (min_mut,min_wd)

def shared2_autG(k,j): #assuming 2 guards, shared walk, output: the minimum(best) 
    mut_list = []      #of all average unmonitored times in all strategies
    aut_list = []
    for wd in range(2,2*k*(j-1)):
        my_distances = [0]
        my_distances.append(wd)
        aut_list.append(autS(my_distances,k,j))
    min_aut =  min(aut_list)
    min_wd = aut_list.index(min_aut)+2
    return (min_aut,min_wd)

f = open("mut.txt","w")
f.write("k \t j \t d1 \t d2  \t d3 \t mutS \t autS \t \t mutG \t wd \t autG \t \t wd \n")
#print("k \t j \t d1 \t d2  \t d3 \t mutS \t autS \t \t mutG \t wd \t autG \t \t wd \n")


k=4
j=7
d1=0
for d2 in range (1,2*k*(j-1)-1):
    for d3 in range (1,2*k*(j-1)-d2):
    
        if d2>d3 or d2<d3 :
            #print("%d \t %d \t %d \t %d \t %d  \t %d \t %f \n" %(k,j,d1,d2,d3 ,mutS([d1,d2,d3],k,j), autS([d1,d2,d3], k,j) ))
            #f.write("%d \t %d \t %d \t %d \t %d  \t %d \t %f \n" %(k,j,d1,d2,d3 ,mutS([d1,d2,d3],k,j), autS([d1,d2,d3], k,j)  ))

#    wd,mutS(my_distances),autS(my_distances))
            f.close()
