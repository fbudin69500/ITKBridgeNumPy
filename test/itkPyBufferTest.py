#==========================================================================
#
#   Copyright Insight Software Consortium
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0.txt
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#==========================================================================*/
from __future__ import print_function
import sys
import unittest
import datetime as dt

import itk
import numpy as np

class TestNumpyITKMemoryviewInterface(unittest.TestCase):
    """ This tests numpy array <-> ITK Scalar Image conversion. """

    def setUp(self):
        pass

    def test_NumPyBridge_itkScalarImage(self):
        "Try to convert all pixel types to NumPy array view"

        Dimension             = 3
        ScalarImageType       = itk.Image[itk.UC, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        region.SetSize(0, 30);
        region.SetSize(1, 20);
        region.SetSize(2, 10);

        scalarImage           = ScalarImageType.New()
        scalarImage.SetRegions(region);
        scalarImage.Allocate();

        scalarndarr           = itk.PyBuffer[ScalarImageType].GetArrayFromImage(scalarImage)
        convertedscalarImage  = itk.PyBuffer[ScalarImageType].GetImageFromArray(scalarndarr)

        ScalarDiffFilterType  = itk.ComparisonImageFilter[ScalarImageType, ScalarImageType]
        ScalarDiffFilter      = ScalarDiffFilterType.New()
        ScalarDiffFilter.SetValidInput(scalarImage)
        ScalarDiffFilter.SetTestInput(convertedscalarImage)

        ScalarDiffFilter.Update()
        diff = ScalarDiffFilter.GetTotalDifference()

        self.assertEqual(0, diff)

    def test_TransposeNumPyBridge_itkScalarImage(self):
        "Try to convert all pixel types to NumPy array view, transpose it, and convert it back"

        Dimension             = 2
        ScalarImageType       = itk.Image[itk.UC, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        size                  = itk.Size[2]()
        size[0]               = 30
        size[1]               = 20
        region.SetSize(size);

        scalarImage           = ScalarImageType.New()
        scalarImage.SetRegions(region);
        scalarImage.Allocate();

        scalarndarr           = itk.PyBuffer[ScalarImageType].GetArrayFromImage(scalarImage)
        convertedScalarImage  = itk.PyBuffer[ScalarImageType].GetImageFromArray(scalarndarr.transpose())

        transposedImageSize = convertedScalarImage.GetLargestPossibleRegion().GetSize()
        self.assertEqual(transposedImageSize[0], size[1])
        self.assertEqual(transposedImageSize[1], size[0])

    def test_NumPyBridge_itkVectorImage(self):
        "Try to convert all pixel types to NumPy array view"

        Dimension             = 3
        VectorImageType       = itk.VectorImage[itk.UC, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        region.SetSize(0, 30);
        region.SetSize(1, 20);
        region.SetSize(2, 10);

        vectorImage           = VectorImageType.New()
        vectorImage.SetRegions(region);
        vectorImage.SetNumberOfComponentsPerPixel(3);
        vectorImage.Allocate();
        vectorndarr           = itk.PyBuffer[VectorImageType].GetArrayFromImage(vectorImage)

        convertedvectorImage  = itk.PyBuffer[VectorImageType].GetImageFromArray(vectorndarr, isVector=True)

    def test_NumPyBridge_itkRGBImage(self):
        "Try to convert an RGB ITK image to NumPy array view"

        Dimension             = 3
        PixelType             = itk.RGBPixel[itk.UC]
        RGBImageType          = itk.Image[PixelType, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        region.SetSize(0, 30);
        region.SetSize(1, 20);
        region.SetSize(2, 10);

        rgbImage              = RGBImageType.New()
        rgbImage.SetRegions(region);
        rgbImage.Allocate();
        rgbndarr              = itk.PyBuffer[RGBImageType].GetArrayFromImage(rgbImage)

        convertedRGBImage     = itk.PyBuffer[RGBImageType].GetImageFromArray(rgbndarr, isVector=True)

    def test_NumPyBridge_itkRGBAImage(self):
        "Try to convert an RGBA ITK image to NumPy array view"

        Dimension             = 3
        PixelType             = itk.RGBAPixel[itk.UC]
        RGBAImageType         = itk.Image[PixelType, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        region.SetSize(0, 30);
        region.SetSize(1, 20);
        region.SetSize(2, 10);

        rgbaImage             = RGBAImageType.New()
        rgbaImage.SetRegions(region);
        rgbaImage.Allocate();
        rgbandarr             = itk.PyBuffer[RGBAImageType].GetArrayFromImage(rgbaImage)

        convertedRGBAImage    = itk.PyBuffer[RGBAImageType].GetImageFromArray(rgbandarr, isVector=True)

    def test_NumPyBridge_itkVectorPixelImage(self):
        "Try to convert an ITK image with vector pixels to NumPy array view"

        Dimension             = 3
        PixelType             = itk.Vector[itk.F,Dimension]
        VectorImageType       = itk.Image[PixelType, Dimension]
        RegionType            = itk.ImageRegion[Dimension]

        region                = RegionType()
        region.SetSize(0, 30);
        region.SetSize(1, 20);
        region.SetSize(2, 10);

        vectorImage           = VectorImageType.New()
        vectorImage.SetRegions(region);
        vectorImage.Allocate();
        vectorndarr           = itk.PyBuffer[VectorImageType].GetArrayFromImage(vectorImage)

        convertedVectorImage  = itk.PyBuffer[VectorImageType].GetImageFromArray(vectorndarr, isVector=True)

if __name__ == '__main__':
    unittest.main()
