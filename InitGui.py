import FreeCADGui
from StructuralMember import StructuralMemberCommand

class Weldments(FreeCADGui.Workbench):
    MenuText = "Weldments"
    ToolTip = "Design of metalworking parts and assemblies"
    Icon = """
    /* XPM */
    static char * weldments_xpm[] = {
    "32 32 4 1",
    " 	c None",
    ".	c #1E1E1E",
    "+	c #FF9800",
    "@	c #FFFFFF",
    "                                ",
    "                                ",
    "        ..............          ",
    "       ..++++++++++++..         ",
    "      ..++++++++++++++..        ",
    "     ..+++++++....++++++..      ",
    "     .+++++++......++++++.      ",
    "     .++++++........++++++.     ",
    "     .+++++..........+++++.     ",
    "     .+++++..........+++++.     ",
    "     .+++++....@@@@....++++.     ",
    "     .+++++....@@@@....++++.     ",
    "     .+++++..........+++++.     ",
    "     .+++++..........+++++.     ",
    "     .++++++........++++++.     ",
    "     .+++++++......++++++.      ",
    "     ..+++++++....++++++..      ",
    "      ..++++++++++++++++..      ",
    "       ..++++++++++++++..       ",
    "        ..............          ",
    "                                ",
    "           @@@@@@@@             ",
    "          @@@@@@@@@@            ",
    "         @@@@      @@           ",
    "        @@@         @@          ",
    "       @@@           @@         ",
    "      @@@             @@        ",
    "     @@@               @@       ",
    "                                ",
    "                                ",
    "                                ",
    "                                "
    };
    """

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
