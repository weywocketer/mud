import npyscreen

class MyForm(npyscreen.Form):
    def create(self):
        self.myText = self.add(npyscreen.Textfield, editable=False, value="spam! "*8)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MyForm, name="my beautiful TUI")


app = MyApplication()
app.run()