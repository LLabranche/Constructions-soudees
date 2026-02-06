import FreeCAD, FreeCADGui, Part


class StructuralMemberCommand:
    def GetResources(self):
        return {
            "Pixmap": """
/* XPM */
static char * StructuralMember_xpm[] = {
"20 20 124 2",
"  	c None",
". 	c #444444",
"+ 	c #434343",
"@ 	c #3B3B3B",
"# 	c #323232",
"$ 	c #404040",
"% 	c #4C4C4C",
"& 	c #424242",
"* 	c #5C5C5C",
"= 	c #8B8B8B",
"- 	c #ABABAB",
"; 	c #CBCBCB",
"> 	c #D8D8D8",
", 	c #B4B4B4",
"' 	c #4B4B4B",
") 	c #3C3C3C",
"! 	c #686868",
"~ 	c #A8A8A8",
"{ 	c #F4F4F4",
"] 	c #FDFDFD",
"^ 	c #FCFCFC",
"/ 	c #FBFBFB",
"( 	c #F9F9F9",
"_ 	c #F8F8F8",
": 	c #F7F7F7",
"< 	c #A4A4A4",
"[ 	c #363636",
"} 	c #787878",
"| 	c #878787",
"1 	c #A9A9A9",
"2 	c #E5E5E5",
"3 	c #FAFAFA",
"4 	c #F6F6F6",
"5 	c #F1F1F1",
"6 	c #D1D1D1",
"7 	c #B1B1B1",
"8 	c #676767",
"9 	c #3E3E3E",
"0 	c #949494",
"a 	c #DDDDDD",
"b 	c #B5B5B5",
"c 	c #7D7D7D",
"d 	c #B8B8B8",
"e 	c #DADADA",
"f 	c #BABABA",
"g 	c #959595",
"h 	c #7B7B7B",
"i 	c #989898",
"j 	c #B9B9B9",
"k 	c #D7D7D7",
"l 	c #838383",
"m 	c #3D3D3D",
"n 	c #AEAEAE",
"o 	c #858585",
"p 	c #C4C4C4",
"q 	c #979797",
"r 	c #888888",
"s 	c #C9C9C9",
"t 	c #F5F5F5",
"u 	c #F3F3F3",
"v 	c #F0F0F0",
"w 	c #B6B6B6",
"x 	c #8D8D8D",
"y 	c #ADADAD",
"z 	c #E0E0E0",
"A 	c #B0B0B0",
"B 	c #EDEDED",
"C 	c #EEEEEE",
"D 	c #BEBEBE",
"E 	c #EFEFEF",
"F 	c #6B6B6B",
"G 	c #666666",
"H 	c #626262",
"I 	c #646464",
"J 	c #717171",
"K 	c #8E8E8E",
"L 	c #EBEBEB",
"M 	c #ECECEC",
"N 	c #E9E9E9",
"O 	c #E6E6E6",
"P 	c #6D6D6D",
"Q 	c #4A4A4A",
"R 	c #5B5B5B",
"S 	c #727272",
"T 	c #E8E8E8",
"U 	c #E1E1E1",
"V 	c #DEDEDE",
"W 	c #373737",
"X 	c #808080",
"Y 	c #A6A6A6",
"Z 	c #E3E3E3",
"` 	c #DCDCDC",
" .	c #D9D9D9",
"..	c #575757",
"+.	c #5D5D5D",
"@.	c #383838",
"#.	c #9A9A9A",
"$.	c #D3D3D3",
"%.	c #333333",
"&.	c #7F7F7F",
"*.	c #343434",
"=.	c #939393",
"-.	c #D5D5D5",
";.	c #D2D2D2",
">.	c #CECECE",
",.	c #828282",
"'.	c #757575",
").	c #8C8C8C",
"!.	c #CDCDCD",
"~.	c #CACACA",
"{.	c #A2A2A2",
"].	c #C5C5C5",
"^.	c #B3B3B3",
"/.	c #BFBFBF",
"(.	c #ACACAC",
"_.	c #3F3F3F",
":.	c #E4E4E4",
"<.	c #E2E2E2",
"[.	c #9F9F9F",
"}.	c #595959",
"|.	c #454545",
"1.	c #515151",
"2.	c #B2B2B2",
"3.	c #494949",
"                                        ",
"              . + @ # $                 ",
"        % & * = - ; > , ' $             ",
"      ) ! ~ { ] ^ / ( _ : < ' $         ",
"    [ } | 1 2 / 3 ( _ 4 5 6 7 8 9       ",
"    # 0 a b c d 4 e f g h i j k l m     ",
"    # n o ; p q } r 1 s 2 t u 5 v #     ",
"    # u , c w x y _ : z A = x d B #     ",
"    # v C D } } E D F G H I J K L #     ",
"    # M N O 6 } t P Q # R S = } T #     ",
"    # T 2 U V } u W   # ) X Y } 2 #     ",
"    # Z z `  .} 5 ..# $ +.@.#.} Z #     ",
"    # V e k $.} C } ..%.J } @.&.z #     ",
"    *.=.-.;.>.} M } g ,.W '.).A V #     ",
"      m Y !.~.} N = {.1 x q j $.r @     ",
"        # ).].} O ^.= | /.$.(.I _.      ",
"          # ,.} :.<.z ; [.}.. |.        ",
"            # 1.2.Y &.* 3.              ",
"              @.W 9 |.                  ",
"                                        "};

""",
            "MenuText": "StructuralMember",
            'ToolTip': 'Ajoute un élément structurel simple',
        }

    def IsActive(self):
        return True

    def Activated(self):
        import FreeCAD
        import FreeCADGui
        from FreeCAD import Vector
        import FreeCAD as App
        import Part
        from PySide2 import QtWidgets, QtCore
        import math
        import Sketcher

        profile_data = {
            "Tube rond": ["17.2x2", "20x1.5", "20x2", "21.3x2"], #1
            "Tube rectangulaire": ["30x15x1.5", "30x20x2", "35x20x2"],
            "Tube carré": ["20x20x2", "25x25x1.5", "25x25x2"]
        }

        def parse_dimensions(profile_type, dimension_str):
            parts = dimension_str.split("x")
            if len(parts) == 1:
                return float(parts[0]), None, None
            if len(parts) == 2:
                return float(parts[0]), float(parts[1]), None
            if len(parts) == 3:
                return float(parts[0]), float(parts[1]), float(parts[2])

        class ProfileTaskPanel:
            def __init__(self):
                # Initialiser variables
                self.body = []
                self.shapebinder = []
                self.sketch = []
                self.additivepipe = []

                self.form = QtWidgets.QWidget()
                self.layout = QtWidgets.QVBoxLayout(self.form)

                # Famille de profil
                self.family_label = QtWidgets.QLabel("Famille de profil :")
                self.family_combo = QtWidgets.QComboBox()
                self.family_combo.addItems(profile_data.keys())

                # Dimensions
                self.dim_label = QtWidgets.QLabel("Dimensions :")
                self.dim_combo = QtWidgets.QComboBox()

                # Symétrie
                self.symmetry_checkbox = QtWidgets.QCheckBox("Symétriser le profil")

                # Rotation
                self.rotation_label = QtWidgets.QLabel("Rotation du profil (°) :")
                self.rotation_input = QtWidgets.QLineEdit()
                self.rotation_input.setPlaceholderText("0.0")

                # Décalage X
                self.offset_x_label = QtWidgets.QLabel("Décalage X (mm) :")
                self.offset_x_input = QtWidgets.QLineEdit()
                self.offset_x_input.setPlaceholderText("0.0")

                # Décalage Y
                self.offset_y_label = QtWidgets.QLabel("Décalage Y (mm) :")
                self.offset_y_input = QtWidgets.QLineEdit()
                self.offset_y_input.setPlaceholderText("0.0")

                # Aide
                self.select_line_label = QtWidgets.QLabel(
                    "<b>Veuillez sélectionner une ligne dans la vue 3D.</b>"
                )

                # Ajouter au layout
                self.layout.addWidget(self.family_label)
                self.layout.addWidget(self.family_combo)
                self.layout.addWidget(self.dim_label)
                self.layout.addWidget(self.dim_combo)
                self.layout.addSpacing(10)
                self.layout.addWidget(self.symmetry_checkbox)
                self.layout.addSpacing(10)
                self.layout.addWidget(self.rotation_label)
                self.layout.addWidget(self.rotation_input)
                self.layout.addWidget(self.offset_x_label)
                self.layout.addWidget(self.offset_x_input)
                self.layout.addWidget(self.offset_y_label)
                self.layout.addWidget(self.offset_y_input)
                self.layout.addSpacing(10)
                self.layout.addWidget(self.select_line_label)

                # Connexions des signaux
                self.family_combo.currentTextChanged.connect(self.update_dimensions)
                self.family_combo.currentTextChanged.connect(self.update_preview)
                self.dim_combo.currentTextChanged.connect(self.update_preview)
                self.symmetry_checkbox.stateChanged.connect(self.update_preview)
                self.rotation_input.textChanged.connect(self.update_preview)
                self.offset_x_input.textChanged.connect(self.update_preview)
                self.offset_y_input.textChanged.connect(self.update_preview)

                # Initialiser les dimensions
                self.update_dimensions(self.family_combo.currentText())

            def update_dimensions(self, selected_family):
                self.dim_combo.blockSignals(True)
                self.dim_combo.clear()
                if selected_family in profile_data:
                    self.dim_combo.addItems(profile_data[selected_family])
                self.dim_combo.blockSignals(False)
                self.update_preview()
                
            def update_preview(self):
                doc = App.activeDocument()
                selection = FreeCADGui.Selection.getSelectionEx()

                # Supprimer l'ancien aperçu
                for i in range(len(self.body)):
                    doc.removeObject(self.body[i].Name)
                    doc.removeObject(self.shapebinder[i].Name)
                    doc.removeObject(self.sketch[i].Name)
                    doc.removeObject(self.additivepipe[i].Name)
                    doc.recompute()
                self.body = []
                self.shapebinder = []
                self.sketch = []
                self.additivepipe = []  
                
                # check si il y a une selection
                if not selection or not selection[0].SubObjects:
                    return

                try:
                    family = self.family_combo.currentText()
                    dimension = self.dim_combo.currentText()
                    symmetry = self.symmetry_checkbox.isChecked()
                    try:
                        rotation = float(self.rotation_input.text())
                    except ValueError:
                        rotation = 0.0
                    try:
                        offset_x = float(self.offset_x_input.text())
                    except ValueError:
                        offset_x = 0.0
                    try:
                        offset_y = float(self.offset_y_input.text())
                    except ValueError:
                        offset_y = 0.0

                    dim1, dim2, dim3 = parse_dimensions(family, dimension)
                    if symmetry == True:
                        angle = 180
                    else:
                        angle = 0

                    counter = 0
                    for n in range(len(selection)): #Pour chaque objet selectionné
                        objselect = selection[n].SubObjects
                        for i in range(len(objselect)): #pour chaque sous objet selectionné
                            if isinstance(objselect[i], Part.Edge): #Si c'est une ligne
                                # Créer un nouveau corps
                                self.body.append(doc.addObject("PartDesign::Body", family + " " + dimension + " "))
                                doc.recompute()

                                # Creer une reference externe
                                self.shapebinder.append(self.body[counter].newObject('PartDesign::ShapeBinder','ShapeBinder'))
                                self.shapebinder[counter].Support = [(selection[n].Object, selection[n].SubElementNames[i])]
                                self.shapebinder[counter].Visibility = False
                                doc.recompute()

                                # Créer une esquisse dans le corps et ancrer sur la ligne de la forme lier
                                self.sketch.append(self.body[counter].newObject('Sketcher::SketchObject', "Profile "))
                                self.sketch[counter].AttachmentSupport = [(self.shapebinder[counter], 'Edge1')]
                                self.sketch[counter].MapMode = 'NormalToEdge'
                                self.sketch[counter].AttachmentOffset = App.Placement(App.Vector(offset_x,offset_y,0), App.Rotation(rotation, 0, angle))
                                self.sketch[counter].Visibility = False
                                doc.recompute()

                                # Créer la forme
                                if family == "Tube rond":
                                    radius = dim1 / 2
                                    thickness = dim2
                                    self.sketch[counter].addGeometry(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), radius))
                                    self.sketch[counter].addGeometry(Part.Circle(App.Vector(0.000000, 0.000000, 0.000000), App.Vector(0.000000, 0.000000, 1.000000), radius-thickness))
                                    doc.recompute()

                                elif family == "Tube rectangulaire" or family == "Tube carré":
                                    width = dim1
                                    height = dim2
                                    thickness = dim3
                                    self.sketch[counter].addGeometry(Part.LineSegment(App.Vector(-25.000000, -25.000000, 0.000000),App.Vector(25.000000, -25.000000, 0.000000)))
                                    self.sketch[counter].addGeometry(Part.LineSegment(App.Vector(25.000000, -25.000000, 0.000000),App.Vector(25.000000, 25.000000, 0.000000)))
                                    self.sketch[counter].addGeometry(Part.LineSegment(App.Vector(25.000000, 25.000000, 0.000000),App.Vector(-25.000000, 25.000000, 0.000000)))
                                    self.sketch[counter].addGeometry(Part.LineSegment(App.Vector(-25.000000, 25.000000, 0.000000),App.Vector(-25.000000, -25.000000, 0.000000)))
                                    doc.recompute()

                                #creer balayage de mon esquisse sur ma ligne
                                self.additivepipe.append(self.body[counter].newObject('PartDesign::AdditivePipe','AdditivePipe'))
                                self.additivepipe[counter].Profile = self.sketch[counter]
                                self.additivepipe[counter].Spine = (self.shapebinder[counter], 'Edge1')
                                doc.recompute()

                                counter=counter+1



                except Exception as e:
                    FreeCAD.Console.PrintError(f"Erreur d'aperçu : {e=}\n")

            def accept(self):
                return True

            def reject(self):
                doc = App.activeDocument()
                for i in range(len(self.body)):
                    doc.removeObject(self.body[i].Name)
                    doc.removeObject(self.shapebinder[i].Name)
                    doc.removeObject(self.sketch[i].Name)
                    doc.removeObject(self.additivepipe[i].Name)
                    doc.recompute()
                FreeCAD.Console.PrintMessage("Opération annulée.\n")
                return True

        panel = ProfileTaskPanel()
        FreeCADGui.Control.showDialog(panel)
