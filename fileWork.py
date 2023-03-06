from record import Record


# work with file to save records
class fileWork:
    def __init__(self, name):
        self.name = name
        self.setRecord()

    # cancel current records and write to the file
    def zeroFile(self):
        with open(self.name, "w") as inFile:
            for i in range(0, 3):
                inFile.write("level - " + str(i + 1) + ": 0\n")

    # update current records
    def updateFile(self):
        with open(self.name, "w") as inFile:
            inFile.write("level - 1: " + str(self.record.record_lv1) + " \n")
            inFile.write("level - 2: " + str(self.record.record_lv2) + " \n")
            inFile.write("level - 3: " + str(self.record.record_lv3) + " \n")

    # show file content
    def showFile(self):
        with open(self.name, "r") as outFile:
            line = outFile.readlines()
            print(line)

    # get records from the file
    def setRecord(self):
        with open(self.name, "r") as outFile:
            line = outFile.readline()
            list = line.split()
            l1 = int(list[-1])

            line = outFile.readline()
            list = line.split()
            l2 = int(list[-1])

            line = outFile.readline()
            list = line.split()
            l3 = int(list[-1])
        self.record = Record(l1, l2, l3)
