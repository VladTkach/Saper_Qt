# class records to manage our records
class Record:
    def __init__(self, l1, l2, l3):
        self.record_lv1 = l1
        self.record_lv2 = l2
        self.record_lv3 = l3
    # update new records
    def setRecord(self, level, new_record):
        if level == 1:
            if self.record_lv1 > new_record and self.record_lv1 != 0:
                self.record_lv1 = new_record
            elif self.record_lv1 == 0:
                self.record_lv1 = new_record

        elif level == 2:
            if self.record_lv2 > new_record and self.record_lv2 != 0:
                self.record_lv2 = new_record
            elif self.record_lv2 == 0:
                self.record_lv2 = new_record
        else:
            if self.record_lv3 > new_record and self.record_lv3 != 0:
                self.record_lv3 = new_record
            elif self.record_lv3 == 0:
                self.record_lv3 = new_record

    # get zero to every records
    def setZero(self):
        self.record_lv1 = 0
        self.record_lv2 = 0
        self.record_lv3 = 0
