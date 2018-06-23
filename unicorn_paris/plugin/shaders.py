class OctaneShader():

    def __init__(self):
        self.diffuse = None
        self.specular = None
        self.roughness = None
        self.normal = None
        self.bump = None
        self.opacity = None
        self.displacement = None

    def generate(self):
        self.doc = c4d.documents.GetActiveDocument()
        self.mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

        # Define material type.
        self.mat()[c4d.OCT_MATERIAL_TYPE] = OCT_MATERIAL_TYPE

        # Create and insert transform node and projection node.
        self.tnode = c4d.BaseShader(ID_OCTANE_TRANSFORM)
        self.pnode = c4d.BaseShader(ID_OCTANE_PROJECTION)
        mat.InsertShader(self.tnode)
        mat.InsertShader(self.pnode)

        # Setup diffuse, specular, roughness, normal.
        self._diffuse()
        self._specular()
        self._roughness()
        self._normal()

    def _diffuse(self):
        pass

    def _specular(self):
        pass

    def _roughness(self):
        pass

    def _normal(self):
        pass
