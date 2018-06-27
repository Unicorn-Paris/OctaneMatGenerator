# Creat Octane Material from file folder by texture name
 
import c4d, os
from c4d import gui
 
# Unique id numbers for each of the GUI elements

# Labels 1
LBL_INFO1 = 1000
LBL_INFO2 = 1001
LBL_INFO3 = 1002
LBL_INFO4 = 1003
LBL_INFO5 = 1004
LBL_INFO6 = 1005
LBL_INFO7 = 1006
LBL_INFO8 = 1007

# Groups 2
GR_MAIN = 2001
GR_FOLDER_ADRESS = 2002

GR_FLUSH = 2003
GR_TEXDEF_L = 2004
GR_TEXDEF_R = 2005

GR_LOAD_BTN = 2006

GR_DDM = 2007

GR_IN_FLUSH = 2008

GR_TEXDEF = 2009

#Edit fields 3
FOLDER_ADRESS = 10001
INDEX = 10003

DIFFUSE_FIELD = 10010
SPECULAR_FIELD = 10011
ROUGHNESS_FIELD = 10012
BUMP_FIELD = 10013
NORMAL_FIELD = 10014

DSPLACEMENT_FIELD = 10020
OPACITY_FIELD = 10021
INDEX_FIELD = 10022
EMISSION_FIELD = 10023
MEDIUM_FIELD = 10024

# Buttons 4
BTN_OK = 20001
BTN_CANCEL = 20002
BTN_COMA = 20003
BTN_LOAD = 20004

# Drop down menu 5
DDM_MATTYPE = 30040


# Octane Plugin ID
ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_CREATE_GLOSSYMAT_PLUGIN = 1033893
ID_OCTANE_IMAGE_TEXTURE = 1029508
ID_OCTANE_DISPLACEMENT = 1031901
ID_OCTANE_TRANSFORM = 1030961
ID_OCTANE_PROJECTION = 1031460

def make_shader(diffuse, specular, roughness, normal, bump, opacity, displacement, name):
    print('shader name: {}'.format(name))
    doc = c4d.documents.GetActiveDocument()
    mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

    #DEFINE MATERIAL TYPE
    mat[c4d.OCT_MATERIAL_TYPE] = 2511
    mat[c4d.ID_BASELIST_NAME] = name 
    
    # TRANSFORM NODE
    TransN = c4d.BaseShader(ID_OCTANE_TRANSFORM)
    mat.InsertShader(TransN)
    
    # PROJECTION NODE
    ProjN = c4d.BaseShader(ID_OCTANE_PROJECTION)
    mat.InsertShader(ProjN)
    
    # DIFFUSE SETUP
    if diffuse :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = IT
        # DIFFUSE IMAGE NAMES = Albedo/Col/Color
        IT[c4d.IMAGETEXTURE_FILE] = diffuse
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN        

    # SPECULAR SETUP
    if specular :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_SPECULAR_LINK] = IT
        # SPECULAR IMAGE NAMES = Specular/Gloss
        IT[c4d.IMAGETEXTURE_FILE] = specular
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

    # ROUGHNESS SETUP
    if roughness :
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_ROUGHNESS_LINK] = IT
        # ROUGHNESS IMAGE NAMES = Roughness/
        IT[c4d.IMAGETEXTURE_FILE] = roughness
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # NORMAL SETUP
    if normal:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_NORMAL_LINK] = IT
        # NORMAL IMAGE NAMES = Normal/NRM
        IT[c4d.IMAGETEXTURE_FILE] = normal
        IT[c4d.IMAGETEXTURE_MODE] = 0
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
        
    else :
        if bump:
            IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
            mat.InsertShader(IT)
            mat[c4d.OCT_MATERIAL_BUMP_LINK] = IT
            # NORMAL IMAGE NAMES = BUMP
            IT[c4d.IMAGETEXTURE_FILE] = bump
            IT[c4d.IMAGETEXTURE_MODE] = 1
            IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
            IT[c4d.IMAGETEX_BORDER_MODE] = 0
            
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
            # TRANSFORM
            IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # OPACITY SETUP
    if opacity:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        mat[c4d.OCT_MATERIAL_OPACITY_LINK] = IT
        # OPACITY IMAGE NAMES = ALPHA/OPACITY/TRANSPARENCY
        IT[c4d.IMAGETEXTURE_FILE] = opacity
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN

    # DISPLACEMENT SETUP
    if displacement:
        IT = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
        mat.InsertShader(IT)
        DISP = c4d.BaseShader(ID_OCTANE_DISPLACEMENT)
        mat.InsertShader(DISP)
        
        DISP[c4d.DISPLACEMENT_INPUT] = IT
        DISP[c4d.DISPLACEMENT_AMOUNT] = 5
        DISP[c4d.DISPLACEMENT_MID] = 0.5
        DISP[c4d.DISPLACEMENT_LEVELOFDETAIL] = c4d.DISPLACEMENT_RES_8192
        
        # DISPACEMENT IMAGE NAMES = DISPACEMENT/DEPTH/HEIGHT
        IT[c4d.IMAGETEXTURE_FILE] = displacement
        IT[c4d.IMAGETEXTURE_MODE] = 1
        IT[c4d.IMAGETEXTURE_GAMMA] = 2.2
        IT[c4d.IMAGETEX_BORDER_MODE] = 0
        
        mat[c4d.OCT_MATERIAL_DISPLACEMENT_LINK] = DISP
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_TRANSFORM_LINK] = TransN
        
        # TRANSFORM
        IT[c4d.IMAGETEXTURE_PROJECTION_LINK] = ProjN
    
    # INDEX SETUP    
    mat[c4d.OCT_MATERIAL_INDEX] = 1.33    
    doc.InsertMaterial(mat)
    
