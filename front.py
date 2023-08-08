from tkinter import *
from tkinter import messagebox
import back
from tkinter import filedialog as fd
Cities = {}
roads={}
road_name={}
road_name[0]=1
def hexGenerator(value):
    value = int(value)
    return "#" + str(value % 100) + str((value*2) % 100) + str((value*3) % 100)


def DecideRoadColor(rtype):
    if rtype == 1:
        return "red"
    elif rtype == 2:
        return "green"
    elif rtype == 3:
        return "blue"


class City:
    def __init__(self, name, positionX, positionY, width, length, height):
        self.name = name
        self.x = int(positionX)
        self.y = int(positionY)
        self.width = int(width)
        self.length = int(length)
        self.height = int(height)
        canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.length, width=2,
                                fill=DecideCityColor(int(self.height)), outline=DecideCityColor(int(self.height)))
        self.CityLabel = Label(root , text=self.name , background="White")
        self.CityLabel.place(x=self.x+(self.width/2) , y=self.y+(self.length/2))
        Cities[name]=self


class Road:
    def __init__(self, start: City, end: City, length, roadtype):
        self.name = road_name[0]
        self.start = start
        self.end = end
        self.length = length
        self.roadtype = roadtype
        canvas.create_line(start.x+(start.width/2), start.y+(start.length/2),
                           end.x+(end.width/2), end.y+(end.length/2), width=2, fill=DecideRoadColor(roadtype))
        roads[road_name[0]]=self
        road_name[0]+=1



root = Tk()
root.geometry("1200x700")
root.resizable(False, False)
canvas = Canvas()
canvas.configure(width=1200, height=450)


def DecideCityColor(height):
    return hexGenerator(height)

def CreateCity(name, positionX, positionY, width, length, height):
    positionX = int(positionX)
    positionY = int(positionY)
    width = int(width)
    length = int(length)
    height = int(height)
    for i in Cities.values():
        if ((positionX >= i.x and positionX <= (i.x + i.width)) or ((i.x + i.width) >= positionX and (i.x + i.width) <= (positionX + width))) and ((positionY >= i.y and positionY <= (i.y + i.length)) or ((i.y + i.length) >= positionY and (i.y + i.length) <= (positionY + length))):
            messagebox.showerror("Error" , "Bad Positions")
            return
        else : 
            city = City(name, positionX, positionY, width, length, height)
            back.add_area(name,positionX,positionY,width,length,height)
            return 
    city = City(name, positionX, positionY, width, length, height)
    back.add_area(name,positionX,positionY,width,length,height)
    return 
def CreateRoad(start, end, length, rtype):
    road = Road(start,end,length,rtype)
    back.add_road(road.name,start.name,end.name,int(length),int(rtype))
    return road

def deleteing_result_canvas(x,y):
    x.destroy()
    y.destroy()
def Search(start:str,end:str,search_type:bool=0,value:bool=0):
    #type=0-->shortest_path        value=0-->path
    #type=1-->fastest_path        value=1-->value
    result=tuple(())
    if search_type==True:
        if value==True:
            result=back.fastest_path(start,end)['time']
        else:
            result=back.fastest_path(start,end)['path']
    else:
        if value==True:
            result=back.shortest_path(start,end)["distance"]
        else:
            result=back.shortest_path(start,end)["path"]
    print(result)
    result_canvas = Canvas()
    result_canvas.configure(width=1200, height=450)
    result_canvas.place(x=0,y=0)
    backButton=Button(root, text="back to main map", command=lambda:deleteing_result_canvas(result_canvas,backButton))
    backButton.place(x=800,y=500)
    for x in result:
        if type(x)==type(int()):
            current_road=roads[x]
            result_canvas.create_line(current_road.start.x+(current_road.start.width/2), current_road.start.y+(current_road.start.length/2),
                           current_road.end.x+(current_road.end.width/2), current_road.end.y+(current_road.end.length/2), width=2, fill=DecideRoadColor(current_road.roadtype))
        else:
            current_city=Cities[x]
            result_canvas.create_rectangle(current_city.x, current_city.y, current_city.x+current_city.width, current_city.y+current_city.length, width=2,
                                fill=DecideCityColor(int(current_city.height)), outline=DecideCityColor(int(current_city.height)))
            current_city.CityLabel = Label(root , text=current_city.name , background="White")
            current_city.CityLabel.place(x=current_city.x+(current_city.width/2) , y=current_city.y+(current_city.length/2))
    
    
