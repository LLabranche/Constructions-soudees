class StructuralMemberCommand:

    def GetResources(self):
        import os
        return {
            "Pixmap": os.path.join(os.path.dirname(__file__), "icons", "StructuralMember.png" ),
            "MenuText": "Elément mécano-soudé",
            'ToolTip': 'Ajouter un profil mécano-soudé',
        }

    def IsActive(self):
        return True

    def Activated(self):
        import FreeCAD as App
        import FreeCADGui as Gui
        import Part
        import os
        from PySide import QtWidgets, QtGui, QtCore

        PROFILE_DIR = os.path.join(os.path.dirname(__file__), "profiles")

        class ProfileSweepTaskPanel:

            def __init__(self):
                # Initialiser variables
                self.body = []
                self.shapebinder = []
                self.sketch = []
                self.additivepipe = []
                self.selected_edges = []

                # ---------------- UI ----------------
                self.form = QtWidgets.QWidget()
                self.form.setWindowTitle("Profilés mecano")
                
                self.layout = QtWidgets.QVBoxLayout(self.form)

                self.family_label = QtWidgets.QLabel("Famille de profil :")
                self.family_combo = QtWidgets.QComboBox()

                self.profil_label = QtWidgets.QLabel("Profil :")
                self.profil_combo = QtWidgets.QComboBox()

                self.symmetry_checkbox = QtWidgets.QCheckBox("Symétriser le profil")

                self.rotation_label = QtWidgets.QLabel("Rotation du profil (°) :")
                self.rotation_input = QtWidgets.QLineEdit()
                self.rotation_input.setPlaceholderText("0.0")

                self.offset_x_label = QtWidgets.QLabel("Décalage X (mm) :")
                self.offset_x_input = QtWidgets.QLineEdit()
                self.offset_x_input.setPlaceholderText("0.0")

                self.offset_y_label = QtWidgets.QLabel("Décalage Y (mm) :")
                self.offset_y_input = QtWidgets.QLineEdit()
                self.offset_y_input.setPlaceholderText("0.0")

                self.edges_label = QtWidgets.QLabel("<b>Trajectoire (Arêtes / Lignes sélectionnées) :</b>")
                
                self.edges_list = QtWidgets.QListWidget()

                self.buttons_layout = QtWidgets.QHBoxLayout()
                self.btn_add_edge = QtWidgets.QPushButton("Ajouter la sélection")
                self.btn_clear_edges = QtWidgets.QPushButton("Vider la liste")
                self.buttons_layout.addWidget(self.btn_add_edge)
                self.buttons_layout.addWidget(self.btn_clear_edges)
                self.btn_refresh = QtWidgets.QPushButton("Rafraîchir")

                self.layout.addWidget(self.family_label)
                self.layout.addWidget(self.family_combo)
                self.layout.addWidget(self.profil_label)
                self.layout.addWidget(self.profil_combo)
                self.layout.addSpacing(10)
                self.layout.addWidget(self.symmetry_checkbox)
                self.layout.addSpacing(10)
                self.layout.addWidget(self.rotation_label)
                self.layout.addWidget(self.rotation_input)
                self.layout.addWidget(self.offset_x_label)
                self.layout.addWidget(self.offset_x_input)
                self.layout.addWidget(self.offset_y_label)
                self.layout.addWidget(self.offset_y_input)
                self.layout.addSpacing(15)
                self.layout.addWidget(self.edges_label)
                self.layout.addWidget(self.edges_list)
                self.layout.addLayout(self.buttons_layout)
                self.layout.addWidget(self.btn_refresh)

                # Connexions des signaux
                self.family_combo.currentIndexChanged.connect(self.update_profiles)
                self.btn_add_edge.clicked.connect(self.add_selected_edges)
                self.btn_clear_edges.clicked.connect(self.clear_edges)
                self.btn_refresh.clicked.connect(self.update_preview)

                # Initialiser les familles
                self.load_families()

            def load_families(self):

                self.family_combo.clear()

                if not os.path.exists(PROFILE_DIR):
                    App.Console.PrintError("Dossier profiles introuvable\n")
                    return

                families = [
                    f for f in os.listdir(PROFILE_DIR)
                    if os.path.isdir(os.path.join(PROFILE_DIR, f))
                ]

                self.family_combo.addItems(families)

                if families:
                    self.update_profiles()

            def update_profiles(self):

                self.profil_combo.clear()

                family = self.family_combo.currentText()
                path = os.path.join(PROFILE_DIR, family)

                if not os.path.exists(path):
                    return

                profiles = [
                    os.path.splitext(f)[0]
                    for f in os.listdir(path)
                    if f.lower().endswith(".fcstd")
                ]

                self.profil_combo.addItems(profiles)

            # =================================================
            # GET SELECTED EDGES
            # =================================================
            def add_selected_edges(self):
                """Récupère les arêtes sélectionnées dans l'écran 3D de FreeCAD et les ajoute à la liste"""
                selection = Gui.Selection.getSelectionEx()
                if not selection:
                    self.edges_label.setText("<font color='red'><b>Aucune sélection dans la vue 3D !</b></font>")
                    return

                for sel in selection:
                    obj = sel.Object
                    
                    # Cas 1 : L'utilisateur a sélectionné des arêtes spécifiques (SubObjects)
                    if sel.HasSubObjects:
                        for sub_obj, sub_name in zip(sel.SubObjects, sel.SubElementNames):
                            if isinstance(sub_obj, Part.Edge):
                                item_text = f"{obj.Name} : {sub_name}"
                                if not self.edges_list.findItems(item_text, QtCore.Qt.MatchExactly):
                                    self.edges_list.addItem(item_text)
                                    self.selected_edges.append((obj, sub_name))
                    else:
                        # Cas 2 : L'utilisateur a sélectionné un objet filaire complet (ex: une ligne seule)
                        if hasattr(obj, "Shape") and obj.Shape.ShapeType == "Edge":
                            item_text = f"{obj.Name} (Objet Complet)"
                            if not self.edges_list.findItems(item_text, QtCore.Qt.MatchExactly):
                                self.edges_list.addItem(item_text)
                                self.selected_edges.append((obj, ""))
                            
                self.edges_label.setText("<b>Trajectoire (Arêtes / Lignes sélectionnées) :</b>")
                self.update_preview()

            def clear_edges(self):
                """Vide la liste des trajectoires"""
                self.edges_list.clear()
                self.selected_edges = []
                self.edges_label.setText("<b>Trajectoire (Arêtes / Lignes sélectionnées) :</b>")
                self.update_preview()
                
            def clear_preview_objects(self):
                doc = App.activeDocument()
                
                for obj_list in [self.body, self.shapebinder, self.sketch, self.additivepipe]:
                    for obj in obj_list:
                        try:
                            doc.removeObject(obj.Name)
                        except:
                            pass

                self.body.clear()
                self.shapebinder.clear()
                self.sketch.clear()
                self.additivepipe.clear()

            def update_preview(self):
                doc = App.activeDocument()
                if not doc:
                    App.Console.PrintError("Aucun document actif\n")
                    return

                # 🔥 nettoyage propre
                self.clear_preview_objects()

                if not self.selected_edges:
                    return

                try:
                    rotation = float(self.rotation_input.text() or 0)
                    offset_x = float(self.offset_x_input.text() or 0)
                    offset_y = float(self.offset_y_input.text() or 0)

                    angle = 180 if self.symmetry_checkbox.isChecked() else 0

                    # 🔥 ouvrir UNE SEULE FOIS
                    src_path = os.path.join(
                        PROFILE_DIR,
                        self.family_combo.currentText(),
                        self.profil_combo.currentText() + ".FCStd"
                    )

                    if not os.path.exists(src_path):
                        App.Console.PrintError("Profil introuvable\n")
                        return

                    src_doc = App.open(src_path)

                    if not src_doc.Objects:
                        App.Console.PrintError("Profil vide\n")
                        return

                    profil = src_doc.Objects[0]

                    for i, (obj, sub_name) in enumerate(self.selected_edges):

                        # Body
                        body = doc.addObject("PartDesign::Body", f"Body_{i}")
                        self.body.append(body)

                        # ShapeBinder
                        sb = body.newObject('PartDesign::ShapeBinder', f"ShapeBinder_{i}")
                        sb.Support = [(obj, (sub_name,))] if sub_name else [(obj, ())]
                        sb.Visibility = False
                        self.shapebinder.append(sb)
                        doc.recompute()

                        # Sketch (copie profil)
                        sk = doc.copyObject(profil)
                        body.addObject(sk)
                        sk.AttachmentSupport = [(sb, 'Edge1')]
                        sk.MapMode = 'NormalToEdge'
                        sk.AttachmentOffset = App.Placement(App.Vector(offset_x, offset_y, 0), App.Rotation(rotation, 0, angle))
                        sk.Visibility = False
                        self.sketch.append(sk)

                        # Sweep
                        pipe = body.newObject('PartDesign::AdditivePipe', f"Pipe_{i}")
                        pipe.Profile = sk
                        pipe.Spine = (sb, 'Edge1')
                        pipe.ViewObject.Transparency = 80  # 🔥 preview propre
                        self.additivepipe.append(pipe)

                    # 🔥 fermer UNE SEULE FOIS
                    App.closeDocument(src_doc.Name)

                    # 🔥 UN SEUL recompute
                    doc.recompute()

                except Exception as e:
                    App.Console.PrintError(f"Erreur : {e}\n")

            def accept(self):
                for pipe in self.additivepipe:
                    pipe.ViewObject.Transparency = 0
                return True

            def reject(self):
                self.clear_preview_objects()
                App.Console.PrintMessage("Opération annulée.\n")
                return True


        # =====================================================
        # LAUNCH UI
        # =====================================================
        panel = ProfileSweepTaskPanel()
        Gui.Control.showDialog(panel)