def UpdateLayout (self, diffuse, specular, roughness, normal, bump, opacity, displacement):
      

      #Texture Liste
      self.LayoutFlushGroup(id=GR_FLUSH)
      self.GroupBorder(c4d.BORDER_GROUP_IN)
      self.GroupBorderSpace(10, 0, 10, 0)

      self.GroupBegin(GR_IN_FLUSH, c4d.BFH_SCALEFIT,1,2)

      # DROP DOWN MATERIAL TYPE
        #STYLE    
      self.GroupBegin(GR_DDM, c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT, 2, 1,)
      self.GroupBorder(c4d.BORDER_NONE)
      self.GroupBorderSpace(10, 5, 10, 10)
    
        #CONTENT
      self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT|c4d.BFV_TOP, name='Material Type')
      self.AddComboBox(DDM_MATTYPE, c4d.BFH_LEFT, initw = 80)
            #ComboBox CONTENT
      self.AddChild(DDM_MATTYPE, 0, 'Diffuse')
      self.AddChild(DDM_MATTYPE, 1, 'Glossy')
      self.AddChild(DDM_MATTYPE, 2, 'Specular')
    
      self.GroupEnd()

      self.GroupBegin(GR_TEXDEF, c4d.BFH_SCALEFIT)

    #GR_L
      self.GroupBegin(GR_TEXDEF_L, c4d.BFH_LEFT, 2,5)
      self.GroupBorderSpace(10, 5, 10, 5)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Diffuse :')
      self.editText = self.AddEditText(DIFFUSE_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(DIFFUSE_FIELD,diffuse)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Specular :')
      self.editText = self.AddEditText(SPECULAR_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(SPECULAR_FIELD,specular)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Roughness :')
      self.editText = self.AddEditText(ROUGHNESS_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(ROUGHNESS_FIELD,roughness)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Bump :')
      self.editText = self.AddEditText(BUMP_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(BUMP_FIELD,bump)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Normal :')
      self.editText = self.AddEditText(NORMAL_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(NORMAL_FIELD,normal)

      self.GroupEnd()

    #GR_R
      self.GroupBegin(GR_TEXDEF_R, c4d.BFH_RIGHT, 2,5)
      self.GroupBorderSpace(10, 5, 10, 5)


      self.AddStaticText(1006,c4d.BFH_LEFT, name='Displacement :')
      self.editText = self.AddEditText(DSPLACEMENT_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(DSPLACEMENT_FIELD,displacement)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Opacity :')
      self.editText = self.AddEditText(OPACITY_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      self.SetString(OPACITY_FIELD,opacity)

      ######
      self.AddStaticText(1006,c4d.BFH_LEFT, name='Index :')
      self.AddEditSlider(INDEX_FIELD,c4d.BFH_SCALEFIT,80,0)
      self.SetFloat(INDEX_FIELD, 1.33, min = 1, max = 8, step=0.001, format=c4d.FORMAT_FLOAT )

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Emission :')
      self.editText = self.AddEditText(EMISSION_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      # self.SetString(EMISSION_FIELD,emission)

      self.AddStaticText(1006,c4d.BFH_LEFT, name='Medium :')
      self.editText = self.AddEditText(MEDIUM_FIELD, c4d.BFH_SCALEFIT, initw = 300)
      # self.SetString(MEDIUM_FIELD,medium)

      self.GroupEnd()

      self.GroupEnd()

      self.LayoutChanged(id=GR_FLUSH)            
      return True
 
# Dialog for renaming objects
class OptionsDialog(gui.GeDialog):
      
  def CreateLayout(self):
    id == 0
    self.SetTitle('THE OCTANE MAT MAKER')
    
    # MEGA GROUP BEGIN------------------------------------------------------------------------------------------
    self.GroupBegin(GR_MAIN, c4d.BFH_SCALEFIT, 1,2)
    self.GroupBorderNoTitle(c4d.BORDER_NONE)
    self.GroupBorderSpace(10, 10, 10, 10)
    
    # TITLE
    
    self.AddSeparatorH(130 ,c4d.BFH_CENTER)
    self.AddStaticText(LBL_INFO3, c4d.BFH_CENTER, name='Material Type', borderstyle = c4d.BORDER_WITH_TITLE_BOLD)
    self.AddSeparatorH(130 ,c4d.BFH_CENTER,)
    
    # DROP DOWN MATERIAL TYPE
        #STYLE    
    #self.GroupBegin(GROUP_OPTIONS, c4d.BFV_SCALEFIT|c4d.BFH_SCALEFIT, 2, 2,title="Material Setup" ,)
    #self.GroupBorder(c4d.BORDER_GROUP_IN)
    #self.GroupBorderSpace(10, 10, 10, 10)
    #
        #CONTENT
    #self.AddStaticText(LBL_INFO2, c4d.BFH_LEFT|c4d.BFV_TOP, name='Material Type')
    #self.AddComboBox(DDM_MATTYPE, c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT, initw = 80)
            #ComboBox CONTENT
    #self.AddChild(DDM_MATTYPE, 0, 'Diffuse')
    #self.AddChild(DDM_MATTYPE, 1, 'Glossy')
    #self.AddChild(DDM_MATTYPE, 2, 'Specular')
    
   
    #
    #self.GroupEnd()
    #
    
    
    # FOLDER SELECTION
    self.GroupBegin(GR_FOLDER_ADRESS, c4d.BFH_SCALEFIT|c4d.BFV_BOTTOM , 3, 1)
    self.GroupBorderSpace(0, 10, 0, 5)
    self.AddStaticText(LBL_INFO1, c4d.BFH_LEFT, name='Folder') 
    self.editText = self.AddEditText(FOLDER_ADRESS, c4d.BFH_SCALEFIT)
    self.AddButton(BTN_COMA, c4d.BFH_RIGHT, name='...')
    self.GroupEnd()
    
    #GroupVide
    self.GroupBegin(GR_FLUSH,c4d.BFH_SCALEFIT,2,1,title='Texture selection')
    #self.GroupBorder(c4d.BORDER_NONE)
    #self.GroupBorderSpace(10, 0, 10, 0)

    self.GroupEnd()
    #GroupeVide End
    
    self.GroupBegin(GR_LOAD_BTN, c4d.BFH_CENTER, 3, 1)
    self.GroupBorderSpace(0, 5, 0, 5)
    self.AddButton(BTN_LOAD, c4d.BFH_LEFT, name='Load')
    self.AddButton(BTN_OK, c4d.BFH_CENTER, name='Load & Creat Mat')
    self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name='Cancel')
    self.GroupEnd()
    
#MEGA GROUP END$------------------------------------------------------------------------------
    self.GroupEnd()

    self.images = None
    self.file_path = None
    
    self.ok = False
    return True
 
  # React to user's input:
  def Command(self, id, msg):
    #print id 
    #print msg
    
    if id == DDM_MATTYPE:
        self.UpdateLayout(self.GetLong(DDM_MATTYPE))
        #print dir(msg)
        #print msg.GetData()
        self.GetLong(DDM_MATTYPE)
        if self.GetLong(30040) == 0:
            print 'Diffuse'
        if self.GetLong(30040) == 1:
            print 'Glossy'
        if self.GetLong(30040) == 2:
            gui.MessageDialog('OctaneMatGenerator doesn`t support specular material yet :)')
            self.SetLong(30040, 0)
            self.UpdateLayout(0)
            print 'Specular'
        
            
    
    if id == BTN_CANCEL:
      print '{}'.format(self.file_path)
      self.Close()
    elif id == BTN_OK:
    
      diffuse = None
      specular = None
      roughness = None
      normal = None
      bump = None
      opacity = None
      displacement = None
      
      if (self.file_path is None):
        self.file_path = self.GetString(FOLDER_ADRESS)
          
      if not os.path.exists(self.file_path):
        gui.MessageDialog('The system cannot find the path specified')
        return
          
      self.images = os.listdir(self.file_path)
      
      for filename in list(map(lambda j: j.lower(), self.images)):
        lowered_filename = filename.lower()
        absolute_filename = os.path.join(self.file_path, filename)
        if 'diffuse' in lowered_filename or 'color' in lowered_filename or 'col' in lowered_filename or 'albedo' in lowered_filename:
          diffuse = absolute_filename
        if 'specular' in lowered_filename or 'gloss' in lowered_filename:
          specular = absolute_filename
        if 'roughness' in lowered_filename:
          roughness = absolute_filename
        if 'normal' in lowered_filename or 'nrm' in lowered_filename:
          normal = absolute_filename
        if 'bump' in lowered_filename:
          bump = absolute_filename
        if 'opacity' in lowered_filename or 'alpha' in lowered_filename:
          opacity = absolute_filename
        if 'displacement' in lowered_filename or 'disp' in lowered_filename or 'depth' in lowered_filename:
          displacement = absolute_filename

      
      make_shader(diffuse, specular, roughness, normal, bump, opacity, displacement, os.path.basename(self.file_path))    
      c4d.EventAdd()    
      
      self.Close()
    
    elif id==BTN_LOAD:
        
        diffuse = None
        specular = None
        roughness = None
        normal = None
        bump = None
        opacity = None
        displacement = None
      
        if (self.file_path is None):
          self.file_path = self.GetString(FOLDER_ADRESS)
          
        if not os.path.exists(self.file_path):
          gui.MessageDialog('The system cannot find the path specified')
          return
          
        self.images = os.listdir(self.file_path)
        
        for filename in self.images:
            lowered_filename = filename.lower()
            if 'diffuse' in lowered_filename or 'color' in lowered_filename or 'col' in lowered_filename or 'albedo' in lowered_filename:
              diffuse = filename
            if 'specular' in lowered_filename or 'gloss' in lowered_filename:
              specular = filename
            if 'roughness' in lowered_filename:
              roughness = filename
            if 'normal' in lowered_filename or 'nrm' in lowered_filename:
              normal = filename
            if 'bump' in lowered_filename:
              bump = filename
            if 'opacity' in lowered_filename or 'alpha' in lowered_filename:
              opacity = filename
            if 'displacement' in lowered_filename or 'disp' in lowered_filename or 'depth' in lowered_filename:
              displacement = filename
      
      
        UpdateLayout (self, diffuse, specular, roughness, normal, bump, opacity, displacement)

        
    
    elif id==BTN_COMA:
      self.ok = True
      self.file_path = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) and c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY) or ''
      print self.file_path
      self.SetString(FOLDER_ADRESS,self.file_path)

     
    return True
 
#This is where the action happens
def main():

  dlg = OptionsDialog()
  
 
  # Open the options dialogue to let users choose their options.  
  dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=400, defaulth=10)
  if not dlg.ok:
    return
 
  c4d.EventAdd()  # Update C4D to see changes.
 
if __name__=='__main__':
  main()