import FreeCADGui
from StructuralMember import StructuralMemberCommand

class Weldments(FreeCADGui.Workbench):
    MenuText = "Weldments"
    ToolTip = "Design of metalworking parts and assemblies"
    Icon = "C:\Program Files\FreeCAD 1.0\Mod\Weldments\Resources\Icons\Weldments.png"

    def Initialize(self):

        from StructuralMember import StructuralMemberCommand

        FreeCADGui.addCommand('StructuralMember', StructuralMemberCommand())

        # Définir les commandes disponibles
        self.appendToolbar("Outils Structure", ["StructuralMember"])
        self.appendMenu("Structure", ["StructuralMember"])

    def Activated(self):
        print("Mon Atelier est activé")

    def Deactivated(self):
        print("Mon Atelier est désactivé")

    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(Weldments())