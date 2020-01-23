''' Written by Nicholas Skakal.
A class for converting dates to YYYY/MM/DD format. Format given must be
Month Day, Year (eg. January 1, 2000). '''

class dateConverter():

    # constructor method to define months and number of days in each month
    def __init__(self):
        self.months = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November",
                       "December"]
        self.thirty_months = ["04", "06", "09", "11"]
        self.thirtyone_months = ["01", "03", "05", "07", "08", "10", "12"]
        self.february = "02"

    ''' Purpose: driver function to convert a date
        Input: date as string (format: "January 1, 2000" (without quotes))
        Output: converted date (format: "2000/01/01" (without quotes), or None
                if invalid
        Assumptions: string is formatted correctly '''
    def convertDate(self, dateStr: str):
        # break date up into parts
        dateParts = dateStr.split(" ")

        ''' split() sometimes results in empty space in first position depending
            on input '''
        if dateParts[0] == "":
            mo = self.convertMonth(dateParts[1])
            dt = self.convertDay(dateParts[2].rstrip(",")) # date will include a comma at end
            yr = self.convertYear(dateParts[3])
        else:
            mo = self.convertMonth(dateParts[0])
            dt = self.convertDay(dateParts[1].rstrip(",")) # date will include a comma at end
            yr = self.convertYear(dateParts[2])

        # check if date is valid
        isValid = self.validDate(mo, dt, yr)

        if isValid:
            date = yr + "/" + mo + "/" + dt
            return date
        else:
            return None

    ''' Purpose: convert a month from word to number string
        Input: month as string (format: "January" (without quotes))
        Output: converted month (format: "01" (without quotes), or None if
                invalid
        Assumptions: string is formatted correctly '''
    def convertMonth(self, mo: str):
        if mo in self.months:
            moNum = self.padZeroes(str(self.months.index(mo) + 1), 2)
            return moNum
        else:
            return "00"

    ''' Purpose: convert a day from number to number string
        Input: month as string (format: "1" (without quotes))
        Output: converted month (format: "01" (without quotes), or None if
                invalid
        Assumptions: string is formatted correctly '''
    def convertDay(self, dt: str):
        if int(dt) <= 31:
            dtNum = self.padZeroes(dt, 2)
            return dtNum
        else:
            return "00"

    ''' Purpose: return year in correct format
        Input: year as string (format: "2000" (without quotes))
        Output: month (format: "2000" (without quotes), or None if not 4
                characters
        Assumptions: none '''
    def convertYear(self, yr: str):
        if len(yr) == 4:
            return yr
        else:
            return "0000"

    ''' Purpose: return string with required number of leading zeroes
        Input: toPad - string to add zeroes to
               length - length string should be when done
        Output: correctly formatted string
        Assumptions: none '''
    def padZeroes(self, toPad: str, length: int):
        numStr = toPad
        
        if len(numStr) == length:
            return numStr
        else:
            while (len(numStr) < length):
                numStr = "0" + toPad
            return numStr

    ''' Purpose: check if a date is valid
        Input: month - month of date to be checked
               day - day of date to be checked
               year - year of date to be checked
        Output: True if valid date, False otherwise
        Assumptions: month, day and year are in correct format (month and day
                     are two character number-strings, year is a four character
                     number-string '''
    def validDate(self, month: str, day: str, year: str):
        if month != "00" and day != "00" and year != "0000":
            if int(year) >= 2011:
                if month in self.thirty_months:
                    if int(day) <= 30 and int(day) > 0:
                        return True
                    else:
                        return False
                elif month in self.thirtyone_months:
                    if int(day) <= 31 and int(day) > 0:
                        return True
                    else:
                        return False
                elif month == self.february:
                    if int(year) % 4 == 0:
                        if int(day) <= 29 and int(day) > 0:
                            return True
                        else:
                            return False
                    else:
                        if int(day) <= 28 and int(day) > 0:
                            return True
                        else:
                            return False
                else:
                    return False
            else:
                return False
        else:
            return False

    ''' Purpose: compare two dates
        Input: dateOne - first date to be compared
               dateTwo - second date to be compared
        Output: True if dateOne is more recent than dateTwo, False otherwise
        Assumptions: dateOne and dateTwo are in correct format
                     (i.e., YYYY/MM/DD) '''
    def compareDates(self, dateOne: str, dateTwo: str):
        dateOneL = dateOne.split("/")
        dateTwoL = dateTwo.split("/")

        if int(dateOneL[0]) > int(dateTwoL[0]):
            return True
        else:
            if int(dateOneL[1]) > int(dateTwoL[1]):
                return True
            else:
                if int(dateOneL[2]) > int(dateTwoL[2]):
                    return True
                else:
                    return False
