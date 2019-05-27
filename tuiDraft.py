import npyscreen
import time
import threading

class Thread1(threading.Thread):
    def run(self):
        runTUI()

        '''
        for i in range(10):
            print("thread 1: i = " + str(i))
            time.sleep(1)
        '''

class Thread2(threading.Thread):
    def run(self):

        time.sleep(1)
        TestApp.getForm('MAIN').myName.value = "pies"
        TestApp.getForm('MAIN').display()
        time.sleep(1)
        TestApp.getForm('MAIN').myName.value = "nicpon"
        TestApp.getForm('MAIN').display()
        time.sleep(1)
        TestApp.getForm('MAIN').myName.value = "kot"
        TestApp.getForm('MAIN').display()
        time.sleep(1)
        TestApp.getForm('MAIN').myName.value = "żuk"
        TestApp.getForm('MAIN').display()



        #print(TestApp.getForm('MAIN').myName.value)

        for i in range(10):
            TestApp.getForm('MAIN').myName.value = str(i)
            TestApp.getForm('MAIN').myName.display()
            time.sleep(1)


def runTUI():
    TestApp.run()

class myEmployeeForm(npyscreen.Form):
    def create(self):
        self.myName        = self.add(npyscreen.TitleText, name='Name')
        self.myDepartment  = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3,
                                     name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
        self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class Experiment(npyscreen.Form):
    def create(self):
        self.myName        = self.add(npyscreen.TitleText, name='Name', editable=False, value=14)
        self.myDepartment  = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3,
                                     name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
        self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')
        self.user_input    = self.add(npyscreen.TextfieldUnicode)
        self.user_input2 = self.add(npyscreen.Autocomplete)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', Experiment, name='New Employee')
        self.addForm('second', Experiment, name='old Employee')


if __name__ == '__main__':
    TestApp = MyApplication()

    thread1 = Thread1()
    thread2 = Thread2()

    thread1.start()
    thread2.start()




# FormBaseNew