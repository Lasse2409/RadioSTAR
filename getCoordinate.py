from src.Coordinate_transforms import coordinates


observer = [55.3959, 10.3883, 17] #define location of observer [altitude, latitude, longitude]
dateAndTime = [2023, 5, 16, 18, 43, 0] #defining date and time [year, month, day, hour, minute, second]



obj = coordinates.getObject('moon', dateAndTime, observer, now=True)
print(obj)

