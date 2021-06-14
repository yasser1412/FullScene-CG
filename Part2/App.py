# pyqt5 imports
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir

# vtk imports
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# other imports
import os
import sys


class volRender(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Loading GUI
        self.ui = uic.loadUi('Part2\RenderGUI.ui', self)
        self.filenames = []
        self.RGB_color = [255.0, 127.5, 76.5, 255]  # RGB, opacity
        self.iso_value = self.iso_slider.value() #iso value
        self.G_opacity = self.GradientOpacity_slider.value()/100 # GradientOpacity Value
        self.S_opacity = self.ScalarOpacity_slider.value()/100  #ScalarOpacity Value

        # Connection of sliders
        self.iso_slider.valueChanged.connect(lambda: self.update_surface_model())
        self.GradientOpacity_slider.valueChanged.connect(
            lambda: self.update_opacity())
        self.ScalarOpacity_slider.valueChanged.connect(
            lambda: self.update_opacity())

        # Connection of buttons
        self.browse_button.clicked.connect(lambda: self.browse())
        self.show_button.clicked.connect(lambda: self.show_model())
        self.colors_button.clicked.connect(lambda: self.color_ray_model())

        # vtk
        self.surfaceExtractor = vtk.vtkContourFilter()
        self.skinMapper = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeProperty = vtk.vtkVolumeProperty()

        # Create the renderer, the render window, and the interactor. The renderer
        # draws into the render window, the interactor enables mouse- and
        # keyboard-based interaction with the scene.
        self.iren = QVTKRenderWindowInteractor()
        self.iren.Initialize()
        self.iren.Start()
        self.ren = vtk.vtkRenderer()
        self.iren.GetRenderWindow().AddRenderer(self.ren)
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    def browse(self):
        self.warning_msg_generator(
            "Check your data", "Select the folder that contains all ur data files in (dcm) type.")
        self.dataDir = QtWidgets.QFileDialog.getExistingDirectory(
            directory=QDir.currentPath())

        if self.dataDir:
            self.load_label.setText(str(self.dataDir))
            self.filenames.clear()
            # Load all files in that folder into self.filenames list
            _, _, self.filenames = next(os.walk(self.dataDir))
            self.read_DCM()
        else:
            self.warning_msg_generator(
                "No data found!", "Please click browse button again and choose correct data directory.")

    def read_DCM(self):
        if len(self.filenames) > 1:
            # The reader is used to read a series of 2D slices (images) that compose the volume.
            self.DICOM_reader = vtk.vtkDICOMImageReader()
            self.DICOM_reader.SetDirectoryName(self.dataDir)

    def show_model(self):
        if self.renMode_CB.currentIndex() == 0:
            # Disabling unnecessary sliders and buttons
            self.iso_slider.setEnabled(False)
            self.ScalarOpacity_slider.setEnabled(True)
            self.GradientOpacity_slider.setEnabled(True)
            self.colors_button.setEnabled(True)
            
            self.ray_casting()
        else:
            # Disabling unnecessary sliders and buttons
            self.iso_slider.setEnabled(True)
            self.ScalarOpacity_slider.setEnabled(False)
            self.GradientOpacity_slider.setEnabled(False)
            self.colors_button.setEnabled(False)
            
            self.surface_render()

    def surface_render(self):
        #Clear the view
        self.ren.RemoveAllViewProps()
        self.surfaceExtractor.SetInputConnection(self.DICOM_reader.GetOutputPort())
        self.surfaceExtractor.SetValue(0, self.iso_slider.value())
        surfaceNormals = vtk.vtkPolyDataNormals()
        surfaceNormals.SetInputConnection(
            self.surfaceExtractor.GetOutputPort())
        surfaceNormals.SetFeatureAngle(60.0)
        surfaceMapper = vtk.vtkPolyDataMapper()
        surfaceMapper.SetInputConnection(surfaceNormals.GetOutputPort())
        surfaceMapper.ScalarVisibilityOff()
        surface = vtk.vtkActor()
        surface.SetMapper(surfaceMapper)

        vol = vtk.vtkVolume()
        vol.SetMapper(self.skinMapper)
        self.center = vol.GetCenter()

        self.adjust_camera()  # adjust camera position according to vol.Center

        self.ren.AddActor(surface)
        self.ren.ResetCamera()
        self.ren.SetBackground(0, 0, 0)
        self.ren.ResetCameraClippingRange()

        # Interact with the data.
        self.iren.Initialize()
        self.ren.Render()
        self.iren.Start()
        self.iren.show()

    def ray_casting(self):

        # The volume will be displayed by ray-cast alpha compositing.
        # A ray-cast mapper (self.skinMapper) is needed to do the ray-casting, and a
        # compositing function is needed to do the compositing along the ray.

        self.ren.RemoveAllViewProps()
        self.skinMapper.SetInputConnection(self.DICOM_reader.GetOutputPort())
        self.skinMapper.SetBlendModeToComposite()

        # color_TF() maps voxel intensities to colors.
        self.color_TF()

        # The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
        # and orientation of the volume in world coordinates.
        vol = vtk.vtkVolume()
        vol.SetMapper(self.skinMapper)
        vol.SetProperty(self.volumeProperty)

        # Add the volume to the renderer
        self.ren.AddViewProp(vol)

        self.center = vol.GetCenter()
        self.adjust_camera()  # adjust camera position according to vol.Center coordinates

        # Interact with the data
        self.iren.Initialize()
        self.ren.Render()
        self.iren.Start()
        self.iren.show()

    def color_TF(self):
        '''The color transfer function maps voxel intensities to colors. '''
        
        # The goal is to one color for flesh (between 500 and 1000)
        # and another color for bone (1150 and over).
        volumeColor = vtk.vtkColorTransferFunction()
        volumeColor.AddRGBPoint(0,    0.0, 0.0, 0.0)
        volumeColor.AddRGBPoint(
            500,  self.RGB_color[0]/255, self.RGB_color[1]/255, self.RGB_color[2]/255)
        volumeColor.AddRGBPoint(
            1000,  self.RGB_color[0]/255, self.RGB_color[1]/255, self.RGB_color[2]/255)
        volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

        # The opacity transfer function is used to control the opacity of different tissue types.
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        volumeScalarOpacity.AddPoint(0,    0.00)
        volumeScalarOpacity.AddPoint(500,  self.S_opacity)
        volumeScalarOpacity.AddPoint(1000, self.S_opacity)
        volumeScalarOpacity.AddPoint(1150, 0.85)
        
        # The gradient opacity function is used to decrease the opacity
        # in the "flat" regions of the volume while maintaining the opacity
        # at the boundaries between tissue types.  The gradient is measured
        # as the amount by which the intensity changes over unit distance.
        # For most medical data, the unit distance is 1mm.
        volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        volumeGradientOpacity.AddPoint(0,   0.0)
        volumeGradientOpacity.AddPoint(90,  1 - self.G_opacity)
        volumeGradientOpacity.AddPoint(100, self.G_opacity)
        
        # The VolumeProperty attaches the color and opacity functions to the
        # volume, and sets other volume properties.
        self.volumeProperty.SetColor(volumeColor)
        self.volumeProperty.SetScalarOpacity(volumeScalarOpacity)
        self.volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        #The interpolation is set to linear to do a high-quality rendering
        self.volumeProperty.SetInterpolationTypeToLinear() 
        #The ShadeOn option turns on directional lighting to enhance the appearance of the volume and make it look more "3D".
        self.volumeProperty.ShadeOn() 
        #To increase the impact of shading, decrease the Ambient and increase the Diffuse and Specular.
        self.volumeProperty.SetAmbient(0.4)
        self.volumeProperty.SetDiffuse(0.6)
        self.volumeProperty.SetSpecular(0.2)
        self.volumeProperty.SetInterpolationTypeToLinear()

    def adjust_camera(self):
        camera = self.ren.GetActiveCamera()
        camera.SetFocalPoint(self.center[0], self.center[1], self.center[2])
        camera.SetPosition(self.center[0], self.center[1]+900, self.center[2])
        camera.SetViewUp(0, 0, -1)

    def color_ray_model(self):
        # Select any color then update the view
        self.RGB_color = QtWidgets.QColorDialog.getColor()
        self.RGB_color = self.RGB_color.getRgb()
        self.ray_casting()

    def update_opacity(self):
        # Get updated slider values and update the view
        self.G_opacity = self.GradientOpacity_slider.value()/100
        self.S_opacity = self.ScalarOpacity_slider.value()/100
        self.ScalarOpacity_val.setText(str(self.S_opacity))
        self.GradientOpacity_val.setText(str(self.G_opacity))
        self.ray_casting()

    def update_surface_model(self):
        self.iso_value = self.iso_slider.value()
        self.surfaceExtractor.SetValue(0, self.iso_value)
        # Update the model with latest slider value (ISO value)
        self.iren.update()

    def warning_msg_generator(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        return msg.exec_()


def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("CUFE")
    app.setOrganizationDomain("CUFEDomain")
    app.setApplicationName("Volume Rendering")
    application = volRender()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
