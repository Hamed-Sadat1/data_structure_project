import heapq

road_types={1:40,2:80,3:110}
#roads has three types
#1=between 20 and 60
#2=80->between 60 and 100
#3=110->between 100 and 120
#speed of roads will be thair average of min and max speed

areas={}   #a dictionary that saves areas,key is name and value is object of area
added_data = ""   #a string for recording roads and areas to be exported easily


#creating classes
#creating area class
class area:
    def __init__(self,name):
        self.name=name
        self.ways=set(())#this attribute will show every area neighborhoods and road that connected them
                         #fromat will be-->{(area1,road1),(area2,road2),(area3,road3),...}
        
#creating road class
class road:
    def __init__(self,name,length,rtype):
        self.name=name
        self.length=length
        self.speed=road_types[rtype]


def add_area(name , positionX , positionY , width , length , height):
    '''this function will act like an api,it will create an area instance and save its data for exporting data file '''
    areas[name]=area(name)
    global added_data
    added_data=added_data+f'{name},{positionX},{positionY},{width},{length},{height}\n'


def add_road(name,area1,area2,length,rtype):
    '''this function will act like an api,it will create a road instance and save its data for exporting data file '''
    current_road=road(name,length,rtype)
    areas[area1].ways.add((areas[area2],current_road))
    areas[area2].ways.add((areas[area1],current_road))
    
    global added_data
    added_data=added_data+f'{name},{area1},{area2},{length},{rtype},ROAD\n'
    
def shortest_path(starting_area,destination):
    '''this function will find shortest path and its length using dijkstra's algorithm with heap''' 
    pq =[]
    dist={}
    path={}
    dist[starting_area]=0
    path[starting_area]=(starting_area,)
    heapq.heappush(pq, (0, starting_area))
    
    while pq:
        current=heapq.heappop(pq)[1]
        for city,road in areas[current].ways:
            city_name=city.name
            if dist.setdefault(city_name,float('inf')) > dist[current]+road.length:
                    dist[city_name]=dist[current]+road.length
                    heapq.heappush(pq, (dist[city_name], city_name))
                    path[city_name]=path[current]+(road.name,city_name)
    
    return {'path':path[destination],'distance':dist[destination]}

def fastest_path(starting_area,destination):
    '''this function will find fastest path and its time using dijkstra's algorithm''' 
    pq =[]
    time={}
    path={}
    time[starting_area]=0
    path[starting_area]=(starting_area,)
    heapq.heappush(pq, (0, starting_area))
    while pq:
        current=heapq.heappop(pq)[1]
        for city,road in areas[current].ways:
            city_name=city.name
            if time.setdefault(city_name,float('inf')) > time[current]+(road.length/road.speed):
                    time[city_name]=time[current]+(road.length/road.speed)
                    heapq.heappush(pq, (time[city_name], city_name))
                    path[city_name]=path[current]+(road.name,city_name)
    
    return {'path':path[destination],'time':time[destination]}

def export_data(file_path='data.csv'):
    global added_data
    try:
        file=open(file_path,'wt')
        file.write(added_data)
        file.close()
        return True
    except:
        return False