def ImportFile():
    file=open(fd.askopenfilename(),'rt')
    try:
        for x in file.read().split('\n'):
            data=x.split(',')
            if data[-1]=='ROAD':
                CreateRoad(Cities[data[1]],Cities[data[2]],data[3],int(data[4]))
            elif x=='':
                continue
            else:
                CreateCity(data[0],data[1],data[2],data[3],data[4],data[5])
        file.close()
        messagebox.showinfo('imported','file has been imported successfuly')
        return
    except:
        messagebox.showerror('error','there was a problem in exporting file')
        return

def ExportFile():
    file=fd.asksaveasfilename(filetypes=[('comma seperated value','csv'),])
    if back.export_data(file):
        messagebox.showinfo('file added',f'Data added in"{file}"')
    else:
        messagebox.showerror('error','there was a problem in exporting file')
        

canvas.place(x=0, y=0)
controlPanelTitle = Label(root, text="Control Panel")
controlPanelTitle.place(x=320, y=460)
# ==================================================================
AddingCityFrame = LabelFrame(root, text="Add City")
AddingCityFrame.place(x=20, y=480)
CityName = Entry(AddingCityFrame)
CityName.grid(row=0, column=0, padx=5, pady=5)
CityName.insert(0, "Enter City Name")
CityX = Entry(AddingCityFrame, width=5)
CityX.grid(row=0, column=10, padx=5)
CityX.insert(0, "X")
CityY = Entry(AddingCityFrame, width=5)
CityY.grid(row=0, column=20, padx=5)
CityY.insert(0, "Y")
CityWidth = Entry(AddingCityFrame, width=10)
CityWidth.grid(row=0, column=30, padx=5)
CityWidth.insert(0, "Width")
CityLength = Entry(AddingCityFrame, width=10)
CityLength.grid(row=0, column=40, padx=5)
CityLength.insert(0, "Length")
CityHeight = Entry(AddingCityFrame, width=10)
CityHeight.grid(row=0, column=50, padx=5)
CityHeight.insert(0, "Height")
CreateCityButton = Button(AddingCityFrame, text="Create", command=lambda: CreateCity(
    CityName.get(), CityX.get(), CityY.get(), CityWidth.get(), CityLength.get(), CityHeight.get()))
CreateCityButton.grid(row=0, column=60, padx=5)
# ==================================================================
AddingRoadFrame = LabelFrame(root, text="Add Road")
AddingRoadFrame.place(x=20, y=540)
CityA = Entry(AddingRoadFrame)
CityA.grid(row=0, column=0, padx=5, pady=5)
CityA.insert(0, "City A Name")
CityB = Entry(AddingRoadFrame)
CityB.grid(row=0, column=10, padx=5, pady=5)
CityB.insert(0, "City B Name")
RoadLength = Entry(AddingRoadFrame, width=10)
RoadLength.grid(row=0, column=20, padx=5, pady=5)
RoadLength.insert(0, "Length")
RoadType = Entry(AddingRoadFrame, width=10)
RoadType.grid(row=0, column=30, padx=5, pady=5)
RoadType.insert(0, "Type")
CreateRoadButton = Button(AddingRoadFrame, text="Create Road", command=lambda: CreateRoad(Cities[CityA.get()], Cities[CityB.get()],int(RoadLength.get()), int(RoadType.get())))
CreateRoadButton.grid(row=0, column=40, padx=5, pady=5)
SearchFrame = LabelFrame(root, text="Search Shortest Path Between 2 Cities")
SearchFrame.place(x=20, y=600)
SearchCityA = Entry(SearchFrame)
SearchCityA.grid(row=0, column=0, padx=5, pady=5)
SearchCityA.insert(0, "City A")
SearchCityB = Entry(SearchFrame)
SearchCityB.grid(row=0, column=10, padx=5, pady=5)
SearchCityB.insert(0, "City B")
SearchButton = Button(SearchFrame, text="Search", command=lambda: Search(SearchCityA.get() , SearchCityB.get()))
SearchButton.grid(row=0, column=20, padx=5, pady=5)
FileFrame = LabelFrame(root , text="File ")
FileFrame.place(x=350 , y=600)
# ImportFileInput = fd.askopenfilename()
ImportDataButton = Button(FileFrame , text="Import Data" , command=lambda : ImportFile())
ImportDataButton.grid(row=0,column=10,padx=5,pady=5)
ExportFileButton = Button(FileFrame , text="Export File" , command=lambda : ExportFile())
ExportFileButton.grid(row=0,column=0,padx=5,pady=5)
root.mainloop()
