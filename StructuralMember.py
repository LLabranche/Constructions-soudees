import FreeCAD, FreeCADGui, Part


class StructuralMemberCommand:
    def GetResources(self):
        return {
            "Pixmap": "C:\Program Files\FreeCAD 1.0\Mod\Weldments\Resources\Icons\StructuralMember.png",
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